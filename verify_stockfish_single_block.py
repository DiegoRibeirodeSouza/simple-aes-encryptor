import pyserpent
import binascii

# --- User Data (New Stockfish Log) ---
key_hex = "fdcddd085fc06fcdafde4abe1b92bf29c8b8f25f063cee061e5f1c64109d1573"
iv_hex = "0d39f5a1a525b8013a6327a6"
ctr = 2
expected_ks = "8974fed0331082ef560dc98c2fb3b5c2"
pt_hex = "73746f636b666973682f000000000000" # "stockfish/......"
ct_hex = "fa0091b35876eb9c3e22c98c2fb3b5c2"

print("--- Verifying Stockfish Log (Single Block) ---")

key = binascii.unhexlify(key_hex)
iv = binascii.unhexlify(iv_hex)
cipher = pyserpent.SerpentCipher(key)

# 1. Generate Keystream using Libgcrypt
zeros = b'\x00' * 16
real_keystream, _ = cipher.encrypt_ctr(iv, ctr, zeros)
real_ks_hex = binascii.hexlify(real_keystream).decode()

print(f"Log Keystream: {expected_ks}")
print(f"Lib Keystream: {real_ks_hex}")

if real_ks_hex == expected_ks:
    print("[MATCH] Keystream is correct via Libgcrypt.")
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
    print(f"[ERROR] XOR Math mismatch!")
