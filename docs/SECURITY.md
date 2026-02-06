# Guia de Segurança - Simple AES Encryptor

## 🔒 Resumo de Segurança

Este aplicativo implementa **criptografia forte** usando AES-256, mas a segurança final depende de **como você o usa**.

> [!WARNING]
> **Regra de Ouro**: A segurança dos seus arquivos é **tão forte quanto sua senha**. Uma senha fraca = criptografia inútil.

## ✅ O Que Este Aplicativo FAZ

### Proteções Implementadas

#### 1. Criptografia AES-256-CBC
- ✅ Algoritmo padrão ouro da indústria
- ✅ Usado por governos e bancos mundialmente
- ✅ Praticamente impossível de quebrar por força bruta

#### 2. Derivação de Chave Robusta (PBKDF2)
- ✅ 100.000 iterações SHA-256
- ✅ Protege contra ataques de dicionário
- ✅ Torna brute-force extremamente lento

#### 3. Salt e IV Únicos
- ✅ Gerados aleatoriamente via `secrets` (CSPRNG)
- ✅ Impede ataques de rainbow table
- ✅ Garante que arquivos idênticos → ciphertexts diferentes

#### 4. Padding Seguro (PKCS7)
- ✅ Padrão da indústria
- ✅ Sem vazamento de informação de tamanho

## ❌ O Que Este Aplicativo NÃO FAZ

### Limitações Importantes

#### 1. Não Protege Contra Keyloggers
Se sua senha for capturada por:
- Keylogger de hardware
- Malware no sistema
- Screen recording

➡️ **O atacante pode descriptografar seus arquivos**

**Mitigação:** Use antivírus atualizado e sistema operacional seguro

#### 2. Não Protege Contra Acesso Físico
Se alguém tem acesso físico:
- Pode instalar keyloggers
- Pode extrair chaves da RAM (cold boot attack)
- Pode usar engenharia social

➡️ **Proteja fisicamente seu computador**

**Mitigação:** Criptografia de disco completo (LUKS, BitLocker)

#### 3. Não Protege Metadados
Informações vazadas:
- ❌ Nome do arquivo original (parcialmente)
- ❌ Tamanho aproximado do arquivo
- ❌ Data de modificação

➡️ **Metadados podem revelar informações**

#### 4. Sem Autenticação (HMAC/GCM)
- ❌ Não detecta modificação maliciosa do ciphertext
- ❌ Vulnerável a bit-flipping attacks (teórico)

**Status atual:** CBC sem HMAC  
**Futuro:** Migração para AES-GCM (autenticação embutida)

#### 5. Sem Recuperação de Senha
> [!CAUTION]
> **ESQUECEU A SENHA = ARQUIVO PERDIDO PARA SEMPRE**

Não há:
- ❌ Backdoor
- ❌ Chave mestra
- ❌ Recuperação de conta
- ❌ "Esqueci minha senha"

**Isso é um RECURSO, não um bug.** Garante que só você pode acessar.

## 🛡️ Boas Práticas de Uso

### 1. Senhas Fortes

#### ❌ Senhas RUINS:
```
senha123
password
12345678
nome+data (ex: maria1985)
palavras do dicionário
```

#### ✅ Senhas BOAS:
```
T#9kL@mP2$qR8nF!vZ4w  (aleatória)
cavalo-correto-bateria-grampo (4+ palavras aleatórias)
M1nh@F@s3S3gur@2026!  (longa e variada)
```

**Recomendações:**
- 🔢 Mínimo **12 caracteres** (ideal: 16+)
- 🔠 Misture maiúsculas, minúsculas, números e símbolos
- 🎲 Use um **gerenciador de senhas** (Bitwarden, KeePassXC)
- 🔄 Senhas únicas para cada arquivo crítico

### 2. Gerenciamento de Senhas

```bash
# NUNCA faça isso:
echo "minha_senha" > senha.txt  # ❌
echo "senha123" | simple-encryptor  # ❌

# Prefira:
# 1. Digite manualmente
# 2. Use gerenciador de senhas
# 3. Copie e cole de fonte segura
```

### 3. Armazenamento de Arquivos

#### Depois de Criptografar:

```bash
# REMOVA o arquivo original de forma segura
# (NUNCA use apenas "rm", dados podem ser recuperados)

# Opção 1: shred (GNU)
shred -vfz -n 10 arquivo_original.pdf

# Opção 2: wipe
wipe -rf arquivo_original.pdf

# Opção 3: srm (secure rm)
srm arquivo_original.pdf
```

#### Backups:

> [!IMPORTANT]
> Faça backup dos arquivos **.encrypted**, mas em locais separados!

```
✅ BOM: arquivo.encrypted na nuvem + backup local
❌ RUIM: apenas uma cópia do arquivo.encrypted
```

### 4. Compartilhamento Seguro

Se precisar compartilhar arquivos criptografados:

```
✅ Envie arquivo.encrypted por um canal (ex: email)
✅ Envie senha por canal DIFERENTE (ex: Signal, Telegram)
❌ NUNCA envie arquivo + senha pelo mesmo canal
```

## 🔍 Cenários de Ameaça

### Cenário 1: Proteção de Arquivos Pessoais

**Ameaça:** Roubo de laptop  
**Solução:** ✅ Este app é suficiente  
**Uso:**
```bash
simple-encryptor documentos_pessoais.zip
# Senha forte
# Delete original com shred
```

