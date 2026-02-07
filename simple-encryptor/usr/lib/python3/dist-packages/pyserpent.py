
# Serpent Cipher Implementation (via libgcrypt)
# Uses the system's standard GnuPG crypto library for maximum performance and security.

import ctypes
import os
import binascii

# --- Libgcrypt Constants ---
GCRY_CIPHER_SERPENT256 = 305
GCRY_CIPHER_MODE_CTR = 6

# --- Load Library ---
_lib = None
try:
    _lib = ctypes.CDLL('libgcrypt.so.20')
    
    # Check version to initialize library
    _lib.gcry_check_version.restype = ctypes.c_char_p
    _lib.gcry_check_version.argtypes = [ctypes.c_char_p]
    _lib.gcry_check_version(None)
    
except OSError:
    print("Warning: libgcrypt.so.20 not found. Serpent encryption will fail.")

# --- Types & Prototypes ---
gcry_cipher_hd_t = ctypes.c_void_p

if _lib:
    _lib.gcry_cipher_open.restype = ctypes.c_int
    _lib.gcry_cipher_open.argtypes = [ctypes.POINTER(gcry_cipher_hd_t), ctypes.c_int, ctypes.c_int, ctypes.c_uint]

    _lib.gcry_cipher_setkey.restype = ctypes.c_int
    _lib.gcry_cipher_setkey.argtypes = [gcry_cipher_hd_t, ctypes.c_void_p, ctypes.c_size_t]

    _lib.gcry_cipher_setctr.restype = ctypes.c_int
    _lib.gcry_cipher_setctr.argtypes = [gcry_cipher_hd_t, ctypes.c_void_p, ctypes.c_size_t]

    _lib.gcry_cipher_encrypt.restype = ctypes.c_int
    _lib.gcry_cipher_encrypt.argtypes = [gcry_cipher_hd_t, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t]

    _lib.gcry_cipher_close.restype = None
    _lib.gcry_cipher_close.argtypes = [gcry_cipher_hd_t]

