# -*- coding:utf-8 -*-
from time import sleep
import sys


global inFp


def foundoffset():
    blank = []
    inFp = open(readfile, "rb")
    for i in range(4):
        startpath = inFp.read(1)
        temp = hex(ord(startpath))
        if temp == "0x0":
            temp = "0x00"
        blank.append(temp)  # 각각 읽어 blank에 추가
    blank.reverse()  # 리틀엔디안->빅엔디안
    pointer = ""
    pointer += blank[0]
    pointer += blank[1]
    pointer += blank[2]
    pointer += blank[3]
    pointer = pointer.replace("0x", "")
    result = "0x" + pointer
    print(result)
    return int(result, 16)


def tableread():
    global TBLword
    global TBLhex
    inFp4 = open(TBLfile, "r", encoding="utf-8")
    while True:
        line = inFp4.readline()
        line = line.replace("\n", "")
        line = line.split("=")
        if line == [""]:
            break
        line[0] = line[0].replace("\ufeff", "")  # BOM고유오류 조정
        TBLword.append(line[1])
        TBLhex.append(line[0])


TBLword = []
TBLhex = []
REALTIVE_POINTER = []  # 상대포인터 저장하는 공간입니다.
MSG_NUMBER = []  # 메시지 넘버 저장하는 공간입니다.
TBLfile = "C:/3DP/TBL.tbl"
# readfile=sys.argv[1]
# readfile="C:/3DP/MessageData_0007.bin"
readfile = "C:/3DP/MessageData_0164.bin"
try:
    writefile = sys.argv[2]
except:
    writefile = readfile
    writefile += ".txt"
tablefile = "C:/3DP/TBL.tbl"

inFp = open(readfile, "rb")
outFp = open(writefile, "w", encoding="utf-8")
# result=inFp.read(0x04)
print(readfile)
tableread()
OFFSET = foundoffset()
print(OFFSET)

inFp.read(0x04)
for i in range(OFFSET):
    blank = []
    for k in range(2):  # 2바이트씩 읽어야 합니다.
        result = inFp.read(0x01)

        temp = hex(ord(result))
        if temp == "0x0":
            temp = "0x00"
        blank.append(temp)
    blank.reverse()  # 리틀엔디안->빅엔디안
    pointer = ""
    pointer += blank[0]
    pointer += blank[1]
    pointer = pointer.replace("0x", "")
    result = "0x" + pointer
    REALTIVE_POINTER.append(result)
temp = inFp.tell()
for i in range(OFFSET):  # 메세지 넘버를 반환합니다.
    blank = []
    for k in range(2):  # 2바이트씩 읽어야 합니다.
        result = inFp.read(0x01)
        if result == "":
            result = 0
        temp = hex(ord(result))
        if temp == "0x0":
            temp = "0x00"
        if temp == "0x1":
            temp = "0x01"
        if temp == "0x2":
            temp = "0x02"
        if temp == "0x3":
            temp = "0x03"
        if temp == "0x4":
            temp = "0x04"
        if temp == "0x5":
            temp = "0x05"
        if temp == "0x6":
            temp = "0x06"
        if temp == "0x7":
            temp = "0x07"
        if temp == "0x8":
            temp = "0x08"
        if temp == "0x9":
            temp = "0x09"
        if temp == "0xa":
            temp = "0x0A"
        if temp == "0xb":
            temp = "0x0B"
        if temp == "0xc":
            temp = "0x0C"
        if temp == "0xd":
            temp = "0x0D"
        if temp == "0xe":
            temp = "0x0E"
        if temp == "0xf":
            temp = "0x0F"
        blank.append(temp)
    blank.reverse()  # 리틀엔디안->빅엔디안
    pointer = ""
    pointer += blank[0]
    pointer += blank[1]
    pointer = pointer.replace("0x", "")
    result = pointer
    MSG_NUMBER.append(result)
print(REALTIVE_POINTER)
print(MSG_NUMBER)
tblresult = ""

outFp.write(str(MSG_NUMBER))
outFp.write("\n")


for i in range(OFFSET):
    tblresult = ""
    while True:
        s = inFp.read(0x01)
        s = str(hex(ord(s)))
        if s == "0x0":
            s = "0x00"
        if s == "0x00":
            break
        s = s.replace("0x", "")
        tblresult += s

    tblresult = tblresult
    for i in range((len(tblresult))):
        try:
            for k in range(len(TBLword)):
                if tblresult[i : i + 2].upper() == TBLhex[k]:
                    front = tblresult[:i]
                    back = tblresult[i + 2 :]
                    tblresult = front + TBLword[k] + back
                    break
                if tblresult[i : i + 4].upper() == TBLhex[k]:
                    front = tblresult[:i]
                    back = tblresult[i + 4 :]
                    tblresult = front + TBLword[k] + back
                    break
        except:
            break
    print(tblresult)
    outFp.write("\n")
    outFp.write(str(tblresult))
