from itertools import product

# S-DES parameters
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]

def permute(bits, permutation):
    return [bits[i-1] for i in permutation]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def generate_subkeys(key):
    key = permute(key, P10)
    left = key[:5]
    right = key[5:]
    
    # First shift
    left = left_shift(left, 1)
    right = left_shift(right, 1)
    K1 = permute(left + right, P8)
    
    # Second shift
    left = left_shift(left, 2)
    right = left_shift(right, 2)
    K2 = permute(left + right, P8)
    
    return K1, K2

def sbox_lookup(sbox, input_bits):
    row = (input_bits[0] << 1) | input_bits[3]
    col = (input_bits[1] << 1) | input_bits[2]
    return sbox[row][col]

def f_function(right, subkey):
    expanded = [right[i] for i in [3, 0, 1, 2, 1, 2, 3, 0]]
    xor_result = [expanded[i] ^ subkey[i] for i in range(8)]
    
    s0 = [[1, 0, 3, 2],
          [3, 2, 1, 0],
          [0, 2, 1, 3],
          [2, 1, 0, 3]]
    s1 = [[0, 1, 2, 3],
          [2, 0, 1, 3],
          [3, 0, 1, 2],
          [2, 1, 0, 3]]
    
    left = sbox_lookup(s0, xor_result[:4])
    right = sbox_lookup(s1, xor_result[4:])
    result = (left << 2) | right
    return [int(b) for b in f'{result:04b}']

def sdes_encrypt(plaintext, key):
    K1, K2 = generate_subkeys(key)
    
    # Initial Permutation
    ip = permute(plaintext, IP)
    left, right = ip[:4], ip[4:]
    
    # Round 1
    f_result = f_function(right, K1)
    new_right = [left[i] ^ f_result[i] for i in range(4)]
    left = right
    right = new_right
    
    # Round 2
    f_result = f_function(right, K2)
    new_right = [left[i] ^ f_result[i] for i in range(4)]
    left = right
    right = new_right
    
    # Final Permutation
    return permute(left + right, IP_INV)

def get_difference_bits(x, y):
    return [a ^ b for a, b in zip(x, y)]

def differential_attack(plaintext_pairs, expected_diff):
    keyspace = product(range(2), repeat=10)  # Gene keys
    counts = {}

    for key in keyspace:
        count = 0
        for pt1, pt2 in plaintext_pairs:
            ct1 = sdes_encrypt(pt1, key)
            ct2 = sdes_encrypt(pt2, key)
            output_diff = get_difference_bits(ct1, ct2)
            if output_diff == expected_diff:
                count += 1
        counts[tuple(key)] = count

    max_count = max(counts.values())
    likely_keys = [list(k) for k, v in counts.items() if v == max_count]
    return likely_keys, max_count

def find_correct_key(likely_keys, known_plaintext, known_ciphertext):
    for key in likely_keys:
        if sdes_encrypt(known_plaintext, key) == known_ciphertext:
            return key
    return None

plaintext_pairs = [
    ([1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 0, 0]),
    ([1, 1, 0, 0, 1, 1, 0, 0], [1, 1, 0, 0, 1, 1, 1, 0]),
    ([1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 1, 0])
]
expected_output_diff = [0, 0, 0, 0, 0, 0, 0, 0]

likely_keys, max_count = differential_attack(plaintext_pairs, expected_output_diff)
print(f"Likely Keys: {[''.join(map(str, key)) for key in likely_keys]}")
print("*******************************************************************")



known_plaintext = [1, 0, 1, 0, 1, 1, 1, 0]
known_ciphertext = [0, 1, 1, 1, 0, 0, 0, 1]  

correct_key = find_correct_key(likely_keys, known_plaintext, known_ciphertext)

for pt in [known_plaintext] + [pt for pair in plaintext_pairs for pt in pair]:
    ct = sdes_encrypt(pt, correct_key)
    print(f"Plaintext: {pt}, Ciphertext: {ct}")
for pt1, pt2 in plaintext_pairs:
    ct1 = sdes_encrypt(pt1, correct_key)
    ct2 = sdes_encrypt(pt2, correct_key)
    actual_diff = get_difference_bits(ct1, ct2)
    print(f"Actual difference: {actual_diff}")
if correct_key:
    print("*******************************************************************")

    print(f"Correct Key: {''.join(map(str, correct_key))}")
else:
    print("Correct key not found among likely keys.")