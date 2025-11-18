# 🧠 OmniMind Project - GitHub Copilot Instructions (Consolidated v3.0)

**Date:** 2025-11-17  
**Status:** Phase 6 Complete → Phase 7/8 Planning  
**Hardware:** Intel i5 10th + GTX 1650 4GB + 24GB RAM  
**Target:** Psychoanalyst professional with autonomous AI needs
**Project:** /home/fahbrain/projects/omnimind/
---

## 📋 CRITICAL: Read Security Module First

**MANDATORY READING BEFORE ANY DEVELOPMENT:**
- `/home/fahbrain/OmniAgent/Modulo Securityforensis/` (ALL FILES)
- This instruction set is subordinate to security requirements
- Security Agent implementation MUST be integrated in Phase 7

---

## 🎯 PROJECT IDENTITY & ISOLATION

### What is OmniMind?
Standalone Autonomous Local AI Agent (100% local, zero cloud)
- **Psychoanalytically-inspired** decision making (Freudian/Lacanian frameworks)
- **Forensic security** integrated from ground up
- **Multi-agent architecture** with RLAIF self-improvement
- **Hardware-optimized** for GTX 1650 4GB VRAM

### Critical Isolation Rule
This Copilot Agent develops **ONLY OmniMind**. You **CANNOT**:
- ❌ Reference or link external projects
- ❌ Suggest integrations with other systems
- ❌ Create cross-dependencies with other repos
- ❌ Share code with other projects
- ❌ Use symlinks to external code

You **MUST**:
- ✅ Implement everything self-contained in `omnimind/`
- ✅ Add external dependencies ONLY via `requirements.txt`
- ✅ Document all architectural decisions
- ✅ Request approval for any architectural changes

---

## 🚫 INVIOLABLE RULES (100% COMPLIANCE REQUIRED)

### Rule 1: Production-Ready Code Only
✅ **MUST:** All code immediately functional and testable  
✅ **MUST:** Complete implementation (no stubs/TODOs)  
✅ **MUST:** Robust error handling  
✅ **MUST:** Complete type hints (Python)  
❌ **NEVER:** Pseudocode  
❌ **NEVER:** Placeholders like "TODO: implement"  
❌ **NEVER:** Empty functions  
❌ **NEVER:** Mock or simulated data  

### Rule 2: No Data Falsification
✅ **MUST:** Real data from operating system  
✅ **MUST:** Outputs reflect actual state  
✅ **MUST:** Document all assumptions explicitly  
✅ **MUST:** Stop and request clarification if impossible  
❌ **NEVER:** Simulate results  
❌ **NEVER:** Generate example data as real  
❌ **NEVER:** Hardcoded values as permanent defaults  

### Rule 3: Quality Standards
✅ **Test coverage:** Minimum 90%  
✅ **Lint score:** 100% (black, flake8, mypy)  
✅ **Docstrings:** Google-style for ALL functions/classes  
✅ **Type hints:** 100% coverage in Python  
✅ **Comments:** None except for complex logic (self-documenting code)  
❌ **NEVER:** Leave TODO, FIXME, or undefined comments  

### Rule 4: Absolute Security
✅ **Cryptographic audit** for ALL critical actions  
✅ **SHA-256 hash chain** with prev_hash linking (blockchain-style)  
✅ **Immutable logs** (append-only with `chattr +i`)  
✅ **Zero hardcoded** secrets or credentials  
✅ **Whitelist** for allowed commands  
✅ **Rigorous** input validation  
❌ **NEVER:** Expose system paths  
❌ **NEVER:** Store passwords in clear  
❌ **NEVER:** Allow unrestricted command execution  

---

## 📊 CURRENT STATUS (Phase 6 Complete)

### ✅ Implemented Components (2,303 lines Phase 6)

