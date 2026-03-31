alpha = [150, 115, 160, 56, 153, 36, 222, 50, 172, 1, 3, 3, 7]
beta = [197, 56, 249, 21, 202, 103, 146, 115, 129, 55, 59, 48, 55]
astring = ""
for n in alpha: astring += chr(n)
astring
#'\x96s\xa08\x99$Þ2¬\x01\x03\x03\x07'
chr(197)
chr(150)
for a, b in zip(alpha, beta): astring += chr(a^b)
