import sys
import os
import struct as s


def readint(file):
    return s.unpack("<I", file.read(4))[0]


def unpack(src, outdir):
    try:
        os.mkdir(outdir)
    except FileExistsError:
        pass
    file = open(src, "rb")
    file.seek(0)
    count = readint(file)
    poses = []
    sizes = []

    file_length = 0
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0, os.SEEK_SET)

    # Get position(pointer)
    for i in range(count):
        file.seek(0x04 + (0x04 * i))
        poses.append(readint(file))

    # Get size
    for i in range(count):
        if i != count - 1:
            sizes.append(poses[i + 1] - poses[i])
        else:
            sizes.append(file_length - poses[i])

    for i in range(count):
        oname = outdir + "/" + src + str(i).zfill(4) + ".hav"
        pos = poses[i]
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
