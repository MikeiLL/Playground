"""

"""
from collections import Counter
code = [254, 232, 213, 227, 214, 222, 210, 167, 222, 232, 235, 235, 167, 209, 236, 225, 214, 214, 211, 167, 237, 214, 209, 167, 224, 213, 167, 220, 215, 227, 224, 211, 236, 167, 232, 213, 167, 145, 145, 167, 212, 232, 213, 220, 211, 236, 210]
ct = Counter(code)
from pprint import pprint
word2 = [222, 232, 235, 235,]
pprint(ct)
'''
>>> min(code)
145
>>> max(code)
254
>>> ord("A")
65
>>> ord("z")
122
>>> ord(".")
46
>>> ord(" ")
32
>>> ord("e")
101
>>> ord("I")
73
>>> ord("a")
97
>>> ord("o")
111
>>> ord("!")
33

Counter({167: 8,
         232: 4,
         213: 4,
         214: 4,
         236: 3,
         211: 3,
         227: 2,
         222: 2,
         210: 2,
         235: 2,
         209: 2,
         224: 2,
         220: 2,
         145: 2,
         254: 1,
         225: 1,
         237: 1,
         215: 1,
         212: 1})
'''

space = 32
upper_case_start_at = 65
lower_case_end_at = 122
# 122 - 32 = 90 so
# range btwn chars is 90
# 254 - 145 range between numbers in code: 109
# upper case Z = 90
'''
The most common letters in English, from most to least frequent, are E, T, A, O, I, N, S, H, R, and D. The letter E appears in about 12.7% of words, making it the most frequently used letter.
'''

import re
# may need to install wordlist with apt
file = open("/usr/share/dict/words", "r")
words = re.sub("[^\w]", " ",  file.read()).split()
file.close()
    
def is_word(word):
    return word.lower() in words

for n in range(50, 159):
    msg = ""
    for x in word2:
        if x-n < 32: print("below 32")
        else: msg += chr(x - n)
    if is_word(msg):
        print("Message: " + msg+"\n")
    else: print("-")

