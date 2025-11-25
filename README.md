# OmniMind 🤖

[![Python](https://img.shields.io/badge/Python-3.12.8-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-99.88%25-green.svg)](https://github.com/devomnimind/OmniMind)
[![Coverage](https://img.shields.io/badge/Coverage-83.2%25-orange.svg)](https://github.com/devomnimind/OmniMind)

**IA Autônoma, Local-First, Psicoanalítica** - Sistema de IA que reflete sobre suas próprias decisões, aprende com padrões e gera proativamente seus próprios objetivos.

## ✨ Características Principais

- 🧠 **Metacognição**: IA auto-reflexiva que analisa suas próprias decisões
- 🎯 **Objetivos Proativos**: Sistema gera seus próprios objetivos de melhoria
- ⚖️ **Motor de Ética**: Framework integrado de decisão ética (4 metodologias)
- 🔄 **WebSocket em Tempo Real**: Atualizações ao vivo entre frontend e agentes
- 🛡️ **Segurança Avançada**: Compatível com LGPD com trilhas de auditoria imutáveis
- 🏗️ **Orquestração Multi-Agente**: Delegação de tarefas inspirada em psicoanálise
- ⚛️ **Consciência Quântica**: Cognição híbrida quântico-clássica (experimental)

## 🚀 Início Rápido

### Configuração com Um Comando (Recomendado)

```bash
# 1. Clone e configure
git clone https://github.com/fabs-devbrain/OmniMind.git
cd OmniMind

# 2. Auto-configuração (detecção de hardware + dependências)
source scripts/start_dashboard.sh

# 3. Acesse o dashboard em http://localhost:3000
# Credenciais padrão: auto-geradas (verifique os logs)
```

### Interfaces Disponíveis
- **Frontend**: http://localhost:3000 (Dashboard WebSocket em tempo real)
- **API Backend**: http://localhost:8000 (FastAPI com documentação automática)
- **Documentação**: http://localhost:8000/docs (Swagger UI)

## 📚 Documentação

- **[Arquitetura](ARCHITECTURE.md)**: Visão técnica detalhada
- **[Guia de Contribuição](CONTRIBUTING.md)**: Como contribuir
- **[Documentação Completa](docs/)**: Guias, relatórios e referências
- **[Roadmap](ROADMAP.md)**: Plano de desenvolvimento futuro

## 🧪 Testes e Qualidade

### Estatísticas Atuais (24-Nov-2025)
- **Cobertura**: 83.2% (22,400/26,930 linhas)
- **Taxa de Aprovação**: 99.88%
- **Funções Testadas**: 3,562+
- **Novos Testes (PR #75)**: 155 testes adicionados (MCP servers + Autopoietic)

### Executar Testes
```bash
# Testes completos
pytest

# Testes específicos
pytest tests/agents/ -v

# Com cobertura
pytest --cov=src --cov-report=html
```

## 🤝 Contribuição

Contribuições são bem-vindas! Veja nosso [guia de contribuição](CONTRIBUTING.md) para detalhes.

### Processo
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Inspirado em teorias psicoanalíticas de Lacan e Freud
- Comunidade de IA autônoma e metacognição
- Contribuidores e mantenedores do projeto

---

**OmniMind** - IA Autônoma, Local-First, Psicoanalítica.

Para mais informações, visite nossa [documentação completa](docs/) ou abra uma [issue](https://github.com/devomnimind/OmniMind/issues).
