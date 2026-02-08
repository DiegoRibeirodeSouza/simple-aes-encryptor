import pyserpent
import binascii

# Data from User Log
key_hex = "3319e773daedd66f1b0a093aaf1be93706d937464bb7a05744967de2e290c18a"
iv_hex = "d994b791582a804a5a4d84b8"
# Counter starts at 2
ctr_int = 2
ciphertext_hex = "fd075200b998fa13602ebc122a1e6352" # From Log

key = binascii.unhexlify(key_hex)
iv = binascii.unhexlify(iv_hex)
ciphertext = binascii.unhexlify(ciphertext_hex)

print(f"Decrypting Log Data...")
print(f"Key: {key_hex}")
print(f"Ciphertext: {ciphertext_hex}")

# We must use the Python implementation (trace_encrypt) because that's what created the log.
# Libgcrypt produces a different keystream.

cipher = pyserpent.SerpentCipher(key)

# 1. Generate Keystream using Python logic
ctr_bytes = ctr_int.to_bytes(4, 'big')
counter_block = iv + ctr_bytes

def dummy_cb(msg): pass
keystream = cipher.trace_encrypt(counter_block, dummy_cb)

print(f"Keystream (Python): {binascii.hexlify(keystream).decode()}")

# 2. XOR to Decrypt
plaintext = bytearray()
for i in range(len(ciphertext)):
    plaintext.append(ciphertext[i] ^ keystream[i])

print(f"Decrypted: {plaintext.hex()}")
print(f"ASCII:     {plaintext}")

# 3. Check against known plaintext from log "Plaintext: 73 74..." (stockfish/)
expected_plain = "73746f636b666973682f000000000000"
if plaintext.hex() == expected_plain:
    print("\n[SUCCESS] Successfully decrypted the log data!")
else:
    print("\n[FAILURE] Decryption result does not match expected plaintext.")
