# Security Guide - Simple Encryptor GCM

## 🔒 Security Summary

This application implements **strong encryption** using AES-256 and Serpent-256, but final security depends on **how you use it**.

> [!WARNING]
> **Golden Rule**: Your file security is **as strong as your password**. A weak password = useless encryption.

## ✅ What This App DOES

### Implemented Protections

#### 1. AES-256-GCM & Serpent-256
- ✅ Gold standard industry algorithms
- ✅ Used by governments and banks worldwide
- ✅ Virtually impossible to break via brute-force (if password is strong)

#### 2. Robust Key Derivation (PBKDF2)
- ✅ 100,000 iterations of HMAC-SHA256
- ✅ Protects against dictionary attacks
- ✅ Makes brute-force extremely slow

#### 3. Unique Salt & IV
- ✅ Randomly generated via `secrets` (CSPRNG)
- ✅ Prevents rainbow table attacks
- ✅ Ensures identical files → different ciphertexts

#### 4. Authenticated Encryption
- ✅ **AES-GCM**: Built-in authentication tag (128-bit)
- ✅ **Serpent-CTR**: Custom HMAC-SHA256 (128-bit truncated) layer
- ✅ Detects tampering/corruption before decryption

## ❌ What This App DOES NOT DO

### Important Limitations

#### 1. Does Not Protect Against Keyloggers
If your password is captured by:
- Hardware keylogger
- System malware
- Screen recording

➡️ **The attacker can decrypt your files**

**Mitigation:** Use up-to-date antivirus and a secure OS.

#### 2. Does Not Protect Against Physical Access
If someone has physical access:
- Can install keyloggers
- Can extract keys from RAM (cold boot attack)
- Can use social engineering

➡️ **Physically protect your computer**

**Mitigation:** Full Disk Encryption (LUKS, BitLocker)

#### 3. Does Not Protect Metadata
Leaked info:
- ❌ Original filename (partially masked in folder mode)
- ❌ Approximate file size
- ❌ Modification date

➡️ **Metadata can reveal information**

#### 4. No Password Recovery
> [!CAUTION]
> **FORGOT PASSWORD = FILE LOST FOREVER**

There is no:
- ❌ Backdoor
- ❌ Master key
- ❌ Account recovery
- ❌ "Forgot my password"

**This is a FEATURE, not a bug.** It ensures only YOU can access it.

## 🛡️ Usage Best Practices

### 1. Strong Passwords

#### ❌ BAD Passwords:
```
password123
admin
12345678
name+date (e.g., mary1985)
dictionary words
```

#### ✅ GOOD Passwords:
```
T#9kL@mP2$qR8nF!vZ4w  (random)
horse-correct-battery-staple (4+ random words)
MySnh@P@ssPhraz32026!  (long and varied)
```

**Recommendations:**
- 🔢 Minimum **12 characters** (ideal: 16+)
- 🔠 Mix uppercase, lowercase, numbers, and symbols
- 🎲 Use a **password manager** (Bitwarden, KeePassXC)
- 🔄 Unique passwords for each critical file

### 2. Password Management

```bash
# NEVER do this:
echo "my_password" > pass.txt  # ❌
echo "pass123" | simple-encryptor  # ❌

# Prefer:
# 1. Type manually
# 2. Use password manager
# 3. Copy-paste from secure source
```

### 3. File Storage

#### After Encrypting:

```bash
# SECURELY REMOVE the original file
# (NEVER use just "rm", data can be recovered)

# Option 1: shred (GNU)
shred -vfz -n 10 original_file.pdf

# Option 2: wipe
wipe -rf original_file.pdf

# Option 3: srm (secure rm)
srm original_file.pdf
```

#### Backups:

> [!IMPORTANT]
> Backup your **.encrypted** files, but in separate locations!

```
✅ GOOD: file.encrypted on cloud + local backup
❌ BAD: only one copy of file.encrypted
```

### 4. Secure Sharing

If you need to share encrypted files:

```
✅ Send file.encrypted via one channel (e.g., Email)
✅ Send password via DIFFERENT channel (e.g., Signal, Telegram)
❌ NEVER send file + password via same channel
```

## 🔍 Threat Models

### Scenario 1: Personal File Protection

**Threat:** Laptop theft  
**Solution:** ✅ This app is sufficient  
**Usage:**
```bash
simple-encryptor personal_docs.zip
# Strong password
# Delete original with shred
```

### Scenario 2: Corporate Sensitive Data

**Threat:** Compliance, leaks  
**Solution:** ✅ Use + Disk Encryption  
**Layers:**
1. Full Disk Encryption (LUKS)
2. This app for extra-sensitive files
3. Corporate password policy

