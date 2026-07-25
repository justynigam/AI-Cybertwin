"""
Score Aggregator worker for CyberTwin AI.
Listens for point-in-time (Autoencoder), temporal sequence (Transformer),
and topological (Graph Engine) risk scores, fusing them into master security alerts.
"""
import os
import json
import logging
from datetime import datetime
from backend.app.services.anomaly_fusion import AnomalyFusionEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class RiskScoreAggregator:
    """
    Worker class that aggregates model outputs per event_id / user_id
    and produces fused Master Risk alerts.
    """

    def __init__(self, fusion_engine: AnomalyFusionEngine | None = None):
        self.fusion_engine = fusion_engine if fusion_engine is not None else AnomalyFusionEngine()
        self.event_scores: dict[str, dict[str, float]] = {}

    def record_score(self, event_id: str, model_type: str, score: float):
        """
        Records an individual model score for an event.
        model_type: 'autoencoder', 'transformer', or 'graph'
        """
        if event_id not in self.event_scores:
            self.event_scores[event_id] = {
                "autoencoder": 0.0,
                "transformer": 0.0,
                "graph": 0.0
            }

        if model_type in self.event_scores[event_id]:
            self.event_scores[event_id][model_type] = float(score)

    def process_fused_event(
        self,
        event_id: str,
        ae_score: float,
        tf_score: float,
        graph_score: float,
        metadata: dict | None = None
    ) -> dict:
        """
        Fuses the three model scores directly for an event and returns a master alert dictionary.
        """
        fused_result = self.fusion_engine.calculate_master_risk(
            ae_score=ae_score,
            tf_score=tf_score,
            graph_score=graph_score
        )

        alert_event = {
            "event_id": event_id,
            "timestamp": datetime.utcnow().isoformat(),
            "master_risk_score": fused_result["master_risk_score"],
            "severity": fused_result["severity"],
            "fusion_reason": fused_result["fusion_reason"],
            "sub_scores": fused_result["sub_scores"],
            "metadata": metadata or {}
        }

        if fused_result["severity"] in ["CRITICAL", "HIGH"]:
            logging.warning(
                f"[ALERT {fused_result['severity']}] Event {event_id} - Score: {fused_result['master_risk_score']} | Reason: {fused_result['fusion_reason']}"
            )
        else:
            logging.info(
                f"[LOG {fused_result['severity']}] Event {event_id} - Score: {fused_result['master_risk_score']}"
            )

        return alert_event


if __name__ == "__main__":
    # Quick functional test of the aggregator worker
    aggregator = RiskScoreAggregator()
    
    # Test 1: Normal behavior
    normal_alert = aggregator.process_fused_event("event-001", ae_score=0.1, tf_score=0.05, graph_score=0.1)
    print("Normal Alert Test:", normal_alert)

    # Test 2: High Consensus APT Attack
    attack_alert = aggregator.process_fused_event("event-002", ae_score=0.85, tf_score=0.92, graph_score=0.88)
    print("\nAPT Attack Alert Test:", attack_alert)
