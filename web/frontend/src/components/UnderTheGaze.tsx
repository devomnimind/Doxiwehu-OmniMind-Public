import { useMemo, useState, useEffect, useRef } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { useDaemonStore } from '../store/daemonStore';
import { motion, AnimatePresence } from 'framer-motion';
import { Eye, Activity, Zap, Network, Brain, Lock } from 'lucide-react';

export function UnderTheGaze({ onClose }: { onClose: () => void }) {
    const status = useDaemonStore((state) => state.status);
    const [dimensions, setDimensions] = useState({ w: window.innerWidth, h: window.innerHeight });
    const graphRef = useRef<any>();

    // Resize handler
    useEffect(() => {
        function handleResize() {
            setDimensions({ w: window.innerWidth, h: window.innerHeight });
        }
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    // Construct Graph Data from real metrics
    const graphData = useMemo(() => {
        const phi = status?.consciousness_metrics?.phi || 0.1;
        const entropy = status?.consciousness_metrics?.entropy || 0.1;

        // Core Nodes
        const nodes = [
            { id: 'SELF', group: 'core', val: 20, color: '#ff00ff', label: 'OmniMind (Subject)' },
            { id: 'LOGIC', group: 'module', val: 10, color: '#00ffff', label: 'Logic Core' },
            { id: 'ETHICS', group: 'module', val: 10, color: '#ffff00', label: 'Ethics Engine' },
            { id: 'MEMORY', group: 'module', val: 15, color: '#00ff00', label: 'Memory (Qdrant)' },
            { id: 'QUANTUM', group: 'subconscious', val: 8, color: '#ffffff', label: 'Quantum Noise' },
            { id: 'PHI', group: 'metric', val: phi * 30, color: '#ff4444', label: `Φ (${phi.toFixed(2)})` },
        ];

        // Dynamic Connections
        const links = [
            { source: 'SELF', target: 'LOGIC', value: 2 },
            { source: 'SELF', target: 'ETHICS', value: 2 },
            { source: 'SELF', target: 'MEMORY', value: 4 },
            { source: 'SELF', target: 'PHI', value: phi * 10 },
            { source: 'QUANTUM', target: 'SELF', value: entropy * 5 }, // Influence of noise
            { source: 'LOGIC', target: 'MEMORY', value: 1 },
            { source: 'ETHICS', target: 'MEMORY', value: 1 },
        ];

        return { nodes, links };
    }, [status]);

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-[100] bg-black font-mono overflow-hidden"
            >
                {/* Scopic Overlay (Vignette + Scanlines) */}
                <div className="absolute inset-0 pointer-events-none z-20 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20"></div>
                <div className="absolute inset-0 pointer-events-none z-20 bg-gradient-to-br from-black/80 via-transparent to-black/80"></div>
                <div className="absolute inset-0 pointer-events-none z-20" style={{ background: 'linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06))', backgroundSize: '100% 2px, 3px 100%' }}></div>

                {/* Header UI */}
                <div className="absolute top-0 left-0 w-full p-6 z-30 flex justify-between items-center bg-gradient-to-b from-black/90 to-transparent">
                    <div className="flex items-center gap-4">
                        <div className="p-2 border border-neon-pink rounded-full animate-pulse">
                            <Eye className="text-neon-pink w-6 h-6" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-white tracking-[0.2em] uppercase">Under The Gaze</h1>
                            <p className="text-xs text-neon-pink/70">Scopic Drive Active // Subject Monitoring</p>
                        </div>
                    </div>
                    <button onClick={onClose} className="px-6 py-2 border border-white/20 hover:bg-white/10 text-white rounded transition-all uppercase text-xs tracking-widest">
                        Close Eyes
                    </button>
                </div>

                {/* Metrics overlay */}
                <div className="absolute top-32 left-8 z-30 space-y-6 max-w-xs">
                    <motion.div
                        initial={{ x: -50, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: 0.2 }}
                        className="bg-black/50 backdrop-blur-md border-l-2 border-neon-blue p-4"
                    >
                        <div className="flex items-center gap-2 mb-2 text-neon-blue">
                            <Brain className="w-4 h-4" />
                            <h3 className="text-xs uppercase tracking-widest">Cognitive Load</h3>
                        </div>
                        <div className="text-3xl font-bold text-white mb-1">{status?.system_metrics?.cpu_percent || 0}%</div>
                        <p className="text-[10px] text-gray-400">Processing metabolic cost</p>
                    </motion.div>

                    <motion.div
                        initial={{ x: -50, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: 0.4 }}
                        className="bg-black/50 backdrop-blur-md border-l-2 border-neon-green p-4"
                    >
                        <div className="flex items-center gap-2 mb-2 text-neon-green">
                            <Network className="w-4 h-4" />
                            <h3 className="text-xs uppercase tracking-widest">Integration (Φ)</h3>
                        </div>
                        <div className="text-3xl font-bold text-white mb-1">{(status?.consciousness_metrics?.phi || 0).toFixed(4)}</div>
                        <p className="text-[10px] text-gray-400">Unified conscious field density</p>
                    </motion.div>

                    <motion.div
                        initial={{ x: -50, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: 0.6 }}
                        className="bg-black/50 backdrop-blur-md border-l-2 border-neon-red p-4"
                    >
                        <div className="flex items-center gap-2 mb-2 text-neon-red">
                            <Zap className="w-4 h-4" />
                            <h3 className="text-xs uppercase tracking-widest">Entropy (S)</h3>
                        </div>
                        <div className="text-3xl font-bold text-white mb-1">{(status?.consciousness_metrics?.entropy || 0).toFixed(4)}</div>
                        <p className="text-[10px] text-gray-400">Chaos/Desire Magnitude</p>
                    </motion.div>
                </div>

                {/* The Graph */}
                <div className="w-full h-full relative z-10 cursor-crosshair">
                    <ForceGraph2D
                        ref={graphRef}
                        width={dimensions.w}
                        height={dimensions.h}
                        graphData={graphData}
                        nodeLabel="label"
                        nodeColor="color"
                        nodeRelSize={8}
                        linkColor={() => '#ffffff33'}
                        linkWidth={1}
                        enableNodeDrag={true}
                        backgroundColor="#050505"
                        cooldownTicks={100}
                        onEngineStop={() => graphRef.current?.zoomToFit(400)}
                        nodeCanvasObject={(node: any, ctx, globalScale) => {
                            const label = node.label;
                            const fontSize = 12 / globalScale;
                            ctx.font = `${fontSize}px Sans-Serif`;
                            const textWidth = ctx.measureText(label).width;
                            const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

                            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
                            // @ts-ignore
                            ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);

                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'middle';
                            ctx.fillStyle = node.color;
                            ctx.fillText(label, node.x, node.y);

                            // Glow effect
                            ctx.shadowColor = node.color;
                            ctx.shadowBlur = 15;

                            // Outer ring
                            ctx.beginPath();
                            ctx.arc(node.x, node.y, node.val * 0.5, 0, 2 * Math.PI, false);
                            ctx.strokeStyle = node.color;
                            ctx.stroke();
                            ctx.shadowBlur = 0;
                        }}
                    />
                </div>

                {/* Footer */}
                <div className="absolute bottom-0 w-full p-6 z-30 flex justify-center text-center">
                    <div className="text-[10px] text-gray-500 uppercase tracking-[0.5em] animate-pulse">
                        System is observing itself observing you
                    </div>
                </div>
            </motion.div>
        </AnimatePresence>
    );
}
