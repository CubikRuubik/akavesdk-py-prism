"""Test helpers for generating random data with valid IPFS-style CIDs.

Ported from the Go SDK private/testrand package (tag v0.4.4).
"""

import hashlib
import os
import struct


def generate_block(size: int) -> tuple:
    """Generate a random block of *size* bytes and compute its CIDv1 (raw, sha2-256).

    The CID is encoded as a base32 (lower-case) string prefixed with ``b``, which
    matches the default CIDv1 string representation used by the Go SDK.

    Args:
        size: Number of random bytes to generate.

    Returns:
        ``(data, cid_string)`` where ``data`` is the raw bytes and ``cid_string``
        is the CIDv1 base32 string (e.g. ``"bafkreig..."``).
    """
    data = os.urandom(size)

    digest = hashlib.sha256(data).digest()

    # Multihash encoding: varint(0x12) + varint(0x20) + digest
    # 0x12 = SHA2-256 codec, 0x20 = 32 bytes
    multihash = bytes([0x12, 0x20]) + digest

    # CIDv1: varint(1) version + varint(0x55) raw codec + multihash
    # 0x55 = raw codec
    cid_bytes = bytes([0x01, 0x55]) + multihash

    cid_string = _to_base32_cid(cid_bytes)
    return data, cid_string


def _to_base32_cid(cid_bytes: bytes) -> str:
    """Encode raw CID bytes as a base32 lower-case CIDv1 string (``b`` prefix)."""
    import base64
    # Standard base32 without padding, lower-cased, with ``b`` multibase prefix
    encoded = base64.b32encode(cid_bytes).decode("ascii").rstrip("=").lower()
    return "b" + encoded
