# -*- coding:utf-8 -*-
# TToT Use Int-Size Pointer(4Bytes) But GB Use Short-Size Pointer(2Bytes)
# So A little bit different With GB
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

    def cv(self, char):
        if len(char) == 1:
            idx = self.tblword.index(char)
            data = self.tblhex[idx]
            return data
        else:
            idx = self.hex.index(char)
            data = self.tblword[idx]
            return data


def hextodatas(chex):
    writehex = binascii.unhexlify(chex)
    return writehex


def readshort(file):
    return s.unpack("<H", file.read(2))[0]


def readint(file):
    return s.unpack("<I", file.read(2))[0]


def writeint(num):
    return s.pack("<I", num)


def writeshort(num):
    return s.pack("<H", num)


def convert(file, tbl):
    texts = []
    hexs = []
    pos = []
    size = []

    out = os.path.splitext(file)[0] + ".hav"
    count = 0
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line == "\n":
                continue
            else:
                count += 1
                texts.append(line.replace("\n", ""))
    for i in range(count):
        text = texts[i]
        outbuf = ""
        tmp = []

        # Get hexes in one line
        for idx, char in enumerate(text):
            if idx in tmp:
                continue
            tbuf = ""
            # If char starts with '[' (제어코드)
            if char == "[":
                tidx = idx
                while True:
                    tidx += 1
                    tmp.append(tidx)
                    tbuf += text[tidx]
                    if text[tidx] == "]":
                        break
                tbuf.replace("]", "")
                outbuf += tbuf

            else:
                tbuf = tbl.cv(char)
            outbuf += tbl.cv(char)

        size.append(len(outbuf))
        hexs.append(outbuf)

        if i != 0:
            pos.append((count * POINTER_FLAG) + size[i-1])
        else:
            pos.append(count * POINTER_FLAG)

    with open(out, "wb") as f:
        # Write count
        if POINTER_FLAG == GB_FLAG:
            writeshort(count)
        elif POINTER_FLAG == TTOT_FLAG:
            writeint(count)

        # Write pointer(position)
        for i in range(count):
            if POINTER_FLAG == GB_FLAG:
                writeshort(pos[i])
            elif POINTER_FLAG == TTOT_FLAG:
                writeint(pos[i])

        for i in range(count):
            chex = hexs[i]
            buf = hextodatas(chex)
            f.write(buf)
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

