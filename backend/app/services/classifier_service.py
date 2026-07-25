"""
Classifier Service for CyberTwin AI Backend.
Loads trained XGBoost model and provides real-time ATT&CK classification inference.
"""
import os
import numpy as np
import logging
from ml.models.attack_classifier import CyberAttackClassifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class AttackClassifierService:
    """
    Real-time inference integration wrapper around CyberAttackClassifier.
    """

    def __init__(self, model_path: str | None = None):
        if model_path is None:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            model_path = os.path.join(project_root, "ml", "weights", "xgboost_classifier.json")

        self.model_path = model_path
        self.classifier: CyberAttackClassifier | None = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.classifier = CyberAttackClassifier(model_path=self.model_path)
                logging.info(f"ClassifierService successfully loaded weights from {self.model_path}")
            except Exception as e:
                logging.error(f"Failed to load XGBoost model from {self.model_path}: {e}")
                self.classifier = None
        else:
            logging.warning(f"No XGBoost model found at {self.model_path}. Running with uninitialized fallback classifier.")
            self.classifier = None

    def classify_event_features(self, feature_vector: np.ndarray, confidence_threshold: float = 0.60) -> dict:
        """
        Classifies feature vector into attack category and confidence score.
        """
        if self.classifier is None:
            return {
                "attack_category": "Unclassified (No Model Loaded)",
                "confidence": 0.0,
                "all_probabilities": []
            }

        if feature_vector.ndim == 1:
            feature_vector = np.expand_dims(feature_vector, axis=0)

        return self.classifier.predict_attack_type(feature_vector, confidence_threshold=confidence_threshold)
