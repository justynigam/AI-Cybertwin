import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import logging
from sklearn.metrics import f1_score, precision_score, recall_score
import numpy as np
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ml.models.sequence_transformer import CyberSequenceTransformer
from ml.data_loaders.window_generator import create_sliding_window_dataloader
from ml.features.temporal import engineer_temporal_features, engineer_behavioral_features
from ml.features.spatial import calculate_spatial_velocity
from ml.features.categorical import encode_categorical_features

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def train_transformer_model(model, train_loader, val_loader, epochs=30, patience=5):
    """
    Trains sequence transformer model with Early Stopping and BCEWithLogitsLoss.
    """
    optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-5)
    pos_weight = torch.tensor([10.0]) # Weight positive attack class
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    
    best_val_loss = float('inf')
    epochs_no_improve = 0
    weights_dir = os.path.join(project_root, "ml", "weights")
    os.makedirs(weights_dir, exist_ok=True)
    best_model_path = os.path.join(weights_dir, "best_transformer.pt")
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        
        for batch_idx, (sequences, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(sequences)
            loss = criterion(outputs.squeeze(), labels.float().squeeze())
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            train_loss += loss.item()
            
        avg_train_loss = train_loss / max(len(train_loader), 1)
        
        model.eval()
        val_loss = 0.0
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            for sequences, labels in val_loader:
                outputs = model(sequences)
                loss = criterion(outputs.squeeze(), labels.float().squeeze())
                val_loss += loss.item()
                
                probs = torch.sigmoid(outputs).squeeze()
                preds = (probs > 0.5).int().cpu().numpy()
                
                if np.isscalar(preds):
                    all_preds.append(preds)
                else:
                    all_preds.extend(preds)

                target_labels = labels.cpu().numpy().squeeze()
                if np.isscalar(target_labels):
                    all_labels.append(target_labels)
                else:
                    all_labels.extend(target_labels)
                
        avg_val_loss = val_loss / max(len(val_loader), 1)
        
        val_f1 = f1_score(all_labels, all_preds, zero_division=0)
        val_prec = precision_score(all_labels, all_preds, zero_division=0)
        val_recall = recall_score(all_labels, all_preds, zero_division=0)
        
        logging.info(f"Epoch {epoch+1}/{epochs} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")
        logging.info(f"Val F1: {val_f1:.4f} | Precision: {val_prec:.4f} | Recall: {val_recall:.4f}")
        
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            epochs_no_improve = 0
            torch.save(model.state_dict(), best_model_path)
            logging.info(f"--> Model improved and saved to {best_model_path}")
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                logging.warning(f"Early stopping triggered after {epoch+1} epochs.")
                break


if __name__ == "__main__":
    data_path = os.path.join(project_root, "ml", "data", "raw", "events.json")
    if os.path.exists(data_path):
        print("\n--- Chronological Split & Sequence Transformer Training ---")
        df = pd.read_json(data_path, lines=True)
        df = engineer_temporal_features(df)
        df = engineer_behavioral_features(df)
        df = calculate_spatial_velocity(df)
        df = encode_categorical_features(df)

        df_sorted = df.sort_values("timestamp")
        split_idx = int(len(df_sorted) * 0.8)
        train_df = df_sorted.iloc[:split_idx]
        val_df = df_sorted.iloc[split_idx:]

        # STRICT FEATURE HYGIENE - Exclude all target labels
        leak_cols = ["is_attack", "attack_category", "event_id", "timestamp", "user_id", "is_impossible_travel_math"]
        pure_feature_cols = [
            "hour_sin", "hour_cos", "day_sin", "day_cos", "is_weekend",
            "time_since_last_event_seconds", "events_last_1hr",
            "distance_km", "velocity_kmh",
            "event_type_hash", "action_hash", "ip_address_hash", "device_id_hash"
        ]
        available_cols = [c for c in pure_feature_cols if c in df.columns and c not in leak_cols]

        train_loader = create_sliding_window_dataloader(train_df, feature_cols=available_cols, window_size=5, batch_size=32)
        val_loader = create_sliding_window_dataloader(val_df, feature_cols=available_cols, window_size=5, batch_size=32)

        model = CyberSequenceTransformer(feature_dim=len(available_cols), d_model=64, nhead=4, num_layers=2)
        train_transformer_model(model, train_loader, val_loader, epochs=15, patience=4)
