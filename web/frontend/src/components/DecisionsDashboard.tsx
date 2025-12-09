import { useState, useEffect, useCallback } from 'react';
import { apiService } from '../services/api';

interface DecisionSummary {
  action: string;
  timestamp: number;
  can_execute: boolean;
  reason: string;
  trust_level: number;
  success: boolean | null;
}

interface DecisionDetail extends DecisionSummary {
  context: Record<string, any>;
  permission_result: Record<string, any>;
  alternatives_considered: string[];
  expected_impact: Record<string, any>;
  risk_assessment: Record<string, any>;
  decision_rationale: string;
  error?: string;
}

interface DecisionStats {
  total_decisions: number;
  successful_decisions: number;
  failed_decisions: number;
  success_rate: number;
  average_trust_level: number;
  decisions_by_action: Record<string, number>;
  decisions_by_reason: Record<string, number>;
}

export function DecisionsDashboard() {
  const [decisions, setDecisions] = useState<DecisionSummary[]>([]);
  const [selectedDecision, setSelectedDecision] = useState<DecisionDetail | null>(null);
  const [stats, setStats] = useState<DecisionStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filtros
  const [filters, setFilters] = useState({
    action: '',
    success: null as boolean | null,
    min_trust_level: 0,
    limit: 100,
  });

  const fetchDecisions = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getDecisions({
        action: filters.action || undefined,
        success: filters.success !== null ? filters.success : undefined,
        min_trust_level: filters.min_trust_level > 0 ? filters.min_trust_level : undefined,
        limit: filters.limit,
      });
      // Defensive check to ensure data is an array
      if (Array.isArray(data)) {
        setDecisions(data);
      } else {
        console.error('Expected array from getDecisions, got:', typeof data, data);
        setDecisions([]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar decisões');
      console.error('Error fetching decisions:', err);
      setDecisions([]);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const fetchStats = useCallback(async () => {
    try {
      const data = await apiService.getDecisionStats();
      // Validate stats object
      if (data && typeof data === 'object') {
        setStats(data as DecisionStats);
      } else {
        setStats(null);
      }
    } catch (err) {
      console.error('Error fetching stats:', err);
      setStats(null);
    }
  }, []);

  const fetchDecisionDetail = useCallback(async (index: number) => {
    try {
      const data = await apiService.getDecisionDetail(index);
      // Validate that data is an object with expected fields
      if (data && typeof data === 'object' && 'action' in data) {
        setSelectedDecision(data as DecisionDetail);
      } else {
        setSelectedDecision(null);
      }
    } catch (err) {
      console.error('Error fetching decision detail:', err);
      setSelectedDecision(null);
    }
  }, []);

  const handleExport = useCallback(async () => {
    try {
      const data = await apiService.exportDecisions({
        action: filters.action || undefined,
        limit: filters.limit,
      });

      // Criar download
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `decisions_export_${new Date().toISOString()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error exporting decisions:', err);
      alert('Erro ao exportar decisões');
    }
  }, [filters]);

  useEffect(() => {
    fetchDecisions();
    fetchStats();

    // Atualizar a cada 30 segundos
    const interval = setInterval(() => {
      fetchDecisions();
      fetchStats();
    }, 30000);

    return () => clearInterval(interval);
  }, [fetchDecisions, fetchStats]);

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString('pt-BR');
  };

  const getTrustLevelColor = (trust: number) => {
    if (trust >= 0.7) return 'text-green-600';
    if (trust >= 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getSuccessBadge = (success: boolean | null) => {
    if (success === null) return <span className="px-2 py-1 bg-gray-200 text-gray-700 rounded text-xs">N/A</span>;
    if (success) return <span className="px-2 py-1 bg-green-200 text-green-700 rounded text-xs">✓ Sucesso</span>;
    return <span className="px-2 py-1 bg-red-200 text-red-700 rounded text-xs">✗ Falhou</span>;
  };

  if (loading && decisions.length === 0) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Dashboard de Decisões</h2>
        <button
          onClick={handleExport}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Exportar JSON
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Estatísticas */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm text-gray-600">Total de Decisões</div>
            <div className="text-2xl font-bold text-gray-800">{stats.total_decisions}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm text-gray-600">Taxa de Sucesso</div>
            <div className="text-2xl font-bold text-green-600">{(stats.success_rate * 100).toFixed(1)}%</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm text-gray-600">Confiança Média</div>
            <div className="text-2xl font-bold text-blue-600">{(stats.average_trust_level * 100).toFixed(1)}%</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm text-gray-600">Decisões Falhadas</div>
            <div className="text-2xl font-bold text-red-600">{stats.failed_decisions}</div>
          </div>
        </div>
      )}

      {/* Filtros */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Filtros</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Ação</label>
            <input
              type="text"
              value={filters.action}
              onChange={(e) => setFilters({ ...filters, action: e.target.value })}
              placeholder="Filtrar por ação..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              value={filters.success === null ? '' : filters.success.toString()}
              onChange={(e) => setFilters({ ...filters, success: e.target.value === '' ? null : e.target.value === 'true' })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos</option>
              <option value="true">Sucesso</option>
              <option value="false">Falhou</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Confiança Mínima</label>
            <input
              type="number"
              min="0"
              max="1"
              step="0.1"
              value={filters.min_trust_level}
              onChange={(e) => setFilters({ ...filters, min_trust_level: parseFloat(e.target.value) || 0 })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Limite</label>
            <input
              type="number"
              min="1"
              max="1000"
              value={filters.limit}
              onChange={(e) => setFilters({ ...filters, limit: parseInt(e.target.value) || 100 })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        <button
          onClick={fetchDecisions}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Aplicar Filtros
        </button>
      </div>

      {/* Lista de Decisões */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold">Histórico de Decisões ({decisions.length})</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ação</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data/Hora</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Confiança</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Razão</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {decisions.map((decision, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{decision.action}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-500">{formatTimestamp(decision.timestamp)}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getSuccessBadge(decision.success)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className={`text-sm font-medium ${getTrustLevelColor(decision.trust_level)}`}>
                      {(decision.trust_level * 100).toFixed(1)}%
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-500">{decision.reason}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <button
                      onClick={() => fetchDecisionDetail(index)}
                      className="text-blue-600 hover:text-blue-800 text-sm"
                    >
                      Ver Detalhes
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {decisions.length === 0 && !loading && (
            <div className="text-center py-8 text-gray-500">
              Nenhuma decisão encontrada
            </div>
          )}
        </div>
      </div>

      {/* Detalhes da Decisão Selecionada */}
      {selectedDecision && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">Detalhes da Decisão</h3>
            <button
              onClick={() => setSelectedDecision(null)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>
          <div className="space-y-4">
            <div>
              <strong>Ação:</strong> {selectedDecision.action}
            </div>
            <div>
              <strong>Data/Hora:</strong> {formatTimestamp(selectedDecision.timestamp)}
            </div>
            <div>
              <strong>Status:</strong> {getSuccessBadge(selectedDecision.success)}
            </div>
            <div>
              <strong>Confiança:</strong> <span className={getTrustLevelColor(selectedDecision.trust_level)}>
                {(selectedDecision.trust_level * 100).toFixed(1)}%
              </span>
            </div>
            <div>
              <strong>Razão:</strong> {selectedDecision.reason}
            </div>
            {selectedDecision.decision_rationale && (
              <div>
                <strong>Racional:</strong>
                <p className="mt-1 text-sm text-gray-600">{selectedDecision.decision_rationale}</p>
              </div>
            )}
            {selectedDecision.alternatives_considered.length > 0 && (
              <div>
                <strong>Alternativas Consideradas:</strong>
                <ul className="mt-1 list-disc list-inside text-sm text-gray-600">
                  {selectedDecision.alternatives_considered.map((alt, i) => (
                    <li key={i}>{alt}</li>
                  ))}
                </ul>
              </div>
            )}
            {selectedDecision.error && (
              <div className="bg-red-50 border border-red-200 rounded p-3">
                <strong className="text-red-800">Erro:</strong>
                <p className="text-sm text-red-600 mt-1">{selectedDecision.error}</p>
              </div>
            )}
            <details className="mt-4">
              <summary className="cursor-pointer text-sm font-medium text-gray-700">Contexto Completo</summary>
              <pre className="mt-2 p-4 bg-gray-50 rounded text-xs overflow-auto">
                {JSON.stringify(selectedDecision.context, null, 2)}
              </pre>
            </details>
          </div>
        </div>
      )}
    </div>
  );
}

