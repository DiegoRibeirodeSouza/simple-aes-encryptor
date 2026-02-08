from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii

# --- AES Visualizer Logic (Copied from simple-encryptor) ---
class AESVisualizer:
    s_box = (
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
    )

    r_con = (
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    )

    def __init__(self, key):
        self.key = key
        self.rounds = 14  # AES-256
        self.nb = 4
        self.nk = 8
        self.w = []
        self._key_expansion()

    def _gmul(self, a, b):
        p = 0
        for _ in range(8):
            if b & 1: p ^= a
            hi_bit_set = a & 0x80
            a <<= 1
            if hi_bit_set: a ^= 0x1B 
            b >>= 1
        return p & 0xFF

    def _key_expansion(self):
        self.w = [0] * (self.nb * (self.rounds + 1))
        key = list(self.key)
        for i in range(self.nk):
            self.w[i] = (key[4*i] << 24) | (key[4*i+1] << 16) | (key[4*i+2] << 8) | key[4*i+3]
        for i in range(self.nk, self.nb * (self.rounds + 1)):
            temp = self.w[i-1]
            if i % self.nk == 0:
                temp = ((temp << 8) & 0xFFFFFFFF) | (temp >> 24)
                temp = (self.s_box[(temp >> 24) & 0xFF] << 24) | \
                       (self.s_box[(temp >> 16) & 0xFF] << 16) | \
                       (self.s_box[(temp >> 8) & 0xFF] << 8) | \
                       self.s_box[temp & 0xFF]
                temp ^= (self.r_con[i // self.nk] << 24)
            elif self.nk > 6 and i % self.nk == 4:
                temp = (self.s_box[(temp >> 24) & 0xFF] << 24) | \
                       (self.s_box[(temp >> 16) & 0xFF] << 16) | \
                       (self.s_box[(temp >> 8) & 0xFF] << 8) | \
                       self.s_box[temp & 0xFF]
            self.w[i] = self.w[i - self.nk] ^ temp

    def encrypt_block(self, block):
        state = self._bytes_to_matrix(block)
        self._add_round_key(state, 0)
        for r in range(1, self.rounds):
            state = self._sub_bytes(state)
            state = self._shift_rows(state)
            state = self._mix_columns(state)
            self._add_round_key(state, r)
        state = self._sub_bytes(state)
        state = self._shift_rows(state)
        self._add_round_key(state, self.rounds)
        return bytes(self._matrix_to_bytes(state))

    def _matrix_to_bytes(self, state):
        res = []
        for c in range(4):
            for r in range(4):
                res.append(state[c][r])
        return res

    def _bytes_to_matrix(self, text):
        return [list(text[i:i+4]) for i in range(0, len(text), 4)]

    def _add_round_key(self, state, round_num):
        start = round_num * self.nb
        for c in range(4):
            word = self.w[start + c]
            state[c][0] ^= (word >> 24) & 0xFF
            state[c][1] ^= (word >> 16) & 0xFF
            state[c][2] ^= (word >> 8) & 0xFF
            state[c][3] ^= word & 0xFF

    def _sub_bytes(self, state):
        return [[self.s_box[b] for b in col] for col in state]

    def _shift_rows(self, state):
        rows = [[state[c][r] for c in range(4)] for r in range(4)]
        rows[1] = rows[1][1:] + rows[1][:1]
        rows[2] = rows[2][2:] + rows[2][:2]
        rows[3] = rows[3][3:] + rows[3][:3]
        return [[rows[r][c] for r in range(4)] for c in range(4)]

    def _mix_columns(self, state):
        new_state = []
        for col in state:
            s0 = self._gmul(0x02, col[0]) ^ self._gmul(0x03, col[1]) ^ col[2] ^ col[3]
            s1 = col[0] ^ self._gmul(0x02, col[1]) ^ self._gmul(0x03, col[2]) ^ col[3]
            s2 = col[0] ^ col[1] ^ self._gmul(0x02, col[2]) ^ self._gmul(0x03, col[3])
            s3 = self._gmul(0x03, col[0]) ^ col[1] ^ col[2] ^ self._gmul(0x02, col[3])
            new_state.append([s0, s1, s2, s3])
        return new_state


# --- Verification ---

key = b'\x01' * 32
iv = b'\x02' * 12
ctr_int = 5
ctr_bytes = ctr_int.to_bytes(4, 'big')
counter_block = iv + ctr_bytes # 16 bytes

print(f"Key: {key.hex()}")
print(f"Counter Block (Input): {counter_block.hex()}")

# 1. AES Visualizer (Python) Output
vis = AESVisualizer(key)
out_vis = vis.encrypt_block(counter_block)
print(f"Visualizer Output: {out_vis.hex()}")

# 2. Cryptography Library Output (ECB mode of output block = raw encrypt)
backend = default_backend()
cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
encryptor = cipher.encryptor()
out_real = encryptor.update(counter_block) + encryptor.finalize()
print(f"Real Crypto Output: {out_real.hex()}")

if out_vis == out_real:
    print("\n[SUCCESS] AES Visualizer matches standard cryptography library.")
else:
    print("\n[FAILURE] AES Verification Mismatch!")
