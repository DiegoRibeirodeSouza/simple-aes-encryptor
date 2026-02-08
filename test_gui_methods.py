#!/usr/bin/env python3
"""
Teste simples: Verificar se os métodos Token A3 existem na classe
"""

import sys
sys.path.insert(0, '/usr/lib/python3/dist-packages')
from token_a3 import TokenA3Manager

# Simular criação de app
exec(open('/usr/bin/simple-encryptor').read())

# Verificar se métodos existem
app_instance = ModernEncryptorApp()

print("Verificando métodos Token A3:")
print(f"  _ask_pin: {hasattr(app_instance, '_ask_pin')}")
print(f"  _encrypt_with_token: {hasattr(app_instance, '_encrypt_with_token')}")
print(f"  _decrypt_with_token: {hasattr(app_instance, '_decrypt_with_token')}")

if hasattr(app_instance, '_encrypt_with_token'):
    print("\n✅ Métodos existem!")
    print("Testando chamada direta...")
    try:
        # Simular clique (sem arquivo selecionado)
        app_instance._encrypt_with_token()
        print("✅ Método executou!")
    except Exception as e:
        print(f"❌ Erro: {e}")
else:
    print("\n❌ Métodos NÃO encontrados na classe!")
