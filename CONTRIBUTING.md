# Contribuindo para Simple AES Encryptor

Obrigado pelo seu interesse em contribuir! 🎉

## 📋 Código de Conduta

- Seja respeitoso e inclusivo
- Aceite críticas construtivas
- Foque no que é melhor para a comunidade

## 🚀 Como Contribuir

### Reportando Bugs

Antes de criar um issue, verifique se já não existe um similar.

**Ao reportar um bug, inclua:**
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Versão do Python, SO, e do aplicativo
- Logs ou screenshots (se aplicável)

### Sugerindo Melhorias

Issues para novas funcionalidades são bem-vindas! Inclua:
- Descrição detalhada da funcionalidade
- Por que seria útil
- Exemplos de uso

### Pull Requests

1. **Fork** o repositório
2. **Crie** um branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push** para o branch (`git push origin feature/MinhaFeature`)
5. **Abra** um Pull Request

## 💻 Configuração do Ambiente de Desenvolvimento

```bash
# Clone seu fork
git clone https://github.com/SEU-USUARIO/simple-aes-encryptor.git
cd simple-aes-encryptor

# Instale dependências
sudo apt-get install python3-tk python3-cryptography

# Teste o aplicativo
python3 simple-encryptor/usr/bin/simple-encryptor
```

## 🧪 Testes

Antes de submeter um PR:

1. **Teste funcional**: Execute o app e teste criptografia/descriptografia
2. **Teste com diferentes arquivos**: Pequenos, grandes, vários formatos
3. **Teste a instalação do .deb**: Reconstrua e instale o pacote

```bash
# Reconstruir pacote
dpkg-deb --build simple-encryptor

# Instalar
sudo dpkg -i simple-encryptor.deb

# Testar
simple-encryptor
```

## 📝 Convenções de Código

### Python
- Siga [PEP 8](https://pep8.org/)
- Use docstrings para funções/classes
- Nomes descritivos de variáveis
- Comentários em português ou inglês

### Commits
- Use mensagens claras e descritivas
- Prefira inglês para mensagens de commit
- Formato: `tipo: descrição`

Exemplos:
```
feat: adiciona suporte a drag and drop
fix: corrige erro ao descriptografar arquivos grandes
docs: atualiza README com exemplos
refactor: melhora estrutura do código de criptografia
```

## 🏗️ Estrutura do Código

```python
class EncryptorApp:
    """Classe principal da aplicação"""
    
    def __init__(self, root):
        """Inicializa a interface"""
        
    def _setup_ui(self):
        """Configura elementos da UI"""
        
    def _encrypt_file_thread(self):
        """Thread de criptografia"""
        
    def _decrypt_file_thread(self):
        """Thread de descriptografia"""
```

## 🎯 Áreas para Contribuição

### Fácil
- Melhorias na documentação
- Correção de typos
- Tradução para outros idiomas
- Melhorias visuais na UI

### Médio
- Adicionar temas de cores
- Melhorar tratamento de erros
- Adicionar validação de senha forte
- Melhorias de performance

### Avançado
- Implementar drag and drop
- Adicionar criptografia de pastas
- Compressão antes da criptografia
- Suporte a outros algoritmos

## 📦 Build do Pacote Debian

Estrutura do controle:
```
Package: simple-aes-encryptor
Version: 1.0.0
Architecture: all
Depends: python3 (>= 3.9), python3-tk, python3-cryptography
```

Ao modificar dependências, atualize `simple-encryptor/DEBIAN/control`

## ✅ Checklist do PR

Antes de submeter:

- [ ] Código segue PEP 8
- [ ] Testado em Debian/Ubuntu
- [ ] Documentação atualizada (se necessário)
- [ ] Commit messages são claros
- [ ] Pacote .deb funciona após rebuild
- [ ] Nenhum warning ou erro no código

## 🤔 Dúvidas?

- Abra uma [Discussion](https://github.com/seu-usuario/simple-aes-encryptor/discussions)
- Ou comente em issues existentes

## 🙏 Reconhecimento

Contribuidores serão listados no README!

---

**Obrigado por contribuir!** 🚀
