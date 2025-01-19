# -*- coding:utf-8 -*-
from time import sleep
import sys
import struct

global outFp


def string_hex_to_hex(temps):
    for i in range(0, int(len(temps) / 2)):
        outtemp = int(temps[i * 2 : i * 2 + 2], 16)
        # print(temps[i * 2:i * 2 + 2])
        outtemp2 = struct.pack("B", outtemp)
        outFp.write(outtemp2)


def tableread():
    global TBLword
    global TBLhex
    inFp4 = open(TBLfile, "r", encoding="utf-8")
    while True:  #
        line = inFp4.readline()
        line = line.replace("\ufeff", "")  # BOM고유오류 조정
        line = str(line)
        try:
            tempa = line[-2]
        except:
            break
        line = line.replace("\n", "")
        line = line.split("=")
        if line == [""]:
            break
        TBLword.append(tempa)
        TBLhex.append(line[0])


TBLword = []
TBLhex = []
REALTIVE_POINTER = []  # 상대포인터 저장하는 공간입니다.
MSG_NUMBER = []  # 메시지 넘버 저장하는 공간입니다.
DEF_LINE = 0  # 총 라인 갯수를 셀때 실질적으로 저장되는 칸입니다.

TBLfile = "C:/3DP/TBLEdit.tbl"
readfile = sys.argv[1]
# readfile="C:/3DP/MessageData_0154.bin.txt"
try:
    writefile = sys.argv[2]
except:
    writefile = readfile
    writefile += ".bin"
tablefile = "C:/3DP/TBLEdit.tbl"

inFp = open(readfile, "r", encoding="utf-8")
outFp = open(writefile, "wb")
# result=inFp.read(0x04)
tableread()
line = []
line = inFp.readline()
print(TBLword)
k = 0
for i in range(len(line)):
    try:
        MSG_NUMBER.append(line[3 + k : 3 + k + 4].upper())  # 지금까지 메시지 넘버 파싱입니다.
        k += 8
        if MSG_NUMBER[-1] == "":
            MSG_NUMBER.remove(MSG_NUMBER[-1])
            break
    except:
        break
inFp.close()
inFp = open(readfile, "r", encoding="utf-8")
lines = 0
lines = len(MSG_NUMBER)  # 총 대사 갯수
DEF_LINE = lines

inFp.seek(0)


lines = str(hex(lines))  # 총 라인수 쓰기시작..
lines = lines[2:]
if len(lines) == 3:
    writelines = lines[1:] + "0" + lines[0] + "0000"
elif len(lines) == 2:
    writelines = lines + "000000"
elif len(lines) == 1:
    writelines = lines + "0000000"
else:
    print("총 라인수 에러!")
writelines = writelines.upper()
string_hex_to_hex(writelines)  # 총 라인수를 셉니다
textlist = []
textlist = inFp.readlines()
textlist[0:2] = []  # 맨앞의 쓸모없는 라인 삭제
for i in range(DEF_LINE):
    templine = textlist[i]
    templine = templine.replace("\n", "")  # 모든 라인에서 엔터 항목을 제거합니다. 이후 00으로 채워줘야됨
    textlist[i] = templine
HEXline = []
for i in range(DEF_LINE):  # 코드들을 HEX로 바꿉니다.
    templine = textlist[i]
    templine = str(templine)
    newline = ""  # 헥스로 실제로 집어넣는 라인코드
    for k in range(len(templine)):
        Errorlevel = 1
        for h in range(len(TBLword)):
            if templine[k] == TBLword[h]:
                newline += TBLhex[h]
                Errorlevel = 0
                break
        if Errorlevel == 1:
            print("정의된 테이블이 없습니다!")
            print(templine[k])
            sleep(1000)
    HEXline.append(newline)
stackINT = 0
for i in range(DEF_LINE + 1):  # 상대포인터(텍스트 길이) 삽입
    try:
        INTERVAL = int(len(HEXline[i]) / 2) + 1 + stackINT
        stackINT = INTERVAL
        INTERVAL = str(hex(INTERVAL))[2:]
        if len(INTERVAL) == 1:
            INTERVAL = "0" + INTERVAL + "00"
        elif len(INTERVAL) == 2:
            INTERVAL = INTERVAL + "00"
        elif len(INTERVAL) == 3:
            INTERVAL = INTERVAL[1:] + "0" + INTERVAL[0]
        elif len(INTERVAL) == 4:
            INTERVAL = INTERVAL[2:] + INTERVAL[0:2]
        INTERVAL = INTERVAL.upper()
        string_hex_to_hex(str(INTERVAL))
    except:
        break
print(MSG_NUMBER)
for i in range(DEF_LINE):
    templine = MSG_NUMBER[i]
    print(templine)
    insert1 = templine[2:]
    insert2 = templine[0:2]
    string_hex_to_hex(insert1.upper())  # 메시지 넘버 삽입
    string_hex_to_hex(insert2.upper())  # 메시지 넘버 삽입
for i in range(DEF_LINE):
    string_hex_to_hex(str(HEXline[i]))
    string_hex_to_hex("00")
outline = str(hex(outFp.tell()))[-1]

if outline == "1" or outline == "5" or outline == "9" or outline == "D":
    string_hex_to_hex("000000")
elif outline == "2" or outline == "6" or outline == "A" or outline == "E":
    string_hex_to_hex("0000")
elif outline == "3" or outline == "7" or outline == "B" or outline == "F":
    string_hex_to_hex("00")
