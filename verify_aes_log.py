from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii

# --- User Data (AES Log) ---
key_hex = "34cecbb3331cf6216260a7e08aebfebc23fd8dbd60b3e51d484c40aa0e341ee4"
iv_hex = "f3f03df06f9fa2dca0f58afc"
ctr_int = 2
expected_ks = "695437ea8216a8a567919d5ca03859a5"
pt_hex = "7f454c46020101004149020000000000" # ELF Header
ct_hex = "16117bac8017a9a526d89f5ca03859a5"

print("--- Verifying AES Log ---")

key = binascii.unhexlify(key_hex)
iv = binascii.unhexlify(iv_hex)

# 1. Generate Keystream using Cryptography Library
# AES-CTR/GCM uses Block Encryption of the Counter Block to generate keystream.
# Counter Block = IV (12) + Counter (4 bytes big endian)
ctr_bytes = ctr_int.to_bytes(4, 'big')
counter_block = iv + ctr_bytes

backend = default_backend()
cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
encryptor = cipher.encryptor()
real_keystream = encryptor.update(counter_block) + encryptor.finalize()
real_ks_hex = binascii.hexlify(real_keystream).decode()

print(f"Log Keystream: {expected_ks}")
print(f"Lib Keystream: {real_ks_hex}")

if real_ks_hex == expected_ks:
    print("[MATCH] Keystream is correct via Cryptography Lib.")
else:
    print("[ERROR] Keystream mismatch!")

# 2. Verify XOR
pt = binascii.unhexlify(pt_hex)
ct = binascii.unhexlify(ct_hex)
ks = binascii.unhexlify(real_ks_hex)

calc_ct = bytes(p ^ k for p, k in zip(pt, ks))
calc_ct_hex = binascii.hexlify(calc_ct).decode()

if calc_ct_hex == ct_hex:
    print(f"[MATCH] XOR Logic correct.")
else:
    print(f"[ERROR] XOR Math mismatch! Calc: {calc_ct_hex} vs Log: {ct_hex}")
