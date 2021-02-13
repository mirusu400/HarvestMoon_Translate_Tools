# Bin file structure in GB and TToT

```
All the files are written in little-endian.

DWORD   count of subfile
QWORD   pointer[i]

Struct of pointer
DWORD   poistion of subfile
DWORD   size of subfile

So file position should be:
0x04 + (0x08 * 0x(Count of subfile)) + (Position of subfile)
```
