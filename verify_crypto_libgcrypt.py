import pyserpent
import binascii

# Data from User Log
key_hex = "3319e773daedd66f1b0a093aaf1be93706d937464bb7a05744967de2e290c18a"
iv_hex = "d994b791582a804a5a4d84b8"
ctr_int = 2
expected_keystream_hex = "690c072f26a34927131010120ff5df01" # This is the REAL one from libgcrypt

key = binascii.unhexlify(key_hex)
iv = binascii.unhexlify(iv_hex)

cipher = pyserpent.SerpentCipher(key)

# Test the new logic added to visualizer
# 1. Get REAL Keystream (Libgcrypt)
zeros = b'\x00' * 16
real_keystream, _ = cipher.encrypt_ctr(iv, ctr_int, zeros)
real_keystream_hex = binascii.hexlify(real_keystream).decode()

print(f"Key: {key_hex}")
print(f"Expected Real Keystream: {expected_keystream_hex}")
print(f"Generated Keystream:     {real_keystream_hex}")

if real_keystream_hex == expected_keystream_hex:
    print("\n[SUCCESS] Visualizer logic now matches File Encryption!")
else:
    print("\n[FAILURE] Still mismatching.")
