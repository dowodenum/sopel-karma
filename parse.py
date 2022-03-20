#!/bin/python3

# Extract karma values from Limnoria-karma.
# Amounts over a certain ++ threshold are formatted for
# importing into dowodenum/sopel-karma.py
# via the command:
# .setkarma <nick> <incremented> <decremented>

import re, sys

file = sys.argv[1]
threshold = int(sys.argv[2])

with open(file, 'r') as datFile:
    lines = datFile.readlines()

for line in lines:
    match = re.search(r',\d+,', line)
    match = match.group(0).replace(',','')
    incremented = int(match)
    if incremented > threshold:
        print('.setkarma ' + ' '.join(line.split(',')))
