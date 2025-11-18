# DEVBRAIN V23 Protocolo Phoenix

Este diretório alberga a evolução do OmniMind descrita no Masterplan do DEVBRAIN V23. Cada submódulo representa uma das camadas sensoriais, cognitivas e imunes necessárias para alcançar a autonomia multimodal e a segurança P0.

Siga o Masterplan completo (`/run/media/fahbrain/DevBrain_Storage/DevBrain_V23/Masterplan.md`) ao implementar novas fases. Atualmente estamos focados em:

1. **Fase 9.2 – Visual Cortex** (`sensory/visual_cortex.py`): combinar OmniParser + YOLOv8 para "ver" o desktop, detectar elementos UI e clicar por labels.
2. **Fase 9.5 – Event Bus Redis** (`infrastructure/event_bus.py`): mover a comunicação JSONL para Redis Streams garantindo latência < 100ms.

Novas fases de cognição (LangGraph), memória A-MEM, e imunidade P0 devem ser adicionadas em diretórios homologados por este README antes de qualquer commit significativo.
