"""
Training script for CyberTwin AI baseline models.
Loads raw telemetry events, extracts temporal/spatial/stateful features,
trains PyTorch Autoencoder and KMeans Clustering models, and exports weights.
"""
import os
import sys
import torch
import numpy as np
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset

# Add parent directory to sys.path if running as script
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ml.features.temporal import engineer_temporal_features, engineer_behavioral_features
from ml.features.spatial import calculate_spatial_velocity
from ml.features.categorical import encode_categorical_features
from ml.models.autoencoder import CyberTwinAutoencoder
from ml.models.clustering import RoleBaselineClustering


DATA_PATH = os.path.join(project_root, "ml", "data", "raw", "events.json")
WEIGHTS_DIR = os.path.join(project_root, "ml", "weights")


def load_and_preprocess_data(json_path: str) -> pd.DataFrame:
    """Loads raw events and executes complete feature pipeline."""
    print(f"Loading raw events from: {json_path}")
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Raw data file not found at {json_path}")

    df = pd.read_json(json_path, lines=True)
    print(f"Loaded {len(df)} raw events.")

    # 1. Temporal & Behavioral Features
    df = engineer_temporal_features(df)
    df = engineer_behavioral_features(df)

    # 2. Spatial Velocity Features
    df = calculate_spatial_velocity(df)

    # 3. Categorical Hashing Features
    df = encode_categorical_features(df)

    return df


def prepare_feature_matrix(df: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    """Selects numerical features for model training."""
    feature_cols = [
        "hour_sin", "hour_cos", "day_sin", "day_cos", "is_weekend",
        "time_since_last_event_seconds", "events_last_1hr",
        "distance_km", "velocity_kmh", "is_impossible_travel_math",
        "event_type_hash", "action_hash", "ip_address_hash", "device_id_hash"
    ]
    # Keep only available columns
    available_cols = [col for col in feature_cols if col in df.columns]
    
    # Fill missing values
    X_df = df[available_cols].fillna(0.0)
    
    # Standardize scale
    mean = X_df.mean(axis=0)
    std = X_df.std(axis=0).replace(0, 1.0)
    X_scaled = ((X_df - mean) / std).values.astype(np.float32)

    return X_scaled, available_cols


def train_autoencoder(X: np.ndarray, epochs: int = 10, batch_size: int = 64, lr: float = 1e-3) -> CyberTwinAutoencoder:
    """Trains PyTorch Autoencoder on scaled numerical feature matrix."""
    input_dim = X.shape[1]
    print(f"\n--- Training Autoencoder (Input Dim: {input_dim}, Samples: {X.shape[0]}) ---")

    dataset = TensorDataset(torch.tensor(X))
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = CyberTwinAutoencoder(input_dim=input_dim, latent_dim=8)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = torch.nn.MSELoss()

    model.train()
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        for (batch_x,) in dataloader:
            optimizer.zero_grad()
            reconstructed, _ = model(batch_x)
            loss = criterion(reconstructed, batch_x)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(batch_x)

        avg_loss = total_loss / len(X)
        print(f"Epoch [{epoch}/{epochs}] - Loss: {avg_loss:.6f}")

    return model


def main():
    os.makedirs(WEIGHTS_DIR, exist_ok=True)

    # 1. Pipeline execution
    df = load_and_preprocess_data(DATA_PATH)
    X, feature_names = prepare_feature_matrix(df)

    # 2. Train KMeans Role Baselines
    print("\n--- Training KMeans Role Clustering Baseline ---")
    clustering_model = RoleBaselineClustering(n_clusters=5)
    clustering_model.fit(X)
    print(f"KMeans fitted with {clustering_model.n_clusters} clusters.")

    # 3. Train Autoencoder Anomaly Model
    ae_model = train_autoencoder(X, epochs=10)

    # 4. Save Weights / Artifacts
    ae_path = os.path.join(WEIGHTS_DIR, "autoencoder.pth")
    torch.save(ae_model.state_dict(), ae_path)
    print(f"\nSaved PyTorch Autoencoder weights to: {ae_path}")

    print("\n[SUCCESS] Baseline training completed successfully!")


if __name__ == "__main__":
    main()
