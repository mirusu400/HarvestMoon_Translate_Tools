# MessageData.bin file structure in SS

```
All the files are written in little-endian.

u32   count of subfile
u32   pointer[i]

So file position should be:
pointer[i]

File size should be:
pointer[i+1] - pointer[i]
```

## Each files in MessageData.bin

Actually, maybe JPN and ENG are different. ENG seems that they use lz77 (11 flag) compression.
You may decompress before unpack.
```
u32   Count of text
for i in (count):
    u16   Pointer[i]
for i in (count):
    u16   Size[i]
```


# ItemMessage.bin structure in SS

```
All the files are written in little-endian

u16   Cound of subfile
for i in (count + 1):
    u16   offsets[i]
for i in count:
    u16   indexs[i]
```

## Each files in ItemMessage.bin

```
This is very simple. You can just open with Shift-JIS
```
