import pyserpent
import binascii

# --- User Data ---
key_hex = "595575ab831dab556addb5722cb0379d83d5006f503dabf91e450f637b1892e7"
iv_hex = "1ad9bdb84d92b6060b947115"

# Block 1 (Start)
ctr1 = 2
log_ks1 = "6539ae0ba62651c713e4c10acfa7ba69"
log_pt1 = "7f454c46020101004149020000000000" # ELF Header
log_ct1 = "1a7ce24da42750c752adc30acfa7ba69"

# Block 2 (Later)
ctr2 = 0xb36002 # 11755522
log_ks2 = "efbf3165bce98066a4688de6ee939295"
log_pt2 = "14be4dbb327e8b8895adb2b0fbfa259c"
log_ct2 = "fb017cde8e970bee31c53f561569b709"

key = binascii.unhexlify(key_hex)
iv = binascii.unhexlify(iv_hex)
cipher = pyserpent.SerpentCipher(key)

print("--- Verifying Bootstrap Log ---")

def verify_block(name, ctr, expected_ks, pt_hex, ct_hex):
    print(f"\nChecking {name} (Ctr {ctr})...")
    
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
        return
        
    # 2. Verify XOR Math
    pt = binascii.unhexlify(pt_hex)
    ct = binascii.unhexlify(ct_hex)
    ks = binascii.unhexlify(real_ks_hex)
    
    calc_ct = bytes(p ^ k for p, k in zip(pt, ks))
    calc_ct_hex = binascii.hexlify(calc_ct).decode()
    
    if calc_ct_hex == ct_hex:
        print(f"[MATCH] XOR Logic correct: {pt_hex[:8]}... ^ {expected_ks[:8]}... = {ct_hex[:8]}...")
    else:
        print(f"[ERROR] XOR Math mismatch! Calc: {calc_ct_hex} vs Log: {ct_hex}")

# Run verify
verify_block("Block 1 (Header)", ctr1, log_ks1, log_pt1, log_ct1)
verify_block("Block 2 (Offset)", ctr2, log_ks2, log_pt2, log_ct2)
