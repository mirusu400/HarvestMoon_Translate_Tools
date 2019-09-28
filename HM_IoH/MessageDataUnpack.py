#-*- coding:utf-8 -*-
import sys
import struct
import binascii
import os
#FileName = Real File Name
#NFileName = File Name Without Extension
#NatFileName = Only File Name

def FILETOTXT(FileName):
    FILESIZE = os.path.getsize(FileName)
    NFileName = os.path.splitext(FileName)[0]
    NatFileName = os.path.split(os.path.splitext(FileName)[0])[1]
    ListOffset = []
    ResultOutput=""
    inFp = open(FileName, "rb")
    buf = inFp.read(4)
    FileIndex = struct.unpack('<I', buf)[0]
    print(FileIndex)
    for i in range(0,FileIndex):
        inFp.seek(4+(i*4))
        buf = inFp.read(4)
        ListOffset.append(struct.unpack('<I',buf)[0])
        
    
    print(ListOffset)
    try:
        os.mkdir(str(NFileName))
    except:
        print("dir already exist!")
    
    for p in range(0,len(ListOffset)):
        OutFileName = str(NFileName) + "/" + str(NatFileName) + "_" + str(p).zfill(4) + ".sbin"
        OutFp = open(OutFileName,"wb")
        try:
            FileLength = ListOffset[p+1] - ListOffset[p]
        except:
            FileLength = FILESIZE - ListOffset[p]
        print("Unpack %s with size %d" % (OutFileName,FileLength))
        inFp.seek(ListOffset[p])
        buf = inFp.read(FileLength)
        OutFp.write(buf)
        OutFp.close()
    
    
        
    inFp.close()
    return


if __name__ == '__main__':
    FILETOTXT(sys.argv[1])

    #FILETOTXT('C:/Clang/HM_TTOT/Release/event_mes_data/event_mes_data_3','C:/Users/user/Desktop/쌍둥이_일어테이블_완성.tbl')
