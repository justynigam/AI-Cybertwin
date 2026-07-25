import React, { useEffect } from 'react';
import { useAlertStore, Alert } from '../store/useAlertStore';
import { ShieldAlert, Activity, Search } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface AlertsPageProps {
  onSelectAlert?: (alert: Alert) => void;
}

export const AlertsPage: React.FC<AlertsPageProps> = ({ onSelectAlert }) => {
  const { alerts, addAlert, selectAlert, globalSearchQuery } = useAlertStore();

  // Simulated WebSocket Connection
  useEffect(() => {
    let ws: WebSocket | null = null;
    try {
      ws = new WebSocket('ws://localhost:8000/api/v1/ws/alerts');
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        addAlert(data);
      };
    } catch (e) {
      console.log("WebSocket demo mode fallback");
    }

    return () => {
      if (ws) ws.close();
    };
  }, [addAlert]);

  const getSeverityColor = (severity: string) => {
    switch(severity) {
      case 'CRITICAL': return 'bg-red-600 text-white animate-pulse';
      case 'HIGH': return 'bg-orange-500 text-white';
      case 'MEDIUM': return 'bg-yellow-500 text-black';
      default: return 'bg-slate-500 text-white';
    }
  };

  const handleCardClick = (alert: Alert) => {
    selectAlert(alert);
    if (onSelectAlert) {
      onSelectAlert(alert);
    }
  };

  // Filter alerts by global search query across User ID, Device ID, IP, and Category
  const filteredAlerts = alerts.filter(alert => {
    const q = globalSearchQuery.toLowerCase().trim();
    if (!q) return true;
    return (
      alert.id.toLowerCase().includes(q) ||
      (alert.user_id && alert.user_id.toLowerCase().includes(q)) ||
      (alert.device_id && alert.device_id.toLowerCase().includes(q)) ||
      (alert.ip_address && alert.ip_address.toLowerCase().includes(q)) ||
      alert.attack_category.toLowerCase().includes(q) ||
      (alert.nlp_explanation && alert.nlp_explanation.toLowerCase().includes(q))
    );
  });

  return (
    <div className="p-6 bg-slate-950 min-h-screen text-slate-50">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Activity className="text-cyan-500" /> Live Threat Feed
        </h1>
        <Badge variant="outline" className="text-slate-400 border-slate-700">
          Monitoring Active ({filteredAlerts.length} / {alerts.length} Alerts)
        </Badge>
      </div>

      <div className="space-y-4">
        {filteredAlerts.length === 0 ? (
          <Card className="bg-slate-900 border-slate-800 p-8 text-center text-slate-400">
            <Search className="h-8 w-8 mx-auto mb-2 text-slate-500 opacity-60" />
            <p>No alerts matched your search query "{globalSearchQuery}"</p>
          </Card>
        ) : (
          filteredAlerts.map((alert) => (
            <Card 
              key={alert.id} 
              className="bg-slate-900 border-slate-800 hover:border-slate-700 transition cursor-pointer"
              onClick={() => handleCardClick(alert)}
            >
              <CardContent className="p-4 flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <ShieldAlert className={alert.severity === 'CRITICAL' ? 'text-red-500 h-8 w-8' : 'text-orange-500 h-8 w-8'} />
                  <div>
                    <h3 className="font-bold text-lg text-slate-200">{alert.attack_category}</h3>
                    <p className="text-sm text-slate-400 line-clamp-1">
                      {alert.nlp_explanation}
                    </p>
                    <div className="flex items-center gap-3 mt-1 text-xs font-mono text-slate-500">
                      <span>User: {alert.user_id || 'N/A'}</span>
                      <span>Device: {alert.device_id || 'N/A'}</span>
                      <span>IP: {alert.ip_address || 'N/A'}</span>
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-sm font-semibold mb-1">
                    Risk Score: {(alert.master_risk_score * 100).toFixed(1)}%
                  </div>
                  <Badge className={getSeverityColor(alert.severity)}>
                    {alert.severity}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};
export default AlertsPage;