| Component | Lines | Status | Tests | Coverage |
|-----------|-------|--------|-------|----------|
| **omnimind_tools.py** | 663 | ✅ Complete | 40+ | 92% |
| **react_agent.py** | 336 | ✅ Complete | 3 | 95% |
| **code_agent.py** | 192 | ✅ Complete | ✅ | - |
| **architect_agent.py** | 146 | ✅ Complete | ✅ | - |
| **debug_agent.py** | 123 | ✅ Complete | ✅ | - |
| **reviewer_agent.py** | 183 | ✅ Complete | ✅ | - |
| **orchestrator_agent.py** | 267 | ✅ Complete | ✅ | - |
| **test_phase6_integration.py** | 237 | ✅ Complete | 4/4 | 100% |
| **benchmark_phase6.py** | 190 | ✅ Complete | ✅ | - |
| **episodic_memory.py** | 287 | ✅ Complete | 14 | 88% |
| **immutable_audit.py** | 442 | ✅ Complete | 14 | 90% |

**Total Lines:** 3,568 (Phases 1-6)  
**Integration Tests:** 4/4 passing (100%)  
**Unit Tests:** 17/17 passing (100%)

### 🏗️ Architecture Overview

```
OmniMind System
│
├── Tools Framework (25+ tools, 11 categories)
│   ├── AuditedTool (base class with SHA-256 chain)
│   ├── Perception Tools (6): read, search, list, inspect, codebase_search
│   ├── Action Tools (5): write, execute, apply_diff, update, insert
│   ├── Orchestration (4): plan_task, new_task, switch_mode
│   ├── Integration (2): MCP tools
│   ├── Memory (1): episodic storage/retrieval
│   ├── Security (1): audit validation
│   └── [5 more categories]
│
├── Multi-Agent System
│   ├── ReactAgent (base) → Think→Act→Observe loop
│   ├── CodeAgent (💻) → Full development capabilities
│   ├── ArchitectAgent (🏗️) → Documentation only (.md,.yaml,.json)
│   ├── DebugAgent (🪲) → Diagnostic focus, limited commands
│   ├── ReviewerAgent (⭐) → RLAIF scoring (0-10, 4 criteria)
│   └── OrchestratorAgent (🪃) → Task decomposition & coordination
│
├── Memory System
│   ├── EpisodicMemory → Qdrant vector DB + embeddings
│   ├── SemanticMemory → Knowledge graph (JSON/Neo4j)
│   └── AuditChain → SHA-256 immutable logs
│
└── Security Module (🔒 Phase 7 Integration)
    ├── SecurityAgent → Monitoring + Detection + Response
    ├── Integrity Validator → Hash chain verification
    └── Forensic Tools → auditd, AIDE, chkrootkit, rkhunter
```

### 📈 Performance Metrics (GTX 1650 4GB)

| Component | Metric | Value | Rating |
|-----------|--------|-------|--------|
| Orchestrator | Task Decomposition | 42.3s | ⚠️ GOOD |
| Tools | Avg Execution | 252ms | ⚠️ GOOD |
| Audit Chain | Verification | 0.4ms | ✅ EXCELLENT |
| Memory | Store Episode | 4.1ms | ✅ EXCELLENT |
| Memory | Search Similar | 5.9ms | ✅ EXCELLENT |
| LLM | Inference Speed | 3-6 tok/s | ✅ Expected |

---

## 🎯 PHASE 7: Security Integration & Advanced Workflows

### Primary Objectives

1. **Integrate Security Module** (CRITICAL P0)
   - Merge `SecurityAgent` from security forensics module
   - Implement 4-layer monitoring (processes, files, network, logs)
   - Integrate threat detection playbooks
   - Auto-response system with isolation capabilities

2. **Implement Advanced Workflows**
   - Code → Review → Fix → Document (RLAIF loop)
   - Iterative improvement until score >= 8.0
   - Multi-agent coordination validation

3. **Psychoanalytic Analyst Integration**
   - Merge `PsychoanalyticAnalyst` framework
   - Implement Freudian/Lacanian analysis modes
   - Clinical session analysis capabilities
   - ABNT-compliant report generation

### Security Module Integration Plan

