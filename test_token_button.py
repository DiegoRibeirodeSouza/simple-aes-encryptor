#!/usr/bin/env python3
"""
Teste: Simular seleção de arquivo e clique no botão Token
"""
import subprocess
import time

# Selecionar arquivo via CLI (simular)
print("1. Abrindo aplicação...")
print("2. Aguarde a GUI aparecer...")
print("3. Selecione um arquivo (clique em SELECT FILE)")
print("4. Depois clique no botão '🔒🔑 ENCRYPT (TOKEN)'")
print()
print("Verificando se o app está rodando...")

# Check if app is running
result = subprocess.run(['pgrep', '-f', 'simple-encryptor'], capture_output=True, text=True)
if result.stdout:
    print(f"✅ App rodando (PID: {result.stdout.strip()})")
else:
    print("❌ App não está rodando")
    
print("\nInstruções para teste manual:")
print("1. SELECT FILE → escolha 'test_token.txt'")
print("2. Clique em '🔒🔑 ENCRYPT (TOKEN)'")
print("3. Se aparecer dialog de PIN = ✅ FUNCIONANDO")
print("4. Se nada acontecer = ❌ BUG")