### Cenário 2: Dados Sensíveis Corporativos

**Ameaça:** Compliance, vazamento  
**Solução:** ✅ Use + criptografia de disco  
**Camadas:**
1. Criptografia de disco (LUKS)
2. Este app para arquivos extra-sensíveis
3. Política de senhas corporativa

### Cenário 3: Proteção Contra Governo/Adversário Forte

**Ameaça:** Vigilância estatal, forensics avançado  
**Solução:** ⚠️ Considere ferramentas extras  
**Recomendações:**
- Use VeraCrypt/LUKS para containers
- Considere nega plausível (hidden volumes)
- Use Tails OS para operações críticas
- Este app ainda é útil como camada adicional

### Cenário 4: Arquivamento de Longo Prazo

**Ameaça:** Esquecimento de senha, obsolescência  
**Solução:** ⚠️ Cuidado extra necessário  
**Práticas:**
```
✅ Documente o método (AES-256-CBC)
✅ Armazene a senha em cofre físico
✅ Teste descriptografia periodicamente (1x/ano)
✅ Mantenha múltiplas cópias do .encrypted
⚠️ Considere key escrow para dados críticos
```

## 🔬 Detalhes Técnicos de Segurança

### Força Criptográfica

```
AES-256 keyspace: 2^256 ≈ 1.15 × 10^77 chaves

Assumindo 1 bilhão de bilhões de tentativas/segundo:
Tempo para testar 50% do keyspace: 10^53 anos

Idade do universo: ~10^10 anos

Conclusão: AES-256 é seguro contra força bruta
```

### PBKDF2 - Proteção de Senha

```python
# Configuração atual:
iterations = 100,000
algorithm = SHA256

# Tempo de derivação: ~100ms (depende do hardware)
# Tempo para atacante testar 10,000 senhas: ~1,000 segundos

# Comparação:
# - Sem PBKDF2: 10,000 senhas em ~0.01 segundos
# - Com PBKDF2: 100,000x mais lento
```

**Recomendação OWASP 2024:** Mínimo 100,000 iterações ✅

### Randomness Quality

```python
import secrets  # ✅ CSPRNG (Cryptographically Secure)

salt = secrets.token_bytes(16)  # Entropia: 128 bits
iv = secrets.token_bytes(16)    # Entropia: 128 bits

# NÃO usamos:
# random.randbytes()  ❌ Não criptograficamente seguro
```

## ⚠️ Avisos Importantes

> [!CAUTION]
> ### 1. Este App NÃO É Certificado
> - Não passou por auditoria de segurança formal
> - Use para dados pessoais, não missão crítica
> - Para dados extremamente sensíveis, use soluções certificadas (GPG, VeraCrypt)

> [!WARNING]
> ### 2. Implementação Própria de Crypto
> - Usa biblioteca `cryptography` (auditada e confiável) ✅
> - Mas a combinação/implementação é custom
> - "Don't roll your own crypto" - seguimos princípios estabelecidos

> [!IMPORTANT]
> ### 3. Sem Garantias Legais
> - Fornecido "AS IS" (Licença MIT)
> - Nenhuma garantia de inviolabilidade
> - Você é responsável por seus dados

## 🆘 E Se...

### "Esqueci minha senha!"
**Resposta:** Não há recuperação. Arquivo perdido.  
**Prevenção:** Use gerenciador de senhas, documente senhas críticas.

### "Meu arquivo criptografado corrompeu!"
**Resposta:** Sem backup = perda total.  
**Prevenção:** Múltiplos backups em locais diferentes.

### "Alguém alterou meu .encrypted!"
**Resposta:** Descriptografia falhará. Sem forma de detectar maliciously.  
**Prevenção:** Checksums (SHA256) do .encrypted, armazenamento seguro.

### "Preciso provar que descriptografei!"
**Resposta:** Aplicativo não gera logs ou certificados.  
**Prevenção:** Para cenários forenses, use ferramentas com non-repudiation.

## 📚 Leitura Adicional

### Padrões e Especificações
- [NIST SP 800-38A](https://csrc.nist.gov/publications/detail/sp/800-38a/final) - Modos de Operação AES
- [RFC 2898](https://tools.ietf.org/html/rfc2898) - PBKDF2
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

### Ferramentas Complementares
- **VeraCrypt**: Containers criptografados
- **GPG**: Criptografia assimétrica, assinatura
- **LUKS**: Criptografia de disco (Linux)
- **Bitwarden/KeePassXC**: Gerenciadores de senha

### Auditoria
Se desejar auditar o código:
1. Veja [simple-encryptor/usr/bin/simple-encryptor](file:///home/diego/Documentos/criptografia/simple-encryptor/usr/bin/simple-encryptor)
2. Foque nas funções `_derive_key`, `_encrypt_file_thread`, `_decrypt_file_thread`
3. Verifique uso correto da biblioteca `cryptography`

---

## ✅ Checklist de Segurança

Antes de criptografar dados críticos:

- [ ] Usei senha forte (16+ caracteres)?
- [ ] Armazenei senha em gerenciador seguro?
- [ ] Farei backup do .encrypted?
- [ ] Deletarei o original com shred/wipe?
- [ ] Testei descriptografar antes de deletar original?
- [ ] Entendo que sem senha = arquivo perdido?

**Última atualização:** 2026-02-06
