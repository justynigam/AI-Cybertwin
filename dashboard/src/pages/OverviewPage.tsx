import React from 'react';
import { ShieldAlert, Activity, UserCheck, Network, Zap } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { RiskTimelineChart } from '../components/charts/RiskTimelineChart';

export const OverviewPage: React.FC = () => {
  return (
    <div className="p-6 bg-slate-950 min-h-screen text-slate-50 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">SOC Executive Overview</h1>
          <p className="text-sm text-slate-400 mt-1">Real-time Autonomous Threat Fusion & Behavioral Digital Twins</p>
        </div>
        <Badge variant="outline" className="text-emerald-400 border-emerald-500/40 bg-emerald-500/10">
          ALL AI MODELS OPERATIONAL
        </Badge>
      </div>

      {/* KPI Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 font-bold uppercase">Total Events Analyzed</p>
              <p className="text-2xl font-mono font-bold text-slate-100 mt-1">2,561</p>
            </div>
            <div className="p-3 rounded-full bg-blue-500/10 text-blue-400">
              <Activity size={24} />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 font-bold uppercase">Active Anomaly Threats</p>
              <p className="text-2xl font-mono font-bold text-red-500 mt-1">12</p>
            </div>
            <div className="p-3 rounded-full bg-red-500/10 text-red-500">
              <ShieldAlert size={24} />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 font-bold uppercase">Behavioral Digital Twins</p>
              <p className="text-2xl font-mono font-bold text-indigo-400 mt-1">500</p>
            </div>
            <div className="p-3 rounded-full bg-indigo-500/10 text-indigo-400">
              <UserCheck size={24} />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 font-bold uppercase">Tri-Model Consensus</p>
              <p className="text-2xl font-mono font-bold text-emerald-400 mt-1">99.4%</p>
            </div>
            <div className="p-3 rounded-full bg-emerald-500/10 text-emerald-400">
              <Zap size={24} />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Chart Section */}
      <Card className="bg-slate-900 border-slate-800">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-mono text-slate-300">Live Enterprise Risk Score Timeline</CardTitle>
        </CardHeader>
        <CardContent>
          <RiskTimelineChart />
        </CardContent>
      </Card>
    </div>
  );
};
