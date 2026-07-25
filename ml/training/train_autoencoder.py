"""
Chronological Training Script for Autoencoder.
Uses MSE reconstruction loss and Early Stopping.
"""
import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ml.models.autoencoder import BehaviorAutoencoder
from ml.features.temporal import engineer_temporal_features, engineer_behavioral_features
from ml.features.spatial import calculate_spatial_velocity
from ml.features.categorical import encode_categorical_features

DATA_PATH = os.path.join(project_root, "ml", "data", "raw", "events.json")
WEIGHTS_DIR = os.path.join(project_root, "ml", "weights")


def train_autoencoder_model():
    os.makedirs(WEIGHTS_DIR, exist_ok=True)
    save_path = os.path.join(WEIGHTS_DIR, "autoencoder.pth")

    df = pd.read_json(DATA_PATH, lines=True)
    df = engineer_temporal_features(df)
    df = engineer_behavioral_features(df)
    df = calculate_spatial_velocity(df)
    df = encode_categorical_features(df)

    # Chronological Split
    df_sorted = df.sort_values("timestamp")
    split_idx = int(len(df_sorted) * 0.8)
    train_df = df_sorted.iloc[:split_idx]
    val_df = df_sorted.iloc[split_idx:]

    feature_cols = [
        "hour_sin", "hour_cos", "day_sin", "day_cos", "is_weekend",
        "time_since_last_event_seconds", "events_last_1hr",
        "distance_km", "velocity_kmh", "is_impossible_travel_math",
        "event_type_hash", "action_hash", "ip_address_hash", "device_id_hash"
    ]
    available_cols = [c for c in feature_cols if c in df.columns]

    X_train = train_df[available_cols].fillna(0.0).values.astype(np.float32)
    X_val = val_df[available_cols].fillna(0.0).values.astype(np.float32)

    # MinMax normalize features safely to [0, 1] range
    min_vals = np.min(X_train, axis=0)
    max_vals = np.max(X_train, axis=0)
    diff = max_vals - min_vals
    diff = np.where(diff > 1e-6, diff, 1.0)

    X_train_norm = np.nan_to_num((X_train - min_vals) / diff, nan=0.0)
    X_val_norm = np.nan_to_num((X_val - min_vals) / diff, nan=0.0)

    train_dataset = TensorDataset(torch.tensor(X_train_norm))
    val_dataset = TensorDataset(torch.tensor(X_val_norm))

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=False)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)

    model = BehaviorAutoencoder(input_dim=len(available_cols), latent_dim=16)
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-5)
    criterion = nn.MSELoss()

    best_val_loss = float("inf")
    patience = 5
    epochs_no_improve = 0

    print(f"\n--- Training Behavior Autoencoder (Features: {len(available_cols)}) ---")

    for epoch in range(1, 31):
        model.train()
        train_loss = 0.0
        for (batch_x,) in train_loader:
            optimizer.zero_grad()
            reconstructed = model(batch_x)
            loss = criterion(reconstructed, batch_x)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * len(batch_x)

        avg_train_loss = train_loss / len(X_train_norm)

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for (batch_x,) in val_loader:
                reconstructed = model(batch_x)
                loss = criterion(reconstructed, batch_x)
                val_loss += loss.item() * len(batch_x)

        avg_val_loss = val_loss / len(X_val_norm)

        print(f"Epoch [{epoch}/30] | Train Loss: {avg_train_loss:.6f} | Val Loss: {avg_val_loss:.6f}")

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            epochs_no_improve = 0
            torch.save(model.state_dict(), save_path)
            print(f"--> Saved best autoencoder model to {save_path}")
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                print(f"Early stopping triggered at epoch {epoch}.")
                break


if __name__ == "__main__":
    train_autoencoder_model()
