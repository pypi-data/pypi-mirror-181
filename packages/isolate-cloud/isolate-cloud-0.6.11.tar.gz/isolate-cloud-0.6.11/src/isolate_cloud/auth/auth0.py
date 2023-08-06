from __future__ import annotations

import time

import click
import requests
from auth0.v3.authentication.token_verifier import (
    AsymmetricSignatureVerifier,
    TokenVerifier,
)

AUTH0_DOMAIN = "dev-n2t1kjuo8uh0ddfg.us.auth0.com"
AUTH0_JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
AUTH0_ALGORITHMS = ["RS256"]
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"
AUTH0_FAL_API_AUDIENCE_ID = "fal-cloud"
AUTH0_CLIENT_ID = "TwXR51Vz8JbY8GUUMy6EyuVR0fTO7N4N"
AUTH0_SCOPE = "openid profile email offline_access"


def login() -> dict:
    """
    Runs the device authorization flow and stores the user object in memory
    """
    device_code_payload = {
        "audience": AUTH0_FAL_API_AUDIENCE_ID,
        "client_id": AUTH0_CLIENT_ID,
        "scope": AUTH0_SCOPE,
    }
    device_code_response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/device/code", data=device_code_payload
    )

    if device_code_response.status_code != 200:
        raise click.ClickException("Error generating the device code")

    print("Device code successful")
    device_code_data = device_code_response.json()
    print(
        "1. On your computer or mobile device navigate to: ",
        device_code_data["verification_uri_complete"],
    )
    print("2. Enter the following code: ", device_code_data["user_code"])

    token_payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": device_code_data["device_code"],
        "client_id": AUTH0_CLIENT_ID,
    }

    while True:
        print("Checking if the user completed the flow...")
        token_response = requests.post(
            f"https://{AUTH0_DOMAIN}/oauth/token", data=token_payload
        )

        token_data = token_response.json()
        if token_response.status_code == 200:
            print("Authenticated!")

            validate_id_token(token_data["id_token"])

            return token_data

        elif token_data["error"] not in ("authorization_pending", "slow_down"):
            raise click.ClickException(token_data["error_description"])

        else:
            time.sleep(device_code_data["interval"])


def refresh(token: str) -> dict:
    token_payload = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "refresh_token": token,
    }

    token_response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token", data=token_payload
    )

    token_data = token_response.json()
    if token_response.status_code == 200:
        # DEBUG: print("Authenticated!")

        validate_id_token(token_data["id_token"])

        return token_data
    else:
        raise click.ClickException(token_data["error_description"])


def revoke(token: str):
    token_payload = {
        "client_id": AUTH0_CLIENT_ID,
        "token": token,
    }

    token_response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/revoke", data=token_payload
    )

    if token_response.status_code != 200:
        token_data = token_response.json()
        raise click.ClickException(token_data["error_description"])


def get_user_info(bearer_token: str) -> dict:
    userinfo_response = requests.post(
        f"https://{AUTH0_DOMAIN}/userinfo",
        headers={"Authorization": bearer_token},
    )

    if userinfo_response.status_code != 200:
        raise click.ClickException(userinfo_response.content.decode("utf-8"))

    return userinfo_response.json()


def validate_id_token(token: str):
    """
    Verify the token and its precedence.
    `id_token`s are intended for the client (this sdk) only.
    Never send one to another service.

    :param id_token:
    """
    sv = AsymmetricSignatureVerifier(AUTH0_JWKS_URL)
    tv = TokenVerifier(
        signature_verifier=sv,
        issuer=AUTH0_ISSUER,
        audience=AUTH0_CLIENT_ID,
    )
    tv.verify(token)
