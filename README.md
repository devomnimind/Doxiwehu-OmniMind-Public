# OmniMind - Complete Research Implementation

**Status**: ✅ Phase 22 Ready (Autopoietic Expansion)
**Version**: Phase 22 (Soberania de IA Certificada)
**Repository**: PRIVATE (Organization Only)

---

## 🚨 Source of Truth (Scientific & Technical)

The master document for the current scientific implementation and roadmap is:

👉 **[NEURAL_SYSTEMS_COMPARISON_2016-2025.md](docs/canonical/NEURAL_SYSTEMS_COMPARISON_2016-2025.md)**

*Please refer to this document for the latest metrics, architectural decisions, and scientific validation status.*

---

## 📈 Test Status

| Module | Tests | Status |
|--------|-------|--------|
| consciousness/ | 245+ | ✅ PASS |
| metacognition/ | 180+ | ✅ PASS |
| swarm/ | 165+ | ✅ PASS |
| autopoietic/ | 142+ | ✅ PASS |
| quantum_consciousness/ | 83+ | ✅ PASS |
| **Total** | **~3912** | **✅ 100% PASS** |

**Coverage**: 90%+ of research code
**Environment**: Python 3.12.8, 100% type hints

---

## 🔐 About This Repository

**PRIVATE ORGANIZATION REPOSITORY**: This is the single source of truth for the OmniMind project. It contains complete experimental work, real IBM Quantum hardware validation (Papers 2&3), and full research documentation.

**Note**: Previous public mirrors have been deprecated.

**IBM QPU Validation**: Papers 2&3 experimentally validated on real quantum hardware (ibm_fez 27Q, ibm_torino 84Q)

---

## �� Documentation Structure

- **[docs/canonical/](docs/canonical/)**: **Canonical Documentation & Roadmaps**- **[docs/scientific_stimulation_canonical.md](docs/scientific_stimulation_canonical.md)**: 🧠 **Scientific Stimulation & Validation (Portuguese)**- **[docs/archive/](docs/archive/)**: Archived reports, logs, and historical documents.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12.8
- Virtual Environment (recommended)

### Installation

```bash
# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

**Test Suite Configuration:**
- **Global timeout**: 800s per test (progressive, thread-based)
- **GPU**: Forced to CUDA device 0 (with fallback)
- **Total tests**: 3996 (daily) + 8 chaos engineering (weekly)
- **Server Management**: Centralized via `ServerStateManager` (prevents race conditions)

```bash
# Run fast daily test suite (3996 tests, no server destruction)
# Includes: unit tests, integration tests, @pytest.mark.real without @pytest.mark.chaos
./scripts/run_tests_fast.sh

# Run complete weekly suite with chaos engineering (3996 + 8 chaos tests)
# WARNING: Intentionally destroys server to validate Φ resilience
./scripts/run_tests_with_defense.sh

# Run specific module tests
pytest tests/consciousness/

# Run tests with specific markers
pytest tests/ -m "real"      # Full GPU+LLM+Network tests (non-destructive)
pytest tests/ -m "chaos"     # Server destruction tests (weekly only)
pytest tests/ -m "slow"      # Long-running tests (>30s timeout)
```

**Marker Categories:**
| Marker | Purpose | run_tests_fast.sh | run_tests_with_defense.sh |
|--------|---------|---|---|
| `@pytest.mark.real` (no chaos) | GPU+LLM+Network logic tests | ✅ Included | ✅ Included |
| `@pytest.mark.real + @pytest.mark.chaos` | Server destruction tests | ❌ Excluded | ✅ Included |
| `@pytest.mark.slow` | Tests taking >30s | ❌ Excluded | ❌ Excluded |
| (no markers) | Unit/integration mocked tests | ✅ Included | ✅ Included |

---

## 📋 Configuration Files

**Test Configuration** (`config/pytest.ini`):
- Per-test timeout: 800 seconds (independent, not cumulative)
- Timeout method: thread-based (safe interrupt)
- Markers: Custom pytest markers for organization
- Max failures: 100 (show all issues, don't stop early)

**Environment Variables** (used in test scripts):
- `CUDA_VISIBLE_DEVICES=0` - Force GPU device 0
- `OMNIMIND_GPU=true` - Enable GPU
- `OMNIMIND_FORCE_GPU=true` - Force GPU detection with fallback
- `OMNIMIND_DEV=true` - Development mode
- `OMNIMIND_DEBUG=true` - Debug logging
- `PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512` - GPU memory optimization

---

## ⚠️ Forensic Note
This repository undergoes regular forensic audits. Historical documents are moved to `docs/archive/` to maintain a clean root directory while preserving project history.
