
import time
import os
import sys
import secrets
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac

# Add path to find pyserpent (Prepend to override installed package)
sys.path.insert(0, os.path.join(os.getcwd(), 'simple-encryptor/usr/lib/python3/dist-packages'))
try:
    import pyserpent
    print(f"pyserpent imported successfully from: {pyserpent.__file__}")
except ImportError:
    print("Failed to import pyserpent. Make sure you act from the root of the workspace.")
    sys.exit(1)

def benchmark_aes_gcm(size_mb=10):
    data = os.urandom(size_mb * 1024 * 1024)
    key = os.urandom(32)
    iv = os.urandom(12)
    
    print(f"Benchmarking AES-GCM ({size_mb} MB)...")
    start = time.time()
    
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    
    end = time.time()
    print(f"AES-GCM Time: {end - start:.4f}s")
    print(f"AES Speed: {size_mb / (end - start):.2f} MB/s")

def benchmark_serpent_ctr_optimized(size_mb=10):
    data = os.urandom(size_mb * 1024 * 1024)
    key = os.urandom(32)
    iv = os.urandom(12)
    
    print(f"Benchmarking Serpent-CTR (Libgcrypt) ({size_mb} MB)...")
    
    cipher = pyserpent.SerpentCipher(key)
    
    ctr_val = 2
    
    start = time.time()
    
    # Use the new fast Libgcrypt function
    encrypted_data, new_ctr = cipher.encrypt_ctr(iv, ctr_val, data)
    
    end = time.time()
    print(f"Serpent-CTR Time: {end - start:.4f}s")
    print(f"Serpent Speed: {size_mb / (end - start):.2f} MB/s")

if __name__ == "__main__":
    benchmark_aes_gcm(10)
    print("-" * 30)
    benchmark_serpent_ctr_optimized(10)
