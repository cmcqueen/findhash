
"""
Python 2.x program

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

def make_hash_lookup(o, hash_function, invalid_value_iter):
    hash_lookup = dict()
    for i in o:
        hash = hash_function(i)
        hash_lookup[hash] = i

    # Find a suitable "invalid" value to fill the holes
    for i in invalid_value_iter:
        if hash_lookup.get(hash_function(i), i) != i:
            default_value = i
            break
    else:
        raise Exception("Couldn't find invalid value to fill holes")
    # Fill in holes with "invalid" value
    for hash in xrange(hash_function.hash_size):
        if hash not in hash_lookup:
            hash_lookup[hash] = default_value

    return hash_lookup

def make_hash_data(d, hash_function, invalid_value):
    hash_data = dict()
    for i, value in d.iteritems():
        hash = hash_function(i)
        hash_data[hash] = value

    # Fill in holes with "invalid" value
    for hash in xrange(hash_function.hash_size):
        if hash not in hash_data:
            hash_data[hash] = invalid_value

    return hash_data

def make_unicode_to_7bit_hash(input_type_max = 0xFFFF):
    unicode_data = gsm0338_parse.read_unicode_data()
    unicode_dict = dict((unicode, gsm) for (unicode, gsm, comment) in unicode_data)
    (best_size_result, best_collision_result) = findhash.find_hash(unicode_dict, findhash.shift_functions_gen(-15, 18, 2, 256))
    print best_size_result, best_size_result['f'].__doc__
    print best_collision_result, best_collision_result['f'].__doc__

    best_result = best_collision_result
    f = best_result['f']
    
    #invalid_fill_values = xrange(input_type_max, -1, -1)
    #invalid_fill_values = xrange(0xFFFF, 0, -0x1111)
    invalid_fill_values = xrange(0xFFF0, 0, -0x1110)
    hash_lookup = make_hash_lookup(unicode_dict, f, invalid_fill_values)
    hash_data = make_hash_data(unicode_dict, f, 0xFF)

    #pprint(hash_lookup)
    for i in xrange(f.hash_size):
        if i % 16 == 0:
            print
        print "0x{0:04X},".format(hash_lookup[i]),
    
    #pprint(hash_data)
    for i in xrange(f.hash_size):
        if i % 16 == 0:
            print
        print "0x{0:02X},".format(hash_data[i]),
    
if __name__ == "__main__":
    make_unicode_to_7bit_hash()
