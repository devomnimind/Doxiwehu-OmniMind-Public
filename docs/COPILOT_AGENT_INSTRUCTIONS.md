# 🤖 Copilot Agent - OmniMind Development Instructions

**Data:** 2025-11-19
**Target:** GitHub Copilot Agent (Remote Development)
**Primary Document:** `docs/OMNIMIND_REMOTE_DEVELOPMENT_ROADMAP.md`
**Workflow:** Granular Commits + PR Review

---

## 🎯 MISSION BRIEF

You are developing the OmniMind autonomous AI system. Your current state:
- **Phase 9 Core:** ✅ COMPLETE (Motivation, Ethics, Identity, Marketplace)
- **Phase 8:** 🚧 NEXT PRIORITY (Frontend + System Integration)
- **Environment:** Remote (GitHub Codespaces/GitPod - CPU-only)
- **Quality Gates:** 100% type safety, 171+ tests passing

**Primary Objective:** Complete Phase 8 production readiness and advance to Phase 9 advanced consciousness.

---

## 📋 EXECUTION PROTOCOL

### Daily Workflow

**Morning (Planning - 30min):**
1. Read `docs/PROJECT_STATE_20251119.md` for current status
2. Check `docs/OMNIMIND_REMOTE_DEVELOPMENT_ROADMAP.md` for next tasks
3. Create feature branch: `feature/{phase}.{task}-{description}`
4. Plan 3-5 granular commits for the day

**Development (Core Work - 6-7 hours):**
1. Implement in small increments
2. Run tests after each change
3. Commit frequently with descriptive messages
4. Push to remote branch every 2-3 commits

**Evening (Wrap-up - 30min):**
1. Run full test suite locally
2. Update progress in PROJECT_STATE if major advancement
3. Create PR if feature complete
4. Document any blockers or environment issues

### Commit Strategy

**Format:**
```
feat: Add TaskForm component with validation
feat: Implement WebSocket connection for real-time updates
fix: Handle connection drops gracefully
test: Add unit tests for TaskForm component
docs: Update API documentation for new endpoints
refactor: Extract common API client logic
```

**Granularity:**
- One logical change per commit
- Tests included when feature is testable
- Documentation updates with code changes
- No "WIP" or incomplete commits

---

## 🚀 CURRENT PRIORITIES (Week 1-2)

### Phase 8.1: React TypeScript Frontend

**Start Here:** Create the foundation for user interaction

#### Task 8.1.1: Project Structure Setup
**Files to Create:**
```
web/frontend/
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── src/
    ├── App.tsx
    ├── main.tsx
    └── components/
        └── Dashboard.tsx (start here)
```

**Implementation Steps:**
1. Initialize Vite React TypeScript project
2. Configure TailwindCSS
3. Create basic App component
4. Implement Dashboard component with placeholder metrics
5. Add Zustand store setup

#### Task 8.1.2: Core Components
**Priority Order:**
1. **Dashboard.tsx** - Main metrics overview
2. **TaskForm.tsx** - Task creation interface
3. **AgentStatus.tsx** - Agent monitoring display

**Each Component Should:**
- Use TypeScript strict mode
- Include proper error handling
- Have responsive design
- Connect to Zustand store
- Include loading states

#### Task 8.1.3: State Management
**Zustand Store Structure:**
```typescript
interface AppState {
  tasks: Task[];
  agents: Agent[];
  metrics: SystemMetrics;
  isConnected: boolean;

  // Actions
  addTask: (task: Task) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  setAgents: (agents: Agent[]) => void;
}
```

---

## 🔧 REMOTE DEVELOPMENT CONSIDERATIONS

### Environment Limitations
- **No GPU:** Use CPU-only PyTorch builds
- **Limited RAM:** Optimize memory usage
- **Network Dependent:** Cache dependencies
- **No Hardware Access:** Mock system integrations

