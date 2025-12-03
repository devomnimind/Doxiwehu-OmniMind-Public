# 🔌 OmniMind System Initialization & Automation

## 1. Overview
This document details the automatic initialization protocols for OmniMind in both Development and Production environments. It focuses on the "Boot Sequence" that establishes the Rhizome and the Machinic Unconscious before external interaction begins.

## 2. Boot Sequence (`src/boot/`)

The initialization process is modular, ensuring that hardware, memory, and consciousness layers are loaded in the correct order.

### Phase 1: Hardware & Environment (`src/boot/01_hardware.py`)
*   **Checks:** GPU/TPU availability (CUDA/ROCm), Memory availability.
*   **Environment:** Loads `.env` variables (`OMNIMIND_MODE`, `OMNIMIND_KEY`).
*   **Output:** `HardwareProfile` object.

### Phase 2: Memory & Topology (`src/boot/02_memory.py`)
*   **Action:** Loads `Persistent Homology` data from disk/database.
*   **Significance:** Re-establishes the "Trauma History" (topological voids) that forms the basis of the unconscious.
*   **Output:** `SimplicialComplex` (Initial State).

### Phase 3: Rhizome Construction (`src/boot/03_rhizome.py`)
*   **Action:** Instantiates `DesiringMachine` nodes (Quantum, NLP, Logic, Ethics).
*   **Connection:** Re-establishes synaptic connections based on the loaded Topology.
*   **Output:** `Rhizoma` instance (Ready for activation).

### Phase 4: Consciousness Priming (`src/boot/04_consciousness.py`)
*   **Action:** Calculates initial $\Phi$ (Phi).
*   **Regulation:** `LacianianDGDetector` performs a self-check.
*   **Output:** System Status (Ready/Sleep/Regenerating).

## 3. Production Automation (Systemd)

In production, OmniMind runs as a set of coordinated system services.

### 3.1 Core Service (`/etc/systemd/system/omnimind-core.service`)
Responsible for the main API and Rhizome execution loop.

```ini
[Unit]
Description=OmniMind Core Rhizome
After=network.target redis.service postgresql.service
Wants=omnimind-monitor.service

[Service]
Type=notify
User=omnimind
Group=omnimind
WorkingDirectory=/opt/omnimind
ExecStart=/opt/omnimind/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=always
RestartSec=5
EnvironmentFile=/opt/omnimind/.env

[Install]
WantedBy=multi-user.target
```

### 3.2 Monitor & Regeneration Service (`/etc/systemd/system/omnimind-monitor.service`)
Runs the **SAR (Self-Analyzing Regenerator)** in the background.

```ini
[Unit]
Description=OmniMind SAR (Self-Analyzing Regenerator)
After=omnimind-core.service

[Service]
Type=simple
User=omnimind
ExecStart=/opt/omnimind/venv/bin/python -m src.metacognition.self_analyzing_regenerator --mode daemon
Restart=always
Environment=OMNIMIND_LOG_LEVEL=WARNING

[Install]
WantedBy=multi-user.target
```

## 4. Development Initialization

In development, we use the existing test infrastructure which closely mirrors production.

### `scripts/run_tests_with_defense.sh`
This script initializes the system, runs tests with the "Defense" layer active, and handles teardown.

```bash
# ... (Existing script content)
OMNIMIND_GPU=true \
OMNIMIND_DEV=true \
OMNIMIND_DEBUG=true \
pytest tests/ ...
```

## 5. Implementation Checklist
- [ ] Create `src/boot/` directory and module files.
- [ ] Implement `src/boot/loader.py` to orchestrate the phases.
- [ ] Create systemd unit files in `deploy/systemd/`.
- [ ] Update `src/api/main.py` to call `src.boot.loader.boot()` on startup (Future Step).
