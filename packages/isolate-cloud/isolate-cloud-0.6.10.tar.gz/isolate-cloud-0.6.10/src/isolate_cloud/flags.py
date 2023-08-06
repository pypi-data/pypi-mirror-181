from __future__ import annotations

import os

TEST_MODE = bool(os.getenv("ISOLATE_TEST_MODE", False))
