#!/usr/bin/env python3
"""Entry point for the news-image-20261125 bounty submission.

Copies the bundled image asset/entry.png to /output/entry.png,
verifying it first: PNG magic bytes, 1024 x 1024 pixels, at most
1 MiB, and a byte-identical re-read after writing.

Standard library only. No network access. No arguments.
Run: python3 main.py
"""

import hashlib
import os
import struct
import sys
import zlib

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "asset", "entry.png")
DST = "/output/entry.png"
MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def png_dimensions(data):
    """Read width/height from the IHDR chunk; raise if malformed."""
    if data[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file (bad magic bytes)")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk where expected")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    if not os.path.isfile(SRC):
        print(f"missing bundled image: {SRC}", file=sys.stderr)
        return 1
    with open(SRC, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        print(f"image is {len(data)} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1
    width, height = png_dimensions(data)
    if (width, height) != (1024, 1024):
        print(f"image is {width}x{height}, expected 1024x1024",
              file=sys.stderr)
        return 1
    # sanity: walk the chunks and decompress the IDAT payloads
    # (catches truncation or corruption in the image data)
    pos = 8
    idat = bytearray()
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        payload = data[pos + 8:pos + 8 + length]
        if len(payload) != length:
            raise ValueError("truncated PNG chunk")
        if ctype == b"IDAT":
            idat.extend(payload)
        if ctype == b"IEND":
            break
        pos += 12 + length
    if not idat:
        raise ValueError("PNG carries no image data (no IDAT chunk)")
    zlib.decompressobj().decompress(bytes(idat))
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(DST, "wb") as fh:
        fh.write(data)
    if sha256_of(DST) != sha256_of(SRC):
        print("output differs from the bundled image", file=sys.stderr)
        return 1
    print(f"wrote {DST} ({len(data)} bytes, 1024x1024, "
          f"sha256 {hashlib.sha256(data).hexdigest()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
