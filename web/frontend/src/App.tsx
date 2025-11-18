import { useCallback, useEffect, useMemo, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";
const CREDENTIALS_PATH = "config/dashboard_auth.json";

interface Snapshot {
  plan_summary?: {
    complexity?: string | null;
    subtasks?: number;
    completed?: number;
    failed?: number;
  };
  last_mcp_result?: { final_result?: string; details?: any };
  last_dbus_result?: { final_result?: string; details?: any };
  mcp_metrics?: Record<string, any>;
  media_players?: string[];
  network_status?: Record<string, any>;
  power_status?: Record<string, any>;
}

interface PlanOverview {
  plan?: {
    subtasks?: Array<{ agent?: string; description?: string; status?: string }>;
    original_task?: string;
  };
  progress?: {
    completed?: number;
    failed?: number;
  };
  snapshot?: Snapshot;
}

interface OperationMetrics {
  count: number;
  errors: number;
  avg_latency: number;
}

interface MetricsResponse {
  backend: {
    requests: number;
    errors: number;
    details: Record<string, OperationMetrics>;
  };
  orchestrator: {
    total_requests: number;
    total_errors: number;
    operations: Record<string, OperationMetrics>;
  };
}

function App() {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [plan, setPlan] = useState<PlanOverview | null>(null);
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [authToken, setAuthToken] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [taskInput, setTaskInput] = useState("");
  const [credentials, setCredentials] = useState({ username: "", password: "" });

  const authHeaders = useMemo(() => {
    if (!authToken) return {} as Record<string, string>;
    return {
      Authorization: `Basic ${authToken}`,
      "Content-Type": "application/json",
    };
  }, [authToken]);

  const fetchWithAuth = useCallback(
    (path: string, options: RequestInit = {}) => {
      const headers = new Headers(options.headers ?? undefined);
      Object.entries(authHeaders).forEach(([key, value]) => {
        headers.set(key, value);
      });
      return fetch(`${API_BASE}${path}`, {
        ...options,
        headers,
      });
    },
    [authHeaders]
  );

  const refreshAll = useCallback(async () => {
    if (!authToken) return;
    setLoading(true);
    setError(null);
    try {
      const [snapshotRes, metricsRes, planRes] = await Promise.all([
        fetchWithAuth("/snapshot"),
        fetchWithAuth("/metrics"),
        fetchWithAuth("/plan"),
      ]);

      if (!snapshotRes.ok || !metricsRes.ok || !planRes.ok) {
        throw new Error("Falha ao carregar dados do dashboard");
      }

      const snapshotPayload = await snapshotRes.json();
      const metricsPayload = await metricsRes.json();
      const planPayload = await planRes.json();

      setSnapshot(snapshotPayload);
      setMetrics(metricsPayload);
      setPlan(planPayload);
      setStatusMessage("Dashboard atualizado");
    } catch (exc) {
      setError((exc as Error).message);
    } finally {
      setLoading(false);
    }
  }, [authToken, fetchWithAuth]);

  useEffect(() => {
    if (!authToken) return;
    refreshAll();
    const interval = setInterval(refreshAll, 15000);
    return () => clearInterval(interval);
  }, [authToken, refreshAll]);

  const handleLogin = () => {
    if (!credentials.username || !credentials.password) {
      setStatusMessage("Preencha usuário e senha");
      return;
    }
    setAuthToken(btoa(`${credentials.username}:${credentials.password}`));
  };

  const handleLogout = () => {
    setAuthToken(null);
    setSnapshot(null);
    setPlan(null);
    setMetrics(null);
    setStatusMessage("Sessão encerrada");
  };

  const handleOrchestrate = async () => {
    if (!taskInput.trim() || !authToken) return;
    setStatusMessage("Executando tarefa...");
    try {
      const response = await fetchWithAuth("/tasks/orchestrate", {
        method: "POST",
        body: JSON.stringify({ task: taskInput.trim(), max_iterations: 3 }),
      });
      if (!response.ok) {
        throw new Error("Falha ao orquestrar tarefa");
      }
      await response.json();
      setTaskInput("");
      refreshAll();
      setStatusMessage("Tarefa orquestrada com sucesso");
    } catch (exc) {
      setStatusMessage((exc as Error).message);
    }
  };

  const handleMCP = async () => {
    if (!authToken) return;
    setStatusMessage("Disparando controle MCP...");
    try {
      const response = await fetchWithAuth("/mcp/execute", {
        method: "POST",
        body: JSON.stringify({ action: "read", path: "config/agent_config.yaml" }),
      });
      if (!response.ok) throw new Error("Falha no fluxo MCP");
      const payload = await response.json();
      setSnapshot(payload.dashboard ?? snapshot);
      setStatusMessage(`MCP: ${payload.result.final_result ?? "ok"}`);
    } catch (exc) {
      setStatusMessage((exc as Error).message);
    }
  };

  const handleDBus = async (flow: "power" | "network" | "media") => {
    if (!authToken) return;
    setStatusMessage("Disparando fluxo D-Bus...");
    try {
      const response = await fetchWithAuth("/dbus/execute", {
        method: "POST",
        body: JSON.stringify({ flow, media_action: flow === "media" ? "playpause" : "" }),
      });
      if (!response.ok) throw new Error("Falha no fluxo D-Bus");
      const payload = await response.json();
      setSnapshot(payload.dashboard ?? snapshot);
      setStatusMessage(`D-Bus: ${payload.result.final_result ?? "executado"}`);
    } catch (exc) {
      setStatusMessage((exc as Error).message);
    }
  };

  const headerBadge = useMemo(() => {
    if (!snapshot) return "Sem dados";
    return `${snapshot.plan_summary?.completed ?? 0}/${snapshot.plan_summary?.subtasks ?? 0} concluídos`;
  }, [snapshot]);

  const metricRows = useMemo(() => {
    const rows: Array<[string, OperationMetrics]> = [];
    if (metrics?.backend.details) {
      for (const [key, value] of Object.entries(metrics.backend.details)) {
        rows.push([key, value]);
      }
    }
    return rows;
  }, [metrics]);

  return (
    <div className="page">
      <header>
        <h1>OmniMind Orchestrator Dashboard</h1>
        <p>Monitoramento MCP/D-Bus, métricas e orquestração segura.</p>
      </header>

      {!authToken ? (
        <section className="panel login-panel">
          <h2>Entrar no dashboard</h2>
          <div className="form-row">
            <label>Usuário</label>
            <input
              type="text"
              value={credentials.username}
              onChange={(event) => setCredentials((prev) => ({ ...prev, username: event.target.value }))}
            />
          </div>
          <div className="form-row">
            <label>Senha</label>
            <input
              type="password"
              value={credentials.password}
              onChange={(event) => setCredentials((prev) => ({ ...prev, password: event.target.value }))}
            />
          </div>
          <button className="primary" onClick={handleLogin}>
            Acessar dashboard
          </button>
          {statusMessage && <p className="status-note">{statusMessage}</p>}
        </section>
      ) : (
        <>
          <section className="panel status-panel">
            <div>
              <strong>Snapshot atual:</strong> {headerBadge}
            </div>
            <div className="status-controls">
              <button className="ghost" onClick={refreshAll} disabled={loading}>
                {loading ? "Atualizando..." : "Atualizar agora"}
              </button>
              <button className="ghost" onClick={handleLogout}>
                Sair
              </button>
            </div>
            <div className="credential-warning">
              Credenciais do dashboard em <code>{CREDENTIALS_PATH}</code> (geradas automaticamente, use <strong>chmod 600</strong> e rotacione conforme política interna).
            </div>
            {statusMessage && <p className="status-note">{statusMessage}</p>}
            {error && <p className="error">{error}</p>}
          </section>

          <section className="panel metrics-panel">
            <div className="panel-header">
              <h2>Métricas</h2>
              <span className="badge">Requests: {metrics?.backend.requests ?? 0}</span>
            </div>
            <div className="metrics-grid">
              <div>
                <p className="label">Erros</p>
                <p className="value">{metrics?.backend.errors ?? 0}</p>
              </div>
              <div>
                <p className="label">Operações Orquestrador</p>
                <p className="value">{metrics?.orchestrator.total_requests ?? 0}</p>
              </div>
              <div>
                <p className="label">Falhas Orquestrador</p>
                <p className="value">{metrics?.orchestrator.total_errors ?? 0}</p>
              </div>
            </div>
            <div className="table">
              <p className="label">Detalhes backend</p>
              <ul>
                {metricRows.map(([route, row]) => (
                  <li key={route}>
                    <strong>{route}</strong>: {row.count} chamadas · {row.errors} erros · {row.avg_latency.toFixed(2)}s
                  </li>
                ))}
              </ul>
            </div>
          </section>

          <section className="panel snapshot-panel">
            <div className="panel-header">
              <h2>Plano corrente</h2>
              <span className="badge">{plan?.progress?.completed ?? 0}/
                {plan?.plan?.subtasks?.length ?? 0} concluídos</span>
            </div>
            <p className="subhead">{plan?.plan?.original_task ?? "Sem plano em execução"}</p>
            <div className="plan-list">
              {plan?.plan?.subtasks?.map((subtask, index) => (
                <div key={`${subtask.description}-${index}`} className="plan-item">
                  <div>
                    <p className="label">{subtask.agent ?? "agente"}</p>
                    <p className="value">{subtask.description}</p>
                  </div>
                  <span className={`pill ${subtask.status === "completed" ? "success" : subtask.status === "failed" ? "error" : "neutral"}`}>
                    {subtask.status ?? "pendente"}
                  </span>
                </div>
              ))}
            </div>
          </section>

          <section className="panel orchestrate-panel">
            <div className="panel-header">
              <h2>Executar tarefa</h2>
            </div>
            <div className="form-grid">
              <input
                placeholder="Descreva a tarefa complexa"
                value={taskInput}
                onChange={(event) => setTaskInput(event.target.value)}
              />
              <button className="primary" onClick={handleOrchestrate} disabled={!taskInput.trim()}>
                Iniciar orquestração
              </button>
            </div>
          </section>

          <section className="panel flow-panel">
            <div className="panel-header">
              <h2>Fluxos MCP / D-Bus</h2>
              <div className="flow-actions">
                <button className="ghost" onClick={handleMCP}>
                  MCP: ler config
                </button>
                <button className="ghost" onClick={() => handleDBus("network")}>
                  D-Bus: rede
                </button>
                <button className="ghost" onClick={() => handleDBus("media")}>
                  D-Bus: mídia
                </button>
              </div>
            </div>
            <div className="flow-grid">
              <article>
                <h3>MCP</h3>
                <p>{snapshot?.last_mcp_result?.final_result ?? "Fluxo aguardando"}</p>
                <pre>{JSON.stringify(snapshot?.last_mcp_result?.details ?? {}, null, 2)}</pre>
              </article>
              <article>
                <h3>D-Bus</h3>
                <p>{snapshot?.last_dbus_result?.final_result ?? "Fluxo aguardando"}</p>
                <pre>{JSON.stringify(snapshot?.last_dbus_result?.details ?? {}, null, 2)}</pre>
              </article>
            </div>
          </section>

          <section className="panel mcp-metrics-panel">
            <div className="panel-header">
              <h2>MCP Metrics</h2>
            </div>
            <pre>{JSON.stringify(snapshot?.mcp_metrics ?? { }, null, 2)}</pre>
          </section>
        </>
      )}
    </div>
  );
}

export default App;
