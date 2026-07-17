#!/usr/bin/env
import time
import psutil
import random
"""
Hog memory (slowly)
Output:
71.4
300000000
81.0
400000000
TODO: make it hog memory faster, perhaps by appending something other than integers.
Would also be good to display how quickly memory is getting depleted.
x = time
y = memory used
Use time.process_time() (to disregard sleep time) or time.perf_counter() (to include sleep time).
"""
growing = []
start = time.process_time()
mem = psutil.virtual_memory()
lastmem = mem.percent
lasttime = start
while True and mem.percent < 90.0:
    growing.append(random.randint(1,4000))
    if len(growing) % 1000**2 == 0:
        mem = psutil.virtual_memory()
        now = time.process_time()
        current_process_time = now - start
        print("Memory: %s" % mem.percent)
        print("Length of array: %s" % len(growing))
        print((mem.percent - lastmem) / (current_process_time - lasttime))
        lasttime = current_process_time
        lastmem = mem.percent
        time.sleep(0.5)
