import xgboost as xgb
import numpy as np
import logging

class CyberAttackClassifier:
    def __init__(self, model_path: str = None):
        """
        Wrapper for the XGBoost Multi-Class model.
        """
        self.model = xgb.Booster()
        if model_path:
            self.model.load_model(model_path)
            logging.info(f"Loaded XGBoost Classifier from {model_path}")
            
        # Standard MITRE ATT&CK inspired mapping
        self.class_mapping = {
            0: "Benign",
            1: "Brute Force",
            2: "Credential Stuffing",
            3: "Impossible Travel",
            4: "Lateral Movement",
            5: "Device Spoofing",
            6: "Insider Threat",
            7: "Privilege Escalation"
        }

    def predict_attack_type(self, feature_vector: np.ndarray, confidence_threshold: float = 0.60) -> dict:
        """
        Infers the specific attack category from the feature vector.
        feature_vector must be a 2D numpy array: shape (1, num_features)
        """
        dmatrix = xgb.DMatrix(feature_vector)
        
        # Returns an array of probabilities for each class
        probabilities = self.model.predict(dmatrix)[0]
        
        # Get the index of the highest probability
        predicted_class_idx = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_class_idx])
        
        # --- The Staff Engineer Fallback Logic ---
        if confidence < confidence_threshold:
            # The model isn't confident enough to label this specific attack.
            # We don't want to mislead the SOC analyst with a bad guess.
            return {
                "attack_category": "Unknown/Novel Anomaly",
                "confidence": confidence,
                "all_probabilities": probabilities.tolist()
            }
            
        return {
            "attack_category": self.class_mapping.get(predicted_class_idx, "Unknown"),
            "confidence": confidence,
            "all_probabilities": probabilities.tolist()
        }
