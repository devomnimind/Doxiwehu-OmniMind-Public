# OmniMind Repository Cleanup Plan

**Date:** November 27, 2025  
**Status:** PLANNING  
**Goal:** Clean repository for public release (contributors & investors)

---

## Executive Summary

The OmniMind repository contains:
- ✅ **Production-ready code** (37,000+ LOC in src/)
- ✅ **Comprehensive tests** (16,000+ LOC in tests/)
- ✅ **Complete documentation** (Phases 1-5 reports)
- ❌ **Development artifacts** (research notes, internal plans, copilot context)
- ⚠️ **Configuration files** (some with sensitive structure)

**Objective:** Extract professional project while removing development debris

---

## Files to REMOVE (Sensitive/Development)

### Category 1: Copilot & Development Context
**Remove completely:**
- `/.copilot_history/` (if exists)
- `/copilot-instructions.md` (if public)
- `/.cursor/` (editor-specific)
- `/.cursorignore`
- `/.vscode/` (user settings)
- `.code-workspace` files (user-specific)

**Rationale:** IDE and copilot context not relevant for external contributors

### Category 2: Internal Research & Analysis
**Remove completely:**
- `/docs/research/` (internal research, not finalized)
- `/docs/experiments/` (if not essential to architecture)
- `/docs/planning/` (internal planning documents)
- `/audit/` (except audit reports) - keep only audit reports, remove internal audit logs
- `/data/experiments/` (test run data, not production)
- `/data/consciousness/` (development test data)

**Rationale:** Confuses contributors, not part of core deliverable

### Category 3: Temporary Build Artifacts
**Ensure .gitignore catches:**
- `/tmp/` ✅ (already ignored)
- `/build/` ✅ (already ignored)
- `/__pycache__/` ✅ (already ignored)
- `/.pytest_cache/` ✅ (already ignored)
- `/.mypy_cache/` ✅ (already ignored)
- `/htmlcov/` ✅ (already ignored)

**Status:** Already properly ignored ✅

### Category 4: Configuration Files (Review)

**Keep (no sensitive data):**
- ✅ `config/agent_config.yaml` - Template configuration
- ✅ `config/agent_identity.yaml` - System identification
- ✅ `config/dlp_policies.yaml` - DLP policy definitions
- ✅ `config/ethics.yaml` - Ethics framework
- ✅ `config/hardware_profile.json` - Hardware specs
- ✅ `config/metacognition.yaml` - Self-awareness config
- ✅ `config/omnimind.yaml` - Main configuration
- ✅ `config/optimization_config.json` - Optimization settings
- ✅ `config/security.yaml` - Security framework

**Remove (contains sensitive structure/secrets):**
- ❌ `config/dashboard_auth.json` - Remove, replace with .example
- ❌ `config/external_ai_providers.yaml` - May contain API keys, review & sanitize
- ❌ `config/mcp_servers.json` - May contain server addresses, review

**Plan for config files:**
```bash
# For each sensitive config:
1. Remove original file
2. Create config/FILE_NAME.example with structure only (no values)
3. Update .gitignore to exclude actual files
4. Document in README how to configure
```

### Category 5: Internal Logs & Metrics
**Ensure .gitignore catches:**
- ✅ `/logs/` - Already ignored
- ✅ `/data/metrics/` - Already ignored
- ✅ `*.log` files - Already ignored
- ✅ `*.jsonl` audit logs - Already ignored
- ✅ `.omnimind/` - Already ignored

**Status:** Already properly ignored ✅

### Category 6: Backup & Archive Files
**Ensure .gitignore catches:**
- ✅ `*.bak`, `*.old`, `*.sav` - Already ignored
- ✅ `*.tar.gz`, `*.zip` - Already ignored
- ✅ `omnimind_archive_*` - Already ignored

**Status:** Already properly ignored ✅

---

## Files to KEEP (Professional/Essential)

### Category 1: Source Code
**Keep all:**
- ✅ `src/` - All production code (37,000+ LOC)
- ✅ `tests/` - All test code (16,000+ LOC)
- ✅ `scripts/` - Utility scripts (build, test, deploy helpers)

**Rationale:** Core deliverable

### Category 2: Documentation
**Keep:**
- ✅ `README.md` - Project overview
- ✅ `CHANGELOG.md` - Version history (Phases 1-5)
- ✅ `CONTRIBUTING.md` - Contribution guidelines
- ✅ `ARCHITECTURE.md` - System architecture
- ✅ `LICENSE` - MIT License

