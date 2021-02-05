# HarvestMoon Localization Tools
[DS] HarvestMoon Series TBL and Text Tools For Translation

If you need my help for localization about HM series(above DS), please e-mail to me.

# DS
## Harvest Moon Islands Of Happiness (HM_IoH)
- 목장이야기 너와 함께 자라는 섬
- Only Support KOR version. If you need USA/EUR/JPN version, You may need to uncompress lz11 and change codepage in source code.

## Harvest Moon Sunshine Islands (HM_SS)
- 목장이야기 반짝반짝 태양과 동료들
- Some of the files are archived with bin, you can unpack/pack them as `binpacker`
- Only Support JPN version, and need a custom encode table. If you need USA/EUR version, You may need to uncompress lz11 and change custom encode table.


## Harvest Moon Grand Bazzar (HM_GB)
- 목장이야기 어서오세요! 바람의 바자르에
- Some of the files are archived with bin, you can unpack/pack them as `binpacker`
- Text tools are same as HM_TToT, Only updated Graphics Info.

## Harvest Moon The Tale of Two Towns (HM_TTOTT)
- 목장이야기 쌍둥이마을
- Some of the files are archived with bin, you can unpack/pack them as `binpacker`
- `scripttotext.py` and `texttoscript.py` are used to extract/import between script and text. They need custom encode table such as HM_SS.


# 3DS
## Story of Seasons Trio of Towns (SoS_ToT)
- 목장이야기 세 마을의 소중한 친구들
- Already [Kuriimu](https://github.com/IcySon55/Kuriimu) has a plugin to modify PAPA plag, but it's not compatable with USA version cause of Encode Issue.
- USA version uses Shift-Jis Encode, but JPN version uses UTF16LE Encode.


# TODO
- upload SoS_ToT PAPA file to xlsx.
- upload documentation of structures.




