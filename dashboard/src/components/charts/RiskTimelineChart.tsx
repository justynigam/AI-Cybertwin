import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const data = [
  { time: '10:00', risk: 0.12, baseline: 0.15 },
  { time: '10:05', risk: 0.14, baseline: 0.15 },
  { time: '10:10', risk: 0.22, baseline: 0.15 },
  { time: '10:15', risk: 0.88, baseline: 0.16 },
  { time: '10:20', risk: 0.98, baseline: 0.15 },
  { time: '10:25', risk: 0.65, baseline: 0.15 },
  { time: '10:30', risk: 0.40, baseline: 0.14 },
];

export const RiskTimelineChart: React.FC = () => {
  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data}>
          <defs>
            <linearGradient id="riskGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#ef4444" stopOpacity={0.0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis dataKey="time" stroke="#64748b" fontSize={12} />
          <YAxis stroke="#64748b" fontSize={12} domain={[0, 1]} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
          <Tooltip
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
            labelStyle={{ color: '#94a3b8' }}
          />
          <Area type="monotone" dataKey="risk" stroke="#ef4444" strokeWidth={2} fillOpacity={1} fill="url(#riskGrad)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
