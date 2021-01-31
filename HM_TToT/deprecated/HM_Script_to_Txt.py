#-*- coding:utf-8 -*-
# TToT Use Int-Size Pointer(4Bytes) But GB Use Short-Size Pointer(2Bytes), So A little bit Different With GB
import sys
import os
import struct
import binascii
TBLword = []
TBLhex = []
TTOT_SIZE = 4 #TToT Use 4 Bytes to Read Pointers
GB_SIZE = 2 #GB Use 2 Bytes to Read Pointers
POINTER_SIZE = GB_SIZE
MAX_FILE_SIZE = 100000
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
def OffsetRead(FileObj, FileOrd):
    TmpOffset = []
    TmpSizeOffset = []
    FileObj.seek(0)
    for i in range(0, FileOrd):
        FileObj.seek(i*POINTER_SIZE)
        buf = FileObj.read(POINTER_SIZE)
        if (POINTER_SIZE == 2):
            value = struct.unpack('<H', buf)[0]
        elif (POINTER_SIZE == 4):
            value = struct.unpack('<I', buf)[0]
        TmpOffset.append(value)
        if(i != 0):
            TmpSizeOffset.append(TmpOffset[i] - TmpOffset[i-1])
    TempBuf = FileObj
    TempBuf.seek(0,2)
    TmpSizeOffset.append(TempBuf.tell() - TmpOffset[FileOrd-1])
    #--마지막 오프셋 배열에 추가해야함
    return TmpOffset, TmpSizeOffset

def FILETOTXT(FileName):
    global TBLword
    global TBLhex
    ListOffset = []
    ListSize = []
    ResultOutput=""

    inFp = open(FileName, "rb")
    buf = inFp.read(2)
    inFp.seek(0)
    if(binascii.hexlify(buf).decode('utf-8').upper() == "0F27"): #NULL 바이너리 일 경우
        print("File "+str(FileName)+" is a Null File")
        inFp.close()
        return
    outFp = open(FileName + ".txt", "w", encoding="utf-8")

    #-------------------------------------------- For Convenience..
    #outFp.write("SPLITSCRIPT\n")
    #outFp.write(os.path.basename(FileName)+".txt\n")
    #--------------------------------------------
    
    buf = inFp.read(POINTER_SIZE)
    if (POINTER_SIZE == 2): FileIndex = struct.unpack('<H', buf)[0]
    elif (POINTER_SIZE == 4): FileIndex = struct.unpack('<I', buf)[0]
    #print("FileIndex : "+str(FileIndex))

    ListOffset, ListSize = OffsetRead(inFp,int(FileIndex/POINTER_SIZE)) #오프셋 읽어서 배열에 저장
    for j in range(0,len(ListOffset)): #각 오프셋(라인)마다 Loop문 진행
        if(ListOffset[j] >= MAX_FILE_SIZE or ListOffset[j] < 0): #if index out of bound
            break
        elif(ListSize[j] >= MAX_FILE_SIZE or ListSize[j] < 0):
            break
        inFp.seek(ListOffset[j]) #오프셋으로 이동
        ResultOutput = ""
        for k in range(0,int(ListSize[j]/2)): #한 줄에서 읽을 바이트 진행(4바이트씩 읽음)
            buf = inFp.read(2)
            ConvHex = binascii.hexlify(buf).decode('utf-8').upper()
            #TempSwitch = 0
            #print(str(k) + "," + str(ConvHex))
            try:
                Temp = TBLhex.index(ConvHex)
                ResultOutput += TBLword[Temp]
            except:
                ResultOutput += "[" + ConvHex + "]"
            '''
            for p in range(0,len(TBLhex)):
                if (ConvHex == TBLhex[p]):
                    ResultOutput += TBLword[p]
                    TempSwitch = 1
                    break
            if(TempSwitch == 0): #테이블에 문자열이 없는경우
            
                ResultOutput += "[" + ConvHex + "]"
            '''
        #print(str(ResultOutput))
        outFp.write(str(ResultOutput)+"\n")
    print("File "+str(FileName)+" Converted To Txt")
    inFp.close()
    outFp.close()
    return


if __name__ == '__main__':
    TBLFILE =  'D:/한글화/목장이야기 바람의바자회/데이터 언팩/Jtable.tbl'
    TableRead(TBLFILE)

    #FILETOTXT('D:/한글화/목장이야기 바람의바자회/데이터 언팩/event_mes_data/event_mes_data_100')
    if(os.path.isdir(sys.argv[1])):
        file_list = os.listdir(sys.argv[1])
        for file in file_list:
            OpenFile = str(sys.argv[1]) + "\\" + str(file)
            FILETOTXT(OpenFile)
    else:
        FILETOTXT(sys.argv[1])

