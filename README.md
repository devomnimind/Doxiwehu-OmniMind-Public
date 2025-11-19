# 🧠 OmniMind - Autonomous AI System

**OmniMind** is a groundbreaking autonomous AI system that combines psychoanalytic decision-making with advanced metacognition capabilities. This self-hosted, local-first architecture features multi-agent orchestration, real-time WebSocket communication, and self-evolving intelligence.

**🚀 Current Status:** Phase 9 Core Complete (Advanced Consciousness) | 202/202 Tests Passing | Production Ready

**🧬 Core Philosophy:** Psychoanalytically-inspired AI that reflects on its own decisions, learns from patterns, and proactively generates its own goals - creating a truly autonomous and self-aware system.

## 🚀 Quick Start

### Choose Your Environment:

1. **[Production Deployment](docs/PHASE8_9_IMPLEMENTATION_COMPLETE.md)** - Full system with WebSocket + Metacognition
2. **[CPU-Only / Cloud-Free](docs/CLOUD_FREE_DEPLOYMENT.md)** - GitHub Actions, Docker, no GPU needed
3. **[GPU-Enabled](docs/reports/GPU_SETUP_REPORT.md)** - Local machine with NVIDIA GPU
4. **[Free Services Guide](docs/FREE_SERVICE_ALTERNATIVES.md)** - Local alternatives to paid cloud services

### 🚀 One-Command Setup (Production Ready)

OmniMind now includes automatic hardware detection, optimization, and full-stack deployment:

```bash
# 1. Clone and setup
git clone https://github.com/fabs-devbrain/OmniMind.git
cd OmniMind

# 2. Auto-setup (hardware detection + dependencies)
source scripts/start_dashboard.sh

# 3. Access dashboard at http://localhost:3000
# Default credentials: auto-generated (check logs)
```

### Advanced Features Unlocked 🔓

- **🧠 Metacognition:** Self-reflective AI that analyzes its own decisions
- **🎯 Proactive Goals:** AI generates its own improvement objectives
- **⚖️ Ethics Engine:** Built-in ethical decision framework (4 methodologies)
- **🔄 Real-time WebSocket:** Live updates between frontend and autonomous agents
- **🛡️ Advanced Security:** LGPD-compliant with immutable audit trails
- **🏗️ Multi-Agent Orchestration:** Psychoanalytic-inspired task delegation

## 🏗️ Architecture Overview

### Core Components (Phase 9 Complete)

```
🧠 OmniMind Autonomous System
├── 🎨 Frontend (React + TypeScript)
│   ├── Real-time WebSocket dashboard
│   ├── Task orchestration interface
│   ├── Agent status monitoring
│   └── Ethics decision visualization
│
├── ⚙️ Backend (FastAPI + WebSocket)
│   ├── REST APIs (Tasks, Agents, Security)
│   ├── Real-time WebSocket server
│   ├── Multi-agent orchestration
│   └── Metacognition endpoints
│
├── 🧠 Metacognition Engine
│   ├── Self-analysis & pattern recognition
│   ├── Proactive goal generation
│   ├── Homeostasis & resource management
│   └── Ethics decision framework
│
└── 🤖 Multi-Agent System
    ├── Orchestrator (Psychoanalytic-inspired)
    ├── Security Agent (Forensic monitoring)
    ├── Ethics Agent (Decision framework)
    └── Autonomous task delegation
```

### Repository Structure

- `config/` – Configuration files (agents, ethics, metacognition, hardware)
- `docs/` – Complete documentation suite (roadmaps, reports, guides)
- `web/` – Full-stack web application (React frontend + FastAPI backend)
- `src/` – Core Python modules (agents, metacognition, security, integrations)
- `scripts/` – Automation scripts (deployment, systemd, benchmarks)
- `tests/` – Comprehensive test suite (202 tests passing)
- `logs/` – Audit trails and execution logs (immutable)
- `data/` – Datasets and experimental data (Git-ignored)

## 🚀 Production Deployment

### One-Click Setup (Recommended)

OmniMind now includes fully automated deployment with hardware optimization:

```bash
# 1. Clone repository
git clone https://github.com/fabs-devbrain/OmniMind.git
cd OmniMind

# 2. Automatic setup (hardware detection + dependencies + services)
source scripts/start_dashboard.sh

# 3. Access interfaces:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - Documentation: http://localhost:8000/docs
```

