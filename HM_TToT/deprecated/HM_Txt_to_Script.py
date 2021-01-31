#-*- coding:utf-8 -*-
# TToT Use Int-Size Pointer(4Bytes) But GB Use Short-Size Pointer(2Bytes), So A little bit Different With GB
import sys
import struct
import binascii
import os
TBLword = []
TBLhex = []
TTOT_SIZE = 4 #TToT Use 4 Bytes to Read Pointers
GB_SIZE = 2 #GB Use 2 Bytes to Read Pointers
POINTER_SIZE = GB_SIZE
def WriteRaw(Data, File, Pointer = -1):
    if(Pointer != -1): File.seek(Pointer)
    WriteHex = binascii.unhexlify(Data)
    File.write(WriteHex)
    return
def WriteOffset(Data, File, Pointer = -1):
    if(Pointer != -1): File.seek(Pointer)
    if (POINTER_SIZE == 2):
        data = struct.pack('<H', Data)
    elif (POINTER_SIZE == 4):
        data = struct.pack('<I', Data)
    File.write(data)
    return
def TableRead(TBLFile):
    inFp=open(TBLFile,"r",encoding='utf-8')
    while True:
        line=inFp.readline()
        line=line.replace("\n","")
        line=line.split("=")
        if (line == ['']):
            break
        line[0] = line[0].replace(u"\ufeff", '') #BOM Error Edit
        TBLword.append(line[1])
        TBLhex.append(line[0])
    inFp.close()
    return
def TXTTOFILE(FileName):
    global TBLword
    global TBLhex
    LastPointer=0
    inFp = open(FileName, "r",encoding='utf-8-sig')
    LineArr = [line for line in inFp.readlines() if line.strip()] #빈 줄 제외하고 lines 배열에 추가
    if(LineArr[0] == "SPLITSCRIPT\n"):
        del LineArr[0]
    if (ord(LineArr[0][0]) >= 48 and ord(LineArr[0][0]) <= 57):
        del LineArr[0]
    if(ord(LineArr[0][0]) >= 65 and ord(LineArr[0][0]) <= 90):
        del LineArr[0]
    if (ord(LineArr[0][0]) >= 97 and ord(LineArr[0][0]) <= 122):
        del LineArr[0]
    #print(LineArr)
    inFp.close()
    OutputName = FileName.replace(".txt","")
    OutFp = open(OutputName, "wb")
    for j in range(0,len(LineArr)): #총 파일만큼 오프셋에 적어주는 반복문
        LineArr[j] = LineArr[j].replace("\n","")
        WriteOffset(0, OutFp,j*POINTER_SIZE)
    for k in range(0, len(LineArr)): #각 라인마다 접근해 단어 하나하나의 값을 테이블에서 찾아와 쓰는 역할
        LastPointer = OutFp.tell()
        WriteOffset(LastPointer,OutFp,k*POINTER_SIZE)
        OutFp.seek(0,2) #포인터 맨 뒤로 이동
        TmpSkip = 0
        for p in range(0,len(LineArr[k])):
            if(TmpSkip != 0):
                TmpSkip -= 1
                continue
            if(LineArr[k][p] == "["): #바이너리 직접 쓰기 모드
                WriteHex = LineArr[k][p+1:p+5]
                WriteRaw(WriteHex, OutFp)
                TmpSkip = 5
            else:
                #ErrorLevel = 0
                try:
                    Temp = TBLword.index(LineArr[k][p])
                    WriteRaw(TBLhex[Temp], OutFp)
                except:
                    print("Something went wrong! Maybe TBL file should not match with txt File. \nFile Name : " + str(FileName) + "\nString Order : " + str(LineArr[k][p]) + "\nProgram Exited.")
                    return
                '''
                for TBLIndex in range(0,len(TBLword)):
                    if(TBLword[TBLIndex] == LineArr[k][p]):
                        WriteRaw(TBLhex[TBLIndex],OutFp)
                        ErrorLevel=1
                        break
                if(ErrorLevel==0):
                    print("Something went wrong! Maybe TBL file should not match with txt File. \nFile Name : " + str(FileName) + "\nString Order : " + str(LineArr[k][p]) + "\nProgram Exited.")
                    return
                '''
    print("File " + str(FileName) + " Converted To File.")
    OutFp.close()
    return



if __name__ == '__main__':
    TBLFILE = 'D:/한글화/목장이야기 바람의바자회/데이터 언팩/Jtable.tbl'
    #TBLFILE = 'D:/한글화/목장이야기 바람의바자회/데이터 언팩/Jtable van 번역.tbl'
    TableRead(TBLFILE)
    #TXTTOFILE('D:\한글화\목장이야기 바람의바자회\데이터 언팩\event_mes_data_txt\event_mes_data_100.sbin.txt')
    if(os.path.isdir(sys.argv[1])):
        file_list = os.listdir(sys.argv[1])
        for file in file_list:
            OpenFile = str(sys.argv[1]) + "\\" + str(file)
            if(os.path.splitext(OpenFile)[1] == '.txt'):
                TXTTOFILE(OpenFile)
    else:
        TXTTOFILE(sys.argv[1])
