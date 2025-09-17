import sys
import os
import struct as s
import shutil
from typing import Union


def readint(file):
    return s.unpack("<I", file.read(4))[0]


def readshort(file):
    return s.unpack("<H", file.read(2))[0]


class ItemMessage:
    def unpack(self, src, outdir):
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

        # Calculate size of each file
        for i in range(count):
            if i != count - 1:
                sizes.append(offsets[i + 1] - offsets[i])
            else:
                sizes.append(file_length - offsets[i])

        basename = os.path.splitext(os.path.basename(src))[0]

        for i in range(count):
            oname = outdir + "/" + basename + str(i).zfill(4) + ".hav"
            pos = 0x02 + (0x02 * len(offsets)) + (0x02 * len(indexs)) + offsets[i]
            size = sizes[i]
            file.seek(pos)
            buffer = file.read(size)
            with open(oname, "wb") as ofile:
                ofile.write(buffer)
        file.close()
        return

    def pack(self, inputdir, outfile: Union[str, None] = None):
        if outfile is None:
            outfile = inputdir + ".bin"

        # if exist, ask user to delete it
        if os.path.exists(outfile):
            print(f"File {outfile} already exists. Do you want to delete it? (y/n)")
            if input() == "y":
                os.remove(outfile)
            else:
                print("Aborting...")
                sys.exit(1)

        # read all *.hav files in inputdir
        files = os.listdir(inputdir)
        files = [f for f in files if os.path.isfile(os.path.join(inputdir, f))]
        files = [f for f in files if f.endswith(".hav")]

        # read all files
        file_buffers = []
        file_count = len(files)
        offsets = []
        indexs = []

        offsets.append(0)
        total_size = 0
        index = 1

        for file in files:
            with open(os.path.join(inputdir, file), "rb") as f:
                buffer = f.read()
                file_buffers.append(buffer)
                total_size += len(buffer)
            offsets.append(total_size)
            file_index = file.split(".")[1].split("bin")[1]
            indexs.append(int(file_index))

        # write to outfile
        with open(outfile, "wb") as f:
            f.write(file_count.to_bytes(2, "little"))
            for offset in offsets:
                f.write(offset.to_bytes(2, "little"))
            for index in indexs:
                f.write(index.to_bytes(2, "little"))
            for buffer in file_buffers:
                f.write(buffer)


def usage():
    print("========== ItemMessage.bin tool ==========")
    print("If you want to extract ItemMessage.bin:")
    print("Usage: itemmessage.py <file> <outdir(optional)>\n")
    print("If you want to pack ItemMessage.bin:")
    print("Usage: itemmessage.py <dir> <outfile(optional)>\n")

    sys.exit(1)


def test():
    item_message = ItemMessage()
    item_message.unpack("ItemMessage.bin", "ItemMessage_test")
    item_message.pack("ItemMessage_test", "ItemMessage_out.bin")

    # Check if the output file is the same as the input file
    with open("ItemMessage.bin", "rb") as f1, open("ItemMessage_out.bin", "rb") as f2:
        if f1.read() == f2.read():
            print("The output file is the same as the input file")
        else:
            print("The output file is not the same as the input file")

    # Remove test files
    shutil.rmtree("ItemMessage_test")
    os.remove("ItemMessage_out.bin")


if __name__ == "__main__":
    # test()
    # exit(0)

    if len(sys.argv) == 1:
        usage()

    item_message = ItemMessage()
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

        item_message.unpack(sys.argv[1], outdir)
        print("Extract Done!")

    # if path is directory
    elif os.path.isdir(path):
        if len(sys.argv) == 3:
            outfile = sys.argv[2]
        else:
            outfile = None
        item_message.pack(path, outfile)
        print("Pack Done!")
