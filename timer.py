#!/usr/bin/env python
import time
import sys

for remaining in range(5, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(50)

sys.stdout.write("\rComplete!            \n")
