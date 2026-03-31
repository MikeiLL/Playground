import random
strings = ["metropolis", "admin"]
substitutions = {
    "a": "@",
    "e": 3,
    "i": 1,
    "o": 0,
    "s": 5,
    "l": 1,
}

blank = ""
ct = 0
variations = set()
while len(variations) < 50:
    for ch in list(strings[0]):
        if random.randint(0,1): blank += chr(ord(ch) - 32)
        else:
            if random.randint(0,1):
                if ch in substitutions:
                    blank += str(substitutions[ch])
                else: blank += ch
            else:
                if ch in substitutions:
                    blank += str(substitutions[ch])
                else: blank += ch

    variations.add(blank)
    blank = ""

for var in variations: print(var)