class SerpentCipher:
    def __init__(self, key):
        if not _lib:
            raise RuntimeError("libgcrypt is not available")
            
        if len(key) != 32:
            raise ValueError("Serpent key must be 256 bits (32 bytes)")
            
        self.key = key
        self.handle = None
        
        # Open Context
        self.handle = gcry_cipher_hd_t()
        ret = _lib.gcry_cipher_open(ctypes.byref(self.handle), GCRY_CIPHER_SERPENT256, GCRY_CIPHER_MODE_CTR, 0)
        if ret != 0:
            raise RuntimeError(f"Failed to open libgcrypt cipher (GCM/CTR constants might differ?): code {ret}")
            
        # Set Key
        ret = _lib.gcry_cipher_setkey(self.handle, key, len(key))
        if ret != 0:
            _lib.gcry_cipher_close(self.handle)
            raise RuntimeError(f"Failed to set key: code {ret}")

    def __del__(self):
        if self.handle and _lib:
            _lib.gcry_cipher_close(self.handle)

    def encrypt_ctr(self, nonce, ctr_int, data):
        """
        Encrypts data in CTR mode.
        nonce: 12 bytes
        ctr_int: integer initial counter
        data: bytes to encrypt
        libgcrypt maintains internal state, so we must set CTR only at start or seek.
        But simple-encryptor design creates a new cipher for each file or manages state?
        Actually simple-encryptor (modified) manages state by ... 
        Wait, standard CTR mode increments the counter.
        Libgcrypt also likely maintains state.
        
        However, if this method is called multiple times for chunks of the SAME stream, we should NOT reset the counter using setctr if libgcrypt already advanced it!
        
        But the current API of this class (as used by my planned simple-encryptor change) assumes statelessness or state managed by caller? 
        The 'simple-encryptor' implementation I planned sends `ctr_val` every time.
        
        If I use `gcry_cipher_setctr` every time, I am implementing the "stateless" chunk encryption.
        This is safer for the caller logic currently in simple-encryptor which manages the counter itself.
        
        So:
        1. Set CTR to (nonce + ctr_int)
        2. Encrypt data
        3. Return encrypted data and new_ctr_int (calculated)
        """
        
        # Prepare Counter Block (16 bytes)
        # Nonce (12) + Counter (4, Big Endian)
        ctr_bytes = nonce + ctr_int.to_bytes(4, 'big')
        
        ret = _lib.gcry_cipher_setctr(self.handle, ctr_bytes, 16)
        if ret != 0:
            raise RuntimeError(f"Failed to set CTR: code {ret}")
            
        data_len = len(data)
        out_buf = ctypes.create_string_buffer(data_len)
        in_buf = (ctypes.c_ubyte * data_len).from_buffer_copy(data) # Safer for read-only bytes
        
        ret = _lib.gcry_cipher_encrypt(self.handle, out_buf, data_len, in_buf, data_len)
        if ret != 0:
             raise RuntimeError(f"Encryption failed: code {ret}")
             
        # Calculate new counter value
        # We processed 'data_len' bytes.
        # How many full/partial blocks?
        # ceil(data_len / 16) blocks were consumed.
        # But wait, did we use 1 block of keystream for 1 byte? Yes, in CTR mode block mechanics.
        # libgcrypt increments the counter for every 16 bytes of output generated.
        # The question is: if I call setctr again next time, I need to know the correct next counter.
        
        blocks_used = (data_len + 15) // 16
        new_ctr = ctr_int + blocks_used
        
        return out_buf.raw, new_ctr
        
    def encrypt_block_raw(self, block):
        # Backward compatibility for pure block encryption if needed
        # But CTR mode in libgcrypt handles the stream.
        # If we need single block encryption, we need ECB mode context.
        # This function was only used by the OLD slow python loop.
        # We shouldn't need it anymore.
        raise NotImplementedError("Use encrypt_ctr for high performance")

    # --- Visualization Helpers ---
    # These are SLOW Python implementations restored purely for the "View Log" feature.
    # They are NOT used for actual file encryption.
    
    def trace_encrypt(self, block, callback):
        """Encrypts a block and calls callback(str) with details for every round."""
        if len(block) != 16: raise ValueError("Block must be 16 bytes")
        
        # We need the key schedule for this
        w = self._key_schedule(self.key)
        
        b = [int.from_bytes(block[i:i+4], 'little') for i in range(0, 16, 4)]
        
        callback(f"Input Words: {[hex(x) for x in b]}")
        
        for i in range(32):
            # Key Mixing
            b[0] ^= w[4*i]
            b[1] ^= w[4*i+1]
            b[2] ^= w[4*i+2]
            b[3] ^= w[4*i+3]
            
            # S-Box
            b = self._sbox(i % 8, b)
            callback(f"Round {i:02d} | KeyMix+SBox[{i%8}]: {[hex(x) for x in b]}")
            
            # Linear Transformation (except last round)
            if i < 31:
                b = self._linear_transform(b)
                callback(f"Round {i:02d} | LinearTransform: {[hex(x) for x in b]}")
        
        # Final Key Mixing (Round 32)
        b[0] ^= w[4*32]
        b[1] ^= w[4*32+1]
        b[2] ^= w[4*32+2]
        b[3] ^= w[4*32+3]
        
        callback(f"Final Output: {[hex(x) for x in b]}")
        return b''.join(x.to_bytes(4, 'little') for x in b)

    def _key_schedule(self, key):
        # 256-bit key -> 8 words
        w = [int.from_bytes(key[i:i+4], 'little') for i in range(0, 32, 4)]
        
        # Expand to 132 words
        for i in range(8, 132):
            # w[i] = (w[i-8] ^ w[i-5] ^ w[i-3] ^ w[i-1] ^ phi ^ i) <<< 11
            t = w[i-8] ^ w[i-5] ^ w[i-3] ^ w[i-1] ^ 0x9e3779b9 ^ (i-8)
            w.append(self._rol(t, 11))
            
        # Apply S-Boxes to generated keys
        k = []
        for i in range(33): # 33 subkeys (r0..r32)
            # Group 4 words
            box_idx = (3 + 32 - i) % 8 # Serpent Key Schedule S-box selection rule
            inp = w[4*i : 4*i+4]
            out = self._sbox(box_idx, inp)
            k.extend(out)
            
        return k

    def _sbox(self, s_idx, x):
        r0, r1, r2, r3 = x[0], x[1], x[2], x[3]
        
        if s_idx == 0:
            r3 ^= r0; r4 = r1; r1 &= r3; r4 ^= r2; r1 ^= r0; r0 |= r3; r0 ^= r4; r4 ^= r3; r3 ^= r2; r2 |= r1; r2 ^= r4; r4 = ~r4; r4 |= r1; r1 ^= r3; r1 ^= r4; r3 |= r0; r1 ^= r3; r4 ^= r3; r0 ^= r1; r4 ^= r0; r0,r1,r2,r3 = r1,r4,r2,r0
        elif s_idx == 1:
            r0 = ~r0; r2 = ~r2; r0 ^= r1; r1 |= r0; r0 ^= r2; r2 ^= r1; r1 &= r0; r1 ^= r3; r4 = r0; r4 |= r1; r0 ^= r2; r2 &= r1; r1 ^= r0; r1 |= r4; r1 ^= r2; r0 &= r2; r0 ^= r3; r4 ^= r0; r2 ^= r0; r0,r1,r2,r3 = r4,r2,r1,r0
        elif s_idx == 2:
            r4 = r0; r0 &= r2; r0 ^= r3; r2 ^= r1; r2 ^= r0; r3 |= r4; r3 ^= r1; r4 ^= r2; r1 = r3; r3 |= r4; r3 ^= r0; r0 &= r1; r4 ^= r0; r1 ^= r3; r1 ^= r4; r4 = ~r4; r0,r1,r2,r3 = r2,r3,r1,r4
        elif s_idx == 3:
            r0 ^= r1; r2 |= r0; r3 &= r1; r1 &= r2; r0 ^= r3; r2 ^= r0; r1 ^= r2; r0 &= r1; r0 ^= r2; r3 ^= r2; r4 = r1; r1 &= r3; r4 ^= r0; r0 |= r1; r0 ^= r3; r2 ^= r3; r1 ^= r0; r3 ^= r0; r3 ^= r1; r0,r1,r2,r3 = r2,r4,r3,r1
        elif s_idx == 4:
            r1 ^= r3; r3 = ~r3; r2 ^= r3; r0 ^= r2; r3 &= r0; r4 = r1; r1 |= r3; r4 ^= r2; r4 ^= r3; r0 ^= r4; r1 |= r0; r1 ^= r2; r3 ^= r4; r1 |= r3; r0 ^= r1; r3 ^= r2; r2 &= r1; r2 ^= r3; r4 ^= r0; r0,r1,r2,r3 = r1,r4,r0,r2
        elif s_idx == 5:
            r0 ^= r1; r1 ^= r3; r3 = ~r3; r0 ^= r3; r1 |= r0; r3 ^= r1; r1 ^= r2; r4 = r2; r4 &= r0; r1 ^= r4; r2 ^= r0; r2 &= r1; r4 ^= r3; r0 ^= r4; r2 ^= r4; r2 ^= r0; r0,r1,r2,r3 = r1,r3,r0,r2
        elif s_idx == 6:
            r0 = ~r0; r0 ^= r1; r1 &= r2; r2 ^= r0; r1 ^= r3; r3 |= r0; r0 ^= r2; r4 = r3; r4 ^= r1; r2 |= r3; r3 ^= r0; r1 &= r0; r1 ^= r2; r2 ^= r4; r0 ^= r4; r0 ^= r1; r3 ^= r1; r4 ^= r2; r0,r1,r2,r3 = r0,r1,r3,r4
        elif s_idx == 7:
            r1 = ~r1; r3 = ~r3; r4 = r1; r1 &= r2; r1 ^= r3; r4 |= r2; r4 ^= r0; r2 ^= r4; r0 &= r3; r3 ^= r2; r4 ^= r1; r0 ^= r4; r1 |= r0; r1 ^= r3; r4 &= r1; r4 ^= r2; r1 ^= r2; r0 ^= r4; r0,r1,r2,r3 = r3,r4,r0,r1
            
        return [r0 & 0xffffffff, r1 & 0xffffffff, r2 & 0xffffffff, r3 & 0xffffffff]

    def _linear_transform(self, x):
        r0, r1, r2, r3 = x[0], x[1], x[2], x[3]
        
        r0 = self._rol(r0, 13)
        r2 = self._rol(r2, 3)
        r1 = r1 ^ r0 ^ r2
        r3 = r3 ^ r2 ^ (r0 << 3)
        r1 = self._rol(r1, 1)
        r3 = self._rol(r3, 7)
        r0 = r0 ^ r1 ^ r3
        r2 = r2 ^ r3 ^ (r1 << 7)
        r0 = self._rol(r0, 5)
        r2 = self._rol(r2, 22)
        
        return [r0 & 0xffffffff, r1 & 0xffffffff, r2 & 0xffffffff, r3 & 0xffffffff]

    def _rol(self, value, bits):
        return ((value << bits) & 0xffffffff) | (value >> (32 - bits))

