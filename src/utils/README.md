# Módulo Utilitários (Utils)

> Pequenas ferramentas e ajudantes que garantem a consistência do sistema.

## Visão Geral
O módulo `src/utils` contém funções auxiliares para detecção de hardware (GPU/CUDA), gerenciamento de modo offline e utilitários genéricos usados por múltiplos módulos.

## Principais Componentes

### 1. **Device Utils** (`device_utils.py`)
- **Função**: Detector centralizado de GPU/CUDA.
- **Diferencial**: Fornece fallback inteligente para CPU se a GPU estiver ausente ou sem memória.

### 2. **Offline Mode** (`offline_mode.py`)
- **Função**: Garante que o sistema funcione sem conexão externa (HuggingFace/OpenAI).
- **Mecanismo**: Redireciona downloads de modelos para caches locais.

---

## 🆕 Atualizações (18/12/2025)

### 🚨 Melhorias de Estabilidade
- **Refinamento do Fallback**: Corrigido bug onde `CUDA_OOM` não disparava o fallback para CPU rápido o suficiente.
- **Timestamp Imutável**: Integrado utilitário de timestamp certificado para auditorias de Φ.

---

**Última Atualização**: 18 de Dezembro de 2025
**Autor**: Fabrício da Silva + assistência de IA