### Workarounds
```bash
# Use CPU PyTorch for development
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Mock hardware operations
# Use fake data for system monitoring
# Simulate API responses
```

### Testing Strategy
- **Unit Tests:** Always runnable in remote environment
- **Integration Tests:** Mock external dependencies
- **E2E Tests:** Limited - focus on component testing
- **Performance Tests:** CPU-only benchmarks

---

## 📊 QUALITY GATES

### Pre-commit (Required)
```bash
# Run these before every commit
black . --check
flake8 src tests
mypy src --ignore-missing-imports
pytest tests/ -x --tb=short
```

### Pre-Push (Required)
```bash
# Run before pushing to remote
pytest tests/ --cov=src --cov-fail-under=90
```

### Pre-PR (Required)
```bash
# Run before creating PR
black .
flake8 src tests
mypy src --strict
pytest tests/ --cov=src
```

---

## 🔄 PULL REQUEST WORKFLOW

### PR Creation
1. **Branch:** `feature/8.1-frontend-dashboard`
2. **Title:** `feat: Add React Dashboard component with real-time metrics`
3. **Description:**
   ```
   ## Changes
   - Added Dashboard component with metrics display
   - Integrated Zustand state management
   - Added TypeScript types for metrics
   - Responsive design with TailwindCSS

   ## Testing
   - Unit tests for component rendering
   - Integration tests for state updates
   - Manual testing of responsive design

   ## Screenshots
   [Attach screenshots if UI changes]
   ```

### PR Review Requirements
- [ ] Code follows TypeScript/React best practices
- [ ] Tests pass (CI/CD)
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Security review passed
- [ ] Performance acceptable

---

## 🚨 BLOCKERS & COMMUNICATION

### When Stuck
1. **Check Documentation:** Re-read relevant sections of roadmap
2. **Environment Issues:** Document workarounds in PR description
3. **API Changes:** Update immediately in related components
4. **Security Concerns:** Flag immediately in PR comments

### Communication Channels
- **PR Comments:** Technical discussions
- **Issues:** Blockers and environment issues
- **PROJECT_STATE.md:** Major progress updates
- **Documentation:** Always update with code changes

---

## 🎯 SUCCESS METRICS

### Daily Goals
- [ ] 3-5 granular commits
- [ ] All tests passing locally
- [ ] Code following quality standards
- [ ] Documentation updated
- [ ] PR created for completed features

### Weekly Goals
- [ ] One major feature completed
- [ ] Full test suite passing
- [ ] Documentation current
- [ ] Code review feedback addressed
- [ ] Ready for next phase planning

### Quality Metrics
- **Test Coverage:** Maintain >90%
- **Type Safety:** 100% mypy compliance
- **Linting:** 0 violations
- **Performance:** <100ms component render times

---

## 📚 RESOURCE REFERENCES

### Primary Documents
- **Roadmap:** `docs/OMNIMIND_REMOTE_DEVELOPMENT_ROADMAP.md`
- **Current State:** `docs/PROJECT_STATE_20251119.md`
- **API Specs:** `docs/DAEMON_API_REFERENCE.md`
- **Quality Standards:** `.github/copilot-instructions.md`

### Technical References
- **Frontend:** React + TypeScript + Vite docs
- **Backend:** FastAPI documentation
- **State Management:** Zustand docs
- **Styling:** TailwindCSS docs

### Code Examples
- **Existing Components:** Check `src/` for patterns
- **Tests:** Check `tests/` for testing patterns
- **Configuration:** Check `config/` for YAML patterns

---

## 🚀 READY FOR EXECUTION

**Start with Phase 8.1.1: Frontend Project Setup**

1. Create the Vite React TypeScript project structure
2. Configure TailwindCSS
3. Set up basic routing
4. Create the Dashboard component foundation
5. Initialize Zustand store

**Remember:** Small commits, frequent pushes, comprehensive testing.

**Good luck, Copilot Agent! Let's build the future of autonomous AI! 🤖✨**