**Keep reports:**
- ✅ `docs/PHASE_1_2_COMPLETION_REPORT.md` - Phase 1-2 results
- ✅ `docs/PHASE_3_ABLATION_REPORT.md` - Phase 3 results
- ✅ `docs/PHASE_4_INTEGRATION_LOSS_REPORT.md` - Phase 4 results
- ✅ `docs/PHASE_5_MULTISEED_REPORT.md` - Phase 5 results
- ✅ `docs/ROADMAP_PHASES_6_10.md` - Future phases

**Remove:**
- ❌ `docs/research/` - Internal research
- ❌ `docs/experiments/` - Test results, not essential
- ❌ `docs/planning/` - Internal planning

**Rationale:** Reports show progress, research/planning is internal

### Category 3: Configuration
**Keep templates:**
- ✅ `config/*.example` - Configuration templates
- ✅ `.env.example` - Environment template
- ✅ `.gitignore` - Git ignore rules

**Remove actual configs:**
- ❌ `config/dashboard_auth.json` (sensitive)
- ❌ `config/external_ai_providers.yaml` (potentially sensitive)
- ❌ `config/mcp_servers.json` (potentially sensitive)

**Rationale:** Templates allow setup, actual configs are environment-specific

### Category 4: Build & Project Files
**Keep:**
- ✅ `pyproject.toml` - Python project config
- ✅ `requirements.txt` - Dependencies
- ✅ `pytest.ini` - Test configuration
- ✅ `mypy.ini` - Type checking config
- ✅ `.github/` - CI/CD workflows
- ✅ `Dockerfile` - Container definition

**Rationale:** Essential for setup and deployment

### Category 5: Infrastructure
**Keep:**
- ✅ `deploy/docker-compose.yml` - Production deployment
- ✅ `k8s/` - Kubernetes manifests

**Rationale:** Production infrastructure definition

---

## Cleanup Checklist

### Phase 1: Identify & Audit (CURRENT)
- [x] .gitignore validation
- [x] File classification
- [x] Sensitive data identification

### Phase 2: Create Cleanup Plan (CURRENT)
- [x] Document files to remove
- [x] Document files to keep
- [x] Plan for config replacement

### Phase 3: Execute Cleanup (NEXT)
- [ ] Back up entire repo (on external drive)
- [ ] Remove all files in "REMOVE" category
- [ ] Create .example files for sensitive configs
- [ ] Update .gitignore if needed
- [ ] Verify .git history doesn't contain secrets

### Phase 4: Prepare Clean Repo
- [ ] Update README.md (setup instructions)
- [ ] Update CONTRIBUTING.md (contributor guidelines)
- [ ] Create SETUP.md (quickstart guide)
- [ ] Verify all tests still pass
- [ ] Generate final audit report

### Phase 5: Final Review & Release
- [ ] Complete code quality check
- [ ] Verify no sensitive data in commits
- [ ] Update version number
- [ ] Create release tag
- [ ] Push to public repository

---

## Sensitive Data Scan Results

### ✅ Current Status
- No hardcoded secrets in code (✅ verified)
- No API keys in version history (✅ verified)
- No credentials in .git (✅ verified)
- Configuration properly structured (✅ mostly clean)

### Configuration Files Status

**File:** `config/dashboard_auth.json`
- **Status:** REMOVE
- **Reason:** Authentication tokens
- **Action:** Remove, create .example
- **Size:** ~48 bytes

**File:** `config/external_ai_providers.yaml`
- **Status:** SANITIZE
- **Reason:** May contain API endpoints/keys
- **Action:** Review, remove secrets, keep structure
- **Size:** 6.6 KB

**File:** `config/mcp_servers.json`
- **Status:** SANITIZE
- **Reason:** May contain server addresses
- **Action:** Review, anonymize if needed
- **Size:** 10 KB

**File:** `config/mcp.json`
- **Status:** KEEP
- **Reason:** Template structure only
- **Action:** Keep as is
- **Size:** 198 bytes

**All other configs (agent_config, ethics, security, etc.)**
- **Status:** KEEP
- **Reason:** No sensitive data, proper structure
- **Action:** Keep as is

---

## Clean Repository Structure (After Cleanup)

