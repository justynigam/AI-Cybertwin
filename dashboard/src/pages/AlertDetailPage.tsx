import React, { useState } from 'react';
import { useAlertStore } from '../store/useAlertStore';
import { ShieldAlert, Zap, Cpu, Network, CheckCircle, AlertOctagon, Terminal } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { TopologyGraph } from '../components/charts/TopologyGraph';

export const AlertDetailPage: React.FC = () => {
  const { selectedAlert, alerts } = useAlertStore();
  const alert = selectedAlert || alerts[0];
  const [remediationStatus, setRemediationStatus] = useState<string | null>(null);

  if (!alert) {
    return (
      <div className="p-12 text-center text-slate-400 space-y-4 bg-slate-950 min-h-screen">
        <ShieldAlert className="h-12 w-12 mx-auto text-amber-500 opacity-80" />
        <h2 className="text-xl font-bold text-slate-200">Awaiting Live Security Threat Event</h2>
        <p className="text-sm text-slate-400 max-w-md mx-auto">
          No active breach loaded. Click the <span className="text-red-400 font-semibold">"🔴 Red Team Attack Simulator"</span> button on the top navigation bar during your demonstration to trigger a live breach simulation!
        </p>
      </div>
    );
  }

  const handleExecuteAction = (actionId: string) => {
    setRemediationStatus(`Executing ${actionId}...`);
    setTimeout(() => {
      setRemediationStatus(`Successfully applied ${actionId} to ${alert.user_id || 'Target User'}`);
    }, 1000);
  };

  return (
    <div className="p-6 bg-slate-950 min-h-screen text-slate-50 space-y-6">
      {/* Header Banner */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-3">
            <Badge className="bg-red-600 text-white font-mono">{alert.severity}</Badge>
            <h1 className="text-2xl font-bold text-slate-100">{alert.attack_category} Threat War Room</h1>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-1">Alert ID: {alert.id} | User: {alert.user_id} | Device: {alert.device_id}</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-400 uppercase font-bold">Fused Master Risk</p>
          <p className="text-3xl font-mono font-bold text-red-500">{(alert.master_risk_score * 100).toFixed(1)}%</p>
        </div>
      </div>

      {/* XAI Natural Language Explanation Card */}
      <Card className="bg-gradient-to-r from-red-950/40 via-slate-900 to-slate-900 border-red-500/30">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-mono text-red-400 flex items-center gap-2">
            <Zap size={16} /> NATURAL LANGUAGE XAI INCIDENT REPORT
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg font-medium text-slate-100 italic">
            "{alert.nlp_explanation || 'This event was flagged due to impossible travel speed between geographical locations combined with accessing a sensitive resource for the first time.'}"
          </p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Model Sub-Scores & SHAP Explainability */}
        <div className="lg:col-span-2 space-y-6">
          <div className="grid grid-cols-3 gap-4">
            <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-4">
                <p className="text-xs text-slate-400 font-mono flex items-center gap-1"><Cpu size={14} /> Autoencoder MSE</p>
                <p className="text-2xl font-bold font-mono text-slate-200 mt-1">0.85</p>
                <p className="text-[10px] text-slate-500 mt-1">Point-in-time Anomaly</p>
              </CardContent>
            </Card>

            <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-4">
                <p className="text-xs text-slate-400 font-mono flex items-center gap-1"><Zap size={14} /> Transformer Seq</p>
                <p className="text-2xl font-bold font-mono text-slate-200 mt-1">0.92</p>
                <p className="text-[10px] text-slate-500 mt-1">APT Temporal Sequence</p>
              </CardContent>
            </Card>

            <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-4">
                <p className="text-xs text-slate-400 font-mono flex items-center gap-1"><Network size={14} /> Graph Hop Risk</p>
                <p className="text-2xl font-bold font-mono text-slate-200 mt-1">0.88</p>
                <p className="text-[10px] text-slate-500 mt-1">3-Hop Lateral Move</p>
              </CardContent>
            </Card>
          </div>

          {/* SHAP Feature Impact Chart */}
          <Card className="bg-slate-900 border-slate-800">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-semibold text-slate-300">SHAP Feature Contributions (Risk Attribution)</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {(alert.shap_features || [
                { feature: 'velocity_kmh', contribution: 0.48 },
                { feature: 'is_new_resource', contribution: 0.32 },
                { feature: 'hour_sin', contribution: 0.15 }
              ]).map((item, idx) => (
                <div key={idx} className="space-y-1">
                  <div className="flex justify-between text-xs font-mono">
                    <span className="text-slate-300">{item.feature}</span>
                    <span className="text-red-400 font-bold">+{(item.contribution * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-slate-950 rounded-full h-2">
                    <div 
                      className="bg-gradient-to-r from-orange-500 to-red-600 h-2 rounded-full" 
                      style={{ width: `${Math.min(item.contribution * 100, 100)}%` }} 
                    />
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* 3-Hop Graph Topology Visualizer */}
          <Card className="bg-slate-900 border-slate-800">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-semibold text-slate-300 flex items-center justify-between">
                <span className="flex items-center gap-2"><Network size={16} /> IN-MEMORY STREAMING GRAPH TOPOLOGY</span>
                <Badge variant="outline" className="text-xs text-amber-400 border-amber-500/40">3 Network Hops Detected</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <TopologyGraph />
            </CardContent>
          </Card>
        </div>

        {/* Behavioral Digital Twin & Playbooks Panel */}
        <div className="space-y-6">
          {/* Next-Move Forecaster */}
          <Card className="bg-slate-900 border-slate-800">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs font-mono text-cyan-400 flex items-center gap-2">
                <Terminal size={14} /> BEHAVIORAL TWIN NEXT-MOVE FORECAST
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {(alert.twin_predictions || [
                { predicted_action: 'Access_HR_Database', probability_score: 0.82, rank: 1 },
                { predicted_action: 'Execute_PowerShell', probability_score: 0.12, rank: 2 },
                { predicted_action: 'Clear_Event_Logs', probability_score: 0.04, rank: 3 }
              ]).map((pred, idx) => (
                <div key={idx} className="p-2.5 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold text-slate-200">#{pred.rank} {pred.predicted_action}</p>
                    <p className="text-[10px] text-slate-500">Predicted Attacker Trajectory</p>
                  </div>
                  <Badge className="bg-blue-600/20 text-blue-400 border-blue-500/30 font-mono text-xs">
                    {(pred.probability_score * 100).toFixed(0)}% prob
                  </Badge>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* AI Security Advisor SOAR Playbooks */}
          <Card className="bg-slate-900 border-slate-800">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs font-mono text-emerald-400 flex items-center gap-2">
                <AlertOctagon size={14} /> AI SECURITY ADVISOR PLAYBOOK
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2 p-3 bg-slate-950 border border-slate-800 rounded-lg">
                <div className="flex justify-between items-center">
                  <h4 className="text-xs font-bold text-slate-200">Force Re-Authentication (MFA)</h4>
                  <Badge className="bg-emerald-500/20 text-emerald-400 text-[10px]">AUTO-EXECUTE</Badge>
                </div>
                <p className="text-[11px] text-slate-400">Invalidate active sessions and enforce MFA.</p>
                <Button 
                  onClick={() => handleExecuteAction('FORCE_MFA')}
                  className="w-full bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold py-1.5 h-auto"
                >
                  Trigger FORCE_MFA
                </Button>
              </div>

              <div className="space-y-2 p-3 bg-slate-950 border border-slate-800 rounded-lg">
                <div className="flex justify-between items-center">
                  <h4 className="text-xs font-bold text-slate-200">Deploy Dynamic Decoy</h4>
                  <Badge variant="outline" className="text-slate-400 text-[10px]">MANUAL APPROVAL</Badge>
                </div>
                <p className="text-[11px] text-slate-400">Spin up decoy Access_HR_Database resource to trap attacker.</p>
                <Button 
                  onClick={() => handleExecuteAction('DEPLOY_HONEYPOT')}
                  variant="outline" 
                  className="w-full border-slate-700 hover:bg-slate-800 text-slate-200 text-xs font-bold py-1.5 h-auto"
                >
                  Deploy Decoy Resource
                </Button>
              </div>

              {remediationStatus && (
                <div className="p-2.5 bg-emerald-950/80 border border-emerald-500/40 rounded-lg text-emerald-400 text-xs flex items-center gap-2 animate-pulse">
                  <CheckCircle size={14} />
                  <span>{remediationStatus}</span>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};
export default AlertDetailPage;
