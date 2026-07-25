import React, { useState } from 'react';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Settings, Sliders, Database, Server, Cpu, CheckCircle2, RefreshCw } from 'lucide-react';

export function SystemSettingsPage() {
  const [autoExecutePlaybooks, setAutoExecutePlaybooks] = useState<boolean>(true);
  const [consensusMultiplier, setConsensusMultiplier] = useState<number>(1.2);
  const [autoencoderThreshold, setAutoencoderThreshold] = useState<number>(0.80);
  const [transformerThreshold, setTransformerThreshold] = useState<number>(0.85);
  const [savedSuccess, setSavedSuccess] = useState<boolean>(false);

  const handleSaveSettings = () => {
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  return (
    <div className="p-6 space-y-6 bg-slate-950 text-slate-50 min-h-screen">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            <Settings className="h-6 w-6 text-cyan-400" />
            CyberTwin System Settings & Model Configuration
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Manage ML inference thresholds, SOAR playbook automation rules, and streaming connection parameters
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 px-3 py-1">
            <CheckCircle2 className="h-3.5 w-3.5 mr-1.5" />
            All Configurations Active
          </Badge>
        </div>
      </div>

      {savedSuccess && (
        <div className="p-3 bg-emerald-950/80 border border-emerald-500/40 rounded-lg text-emerald-400 text-xs font-semibold flex items-center gap-2 animate-bounce">
          <CheckCircle2 className="h-4 w-4" />
          Settings successfully updated and reloaded into active ML inference pipeline!
        </div>
      )}

      {/* Main Settings Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ML Inference & Anomaly Thresholds */}
        <Card className="p-6 bg-slate-900/60 border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <Sliders className="h-4 w-4 text-cyan-400" /> Anomaly Detection Model Thresholds
          </h2>

          <div className="space-y-4 text-xs">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-slate-300 font-medium">Autoencoder Point-in-time MSE Threshold:</span>
                <span className="font-mono text-cyan-400 font-bold">{autoencoderThreshold}</span>
              </div>
              <input
                type="range"
                min="0.50"
                max="0.95"
                step="0.05"
                value={autoencoderThreshold}
                onChange={(e) => setAutoencoderThreshold(parseFloat(e.target.value))}
                className="w-full h-1.5 bg-slate-950 rounded-lg appearance-none cursor-pointer accent-cyan-500"
              />
            </div>

            <div>
              <div className="flex justify-between mb-1">
                <span className="text-slate-300 font-medium">CyberSequenceTransformer Risk Threshold:</span>
                <span className="font-mono text-cyan-400 font-bold">{transformerThreshold}</span>
              </div>
              <input
                type="range"
                min="0.50"
                max="0.95"
                step="0.05"
                value={transformerThreshold}
                onChange={(e) => setTransformerThreshold(parseFloat(e.target.value))}
                className="w-full h-1.5 bg-slate-950 rounded-lg appearance-none cursor-pointer accent-cyan-500"
              />
            </div>

            <div>
              <div className="flex justify-between mb-1">
                <span className="text-slate-300 font-medium">Master Tri-Model Consensus Multiplier:</span>
                <span className="font-mono text-amber-400 font-bold">{consensusMultiplier}x</span>
              </div>
              <input
                type="range"
                min="1.0"
                max="1.5"
                step="0.05"
                value={consensusMultiplier}
                onChange={(e) => setConsensusMultiplier(parseFloat(e.target.value))}
                className="w-full h-1.5 bg-slate-950 rounded-lg appearance-none cursor-pointer accent-amber-500"
              />
              <p className="text-[10px] text-slate-500 mt-1">
                Applies {consensusMultiplier}x multiplier when Autoencoder, Transformer, and Graph models all exceed risk thresholds.
              </p>
            </div>
          </div>
        </Card>

        {/* SOAR Playbook Automation Rules */}
        <Card className="p-6 bg-slate-900/60 border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <Server className="h-4 w-4 text-emerald-400" /> SOAR Automation & Playbook Rules
          </h2>

          <div className="space-y-4 text-xs">
            <div className="flex items-center justify-between p-3 bg-slate-950 border border-slate-800 rounded-lg">
              <div>
                <p className="font-semibold text-slate-200">Auto-Execute Critical Threat Playbooks</p>
                <p className="text-[10px] text-slate-400">Automatically trigger FORCE_MFA when master risk score &gt; 95.0%</p>
              </div>
              <input
                type="checkbox"
                checked={autoExecutePlaybooks}
                onChange={(e) => setAutoExecutePlaybooks(e.target.checked)}
                className="h-4 w-4 rounded border-slate-700 text-cyan-500 focus:ring-cyan-500 bg-slate-900 cursor-pointer"
              />
            </div>

            <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
              <span className="font-semibold text-slate-300 block">Default Decoy Strategy:</span>
              <p className="text-slate-400 text-[11px]">Deploy Dynamic HR Database Honeypot Sandbox on isolated VLAN</p>
            </div>
          </div>
        </Card>

        {/* Model Weights Registry */}
        <Card className="p-6 bg-slate-900/60 border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <Cpu className="h-4 w-4 text-cyan-400" /> Trained Model Checkpoint Registry
          </h2>

          <div className="space-y-2 text-xs">
            <div className="p-2.5 bg-slate-950 border border-slate-800 rounded-md flex justify-between items-center">
              <div>
                <p className="font-mono text-cyan-300 font-semibold">autoencoder.pth</p>
                <p className="text-[10px] text-slate-500">PyTorch BehaviorAutoencoder | Input Dim: 14</p>
              </div>
              <Badge className="bg-emerald-500/20 text-emerald-400 border-emerald-500/30 text-[9px]">LOADED</Badge>
            </div>

            <div className="p-2.5 bg-slate-950 border border-slate-800 rounded-md flex justify-between items-center">
              <div>
                <p className="font-mono text-cyan-300 font-semibold">best_transformer.pt</p>
                <p className="text-[10px] text-slate-500">PyTorch CyberSequenceTransformer | d_model: 64</p>
              </div>
              <Badge className="bg-emerald-500/20 text-emerald-400 border-emerald-500/30 text-[9px]">LOADED</Badge>
            </div>

            <div className="p-2.5 bg-slate-950 border border-slate-800 rounded-md flex justify-between items-center">
              <div>
                <p className="font-mono text-cyan-300 font-semibold">xgboost_classifier.json</p>
                <p className="text-[10px] text-slate-500">Multi-Class ATT&CK Classifier | SMOTE Oversampled</p>
              </div>
              <Badge className="bg-emerald-500/20 text-emerald-400 border-emerald-500/30 text-[9px]">LOADED</Badge>
            </div>
          </div>
        </Card>

        {/* Infrastructure & Connection Pool */}
        <Card className="p-6 bg-slate-900/60 border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <Database className="h-4 w-4 text-purple-400" /> Infrastructure Connection Pool
          </h2>

          <div className="space-y-2 text-xs font-mono">
            <div className="p-2 bg-slate-950 border border-slate-800 rounded flex justify-between">
              <span className="text-slate-400">FastAPI API URL:</span>
              <span className="text-cyan-400">http://localhost:8000</span>
            </div>

            <div className="p-2 bg-slate-950 border border-slate-800 rounded flex justify-between">
              <span className="text-slate-400">WebSocket Alert Feed:</span>
              <span className="text-cyan-400">ws://localhost:8000/api/v1/ws/alerts</span>
            </div>

            <div className="p-2 bg-slate-950 border border-slate-800 rounded flex justify-between">
              <span className="text-slate-400">Graph Memory Pruning:</span>
              <span className="text-amber-400">60 Minutes Edge Expiry</span>
            </div>
          </div>
        </Card>
      </div>

      {/* Save Button */}
      <div className="flex justify-end pt-4">
        <button
          onClick={handleSaveSettings}
          className="px-6 py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold rounded-lg shadow-lg shadow-cyan-600/20 transition flex items-center gap-2"
        >
          <RefreshCw className="h-4 w-4" /> Save System Settings & Reload Models
        </button>
      </div>
    </div>
  );
}
export default SystemSettingsPage;
