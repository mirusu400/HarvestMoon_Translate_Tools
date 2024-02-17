import sys
import os
import struct as s


def pack(src: str, dst: str):
    file_blobs = []
    sizes = []
    for file in os.listdir(src):
        if not file.endswith(".hav"):
            continue
        with open(os.path.join(src, file), "rb") as f:

            file_blobs.append(f.read())
            sizes.append(len(file_blobs[-1]))

    with open(dst, "wb") as f:
        f.write(s.pack("<I", len(file_blobs)))
        offset = 4 + 4 * len(file_blobs)
        for i in range(len(file_blobs)):
            f.write(s.pack("<I", offset))
            offset += sizes[i]
        for blob in file_blobs:
            f.write(blob)


if __name__ == "__main__":
    try:
        src = sys.argv[1]
        dest = sys.argv[2]
    except IndexError:
        print("Usage: binpack.py <folder> <destination>")
        sys.exit(1)

    pack(src, dest)
    print("Done!")
