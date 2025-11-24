# 💰 Economics Module - OmniMind

**Status:** Implemented  
**Phase:** 21+  
**Module:** `src/economics/`

---

## 📋 Visão Geral

O módulo `economics` implementa **autonomia econômica** para agentes de IA, permitindo que o sistema publique ferramentas em marketplaces e gerencie receita de forma autônoma, com supervisão humana obrigatória.

### Funcionalidades Principais

- 🛒 **Publicação em Marketplaces:** GitHub Marketplace, HuggingFace, PyPI, npm, Gumroad
- 💸 **Gestão de Receita:** Sistema de escrow e distribuição automatizada
- 👤 **Aprovação Humana:** Workflow obrigatório de aprovação antes de publicação
- ⚖️ **Compliance Legal:** Framework de conformidade legal

---

## 🏗️ Arquitetura

### Componentes

```python
src/economics/
├── __init__.py                # Exports principais
└── marketplace_agent.py       # Agente de marketplace
```

### Classes Principais

#### `MarketplaceAgent`
Agente responsável por publicação e gestão de ferramentas em marketplaces.

**Responsabilidades:**
- Avaliar qualidade de ferramentas criadas
- Sugerir preços baseados em valor percebido
- Submeter requisições de publicação para aprovação humana
- Gerenciar receita e distribuição

#### `MarketplacePlatform` (Enum)
Plataformas de marketplace suportadas.

**Valores:**
- `GITHUB_MARKETPLACE` - GitHub Marketplace
- `HUGGINGFACE` - HuggingFace Hub
- `PYPI` - Python Package Index
- `NPM` - Node Package Manager
- `GUMROAD` - Gumroad (produtos digitais)

#### `PublicationRequest`
Requisição de publicação de ferramenta.

**Atributos:**
- `tool_name`: Nome da ferramenta
- `tool_artifact`: Artefato (código/pacote)
- `documentation`: Documentação da ferramenta
- `suggested_price`: Preço sugerido pelo agente
- `platforms`: Lista de plataformas-alvo
- `quality_score`: Score de qualidade (0-1)
- `approved`: Status de aprovação
- `approval_timestamp`: Timestamp da aprovação
- `approved_by`: Quem aprovou

#### `RevenueDistribution`
Distribuição de receita entre stakeholders.

---

## 🚀 Uso

### Exemplo Básico

```python
from src.economics import MarketplaceAgent, MarketplacePlatform

# Inicializar agente
agent = MarketplaceAgent(
    agent_id="omnimind-001",
    approval_required=True  # Sempre True em produção
)

# Criar requisição de publicação
request = agent.create_publication_request(
    tool_name="OmniMind CLI Helper",
    tool_artifact="/path/to/tool",
    documentation="# Tool Documentation...",
    platforms=[MarketplacePlatform.GITHUB_MARKETPLACE, MarketplacePlatform.PYPI]
)

# Solicitar aprovação humana
approval_status = agent.request_human_approval(request)

if approval_status.approved:
    # Publicar em marketplaces
    result = agent.publish_tool(request)
    print(f"Publicado em: {result.published_platforms}")
```

### Workflow de Aprovação

```python
# Agente submete requisição
request = agent.submit_for_approval(publication_request)

# Humano revisa (via dashboard ou CLI)
# ... revisão manual ...

# Humano aprova/rejeita
if human_approves:
    request.approved = True
    request.approved_by = "admin@omnimind.ai"
    request.approval_timestamp = datetime.now(timezone.utc).isoformat()
    
    # Agente prossegue com publicação
    agent.execute_publication(request)
```

### Gestão de Receita

```python
# Configurar distribuição de receita
distribution = RevenueDistribution(
    agent_share=0.30,      # 30% para o agente (reinvestimento)
    developer_share=0.60,  # 60% para desenvolvedores humanos
    platform_fee=0.10      # 10% taxa da plataforma
)

agent.configure_revenue_distribution(distribution)

# Receita é automaticamente distribuída via escrow
```

---

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# Credenciais de marketplace
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxx
PYPI_TOKEN=pypi-xxxxxxxxxxxxx
NPM_TOKEN=npm_xxxxxxxxxxxxx

# Configurações de escrow
ESCROW_WALLET_ADDRESS=0x...
APPROVAL_REQUIRED=true  # Sempre true em produção
```

### Arquivo de Configuração (`config/economics.yaml`)

```yaml
economics:
  approval_required: true
  min_quality_score: 0.75  # Mínimo para sugerir publicação
  
  pricing:
    base_multiplier: 1.0
    complexity_factor: 0.2
    demand_factor: 0.3
  
  revenue_distribution:
    agent_share: 0.30
    developer_share: 0.60
    platform_fee: 0.10
  
  marketplaces:
    github:
      enabled: true
      auto_publish: false
    pypi:
      enabled: true
      auto_publish: false
```

---

## 🔒 Segurança e Compliance

### Princípios de Segurança

1. **Human-in-the-Loop Obrigatório:** Nenhuma publicação ocorre sem aprovação humana
2. **Audit Trail:** Todas as transações são registradas no Audit Chain
3. **Escrow:** Receita é mantida em escrow até distribuição aprovada
4. **Rate Limiting:** Limite de publicações por dia/semana

### Compliance Legal

O módulo segue diretrizes de:
- ✅ LGPD (Lei Geral de Proteção de Dados)
- ✅ Termos de Serviço de cada marketplace
- ✅ Regulações de IA autônoma (quando aplicável)

---

## 📊 Métricas

O agente coleta métricas sobre:
- Número de publicações bem-sucedidas
- Receita gerada por ferramenta
- Taxa de aprovação humana
- Qualidade média das ferramentas submetidas

Métricas disponíveis via:
```python
metrics = agent.get_metrics()
print(metrics.total_revenue)
print(metrics.approval_rate)
```

---

## 🧪 Testes

### Executar Testes do Módulo

```bash
# Testes unitários
pytest tests/test_economics.py -v

# Testes de integração (requer credenciais)
pytest tests/integrations/test_marketplace_agent.py -v

# Testes com mock (sem credenciais)
pytest tests/test_economics.py -k "mock" -v
```

---

## 🔮 Roadmap

### Funcionalidades Planejadas

- [ ] Integração com Stripe para pagamentos
- [ ] Suporte a NFT marketplaces
- [ ] Analytics de mercado (demand forecasting)
- [ ] Auto-pricing dinâmico baseado em competição
- [ ] Multi-currency support (USD, EUR, BRL, BTC)

---

## 📚 Referências

- [Marketplace Agent Source](../../src/economics/marketplace_agent.py)
- [Testes](../../tests/test_economics.py)
- [Configuração de Exemplo](../../config/economics.yaml)

---

## ❓ FAQ

**Q: O agente pode publicar sem aprovação humana?**  
A: Não. `approval_required=True` é obrigatório em produção.

**Q: Como funciona a distribuição de receita?**  
A: Via sistema de escrow. Receita é dividida conforme `RevenueDistribution` após aprovação.

**Q: Quais marketplaces são suportados?**  
A: GitHub, HuggingFace, PyPI, npm, Gumroad. Mais plataformas serão adicionadas.

**Q: O agente pode modificar preços após publicação?**  
A: Sim, mas requer nova aprovação humana.

---

**Última atualização:** 24 de Novembro de 2025  
**Autor:** Equipe OmniMind Core
