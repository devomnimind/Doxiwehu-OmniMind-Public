# OmniMind Port Configuration

## ✅ Authorized Services & Ports

### Frontend
- **Port 3000**: React Vite Dev Server
  - Service: `npm run dev` from `web/frontend`
  - Protocol: HTTP
  - Purpose: Dashboard UI

### Backend Services  
- **Port 8000**: FastAPI Backend
  - Service: `python -m uvicorn web.backend.main:app`
  - Protocol: HTTP
  - Purpose: Dashboard API, Audit stats, Daemon control

### Optional/Development
- **Port 9000**: Minimal Backend (testing only)
  - Service: `python simple_backend.py`
  - Protocol: HTTP
  - Purpose: Lightweight testing
  - Note: Should NOT run in production

## ❌ Services That Should NOT Be Running
- MCP Orchestrator (background service, not exposed)
- Any orphaned Node/Python processes
- Vite build processes (only dev server should run)

## Configuration

### Environment Variables (.env)
```
# Frontend
VITE_API_URL=http://127.0.0.1:8000

# Backend  
OMNIMIND_DASHBOARD_USER=admin
OMNIMIND_DASHBOARD_PASS=omnimind2025!
PYTHONPATH=./src:.
```

## Startup Order (One by One)

### 1. Backend (Port 8000)
```bash
cd /home/fahbrain/projects/omnimind
PYTHONPATH=./src:. python -m uvicorn web.backend.main:app --host 127.0.0.1 --port 8000 --log-level info
```

### 2. Frontend (Port 3000)
```bash
cd /home/fahbrain/projects/omnimind/web/frontend
npm run dev
```

## Verification

### Check Ports
```bash
netstat -tulpn | grep -E ":(3000|8000|9000)"
# or
ss -tulpn | grep -E ":(3000|8000|9000)"
```

### Test Endpoints
```bash
# Health check
curl http://127.0.0.1:8000/health

# Audit stats (with auth)
curl -u admin:omnimind2025! http://127.0.0.1:8000/audit/stats
```

## Issues Encountered

1. **Port 9000 lingering**: Python process wasn't cleaning up
   - Solution: Explicit pkill before new starts

2. **Multiple Node processes**: Vite and esbuild spawning orphans
   - Solution: Kill all node/python, restart clean

3. **Zombie processes**: `[node] <defunct>` and `[xcalc] <defunct>`
   - Solution: Parent process cleanup, pkill -9

