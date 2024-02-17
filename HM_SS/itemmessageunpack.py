import sys
import os
import struct as s


def readint(file):
    return s.unpack("<I", file.read(4))[0]


def readshort(file):
    return s.unpack("<H", file.read(2))[0]


def unpack(src, outdir):
    try:
        os.mkdir(outdir)
    except FileExistsError:
        pass
    file = open(src, "rb")
    file.seek(0)
    count = readshort(file)

    offsets = []
    indexs = []
    sizes = []

    file_length = 0
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0, os.SEEK_SET)

    file.seek(0x02)
    for i in range(count + 1):
        offsets.append(readshort(file))

    for i in range(count):
        indexs.append(readshort(file))
    print(offsets, indexs)
    # Calculate size of each file
    for i in range(count):
        if i != count - 1:
            sizes.append(offsets[i + 1] - offsets[i])
        else:
            sizes.append(file_length - offsets[i])

    for i in range(count):
        oname = outdir + "/" + src + str(i).zfill(4) + ".hav"
        pos = 0x02 + (0x02 * len(offsets)) + (0x02 * len(indexs)) + offsets[i]
        size = sizes[i]
        file.seek(pos)
        buffer = file.read(size)
        with open(oname, "wb") as ofile:
            ofile.write(buffer)
    file.close()
    return


def usage():
    print("Usage: binunpack.py <file>")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
    path = os.path.abspath(sys.argv[1])

    # The directory of file
    fdir = os.path.dirname(os.path.realpath(path))

    # The name of file
    fname = os.path.splitext(os.path.basename(path))[0]

    outdir = fdir + "/" + fname

    unpack(sys.argv[1], outdir)
    print("Done!")
