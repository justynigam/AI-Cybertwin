"""
Autoregressive PyTorch model for sequence forecasting in Behavioral Twin.
Predicts next-step probabilities over security action token vocabularies.
"""
import torch
import torch.nn as nn


class BehavioralAutoregressiveModel(nn.Module):
    """
    LSTM/Embedding autoregressive model predicting next token logits given sequence history.
    """

    def __init__(self, vocab_size: int = 200, embedding_dim: int = 64, hidden_dim: int = 128, num_layers: int = 2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True
        )
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        Input x: [Batch_Size, Sequence_Length]
        Output logits: [Batch_Size, Sequence_Length, Vocab_Size]
        """
        embeds = self.embedding(x)  # [Batch, Seq_Len, Embed_Dim]
        lstm_out, _ = self.lstm(embeds)  # [Batch, Seq_Len, Hidden_Dim]
        logits = self.fc(lstm_out)  # [Batch, Seq_Len, Vocab_Size]
        return logits
