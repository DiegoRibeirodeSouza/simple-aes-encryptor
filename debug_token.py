#!/usr/bin/env python3
"""Debug decryption"""

import sys
sys.path.insert(0, '/home/diego/Documentos/criptografia/simple-encryptor/usr/lib/python3/dist-packages')

from token_a3 import TokenA3Manager

manager = TokenA3Manager()

# Debug encryption
print("=" * 60)
print("TESTE: CRIPTOGRAFAR")
print("=" * 60)

success, msg = manager.encrypt_file_with_token(
    '/home/diego/Documentos/criptografia/test_token.txt',
    '/tmp/test_debug.token',
    'DETHklok1'
)
print(f"Resultado: {msg}\n")

# Debug decryption
print("=" * 60)
print("TESTE: DESCRIPTOGRAFAR")
print("=" * 60)

success, msg = manager.decrypt_file_with_token(
    '/tmp/test_debug.token',
    '/tmp/test_debug_decrypted.txt',
    'DETHklok1'
)
print(f"Resultado: {msg}\n")

if success:
    with open('/tmp/test_debug_decrypted.txt', 'r')as f:
        print("✅ Conteúdo descriptografado:")
        print(f.read())
