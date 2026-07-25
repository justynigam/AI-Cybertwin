import logging

class AnomalyFusionEngine:
    def __init__(self):
        # Base weights for the ensemble (Can be tuned via hyperparameter optimization)
        self.weights = {
            'autoencoder': 0.30,  # Point-in-time
            'transformer': 0.45,  # Sequence (Most reliable for APTs)
            'graph': 0.25         # Topology
        }
        
    def normalize_autoencoder_score(self, raw_mse: float, historical_max_mse: float) -> float:
        """Min-Max scales the MSE to a 0.0-1.0 probability range."""
        if historical_max_mse == 0:
            return 0.0
        normalized = min(raw_mse / historical_max_mse, 1.0)
        return float(normalized)

    def calculate_master_risk(self, ae_score: float, tf_score: float, graph_score: float) -> dict:
        """
        Fuses the normalized scores into a prioritized alert.
        """
        # 1. Base Weighted Average
        base_score = (
            (ae_score * self.weights['autoencoder']) +
            (tf_score * self.weights['transformer']) +
            (graph_score * self.weights['graph'])
        )
        
        # 2. Consensus Multiplier (The Staff Engineer Secret)
        # If all 3 models independently score > 0.8, they agree an attack is happening.
        # We boost the score to ensure it hits CRITICAL.
        if ae_score > 0.8 and tf_score > 0.8 and graph_score > 0.8:
            master_score = min(base_score * 1.2, 1.0)
            reason = "High consensus across all AI models."
        # If the Transformer flags a massive sequence risk, but point-in-time is low
        elif tf_score > 0.95:
            master_score = min(base_score * 1.1, 1.0)
            reason = "Critical temporal sequence detected (APT behavior)."
        else:
            master_score = base_score
            reason = "Standard weighted evaluation."

        # 3. Alert Prioritization Tiers
        severity = self._determine_severity(master_score)
        
        return {
            "master_risk_score": round(master_score, 4),
            "severity": severity,
            "fusion_reason": reason,
            "sub_scores": {
                "autoencoder": round(ae_score, 4),
                "transformer": round(tf_score, 4),
                "graph": round(graph_score, 4)
            }
        }

    def _determine_severity(self, score: float) -> str:
        if score >= 0.90:
            return "CRITICAL" # PagerDuty goes off, automate defense
        elif score >= 0.75:
            return "HIGH"     # Show in dashboard immediately
        elif score >= 0.50:
            return "MEDIUM"   # Log for analyst review
        else:
            return "LOW"      # Ignore (Normal behavior)
