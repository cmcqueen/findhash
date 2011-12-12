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

def make_unicode_to_7bit_hash(input_type_max = 0xFFFF):
    def hash_functions_gen():
        return findhash.shift_functions_gen(-15, 19, 3, 256)

    unicode_data = gsm0338_parse.read_unicode_data()
    unicode_dict = dict((unicode, gsm) for (unicode, gsm, comment) in unicode_data)

    # All collision-free hashes
    if 1:
        print('\nAll collision-free hashes:')
        collision_free = []
        for result in findhash.find_collision_free_hashes(unicode_dict, hash_functions_gen()):
            collision_free.append(result)
            print(result, result['f'].__doc__)

    # "best" hash
    if 1:
        print('\n"Best" hashes:')
        (best_size_result, best_collision_result) = findhash.find_best_hash(unicode_dict, hash_functions_gen())
        print(best_size_result, best_size_result['f'].__doc__)
        print(best_collision_result, best_collision_result['f'].__doc__)

    if 0:
        # Use "best"
        best_result = best_collision_result
    else:
        # Manually select the most appealing of the collision-free hashes
        best_result = collision_free[0]
    f = best_result['f']
    
    invalid_fill_values = range(input_type_max, -1, -1)
    #invalid_fill_values = range(0xFFFF, 0, -0x1111)
    #invalid_fill_values = range(0, 0x10000, 0x1111)
    #invalid_fill_values = range(0xFFF0, 0, -0x1110)
    hash_lookup = findhash.make_hash_lookup(unicode_dict, f, invalid_fill_values)
    hash_data = findhash.make_hash_data(unicode_dict, f, 0xFF)

    print("\nTables with function {0}".format(f.__doc__))
    for i, x in enumerate(hash_lookup):
        if i % 16 == 0:
            print()
        print("0x{0:04X},".format(x), end='')
    
    print()
    for i, x in enumerate(hash_data):
        if i % 16 == 0:
            print()
        print("0x{0:02X},".format(x), end='')

def make_7bit_to_unicode_hash(input_type_max = 0xFF):
    def hash_functions_gen():
        return findhash.shift_functions_gen(-7, 11, 3, 64)

    default_7bit_data = gsm0338_parse.read_7bit_data()
    default_7bit_dict = dict((gsm, unicode) for (gsm, unicode, comment) in default_7bit_data)

    # All collision-free hashes
    if 1:
        print('\nAll collision-free hashes:')
        collision_free = []
        for result in findhash.find_collision_free_hashes(default_7bit_dict, hash_functions_gen()):
            collision_free.append(result)
            print(result, result['f'].__doc__)

    # "best" hash
    if 1:
        print('\n"Best" hashes:')
        (best_size_result, best_collision_result) = findhash.find_best_hash(default_7bit_dict, hash_functions_gen())
        print(best_size_result, best_size_result['f'].__doc__)
        print(best_collision_result, best_collision_result['f'].__doc__)

    if 0:
        # Use "best"
        best_result = best_collision_result
    else:
        # Manually select the most appealing of the collision-free hashes
        best_result = collision_free[1]
    f = best_result['f']
    
    invalid_fill_values = range(input_type_max, -1, -1)
    hash_lookup = findhash.make_hash_lookup(default_7bit_dict, f, invalid_fill_values)
    hash_data = findhash.make_hash_data(default_7bit_dict, f, 0xFFFF)

    print("\nTables with function {0}".format(f.__doc__))
    for i, x in enumerate(hash_lookup):
        if i % 16 == 0:
            print()
        print("0x{0:02X},".format(x), end='')

    print()
    for i, x in enumerate(hash_data):
        if i % 16 == 0:
            print()
        print("0x{0:04X},".format(x), end='')

def make_7bit_escape_to_unicode_hash(input_type_max = 0xFF):
    def hash_functions_gen():
        return findhash.shift_functions_gen(-3, 7, 3, 16)

    escape_data = gsm0338_parse.read_escape_data()
    escape_dict = dict((gsm, unicode) for (gsm, unicode, comment) in escape_data)

    # All collision-free hashes
    if 1:
        print('\nAll collision-free hashes:')
        collision_free = []
        for result in findhash.find_collision_free_hashes(escape_dict, hash_functions_gen()):
            collision_free.append(result)
            print(result, result['f'].__doc__)

    # "best" hash
    if 1:
        print('\n"Best" hashes:')
        (best_size_result, best_collision_result) = findhash.find_best_hash(escape_dict, hash_functions_gen())
        print(best_size_result, best_size_result['f'].__doc__)
        print(best_collision_result, best_collision_result['f'].__doc__)

    if 0:
        # Use "best"
        best_result = best_collision_result
    else:
        # Manually select the most appealing of the collision-free hashes
        best_result = collision_free[0]
    f = best_result['f']
    
    invalid_fill_values = range(input_type_max, -1, -1)
    hash_lookup = findhash.make_hash_lookup(escape_dict, f, invalid_fill_values)
    hash_data = findhash.make_hash_data(escape_dict, f, 0xFFFF)

    print("\nTables with function {0}".format(f.__doc__))
    for i, x in enumerate(hash_lookup):
        if i % 16 == 0:
            print()
        print("0x{0:02X},".format(x), end='')

    print()
    for i, x in enumerate(hash_data):
        if i % 16 == 0:
            print()
        print("0x{0:04X},".format(x), end='')

if __name__ == "__main__":
    make_unicode_to_7bit_hash()
    #make_7bit_to_unicode_hash()
    #make_7bit_escape_to_unicode_hash()
