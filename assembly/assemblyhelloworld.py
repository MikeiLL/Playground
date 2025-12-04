"""
Generates an INTEL file that prints and astericks to the console.
Can run output file with DOSbox it creates a binary file
that `hd`d looks like:
```
00000000  `b4 02 b2 2a cd 21 cd 20`     |...*.!. |
00000008
```
`b4 02 b2 2a cd 21 cd 20` Translates to
```
MOV AH, 02
MOV DL, 2A
INT 21
INT 20
MOV AH, 02 ; B4 02
```

`INT` is interrupt
`MOV` is move and sets/assigns something

Before Unicode there was BoxCode variations
IMB OEN sometimes called codepage 437
"""

open("writestr.com", "wb").write(b"\xb4\x02\xb2\x2a\xcd\x21\xcd\x20")
