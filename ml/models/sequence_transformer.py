import math
import torch
import torch.nn as nn
from ml.models.positional_encoding import PositionalEncoding


class CyberSequenceTransformer(nn.Module):
    def __init__(self, feature_dim: int, d_model: int = 128, nhead: int = 8, 
                 num_layers: int = 4, num_classes: int = 1, dropout: float = 0.1):
        super().__init__()
        
        # 1. Project raw features into a higher-dimensional embedding space
        self.input_projection = nn.Linear(feature_dim, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        
        # 2. Transformer Encoder Blocks
        encoder_layers = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead, dropout=dropout, batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)
        
        # 3. Classification Head (Outputs Risk Score or Attack Class)
        self.classifier = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, num_classes),
            nn.Sigmoid() # Use Sigmoid for Binary Risk Score (0 to 1)
        )

    def forward(self, src, src_key_padding_mask=None):
        """
        src shape: [Batch_Size, Seq_Length, Feature_Dim]
        """
        # Embed and add positional context
        x = self.input_projection(src)
        x = self.pos_encoder(x.transpose(0, 1)).transpose(0, 1) # Handle batch_first
        
        # Pass through Transformer
        encoded_seq = self.transformer_encoder(x, src_key_padding_mask=src_key_padding_mask)
        
        # For sequence classification, we typically grab the output of the LAST event
        # (or use global average pooling across the sequence)
        last_event_state = encoded_seq[:, -1, :] 
        
        # Calculate Risk Score
        risk_score = self.classifier(last_event_state)
        return risk_score
