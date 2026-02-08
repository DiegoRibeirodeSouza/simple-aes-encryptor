#!/usr/bin/env python3
"""
Nova abordagem: Usar operação WRAP/UNWRAP do token
Em vez de encrypt/decrypt, usar C_WrapKey/C_UnwrapKey
"""

import sys
sys.path.insert(0, '/home/diego/Documentos/criptografia/simple-encryptor/usr/lib/python3/dist-packages')

from PyKCS11 import *
import os

TOKEN_DRIVER = "/usr/lib/libaetpkss.so"
PIN = "DETHklok1"

pkcs11 = PyKCS11Lib()
pkcs11.load(TOKEN_DRIVER)

slots = pkcs11.getSlotList(tokenPresent=True)
slot = slots[0]

session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)
session.login(PIN)

# Testar wrap/unwrap
print("Testando operações de wrapping/unwrapping...")

# 1. Gerar chave AES temporária no token (para testar)
aes_key_template = [
    (CKA_CLASS, CKO_SECRET_KEY),
    (CKA_KEY_TYPE, CKK_AES),
    (CKA_VALUE_LEN, 32),  # 256 bits
    (CKA_ENCRYPT, True),
    (CKA_DECRYPT, True),
    (CKA_SENSITIVE, False),
    (CKA_EXTRACTABLE, True),
    (CKA_TOKEN, False),  # Sessão temporária
]

try:
    mechanism_gen = Mechanism(CKM_AES_KEY_GEN)
    aes_key_obj = session.generateKey(aes_key_template, mechanism_gen)
    print("✅ Chave AES gerada no token")
    
    # 2. Buscar chave pública RSA
    public_keys = session.findObjects([(CKA_CLASS, CKO_PUBLIC_KEY)])
    if not public_keys:
        print("❌ Nenhuma chave pública encontrada")
        session.logout()
        session.closeSession()
        sys.exit(1)
    
    public_key = public_keys[0]
    print("✅ Chave pública RSA encontrada")
    
    # 3. Wrap (criptografar chave AES com RSA pública)
    mechanism_wrap = Mechanism(CKM_RSA_PKCS)
    wrapped_key = bytes(session.wrapKey(public_key, aes_key_obj, mechanism_wrap))
    print(f"✅ Chave wrapped (tamanho: {len(wrapped_key)} bytes)")
    
    # 4. Buscar chave privada RSA
    private_keys = session.findObjects([(CKA_CLASS, CKO_PRIVATE_KEY)])
    private_key = private_keys[0]
    
    # 5. Unwrap (descriptografar wrapped key com RSA privada)
    mechanism_unwrap = Mechanism(CKM_RSA_PKCS)
    unwrap_template = [
        (CKA_CLASS, CKO_SECRET_KEY),
        (CKA_KEY_TYPE, CKK_AES),
        (CKA_VALUE_LEN, 32),
        (CKA_ENCRYPT, True),
        (CKA_DECRYPT, True),
        (CKA_SENSITIVE, False),
        (CKA_EXTRACTABLE, True),
        (CKA_TOKEN, False),
    ]
    
    unwrapped_key_obj = session.unwrapKey(
        private_key,
        wrapped_key,
        unwrap_template,
        mechanism_unwrap
    )
    print("✅ Chave unwrapped com sucesso!")
    
    # 6. Extrair valor da chave original e unwrapped para comparar
    original_value = bytes(session.getAttributeValue(aes_key_obj, [CKA_VALUE])[0])
    unwrapped_value = bytes(session.getAttributeValue(unwrapped_key_obj, [CKA_VALUE])[0])
    
    if original_value == unwrapped_value:
        print("\n🎉 WRAP/UNWRAP FUNCIONANDO PERFEITAMENTE!")
        print(f"   Chave original:  {original_value.hex()[:32]}...")
        print(f"   Chave unwrapped: {unwrapped_value.hex()[:32]}...")
    else:
        print("\n❌ Chaves diferem!")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

session.logout()
session.closeSession()
