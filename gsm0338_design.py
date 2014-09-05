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
from pprint import pprint

import findhash
import gsm0338_parse

def parse_shift_table(stream):
    for line in stream:
        line = line.strip('\n\r')
        if len(line) > 1:
            line = line.encode('utf-8').decode('unicode_escape')
        elif len(line) == 0:
            line = ' '
        yield line

def read_locking_7bit(filename):
    locking_dict = {}
    with open(filename, 'r', encoding='utf-8-sig') as f:
        for i, line in enumerate(parse_shift_table(f)):
            line_int = ord(line)
            if line_int != i:
                locking_dict[i] = line_int
    return locking_dict

def print_tables(tables):
    for table in tables:
        max_value = max(table)
        for i, x in enumerate(table):
            if i % 16 == 0:
                print()
            if max_value > 0xFFFF:
                print("0x{0:08X}, ".format(x), end='')
            elif max_value > 0xFF:
                print("0x{0:04X}, ".format(x), end='')
            else:
                print("0x{0:02X}, ".format(x), end='')
        print()

def max_size_for_data(data):
    max_value = max(data)
    if max_value > 0xFFFF:
        return 0xFFFFFFFF
    elif max_value > 0xFF:
        return 0xFFFF
    else:
        return 0xFF

def make_hash(data_dict, input_bits, hash_bits, hash_shifts, find_collision_free = True, find_best = True, select_manual = None, invalid_fill_values = None):
    def hash_functions_gen():
        return findhash.shift_functions_gen(-input_bits + 1, hash_bits + hash_shifts, hash_shifts, 2**hash_bits)

    # All collision-free hashes
    if find_collision_free:
        print('\nAll collision-free hashes:')
        collision_free = []
        for result in findhash.find_collision_free_hashes(data_dict, hash_functions_gen()):
            collision_free.append(result)
            print(result, result['f'].__doc__)

    # "best" hash
    if find_best:
        print('\n"Best" hashes:')
        (best_size_result, best_collision_result) = findhash.find_best_hash(data_dict, hash_functions_gen())
        print(best_size_result, best_size_result['f'].__doc__)
        print(best_collision_result, best_collision_result['f'].__doc__)

    if select_manual == None:
        # Use "best"
        best_result = best_collision_result
    else:
        # Manually select the most appealing of the collision-free hashes
        best_result = collision_free[select_manual]
    f = best_result['f']
    
    if invalid_fill_values == None:
        invalid_fill_values = range(max_size_for_data(data_dict), -1, -1)
    hash_lookup = findhash.make_hash_lookup(data_dict, f, invalid_fill_values)
    hash_data = findhash.make_hash_data(data_dict, f, max_size_for_data(data_dict.values()))
    
    print("\nTables with function {0}".format(f.__doc__))
    print_tables( (hash_lookup, hash_data) )

def make_unicode_to_7bit_hash(input_type_max = 0xFFFF):
    unicode_data = gsm0338_parse.read_unicode_data()
    unicode_dict = dict((unicode, gsm) for (unicode, gsm, comment) in unicode_data)

    invalid_fill_values = range(input_type_max, -1, -1)
    #invalid_fill_values = range(0xFFFF, 0, -0x1111)
    #invalid_fill_values = range(0, 0x10000, 0x1111)
    #invalid_fill_values = range(0xFFF0, 0, -0x1110)

    make_hash(unicode_dict, 16, 8, 3, True, True, 0, invalid_fill_values)

def make_7bit_to_unicode_hash():
    default_7bit_data = gsm0338_parse.read_7bit_data()
    default_7bit_dict = dict((gsm, unicode) for (gsm, unicode, comment) in default_7bit_data)

    make_hash(default_7bit_dict, 8, 6, 3, True, True, 1)

def make_7bit_escape_to_unicode_hash():
    escape_data = gsm0338_parse.read_escape_data()
    escape_dict = dict((gsm, unicode) for (gsm, unicode, comment) in escape_data)

    make_hash(escape_dict, 8, 4, 3, True, True, 0)

def make_7bit_portuguese_to_unicode_hash():
    default_7bit_dict = read_locking_7bit('tables/portuguese_locking_shift.txt')

    make_hash(default_7bit_dict, 8, 6, 3, True, True, 1)

def make_7bit_turkish_to_unicode_hash():
    default_7bit_dict = read_locking_7bit('tables/turkish_locking_shift.txt')

    make_hash(default_7bit_dict, 8, 6, 3, True, True, 1)

if __name__ == "__main__":
    make_unicode_to_7bit_hash()
    #make_7bit_to_unicode_hash()
    #make_7bit_escape_to_unicode_hash()
    #make_7bit_portuguese_to_unicode_hash()
    #make_7bit_turkish_to_unicode_hash()
