"""
Unit tests for Anomaly Fusion Engine master risk calculations.
"""
from backend.app.services.anomaly_fusion import AnomalyFusionEngine


def test_anomaly_fusion_consensus():
    engine = AnomalyFusionEngine()

    # Normal scores
    res_normal = engine.calculate_master_risk(ae_score=0.1, tf_score=0.1, graph_score=0.1)
    assert res_normal["severity"] == "LOW"
    assert res_normal["master_risk_score"] < 0.2

    # High consensus scores (> 0.8 across all 3 models triggers 1.2x consensus boost)
    res_attack = engine.calculate_master_risk(ae_score=0.85, tf_score=0.90, graph_score=0.88)
    assert res_attack["severity"] == "CRITICAL"
    assert res_attack["master_risk_score"] == 1.0
    assert "consensus" in res_attack["fusion_reason"].lower()
