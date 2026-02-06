# Guia de Instalação - Simple AES Encryptor

## 📋 Pré-requisitos

### Sistema Operacional
- Debian 11+ (Bullseye, Bookworm, Trixie)
- Ubuntu 20.04+ (Focal, Jammy, Noble)
- Linux Mint 20+
- Outros derivados Debian/Ubuntu

### Dependências
- `python3` (>= 3.9)
- `python3-tk`
- `python3-cryptography`

## 🚀 Método 1: Instalação via Pacote .deb (Recomendado)

### Passo 1: Download

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/simple-aes-encryptor.git
cd simple-aes-encryptor

# Ou baixe apenas o .deb se disponível
wget https://github.com/seu-usuario/simple-aes-encryptor/releases/download/v1.0.0/simple-encryptor.deb
```

### Passo 2: Instalação

```bash
# Instale o pacote
sudo dpkg -i simple-encryptor.deb

# Se houver erros de dependências, resolva com:
sudo apt-get install -f
```

### Passo 3: Verificação

```bash
# Verifique se está instalado
which simple-encryptor

# Deve retornar: /usr/bin/simple-encryptor

# Execute o aplicativo
simple-encryptor
```

### Desinstalação

```bash
sudo apt remove simple-aes-encryptor
```

## 🔧 Método 2: Execução Direta (Sem Instalação)

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/seu-usuario/simple-aes-encryptor.git
cd simple-aes-encryptor
```

### Passo 2: Instale as Dependências

```bash
sudo apt-get update
sudo apt-get install python3-tk python3-cryptography
```

### Passo 3: Execute

```bash
python3 simple-encryptor/usr/bin/simple-encryptor
```

## 🏗️ Método 3: Build do Pacote (Desenvolvedores)

### Passo 1: Prepare o Ambiente

```bash
git clone https://github.com/seu-usuario/simple-aes-encryptor.git
cd simple-aes-encryptor
```

### Passo 2: Build

```bash
# Construa o pacote .deb
dpkg-deb --build simple-encryptor

# O arquivo simple-encryptor.deb será gerado
```

### Passo 3: Instale

```bash
sudo dpkg -i simple-encryptor.deb
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'tkinter'"

**Problema:** Python Tkinter não está instalado.

**Solução:**
```bash
sudo apt-get install python3-tk
```

### Erro: "ModuleNotFoundError: No module named 'cryptography'"

**Problema:** Biblioteca cryptography não está instalada.

**Solução:**
```bash
sudo apt-get install python3-cryptography
```

### Erro: "dpkg: dependency problems prevent configuration"

**Problema:** Dependências faltando.

**Solução:**
```bash
sudo apt-get install -f
```

### Erro: "Permission denied"

**Problema:** Arquivo não é executável.

**Solução:**
```bash
chmod +x simple-encryptor/usr/bin/simple-encryptor
```

### Aplicativo não aparece no menu

**Solução:**
```bash
# Atualize cache do menu
sudo update-desktop-database
```

## 📦 Estrutura de Instalação

Após a instalação, os seguintes arquivos serão criados:

```
/usr/bin/simple-encryptor              → Executável principal
/usr/share/applications/simple-encryptor.desktop  → Entry do menu
/usr/share/icons/simple-encryptor.png  → Ícone da aplicação
```

## 🔍 Verificação da Instalação

Execute os seguintes comandos para verificar:

```bash
# 1. Verificar executável
ls -l /usr/bin/simple-encryptor

# 2. Verificar desktop entry
ls -l /usr/share/applications/simple-encryptor.desktop

# 3. Verificar ícone
ls -l /usr/share/icons/simple-encryptor.png

# 4. Verificar dependências
dpkg -l | grep python3-tk
dpkg -l | grep python3-cryptography

# 5. Testar execução
simple-encryptor --help 2>/dev/null || echo "OK - App iniciado"
```

## 💾 Instalação em Outros Sistemas

### Arch Linux / Manjaro

```bash
# Instale dependências
sudo pacman -S python-tk python-cryptography

# Execute diretamente
python simple-encryptor/usr/bin/simple-encryptor
```

### Fedora / RHEL / CentOS

```bash
# Instale dependências
sudo dnf install python3-tkinter python3-cryptography

# Execute diretamente
python3 simple-encryptor/usr/bin/simple-encryptor
```

### openSUSE

```bash
# Instale dependências
sudo zypper install python3-tk python3-cryptography

# Execute diretamente
python3 simple-encryptor/usr/bin/simple-encryptor
```

> [!NOTE]
> O pacote .deb é específico para Debian/Ubuntu. Para outros sistemas, use o método de execução direta.

## 🆘 Suporte

Se encontrar problemas:

1. Verifique os [Issues](https://github.com/seu-usuario/simple-aes-encryptor/issues) existentes
2. Abra um novo issue com:
   - Versão do sistema operacional
   - Versão do Python (`python3 --version`)
   - Mensagem de erro completa
   - Passos para reproduzir

---

**Última atualização:** 2026-02-06