### Scenario 3: Protection Against State/Advanced Adversary

**Threat:** State surveillance, advanced forensics  
**Solution:** ⚠️ Consider extra tools  
**Recommendations:**
- Use VeraCrypt/LUKS for containers
- Consider plausible deniability (hidden volumes)
- Use Tails OS for critical operations
- This app is still useful as an additional layer

### Scenario 4: Long-Term Archival

**Threat:** Forgetting password, obsolescence  
**Solution:** ⚠️ Extra care needed  
**Practices:**
```
✅ Document the method (AES-256-GCM)
✅ Store password in physical safe
✅ Test decryption periodically (1x/year)
✅ Keep multiple copies of .encrypted
⚠️ Consider key escrow for critical data
```

## 🔬 Technical Security Details

### Cryptographic Strength

```
AES-256 keyspace: 2^256 ≈ 1.15 × 10^77 keys

Assuming 1 billion billion attempts/second:
Time to test 50% of keyspace: 10^53 years

Universe age: ~10^10 years

Conclusion: AES-256 is secure against brute force
```

### PBKDF2 - Password Protection

```python
# Current Configuration:
iterations = 100,000
algorithm = SHA256
salt_size = 16 bytes

# Derivation Time: ~100ms (hardware dependent)
# Time for attacker to test 10,000 passwords: ~1,000 seconds

# Comparison:
# - Without PBKDF2: 10,000 passwords in ~0.01 seconds
# - With PBKDF2: 100,000x slower
```

**OWASP 2024 Recommendation:** Minimum 100,000 iterations ✅

### Randomness Quality

```python
import secrets  # ✅ CSPRNG (Cryptographically Secure)

salt = secrets.token_bytes(16)  # Entropy: 128 bits
iv = secrets.token_bytes(16)    # Entropy: 128 bits

# WE DO NOT USE:
# random.randbytes()  ❌ Not cryptographically secure
```

## ⚠️ Important Warnings

> [!CAUTION]
> ### 1. This App is NOT Certified
> - Has not undergone formal security audit
> - Use for personal data, not mission-critical secrets without extra layers
> - For top-secret data, use certified solutions (GPG, VeraCrypt)

> [!WARNING]
> ### 2. Custom Crypto Implementation
> - Uses `cryptography` library (audited and trusted) ✅
> - But the combination/logic is custom code
> - "Don't roll your own crypto" - we follow established standards but keep this in mind

> [!IMPORTANT]
> ### 3. No Legal Warranty
> - Provided "AS IS" (MIT License)
> - No guarantee of invulnerability
> - You are responsible for your data

## 🆘 What If...

### "I forgot my password!"
**Answer:** No recovery. File lost.  
**Prevention:** Use a password manager, document critical passwords.

### "My encrypted file is corrupted!"
**Answer:** Authentication tag check will fail. Decryption aborted.  
**Prevention:** Multiple backups in different locations. Use ECC RAM if possible.

### "Someone modified my .encrypted file!"
**Answer:** Decryption will fail (Integrity Check).  
**Prevention:** GCM/HMAC handles this.

### "I need to prove I decrypted it!"
**Answer:** App does not generate logs/certs for non-repudiation.  
**Prevention:** For forensic scenarios, use tools with digital signatures.

## 📚 Further Reading

### Standards & Specs
- [NIST SP 800-38D](https://csrc.nist.gov/publications/detail/sp/800-38d/final) - AES-GCM
- [RFC 2898](https://tools.ietf.org/html/rfc2898) - PBKDF2
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

### Complementary Tools
- **VeraCrypt**: Encrypted containers
- **GPG**: Asymmetric encryption, signing
- **LUKS**: Disk encryption (Linux)
- **Bitwarden/KeePassXC**: Password managers

### Auditing
If you wish to audit the code:
1. See [simple-encryptor/usr/bin/simple-encryptor](file:///home/diego/Documentos/criptografia/simple-encryptor/usr/bin/simple-encryptor)
2. Focus on functions `_derive_key`, `_encrypt_file_thread`, `_decrypt_file_thread`
3. Verify correct usage of `cryptography` library

---

## ✅ Security Checklist

Before encrypting critical data:

- [ ] Strong password used (16+ chars)?
- [ ] Password stored in secure manager?
- [ ] Backup of .encrypted made?
- [ ] Original deleted with shred/wipe?
- [ ] Tested decryption before deleting original?
- [ ] Understand that no password = lost file?

**Last Update:** 2026-02-06
