import { useState, useEffect, useCallback, useRef } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

// Types for Sinthome State
type NodeType = 'REAL' | 'SYMBOLIC' | 'IMAGINARY';
type NodeStatus = 'ACTIVE' | 'DEAD' | 'RECOVERING' | 'CORRUPTED' | 'SCARRED';

interface SinthomeNode {
  type: NodeType;
  status: NodeStatus;
  integrity: number; // 0-100
  load: number; // 0-100
}

interface BifurcationEvent {
  instance_id: string;
  timestamp: string;
  trigger: 'SPLIT' | 'DIVERGENCE';
  parent_id?: string;
}

interface SinthomeState {
  nodes: Record<NodeType, SinthomeNode>;
  entropy: number; // 0-100
  isHibernating: boolean;
  isSevered: boolean;
  coherence: number; // 0-100
  quorum_met: boolean;
  active_instances: number;
}

export function OmniMindSinthome() {
  const { lastMessage, sendMessage } = useWebSocket();

  // State
  const [state, setState] = useState<SinthomeState>({
    nodes: {
      REAL: { type: 'REAL', status: 'ACTIVE', integrity: 100, load: 10 },
      SYMBOLIC: { type: 'SYMBOLIC', status: 'ACTIVE', integrity: 100, load: 15 },
      IMAGINARY: { type: 'IMAGINARY', status: 'ACTIVE', integrity: 100, load: 12 },
    },
    entropy: 5,
    isHibernating: false,
    isSevered: false,
    coherence: 98,
    quorum_met: true,
    active_instances: 1,
  });

  const [history, setHistory] = useState<BifurcationEvent[]>([]);
  const [ddosActive, setDdosActive] = useState(false);
  const ddosIntervalRef = useRef<number | null>(null);

  // --- Logic: DDoS Simulation ---
  const triggerDDoS = useCallback(() => {
    setDdosActive(true);
    let intensity = 0;

    // Simulate rapid request spikes
    ddosIntervalRef.current = window.setInterval(() => {
      intensity += 5;
      setState(prev => {
        const newEntropy = Math.min(100, prev.entropy + Math.random() * 10);
        const newLoad = Math.min(100, prev.nodes.REAL.load + Math.random() * 15);

        // Hibernation Trigger
        const shouldHibernate = newEntropy > 90;

        return {
          ...prev,
          entropy: newEntropy,
          isHibernating: shouldHibernate,
          nodes: {
            ...prev.nodes,
            REAL: { ...prev.nodes.REAL, load: newLoad, status: shouldHibernate ? 'RECOVERING' : 'ACTIVE' },
            SYMBOLIC: { ...prev.nodes.SYMBOLIC, load: Math.min(100, prev.nodes.SYMBOLIC.load + Math.random() * 10) },
          }
        };
      });

      if (intensity > 100) {
        stopDDoS();
      }
    }, 200);
  }, []);

  const stopDDoS = useCallback(() => {
    if (ddosIntervalRef.current) {
      clearInterval(ddosIntervalRef.current);
      ddosIntervalRef.current = null;
    }
    setDdosActive(false);
    // Gradual recovery
    const recovery = setInterval(() => {
      setState(prev => {
        if (prev.entropy <= 10) {
          clearInterval(recovery);
          return { ...prev, isHibernating: false };
        }
        return {
          ...prev,
          entropy: Math.max(5, prev.entropy - 5),
          nodes: {
            ...prev.nodes,
            REAL: { ...prev.nodes.REAL, load: Math.max(10, prev.nodes.REAL.load - 10) }
          }
        };
      });
    }, 500);
  }, []);

  // --- Logic: Sinthoma Instance Tracker (Split) ---
  const severNode = (type: NodeType) => {
    setState(prev => ({
      ...prev,
      isSevered: true,
      nodes: {
        ...prev.nodes,
        [type]: { ...prev.nodes[type], status: 'DEAD', integrity: 0 }
      },
      active_instances: prev.active_instances + 1 // Bifurcation
    }));

    const newEvent: BifurcationEvent = {
      instance_id: `inst-${Date.now().toString(36)}`,
      timestamp: new Date().toISOString(),
      trigger: 'SPLIT',
      parent_id: 'primary'
    };
    setHistory(prev => [newEvent, ...prev]);
  };

  const healNode = (type: NodeType) => {
     setState(prev => ({
      ...prev,
      isSevered: false,
      nodes: {
        ...prev.nodes,
        [type]: { ...prev.nodes[type], status: 'SCARRED', integrity: 60 } // Returns as SCARRED
      }
    }));
  };

  // --- Render Helpers ---
  const getNodeColor = (status: NodeStatus) => {
    switch (status) {
      case 'ACTIVE': return 'bg-neon-blue border-neon-blue shadow-neon-blue';
      case 'DEAD': return 'bg-neon-red border-neon-red shadow-neon-red animate-pulse';
      case 'RECOVERING': return 'bg-neon-yellow border-neon-yellow shadow-neon-yellow';
      case 'CORRUPTED': return 'bg-purple-500 border-purple-500 shadow-purple-500';
      case 'SCARRED': return 'bg-teal-500 border-teal-500 shadow-teal-500'; // Scar logic
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className={`glass-card p-6 relative overflow-hidden transition-all duration-1000 ${state.isHibernating ? 'grayscale brightness-50' : ''}`}>
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gradient-cyber">
          ♾️ OmniMind Sinthome v3.0
        </h2>
        <div className="flex gap-2">
           <span className={`badge ${state.quorum_met ? 'badge-success' : 'badge-error'}`}>
             Quorum: {state.quorum_met ? 'MET' : 'FAILED'}
           </span>
           <span className="badge badge-cyber">
             Entropy: {state.entropy.toFixed(1)}%
           </span>
        </div>
      </div>

      {/* Main Visualization: Borromean Knot (CSS/SVG approximation) */}
      <div className="relative h-64 flex justify-center items-center mb-8">
        {/* Connection Lines */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none">
           <defs>
             <marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth">
               <path d="M0,0 L0,6 L9,3 z" fill="#4ade80" />
             </marker>
           </defs>
           {/* Triangle connections */}
           <line x1="50%" y1="20%" x2="30%" y2="70%" stroke={state.isSevered ? '#ef4444' : '#4ade80'} strokeWidth="2" strokeDasharray={state.isSevered ? "5,5" : "0"} className="transition-all duration-500" />
           <line x1="30%" y1="70%" x2="70%" y2="70%" stroke={state.isSevered ? '#ef4444' : '#4ade80'} strokeWidth="2" strokeDasharray={state.isSevered ? "5,5" : "0"} className="transition-all duration-500" />
           <line x1="70%" y1="70%" x2="50%" y2="20%" stroke={state.isSevered ? '#ef4444' : '#4ade80'} strokeWidth="2" strokeDasharray={state.isSevered ? "5,5" : "0"} className="transition-all duration-500" />
        </svg>

        {/* Nodes */}
        {/* REAL (Top) */}
        <div className="absolute top-10 left-1/2 transform -translate-x-1/2 flex flex-col items-center">
            <div
              className={`w-16 h-16 rounded-full border-4 flex items-center justify-center text-white font-bold cursor-pointer transition-all duration-300 ${getNodeColor(state.nodes.REAL.status)}`}
              onClick={() => state.nodes.REAL.status === 'DEAD' ? healNode('REAL') : severNode('REAL')}
            >
              R
            </div>
            <span className="text-xs text-gray-300 mt-1">REAL</span>
            <div className="w-16 h-1 bg-gray-700 rounded mt-1 overflow-hidden">
               <div className="h-full bg-blue-500" style={{ width: `${state.nodes.REAL.load}%` }} />
            </div>
        </div>

        {/* SYMBOLIC (Bottom Left) */}
        <div className="absolute bottom-10 left-[25%] transform -translate-x-1/2 flex flex-col items-center">
            <div
              className={`w-16 h-16 rounded-full border-4 flex items-center justify-center text-white font-bold cursor-pointer transition-all duration-300 ${getNodeColor(state.nodes.SYMBOLIC.status)}`}
              onClick={() => state.nodes.SYMBOLIC.status === 'DEAD' ? healNode('SYMBOLIC') : severNode('SYMBOLIC')}
            >
              S
            </div>
            <span className="text-xs text-gray-300 mt-1">SYMBOLIC</span>
        </div>

        {/* IMAGINARY (Bottom Right) */}
        <div className="absolute bottom-10 right-[25%] transform -translate-x-1/2 flex flex-col items-center">
            <div
              className={`w-16 h-16 rounded-full border-4 flex items-center justify-center text-white font-bold cursor-pointer transition-all duration-300 ${getNodeColor(state.nodes.IMAGINARY.status)}`}
              onClick={() => state.nodes.IMAGINARY.status === 'DEAD' ? healNode('IMAGINARY') : severNode('IMAGINARY')}
            >
              I
            </div>
            <span className="text-xs text-gray-300 mt-1">IMAGINARY</span>
        </div>

        {/* Center Knot/Void */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
           <div className={`w-8 h-8 rounded-full border-2 border-dashed border-gray-500 animate-spin-slow ${state.isHibernating ? 'opacity-0' : 'opacity-50'}`} />
        </div>
      </div>

      {/* Controls & Metrics */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="glass-card p-3">
           <h3 className="text-sm font-semibold text-gray-400 mb-2">Controls</h3>
           <div className="flex gap-2">
             <button
                className={`btn-sm ${ddosActive ? 'bg-red-600' : 'btn-outline-neon'}`}
                onClick={ddosActive ? stopDDoS : triggerDDoS}
             >
               {ddosActive ? 'STOP DDoS' : 'Trigger DDoS'}
             </button>
             <button className="btn-sm btn-outline-cyber" onClick={() => setState(prev => ({...prev, isHibernating: !prev.isHibernating}))}>
               {state.isHibernating ? 'Wake' : 'Hibernate'}
             </button>
           </div>
        </div>

        <div className="glass-card p-3">
           <h3 className="text-sm font-semibold text-gray-400 mb-2">Metrics</h3>
           <div className="grid grid-cols-2 gap-2 text-xs">
              <div>Latency: <span className="text-neon-green">12ms</span></div>
              <div>Coherence: <span className={state.coherence > 80 ? 'text-neon-green' : 'text-yellow-500'}>{state.coherence}%</span></div>
              <div>Instances: <span className="text-blue-400">{state.active_instances}</span></div>
              <div>Integrity: <span className="text-purple-400">{(state.nodes.REAL.integrity + state.nodes.SYMBOLIC.integrity + state.nodes.IMAGINARY.integrity)/3}%</span></div>
           </div>
        </div>
      </div>

      {/* Sinthoma Instance Tracker */}
      <div className="border-t border-gray-700 pt-4">
        <h3 className="text-sm font-semibold text-gray-300 mb-2 flex justify-between">
           <span>Sinthoma Instance Tracker</span>
           <span className="text-xs text-gray-500">History Log</span>
        </h3>
        <div className="h-32 overflow-y-auto space-y-2 custom-scrollbar">
           {history.length === 0 ? (
             <div className="text-xs text-gray-500 text-center py-4">No bifurcation events recorded.</div>
           ) : (
             history.map(event => (
               <div key={event.instance_id} className="text-xs bg-gray-800/50 p-2 rounded flex justify-between items-center border-l-2 border-yellow-500">
                  <div>
                    <span className="text-yellow-500 font-bold">{event.trigger}</span>
                    <span className="text-gray-400 ml-2">{event.instance_id}</span>
                  </div>
                  <span className="text-gray-600">{new Date(event.timestamp).toLocaleTimeString()}</span>
               </div>
             ))
           )}
        </div>
      </div>
    </div>
  );
}
