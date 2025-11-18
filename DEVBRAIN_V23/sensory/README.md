# Tier 1 Sensory Stack

This package contains the Tier 1 sensory components for DEVBRAIN V23:

- `VisualCortex`: Screen understanding + GUI interaction via OmniParser/YOLO fallback, with performance logging, error alerting, and click helpers.
- `VoiceInterface`: Local voice I/O that wraps Whisper (STT) and the TTS module, exposing `listen`/`speak` flows plus instrumentation and alert hooks.

Both modules expose async helpers, accept injection points (parser/yolo models, STT/TTS clients, audio handlers), and maintain small metric buffers to monitor responsiveness. Use this package for the visual+voice experience layer and surface its alerts back to Tier 0 orchestrators for telemetry.# DEVBRAIN V23 Sensory Vision

Este módulo implementa o **Visual Cortex** descrito no Masterplan (Fase 9.2) e representa o "olho" do DevBrain V23. Ele combina o parser de UI da Microsoft (`OmniParser`) com o detector YOLOv8 para identificar elementos visuais na tela e agir sobre eles sem depender de coordenadas fixas.

## Estrutura

- `VisualCortex`: captura screenshots, normaliza os elementos detectados e dispara cliques inteligentes por label.
- O parser e o detector são inicializados de forma flexível para permitir mocks em ambientes de teste ou sensores físicos diferentes.
- É possível passar um handler de clique customizado para integrar com ferramentas como `pyautogui`, `xdotool` ou interfaces headless.

## Uso básico

```python
from DEVBRAIN_V23.sensory.visual_cortex import VisualCortex

visual = VisualCortex()
result = await visual.see_screen()
print(result["elements"])
await visual.click_element("Salvar")
```

## Testes e automação de apps legados

O teste `tests/test_visual_cortex.py` valida que capturamos `elements` e `detections` sem exigir uma tela real, utilizando mocks para o parser e o detector. Isso garante que a integração com aplicações legadas (sem API) seja confiável antes mesmo de conectar sensores reais.
