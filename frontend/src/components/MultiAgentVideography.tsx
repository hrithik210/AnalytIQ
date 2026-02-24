import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function MultiAgentVideography({ onComplete }: { onComplete: () => void }) {
  const [scene, setScene] = useState<0 | 1 | 2 | 3>(0);

  useEffect(() => {
    // Extended pacing by an additional 7s as requested
    const s1 = setTimeout(() => setScene(1), 5200); // The Purge triggers (Hold Oldies + 2s)
    const s2 = setTimeout(() => setScene(2), 7600); // The Agents assemble (+ 2s)
    const s3 = setTimeout(() => setScene(3), 10600); // The Reveal (+ 2.5s)
    const s4 = setTimeout(() => {
      onComplete();
    }, 16500); // Transition out to Hero (Hold Reveal + 2.5s)

    return () => {
      clearTimeout(s1);
      clearTimeout(s2);
      clearTimeout(s3);
      clearTimeout(s4);
    };
  }, [onComplete]);

  return (
    // Added -mt-48 to shift the entire videography upward into the middle/upper half of the screen
    <div className="absolute inset-0 z-50 flex items-center justify-center bg-[#2B2B2B] overflow-hidden -mt-48">
      {/* 
        ========================================
        SCENE 0: THE OLDIES (Legacy BI Tools)
        ========================================
      */}
      <AnimatePresence>
        {scene === 0 && (
          <motion.div
            key="oldies"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ 
              opacity: 0,
              filter: "blur(20px)",
              scale: 0.9,
              transition: { duration: 0.4, ease: "circIn" }
            }}
            className="flex flex-col items-center justify-center gap-8"
          >
            {/* Clear Text Label so users know what they are looking at */}
            <motion.h3 
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bricolage text-2xl font-semibold text-[#B3B3B3] uppercase tracking-[0.2em]"
            >
              Legacy Dashboards
            </motion.h3>

            <div className="relative flex w-full max-w-4xl flex-wrap justify-center gap-4">
              {/* Box 1 */}
              <motion.div
                initial={{ x: -20, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ delay: 0.4 }}
                className="h-32 w-48 rounded-md border border-dashed border-[#D4D4D4]/30 bg-[#2B2B2B] flex flex-col justify-end p-4 gap-2"
              >
                <div className="h-2 w-full bg-[#B3B3B3]/20 animate-pulse rounded" />
                <div className="h-8 w-full bg-[#D4D4D4]/10 rounded" />
                <div className="text-[10px] text-[#B3B3B3] font-mono">Loading data model...</div>
              </motion.div>

              {/* Box 2 */}
              <motion.div
                initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.6 }}
                className="h-48 w-64 rounded-md border border-solid border-[#D4D4D4]/40 bg-[#2B2B2B] flex flex-col p-4 gap-3 shadow-sm"
              >
                <div className="h-4 w-1/2 bg-[#B3B3B3]/20 rounded" />
                <div className="flex-1 flex items-end gap-2">
                  <div className="h-3/4 w-8 bg-[#D4D4D4]/20 rounded-t" />
                  <div className="h-1/2 w-8 bg-[#D4D4D4]/20 rounded-t" />
                  <div className="h-full w-8 bg-[#D4D4D4]/20 rounded-t" />
                </div>
                <div className="text-[10px] text-[#B3B3B3] font-mono text-center">Sync Error 504.</div>
              </motion.div>

              {/* Box 3 */}
              <motion.div
                initial={{ x: 20, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ delay: 0.8 }}
                className="h-40 w-56 rounded-md border border-solid border-[#D4D4D4]/50 bg-[#2B2B2B] flex items-center justify-center -rotate-2"
              >
                 <motion.div 
                   animate={{ rotate: 360 }} 
                   transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                   className="h-8 w-8 rounded-full border-2 border-t-[#FFFFFF] border-r-transparent border-b-transparent border-l-transparent"
                 />
                 <div className="ml-3 text-[10px] text-[#B3B3B3] font-mono">Stuck...</div>
              </motion.div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 
        ========================================
        SCENE 1: THE PURGE (Scanner Sweep)
        ========================================
      */}
      <AnimatePresence>
        {scene === 1 && (
          <motion.div
            key="purge"
            initial={{ height: "2px", width: 0, opacity: 1 }}
            animate={{ width: "100vw" }}
            exit={{ opacity: 0, transition: { duration: 0.1 } }}
            transition={{ duration: 0.6, ease: "circOut" }}
            className="absolute bg-[#FFFFFF] shadow-[0_0_40px_10px_rgba(255,255,255,0.2)]"
          />
        )}
      </AnimatePresence>

      {/* 
        ========================================
        SCENE 2: THE SWARM (Multi-Agent Engine)
        ========================================
      */}
      <AnimatePresence>
        {(scene === 2 || scene === 3) && (
          <motion.div
            key="swarm"
            initial={{ scale: 0 }}
            animate={{ scale: scene === 3 ? 0.35 : 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 1.2, ease: "circOut" }}
            className={`absolute flex h-64 w-64 items-center justify-center ${scene === 3 ? 'top-[-80px]' : ''}`}
          >
            {/* Core Nucleus */}
            <motion.div 
              initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
              className="absolute h-16 w-16 rounded-full bg-[#FFFFFF] shadow-[0_0_60px_-10px_rgba(255,255,255,0.4)] z-20 flex items-center justify-center"
            >
              <div className="h-6 w-6 rounded-full bg-[#2B2B2B]" />
            </motion.div>

            {/* Orbiting Agent Nodes */}
            {[0, 1, 2, 3].map((i) => (
              <motion.div
                key={`agent-${i}`}
                initial={{ opacity: 0, radius: 0 }}
                animate={{ opacity: 1, rotate: 360 }}
                transition={{ 
                  opacity: { delay: 0.4 + i * 0.1 },
                  rotate: { repeat: Infinity, duration: 6, ease: "linear", delay: i * 1.5 }
                }}
                className="absolute h-[240px] w-[240px] border border-dashed border-[#D4D4D4]/30 rounded-full"
                style={{ originX: 0.5, originY: 0.5 }}
              >
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 h-8 w-24 rounded-full bg-[#FFFFFF] text-[#2B2B2B] flex items-center justify-center text-[10px] font-bold tracking-widest uppercase">
                  Agent {i + 1}
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* 
        ========================================
        SCENE 3: THE REVEAL (Typography Lock)
        ========================================
      */}
      <AnimatePresence>
        {scene === 3 && (
          <motion.div
            key="reveal"
            className="flex flex-col items-center text-center mt-32 px-4"
          >
            <motion.h2 
              initial={{ y: 40, opacity: 0, filter: "blur(10px)" }}
              animate={{ y: 0, opacity: 1, filter: "blur(0px)" }}
              exit={{ opacity: 0, scale: 1.05 }}
              transition={{ duration: 0.8, ease: "backOut" }}
              className="bricolage text-4xl md:text-6xl lg:text-7xl font-semibold text-[#FFFFFF] tracking-tight text-balance"
            >
              AnalytIQ:<br/>
              A multi-agent system<br/>
            </motion.h2>
            
            <motion.p
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.8, delay: 0.3, ease: "circOut" }}
              className="mt-6 text-xl md:text-3xl text-[#D4D4D4] font-medium tracking-wide"
            >
              designed to replace the oldies.
            </motion.p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
