import pyserpent
import binascii

# Data from User Log
key_hex = "3319e773daedd66f1b0a093aaf1be93706d937464bb7a05744967de2e290c18a"
iv_hex = "d994b791582a804a5a4d84b8"
counter_int = 2
expected_keystream_hex = "8e733d63d2fe93600801bc122a1e6352"

key = binascii.unhexlify(key_hex)
iv = binascii.unhexlify(iv_hex)

print(f"Key: {key_hex}")
print(f"IV:  {iv_hex}")
print(f"Ctr: {counter_int}")

# 1. Test using Libgcrypt (via pyserpent.SerpentCipher)
cipher = pyserpent.SerpentCipher(key)

# We want to encrypt a block of ZEROs to get the keystream?
# CTR Mode: Ciphertext = Plaintext XOR Encrypt(Counter)
# If Plaintext is 00..00, then Ciphertext = Encrypt(Counter) = Keystream.
# pyserpent.encrypt_ctr takes (nonce, ctr, data).
# It will generate counter block: nonce + ctr.
# Then encrypt it to get keystream.
# Then XOR data.
# So if data is bytes(16) (all zeros), output should be keystream.

dummy_data = b'\x00' * 16
keystream_bytes, _ = cipher.encrypt_ctr(iv, counter_int, dummy_data)
keystream_hex_lib = binascii.hexlify(keystream_bytes).decode('utf-8')

print(f"\nExpected Keystream (Log): {expected_keystream_hex}")
print(f"Libgcrypt Keystream:      {keystream_hex_lib}")

if keystream_hex_lib == expected_keystream_hex:
    print("\n[SUCCESS] Libgcrypt matches the visualization log!")
else:
    print("\n[FAILURE] Mismatch!")

# 2. Verify Decryption of the ciphertext provided
plaintext_first_block_hex = "73746f636b666973682f000000000000" # "stockfish/......"
ciphertext_hex = "fd075200b998fa13602ebc122a1e6352"

plaintext_first_block = binascii.unhexlify(plaintext_first_block_hex)
ciphertext = binascii.unhexlify(ciphertext_hex)

# Decrypt using libgcrypt
# CTR decryption is same as encryption
out_plain, _ = cipher.encrypt_ctr(iv, counter_int, ciphertext)
print(f"\nCiphertext: {ciphertext_hex}")
print(f"Decrypted:  {binascii.hexlify(out_plain).decode()}")
print(f"Original:   {plaintext_first_block_hex}")

if out_plain == plaintext_first_block:
    print("[SUCCESS] Decryption restores original plaintext.")
else:
    print("[FAILURE] Decryption failed.")
