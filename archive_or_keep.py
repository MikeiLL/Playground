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

if len(sys.argv) < 2:
  print("Usage: archive_or_keep.py inputfile.csv")
  sys.exit

INPUT_FILE = sys.argv[1]
QUIT_FOR_NOW = False
TODAY = dt.date.today().strftime('%F')
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
      if not QUIT_FOR_NOW:
        try:
          if (not row[0].startswith("http")):
            print("Adding note")
            time.sleep(0.5)
            with open("NOTES.csv", 'w', newline='') as notes:
                writer = csv.writer(notes, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)
                continue
          print(f"{row[1]} on {row[0].split("//")[1][:22]}") # Web Site
          selection = input(f"#{idx}: \033[0;32mk\033[0m=keep; \033[0;31ma\033[0m=archive; \033[0;36m\033[0mu=undecided; \033[0;34mq\033[0m=quit; \033[0;33mi\033[0m=mark for inspection. \033[0m\n")
          passwd_len = len(row[2])
          if QUIT_FOR_NOW or selection == 'q':
            QUIT_FOR_NOW = True
            with open(INPUT_FILE +"_"+ TODAY + "_unparsed.csv", 'w', newline='') as k:
              writer = csv.writer(k, delimiter=',',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
              writer.writerow(row)
              print(f"Done for now. Continue later with \033[0;32m{INPUT_FILE +"_"+ TODAY + "_unparsed.csv"}\033[0m\n")
          elif selection in ['k','i']:
            print("\033[0;33mKeeping\033[0m\n")
            with open(INPUT_FILE + "_keep.csv", 'w', newline='') as k:
                writer = csv.writer(k, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)
                if selection == 'i':
                  with open(INPUT_FILE + "_inspect.csv", 'w', newline='') as k:
                    writer = csv.writer(k, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(row)
                if passwd_len >= 12 or "jaco" in row[2] or "mingus" in row[2]:
                  print("\033[0;33mInsecure Passwd Alert\033[0m (storing in file)\n")
                  with open(INPUT_FILE + "_insecure.csv", 'w', newline='') as k:
                    writer = csv.writer(k, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(row)
          elif selection == 'a':
            print("\033[0;31mArchiving\033[0m\n")
            with open(INPUT_FILE + "_archive.csv", 'w', newline='') as k:
                writer = csv.writer(k, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)
          elif selection == 'u':
            print("Undecided")
            with open(INPUT_FILE + "_wait.csv", 'w', newline='') as k:
                writer = csv.writer(k, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)
        except IndexError:
          print("############\n\tBad one at line", idx)
          print(row)
          print("\n###############\n")
