"""
Evaluation Metrics utility module for CyberTwin AI.
Calculates Precision, Recall, F1-Score, and AUROC for imbalanced security telemetry classification.
"""
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix


def evaluate_security_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray | None = None) -> dict:
    """
    Computes Precision, Recall, F1-Score, and AUROC metrics.
    
    Args:
        y_true: Ground truth binary labels (0 = Normal, 1 = Attack)
        y_pred: Predicted binary labels
        y_prob: Predicted attack probabilities (optional, for AUROC)

    Returns:
        Dict containing security metrics.
    """
    precision = float(precision_score(y_true, y_pred, zero_division=0))
    recall = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))

    metrics = {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4)
    }

    if y_prob is not None and len(np.unique(y_true)) > 1:
        try:
            auroc = float(roc_auc_score(y_true, y_prob))
            metrics["auroc"] = round(auroc, 4)
        except Exception:
            metrics["auroc"] = 0.0

    cm = confusion_matrix(y_true, y_pred)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        metrics["true_positives"] = int(tp)
        metrics["false_positives"] = int(fp)
        metrics["true_negatives"] = int(tn)
        metrics["false_negatives"] = int(fn)

    return metrics
