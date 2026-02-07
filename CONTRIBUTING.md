# Contributing to Simple Encryptor GCM

Thank you for your interest in contributing! 🎉

## 📋 Code of Conduct

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what is best for the community

## 🚀 How to Contribute

### Reporting Bugs

Before creating an issue, check if a similar one already exists.

**When reporting a bug, include:**
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Python version, OS, and app version
- Logs or screenshots (if applicable)

### Suggesting Improvements

Issues for new features are welcome! Include:
- Detailed description of the feature
- Why it would be useful
- Usage examples

### Pull Requests

1. **Fork** the repository
2. **Create** a branch for your feature (`git checkout -b feature/MyFeature`)
3. **Commit** your changes (`git commit -m 'Add MyFeature'`)
4. **Push** to the branch (`git push origin feature/MyFeature`)
5. **Open** a Pull Request

## 💻 Development Environment Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/simple-aes-encryptor.git
cd simple-aes-encryptor

# Install dependencies
sudo apt-get install python3-tk python3-cryptography

# Test the app
python3 simple-encryptor/usr/bin/simple-encryptor
```

## 🧪 Testing

Before submitting a PR:

1. **Functional Test**: Run the app and test encryption/decryption
2. **Test with different files**: Small, large, various formats
3. **Test .deb installation**: Rebuild and install the package

```bash
# Rebuild package
dpkg-deb --build simple-encryptor

# Install
sudo dpkg -i simple-encryptor.deb

# Test
simple-encryptor
```

## 📝 Code Conventions

### Python
- Follow [PEP 8](https://pep8.org/)
- Use docstrings for functions/classes
- Descriptive variable names
- Comments in English

### Commits
- Use clear and descriptive messages
- Use English for commit messages
- Format: `type: description`

Examples:
```
feat: add drag and drop support
fix: fix error when decrypting large files
docs: update README with examples
refactor: improve encryption code structure
```

## 🏗️ Code Structure

```python
class EncryptorApp:
    """Main application class"""
    
    def __init__(self, root):
        """Initialize UI"""
        
    def _setup_ui(self):
        """Setup UI elements"""
        
    def _encrypt_file_thread(self):
        """Encryption thread"""
        
    def _decrypt_file_thread(self):
        """Decryption thread"""
```

## 🎯 Contribution Areas

### Easy
- Documentation improvements
- Typo fixes
- Translations
- Visual UI improvements

### Medium
- Add color themes
- Improve error handling
- Add strong password validation
- Performance improvements

### Advanced
- Implement drag and drop (Platform specific improvements)
- Add folder encryption (Native recursion)
- Compression before encryption
- Support for other algorithms

## 📦 Debian Package Build

Control structure:
```
Package: simple-aes-encryptor
Version: 1.0.0
Architecture: all
Depends: python3 (>= 3.9), python3-tk, python3-cryptography
```

When modifying dependencies, update `simple-encryptor/DEBIAN/control`

## ✅ PR Checklist

Before submitting:

- [ ] Code follows PEP 8
- [ ] Tested on Debian/Ubuntu
- [ ] Documentation updated (if necessary)
- [ ] Commit messages are clear
- [ ] .deb package works after rebuild
- [ ] No warnings or errors in code

## 🤔 Questions?

- Open a [Discussion](https://github.com/your-username/simple-aes-encryptor/discussions)
- Or comment on existing issues

## 🙏 Recognition

Contributors will be listed in the README!

---

**Thanks for contributing!** 🚀
