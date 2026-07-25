import shap
import numpy as np
import logging

class ExplainerXAI:
    def __init__(self, model):
        """
        model: The trained XGBoost model from Phase 12.
        """
        # We use TreeExplainer because it is highly optimized for XGBoost
        self.explainer = shap.TreeExplainer(model)
        
        # Mapping raw feature names to human-readable strings
        self.feature_translation = {
            "failed_logins_15m": "high number of failed authentication attempts",
            "travel_velocity": "impossible travel speed between locations",
            "velocity_kmh": "impossible travel speed between locations",
            "is_new_resource": "accessing a sensitive resource for the first time",
            "hour_sin": "activity outside normal working hours",
            "device_spoof_flag": "unrecognized browser or device fingerprint"
        }

    def generate_explanation(self, feature_vector: np.ndarray, feature_names: list) -> dict:
        """
        Generates both the mathematical SHAP values and a Natural Language explanation.
        """
        # 1. Calculate SHAP values for this specific instance
        shap_values = self.explainer.shap_values(feature_vector)
        
        # If multi-class, shap_values might be a list. We take the values for the predicted class.
        if isinstance(shap_values, list):
            shap_values = shap_values[0] # Assuming index 0 is the anomalous class for this example

        # Flatten arrays for processing
        shap_values_flat = shap_values.flatten()
        
        # 2. Extract Top 3 Contributing Features
        # We want the features with the highest POSITIVE SHAP values (pushed risk higher)
        top_indices = np.argsort(shap_values_flat)[-3:][::-1]
        
        top_features = []
        for idx in top_indices:
            feat_name = feature_names[idx]
            feat_contribution = shap_values_flat[idx]
            if feat_contribution > 0: # Only care about factors increasing risk
                top_features.append({
                    "feature": feat_name,
                    "contribution": round(float(feat_contribution), 4)
                })

        # 3. Generate Natural Language Explanation (NLG)
        explanation_text = self._build_natural_language(top_features)

        return {
            "shap_array": top_features, # Send this to React for a bar chart
            "nlp_explanation": explanation_text # Send this to React for the text alert
        }

    def _build_natural_language(self, top_features: list) -> str:
        if not top_features:
            return "Flagged due to complex, multi-variable deviation from baseline behavior."

        reasons = []
        for item in top_features:
            friendly_name = self.feature_translation.get(item['feature'], item['feature'])
            reasons.append(friendly_name)

        if len(reasons) == 1:
            return f"This event was flagged primarily due to {reasons[0]}."
        elif len(reasons) == 2:
            return f"This event was flagged due to {reasons[0]} combined with {reasons[1]}."
        else:
            return f"This event was flagged due to a combination of {reasons[0]}, {reasons[1]}, and {reasons[2]}."


# --- Usage Example ---
if __name__ == "__main__":
    # Fallback simulation explainer when SHAP TreeExplainer receives feature arrays directly
    explainer = ExplainerXAI.__new__(ExplainerXAI)
    explainer.feature_translation = {
        "travel_velocity": "impossible travel speed between locations",
        "is_new_resource": "accessing a sensitive resource for the first time",
        "failed_logins_15m": "high number of failed authentication attempts"
    }
    sample_top = [
        {"feature": "travel_velocity", "contribution": 0.42},
        {"feature": "is_new_resource", "contribution": 0.28}
    ]
    nlp = explainer._build_natural_language(sample_top)
    print("\n--- XAI Explanation Test Output ---")
    print(nlp)
