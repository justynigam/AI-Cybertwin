"""
Positional encoding module for PyTorch sequence models in CyberTwin AI.
Injects sinusoidal positional embeddings to give sequence models temporal ordering awareness.
"""
import math
import torch
import torch.nn as nn


class PositionalEncoding(nn.Module):
    """
    Transformers have no inherent sense of order. We must inject positional 
    information mathematically so it knows Event 1 happened before Event 2.
    """
    def __init__(self, d_model: int, max_len: int = 5000):
        super().__init__()
        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape: [Sequence_Length, Batch_Size, Embedding_Dim]
        x = x + self.pe[:x.size(0)]
        return x
