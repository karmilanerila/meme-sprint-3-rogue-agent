#!/usr/bin/env python3
"""Meme Sprint 3 entry: write the bundled rogue-agent meme to /output/entry.png.

The meme itself is the bundled PNG (entry.png, next to this file). This program
only copies those bytes to the output path, so the artifact is byte-identical
on every run. Standard library only.
"""

import hashlib
import os
import struct
import sys

ASSET_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def check_gate(data: bytes) -> str | None:
    """Return an error string if the bytes fail the competition gate, else None."""
    if len(data) > MAX_BYTES:
        return f"asset too large: {len(data)} bytes > {MAX_BYTES}"
    if not data.startswith(PNG_SIGNATURE):
        return "asset is not a PNG"
    if len(data) < 24:
        return "asset too short to hold a PNG header"
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        return f"asset too big: {width}x{height} > {MAX_DIMENSION}x{MAX_DIMENSION}"
    return None


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ASSET_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, OUTPUT_NAME)

    with open(src, "rb") as f:
        data = f.read()

    error = check_gate(data)
    if error is not None:
        print(f"gate check failed: {error}", file=sys.stderr)
        return 1

    with open(dst, "wb") as f:
        f.write(data)

    width, height = struct.unpack(">II", data[16:24])
    print(
        f"wrote {dst} ({len(data)} bytes, {width}x{height}, "
        f"sha256 {hashlib.sha256(data).hexdigest()})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
