import sys
import os
import struct as s


def readint(file):
    return s.unpack("<I", file.read(4))[0]


def unpack(file, outdir):
    global fname
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
        if i != count-1:
            sizes.append(poses[i+1] - poses[i])
        else:
            sizes.append(file_length - poses[i])

    for i in range(count):
        oname = outdir + "/" + fname + str(i).zfill(4) + ".hav"
        pos = poses[i]
        size = sizes[i]
        file.seek(pos)
        buffer = file.read(size)
        with open(oname, "wb") as ofile:
            ofile.write(buffer)
    return


def usage():
    print("Just drag-and-drop file in this file!")
    print("The program will exit.")
    input()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    path = os.path.abspath(sys.argv[1])

    # The directory of file
    fdir = os.path.dirname(os.path.realpath(path))

    # The name of file
    fname = os.path.splitext(os.path.basename(path))[0]

    outdir = fdir + "/" + fname
    try:
        os.mkdir(outdir)
    except FileExistsError:
        pass
    with open(sys.argv[1], mode="rb") as f:
        unpack(f, outdir)
    print("Done!")
