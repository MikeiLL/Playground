'''
Use a hash map to store the last index of each character.
use 'left' and 'right' index indicators to evaluate contents of a siding window
loop through the string by right index
  AND within the loop
    IF char IS NOT present in the map,
      add it at the index of ch
    increment right index
    IF window size > longest, incremenet longest
    IF char IS present
      set left to the index of the char in the map + 1
    set the index of the char in the map to the current index
    increment right index
return longest
'''

def lols(s: str) -> int:
    n = len(s)
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
        #print(charMap)
    return longest

print(lols("aaclaxlphabbb")) # 6
print(lols("aaclaxlphabygbb")) # 8
print(lols("")) # 0
print(lols("aaclaxlphabyglphabygaaabb")) # 8
print(lols("aaclaxlphabayglphabygaaabb")) # 7
