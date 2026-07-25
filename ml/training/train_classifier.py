"""
Training script for XGBoost MITRE ATT&CK Multi-Class Classifier.
Uses explicit class mapping (0 = Benign/Normal, 1-7 = ATT&CK categories),
LabelEncoder for contiguous target indices, and strict feature matrix hygiene.
"""
import os
import sys
import numpy as np
import pandas as pd
import xgboost as xgb
from imblearn.over_sampling import SMOTE, RandomOverSampler
from sklearn.preprocessing import LabelEncoder

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ml.features.temporal import engineer_temporal_features, engineer_behavioral_features
from ml.features.spatial import calculate_spatial_velocity
from ml.features.categorical import encode_categorical_features
from ml.utils.metrics import evaluate_security_metrics

DATA_PATH = os.path.join(project_root, "ml", "data", "raw", "events.json")
WEIGHTS_DIR = os.path.join(project_root, "ml", "weights")
MODEL_SAVE_PATH = os.path.join(WEIGHTS_DIR, "xgboost_classifier.json")

CLASS_MAP = {
    "None": 0,
    "Benign": 0,
    "Brute Force": 1,
    "Credential Stuffing": 2,
    "Impossible Travel": 3,
    "Lateral Movement": 4,
    "Device Spoofing": 5,
    "Insider Threat": 6,
    "Privilege Escalation": 7
}


def load_and_prepare_dataset(json_path: str) -> tuple[pd.DataFrame, np.ndarray, list[str]]:
    """Loads raw json logs, applies feature pipeline, and returns (X, y, feature_names)."""
    df = pd.read_json(json_path, lines=True)

    df = engineer_temporal_features(df)
    df = engineer_behavioral_features(df)
    df = calculate_spatial_velocity(df)
    df = encode_categorical_features(df)

    # STRICT FEATURE HYGIENE - Exclude all label answers & target indicators
    leak_cols = ["is_attack", "attack_category", "event_id", "timestamp", "user_id", "is_impossible_travel_math"]

    pure_feature_cols = [
        "hour_sin", "hour_cos", "day_sin", "day_cos", "is_weekend",
        "time_since_last_event_seconds", "events_last_1hr",
        "distance_km", "velocity_kmh",
        "event_type_hash", "action_hash", "ip_address_hash", "device_id_hash"
    ]
    feature_cols = [c for c in pure_feature_cols if c in df.columns and c not in leak_cols]

    X = df[feature_cols].fillna(0.0)

    # Target Mapping (0 = Normal/Benign, >0 = Attacks)
    raw_target = df["attack_category"].fillna("None") if "attack_category" in df.columns else df["is_attack"].astype(str)
    y_raw = raw_target.map(lambda c: CLASS_MAP.get(str(c), 0)).astype(int).values

    return X, y_raw, feature_cols


def train_classifier():
    os.makedirs(WEIGHTS_DIR, exist_ok=True)

    print(f"Loading raw telemetry dataset from: {DATA_PATH}")
    X, y_raw, feature_cols = load_and_prepare_dataset(DATA_PATH)
    print(f"Features used ({len(feature_cols)}): {feature_cols}")

    # Encode labels to contiguous integers 0, 1, ...
    le = LabelEncoder()
    y = le.fit_transform(y_raw)

    # Chronological Train / Val Split
    split_idx = int(len(X) * 0.8)

    X_train, y_train = X.iloc[:split_idx], y[:split_idx]
    X_val, y_val = X.iloc[split_idx:], y[split_idx:]

    print(f"Chronological Train Shape: X={X_train.shape}, y distribution={dict(pd.Series(y_train).value_counts())}")
    print(f"Chronological Val Shape:   X={X_val.shape}, y distribution={dict(pd.Series(y_val).value_counts())}")

    # Oversample minority attack classes in training set
    unique_classes, counts = np.unique(y_train, return_counts=True)
    min_samples = np.min(counts)

    if len(unique_classes) > 1:
        if min_samples >= 6:
            sampler = SMOTE(k_neighbors=min(5, min_samples - 1), random_state=42)
        else:
            sampler = RandomOverSampler(random_state=42)
        X_train_res, y_train_res = sampler.fit_resample(X_train, y_train)
    else:
        X_train_res, y_train_res = X_train, y_train

    print(f"Resampled Train Shape: X={X_train_res.shape}, y distribution={dict(pd.Series(y_train_res).value_counts())}")

    num_classes = len(le.classes_)
    print(f"\n--- Training XGBoost Classifier (Unique Present Classes: {num_classes}) ---")

    if num_classes > 2:
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            objective="multi:softprob",
            num_class=num_classes,
            random_state=42,
            eval_metric="mlogloss"
        )
    else:
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            objective="binary:logistic",
            random_state=42,
            eval_metric="logloss"
        )

    model.fit(X_train_res, y_train_res, eval_set=[(X_val, y_val)], verbose=False)

    # Evaluate validation metrics (Class 0 = Normal, Class > 0 = Attack)
    val_preds = model.predict(X_val)
    
    # Map back encoded indices to original CLASS_MAP targets (0 = Normal)
    orig_val_y = le.inverse_transform(y_val)
    orig_val_preds = le.inverse_transform(val_preds)

    binary_val_y = (orig_val_y > 0).astype(int)
    binary_val_preds = (orig_val_preds > 0).astype(int)

    metrics = evaluate_security_metrics(binary_val_y, binary_val_preds)
    print(f"\n--- Validation Performance Metrics ---")
    print(f"Precision (Positive=Attack): {metrics['precision']}")
    print(f"Recall (Positive=Attack):    {metrics['recall']}")
    print(f"F1-Score:                   {metrics['f1_score']}")
    if "true_positives" in metrics:
        print(f"TP: {metrics['true_positives']} | FP: {metrics['false_positives']} | TN: {metrics['true_negatives']} | FN: {metrics['false_negatives']}")

    booster = model.get_booster()
    booster.save_model(MODEL_SAVE_PATH)
    print(f"\n[SUCCESS] XGBoost model saved to: {MODEL_SAVE_PATH}")


if __name__ == "__main__":
    train_classifier()
