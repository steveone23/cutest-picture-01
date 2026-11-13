"""Copy the bundled picture to the bounty output path."""

import os
import shutil
import sys
from pathlib import Path

MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"

SOURCE = Path(__file__).resolve().parent / "assets" / "entry.png"


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if not SOURCE.is_file():
        fail(f"picture not found: {SOURCE}")

    size = SOURCE.stat().st_size
    if size > MAX_BYTES:
        fail(f"picture is {size} bytes, limit is {MAX_BYTES}")

    with SOURCE.open("rb") as f:
        head = f.read(len(PNG_MAGIC))
    if not (head.startswith(PNG_MAGIC) or head.startswith(JPEG_MAGIC)):
        fail("picture is not a PNG or JPEG file")

    output_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({size} bytes)")


if __name__ == "__main__":
    main()