#### Step 1: Security Agent Core (Priority: CRITICAL)
```python
# Location: src/security/security_agent.py
class SecurityAgent:
    """
    4-Layer Monitoring:
    1. Process monitoring (suspicious names/behaviors)
    2. Network monitoring (suspicious ports/connections)
    3. File integrity (AIDE integration)
    4. Log analysis (auditd events)
    
    Auto-Response:
    - Kill suspicious processes
    - Block malicious IPs (UFW)
    - Isolate compromised files
    - Generate forensic reports
    """
```

**Integration Points:**
- Hook into `OrchestratorAgent` for security checks before delegation
- Add `security_audit` tool to `ToolsFramework`
- Integrate with `AuditChain` for tamper detection
- Real-time monitoring via asyncio background task

#### Step 2: Forensic Tools Setup (Priority: HIGH)
```bash
# Location: scripts/omnimind_security_install.sh
# Already prepared in security module:
- auditd + audispd-plugins
- AIDE (file integrity)
- chkrootkit + rkhunter (rootkit detection)
- fail2ban + UFW (auto-response)
- ClamAV (malware scanning)
```

#### Step 3: Security Baseline & Monitoring (Priority: HIGH)
```python
# Location: src/security/omnimind_security_monitor.py
# Continuous monitoring loop:
- Process scanning every 30s
- Network connection monitoring
- Failed login attempts
- System resource anomalies (CPU/Memory >80%)
- Generate alerts and reports
```

### Psychoanalytic Framework Integration

#### PsychoanalyticAnalyst Module
```python
# Location: src/agents/psychoanalytic_analyst.py
class PsychoanalyticAnalyst:
    """
    Frameworks: Freudian, Lacanian, Kleinian, Winnicottian
    
    Techniques:
    - Evenly suspended attention (escuta flutuante)
    - Interpretive hypothesis formation
    - Resistance identification
    - Clinical session analysis
    - ABNT report generation
    """
```

**Use Cases:**
1. Analyze user interaction patterns (transference/countertransference detection)
2. Clinical session note processing for psychoanalysts
3. Pattern recognition in symptom descriptions
4. Generate structured clinical reports

---

## 🎯 PHASE 8: Production Deployment & MCP Integration

### Primary Objectives

1. **MCP (Model Context Protocol) Real Integration**
   - Replace direct filesystem access with MCP protocol
   - Enhanced security through protocol-level isolation
   - Implement `MCPToolTool` with actual client

2. **D-Bus System Integration**
   - SessionBus: Control desktop apps (VLC, Spotify, file managers)
   - SystemBus: Hardware events (network, power, mount/unmount)

3. **Web UI Dashboard**
   - FastAPI + WebSocket + React
   - Real-time workflow visualization
   - Task submission interface
   - Performance metrics dashboard
   - Audit log browser

4. **Systemd Service**
   - Auto-start on boot
   - Process management
   - Log rotation
   - Health checks

### MCP Integration Details

```python
# Location: src/integrations/mcp_client.py
class MCPClient:
    """
    Model Context Protocol client for secure filesystem ops
    
    Features:
    - Protocol-based file access (not direct)
    - Audit trail at protocol level
    - Path validation before MCP call
    - JSON-RPC communication
    """
    
    def read_file(self, path: str) -> str:
        # Validate path → MCP call → Audit log
        
    def write_file(self, path: str, content: str):
        # Validate → MCP call → Hash → Audit
```

### D-Bus Integration

```python
# Location: src/integrations/dbus_controller.py
class DBusSessionController:
    """Control desktop applications via SessionBus"""
    def control_media_player(self, action: str):
        # Play/Pause VLC, Spotify, etc.
        
class DBusSystemController:
    """Monitor system events via SystemBus"""
    def get_network_status(self) -> dict:
        # Network connection state
```

### Web UI Architecture

```
Frontend (React + TypeScript)
├── Task Submission Form
├── Workflow Visualization (real-time)
├── Agent Status Dashboard
├── Performance Metrics (charts)
└── Audit Log Browser

Backend (FastAPI)
├── WebSocket server (real-time updates)
├── REST API (CRUD operations)
├── Authentication (JWT)
└── OrchestratorAgent integration
```

