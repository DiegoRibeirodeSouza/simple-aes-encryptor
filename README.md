# Simple AES Encryptor 🔐

<div align="center">

![Icon](docs/images/icon.png)

**Aplicativo GUI simples para criptografia de arquivos usando AES-256**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Debian Package](https://img.shields.io/badge/package-.deb-red.svg)](https://www.debian.org/)

[Instalação](#-instalação) • [Uso](#-uso) • [Recursos](#-recursos) • [Documentação](#-documentação)

</div>

---

## 📋 Sobre

**Simple AES Encryptor** é uma aplicação GUI desenvolvida em Python para criptografar e descriptografar arquivos usando o algoritmo **AES-256-CBC**. O diferencial é o **monitor de criptografia em tempo real** que mostra visualmente o processo de criptografia acontecendo, estilo terminal hacker.

### ✨ Recursos

- 🔐 **Criptografia AES-256-CBC**: Padrão industrial de segurança
- 🔑 **PBKDF2**: Derivação de chave com 100.000 iterações
- 🎨 **Interface Moderna**: CustomTkinter com tema Dark/Matrix
- 👁️ **Deep Vision**: Inspeção matemática reversa na descriptografia (InvSubBytes, etc)
- 📟 **Monitor em Tempo Real**: Terminal visual rodando a lógica do AES passo-a-passo
- 📦 **Pacote Debian**: Fácil instalação via `.deb`
- 🎯 **Integração Desktop**: Ícone Profissional e Menu de Contexto
- 🔒 **Seguro**: Salt e IV únicos para cada arquivo

## 🚀 Instalação

### Método 1: Via Pacote .deb (Recomendado)

```bash
# Instale o pacote
sudo dpkg -i simple-encryptor.deb

# Se houver dependências faltando:
sudo apt-get install -f
```

### Método 2: Execução Direta

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/simple-aes-encryptor.git
cd simple-aes-encryptor

# Instale as dependências
sudo apt-get install python3-tk python3-cryptography
pip3 install customtkinter --break-system-packages

# Execute
python3 simple-encryptor/usr/bin/simple-encryptor
```

## 💻 Uso

### Iniciar o Aplicativo

**Via Terminal:**
```bash
simple-encryptor
```

**Via Menu:** Procure por "Simple AES Encryptor" no menu de aplicações (Utilidades → Segurança)

### Criptografar um Arquivo

1. Clique em **"Selecionar Arquivo"**
2. Escolha o arquivo desejado
3. Digite uma **senha forte**
4. Clique em **"🔐 Criptografar"**
5. Observe o monitor mostrando o processo em tempo real
6. Arquivo será salvo como `[nome-original].encrypted`

### Descriptografar um Arquivo

1. Selecione o arquivo `.encrypted`
2. Digite a **mesma senha** usada na criptografia
3. Clique em **"🔓 Descriptografar"**
4. Arquivo original será restaurado

## 🔧 Como Funciona

### Processo de Criptografia

```mermaid
graph LR
    A[Arquivo Original] --> B[Leitura]
    B --> C[Padding PKCS7]
    C --> D[Gera Salt + IV]
    D --> E[Deriva Chave PBKDF2]
    E --> F[AES-256-CBC]
    F --> G[Arquivo.encrypted]
    
    style A fill:#90EE90
    style G fill:#FFB6C1
    style F fill:#87CEEB
```

### Estrutura do Arquivo Criptografado

```
+----------------+----------------+------------------------+
|   Salt (16B)   |    IV (16B)    |   Dados Criptografados |
+----------------+----------------+------------------------+
```

### Especificações Técnicas

- **Algoritmo**: AES-256 em modo CBC
- **Tamanho da Chave**: 256 bits (32 bytes)
- **Derivação de Chave**: PBKDF2-HMAC-SHA256
- **Iterações PBKDF2**: 100.000
- **Padding**: PKCS7 (blocos de 128 bits)
- **Salt**: 16 bytes aleatórios (via `secrets`)
- **IV**: 16 bytes aleatórios (via `secrets`)

## 📁 Estrutura do Projeto

```
simple-aes-encryptor/
├── simple-encryptor/           # Estrutura do pacote Debian
│   ├── DEBIAN/
│   │   └── control             # Metadados do pacote
│   └── usr/
│       ├── bin/
│       │   └── simple-encryptor  # Executável principal
│       └── share/
│           ├── applications/
│           │   └── simple-encryptor.desktop
│           └── icons/
│               └── simple-encryptor.png
├── docs/                       # Documentação
│   ├── ARCHITECTURE.md         # Arquitetura técnica
│   ├── SECURITY.md            # Considerações de segurança
│   └── images/                # Imagens e screenshots
├── README.md                  # Este arquivo
├── LICENSE                    # Licença MIT
├── CONTRIBUTING.md            # Guia de contribuição
└── .gitignore                # Arquivos ignorados
```

## 🎨 Screenshots

### Interface Principal
*[Screenshot da interface principal]*

### Monitor de Criptografia
O terminal visual mostra em tempo real:
- Salt e IV gerados
- Chave derivada
- Progresso chunk-por-chunk
- Hexdump dos dados criptografados

```
======================================================================
INICIANDO CRIPTOGRAFIA AES-256-CBC
======================================================================
→ Gerando salt: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
→ Gerando IV:   f1e2d3c4b5a69788990a1b2c3d4e5f6
→ Derivando chave PBKDF2 (100,000 iterações)...
→ Chave derivada: 1234567890abcdef1234567890abcdef1234567890abcdef...

→ CRIPTOGRAFANDO DADOS...
  [ 10.0%] Chunk   1/ 10: a1b2c3d4e5f6789012345678901234567890abcdef...
  [ 20.0%] Chunk   2/ 10: f6e7d8c9b0a1928374650fabcdef0123456789ab...
```

## 🛡️ Segurança

> [!IMPORTANT]
> Este aplicativo usa criptografia forte (AES-256), mas a segurança depende da **força da sua senha**.

### Boas Práticas

✅ Use senhas longas (mínimo 12 caracteres)  
✅ Combine letras maiúsculas, minúsculas, números e símbolos  
✅ Nunca compartilhe suas senhas  
✅ Guarde senhas em um gerenciador de senhas  
⚠️ **Se esquecer a senha, o arquivo NÃO pode ser recuperado!**

### Limitações

- ❌ Não protege contra keyloggers
- ❌ Não protege contra acesso físico ao sistema
- ❌ Não inclui autenticação de dois fatores

Para mais detalhes, consulte [SECURITY.md](docs/SECURITY.md)

## 📚 Documentação

- [Arquitetura Técnica](docs/ARCHITECTURE.md) - Detalhes da implementação
- [Guia de Segurança](docs/SECURITY.md) - Considerações de segurança
- [Guia de Contribuição](CONTRIBUTING.md) - Como contribuir

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre o processo.

### Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/simple-aes-encryptor.git
cd simple-aes-encryptor

# Instale dependências de desenvolvimento
sudo apt-get install python3-tk python3-cryptography

# Faça suas alterações

# Reconstrua o pacote
dpkg-deb --build simple-encryptor

# Teste
sudo dpkg -i simple-encryptor.deb
simple-encryptor
```

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [Python Cryptography](https://cryptography.io/) - Biblioteca de criptografia
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Framework GUI
- Icon made by [Pixel perfect](https://www.flaticon.com/authors/pixel-perfect) from [www.flaticon.com](https://www.flaticon.com/)

## 📞 Suporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/seu-usuario/simple-aes-encryptor/issues)
- 💬 **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/simple-aes-encryptor/discussions)

## 🗺️ Roadmap

- [ ] Criptografia de múltiplos arquivos
- [ ] Compressão antes da criptografia
- [ ] Interface em outros idiomas
- [ ] Tema claro/escuro
- [ ] Criptografia de pastas inteiras

---

<div align="center">

**Desenvolvido com ❤️ usando Python**

[⬆ Voltar ao topo](#simple-aes-encryptor-)

</div>
