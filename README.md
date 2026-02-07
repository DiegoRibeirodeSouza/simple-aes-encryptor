# Simple Encryptor GCM 🔐

<div align="center">

**Simple GUI app for file encryption using AES-256-GCM & Serpent**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Debian Package](https://img.shields.io/badge/package-.deb-red.svg)](https://www.debian.org/)

[Installation](#-installation) • [Usage](#-usage) • [Features](#-features) • [Documentation](#-documentation)

</div>

---

## 📋 About

**Simple Encryptor GCM** is a GUI application developed in Python to encrypt and decrypt files using **AES-256-GCM** and **Serpent-256**. The key feature is the **real-time education monitor** that visually shows the encryption process step-by-step (e.g. Matrix Mixing, S-Boxes) while maintaining high performance via C extensions.

### ✨ Features

- 🔐 **Multi-Algorithm**: AES-256-GCM (Standard) & Serpent-256 (High Security)
- 🚀 **Turbo Performance**: Custom C backend (`libserpent`) for Serpent acceleration
- 🔑 **PBKDF2**: Key derivation with HMAC-SHA256
- 🎨 **Modern Interface**: CustomTkinter with Dark/Matrix theme
- 👁️ **Deep Vision**: Inspection of internal rounds (AES MixColumns, Serpent S-Boxes)
- 📟 **Real-Time Monitor**: Visual terminal showing the crypto math live via sampling
- 📦 **Debian Package**: Easy installation via `.deb`
- 🎯 **Desktop Integration**: Drag & Drop support, Native File Dialogs
- 🔒 **Authenticated Encryption**: GCM (AES) and CTR+HMAC (Serpent) ensure integrity

## 🚀 Installation

### Method 1: Via .deb Package (Recommended)

```bash
# Install the package
sudo dpkg -i simple-encryptor.deb

# If dependencies are missing:
sudo apt-get install -f
```

### Method 2: Direct Execution

```bash
# Clone the repository
git clone https://github.com/your-username/simple-aes-encryptor.git
cd simple-aes-encryptor

# Install dependencies
sudo apt-get install python3-tk python3-cryptography
pip3 install customtkinter --break-system-packages

# Run
python3 simple-encryptor/usr/bin/simple-encryptor
```

## 💻 Usage

### Launch the Application

**Via Terminal:**
```bash
simple-encryptor
```

**Via Menu:** Search for "Simple AES Encryptor" in your applications menu (Utilities → Security)

### Encrypt a File

1. Click on **"Select File"**
2. Choose the desired file
3. Enter a **strong password**
4. Click on **"🔐 Encrypt"**
5. Watch the monitor showing the process in real-time
6. File will be saved as `[original-name].encrypted`

### Decrypt a File

1. Select the `.encrypted` file
2. Enter the **same password** used for encryption
3. Click on **"🔓 Decrypt"**
4. Original file will be restored

## 🔧 How It Works

### Encryption Process

```mermaid
graph LR
    A[Original File] --> B[Read]
    B --> C[PKCS7 Padding]
    C --> D[Generate Salt + IV]
    D --> E[Derive Key PBKDF2]
    E --> F[AES-256-CBC]
    F --> G[File.encrypted]
    
    style A fill:#90EE90
    style G fill:#FFB6C1
    style F fill:#87CEEB
```

### Encrypted File Structure

```
+----------------+----------------+------------------------+
|   Salt (16B)   |    IV (16B)    |   Encrypted Data       |
+----------------+----------------+------------------------+
```

### Technical Specifications

- **Algorithms**: 
    - AES-256 (GCM Mode)
    - Serpent-256 (CTR Mode + HMAC-SHA256)
- **Key Size**: 256 bits (32 bytes)
- **KDF**: PBKDF2-HMAC-SHA256 (100,000 iterations)
- **Integrity**: GCM Tag (16 bytes) or HMAC-SHA256 Tag (16 bytes)
- **Salt/IV**: Randomly generated per file (Secrets module)
- **Backend**: 
    - AES: OpenSSL (via `cryptography`)
    - Serpent: Custom C Extension (`libserpent.so`) + Pure Python Fallback

## 📁 Project Structure

```
simple-aes-encryptor/
├── simple-encryptor/           # Debian package structure
│   ├── DEBIAN/
│   │   └── control             # Package metadata
│   └── usr/
│       ├── bin/
│       │   └── simple-encryptor  # Main executable
│       └── share/
│           ├── applications/
│           │   └── simple-encryptor.desktop
│           └── icons/
│               └── simple-encryptor.png
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md         # Technical architecture
│   ├── SECURITY.md            # Security considerations
│   └── images/                # Images and screenshots
├── README.md                  # This file
├── LICENSE                    # MIT License
├── CONTRIBUTING.md            # Contribution guide
└── .gitignore                # Ignored files
```

## 🎨 Screenshots

### Main Interface
![Main Application Interface](docs/images/main_interface.png)

### Encryption Monitor
The visual terminal shows in real-time:
- Generated Salt and IV
- Derived Key
- Chunk-by-chunk progress
- Hexdump of encrypted data

![Real-time Encryption Monitor](docs/images/encryption_monitor.png)

```
======================================================================
STARTING ENCRYPTION AES-256-CBC
======================================================================
→ Generating salt: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
→ Generating IV:   f1e2d3c4b5a69788990a1b2c3d4e5f6
→ Deriving key PBKDF2 (100,000 iterations)...
→ Derived Key: 1234567890abcdef1234567890abcdef1234567890abcdef...

→ ENCRYPTING DATA...
  [ 10.0%] Chunk   1/ 10: a1b2c3d4e5f6789012345678901234567890abcdef...
  [ 20.0%] Chunk   2/ 10: f6e7d8c9b0a1928374650fabcdef0123456789ab...
```

## 🛡️ Security

> [!IMPORTANT]
> This app uses strong encryption (AES-256), but security depends on the **strength of your password**.

### Best Practices

✅ Use long passwords (minimum 12 characters)  
✅ Combine uppercase, lowercase, numbers, and symbols  
✅ Never share your passwords  
✅ Store passwords in a password manager  
⚠️ **If you forget the password, the file CANNOT be recovered!**

### Limitations

- ❌ Does not protect against keyloggers
- ❌ Does not protect against physical access to the system
- ❌ Does not include two-factor authentication

For more details, see [SECURITY.md](docs/SECURITY.md)

## 📚 Documentation

- [Technical Architecture](docs/ARCHITECTURE.md) - Implementation details
- [Security Guide](docs/SECURITY.md) - Security considerations
- [Contribution Guide](CONTRIBUTING.md) - How to contribute

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the process.

### Development

```bash
# Clone the repository
git clone https://github.com/your-username/simple-aes-encryptor.git
cd simple-aes-encryptor

# Install dev dependencies
sudo apt-get install python3-tk python3-cryptography

# Make your changes

# Rebuild package
dpkg-deb --build simple-encryptor

# Test
sudo dpkg -i simple-encryptor.deb
simple-encryptor
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Python Cryptography](https://cryptography.io/) - Cryptography library
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI Framework
- Icon made by [Pixel perfect](https://www.flaticon.com/authors/pixel-perfect) from [www.flaticon.com](https://www.flaticon.com/)

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/simple-aes-encryptor/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-username/simple-aes-encryptor/discussions)

## 🗺️ Roadmap

- [ ] Multi-file encryption
- [ ] Compression before encryption
- [ ] Interface in other languages
- [ ] Light/Dark theme
- [ ] Full folder encryption

---

<div align="center">

**Developed with ❤️ using Python**

[⬆ Back to top](#simple-aes-encryptor-)

</div>
