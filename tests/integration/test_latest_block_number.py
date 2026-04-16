# Copyright (C) 2025 Akave
# See LICENSE for copying information.

import os
import pytest

from sdk.config import SDKConfig
from sdk.sdk import SDK

DIAL_URI = os.getenv("DIAL_URI", "")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
IPC_ADDRESS = os.getenv("IPC_ADDRESS", "")


def pick_dial_uri() -> str:
    if not DIAL_URI or DIAL_URI.lower() == "omit":
        pytest.skip("dial uri flag missing, set DIAL_URI environment variable")
    return DIAL_URI


def pick_private_key() -> str:
    if not PRIVATE_KEY or PRIVATE_KEY.lower() == "omit":
        pytest.skip("private key flag missing, set PRIVATE_KEY environment variable")
    return PRIVATE_KEY


@pytest.mark.integration
def test_sdk_latest_block_number():
    """Integration test: SDK-level LatestBlockNumber returns a positive value end-to-end."""
    dial_uri = pick_dial_uri()
    private_key = pick_private_key()

    config = SDKConfig(
        address=dial_uri,
        private_key=private_key,
    )

    sdk = SDK(config)
    try:
        ipc = sdk.ipc()
        block_number = ipc.latest_block_number(ctx=None)
        assert block_number > 0, f"Expected a positive block number, got {block_number}"
    finally:
        sdk.close()
