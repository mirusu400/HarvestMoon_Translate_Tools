#-*- coding:utf-8 -*-
# TToT Use Int-Size Pointer(4Bytes) But GB Use Short-Size Pointer(2Bytes), So A little bit Different With GB
import sys
import os
import struct
import binascii
TBLword = []
TBLhex = []
IOH_SIZE = 2
GB_SIZE = 2 #GB Use 2 Bytes to Read Pointers
POINTER_SIZE = IOH_SIZE
MAX_FILE_SIZE = 100000


def FILETOTXT(FileName):
    NFileName = os.path.splitext(FileName)[0]
    OutFileName = str(NFileName) + ".txt"
    ListOffset=[]
    ListFileOrder=[]
    inFp = open(FileName, "rb")
    OutFp = open(OutFileName,"w")
    buf = inFp.read(4)
    if(buf==""):
        return
    inFp.seek(0)
    try:
        FileIndex = struct.unpack('<I', buf)[0]
    except:
        print("File "+str(FileName)+" Cannot Converted")
        inFp.close()
        OutFp.close()
        return
        
     
    for i in range(0,FileIndex):
        inFp.seek(4+(i*POINTER_SIZE))
        buf = inFp.read(POINTER_SIZE)
        if (POINTER_SIZE == 2): ListOffset.append(struct.unpack('<H', buf)[0])
        elif (POINTER_SIZE == 4): ListOffset.append(struct.unpack('<I', buf)[0])
    
    for i in range(0,FileIndex):
        inFp.seek(4+(FileIndex * POINTER_SIZE) + (i*POINTER_SIZE))
        buf = inFp.read(POINTER_SIZE) 
        if (POINTER_SIZE == 2): ListFileOrder.append(str(struct.unpack('<H', buf)[0]).zfill(4))
        elif (POINTER_SIZE == 4): ListFileOrder.append(str(struct.unpack('<I', buf)[0]).zfill(4))
        
    for i in range(0,FileIndex):
        
        if(i == 0):
            inFp.seek(4+(FileIndex * POINTER_SIZE * 2))
            FileLength = ListOffset[i]
        else:
            inFp.seek(4+(FileIndex * POINTER_SIZE * 2) + int(ListOffset[i-1]))
            FileLength = ListOffset[i] - ListOffset[i-1]
        buf = inFp.read(FileLength)
        raw_text = buf.decode("cp949")
        OutFp.write(str(ListFileOrder[i]) + " : " + str(raw_text)+"\n")

    print("File "+str(FileName)+" Converted To Txt")
    inFp.close()
    OutFp.close()
    return


if __name__ == '__main__':
    if(os.path.isdir(sys.argv[1])):
        file_list = os.listdir(sys.argv[1])
        for file in file_list:
            OpenFile = str(sys.argv[1]) + "\\" + str(file)
            FILETOTXT(OpenFile)
    else:
        FILETOTXT(sys.argv[1])

