# Bin file structure in SS

```
All the files are written in little-endian.

DWORD   count of subfile
DWORD   pointer[i]

So file position should be:
pointer[i]

File size should be:
pointer[i+1] - pointer[i]
```


# Script structure in SS (JPNver.)

```
WIP
```