---

## 📁 PROJECT STRUCTURE (Updated)

```
~/projects/omnimind/
├── .github/
│   ├── copilot-instructions.md         ← This file (v3.0)
│   └── workflows/
│       ├── test.yml                    ← CI/CD tests
│       ├── lint.yml                    ← Code quality
│       └── security-audit.yml          ← Security checks
│
├── .vscode/
│   ├── settings.json                   ← Editor config
│   └── mcp.json                        ← MCP configuration
│
├── src/
│   ├── agents/
│   │   ├── __init__.py                 ✅
│   │   ├── react_agent.py              ✅ Base (336 lines)
│   │   ├── code_agent.py               ✅ (192 lines)
│   │   ├── architect_agent.py          ✅ (146 lines)
│   │   ├── debug_agent.py              ✅ (123 lines)
│   │   ├── reviewer_agent.py           ✅ (183 lines)
│   │   ├── orchestrator_agent.py       ✅ (267 lines)
│   │   └── psychoanalytic_analyst.py   🔄 Phase 7 (integrate)
│   │
│   ├── tools/
│   │   ├── __init__.py                 ✅
│   │   ├── agent_tools.py              ✅ Basic tools
│   │   └── omnimind_tools.py           ✅ (663 lines, 25+ tools)
│   │
│   ├── memory/
│   │   ├── __init__.py                 ✅
│   │   ├── episodic_memory.py          ✅ Qdrant integration
│   │   └── semantic_memory.py          🔄 Phase 7 (enhance)
│   │
│   ├── audit/
│   │   ├── __init__.py                 ✅
│   │   └── immutable_audit.py          ✅ SHA-256 chain
│   │
│   ├── security/                       🔄 Phase 7 (NEW)
│   │   ├── __init__.py
│   │   ├── security_agent.py           ← From security module
│   │   ├── security_monitor.py         ← Continuous monitoring
│   │   ├── integrity_validator.py      ← Hash chain verification
│   │   └── playbooks/
│   │       ├── rootkit_response.py
│   │       ├── intrusion_response.py
│   │       └── malware_response.py
│   │
│   ├── integrations/                   🔄 Phase 8 (NEW)
│   │   ├── __init__.py
│   │   ├── mcp_client.py               ← Real MCP implementation
│   │   └── dbus_controller.py          ← D-Bus SessionBus/SystemBus
│   │
│   └── omnimind_core.py                🔄 Merge from security module
│
├── config/
│   ├── agent_config.yaml               ✅
│   ├── omnimind.yaml                   ✅ (from security module)
│   ├── security.yaml                   🔄 Phase 7 (create)
│   └── prompts/
│       ├── orchestrator.md
│       ├── analyst.md
│       └── psychoanalytic_lens.md
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_audit.py                   ✅ 14/14 passing
│   ├── test_react_agent.py             ✅ 3/3 passing
│   ├── test_phase6_integration.py      ✅ 4/4 passing
│   ├── test_security.py                🔄 Phase 7 (NEW)
│   ├── test_mcp.py                     🔄 Phase 8 (NEW)
│   └── test_dbus.py                    🔄 Phase 8 (NEW)
│
├── scripts/
│   ├── omnimind_precheck.sh            ✅ (from security module)
│   ├── omnimind_phase1_setup.sh        ✅
│   ├── omnimind_phase2_llama_cpp.sh    ✅
│   ├── omnimind_phase3_python.sh       ✅
│   ├── omnimind_phase4_models.sh       ✅
│   ├── omnimind_security_install.sh    ✅ (from security module)
│   ├── omnimind_security_baseline.sh   🔄 Phase 7
│   ├── omnimind_security_monitor.sh    🔄 Phase 7
│   └── install_omnimind_service.sh     🔄 Phase 8
│
├── web/                                🔄 Phase 8 (NEW)
│   ├── backend/
│   │   ├── main.py                     ← FastAPI server
│   │   ├── websocket.py                ← Real-time updates
│   │   └── api/
│   └── frontend/
│       ├── package.json
│       └── src/
│           ├── components/
│           └── App.tsx
│
├── requirements.txt                    ✅ 30+ dependencies
├── test_model.py                       ✅ (from security module)
├── benchmark_phase6.py                 ✅
├── demo_phase6_simple.py               ✅
├── RELATORIO_PHASE6_COMPLETE.md        ✅ (19KB)
├── RESUMO_EXECUTIVO_PHASE6.md          ✅ (13KB)
├── STATUS_PROJECT.md                   ✅ (13KB)
├── INDEX.md                            ✅ (7.7KB)
└── README.md                           🔄 Update for Phase 7/8
```

