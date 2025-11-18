# DEVBRAIN V23 Event Bus

Este componente representa o backbone de mensagens do DevBrain V23 (Fase 9.5). Substitui os arquivos JSONL por **Redis Streams**, garantindo comunicação em tempo real, latência reduzida e controle de ordenação entre agentes.

A classe `EventBusRedis` permite publicar eventos em canais nomeados e registrar _handlers_ assíncronos que respondem automaticamente, mantendo o modelo event-driven previsto no Masterplan.
