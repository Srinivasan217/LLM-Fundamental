"""Create sinusoidal positional encodings and render a small heatmap PNG."""

from __future__ import annotations

import math
import struct
import zlib
from pathlib import Path


def positional_encoding(position: int, dimensions: int) -> list[float]:
    """Return the original Transformer sinusoidal encoding for one position."""
    if position < 0 or dimensions < 1:
        raise ValueError("position must be non-negative and dimensions must be positive")

    values = []
    for dimension in range(dimensions):
        angle = position / (10000 ** (2 * (dimension // 2) / dimensions))
        values.append(math.sin(angle) if dimension % 2 == 0 else math.cos(angle))
    return values


def _png_chunk(kind: bytes, data: bytes) -> bytes:
    payload = kind + data
    checksum = zlib.crc32(payload) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + payload + struct.pack(">I", checksum)


def write_heatmap(path: Path, positions: int = 96, dimensions: int = 32) -> None:
    """Write the encodings as a dependency-free RGB PNG heatmap."""
    rows = bytearray()
    for position in range(positions):
        rows.append(0)
        for value in positional_encoding(position, dimensions):
            intensity = round((value + 1) * 127.5)
            rows.extend((intensity, 80, 255 - intensity))

    header = struct.pack(">2I5B", dimensions, positions, 8, 2, 0, 0, 0)
    image = b"\x89PNG\r\n\x1a\n"
    image += _png_chunk(b"IHDR", header)
    image += _png_chunk(b"IDAT", zlib.compress(bytes(rows)))
    image += _png_chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(image)


def main() -> None:
    output = Path(__file__).parent / "outputs" / "positional_encoding.png"
    write_heatmap(output)
    print(f"Wrote {output}")
    print("Position 0:", positional_encoding(0, 8))


if __name__ == "__main__":
    main()