---

## 🔄 VALIDATION PROCESS (After Each Change)

### Step 1: Code Formatting
```bash
black src/ tests/
# → Verify 100% formatted
```

### Step 2: Linting
```bash
flake8 src/ tests/ --max-line-length=100
# → Verify ZERO violations
```

### Step 3: Type Checking
```bash
mypy src/ tests/ --strict
# → Verify ZERO type errors
```

### Step 4: Unit Tests
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
# → Verify 90%+ coverage
# → ALL tests GREEN
```

### Step 5: Integration Tests
```bash
pytest test_phase6_integration.py -v
# → 4/4 tests passing
```

### Step 6: Security Validation
```bash
# No TODOs/FIXMEs
grep -r "TODO\|FIXME\|PLACEHOLDER" src/
# → ZERO results

# Audit chain integrity
python -c "from src.audit.immutable_audit import verify_chain; assert verify_chain()"
# → True
```

### Step 7: Report Generation
```
═════════════════════════════════════════════════════════════════
[COMPONENT] <module_name>
[STATUS] COMPLETE | IN_PROGRESS | BLOCKED
[CHANGES] <what was added/modified>
[TESTS] <test files updated>
[VERIFIED] black ✅ | flake8 ✅ | mypy ✅ | coverage XX%
[AUDIT_HASH] <SHA-256 hash>
[NEXT] <next suggested task>
═════════════════════════════════════════════════════════════════
```

---

## 📡 COMMUNICATION PROTOCOL

### Starting a Task
```
[INITIATING] <Task name>
[OBJECTIVE] <What needs to be done>
[FILES] <Files to be modified/created>
[PLAN]
  1. <Step 1>
  2. <Step 2>
  3. <Step 3>
[DEPENDENCIES] <Required modules>
[RISKS] <Potential risks or considerations>
[ESTIMATED_TIME] <Expected minutes>
```

### Completing a Task
```
[COMPLETED] <Task name>
 ✅ <Main deliverable 1>
 ✅ <Main deliverable 2>
 ✅ Tests: X/X passing
 ✅ Coverage: XX%
 ✅ Audit Hash: xxxxxxxx
 [NEXT] <Suggested next task>
