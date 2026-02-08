import pyserpent
import binascii
import struct

# Reference (Libgcrypt Output from previous step)
# Key: 3319e773daedd66f1b0a093aaf1be93706d937464bb7a05744967de2e290c18a
# Counter Block (Input): d994b791582a804a5a4d84b800000002
# Expected Libgcrypt Output: 690c072f26a34927131010120ff5df01

key_hex = "3319e773daedd66f1b0a093aaf1be93706d937464bb7a05744967de2e290c18a"
input_hex = "d994b791582a804a5a4d84b800000002"
expected_hex = "690c072f26a34927131010120ff5df01"

key = binascii.unhexlify(key_hex)
inp = binascii.unhexlify(input_hex)
expected = binascii.unhexlify(expected_hex)

cipher = pyserpent.SerpentCipher(key)

print("--- Debugging Serpent Mismatch ---")
print(f"Key: {key_hex}")
print(f"Input: {input_hex}")
print(f"Target: {expected_hex}")

# 1. Standard Python Trace (Current)
def dummy_cb(msg): pass
out_std = cipher.trace_encrypt(inp, dummy_cb)
print(f"Current Python: {binascii.hexlify(out_std).decode()}")

# 2. Try Key Reverse?
key_rev = key[::-1]
cipher_rev = pyserpent.SerpentCipher(key_rev) # NOTE: This initializes libgcrypt context too but we use python method
# Re-init key schedule manually effectively? No, trace_encrypt calls _key_schedule(self.key).
# So we need to hack the object or class.
# Easier to just modify the python logic here.

def python_encrypt_variant(key, block, variant=0):
    # variant 0: Standard (Little Endian words)
    # variant 1: Big Endian Words
    # variant 2: Key Reverse bytes
    
    byte_order = 'little'
    if variant == 1: byte_order = 'big'
    
    k_input = key
    if variant == 2: k_input = key[::-1]
    
    # Key Schedule
    w = [int.from_bytes(k_input[i:i+4], byte_order) for i in range(0, 32, 4)]
    for i in range(8, 132):
        t = w[i-8] ^ w[i-5] ^ w[i-3] ^ w[i-1] ^ 0x9e3779b9 ^ (i-8)
        # ROL 11
        t = ((t << 11) & 0xffffffff) | (t >> (32 - 11))
        w.append(t)
        
    k = []
    for i in range(33):
        box_idx = (3 + 32 - i) % 8
        inp_k = w[4*i : 4*i+4]
        out_k = cipher._sbox(box_idx, inp_k)
        k.extend(out_k)
        
    # Encrypt
    b = [int.from_bytes(block[i:i+4], byte_order) for i in range(0, 16, 4)]
    
    for i in range(32):
        b[0] ^= k[4*i]; b[1] ^= k[4*i+1]; b[2] ^= k[4*i+2]; b[3] ^= k[4*i+3]
        b = cipher._sbox(i % 8, b)
        if i < 31: b = cipher._linear_transform(b)
        
    b[0] ^= k[4*32]; b[1] ^= k[4*32+1]; b[2] ^= k[4*32+2]; b[3] ^= k[4*32+3]
    
    return b''.join(x.to_bytes(4, byte_order) for x in b)

out_v1 = python_encrypt_variant(key, inp, 1)
print(f"Variant 1 (Big Endian): {binascii.hexlify(out_v1).decode()}")

out_v2 = python_encrypt_variant(key, inp, 2)
print(f"Variant 2 (Key Rev):    {binascii.hexlify(out_v2).decode()}")

# 3. Try Inverted Input/Output
out_v3 = python_encrypt_variant(key, inp[::-1], 0)
print(f"Variant 3 (Inp Rev):    {binascii.hexlify(out_v3).decode()}")

