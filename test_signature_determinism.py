#!/usr/bin/env python3
"""
Test raw signature consistency
"""

import sys
sys.path.insert(0, '/home/diego/Documentos/criptografia/simple-encryptor/usr/lib/python3/dist-packages')

from PyKCS11 import *
import os
import hashlib

TOKEN_DRIVER = "/usr/lib/libaetpkss.so"
PIN = "DETHklok1"

pkcs11 = PyKCS11Lib()
pkcs11.load(TOKEN_DRIVER)

slots = pkcs11.getSlotList(tokenPresent=True)
slot = slots[0]

session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)
session.login(PIN)

# Test: assinar o mesmo desafio 3 vezes
challenge = os.urandom(32)
print(f"Desafio (hex): {challenge.hex()[:64]}...")

private_keys = session.findObjects([(CKA_CLASS, CKO_PRIVATE_KEY)])
private_key = private_keys[0]

mechanism = Mechanism(CKM_SHA256_RSA_PKCS)

print("\nAssinando 3 vezes o MESMO desafio:")
signatures = []
for i in range(3):
    sig = bytes(session.sign(private_key, challenge, mechanism))
    sig_hash = hashlib.sha256(sig).hexdigest()
    print(f"  Assinatura {i+1} (SHA256): {sig_hash}")
    signatures.append(sig)

# Verificar se são idênticas
if signatures[0] == signatures[1] == signatures[2]:
    print("\n✅ ASSINATURAS SÃO DETERMINÍSTICAS!")
else:
    print("\n❌ ASSINATURAS DIFEREM (problema found!)")

# Derivar chave AES
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(signatures[0])
aes_key = digest.finalize()

print(f"\nChave AES derivada: {aes_key.hex()}")

session.logout()
session.closeSession()
