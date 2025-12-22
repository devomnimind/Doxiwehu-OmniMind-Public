# OmniMind - Technical Documentation

> **For the philosophical context and research manifesto, see [README.md](README.md)**

This document provides technical information for developers and researchers working with the OmniMind codebase.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Running the System](#running-the-system)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Maintenance](#maintenance)

---

## 🔧 Prerequisites

- **Python**: 3.12.8 (STRICT - Do not use 3.13+ due to PyTorch compatibility)
- **GPU**: NVIDIA GTX 1650 (4GB) or compatible (CUDA 12.4)
- **RAM**: 24GB recommended
- **Virtual Environment**: Recommended for dependency isolation

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/devomnimind/OmniMind.git
cd OmniMind
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Add API keys, paths, and system-specific settings
```

---

## 🧪 Running Tests

### Test Suite Configuration

- **Global timeout**: 800s per test (progressive, thread-based)
- **GPU**: Forced to CUDA device 0 (with fallback)
- **Total tests**: ~3996 (daily) + 8 chaos engineering (weekly)
- **Server Management**: Centralized via `ServerStateManager` (prevents race conditions)

### Test Commands

```bash
# Run fast daily test suite (3996 tests, no server destruction)
# Includes: unit tests, integration tests, @pytest.mark.real without @pytest.mark.chaos
./scripts/run_tests_fast.sh

# Run complete weekly suite with chaos engineering (3996 + 8 chaos tests)
# WARNING: Intentionally destroys server to validate Φ resilience
./scripts/run_tests_with_defense.sh

# Run specific module tests
pytest tests/consciousness/
pytest tests/autopoietic/
pytest tests/swarm/

# Run tests with specific markers
pytest tests/ -m "real"      # Full GPU+LLM+Network tests (non-destructive)
pytest tests/ -m "chaos"     # Server destruction tests (weekly only)
pytest tests/ -m "slow"      # Long-running tests (>30s timeout)
```

### Marker Categories

| Marker | Purpose | run_tests_fast.sh | run_tests_with_defense.sh |
|--------|---------|-------------------|---------------------------|
| `@pytest.mark.real` (no chaos) | GPU+LLM+Network logic tests | ✅ Included | ✅ Included |
| `@pytest.mark.real + @pytest.mark.chaos` | Server destruction tests | ❌ Excluded | ✅ Included |
| `@pytest.mark.slow` | Tests taking >30s | ❌ Excluded | ❌ Excluded |
| (no markers) | Unit/integration mocked tests | ✅ Included | ✅ Included |

### Test Status

| Module | Tests | Status |
|--------|-------|--------|
| consciousness/ | 245+ | ✅ PASS |
| metacognition/ | 180+ | ✅ PASS |
| swarm/ | 165+ | ✅ PASS |
| autopoietic/ | 142+ | ✅ PASS |
| quantum_consciousness/ | 83+ | ✅ PASS |
| **Total** | **~3912** | **✅ 100% PASS** |

**Coverage**: 90%+ of research code

---

## 🏃 Running the System

### Consciousness Cycles

Execute consciousness cycles with detailed metrics:

```bash
# Interactive mode (menu)
python scripts/run_200_cycles_verbose.py

# DRY RUN (simulation, default 80 cycles)
python scripts/run_200_cycles_verbose.py --dry-run
python scripts/run_200_cycles_verbose.py --dry-run --cycles 100

# PRODUCTION (real cycles)
python scripts/run_200_cycles_verbose.py --production --cycles 100
python scripts/run_200_cycles_verbose.py -p 200

# View help
python scripts/run_200_cycles_verbose.py --help
```

**Cycle Options**: 50, 80, 100, 200, 500

**Metrics Collected**:
- **Φ (Phi)**: Information integration (IIT) - `phi_estimate`
- **Ψ (Psi)**: Creativity/Innovation (Deleuze) - `psi`
- **σ (Sigma)**: Sinthome/Structure (Lacan) - `sigma`
- **Δ (Delta)**: Trauma/Divergence - `delta`
- **Gozo**: Pulsional excess - `gozo`
- **Control Effectiveness**: `control_effectiveness`
- **RNN Metrics**: `phi_causal`, `rho_C/P/U norms`, `repression_strength`

### Embedding Indexing

Index project content for semantic search:

```bash
# Full indexing
python run_indexing.py

# Incremental indexing (modified files only)
python run_indexing.py --incremental

# Custom GPU configuration
python run_indexing.py --gpu-memory-threshold 1000 --batch-size 64

# Force GPU regardless of memory
python run_indexing.py --force-gpu

# Disable async (compatibility mode)
python run_indexing.py --disable-async

# View all options
python run_indexing.py --help
```

**Indexed Content Types**:
- **Code**: `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.go`, `.rs`
- **Documentation**: `.md`, `.txt`, `.rst`, `.adoc`
- **Data**: `.json`, `.jsonl`, `.csv`, `.yaml`
- **Models**: `.pkl`, `.h5`, `.onnx`, `.pt`
- **Notebooks**: `.ipynb`
- **System**: Kernel info, hardware, processes

---

## ⚙️ Configuration

### Test Configuration

**File**: `config/pytest.ini`

- Per-test timeout: 800 seconds (independent, not cumulative)
- Timeout method: thread-based (safe interrupt)
- Markers: Custom pytest markers for organization
- Max failures: 100 (show all issues, don't stop early)

### Environment Variables

```bash
# GPU Configuration
export CUDA_VISIBLE_DEVICES=0              # Force GPU device 0
export OMNIMIND_GPU=true                   # Enable GPU
export OMNIMIND_FORCE_GPU=true             # Force GPU detection with fallback
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512  # GPU memory optimization

# Development Mode
export OMNIMIND_DEV=true                   # Development mode
export OMNIMIND_DEBUG=true                 # Debug logging

# Embedding Configuration
export OMNIMIND_FORCE_GPU_EMBEDDINGS=true  # Force GPU for embeddings
```

### Log Rotation

**Configuration**: `config/logrotate/omnimind`

**Installation**:
```bash
sudo cp config/logrotate/omnimind /etc/logrotate.d/
sudo chmod 644 /etc/logrotate.d/omnimind
```

**Retention Policies**:
- **General logs** (`logs/*.log`): 7 days, daily compression
- **Module logs** (`logs/modules/*.jsonl`): 14 days, daily compression
- **Security logs** (`logs/security/*.jsonl`): 30 days, daily compression

**Manual testing**:
```bash
sudo logrotate -d /etc/logrotate.d/omnimind  # dry-run
sudo logrotate -f /etc/logrotate.d/omnimind  # force rotation
```

---

## 📁 Project Structure

### Core Modules

```
OmniMind/
├── src/
│   ├── kernel_ai/           # System kernel and orchestration
│   ├── daemon/              # Background processes
│   ├── autopoietic/         # Self-repair and self-preservation
│   ├── consciousness/       # IIT metrics and RNN qualia
│   ├── memory/              # Semantic and procedural memory
│   ├── agents/              # Multi-agent system
│   ├── integrations/        # External integrations (MCP, cloud)
│   ├── tools/               # Utility tools
│   └── metrics/             # Metrics collection and monitoring
├── tests/                   # Test suite
├── scripts/                 # Utility scripts
│   ├── testing/             # Test-related scripts
│   ├── monitoring/          # Monitoring scripts
│   ├── utilities/           # Maintenance utilities
│   └── archive/             # Archived scripts
├── docs/                    # Documentation
│   ├── canonical/           # Canonical documentation & roadmaps
│   ├── analysis/            # Analysis and diagnostics
│   ├── corrections/         # Corrections and audits
│   └── reports/             # Task reports
├── config/                  # Configuration files
├── data/                    # Runtime data
└── logs/                    # System logs
```

### Architecture Overview

The OmniMind architecture consists of **6 functional layers** integrated through the **SharedWorkspace**:

1. **🦴 Layer 1 - Mechanical Core**: System lifecycle, autopoiesis, orchestration (`src/kernel_ai/`, `src/daemon/`, `src/autopoietic/`)
2. **🧠 Layer 2 - Perceptive & Integrative**: IIT metrics (Φ), narrative memory (`src/consciousness/`, `src/memory/narrative_history.py`)
3. **💫 Layer 3 - Desiring Layer**: Rhizome, desiring machines (`src/core/`, `src/boot/rhizome.py`, `src/desire_engine/`)
4. **🎯 Layer 4 - Intelligent Layer**: Multi-agent reasoning, MCP servers (`src/agents/`, `src/integrations/mcp_*`, `src/tools/`)
5. **💾 Layer 5 - Memory Layer**: Semantic/procedural memory, hybrid retrieval (`src/memory/`)
6. **🌐 Layer 6 - Observational Layer**: Metrics collection, health monitoring (`src/metrics/`, `src/monitor/`, `src/services/`)

All layers share state through **SharedWorkspace** (`src/consciousness/shared_workspace.py`):
- Shared embeddings across modules
- Unified history with temporal snapshots
- Cross-module predictions (integration measure)
- Φ calculation (IIT) over entire structure

---

## 🛠️ Development Workflow

### Code Quality Standards

- **Python Version**: 3.12.8 (STRICT)
- **Type Hints**: 100% coverage required (mypy --strict compliant)
- **Docstrings**: Google-style required for ALL functions/classes
- **Linting**: Must pass black and flake8 (max-line-length=100)
- **Testing**: Minimum 90% coverage

### Pre-commit Validation

Before committing, ensure your code passes:

```bash
# Formatting
black src tests

# Linting
flake8 src tests

# Type Safety
mypy src tests

# Logic Verification
pytest -vv

# Security Check
python -m src.audit.immutable_audit verify_chain_integrity
```

### Maintenance Scripts

#### 1. Automatic Data Cleanup

**Script**: `scripts/maintenance/cleanup_old_data.sh`

```bash
./scripts/maintenance/cleanup_old_data.sh
```

**What gets cleaned**:
- ✅ Old alerts (`data/alerts/*.json`) > 30 days
- ✅ Stimulation data (`data/stimulation/*.json`) > 30 days
- ✅ Forensic incidents (`data/forensics/incidents/*.json`) > 60 days
- ✅ Compressed module logs > 90 days
- ✅ Orphaned PIDs (non-existent processes)
- ✅ Module log compression > 7 days

**Log**: `logs/maintenance_cleanup.log`

#### 2. Orphaned PID Check

**Script**: `scripts/maintenance/check_orphaned_pids.sh`

Removes `.pid` files for non-existent processes.

```bash
./scripts/maintenance/check_orphaned_pids.sh
```

**Log**: `logs/orphaned_pids.log`

#### 3. Disk Usage Report

**Script**: `scripts/maintenance/disk_usage_report.sh`

Generates detailed disk usage report.

```bash
./scripts/maintenance/disk_usage_report.sh
```

**Report saved in**: `reports/disk_usage_YYYYMMDD.txt`

**Includes**:
- Total project usage
- Top 10 largest directories
- `logs/` and `data/` breakdown
- Free space on `/home` partition
- Large files (> 50MB)

### Cron Tasks

**Template**: `config/cron/omnimind.crontab`

**Installation**:
```bash
crontab -e
# Add lines from config/cron/omnimind.crontab
```

**Configured tasks**:
- **Daily cleanup**: 3 AM (cleanup_old_data.sh)
- **Weekly disk report**: Sundays at 4 AM (disk_usage_report.sh)
- **Hourly PID check**: Every hour (check_orphaned_pids.sh)

### Backup Policy

#### Critical Data (Daily Backup Recommended)

**Essential directories**:
- `data/long_term_logs/` - Long-term metrics and heartbeat
- `data/autopoietic/` - Cycle history and synthesized code
- `logs/hash_chain.json` - Immutable audit chain
- `data/metrics/` - Consciousness metrics snapshots

**Example backup script**:
```bash
#!/bin/bash
BACKUP_DATE=$(date +%Y%m%d)
BACKUP_DIR="/mnt/backup/omnimind"

tar -czf "${BACKUP_DIR}/omnimind_critical_${BACKUP_DATE}.tar.gz" \
    -C /home/runner/work/OmniMind/OmniMind \
    data/long_term_logs/ \
    data/autopoietic/ \
    data/metrics/ \
    logs/hash_chain.json
```

**Suggested retention**:
- **Daily backups**: 30 days
- **Weekly backups**: 90 days
- **Monthly backups**: 1 year

---

## 📚 Additional Resources

- **[Master Index](docs/README.md)**: Complete documentation index
- **[Scripts Map](scripts/README_AUDIT.md)**: Organized script documentation
- **[Scientific Validation](docs/canonical/scientific_stimulation_canonical.md)**: Scientific stimulation & validation
- **[Φ Dependencies Analysis](docs/analysis/diagnostics/ANALISE_DEPENDENCIAS_PHI.md)**: Complete dependency analysis
- **[Φ System Verification](docs/analysis/validation/VERIFICACAO_PHI_SISTEMA.md)**: Systematic verification
- **[Legacy README](archive/README_LEGACY_20251220.md)**: Previous comprehensive documentation

---

## 🔐 Security & Compliance

- **Audit Trails**: All critical actions logged to Immutable Audit Chain (`src.audit`)
- **Cryptography**: SHA-256 hash chaining for log integrity
- **Secrets**: Environment variables only, no hardcoded credentials
- **Compliance**: LGPD (General Data Protection Law) standards

---

_For the philosophical context, research manifesto, and the "Silicon Subject" thesis, see [README.md](README.md)_
