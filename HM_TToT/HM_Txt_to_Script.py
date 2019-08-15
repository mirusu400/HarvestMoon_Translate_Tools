#-*- coding:utf-8 -*-
import sys
import struct
import binascii
TBLword = []
TBLhex = []
def WriteRaw(Data, File, Pointer = -1):
    if(Pointer != -1): File.seek(Pointer)
    WriteHex = binascii.unhexlify(Data)
    File.write(WriteHex)
    return
def WriteInt(Data, File, Pointer = -1):
    if(Pointer != -1): File.seek(Pointer)
    data = struct.pack('<i', Data)
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
def TXTTOFILE(FileName, TBLName):
    global TBLword
    global TBLhex
    LastPointer=0
    TableRead(TBLName)
    inFp = open(FileName, "r",encoding='utf-8-sig')
    LineArr = [line for line in inFp.readlines() if line.strip()] #빈 줄 제외하고 lines 배열에 추가
    #print(LineArr)
    inFp.close()
    OutputName = FileName.replace(".txt","")
    OutFp = open(OutputName, "wb")
    for j in range(0,len(LineArr)):
        LineArr[j] = LineArr[j].replace("\n","")
        WriteInt(0, OutFp,j*4)
    for k in range(0, len(LineArr)):
        LastPointer = OutFp.tell()
        WriteInt(LastPointer,OutFp,k*4)
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
                ErrorLevel = 0
                for TBLIndex in range(0,len(TBLword)):
                    if(TBLword[TBLIndex] == LineArr[k][p]):
                        WriteRaw(TBLhex[TBLIndex],OutFp)
                        ErrorLevel=1
                        break
                if(ErrorLevel==0):
                    print("Something went wrong! Maybe TBL file should not match with txt File. \nFile Name : " + str(FileName) + "\nString Order : " + str(LineArr[k][p]) + "\nProgram Exited.")
                    return

    OutFp.close()
    return



if __name__ == '__main__':
    TXTTOFILE(sys.argv[1], 'C:/Users/user/Desktop/쌍둥이_일어테이블_완성.tbl')
    #TXTTOFILE('C:/Clang/HM_TTOT/Release/Script/event_mes_data_1.txt','C:/Users/user/Desktop/쌍둥이_일어테이블_완성.tbl')
