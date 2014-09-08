#!/usr/bin/env python3

from collections import defaultdict
import itertools

def shift_vector_gen(smin, smax, n):
    if n > 1:
        for x in shift_vector_gen(smin, smax, n - 1):
            yield x
    vector = list(range(smin, smin + n))
    while True:
        yield tuple(vector)
        i = n - 1
        while True:
            for j in range(i, n):
                if j == i:
                    vector[j] += 1
                else:
                    vector[j] = vector[j - 1] + 1
                if (vector[j] >= smax):
                    if i == 0:
                        return
                    else:
                        i -= 1
                        break
            else:
                break

def shift_xor_functions_gen(smin, smax, n, hash_size):
    for shift_vector in shift_vector_gen(smin, smax, n):
        def make_hash_function(shift_vector, hash_size):
            def hash_function(value):
                out_value = 0
                for shift_value in shift_vector:
                    if shift_value >= 0:
                        out_value ^= value << shift_value
                    else:
                        out_value ^= value >> (-shift_value)
                return out_value % hash_size
            hash_function.__doc__ = "Shift-xor function with vectors {0}, hash size {1}".format(shift_vector, hash_size)
            hash_function.hash_size = hash_size
            return hash_function
        yield make_hash_function(shift_vector, hash_size)

def shift_add_functions_gen(smin, smax, n, hash_size):
    for shift_vector in shift_vector_gen(smin, smax, n):
        def make_hash_function(shift_vector, hash_size):
            def hash_function(value):
                out_value = 0
                for shift_value in shift_vector:
                    if shift_value >= 0:
                        out_value += value << shift_value
                    else:
                        out_value += value >> (-shift_value)
                return out_value % hash_size
            hash_function.__doc__ = "Shift-add function with vectors {0}, hash size {1}".format(shift_vector, hash_size)
            hash_function.hash_size = hash_size
            return hash_function
        yield make_hash_function(shift_vector, hash_size)

def shift_all_functions_gen(smin, smax, n, hash_size):
    for x in itertools.chain(shift_xor_functions_gen(smin, smax, n, hash_size),
                             shift_add_functions_gen(smin, smax, n, hash_size)):
        yield x

def check_hash(o, hash_function):
    hash_output_count = defaultdict(int)
    hash_size = 0
    num_collisions = 0
    max_collisions = 0
    for i in o:
        hash = hash_function(i)
        if hash_size < hash:
            hash_size = hash
        if hash_output_count[hash]:
            num_collisions += 1
        hash_output_count[hash] += 1
        if max_collisions < hash_output_count[hash]:
            max_collisions = hash_output_count[hash]
    return (hash_size, num_collisions, max_collisions, hash_function.hash_size)

def find_collision_free_hashes(o, hash_functions):
    for f in hash_functions:
        (hash_size, num_collisions, max_collisions, f_hash_size) = check_hash(o, f)
        if num_collisions == 0:
            yield { 'size' : hash_size, 'collisions' : num_collisions, 'f_hash_size' : f_hash_size, 'f': f }

def find_best_hash(o, hash_functions, max_collisions_thresh = 1):
    # best_size_result in form (hash_size, num_collisions, f_hash_size, f)
    best_size_result = { 'size' : 1000000000, 'collisions' : 1000000000, 'f_hash_size' : None, 'f' : None }
    best_collision_result = { 'size' : 1000000000, 'collisions' : 1000000000, 'f_hash_size' : None, 'f' : None }
    for f in hash_functions:
        (hash_size, num_collisions, max_collisions, f_hash_size) = check_hash(o, f)
        if ((max_collisions <= max_collisions_thresh) and (hash_size < best_size_result['size'])):
                best_size_result = { 'size' : hash_size, 'collisions' : num_collisions, 'f_hash_size' : f_hash_size, 'f': f } 
        if ((num_collisions < best_collision_result['collisions']) or
            ((num_collisions == best_collision_result['collisions']) and (hash_size < best_collision_result['size']))):
                best_collision_result = { 'size' : hash_size, 'collisions' : num_collisions, 'f_hash_size' : f_hash_size, 'f': f } 
    return (best_size_result, best_collision_result)

def make_hash_lookup(o, hash_function, invalid_value_iter):
    hash_lookup = dict()
    for i in o:
        hash = hash_function(i)
        hash_lookup[hash] = i

    # Find a suitable "invalid" value to fill the holes
    for i in invalid_value_iter:
        if hash_lookup.get(hash_function(i), i) != i:
            invalid_value = i
            break
    else:
        raise Exception("Couldn't find invalid value to fill holes")

    # Convert to list, filling in holes with "invalid" value
    hash_lookup_list = [ hash_lookup.get(i, invalid_value) for i in range(hash_function.hash_size) ]

    return hash_lookup_list

def make_hash_data(d, hash_function, invalid_value):
    hash_data = dict()
    for i, value in d.items():
        hash = hash_function(i)
        hash_data[hash] = value

    # Convert to list, filling in holes with "invalid" value
    hash_data_list = [ hash_data.get(i, invalid_value) for i in range(hash_function.hash_size) ]

    return hash_data_list


if __name__ == "__main__":
    for f in shift_xor_functions_gen(-3, 6, 3, 16):
        print(f.__doc__)
    print()
    
    f = list(shift_xor_functions_gen(-3, 6, 3, 16))[54]
    print(f.__doc__)
    for i in range(f.hash_size):
        print(f(i))
