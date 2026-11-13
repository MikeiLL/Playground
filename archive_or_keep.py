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

if len(sys.argv) < 2:
  print("Usage: archive_or_keep.py inputfile.csv")
  sys.exit

input_file = sys.argv[1]

with open(input_file, newline='') as i:
    data = csv.reader(i, delimiter=',', quotechar='|')
    for idx, row in enumerate(data):
        try:
          print(row)
        except IndexError:
           print("############\n\tBad one at line", idx)
           print(row)
           print("\n###############\n")
