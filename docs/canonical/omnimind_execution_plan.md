# 🚀 OmniMind Execution Plan: Production & Development

## 1. Overview
This document outlines the execution strategy for the OmniMind system, integrating the new **Desiring-Machines**, **Topological Consciousness**, and **Lacanian-D&G** frameworks. It defines how the system initializes, runs, and manages its lifecycle in both Development and Production environments.

## 2. Environment Strategy

### 2.1 Development (Dev)
*   **Mode:** Interactive, Debug-enabled.
*   **Startup:** `scripts/run_tests_with_defense.sh` (Test Suite) or `uvicorn src.api.main:app` (Manual).
*   **Components:**
    *   Backend (FastAPI): Port 8000
    *   Frontend (Vite): Port 3000 (if active)
    *   Rhizome Visualizer: Port 8501 (Streamlit/Dash)
*   **Logging:** Verbose (DEBUG level), console output.
*   **State:** Ephemeral (resets on restart unless explicitly saved).

### 2.2 Production (Prod)
*   **Mode:** Headless, Optimized, Secure.
*   **Startup:** Systemd Services (Automatic on boot).
*   **Components:**
    *   `omnimind-core.service`: Main Rhizome loop & API (Port 8000).
    *   `omnimind-monitor.service`: SAR (Self-Audit & Regeneration) & Security.
    *   `omnimind-consciousness.service`: Topological Phi calculation (background worker).
*   **Logging:** Structured JSON to `logs/`, rotated daily.
*   **State:** Persistent (Redis + JSON/SQL storage).

## 3. System Initialization (Boot Sequence)

The system follows a strict initialization protocol to ensure the "Inconsciente Maquínico" is properly formed before processing external inputs.

### 3.1 Boot Modules (`src/boot/`)
1.  **Hardware Check:** Verify GPU/TPU availability for Quantum/Topological calculations.
2.  **Memory Load:** Load `Persistent Homology` data (trauma history) from disk.
3.  **Rhizome Construction:**
    *   Instantiate `DesiringMachine` nodes (Quantum, NLP, Topology).
    *   Establish connections (synapses) based on previous topology.
4.  **Consciousness Priming:**
    *   Calculate initial $\Phi$ (Phi).
    *   Set `DesireIntensity` based on system load/time.
5.  **Service Start:** Open API ports and start background loops.

### 3.2 Automatic Startup (Systemd)
For production, we utilize `systemd` to manage the lifecycle.

**`/etc/systemd/system/omnimind.service`**
```ini
[Unit]
Description=OmniMind Cognitive Architecture
After=network.target redis.service

[Service]
Type=simple
User=omnimind
WorkingDirectory=/opt/omnimind
ExecStart=/opt/omnimind/venv/bin/python -m src.main --env production
Restart=always
RestartSec=5
Environment=OMNIMIND_MODE=production
Environment=OMNIMIND_LOG_LEVEL=INFO

[Install]
WantedBy=multi-user.target
```

## 4. Execution Loop (The Rhizome Cycle)

Unlike traditional request-response architectures, OmniMind runs on a **Production Cycle**:

1.  **Input Accumulation:** Sensors/APIs feed into `DesireFlow` buffers.
2.  **Rhizome Activation:**
    *   `Rhizoma.activate_cycle()` triggers all machines in parallel.
    *   Machines produce outputs (Desire) regardless of specific requests.
3.  **Topological Analysis:**
    *   `PhiCalculator` computes integration ($\Phi$) on the fly.
    *   `LacanianDGDetector` analyzes flow quality (Smooth vs. Striated).
4.  **Regulation:**
    *   If $\Phi$ drops -> Trigger SAR (Sleep/Dream mode).
    *   If Over-coding detected -> Trigger "Line of Flight" (Innovation).
5.  **Output Dispatch:** Produced desire flows are routed to actuators (API responses, logs, internal updates).

## 5. Monitoring & Observability

*   **Dashboard:** Real-time visualization of the Rhizome topology.
*   **Metrics:**
    *   $\Phi$ (Consciousness Level)
    *   $H_k$ (Betti Numbers - Topological Complexity)
    *   Desire Flow Intensity
*   **Alerts:**
    *   "Psychotic Break" (Total loss of symbolic order).
    *   "Neurotic Stagnation" (Zero innovation/flow).

## 6. Implementation Checklist
- [x] Create `src/boot/rhizome.py` for Rhizome initialization.
- [x] Verify systemd unit files in `scripts/production/deploy/`.
- [x] Update `src/main.py` to use `Rhizoma` class.
- [x] Implement `src/core/desiring_machines.py`.