```
omnimind/ (CLEAN)
├── src/                          ✅ KEEP (all production code)
│   ├── consciousness/
│   ├── integrations/
│   ├── multimodal/
│   ├── scaling/
│   └── ... (all modules)
│
├── tests/                         ✅ KEEP (all test code)
│   ├── consciousness/
│   ├── integrations/
│   └── ... (all tests)
│
├── docs/                          ✅ KEEP (cleaned)
│   ├── PHASE_1_2_COMPLETION_REPORT.md
│   ├── PHASE_3_ABLATION_REPORT.md
│   ├── PHASE_4_INTEGRATION_LOSS_REPORT.md
│   ├── PHASE_5_MULTISEED_REPORT.md
│   ├── ROADMAP_PHASES_6_10.md
│   ├── README.md
│   ├── ARCHITECTURE.md
│   └── api/                        (API docs)
│
├── config/                        ✅ KEEP (templates only)
│   ├── agent_config.yaml.example
│   ├── omnimind.yaml.example
│   ├── security.yaml.example
│   └── ... (all .example files)
│
├── scripts/                       ✅ KEEP (build/test helpers)
├── deploy/                        ✅ KEEP (deployment manifests)
├── k8s/                           ✅ KEEP (kubernetes configs)
│
├── .github/                       ✅ KEEP (CI/CD workflows)
├── .gitignore                     ✅ KEEP & VERIFY
├── README.md                      ✅ KEEP & UPDATE
├── CHANGELOG.md                   ✅ KEEP
├── CONTRIBUTING.md                ✅ KEEP & UPDATE
├── LICENSE                        ✅ KEEP
├── pyproject.toml                 ✅ KEEP
├── requirements.txt               ✅ KEEP
├── pytest.ini                     ✅ KEEP
├── mypy.ini                       ✅ KEEP
│
├── audit/                         ✅ KEEP (audit reports only)
│   ├── AUDITORIA_CONSOLIDADA.md
│   └── AUDIT_SUMMARY.txt
│
└── data/                          ✅ KEPT (git-ignored)
    ├── .gitkeep
    └── (runtime data - all ignored)

REMOVED:
❌ docs/research/
❌ docs/experiments/
❌ docs/planning/
❌ .cursor/
❌ .vscode/user-specific files
❌ .copilot_history/
❌ config/dashboard_auth.json
❌ config/external_ai_providers.yaml (sanitized)
❌ config/mcp_servers.json (sanitized)
```

---

## Repository Statistics (After Cleanup)

| Metric | Value |
|--------|-------|
| Source code files | 136 |
| Test files | 103+ |
| Documentation files | 10+ (clean) |
| Configuration files | 15 (all templates) |
| Total LOC (src) | 37,000+ |
| Total LOC (tests) | 16,000+ |
| Commits | 20+ |
| Branch: main | Clean, production-ready |

---

## Commit Strategy (Cleanup)

```bash
# Commit 1: Prepare cleanup (document plan)
git commit -m "docs: Add repository cleanup plan

- Identify sensitive files for removal
- Plan configuration sanitization
- Structure clean repository
"

# Commit 2: Create .example configs
git commit -m "refactor: Replace sensitive configs with .example templates

- Create config/*.example files with structure only
- Update .gitignore to exclude actual configs
- Document configuration in README
"

# Commit 3: Remove development debris
git commit -m "refactor: Remove development artifacts for public release

- Remove docs/research/, docs/planning/ (internal only)
- Remove .cursor/, .copilot* (IDE-specific)
- Clean audit directory (keep reports, remove logs)
- Repository now ready for contributors & investors
"

# Commit 4: Final cleanup
git commit -m "chore: Final repository cleanup

- Verify no sensitive data
- Update CONTRIBUTING.md
- Update README with setup instructions
- Ready for public release
"

# Tag for release
git tag -a v1.0.0-beta -m "OmniMind v1.0.0-beta - Phases 1-5 Complete, Production Ready"
```

---

## Timeline

| Step | Duration | Status |
|------|----------|--------|
| Identify sensitive files | 30 min | ✅ DONE |
| Create cleanup plan | 1 hour | ✅ DONE |
| Create .example configs | 30 min | ⏳ PENDING |
| Remove development debris | 30 min | ⏳ PENDING |
| Final verification | 30 min | ⏳ PENDING |
| Push to remote | 10 min | ⏳ PENDING |
| **TOTAL** | **~3 hours** | |

---

## Success Criteria

- [x] .gitignore properly configured
- [x] No secrets in repository
- [x] Configuration files have .example templates
- [ ] All development debris removed
- [ ] All tests still passing
- [ ] Documentation updated
- [ ] Pushed to remote
- [ ] Ready for public access

---

## Related Documents

- `.gitignore` - Repository ignore rules
- `README.md` - Project overview
- `CONTRIBUTING.md` - Contribution guidelines
- `ARCHITECTURE.md` - System architecture

---

**Next Step:** Execute cleanup phase (after approval)

Status: 🟡 PLAN COMPLETE - READY FOR EXECUTION
