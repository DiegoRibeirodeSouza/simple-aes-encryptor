# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [3.12.0] - 2026-02-07
### Adicionado
- 👁️ **CLI Visualization**: Adicionado modo visual (`--verbose` ou `-v`) na CLI.
    - Exibe logs detalhados de criptografia em tempo real no terminal.
    - Mostra rounds do Serpent/AES, geração de keystream e operações XOR.
    - Ideal para fins educacionais e de auditoria via terminal.
- ℹ️ **Help Otimizado**: Mensagens de ajuda da CLI (`-h`) refinadas e 100% em inglês.

## [3.11.0] - 2026-02-07
### Adicionado
- 💻 **CLI Mode**: Nova ferramenta de linha de comando `simple-encryptor-cli` incluída no pacote.
    - Suporte completo a criptografia/descriptografia via terminal.
    - Compatível com scripts e automação.
    - Uso: `simple-encryptor-cli -e arquivo -p senha --algo SERPENT`

## [3.10.0] - 2026-02-07
### Otimizações
- 🚀 **Performance Extrema**: Substituída a implementação Python pura do Serpent CTR por chamadas diretas à `libgcrypt` do sistema.
- ⚡ **Aceleração**: Velocidade de criptografia Serpent saltou de ~2 MB/s para **~300 MB/s**.
- 👁️ **Visualização Precisa**: Log visual agora exibe o keystream real gerado pela `libgcrypt` e `cryptography` (AES), garantindo fidelidade matemática absoluta.

### Correções
- 🐛 **Sincronia de Logs**: Corrigida a discrepância entre o log visual (simulação) e o arquivo real. Agora o que você vê é o que é gravado.
- 📦 **Dependências**: Atualizado pacote `.deb` para depender da `libgcrypt20`.

## [4.7] - 2026-02-06
### Added
- 🌍 **English Translation**: Complete localization of UI and Technical Logs.
- 🎨 **New Icon**: Final professional icon integrated.
- 🐛 **Bug Fixes**: Fixed import errors and redundant translation blocks.

## [4.6] - 2026-02-06
### Added
- 🚀 **Turbo Serpent**: Implemented `libserpent.so` (C Extension) to replace pure Python backend.
- ⚡ **Performance**: Encryption of large files is now instant (native speed).
- 🧠 **Hybrid Architecture**: Uses C for data processing and Python for educational visualization.

## [4.5] - 2026-02-06
### Added
- 🐍 **Serpent Cipher**: Added Serpent-256 algorithm support.
- 👁️ **32-Round Trace**: Full visualization of Serpent's internal rounds.
- 🔒 **Authenticated Encryption**: Implemented CTR mode + HMAC-SHA256 for Serpent.

## [4.0] - 2026-02-06
### Changed
- 🛡️ **AES-GCM**: Migrated from CBC to GCM mode for authenticated encryption.
- 📂 **Folder Support**: Added automatic tar-stream encryption for folders.

## [3.9] - 2026-02-06
### Adicionado
- 🔐 **Descriptografia Visível ("Deep Vision")**: Implementação completa da matemática inversa do AES (InvSubBytes, InvShiftRows, InvMixColumns) no visualizador.
- 🎨 **Interface Moderna**: Migração completa para `CustomTkinter` (Material Design Dark).
- 🛡️ **Ícone Profissional**: Novo ícone "Gold Lock" de alta definição.
- � **Barra de Progresso Real**: Visualização precisa do progresso de criptografia/descriptografia.
- � **Seletor Nativo**: Uso de `zenity/kdialog` para seleção de arquivos mais amigável.

### Corrigido
- 🐛 Correção no `startup-notification` que causava cursor girando infinitamente.
- 🐛 Correção na assinatura da função de descriptografia que impedia a visualização.
- ⚡ Otimização do visualizador para não gargalar a criptografia (throttling inteligente).

## [2.0] - 2026-02-06
### Adicionado
- �️ **Deep Vision**: Modo de inspeção detalhada dos rounds do AES.
- � Medidor de Força de Senha em tempo real.

## [1.0.0] - 2026-02-06
### Adicionado
- ✨ Interface gráfica básica (Tkinter clássico)
- � Criptografia AES-256-CBC
- 🔑 Derivação de chave PBKDF2
- 📦 Pacote Debian (.deb)

---

## [Unreleased]

### Planejado
- [ ] Suporte a drag and drop
- [ ] Criptografia de múltiplos arquivos (batch)
- [ ] Compressão antes de criptografar
- [ ] Progress bar gráfica
- [ ] Temas de cores (claro/escuro)
- [ ] Internacionalização (i18n)
- [ ] HMAC para autenticação (ou migrar para AES-GCM)
- [ ] Verificador de força de senha
- [ ] Histórico de operações

---

## Legenda

- **Adicionado**: para novas funcionalidades
- **Modificado**: para mudanças em funcionalidades existentes
- **Descontinuado**: para funcionalidades que serão removidas
- **Removido**: para funcionalidades removidas
- **Corrigido**: para correção de bugs
- **Segurança**: em caso de vulnerabilidades
