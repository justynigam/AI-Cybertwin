"""
Window generator and sequence dataset utilities for CyberTwin AI.
Converts tabular event data into sliding window sequence tensors for PyTorch sequence transformers.
"""
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader


class SlidingWindowSequenceDataset(Dataset):
    """
    PyTorch Dataset that creates sliding window sequences of length `window_size`
    grouped by entity (e.g., user_id).
    """

    def __init__(
        self,
        df: pd.DataFrame,
        feature_cols: list[str],
        group_col: str = "user_id",
        label_col: str = "is_attack",
        window_size: int = 10,
        stride: int = 1
    ):
        self.window_size = window_size
        self.stride = stride
        self.sequences = []
        self.labels = []

        # Sort temporally per user group
        df_sorted = df.sort_values(by=[group_col, "timestamp"])

        for _, user_df in df_sorted.groupby(group_col):
            features = user_df[feature_cols].fillna(0.0).values.astype(np.float32)
            targets = user_df[label_col].values.astype(np.float32) if label_col in user_df.columns else np.zeros(len(user_df))

            num_events = len(features)
            if num_events < window_size:
                # Pad sequence if user has fewer events than window size
                pad_len = window_size - num_events
                padded_features = np.pad(features, ((pad_len, 0), (0, 0)), mode="constant")
                self.sequences.append(padded_features)
                self.labels.append(targets[-1])
            else:
                for i in range(0, num_events - window_size + 1, stride):
                    seq = features[i : i + window_size]
                    label = targets[i + window_size - 1]
                    self.sequences.append(seq)
                    self.labels.append(label)

        self.sequences = torch.tensor(np.array(self.sequences), dtype=torch.float32)
        self.labels = torch.tensor(np.array(self.labels), dtype=torch.float32).unsqueeze(1)

    def __len__(self) -> int:
        return len(self.sequences)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.sequences[idx], self.labels[idx]


def create_sliding_window_dataloader(
    df: pd.DataFrame,
    feature_cols: list[str],
    window_size: int = 10,
    batch_size: int = 32,
    shuffle: bool = True
) -> DataLoader:
    """
    Helper function to generate a PyTorch DataLoader yielding sliding sequence batches.
    """
    dataset = SlidingWindowSequenceDataset(
        df=df,
        feature_cols=feature_cols,
        window_size=window_size
    )
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
