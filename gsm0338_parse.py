#!/usr/bin/env python3
"""
Python 3.x program

Parse GSM0338.TXT file to generate C code for SMS handling of GSM 03.38 which
specifies SMS 7-bit alphabet. C code tables are needed for:

* Unicode to 7-bit alphabet mapping
* 7-bit alphabet to Unicode mapping

GSM0338.TXT file is from Unicode web site:
    http://unicode.org/Public/MAPPINGS/ETSI/GSM0338.TXT
"""

# Standard Python modules
import re
from pprint import pprint
from collections import defaultdict

GSM0338_FILENAME = 'GSM0338.TXT'

# Regular expression for mapping table entries. Matches 7-bit code values, Unicode value, comment
line_re = re.compile(r'^\#?0x([0-9a-fA-F]{2})([0-9a-fA-F]*)\s+0x([0-9a-fA-F]{4})\s+\#\s+(.*)$')

def parse_line(line):
    match = line_re.match(line)
    if match:
        #print match.groups()
        gsm1, gsm2, uni, comment = match.groups()
        gsm1 = int(gsm1, 16)
        if gsm2:
            gsm2 = int(gsm2, 16)
        else:
            gsm2 = 0
        uni = int(uni, 16)
        return (gsm1, gsm2, uni, comment)

def read_data(include_commented = False):

    data = []

    with open(GSM0338_FILENAME) as f:
        for line in f:
            if not include_commented and line[0] == '#':
                continue
            parsed = parse_line(line)
            if parsed:
                data.append(parsed)
    return data

def read_unicode_data(include_commented = True):

    data = []

    for row in read_data(include_commented):
        (gsm1, gsm2, uni, comment) = row
        if gsm2:
            if gsm1 != 0x1b:
                raise Exception("Unexpected gsm1 value")
            gsm1 = gsm2 + 128
        data.append((uni, gsm1, comment))
    return data

def read_escape_data():
    data = []
    
    for row in read_data():
        (gsm1, gsm2, uni, comment) = row
        if gsm2:
            if gsm1 != 0x1b:
                raise Exception("Unexpected gsm1 value")
            data.append((gsm2, uni, comment))
    return data

def read_7bit_data():
    data = []

    for row in read_data():
        (gsm1, gsm2, uni, comment) = row
        if not gsm2 and gsm1 != uni:
            data.append((gsm1, uni, comment))
    return data

def make_7bit_to_unicode_table_old():

    #pprint(read_data())
    pprint(read_7bit_data())

if __name__ == "__main__":
    make_7bit_to_unicode_table_old()
