import React from 'react';
import { Network, Server, User, ShieldAlert } from 'lucide-react';

export const TopologyGraph: React.FC = () => {
  return (
    <div className="relative h-72 w-full bg-slate-950/60 rounded-xl border border-slate-800 p-4 flex flex-col justify-between overflow-hidden">
      <div className="flex items-center justify-between z-10">
        <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
          <Network size={14} className="text-blue-400" />
          <span>IN-MEMORY STREAMING GRAPH TOPOLOGY</span>
        </div>
        <span className="text-[11px] text-amber-400 font-mono bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/30">
          3 Network Hops Detected
        </span>
      </div>

      {/* Simulated Topology Graph Representation */}
      <div className="relative my-auto flex items-center justify-around px-8 z-10">
        <div className="flex flex-col items-center gap-2">
          <div className="w-12 h-12 rounded-full bg-blue-600/20 border-2 border-blue-500 flex items-center justify-center text-blue-400 shadow-lg shadow-blue-500/20">
            <User size={20} />
          </div>
          <span className="text-xs font-mono text-slate-300">usr-9982</span>
          <span className="text-[10px] text-slate-500">Normal Domain</span>
        </div>

        <div className="h-0.5 w-20 bg-gradient-to-r from-blue-500 to-amber-500 relative">
          <div className="absolute -top-3 left-1/2 -translate-x-1/2 text-[9px] font-mono text-amber-400">Hop 1</div>
        </div>

        <div className="flex flex-col items-center gap-2">
          <div className="w-12 h-12 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300">
            <Server size={20} />
          </div>
          <span className="text-xs font-mono text-slate-300">Auth-Gateway</span>
          <span className="text-[10px] text-slate-500">Hop Node</span>
        </div>

        <div className="h-0.5 w-20 bg-gradient-to-r from-amber-500 to-red-500 relative">
          <div className="absolute -top-3 left-1/2 -translate-x-1/2 text-[9px] font-mono text-red-400">Hop 2</div>
        </div>

        <div className="flex flex-col items-center gap-2">
          <div className="w-14 h-14 rounded-full bg-red-600/20 border-2 border-red-500 flex items-center justify-center text-red-400 animate-pulse shadow-lg shadow-red-500/30">
            <ShieldAlert size={24} />
          </div>
          <span className="text-xs font-mono text-red-400 font-bold">HR_Database</span>
          <span className="text-[10px] text-red-400">Isolated Target</span>
        </div>
      </div>

      <div className="text-xs text-slate-500 font-mono text-center z-10">
        Lateral Movement Risk Score: <span className="text-red-400 font-bold">0.95 (High Anomaly)</span>
      </div>
    </div>
  );
};
