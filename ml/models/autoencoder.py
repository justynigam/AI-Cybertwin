import torch
import torch.nn as nn

class BehaviorAutoencoder(nn.Module):
    def __init__(self, input_dim: int, latent_dim: int = 16):
        super(BehaviorAutoencoder, self).__init__()
        
        # Encoder: Compresses the behavioral features
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            
            nn.Linear(32, latent_dim),
            nn.ReLU() # Latent bottleneck
        )
        
        # Decoder: Attempts to reconstruct the features
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            nn.Linear(32, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            
            nn.Linear(64, input_dim),
            nn.Sigmoid() # Assumes inputs are scaled between 0 and 1
        )

    def forward(self, x):
        latent = self.encoder(x)
        reconstructed = self.decoder(latent)
        return reconstructed
    
    def compute_anomaly_score(self, x):
        """
        Runs inference and returns the Mean Squared Error per row.
        High error = High Anomaly/Risk.
        """
        self.eval() # Ensure dropout is disabled during inference
        with torch.no_grad():
            reconstructed = self.forward(x)
            # MSE loss per sample
            mse = torch.mean((x - reconstructed) ** 2, dim=1)
        return mse