import { create } from 'zustand';

export interface Alert {
  id: string;
  timestamp: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  attack_category: string;
  master_risk_score: number;
  nlp_explanation?: string;
  user_id?: string;
  device_id?: string;
  ip_address?: string;
  shap_features?: { feature: string; contribution: number }[];
  twin_predictions?: { predicted_action: string; probability_score: number; rank: number }[];
}

interface AlertStore {
  alerts: Alert[];
  selectedAlert: Alert | null;
  globalSearchQuery: string;
  addAlert: (alert: Alert) => void;
  selectAlert: (alert: Alert | null) => void;
  setGlobalSearchQuery: (query: string) => void;
  clearAlerts: () => void;
}

export const useAlertStore = create<AlertStore>((set) => ({
  alerts: [
    {
      id: 'demo-alert-1',
      timestamp: new Date().toISOString(),
      severity: 'CRITICAL',
      attack_category: 'Impossible Travel',
      master_risk_score: 0.98,
      nlp_explanation: 'This event was flagged due to impossible travel speed between geographical locations combined with accessing a sensitive resource for the first time.',
      user_id: 'usr-9982',
      device_id: 'dev-4410',
      ip_address: '185.220.101.4',
      shap_features: [
        { feature: 'velocity_kmh', contribution: 0.48 },
        { feature: 'is_new_resource', contribution: 0.32 },
        { feature: 'hour_sin', contribution: 0.15 }
      ],
      twin_predictions: [
        { predicted_action: 'Access_HR_Database', probability_score: 0.82, rank: 1 },
        { predicted_action: 'Execute_PowerShell', probability_score: 0.12, rank: 2 },
        { predicted_action: 'Clear_Event_Logs', probability_score: 0.04, rank: 3 }
      ]
    },
    {
      id: 'demo-alert-2',
      timestamp: new Date(Date.now() - 300000).toISOString(),
      severity: 'HIGH',
      attack_category: 'Lateral Movement',
      master_risk_score: 0.84,
      nlp_explanation: 'This event was flagged due to sudden network hop distance increase across 3 isolated subnets.',
      user_id: 'usr-3104',
      device_id: 'dev-8812',
      ip_address: '10.0.4.99',
      shap_features: [
        { feature: 'graph_shortest_path', contribution: 0.55 },
        { feature: 'events_last_1hr', contribution: 0.22 }
      ],
      twin_predictions: [
        { predicted_action: 'Access_HR_Database', probability_score: 0.65, rank: 1 }
      ]
    }
  ],
  selectedAlert: null,
  globalSearchQuery: '',
  addAlert: (alert) => set((state) => ({ alerts: [alert, ...state.alerts], selectedAlert: alert })),
  selectAlert: (alert) => set({ selectedAlert: alert }),
  setGlobalSearchQuery: (query) => set({ globalSearchQuery: query }),
  clearAlerts: () => set({ alerts: [], selectedAlert: null })
}));
