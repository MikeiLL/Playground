#!/etc/bin python
"""
Read input csv file and for each line, promt to keep or archive.
Keep will write to one file, archive will write to another.
Want to also track, one way or another, what remains to parse -
in case process is not completed in single session.
Perhaps best way to do this is to initially copy the entire input file
and write it out to a TODO file, removing each line from the TODO file
once either archived or kept.
The brings up the question of, what about postponed decisions, where
there isn't an obvious yes or no answer.
"""

import csv
import sys
import time
import datetime as dt
import requests

if len(sys.argv) < 2:
  print("Usage: archive_or_keep.py inputfile.csv")
  sys.exit

INPUT_FILE = sys.argv[1]
QUIT_FOR_NOW = False
NOW = dt.datetime.now().strftime('%Y-%m-%dat%H:%M:%S')
""" ANSI color codes """
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"

with open(INPUT_FILE, newline='') as i:
  data = csv.reader(i, delimiter=',', quotechar='|')
  for idx, row in enumerate(data):
    try:
      if not QUIT_FOR_NOW:
        if not row[0].startswith("http"):
          print("Adding note")
          time.sleep(0.5)
          with open("vaultexports/NOTES.csv", 'a', newline='') as notes:
              writer = csv.writer(notes, delimiter=',',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
              writer.writerow(row)
              continue
        print(f"{row[1]} on {row[0].split("//")[1][:22]}") # Web Site
        try:
          print("CONNECTING...")
          r = requests.head(row[0], timeout=2)
          if r.status_code <= 200 and r.status_code >= 300: color = GREEN
          elif r.status_code >= 500: color = RED
          else: color = YELLOW
          print(f"STATUS: {color}{r.status_code}\033[0m")
        except Exception as e:
          print(f"\033[0;33mCould not connect to site: {row[0]} ({e})\033[0m")
        selection = input(f"#{idx}: \033[0;32mk\033[0m=keep; \033[0;31ma\033[0m=archive; \033[0;36m\033[0md=discard; \033[0;36m\033[0mu=undecided; \033[0;34mq\033[0m=quit; \033[0;33mi\033[0m=mark for inspection. \033[0m\n")
        passwd_len = len(row[2])
        #See if it's even valid
        if selection == 'q':
          QUIT_FOR_NOW = True
          continue
        if selection == 'd': print(f'Discarding {row[0].split("//")[1][:22]}'); continue
        elif selection in ['k','i']:
          print("\033[0;33mKeeping\033[0m\n")
          with open("vaultexports/keep.csv", 'a', newline='') as k:
              writer = csv.writer(k, delimiter=',',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
              writer.writerow(row)
              if selection == 'i':
                with open("vaultexports/inspect.csv", 'a', newline='') as k:
                  writer = csv.writer(k, delimiter=',',
                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
                  writer.writerow(row)
              if passwd_len >= 12 or "jaco" in row[2] or "mingus" in row[2]:
                print("\033[0;33mInsecure Passwd Alert\033[0m (storing in file)\n")
                with open("vaultexports/insecure.csv", 'a', newline='') as k:
                  writer = csv.writer(k, delimiter=',',
                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
                  writer.writerow(row)
        elif selection == 'a':
          print("\033[0;31mArchiving\033[0m\n")
          with open("vaultexports/archive.csv", 'a', newline='') as k:
              writer = csv.writer(k, delimiter=',',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
              writer.writerow(row)
        elif selection == 'u':
          print("Undecided")
          with open("vaultexports/undecided.csv", 'a', newline='') as k:
              writer = csv.writer(k, delimiter=',',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
              writer.writerow(row)
        else:
          print("\033[0;31mArchiving by default\033[0m\n")
          with open("vaultexports/archive.csv", 'a', newline='') as k:
              writer = csv.writer(k, delimiter=',',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
              writer.writerow(row)
      else: #QUIT
          filepath = "vaultexports/unparsed_"+ NOW + ".csv"
          with open(filepath, 'a', newline='') as k:
            writer = csv.writer(k, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
            continue
          print(f"Done for now. Continue later with \033[0;32m{filepath}\033[0m\n")
    except IndexError:
      print("############\n\tBad one at line", idx)
      print(row)
      print("\n###############\n")
