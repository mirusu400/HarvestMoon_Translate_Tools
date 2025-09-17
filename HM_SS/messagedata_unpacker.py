"""
This is a script for packing and unpacking MessageData.bin
"""

import sys
import os
import struct as s
import shutil
from typing import Union


def readint(file):
    return s.unpack("<I", file.read(4))[0]


class MessageData:
    def unpack(self, src, outdir):
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
        basename = os.path.splitext(os.path.basename(src))[0]
        for i in range(count):
            oname = outdir + "/" + basename + str(i).zfill(4) + ".hav"
            pos = poses[i]
            size = sizes[i]
            file.seek(pos)
            buffer = file.read(size)
            with open(oname, "wb") as ofile:
                ofile.write(buffer)
        file.close()
        return

    def pack(self, src, outfile: Union[str, None] = None):
        if outfile is None:
            outfile = src + ".bin"

        # if exist, ask user to delete it
        if os.path.exists(outfile):
            print(f"File {outfile} already exists. Do you want to delete it? (y/n)")
            if input() == "y":
                os.remove(outfile)
            else:
                print("Aborting...")
                sys.exit(1)

        file_blobs = []
        sizes = []
        for file in os.listdir(src):
            if not file.endswith(".hav"):
                continue
            with open(os.path.join(src, file), "rb") as f:

                file_blobs.append(f.read())
                sizes.append(len(file_blobs[-1]))

        with open(outfile, "wb") as f:
            f.write(s.pack("<I", len(file_blobs)))
            offset = 4 + 4 * len(file_blobs)
            for i in range(len(file_blobs)):
                f.write(s.pack("<I", offset))
                offset += sizes[i]
            for blob in file_blobs:
                f.write(blob)


def usage():
    print("========== MessageData.bin tool ==========")
    print("If you want to extract MessageData.bin:")
    print("Usage: messagedata.py <file> <outdir(optional)>\n")
    print("If you want to pack MessageData.bin:")
    print("Usage: messagedata.py <dir> <outfile(optional)>\n")

    sys.exit(1)


def test():
    message_data = MessageData()
    message_data.unpack("MessageData.bin", "MessageData_test")
    message_data.pack("MessageData_test", "MessageData_test.bin")

    with open("MessageData.bin", "rb") as f1, open("MessageData_test.bin", "rb") as f2:
        assert f1.read() == f2.read()
    print("Passed!")

    shutil.rmtree("MessageData_test")
    os.remove("MessageData_test.bin")


if __name__ == "__main__":
    # test()
    # exit(0)

    if len(sys.argv) == 1:
        usage()

    message_data = MessageData()
    path = os.path.abspath(sys.argv[1])

    # if path is file
    if os.path.isfile(path):
        if len(sys.argv) == 3:
            outdir = sys.argv[2]
        else:
            # Make output directory
            fdir = os.path.dirname(os.path.realpath(path))
            fname = os.path.splitext(os.path.basename(path))[0]
            outdir = fdir + "/" + fname

        message_data.unpack(sys.argv[1], outdir)
        print("Extract Done!")

    # if path is directory
    elif os.path.isdir(path):
        if len(sys.argv) == 3:
            outfile = sys.argv[2]
        else:
            outfile = None
        message_data.pack(path, outfile)
        print("Pack Done!")
