'''
Use a hash map to store the last index of each character.
use 'left' and 'right' index indicators to evaluate contents of a siding window
loop through the string by right index
  AND within the loop
    IF (
          char IS NOT present in the map,
          OR left has already moved passed its mapped value
        )
      set/add it at the index of ch (right)
    increment right index by (one more than the difference between right and left)
    IF window size > longest, incremenet longest
    ELSE (char IS present)
      set left to the index of the char->value in the map + 1
    set the index of the char in the map to the current index
    increment right index
return longest
'''

def lols(s: str) -> int:
    charMap = {}
    longest = 0
    left = 0
    for right in range(len(s)):
        if s[right] not in charMap or charMap[s[right]] < left:
            charMap[s[right]] = right
            longest = max(longest, right - left + 1)
        else:
            left = charMap[s[right]] + 1
            charMap[s[right]] = right
    return longest

print(lols("aaclaxlphabbb") == 6) # claxlp
print(lols("aaclaxlphabygbb") == 8) # xlphabyg
print(lols("") == 0)
print(lols("pphapahabyzygaaabb") == 5) # habyz
print(lols("aaclaxlphabayglphabygaaabb") == 7) # bayglph
