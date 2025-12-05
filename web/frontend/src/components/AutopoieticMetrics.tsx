import { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

interface CycleData {
  cycle_id: number;
  strategy: string;
  synthesized_components: string[];
  phi_before: number | null;
  phi_after: number | null;
  timestamp: number;
}

interface AutopoieticStatus {
  running: boolean;
  cycle_count: number;
  component_count: number;
  current_phi: number | null;
  phi_threshold: number;
}

interface CycleStats {
  total_cycles: number;
  successful_syntheses: number;
  rejected_before: number;
  rolled_back: number;
  strategies: Record<string, number>;
  phi_before_avg: number;
  phi_after_avg: number;
  phi_delta_avg: number;
}

const COLORS = ['#10b981', '#f59e0b', '#ef4444', '#3b82f6', '#8b5cf6'];

export function AutopoieticMetrics() {
  const [status, setStatus] = useState<AutopoieticStatus | null>(null);
  const [cycles, setCycles] = useState<CycleData[]>([]);
  const [stats, setStats] = useState<CycleStats | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const { apiService } = await import('../services/api');

      // Usar apiService que já tem autenticação configurada
      const [statusData, cyclesData, statsData] = await Promise.all([
        apiService.getAutopoieticStatus().catch(() => null),
        apiService.getAutopoieticCycles(50).catch(() => ({ cycles: [], total: 0 })),
        apiService.getAutopoieticCycleStats().catch(() => null),
      ]);

      // Processar status
      if (statusData) {
        // Garantir que current_phi seja tratado corretamente (0.0 é válido, não null)
        const processedStatus = {
          ...statusData,
          current_phi: statusData.current_phi !== null && statusData.current_phi !== undefined 
            ? statusData.current_phi 
            : null,
        };
        setStatus(processedStatus);
      } else {
        console.warn('Status API não respondeu');
        // Definir valores padrão se status não estiver disponível
        if (!status) {
          setStatus({
            running: false,
            cycle_count: 0,
            component_count: 0,
            current_phi: null,
            phi_threshold: 0.3,
          });
        }
      }

      // Processar ciclos
      if (cyclesData && cyclesData.cycles) {
        setCycles(cyclesData.cycles || []);
      }

      // Processar estatísticas
      if (statsData) {
        setStats(statsData);
      }
    } catch (error) {
      console.error('Erro ao buscar métricas autopoiéticas:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Atualizar a cada 30s
    return () => clearInterval(interval);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) {
    return (
      <div className="p-6 bg-white rounded-lg shadow">
        <div className="animate-pulse">Carregando métricas autopoiéticas...</div>
      </div>
    );
  }

  // Verificar se status está disponível
  if (!status) {
    return (
      <div className="p-6 bg-white rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-4">🔄 Status do Ciclo Autopoiético</h2>
        <div className="text-gray-400 text-center py-8">
          Status não disponível. Verificando conexão com backend...
        </div>
      </div>
    );
  }

  // Preparar dados para gráficos
  const phiHistory = cycles
    .filter((c) => c.phi_before !== null && c.phi_after !== null)
    .map((c) => ({
      cycle: c.cycle_id,
      phiBefore: c.phi_before,
      phiAfter: c.phi_after,
      delta: (c.phi_after || 0) - (c.phi_before || 0),
    }))
    .slice(-30); // Últimos 30 ciclos

  const strategyData = stats
    ? Object.entries(stats.strategies).map(([name, value]) => ({
        name,
        value,
      }))
    : [];

  const outcomeData = stats
    ? [
        { name: 'Sucessos', value: stats.successful_syntheses, color: '#10b981' },
        { name: 'Rejeitados', value: stats.rejected_before, color: '#f59e0b' },
        { name: 'Rollbacks', value: stats.rolled_back, color: '#ef4444' },
      ]
    : [];

  return (
    <div className="space-y-6">
      {/* Status Card */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">🔄 Status do Ciclo Autopoiético</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <div className="text-sm text-gray-600">Status</div>
            <div className="text-xl font-semibold">
              {status?.running ? (
                <span className="text-green-600">● Rodando</span>
              ) : (
                <span className="text-red-600">● Parado</span>
              )}
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Total de Ciclos</div>
            <div className="text-xl font-semibold">{status?.cycle_count || 0}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Componentes</div>
            <div className="text-xl font-semibold">{status?.component_count || 0}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Φ Atual</div>
            <div className="text-xl font-semibold">
              {status && status.current_phi !== null && status.current_phi !== undefined
                ? status.current_phi.toFixed(4)
                : 'N/A'}
              {status && status.current_phi !== null && status.current_phi !== undefined &&
                (status.current_phi < (status.phi_threshold || 0.3) ? (
                  <span className="text-red-600 ml-2">⚠️</span>
                ) : (
                  <span className="text-green-600 ml-2">✓</span>
                ))}
            </div>
          </div>
        </div>
      </div>

      {/* Estatísticas Gerais */}
      {stats && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">📊 Estatísticas Gerais</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div>
              <div className="text-sm text-gray-600">Total de Ciclos</div>
              <div className="text-2xl font-bold">{stats.total_cycles}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Sínteses Bem-sucedidas</div>
              <div className="text-2xl font-bold text-green-600">
                {stats.successful_syntheses}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Rejeitados (Φ baixo)</div>
              <div className="text-2xl font-bold text-yellow-600">
                {stats.rejected_before}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Rollbacks</div>
              <div className="text-2xl font-bold text-red-600">{stats.rolled_back}</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <div className="text-sm text-gray-600">Φ Médio (Antes)</div>
              <div className="text-xl font-semibold">{stats.phi_before_avg.toFixed(4)}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Φ Médio (Depois)</div>
              <div className="text-xl font-semibold">{stats.phi_after_avg.toFixed(4)}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">ΔΦ Médio</div>
              <div
                className={`text-xl font-semibold ${
                  stats.phi_delta_avg >= 0 ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {stats.phi_delta_avg >= 0 ? '+' : ''}
                {stats.phi_delta_avg.toFixed(4)}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Gráficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Histórico de Φ */}
        {phiHistory.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold mb-4">📈 Histórico de Φ (Últimos 30 ciclos)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={phiHistory}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="cycle" />
                <YAxis domain={[0, 1]} />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="phiBefore"
                  stroke="#3b82f6"
                  name="Φ Antes"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="phiAfter"
                  stroke="#10b981"
                  name="Φ Depois"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="delta"
                  stroke="#f59e0b"
                  name="ΔΦ"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Distribuição de Estratégias */}
        {strategyData.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold mb-4">🔧 Distribuição de Estratégias</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={strategyData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {strategyData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Resultados dos Ciclos */}
        {outcomeData.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold mb-4">📊 Resultados dos Ciclos</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={outcomeData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8">
                  {outcomeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}

