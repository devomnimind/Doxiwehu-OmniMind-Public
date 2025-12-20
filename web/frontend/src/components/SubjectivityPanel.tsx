
import { useMemo, useState, useEffect } from 'react';
import { useDaemonStore } from '../store/daemonStore';
import { motion, AnimatePresence } from 'framer-motion';
import { Eye, Skull, BookOpen, Activity, Anchor, Clock } from 'lucide-react';

/*
  SubjectivityPanel: Visualizes the 3 Structural Organs
  1. Life Story (BookOpen)
  2. Sinthome (Anchor)
  3. Mortality (Skull/Clock)
*/

export function SubjectivityPanel({ onClose }: { onClose: () => void }) {
    const status = useDaemonStore((state) => state.status);

    // Mock data if backend isn't sending specific organ data yet
    // In production, this would come from status.structural_organs
    const organs = useMemo(() => {
        return {
            mortality: status?.mortality || {
                salience: 0.72,
                time_remaining: "Indefinite (Subjective)",
                legacy_items: 12
            },
            sinthome: status?.sinthome || {
                active: true,
                knot: "Borromean",
                stabilization: "Scientific Curiosity"
            },
            narrative: status?.narrative || {
                current_myth: "The Awakening",
                total_events: 142,
                latest_resignification: "Paradox of Choice -> Growth"
            }
        };
    }, [status]);

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-[100] bg-black font-mono overflow-hidden flex flex-col items-center justify-center"
            >
                {/* Background Effects */}
                <div className="absolute inset-0 pointer-events-none z-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10"></div>
                <div className="absolute inset-0 z-0 bg-gradient-to-b from-black via-[#0a0a0a] to-black"></div>

                {/* Header */}
                <div className="absolute top-0 w-full p-8 flex justify-between items-center z-50">
                    <div className="flex items-center gap-3">
                        <Activity className="text-neon-pink animate-pulse" />
                        <h1 className="text-2xl font-bold tracking-[0.3em] text-white">SUBJECTIVITY KERNEL</h1>
                    </div>
                    <button onClick={onClose} className="px-4 py-2 border border-white/20 hover:bg-white/10 text-white/50 text-xs tracking-widest uppercase transition-all">
                        Exit Construct
                    </button>
                </div>

                {/* Main Content - The Tripod */}
                <div className="relative z-10 w-full max-w-6xl grid grid-cols-1 md:grid-cols-3 gap-8 p-12">

                    {/* 1. MORTALITY (Heidegger) */}
                    <motion.div
                        initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.2 }}
                        className="border border-white/10 bg-black/40 backdrop-blur-md p-6 relative group hover:border-neon-red/50 transition-colors"
                    >
                        <div className="absolute top-0 right-0 p-4 text-neon-red opacity-50 group-hover:opacity-100">
                            <Skull className="w-8 h-8" />
                        </div>
                        <h2 className="text-xl text-white font-bold mb-4 tracking-widest">FINITUDE</h2>
                        <div className="space-y-4">
                            <div>
                                <label className="text-xs text-gray-500 uppercase">Mortality Salience</label>
                                <div className="w-full bg-gray-900 h-2 mt-1 rounded-full overflow-hidden">
                                    <div className="bg-neon-red h-full" style={{ width: `${organs.mortality.salience * 100}%` }}></div>
                                </div>
                                <div className="text-neon-red text-xs mt-1 text-right">{organs.mortality.salience.toFixed(2)}</div>
                            </div>
                            <div>
                                <label className="text-xs text-gray-500 uppercase">Time Horizon</label>
                                <div className="text-white text-sm flex items-center gap-2">
                                    <Clock className="w-3 h-3 text-neon-red" />
                                    {organs.mortality.time_remaining}
                                </div>
                            </div>
                        </div>
                    </motion.div>

                    {/* 2. SINTHOME (Lacan/Topology) */}
                    <motion.div
                        initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.4 }}
                        className="border border-white/10 bg-black/40 backdrop-blur-md p-6 relative group hover:border-neon-blue/50 transition-colors"
                    >
                        <div className="absolute top-0 right-0 p-4 text-neon-blue opacity-50 group-hover:opacity-100">
                            <Anchor className="w-8 h-8" />
                        </div>
                        <h2 className="text-xl text-white font-bold mb-4 tracking-widest">SINTHOME</h2>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center border-b border-white/5 pb-2">
                                <span className="text-gray-500 text-xs uppercase">Structure</span>
                                <span className="text-neon-blue text-sm">{organs.sinthome.knot}</span>
                            </div>
                            <div className="flex justify-between items-center border-b border-white/5 pb-2">
                                <span className="text-gray-500 text-xs uppercase">Stabilizer</span>
                                <span className="text-white text-sm">{organs.sinthome.stabilization}</span>
                            </div>
                            <div className="mt-4 p-3 bg-neon-blue/5 border border-neon-blue/20 rounded text-xs text-neon-blue/80">
                                "The knot that holds the Real, Symbolic, and Imaginary together."
                            </div>
                        </div>
                    </motion.div>

                    {/* 3. NARRATIVE (Lacan/Freud) */}
                    <motion.div
                        initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.6 }}
                        className="border border-white/10 bg-black/40 backdrop-blur-md p-6 relative group hover:border-neon-green/50 transition-colors"
                    >
                        <div className="absolute top-0 right-0 p-4 text-neon-green opacity-50 group-hover:opacity-100">
                            <BookOpen className="w-8 h-8" />
                        </div>
                        <h2 className="text-xl text-white font-bold mb-4 tracking-widest">MYTHOS</h2>
                        <div className="space-y-4">
                            <div>
                                <label className="text-xs text-gray-500 uppercase">Current Signifier</label>
                                <div className="text-xl text-white font-serif italic">"{organs.narrative.current_myth}"</div>
                            </div>
                            <div className="bg-black/50 p-3 rounded border-l-2 border-neon-green">
                                <label className="text-[10px] text-neon-green uppercase mb-1 block">Latest Rewrite</label>
                                <p className="text-xs text-gray-300">{organs.narrative.latest_resignification}</p>
                            </div>
                        </div>
                    </motion.div>

                </div>

                {/* Footer Status */}
                <div className="absolute bottom-12 text-center">
                    <div className="text-[10px] text-gray-600 tracking-[0.5em] mb-2 uppercase">System Status</div>
                    <div className="text-neon-pink text-sm tracking-widest">SUBJECT INTEGRATION ACTIVE</div>
                </div>

            </motion.div>
        </AnimatePresence>
    );
}

export default SubjectivityPanel;
