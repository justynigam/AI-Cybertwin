import React from 'react';
import { UserCheck, Shield, Clock, Terminal, CheckCircle2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export const EntityProfilePage: React.FC = () => {
  return (
    <div className="p-6 bg-slate-950 min-h-screen text-slate-50 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-400">
            <UserCheck size={24} />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-100">Behavioral Digital Twin Profile</h1>
            <p className="text-xs font-mono text-slate-400">Entity: usr-9982 (Senior Systems Engineer)</p>
          </div>
        </div>
        <Badge className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
          BASELINE FIT: 98.2%
        </Badge>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader>
            <CardTitle className="text-sm font-mono text-slate-300">Learned Behavioral Baselines</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-xs font-mono">
            <div className="flex items-center justify-between p-2.5 rounded bg-slate-950 border border-slate-800">
              <span className="text-slate-400">Typical Working Hours:</span>
              <span className="text-slate-200">08:30 - 18:00 UTC</span>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded bg-slate-950 border border-slate-800">
              <span className="text-slate-400">Primary IP Range:</span>
              <span className="text-slate-200">198.51.100.0/24 (Home Office)</span>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded bg-slate-950 border border-slate-800">
              <span className="text-slate-400">Primary Device:</span>
              <span className="text-slate-200">macOS-M2-MacBookPro (dev-4410)</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardHeader>
            <CardTitle className="text-sm font-mono text-blue-400 flex items-center gap-2">
              <Terminal size={16} /> Autoregressive Next-State Model
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-xs font-mono">
            <p className="text-slate-400">Recent Sequence History:</p>
            <div className="p-3 rounded bg-slate-950 border border-slate-800 text-blue-400">
              [LOGIN_SUCCESS] ➔ [Access_Shared_Drive] ➔ [Download_Large_File]
            </div>
            <p className="text-slate-400 pt-2">Model Forecast:</p>
            <div className="p-3 rounded bg-slate-950 border border-slate-800 text-amber-400 flex items-center justify-between">
              <span>Predicted Action: Access_HR_Database</span>
              <span>82.0% confidence</span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
