import sys
import os
import struct as s


def readint(file):
    return s.unpack("<I", file.read(4))[0]


def writeint(num):
    return s.pack("<I", num)


def pack(file, outdir):
    global fname
    count = int(sorted(os.listdir(path))[-1].split(".")[0].replace(fname, "")) + 1
    pointer = 0
    file.write(writeint(count))

    for i in range(count):
        tname = outdir + "/" + fname + str(i).zfill(4) + ".hav"
        size = os.path.getsize(tname)

        file.write(writeint(pointer))
        file.write(writeint(size))

        pointer += size

        # Position must be multiplies of 4.
        while pointer % 4 != 0:
            pointer += 1

    for i in range(count):
        tname = outdir + "/" + fname + str(i).zfill(4) + ".hav"
        with open(tname, "rb") as t:
            buffer = t.read()

            # Position must be multiplies of 4.
            # So put nullbytes to set the position.
            while len(buffer) % 4 != 0:
                buffer += s.pack("B", 0)

            file.write(buffer)
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

    # The upper directory of dir
    fdir = os.path.dirname(path)

    # The name of dir
    fname = os.path.splitext(os.path.basename(path))[0]

    outfname = fdir + "/" + fname + ".out.bin"

    with open(outfname, mode="wb") as f:
        pack(f, path)
    print("Done!")