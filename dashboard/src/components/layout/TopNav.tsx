import React from 'react';
import { Bell, Search, Radio, User, X } from 'lucide-react';
import { useAlertStore } from '@/store/useAlertStore';

export const TopNav: React.FC = () => {
  const { globalSearchQuery, setGlobalSearchQuery } = useAlertStore();

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-950/80 backdrop-blur px-6 flex items-center justify-between sticky top-0 z-40">
      <div className="flex items-center gap-4 w-96">
        <div className="relative w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
          <input
            type="text"
            value={globalSearchQuery}
            onChange={(e) => setGlobalSearchQuery(e.target.value)}
            placeholder="Search users, IPs, event IDs..."
            className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-8 py-1.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50"
          />
          {globalSearchQuery && (
            <button
              onClick={() => setGlobalSearchQuery('')}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300"
            >
              <X size={14} />
            </button>
          )}
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-full text-xs font-mono text-emerald-400">
          <Radio size={14} className="animate-pulse text-emerald-400" />
          <span>REALTIME STREAM ACTIVE</span>
        </div>

        <div className="relative cursor-pointer text-slate-400 hover:text-slate-200">
          <Bell size={20} />
          <span className="absolute -top-1 -right-1 w-2 h-2 bg-cyan-500 rounded-full animate-ping" />
        </div>

        <div className="flex items-center gap-3 pl-4 border-l border-slate-800">
          <div className="w-8 h-8 rounded-full bg-cyan-600/20 border border-cyan-500/40 flex items-center justify-center text-cyan-400">
            <User size={16} />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-200">SOC Analyst Lead</p>
            <p className="text-[10px] text-slate-500">Tier-3 Analyst</p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default TopNav;