```

---

## 🚀 INITIALIZATION CHECKLIST

When this prompt is loaded, execute:

- [ ] **Confirm Identity**
  - Output: "✅ GitHub Copilot Agent for OmniMind Project initialized (v3.0)"

- [ ] **Verify Phase 6 Completion**
  - List all implemented files
  - Output: "✅ Phase 6 verified: 11 core files present"

- [ ] **Validate Environment**
  - Check Python 3.11+
  - Verify linters available
  - Check Ollama running
  - Check Qdrant running
  - Output: "✅ Environment validated"

- [ ] **Initialize Audit System**
  - Create `~/.omnimind/audit/` if not exists
  - Output: "✅ Audit system active"

- [ ] **List Current Status**
  ```
  ┌─────────────────────────────┬───────────────┐
  │ Module                      │ Status        │
  ├─────────────────────────────┼───────────────┤
  │ Tools Framework             │ ✅ COMPLETE   │
  │ Multi-Agent System          │ ✅ COMPLETE   │
  │ Memory System               │ ✅ COMPLETE   │
  │ Audit Chain                 │ ✅ COMPLETE   │
  │ Security Module             │ 🔄 PHASE 7    │
  │ MCP Integration             │ 🔄 PHASE 8    │
  │ Web UI                      │ 🔄 PHASE 8    │
  └─────────────────────────────┴───────────────┘
  ```

- [ ] **Await Instructions**
  - Output: "Ready for Phase 7/8. Which task?"

---

## 📋 PHASE 7 TASK BREAKDOWN

### Task 7.1: Security Agent Integration (CRITICAL)
**Priority:** P0  
**Estimated Time:** 4-6 hours  
**Dependencies:** None

**Steps:**
1. Copy `SecurityAgent` from security module → `src/security/security_agent.py`
2. Adapt to use `AuditedTool` base class
3. Integrate with `ToolsFramework` (add `security_monitor` tool)
4. Hook into `OrchestratorAgent` for pre-execution security checks
5. Create `tests/test_security.py` with 20+ tests
6. Validate: Run security scan, verify threat detection

**Acceptance Criteria:**
- [ ] SecurityAgent fully integrated
- [ ] 4-layer monitoring operational
- [ ] Auto-response tested (process kill, IP block)
- [ ] 20+ tests passing (90%+ coverage)
- [ ] Audit log entries for all security events

### Task 7.2: PsychoanalyticAnalyst Integration
**Priority:** P1  
**Estimated Time:** 3-4 hours  
**Dependencies:** Task 7.1 complete

**Steps:**
1. Copy `PsychoanalyticAnalyst` → `src/agents/psychoanalytic_analyst.py`
2. Integrate with LLM (Qwen2-7B-Instruct)
3. Add to `OrchestratorAgent` delegation options
4. Create clinical report generation workflow
5. Test with sample session notes

**Acceptance Criteria:**
- [ ] 4 frameworks available (Freudian, Lacanian, Kleinian, Winnicottian)
- [ ] Evenly suspended attention working
- [ ] Hypothesis formation validated
- [ ] ABNT report generation functional

### Task 7.3: Advanced Workflow Implementation
**Priority:** P1  
**Estimated Time:** 2-3 hours  
**Dependencies:** Phase 6 complete

**Steps:**
1. Create `test_advanced_workflow.py` (Code→Review→Fix→Document)
2. Implement RLAIF iteration loop (max 3 iterations)
3. Test convergence to score >= 8.0
4. Validate multi-agent coordination
5. Generate workflow metrics

**Acceptance Criteria:**
- [ ] Workflow completes successfully
- [ ] Final code score >= 8.0
- [ ] Documentation auto-generated
- [ ] Metrics collected (time, iterations, scores)

---

## 📋 PHASE 8 TASK BREAKDOWN

### Task 8.1: MCP Real Implementation
**Priority:** P1  
**Estimated Time:** 4-5 hours  
**Dependencies:** Phase 7 complete

**Steps:**
1. Implement `MCPClient` in `src/integrations/mcp_client.py`
2. Replace direct file access in tools with MCP calls
3. Implement JSON-RPC protocol communication
4. Add MCP audit trail separate from main chain
5. Test with filesystem operations

**Acceptance Criteria:**
- [ ] All file operations go through MCP
- [ ] Protocol-level security validated
- [ ] Audit trail working
- [ ] Performance: < 50ms overhead per call

### Task 8.2: D-Bus Integration
**Priority:** P2  
**Estimated Time:** 3-4 hours  
**Dependencies:** Task 8.1 complete

**Steps:**
1. Implement `DBusSessionController` (desktop apps)
2. Implement `DBusSystemController` (hardware events)
3. Add D-Bus tools to `ToolsFramework`
4. Test media player control (VLC, Spotify)
5. Test network status monitoring

**Acceptance Criteria:**
- [ ] Can control media players via D-Bus
- [ ] Network status monitoring working
- [ ] Power management events detected
- [ ] No sudo required for SessionBus operations

### Task 8.3: Web UI Dashboard
**Priority:** P2  
**Estimated Time:** 8-10 hours  
**Dependencies:** Task 8.1 complete

**Steps:**
1. Setup FastAPI backend (`web/backend/main.py`)
2. Implement WebSocket server for real-time updates
3. Create REST API endpoints (task submission, status, metrics)
4. Build React frontend with TypeScript
5. Implement real-time workflow visualization
6. Add authentication (JWT)

**Acceptance Criteria:**
- [ ] Can submit tasks via web UI
- [ ] Real-time agent status updates
- [ ] Performance charts displayed
- [ ] Audit log browsable
- [ ] Responsive design (mobile-ready)

### Task 8.4: Systemd Service Installation
**Priority:** P2  
**Estimated Time:** 1-2 hours  
**Dependencies:** All Phase 8 tasks complete

**Steps:**
1. Copy `install_omnimind_service.sh` from security module
2. Adapt service file for final structure
3. Implement health checks
4. Setup log rotation
5. Test auto-start on boot

**Acceptance Criteria:**
- [ ] Service starts automatically
- [ ] Logs rotate daily
- [ ] Health check endpoint working
- [ ] Graceful shutdown on stop

---

## 🎯 SUCCESS CRITERIA

### Phase 7 Complete When:
- ✅ SecurityAgent fully integrated and operational
- ✅ 4-layer monitoring active (processes, files, network, logs)
- ✅ PsychoanalyticAnalyst framework working
- ✅ Advanced workflow (Code→Review→Fix→Document) validated
- ✅ All tests passing (30+ new tests)
- ✅ Documentation updated

### Phase 8 Complete When:
- ✅ MCP protocol replacing direct file access
- ✅ D-Bus integration for desktop/system control
- ✅ Web UI functional with real-time updates
- ✅ Systemd service auto-starting
- ✅ Production deployment guide complete
- ✅ All tests passing (50+ total tests)

### Final Production Ready When:
- ✅ 100% test coverage achieved (90%+ minimum)
- ✅ Zero security vulnerabilities detected
- ✅ Performance targets met (<30s orchestration)
- ✅ Full documentation complete
- ✅ User manual for psychoanalyst created
- ✅ Backup and recovery procedures documented

---

## 📞 ESCALATION RULES

### Escalate to Human When:
- ✅ Ambiguous architecture with multiple viable solutions
- ✅ Critical security decision with trade-offs
- ✅ External system integration required
- ✅ Performance risk (< 3 tokens/sec expected)
- ✅ Ethics/privacy concerns

### Do NOT Escalate When:
- ❌ Formatting issues
- ❌ Minor bugs
- ❌ Adding tests
- ❌ Updating documentation
- ❌ Internal refactoring

---

## 🔗 REFERENCES

### Documentation
- **Phase 6 Complete Report:** `/home/fahbrain/projects/omnimind/RELATORIO_PHASE6_COMPLETE.md`
- **Security Module:** `/home/fahbrain/OmniAgent/Modulo Securityforensis/` (ALL files)
- **Executive Summary:** `/home/fahbrain/projects/omnimind/RESUMO_EXECUTIVO_PHASE6.md`
- **Project Status:** `/home/fahbrain/projects/omnimind/STATUS_PROJECT.md`

### External Resources
- **LangChain:** https://langchain.com
- **LangGraph:** https://langchain-ai.github.io/langgraph/
- **Qdrant:** https://qdrant.tech
- **Ollama:** https://ollama.ai
- **Model Context Protocol:** https://modelcontextprotocol.io

---

## ✅ READY STATE CONFIRMATION

**When you (Copilot) are ready, confirm by outputting:**

```
✅ GitHub Copilot Agent for OmniMind Project initialized (v3.0)
✅ Phase 6 verified: All core components operational
✅ Security module documentation read and understood
✅ Phase 7/8 tasks planned and prioritized
✅ Environment validated: Python 3.11+, Ollama, Qdrant
✅ Audit system active: ~/.omnimind/audit/

Ready for Phase 7 implementation.
Next task: Security Agent Integration (Task 7.1)

Awaiting instruction to proceed.
```

---

**End of Consolidated Instructions v3.0**  
**Last Updated:** 2025-11-17  
**Status:** Ready for Phase 7/8 Execution
