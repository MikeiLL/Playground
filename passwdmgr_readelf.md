# NCL password manager hack

Check file header with hexdump: `hd pass_manager-x32 | head`. The `file` command will also (perhaps more elegantly) yield this information.: `file pass_manager-x32`.
It is piped to the `head` command to view just the first few lines.
File type appears to possibly be `ELF` which is an Executable Linked File and on unix can be read with the `readelf` utility.
[Good writeup on readelf](https://www.geeksforgeeks.org/linux-unix/readelf-command-in-linux-with-examples/)

- Inspecting the file header I learned what language the app is written in: `readelf -h pass_manager-x32` (The `-n` notes flag also yeilds this.)
- Apparently there are sections which can be viewed with the `objdump` utility: `objdump -h pass_manager-x32`
- - [baeldung post](https://www.baeldung.com/linux/file-elf-extract-raw-contents)

```
$ objdump -h pass_manager-x32 

pass_manager-x32:     file format elf32-i386

Sections:
Idx Name          Size      VMA       LMA       File off  Algn
  0 .text         0009eb00  08049000  08049000  00001000  2**4
                  CONTENTS, ALLOC, LOAD, READONLY, CODE
  1 .rodata       0005cd67  080e8000  080e8000  000a0000  2**5
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  2 .typelink     000011cc  08144d68  08144d68  000fcd68  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  3 .gosymtab     00000000  08145f34  08145f34  000fdf34  2**0
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  4 .gopclntab    00042811  08145f40  08145f40  000fdf40  2**5
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  5 .noptrdata    0000b460  08189000  08189000  00141000  2**5
                  CONTENTS, ALLOC, LOAD, DATA
  6 .data         00003008  08194460  08194460  0014c460  2**5
                  CONTENTS, ALLOC, LOAD, DATA
  7 .bss          0000ff24  08197480  08197480  0014f480  2**5
                  ALLOC
  8 .noptrbss     000040e0  081a73c0  081a73c0  0015f3c0  2**5
                  ALLOC
  9 .note.go.buildid 00000038  08048fc8  08048fc8  00000fc8  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
```

- Then readelf can dump these to STDOUT either with the -x flag for hex or -p for string. eg: `readelf -x 2 pass_manager-x32` which yields some readable strings amongst the non-ascii content:
- - (The numeral 2 refers to the second section.)
```
- - 0x08143bc0 69657261 6c6c2069 6e743332 3b206763 ierall int32; gc
- - 0x08143bd0 73746f70 74686577 6f726c64 20696e74 stoptheworld int
- - 0x08143be0 33323b20 67637472 61636520 696e7433 32; gctrace int3
- - 0x08143bf0 323b2069 6e76616c 69647074 7220696e 2; invalidptr in
- - 0x08143c00 7433323b 20736272 6b20696e 7433323b t32; sbrk int32;
- - 0x08143c10 20736361 76656e67 6520696e 7433323b  scavenge int32;
```
I was able to confirm that `2` represents the second header which in our case is `.rodata` (whatever that is):
```
$ readelf -x .rodata pass_manager-x32 | grep stoptheworld
  0x081251a0 67637374 6f707468 65776f72 6c640000 gcstoptheworld..
  0x08143bd0 73746f70 74686577 6f726c64 20696e74 stoptheworld int
```
There must be something more though...

- There is a `dd` utility which will "convert and copy a file" (see `man dd`). Out command ends up being:
- - `dd if=pass_manager-x32 of=out_objdump_text bs=1 count=$((0x9eb00)) skip=$((0x9000))`, which reads through nearly 650000 records into a file called out_objdump_text.

Those records, though, don't seem to be ascii nor very readable. It's raw (binary?) data: 
```
$ file out_objdump_text 
out_objdump_text: data
```

- - TIP The `awk` utility can be used to populate the `dd` command with the details from the `readelf` output:
```
$ objdump -h pass_manager-x32 | grep .text | awk '{print "dd if=pass_manager-x32 of=out_objdump_text bs=1 count=$((0x"$3")) skip=$((0x"$6"))"}'
dd if=pass_manager-x32 of=out_objdump_text bs=1 count=$((0x0009eb00)) skip=$((0x00001000))
```

I wonder what would happen if we ran that command on the `.data` header:
```
$ objdump -h pass_manager-x32 | grep .data | awk '{print "dd if=pass_manager-x32 of=out_objdump_data bs=1 count=$((0x"$3")) skip=$((0x"$6"))"}'
dd if=pass_manager-x32 of=out_objdump_data bs=1 count=$((0x0005cd67)) skip=$((0x000a0000))
dd if=pass_manager-x32 of=out_objdump_data bs=1 count=$((0x0000b460)) skip=$((0x00141000))
dd if=pass_manager-x32 of=out_objdump_data bs=1 count=$((0x00003008)) skip=$((0x0014c460))
```
Okay let's try one of those commands: 
```
$ dd if=pass_manager-x32 of=out_objdump_data bs=1 count=$((0x0005cd67)) skip=$((0x000a0000))
380263+0 records in
380263+0 records out
380263 bytes (380 kB, 371 KiB) copied, 0.384636 s, 989 kB/s
```
So it's getting something but I still don't know how to read it.

I installed a hex editor called `hexedit` by Apache, but I think this GUI tool, [ghex](https://github.com/GNOME/ghex/blob/master/HACKING) might be easier to utilize at least at first.
Hmmm. I see some words:
```
Multiply, December, September
```
Those three `.data` dumps let's run the other two, generating additional files by changing the name:
```
dd if=pass_manager-x32 of=out_objdump_data2 bs=1 count=$((0x0000b460)) skip=$((0x00141000))
dd if=pass_manager-x32 of=out_objdump_data3 bs=1 count=$((0x00003008)) skip=$((0x0014c460))
```
(Count is how much to take and skip is where to start)
Not much ascii in those.

Hmmm could the UUID they said to use be in any of these files? `$ hd out_objdump_text | grep 34678beb895f9a9b61acef375dcd7375` etc... No.
What if we searched for "pass":
```
$ hd out_objdump_data | grep pass
0004f970  65 20 70 61 73 73 65 64  20 74 6f 20 54 79 70 65  |e passed to Type|
00050db0  65 20 70 61 73 73 65 64  20 74 6f 20 54 79 70 65  |e passed to Type|
00050df0  65 20 70 61 73 73 65 64  20 74 6f 20 54 79 70 65  |e passed to Type|
00051280  20 31 20 70 61 73 73 77  6f 72 64 20 73 74 6f 72  | 1 password stor|
00052c30  65 72 66 61 63 65 20 74  79 70 65 20 70 61 73 73  |erface type pass|
00052ec0  61 73 74 65 72 20 70 61  73 73 77 6f 72 64 20 74  |aster password t|
```

In the first `data` dump there doesn't seem to be a [file signature](https://en.wikipedia.org/wiki/List_of_file_signatures).
Found this on [so](https://stackoverflow.com/a/30452453/2223106)
> You should prefer readelf when possible since objdump simply does not show some sections like .symtab: Why does objdump not show .bss, .shstratab, .symtab and .strtab sections?
> You can also extract the raw bytes with the techniques mentioned at: [How do you extract only the contents of an ELF section](https://stackoverflow.com/questions/3925075/how-to-extract-only-the-raw-contents-of-an-elf-section) and as mentioned by ysdx.

What would copying the sections do?
```
objcopy --dump-section .text=input.data.bin --dump-section .text=input.text.bin pass_manager-x32 /dev/null
```

Those files have different headers but also not ones in the list of file signatures.

[ELF Mangler](https://github.com/acolomb/elf-mangle) looks interesting.

[How to read and convert hex dumps](https://hextoascii.co/articles/how-to-read-convert-hex-dumps) and it recommends the `xxd` utility which I installed with `sudo apt install xxd` but not sure if it's necessary as we have a bunch of other similar tools at this point. He also mentions `od` or Octal Dump.

Hmmm the `strings` utility (referenced [in the yt video](https://www.youtube.com/watch?v=FNyo1CSxBrg)) output looks interesting: 
```
strings pass_manager-x32 | grep pass
runtime.SetFinalizer: cannot pass 
reflect: nil type passed to Type.Implements
reflect: nil type passed to Type.AssignableTo
reflect: nil type passed to Type.ConvertibleTo
Welcome back! You currently have 1 password stored:
reflect: non-interface type passed to Type.Implements
Simple Password Manager. Enter master password to begin: 
runtime.mapassign1
reflect.mapassign
secure_passmgr.go
```

The leftmost column is the location so the 1 password part is at `00051280`.

Okay this is interesting:
```
$ strings out_objdump_data | grep pass
runtime.SetFinalizer: cannot pass 
reflect: nil type passed to Type.Implements
reflect: nil type passed to Type.AssignableTo
reflect: nil type passed to Type.ConvertibleTo
Welcome back! You currently have 1 password stored:
reflect: non-interface type passed to Type.Implements
Simple Password Manager. Enter master password to begin: 
```

And there is this:
```
$ hd out_objdump_data | grep pass
0004f970  65 20 70 61 73 73 65 64  20 74 6f 20 54 79 70 65  |e passed to Type|
00050db0  65 20 70 61 73 73 65 64  20 74 6f 20 54 79 70 65  |e passed to Type|
00050df0  65 20 70 61 73 73 65 64  20 74 6f 20 54 79 70 65  |e passed to Type|
00051280  20 31 20 70 61 73 73 77  6f 72 64 20 73 74 6f 72  | 1 password stor|
00052c30  65 72 66 61 63 65 20 74  79 70 65 20 70 61 73 73  |erface type pass|
00052ec0  61 73 74 65 72 20 70 61  73 73 77 6f 72 64 20 74  |aster password t|
```

In `ghex` I scrolled down to the `00051260` line and found in the ascii column "Welcome back... 1 password stored" and confirmed the hex values match with python:
```
>>> hex(ord("W"))
'0x57'
>>> hex(ord("e"))
'0x65'
>>> hex(ord(":"))
'0x3a'
```
Or
```
>>> for x in [0x57, 0x65, 0x6c, 0x63, 0x6f]: print(chr(x))
... 
W
e
l
c
o
```
Unfortunately following the colon it's just a bunch of zeroes and then the next string: `[]struct`. Fuck.

There's a check security utility:
```
$ checksec --file=pass_manager-x32
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFYFortified	Fortifiable	FILE
No RELRO        No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols	  No	00		pass_manager-x32
```

Here's a [medium article](https://medium.com/@elmin.farzaliyev/elf-files-unmasked-a-practical-guide-15b9036b9a01) about reverse engineering elf files. The article mentions a util called [gdb](http://www.gnu.org/software/gdb/documentation/). The gdb docs are [here](https://sourceware.org/gdb/current/onlinedocs/gdb.html/).

Okay made the file executable `chmod u+x pass_manager-x32` and can now run:
```
mike@oduwa:~/cyber$ ./pass_manager-x32 
usage: ./pass_manager-x32 <uid>
```
Okay they gave us a uid:
```
mike@oduwa:~/cyber$ ./pass_manager-x32 34678beb895f9a9b61acef375dcd7375
Simple Password Manager. Enter master password to begin: 
-> password
Intruder alert!
```

Run it again and don't enter a password. While running, inspect with gdb:
```
$ gdb pass_manager-x32 
GNU gdb (Debian 13.1-3) 13.1
Copyright (C) 2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from pass_manager-x32...
(No debugging symbols found in pass_manager-x32)
(gdb)
(gdb) show language
The current source language is "auto; currently c". 
```