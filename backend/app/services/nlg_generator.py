"""
Natural Language Generation (NLG) Translator Service for CyberTwin AI.
Translates raw model risk metrics, SHAP feature contributions, and fusion scores
into human-readable SOC security incident explanations.
"""
import logging


class NaturalLanguageExplanationGenerator:
    """
    Translates model output math into executive and SOC-level English text summaries.
    """

    FEATURE_TRANSLATIONS = {
        "failed_logins_15m": "high number of failed authentication attempts",
        "travel_velocity": "impossible travel speed between locations",
        "velocity_kmh": "impossible travel speed between geographical locations",
        "distance_km": "login originating from an anomalous geographical distance",
        "is_new_resource": "accessing a sensitive resource for the first time",
        "hour_sin": "activity occurring outside normal working hours",
        "is_weekend": "weekend activity for a standard weekday user",
        "device_spoof_flag": "unrecognized browser or device fingerprint",
        "time_since_last_event_seconds": "rapid succession of authentication events",
        "events_last_1hr": "spike in event volume over the past hour",
        "ip_address_hash": "unfamiliar or reputation-flagged IP address",
        "device_id_hash": "unrecognized endpoint hardware identifier"
    }

    def generate_incident_report(
        self,
        master_risk_score: float,
        severity: str,
        attack_category: str,
        top_shap_features: list[dict],
        fusion_reason: str = ""
    ) -> str:
        """
        Generates a full natural language alert paragraph.
        """
        # 1. Headline summary
        score_percent = int(round(master_risk_score * 100))
        headline = f"ALERT! Risk Score: {score_percent}% ({severity})"
        if attack_category and attack_category != "Benign":
            headline += f" - Suspected {attack_category}"

        # 2. Key Reason Translation
        reasons = []
        for feat in top_shap_features[:3]:
            fname = feat.get("feature", "")
            friendly = self.FEATURE_TRANSLATIONS.get(fname, fname.replace("_", " "))
            reasons.append(friendly)

        if not reasons:
            body = "This event was flagged due to complex multi-variable deviation from historical behavioral baselines."
        elif len(reasons) == 1:
            body = f"This event was flagged primarily due to {reasons[0]}."
        elif len(reasons) == 2:
            body = f"This event was flagged due to {reasons[0]} combined with {reasons[1]}."
        else:
            body = f"This event was flagged due to a combination of {reasons[0]}, {reasons[1]}, and {reasons[2]}."

        # 3. Append fusion reasoning if consensus was triggered
        if "consensus" in fusion_reason.lower():
            body += " High consensus was detected simultaneously across Autoencoder, Transformer, and Graph models."

        return f"{headline}\n\"{body}\""


if __name__ == "__main__":
    nlg = NaturalLanguageExplanationGenerator()
    sample_shap = [
        {"feature": "velocity_kmh", "contribution": 0.45},
        {"feature": "is_new_resource", "contribution": 0.31}
    ]
    report = nlg.generate_incident_report(
        master_risk_score=0.98,
        severity="CRITICAL",
        attack_category="Impossible Travel",
        top_shap_features=sample_shap,
        fusion_reason="High consensus across all AI models."
    )
    print("\n--- NLG Generated Incident Report ---")
    print(report)
