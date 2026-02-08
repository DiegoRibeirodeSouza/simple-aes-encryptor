#!/usr/bin/env python3
"""
Teste rápido de detecção do token A3
"""

from PyKCS11 import *

TOKEN_DRIVER = "/usr/lib/libaetpkss.so"

print("🔍 Testando detecção do Token A3...")

try:
    pkcs11 = PyKCS11Lib()
    pkcs11.load(TOKEN_DRIVER)
    
    print(f"✅ Driver carregado: {TOKEN_DRIVER}")
    
    # Listar todos os slots
    all_slots = pkcs11.getSlotList()
    print(f"\n📋 Slots totais: {len(all_slots)}")
    
    for slot in all_slots:
        info = pkcs11.getSlotInfo(slot)
        print(f"\nSlot {slot}:")
        print(f"  Descrição: {info.slotDescription.strip()}")
        print(f"  Fabricante: {info.manufacturerID.strip()}")
        print(f"  Flags: {info.flags}")
        
        # Verificar se há token inserido
        if info.flags & CKF_TOKEN_PRESENT:
            print(f"  ✅ Token presente!")
            token_info = pkcs11.getTokenInfo(slot)
            print(f"  Token label: {token_info.label.strip()}")
            print(f"  Fabricante do token: {token_info.manufacturerID.strip()}")
        else:
            print(f"  ❌ Sem token")
    
    # Slots com token
    slots_with_token = pkcs11.getSlotList(tokenPresent=True)
    print(f"\n✅ Slots com token: {len(slots_with_token)}")
    
    if slots_with_token:
        print(f"   Slot ativo: {slots_with_token[0]}")
    else:
        print("   ⚠️  Nenhum token detectado!")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
