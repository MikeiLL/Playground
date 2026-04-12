
code = "01001001 00100000 01100001 01101101 00100000 01010111 01010110 00101110 00100000 01001100 01100101 01110100 01110011 00100000 01100111 01100101 01110100 00100000 01110100 01101000 01100101 01100001 01110100 01110010 01101001 01100011 01100001 01101100 00100001".split(' ')

decrypted = ""
for c in code: decrypted += chr(int(c,2))

print(decrypted)

# Better yet
''.join([chr(int(c,2)) for c in code])

code = [int(n) for n in "104 141 162 151 156 147 40 144 165 143 153 40 157 146 40 145 156 151 147 155 141 54 40 114 165 155 151 156 141 162 171 40 157 146 40 144 145 154 151 147 150 164".split(' ')]
''.join([chr(c) for c in code])

code = [int(n,16) for n in "48 65 20 69 73 20 74 68 65 20 63 68 69 6c 6c 20 74 68 61 74 20 63 68 6f 6b 65 73 20 69 6e 20 74 68 65 20 61 69 72 21"]

import base64
base64.b64decode('VGhleSBjYWxsIG1lIE1lZ2F2b2x0LiBUaGlzIGlzIG15IHBhcnRuZXIgVi5JLg==')

code = [int(c, 16) for c in "4d 54 49 30 49 44 45 31 4d 43 41 78 4e 44 55 67 4d 54 63 78 49 44 41 30 4d 43 41 78 4e 44 4d 67 4d 54 51 78 49 44 45 31 4e 43 41 78 4e 54 51 67 4d 44 51 77 49 44 45 31 4e 53 41 78 4e 44 55 67 4d 44 51 77 49 44 45 78 4d 43 41 78 4e 44 55 67 4d 54 51 78 49 44 45 32 4e 43 41 78 4e 6a 63 67 4d 54 51 78 49 44 45 32 4e 69 41 78 4e 44 55 67 4d 44 55 32 49 44 41 30 4d 43 41 78 4d 6a 51 67 4d 54 55 77 49 44 45 31 4d 53 41 78 4e 6a 4d 67 4d 44 51 77 49 44 45 31 4d 53 41 78 4e 6a 4d 67 4d 44 51 77 49 44 45 31 4e 53 41 78 4e 7a 45 67 4d 44 51 77 49 44 45 32 4d 43 41 78 4e 44 45 67 4d 54 59 79 49 44 45 32 4e 43 41 78 4e 54 59 67 4d 54 51 31 49 44 45 32 4d 69 41 77 4e 44 41 67 4d 54 49 77 49 44 41 31 4e 69 41 78 4d 6a 55 67 4d 44 55 32".split(' ')]

pigpencipyerdecrypt = {"https://www.dcode.fr/tools/pigpen/images/char(65).png": "A",
                       #...
                "https://www.dcode.fr/tools/pigpen/images/char(90).png": "Z"
                }
""" 
meet tonight at midnght 
location outside UmBRCALE x GARDENS x 
UNDER x THE x  ASSUT x BRIDGE x  
THE x ?Ol x IS x IN x A x FA?SE x BRIC? x 
A?ONG x THE x WALL x 
ONCE x ?OU x ARE x INSIDE x ?HEN x AS?ED x 
THE x PHE x PASS?ORD x IS x ?AN?IBAR
FRot0: M
FFlip: L
FRot2: K
FRot1: W
FRot1Flip: Z
"""