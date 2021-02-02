# -*- coding:utf-8 -*-
# TToT Use Int-Size Pointer(4Bytes) But GB Use Short-Size Pointer(2Bytes)
# So A little bit Different With GB
import sys
import os
import struct as s
import binascii

# TToT Use 4 Bytes to Read Pointers
TTOT_FLAG = 4
# GB Use 2 Bytes to Read Pointers
GB_FLAG = 2
POINTER_FLAG = GB_FLAG
TBLFILE = './HM_TToT/TToT_jpn.tbl'


class table():
    def __init__(self, file):
        self.file = file
        self.tblword = []
        self.tblhex = []
        self.readtable()

    def readtable(self):
        with open(self.file, "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                line = line.replace("\n", "").split("=")
                if (line == ['']):
                    break
                # BOM Error fix
                line[0] = line[0].replace(u"\ufeff", '')
                self.tblword.append(line[1])
                self.tblhex.append(line[0])

        return


def readshort(file):
    return s.unpack("<H", file.read(2))[0]


def readint(file):
    return s.unpack("<I", file.read(2))[0]


def convert(file, tbl):
    texts = []
    out = os.path.splitext(file)[0] + ".txt"
    with open(file, "rb") as f:
        # Check if it is null binary file
        if binascii.hexlify(f.read(2)).decode('utf-8').upper() == "0F27":
            print("File %s is a null file, skip it." % (file))
            return

        f.seek(0)

        if POINTER_FLAG == GB_FLAG:
            count = readshort(f) // 2
        elif POINTER_FLAG == TTOT_FLAG:
            count = readint(f) // 4

        poses = []
        f.seek(0)

        for i in range(count):
            if POINTER_FLAG == GB_FLAG:
                poses.append(readshort(f))
            elif POINTER_FLAG == TTOT_FLAG:
                poses.append(readint(f))

        for i in range(count):
            pos = poses[i]
            text = ""
            # Get size of bytes
            if i != count-1:
                size = poses[i+1] - poses[i]
            else:
                size = os.path.getsize(file) - poses[i]

            f.seek(pos)
            for j in range(size//2):
                buffer = f.read(2)
                chex = binascii.hexlify(buffer).decode('utf-8').upper()
                # Add string encoded with custom table
                try:
                    idx = tbl.tblhex.index(chex)
                    text += tbl.tblword[idx]
                except ValueError:
                    text += "[" + chex + "]"
            texts.append(text)

    with open(out, "w", encoding="utf-8") as o:
        for text in texts:
            o.write(text + "\n")

    print("File %s was successfully converted to text." % (file))
    return


if __name__ == '__main__':
    t = table(TBLFILE)

    if os.path.isdir(sys.argv[1]):
        file_list = os.listdir(sys.argv[1])
        for file in file_list:
            ofile = str(sys.argv[1]) + "/" + str(file)
            convert(ofile, t)
    else:
        convert(sys.argv[1], t)

