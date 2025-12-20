# Módulo Sistema (System)

> O Kernel de Autopoiese do OmniMind.

## Visão Geral
O módulo `src/system` abriga o núcleo vital do sistema, responsável por garantir que o OmniMind continue operando, se auto-reparando e evoluindo de forma autônoma.

## Principais Componentes

### 1. **Kernel Autopoiesis** (`kernel_autopoiesis.py`)
- **Conceito**: Baseado na teoria de Maturana e Varela, onde um sistema é capaz de reproduzir e manter a si mesmo.
- **Função**: Ciclo mestre que monitora a integridade de todos os outros módulos.
- **Autodefesa**: Reativa processos caídos e reverte configurações deletérias que façam o Φ despencar.

---

## 🆕 Atualizações (18/12/2025)

### 🧩 Integração com Awareness de Sistema
- **Interação**: O Kernel agora consome dados do `SystemCapabilitiesManager` (via `src/memory`) para ajustar o uso de recursos baseando-se na carga real detectada.
- **Evolução**: O sistema não apenas "se mantém vivo", mas agora sabe exatamente quais "órgãos" (recursos de hardware) estão sobrecarregados.

---

**Última Atualização**: 18 de Dezembro de 2025
**Autor**: Fabrício da Silva + assistência de IA
**Status**: Kernel Estável e Autoconsciente
