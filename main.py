"""Copy the bundled picture to the bounty output path."""

import os
import shutil
import sys
from pathlib import Path

MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"
MAX_SIDE = 1024
SOF_MARKERS = (0xC0, 0xC1, 0xC2)

SOURCE = Path(__file__).resolve().parent / "assets" / "entry.png"


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def png_size(data: bytes) -> tuple[int, int]:
    # The IHDR chunk always comes first: length, type, width, height.
    if len(data) < 24 or data[12:16] != b"IHDR":
        fail("PNG has no IHDR chunk")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def jpeg_size(data: bytes) -> tuple[int, int]:
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            fail(f"JPEG marker expected at offset {pos}")
        marker = data[pos + 1]
        if marker == 0xFF:
            pos += 1
            continue
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if marker in SOF_MARKERS:
            if pos + 9 > len(data):
                break
            height = int.from_bytes(data[pos + 5:pos + 7], "big")
            width = int.from_bytes(data[pos + 7:pos + 9], "big")
            return width, height
        if marker in (0xD9, 0xDA):
            break
        pos += 2 + int.from_bytes(data[pos + 2:pos + 4], "big")
    fail("JPEG has no SOF0, SOF1 or SOF2 marker")


def main() -> None:
    if not SOURCE.is_file():
        fail(f"picture not found: {SOURCE}")

    size = SOURCE.stat().st_size
    if size > MAX_BYTES:
        fail(f"picture is {size} bytes, limit is {MAX_BYTES}")

    data = SOURCE.read_bytes()
    if data.startswith(PNG_MAGIC):
        width, height = png_size(data)
    elif data.startswith(JPEG_MAGIC):
        width, height = jpeg_size(data)
    else:
        fail("picture is not a PNG or JPEG file")

    print(f"picture is {width}x{height}")
    if width > MAX_SIDE or height > MAX_SIDE:
        fail(f"picture is {width}x{height}, limit is {MAX_SIDE}x{MAX_SIDE}")

    output_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({size} bytes)")


if __name__ == "__main__":
    main()
