#!/usr/bin/env python
"""
Display a simple timer in the console
"""
import time
import sys
import math
# TODO maybe implement multiline flushing https://stackoverflow.com/a/6840469/2223106

minutes = 300 // 60
if len(sys.argv) < 2:
    print("""
         Defaulting to a five minute timer.
         """)
else:
    minutes = int(sys.argv[1])
    print("Counting down %d minute%s." % (minutes, "" if minutes == 1 else "s"))
seconds = minutes * 60
for remaining in range(seconds, 0, -5):
    sys.stdout.write("\r")
    color = "\033[0;32m" if remaining / seconds >= .6 else "\033[0;36m" if remaining / seconds >= .4 else "\033[0;33m" if remaining / seconds >= .25 else "\033[0;31m" #green else if .5 yellow else red
    sys.stdout.write("{} {:}:{:02} {}".format(color, remaining // 60, remaining % 60, (math.floor(remaining / 5) * "x")))
    sys.stdout.flush()
    time.sleep(5)

sys.stdout.write("\r\033[0mComplete!            \n") # reset
