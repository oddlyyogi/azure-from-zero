"""Write three small sample photos (solid-colour PNG files) using only the standard library."""
import struct
import zlib
from pathlib import Path


def chunk(kind, data):
    return (struct.pack(">I", len(data)) + kind + data
            + struct.pack(">I", zlib.crc32(kind + data)))


def png(width, height, rgb):
    row = b"\x00" + bytes(rgb) * width
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(row * height)) + chunk(b"IEND", b""))


out = Path("samples/photos")
out.mkdir(parents=True, exist_ok=True)
colours = {"harbour": (40, 90, 160), "beach": (230, 200, 120), "market": (190, 60, 50)}
for name, rgb in colours.items():
    (out / f"{name}.png").write_bytes(png(320, 240, rgb))
    print(name, (out / f"{name}.png").stat().st_size, "bytes")
