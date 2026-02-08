# 🔐 Integração Token A3 - Documentação

## Visão Geral

O Simple Encryptor agora suporta criptografia usando **Token A3 (certificados digitais ICP-Brasil)**!

Arquivos criptografados com o token **só podem ser descriptografados** com:
1. **Token físico** inserido no computador
2. **PIN correto** do token

## Como Funciona

### Tecnologia
- **PBKDF2**: Deriva chave AES-256 do PIN + fingerprint do certificado
- **AES-256-GCM**: Criptografia do arquivo
- **Determinístico**: Mesmo PIN + mesmo token = mesma chave

### Fluxo de Criptografia
```
1. Detecta token inserido
2. Usuário digita PIN
3. Extrai fingerprint SHA-256 do certificado do token
4. Deriva chave AES com PBKDF2(PIN + fingerprint, 100k iterações)
5. Criptografa arquivo com AES-256-GCM
6. Salva: [salt][iv][tag][dados criptografados]
```

### Fluxo de Descriptografia
```
1. Detecta token inserido  
2. Usuário digita PIN
3. Extrai fingerprint do certificado (deve ser o MESMO token)
4. Deriva mesma chave AES com PBKDF2
5. Descriptografa arquivo
```

## Uso

### Instalação de Dependências
```bash
sudo apt install libpcsclite-dev swig
pip install --break-system-packages PyKCS11 pyscard
```

### CLI - Linha de Comando

**Criptografar:**
```bash
simple-encryptor-token --encrypt documento.pdf \
  --output documento.pdf.token \
  --pin SEU_PIN
```

**Descriptografar:**
```bash
simple-encryptor-token --decrypt documento.pdf.token \
  --output documento.pdf \
  --pin SEU_PIN
```

**Testar token:**
```bash
simple-encryptor-token --test
```

### Exemplo Completo
```bash
# 1. Criptografar contrato
$ simple-encryptor-token -e contrato.pdf -o contrato.pdf.token
Digite o PIN do token: ********
🔒 Arquivo criptografado: contrato.pdf.token
🔒 Só pode ser aberto com o token A3 + PIN correto!

# 2. Tentar abrir SEM token = FALHA
$ simple-encryptor-token -d contrato.pdf.token -o contrato.pdf
❌ Nenhum token detectado. Insira o token A3.

# 3. Inserir token + descriptografar
$ simple-encryptor-token -d contrato.pdf.token -o contrato.pdf -p SEU_PIN
✅ Arquivo descriptografado: contrato.pdf
```

## Casos de Uso

### 1. Backup Pessoal Seguro
```bash
# Criptografar backup de documentos
tar -czf ~/Documentos_Importantes.tar.gz ~/Documentos/
simple-encryptor-token -e ~/Documentos_Importantes.tar.gz \
  -o ~/Backup_Seguro.tar.gz.token

# Enviar para nuvem (Dropbox, Google Drive)
# Mesmo se vazarem, SÓ VOCÊ pode abrir (precisa do token físico)
```

### 2. Advogados/Contadores
```bash
# Proteger processos jurídicos
simple-encryptor-token -e processo_123.pdf -o processo_123.pdf.token

# Arquivo fica no PC, mas sem token = inútil
# Conformidade LGPD: proteção física + lógica
```

### 3. Empresas (LGPD/Compliance)
```bash
# Criptografar planilha de clientes
simple-encryptor-token -e clientes.xlsx -o clientes.xlsx.token

# Token fica com gestor responsável
# Auditoria: rastrear quem tem token = quem pode abrir
```

## Segurança

### ✅ Pontos Fortes
- **Hardware Security**: Chave privada NUNCA sai do token
- **Two-Factor**: Precisa do token físico + PIN
- **PBKDF2 100k iterações**: Proteção contra brute-force
- **AES-256-GCM**: Criptografia autenticada

### ⚠️ Limitações
- **Backup do certificado**: Se você renovou o certificado A3, precisa do token ORIGINAL para abrir arquivos antigos
- **PIN esquecido**: Sem recuperação! (Proteção, não bug)
- **Performance**: PBKDF2 leva ~01s (intencional, proteção contra brute-force)

## Troubleshooting

### Token não detectado
```bash
# Verificar serviço pcscd
sudo systemctl status pcscd

# Reiniciar se necessário
sudo systemctl restart pcscd

# Testar manualmente
pkcs11-tool --module /usr/lib/libaetpkss.so --list-slots
```

### PIN bloqueado
- **Solução**: Desbloqueio com PUK (vem com o token)
- **Prevenção**: Testar PIN antes de criptografar arquivos importantes

### Erro "CKR_DEVICE_ERROR"
- **Causa**: Token com firmware desatualizado ou driver incompatível
- **Solução**: Usar driver oficial do fabricante (SafeNet, Watchdata, etc)

## Roadmap Futuro

- [ ] **GUI**: Integrar com interface gráfica do Simple Encryptor
- [ ] **Menu de contexto**: Criptografar com token via botão direito
- [ ] **Pastas**: Suporte para criptografar diretórios inteiros
- [ ] **Multi-certificado**: Criptografar para múltiplos tokens (compartilhamento)
- [ ] **CMS/PKCS#7**: Formato padrão ICP-Brasil (interoperabilidade)

## Detalhes Técnicos

**Bibliotecas:**
- `PyKCS11`: Comunicação com token via PKCS#11
- `pyscard`: Interface smartcard (PC/SC)
- `cryptography`: AES-GCM, PBKDF2, manipulação de certificados

**Driver:**
- `/usr/lib/libaetpkss.so` (A.E.T./SafeNet)

**Formato do arquivo `.token`:**
```
[16 bytes salt][12 bytes IV][16 bytes GCM tag][N bytes dados criptografados]
```

**Key Derivation:**
```python
salt = random(16)
cert_fingerprint = SHA256(certificate.DER)
password = PIN + cert_fingerprint
key = PBKDF2-HMAC-SHA256(password, salt, 100000 iterations, 32 bytes)
```

---

**Desenvolvido para:** Simple Encryptor v3.16+  
**Licença:** MIT  
**Autor:** Diego Ribeiro de Souza
