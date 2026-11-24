"""Status Report Comedy Sprint entry.

Reads the one-line status report from line.txt and writes it to
/output/entry.txt, byte for byte, after checking it against the gate:
UTF-8 text, 1 to 200 characters, not only white space, a single line.

Set MAKEFUN_OUTPUT_DIR to test locally with a stand-in directory
instead of /output. Standard library only; no network, no randomness,
no timestamps, nothing read from outside this repository.
"""

import os
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
LINE_FILE = REPO_DIR / "line.txt"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUTPUT_FILE = OUTPUT_DIR / "entry.txt"


def load_entry() -> tuple[bytes, str]:
    """Return the entry as (raw bytes, decoded text), or fail loudly."""
    raw = LINE_FILE.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"line.txt is not valid UTF-8: {exc}") from exc
    if not 1 <= len(text) <= 200:
        raise ValueError(
            f"entry is {len(text)} characters, the gate allows 1-200"
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return raw, text


def write_entry(raw: bytes) -> None:
    """Write the entry and confirm the file on disk matches it exactly."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_bytes(raw)
    written = OUTPUT_FILE.read_bytes()
    if len(written) != len(raw):
        raise ValueError(
            f"wrote {len(written)} bytes but line.txt holds {len(raw)}"
        )
    if written != raw:
        offset = next(
            i for i, (a, b) in enumerate(zip(written, raw)) if a != b
        )
        raise ValueError(
            "copy differs from line.txt at byte "
            f"{offset} (wrote 0x{written[offset]:02x}, "
            f"line.txt holds 0x{raw[offset]:02x})"
        )


def main() -> int:
    try:
        raw, text = load_entry()
        write_entry(raw)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        f"wrote {OUTPUT_FILE} "
        f"({len(raw)} bytes, {len(text)} characters)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