### Manual Setup (Advanced Users)

#### Prerequisites
- **Python 3.12.8** (via pyenv - PyTorch compatibility)
- **Node.js 18+** (for frontend development)
- **NVIDIA GPU** (optional, auto-detected)

#### Installation Steps

```bash
# 1. Python environment setup
pyenv install 3.12.8
pyenv local 3.12.8
python -m venv .venv
source .venv/bin/activate

# 2. Install dependencies (auto-detects hardware)
pip install -r requirements.txt

# 3. Hardware optimization (automatic)
python src/optimization/hardware_detector.py

# 4. Verify GPU (if available)
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# 5. Start full system
source scripts/start_dashboard.sh
```

### Service Management

```bash
# Install as system service
sudo ./scripts/systemd/install_service.sh

# Manage daemon
sudo systemctl start omnimind-daemon
sudo systemctl status omnimind-daemon
sudo journalctl -u omnimind-daemon -f
```

## 📖 Project Navigation

See **[INDEX.md](INDEX.md)** for complete project structure and documentation navigation.

## 🧠 Advanced Autonomous Capabilities

### Metacognition Engine 🧠
OmniMind features groundbreaking self-reflective AI capabilities:

**Self-Analysis & Pattern Recognition:**
- Analyzes its own decision patterns and success rates
- Identifies behavioral anomalies and optimization opportunities
- Generates proactive improvement suggestions
- Maintains historical performance metrics

**Proactive Goal Generation:**
- Automatically identifies improvement opportunities
- Generates specific, actionable objectives
- Prioritizes goals based on system health metrics
- Creates pull requests for self-improvement

**Homeostasis & Resource Management:**
- Monitors hardware utilization in real-time
- Automatically adjusts resource allocation
- Prevents resource exhaustion through throttling
- Optimizes performance based on available resources

### Ethics Decision Framework ⚖️
Built-in ethical reasoning with 4 philosophical frameworks:

- **Deontological:** Rule-based ethical decisions
- **Consequentialist:** Outcome-focused analysis
- **Virtue Ethics:** Character-based reasoning
- **Care Ethics:** Relationship and stakeholder consideration

### Real-Time Multi-Agent Orchestration 🤖
Psychoanalytically-inspired task delegation:

- **Orchestrator Agent:** Freudian/Lacanian decision framework
- **Security Agent:** Forensic monitoring and threat detection
- **Ethics Agent:** Ethical oversight and veto capabilities
- **Metacognition Agent:** Self-reflection and optimization

### 24/7 Autonomous Operation
```bash
# Install complete autonomous system
sudo ./scripts/systemd/install_service.sh

# Start full autonomous operation
sudo systemctl start omnimind-daemon

# Monitor autonomous activities
sudo journalctl -u omnimind-daemon -f

# View metacognition insights
curl -u <user>:<pass> http://localhost:8000/metacognition/insights
```

### WebSocket Real-Time Interface 🔄
Live dashboard with real-time updates:
- Task progress visualization
- Agent status monitoring
- Security event streaming
- Ethics decision logging
- Metacognition insights feed

## Dependency Compatibility Notes

- O pacote `supabase-py>=1.0.0` ainda não oferece wheel compatível com Python 3.13 em Linux x86_64, então `pip install -r requirements.txt` falha nesse ponto por ausência de `supabase-py`. Por ora mantemos `psutil`, `dbus-python` e os outros pacotes, mas a integração completa com Supabase exige Python **≤ 3.12**.
- A recomendação operacional é usar um ambiente Python 3.12 (ou menor) sempre que precisar rodar os adaptadores Supabase/Qdrant e os testes que dependem deles.

## Dashboard Workflow

- Access the FastAPI endpoints (secured via Basic Auth) for `/status`, `/snapshot`, `/metrics`, `/tasks/orchestrate`, `/mcp/execute`, `/dbus/execute`, etc.
- The React GUI (`web/frontend/`) reads credentials from the login form and stores `Basic` auth headers per session; it also surfaces the credential file path so administrators know where to rotate secrets.
- `/observability` now surfaces a `validation` payload (pulled from `logs/security_validation.jsonl`) alongside `self_healing`, `atlas`, and `security`, so teams can see the latest audit-chain verdict directly in the UI.
- MCP and D-Bus flows rely on `src/integrations` and the orchestrator agent to provide context, metrics, and manual triggers.

