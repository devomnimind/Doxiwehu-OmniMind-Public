# Agentic Memory (A‑MEM)

This package provides the **A‑MEM** Agentic Memory described in the Phase 9 Tier 0 foundation. It integrates directly with `chromadb` to store:

- **Episodic traces** (`episodic` collection with version metadata).
- **Semantic extractions** (`semantic` collection for learned concepts).
- **Procedural fixes** (`procedural` collection for resilience scripts).

Features:
- Async wrapper over blocking Chroma operations via `asyncio.to_thread`.
- Query caching and simple cache statistics to reduce repeated vector lookups.
- Version tracking per write and consolidation reporting to support control of memory drift.
- Alerts via callback for any storage/query failures so monitoring systems can react.

Use `AgenticMemory` as a dependency for `LangGraphCoordinator` to persist plans, share heuristics, and drive longer-term experience accumulation.