import React from 'react';
import { Shield, Activity, Network, UserCheck, Settings, AlertTriangle } from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: Shield },
    { id: 'alerts', label: 'Threat Feed', icon: Activity },
    { id: 'detail', label: 'War Room (XAI)', icon: AlertTriangle },
    { id: 'entities', label: 'Behavioral Twins', icon: UserCheck },
    { id: 'network', label: 'Graph Topology', icon: Network },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between p-4 h-screen sticky top-0">
      <div>
        <div className="flex items-center gap-3 px-3 py-4 mb-6 border-b border-slate-800">
          <div className="p-2 rounded-lg bg-gradient-to-tr from-cyan-600 to-indigo-500 text-white shadow-lg shadow-cyan-500/20">
            <Shield size={24} />
          </div>
          <div>
            <h2 className="font-bold text-lg text-slate-100 tracking-tight">CyberTwin AI</h2>
            <p className="text-xs text-cyan-400 font-mono">SOC Defense v2.4</p>
          </div>
        </div>

        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-cyan-600/10 text-cyan-400 border border-cyan-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      <div className="pt-4 border-t border-slate-800">
        <button 
          onClick={() => setActiveTab('settings')}
          className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
            activeTab === 'settings'
              ? 'bg-cyan-600/10 text-cyan-400 border border-cyan-500/30'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <Settings size={18} />
          <span>System Settings</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
