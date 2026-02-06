
import os
import time
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def benchmark_encryption(size_mb=100):
    filename = "test_bench.bin"
    print(f"Generating {size_mb}MB file...")
    with open(filename, "wb") as f:
        f.write(os.urandom(size_mb * 1024 * 1024))
    
    password = "benchmark_pass"
    salt = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    
    print("Deriving key...")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    
    print("Starting encryption...")
    start_time = time.time()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    
    chunk_size = 64 * 1024
    output_path = filename + ".enc"
    
    with open(filename, 'rb') as f_in, open(output_path, 'wb') as f_out:
        f_out.write(salt)
        f_out.write(iv)
        
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                padded = padder.finalize()
                f_out.write(encryptor.update(padded) + encryptor.finalize())
                break
            
            padded_chunk = padder.update(chunk)
            f_out.write(encryptor.update(padded_chunk))
            
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Done! {size_mb}MB encrypted in {duration:.2f} seconds.")
    print(f"Speed: {size_mb/duration:.2f} MB/s")
    
    # Clean up
    os.remove(filename)
    os.remove(output_path)

if __name__ == "__main__":
    benchmark_encryption(100)
