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

if len(sys.argv) < 2:
  print("Usage: archive_or_keep.py inputfile.csv")
  sys.exit

input_file = sys.argv[1]

with open(input_file, newline='') as i:
    data = csv.reader(i, delimiter=',', quotechar='|')
    for idx, row in enumerate(data):
        try:
          if (not row[0].startswith("http")):
             print("Adding note")
             time.sleep(0.5)
             with open("NOTES.csv", 'w', newline='') as notes:
                writer = csv.writer(notes, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)
                continue
          print(row)
          selection = input("input k=keep; a=archive; u=undecided; x=exit; i=mark for inspection")
          if selection in ['k','i']:
             print("Keeping")
             with open(input_file + "_keep.csv", 'w', newline='') as k:
                writer = csv.writer(k, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)
                if selection == 'i':
                  with open(input_file + "_inspect.csv", 'w', newline='') as k:
                    writer = csv.writer(k, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(row)
          elif selection == 'a':
             print("Archiving")
             with open(input_file + "_archive.csv", 'w', newline='') as k:
                writer = csv.writer(k, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)
          elif selection == 'u':
             print("Undecided")
             with open(input_file + "_wait.csv", 'w', newline='') as k:
                writer = csv.writer(k, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)
          elif selection == 'x':
             print("Exiting")
             """
             Now break out of the loop and write all the rest of the file out to a new file with today's date
             TODO
             """
             with open(input_file + "_unparsed.csv", 'w', newline='') as k:
                writer = csv.writer(k, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)
        except IndexError:
           print("############\n\tBad one at line", idx)
           print(row)
           print("\n###############\n")
