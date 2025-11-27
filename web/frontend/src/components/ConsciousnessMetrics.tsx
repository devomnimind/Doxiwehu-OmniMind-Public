import { useDaemonStore } from '../store/daemonStore';

export function ConsciousnessMetrics() {
  const status = useDaemonStore((state) => state.status);

  if (!status) return null;

  // Check if consciousness metrics are available
  const consciousnessMetrics = status.consciousness_metrics;

  if (!consciousnessMetrics) {
    return (
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Consciousness Metrics</h2>
        <div className="text-gray-400 text-center py-8">
          Consciousness metrics not available
        </div>
      </div>
    );
  }

  const getConsciousnessColor = (value: number) => {
    if (value >= 0.8) return 'text-green-400';
    if (value >= 0.6) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getConsciousnessBarColor = (value: number) => {
    if (value >= 0.8) return 'bg-gradient-to-r from-green-500 to-green-600';
    if (value >= 0.6) return 'bg-gradient-to-r from-yellow-500 to-yellow-600';
    return 'bg-gradient-to-r from-red-500 to-red-600';
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence.toLowerCase()) {
      case 'high':
        return 'text-green-400';
      case 'moderate':
        return 'text-yellow-400';
      default:
        return 'text-red-400';
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
        🧠 Consciousness Metrics
        <span className="text-sm text-gray-400 font-normal">(Simulated Correlates)</span>
      </h2>

      <div className="space-y-6">
        {/* ICI - Integrated Coherence Index */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-gray-300">Integrated Coherence Index (ICI)</span>
            <span className={`text-xl font-bold ${getConsciousnessColor(consciousnessMetrics.ICI)}`}>
              {(consciousnessMetrics.ICI * 100).toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-4 overflow-hidden">
            <div
              className={`h-full transition-all duration-500 ${getConsciousnessBarColor(consciousnessMetrics.ICI)}`}
              style={{ width: `${consciousnessMetrics.ICI * 100}%` }}
            ></div>
          </div>
          <div className="text-xs text-gray-400 mt-1">
            Temporal: {(consciousnessMetrics.details?.ici_components?.temporal_coherence * 100)?.toFixed(1) || 0}% |
            Marker: {(consciousnessMetrics.details?.ici_components?.marker_integration * 100)?.toFixed(1) || 0}% |
            Resonance: {(consciousnessMetrics.details?.ici_components?.resonance * 100)?.toFixed(1) || 0}%
          </div>
        </div>

        {/* PRS - Panarchic Resonance Score */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-gray-300">Panarchic Resonance Score (PRS)</span>
            <span className={`text-xl font-bold ${getConsciousnessColor(consciousnessMetrics.PRS)}`}>
              {(consciousnessMetrics.PRS * 100).toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-4 overflow-hidden">
            <div
              className={`h-full transition-all duration-500 ${getConsciousnessBarColor(consciousnessMetrics.PRS)}`}
              style={{ width: `${consciousnessMetrics.PRS * 100}%` }}
            ></div>
          </div>
          <div className="text-xs text-gray-400 mt-1">
            Micro Entropy: {(consciousnessMetrics.details?.prs_components?.avg_micro_entropy * 100)?.toFixed(1) || 0}% |
            Macro Entropy: {(consciousnessMetrics.details?.prs_components?.macro_entropy * 100)?.toFixed(1) || 0}%
          </div>
        </div>

        {/* Interpretation */}
        <div className="bg-gray-700/50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-300 font-medium">Consciousness State</span>
            <span className={`text-sm font-semibold ${getConfidenceColor(consciousnessMetrics.interpretation?.confidence || 'Low')}`}>
              Confidence: {consciousnessMetrics.interpretation?.confidence || 'Low'}
            </span>
          </div>
          <p className="text-white text-sm">
            {consciousnessMetrics.interpretation?.message || 'Analysis in progress...'}
          </p>
          <p className="text-xs text-gray-400 mt-2 italic">
            {consciousnessMetrics.interpretation?.disclaimer || 'These are simulated correlates, not proof of consciousness.'}
          </p>
        </div>

        {/* Phi Indicator (if available) */}
        {consciousnessMetrics.phi && (
          <div className="bg-purple-900/30 border border-purple-500/50 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-purple-400 font-medium">Φ (Phi) Value</span>
                <p className="text-xs text-gray-400">Integrated Information Measure</p>
              </div>
              <span className="text-2xl font-bold text-purple-400">
                {consciousnessMetrics.phi.toFixed(4)}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}