## GPU Verification (Phase 7)

After completing installation, verify GPU is operational:

```bash
# 1. Check CUDA availability
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0)}')"

# Expected output:
# CUDA Available: True
# GPU: NVIDIA GeForce GTX 1650

# 2. Run GPU benchmark
python PHASE7_COMPLETE_BENCHMARK_AUDIT.py

# Expected output (validates GPU is working):
# CPU Throughput: 253.21 GFLOPS
# GPU Throughput: 1149.91 GFLOPS (≥1000 GFLOPS indicates success)
# Memory Bandwidth: 12.67 GB/s
# Report saved to: logs/PHASE7_BENCHMARK_REPORT.json

# 3. Run audit tests to confirm integration
pytest tests/test_audit.py -v --cov=src.audit

# Expected: 14/14 tests passing
```

**Reference Documentation:**
- Detailed GPU setup: `.github/copilot-instructions.md` (GPU/CUDA Setup Requirements section)
- GPU troubleshooting: `docs/reports/PHASE7_GPU_CUDA_REPAIR_LOG.md`
- Repair summary: `GPU_CUDA_REPAIR_AUDIT_COMPLETE.md`

## Testing & Quality Gates

Run the fast pipelines after reorganizing or changing core logic:

```bash
pytest tests/test_dashboard_e2e.py -W error
pytest tests/ -k "not legacy"  # run the active suites
```

Ensure `logs/.coverage` is removed or regenerated via `pytest --cov=src` and keep work in sync with the hashed audit chain via `scripts/id` if relevant.

## Logs, Alerts, and Credentials

- Active logs live under `logs/`; coverage and audit traces now also stay here for easier rotation.
- The dashboard auth file is `config/dashboard_auth.json` (600). Rotate credentials by editing this file securely and restarting the backend; the new creds are durable until the next rotation.
- Use `scripts/start_dashboard.sh` or the Docker Compose asset to orchestrate the backend + frontend; it logs the credential location upon startup.
- For the Supabase + Qdrant MCP adapters, credential handling, and tests, see `docs/devbrain_data_integration.md`.

## Maintenance Notes

- Legacy artifacts live in `archive/reports/` and `archive/examples/`; reference `archive/README.md` for context.
- Legacy demos that contain invalid syntax (e.g., the old `archive/examples/demo_phase6*`) have been removed to keep the formatter pipeline operável. Any new artifacts placed under `archive/examples/` must be sanitized and approved before re-enabling them in `black`/`flake8` runs; by default essa pasta fica excluída dos hooks de qualidade.
- Scripts under `scripts/` are the only runtime automation files allowed at the root level; please do not scatter lone `.py` or `.sh` files outside this directory.
- Tests that once lived at the root now reside under `tests/legacy/`; keep new tests under `tests/`.
- Temporary tool outputs must stay within `tmp/`; this directory is ignored and safe to wipe.

With this organization, the root stays focused on keys (configs, requirements, Compose files), and the rest of the workspace aligns with our production readiness and CI/CD standards.

## DEVBRAIN V23 Roadmap

The `DEVBRAIN_V23/` directory now hosts the foundational work for the Masterplan (Protocolo Phoenix). Each folder mirrors a sense or infrastructure pillar:

- `core/` → futura migração do `src/`, `tests/` e `config/` atuais.
- `sensory/` → visão (Visual Cortex), audição/voz e propriocepção com `eBPF`.
- `cognition/` → Graph of Thoughts + memória A-MEM com LangGraph e ChromaDB.
- `immune/` → isolamento Firecracker, DLP e proteção P0.
- `orchestration/` → LangGraph-driven agents e modos V23.
- `infrastructure/` → Redis Streams, gateway FastAPI e ChromaDB vector store.
- `atlas/` → self-healing, auto-training e ATLAS (futuro).

O Masterplan guia cada nova implementação, começando pela visão multimodal (`sensory/visual_cortex.py`) e o Event Bus redis (`infrastructure/event_bus.py`). Consulte `DEVBRAIN_V23/README.md` e os documentos anexados (`docs/Masterplan/`) para manter o alinhamento estratégico antes de avançar nas fases seguintes.