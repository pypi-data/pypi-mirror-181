from __future__ import annotations

import pkgutil
from collections import namedtuple
from dataclasses import dataclass
from typing import Any, ClassVar

import grpc
import isolate_cloud.auth as auth
import isolate_proto
from isolate.backends import BasicCallable
from isolate.backends.remote import IsolateServer, IsolateServerConnection
from isolate.backends.settings import IsolateSettings
from isolate.interface import BoxedEnvironment, RemoteBox
from isolate.server import interface
from isolate.server.definitions import EnvironmentDefinition
from isolate_cloud import flags

MACHINE_TYPES = ["XS", "S", "M", "GPU"]

CloudKeyCredentials = namedtuple("CloudKeyCredentials", ["key_id", "key_secret"])


@dataclass
class HostedRemoteBox(RemoteBox):
    """Run on an hosted isolate server."""

    machine_type: str = "S"
    creds: CloudKeyCredentials | None = None

    def __post_init__(self):
        if self.machine_type not in MACHINE_TYPES:
            raise RuntimeError(
                f"Machine type {self.machine_type} not supported. Use one of: {' '.join(MACHINE_TYPES)}"
            )

    def wrap(
        self,
        definition: dict[str, Any],
        settings: IsolateSettings,
    ) -> BoxedEnvironment:
        definition = definition.copy()

        # Extract the kind of environment to use.
        kind = definition.pop("kind", None)
        assert kind is not None, f"Corrupted definition: {definition}"

        target_list = [{"kind": kind, "configuration": definition}]

        # Create a remote environment.
        return BoxedEnvironment(
            FalHostedServer(
                host=self.host,
                machine_type=self.machine_type,
                target_environments=target_list,
                creds=self.creds,
            ),
            pool_size=self.pool_size,
        )


@dataclass
class FalHostedServer(IsolateServer):
    machine_type: str
    BACKEND_NAME: ClassVar[str] = "hosted-isolate-server"
    creds: CloudKeyCredentials | None = None

    def open_connection(
        self,
        connection_key: list[EnvironmentDefinition],
    ) -> FalHostedServerConnection:
        return FalHostedServerConnection(
            self,
            self.host,
            connection_key,
            machine_type=self.machine_type,
            creds=self.creds,
        )


@dataclass
class FalHostedGrpcConnection:
    host: str
    creds: CloudKeyCredentials | None = None

    def _acquire_channel(self) -> None:
        SECRET_KEY = "auth-key"
        SECRET_ID_KEY = "auth-key-id"

        root_cert = pkgutil.get_data(__name__, "ca.pem")

        class GrpcAuth(grpc.AuthMetadataPlugin):
            def __init__(self, key, value):
                self._key = key
                self._value = value

            def __call__(
                self,
                context: grpc.AuthMetadataContext,
                callback: grpc.AuthMetadataPluginCallback,
            ):
                # Add token to metadata before sending
                callback(((self._key, self._value),), None)

        if flags.TEST_MODE:
            channel_creds = grpc.local_channel_credentials()
        else:
            if self.creds and self.creds.key_secret and self.creds.key_id:
                channel_creds = grpc.composite_channel_credentials(
                    grpc.ssl_channel_credentials(root_cert),
                    grpc.metadata_call_credentials(
                        GrpcAuth(SECRET_KEY, self.creds.key_secret)
                    ),
                    grpc.metadata_call_credentials(
                        GrpcAuth(SECRET_ID_KEY, self.creds.key_id)
                    ),
                )
            else:
                channel_creds = grpc.composite_channel_credentials(
                    # Channel credentials
                    grpc.ssl_channel_credentials(root_cert),
                    # User credentials
                    grpc.access_token_call_credentials(auth.USER.access_token),
                )

        # HACK: Accept 'localhost' in CN of certificate.
        # TODO: Remove once we have a deployed service to accept valid certificates only
        options = (("grpc.ssl_target_name_override", "localhost"),)
        self._channel = grpc.secure_channel(self.host, channel_creds, options)

    def create_user_key(self):
        self._acquire_channel()
        isolate_controller = isolate_proto.IsolateControllerStub(self._channel)
        return isolate_controller.CreateUserKey(isolate_proto.CreateUserKeyRequest())


@dataclass
class FalHostedServerConnection(FalHostedGrpcConnection, IsolateServerConnection):
    machine_type: str = "S"

    def run(
        self,
        executable: BasicCallable,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self._acquire_channel()
        isolate_controller = isolate_proto.IsolateControllerStub(self._channel)

        request = isolate_proto.HostedRun(
            environments=self.definitions,
            machine_requirements=isolate_proto.MachineRequirements(
                machine_type=self.machine_type
            ),
            function=interface.to_serialized_object(
                executable,
                method="dill",
                was_it_raised=False,
            ),
        )

        return_value = []
        for result in isolate_controller.Run(request):
            for raw_log in result.logs:
                log = interface.from_grpc(raw_log)
                self.log(log.message, level=log.level, source=log.source)
            if result.return_value.definition:
                return_value.append(interface.from_grpc(result.return_value))
        return return_value[0]
