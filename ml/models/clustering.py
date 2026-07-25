"""
KMeans clustering module for behavioral role baselines in CyberTwin AI.
Groups users/devices into behavioral peer clusters and identifies cluster outliers.
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class RoleBaselineClustering:
    """
    KMeans clustering model for building peer behavioral baselines.
    """

    def __init__(self, n_clusters: int = 5, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        self.is_fitted = False

    def fit(self, X: np.ndarray | pd.DataFrame) -> "RoleBaselineClustering":
        """Fits standard scaler and KMeans model on feature matrix."""
        X_scaled = self.scaler.fit_transform(X)
        self.kmeans.fit(X_scaled)
        self.is_fitted = True
        return self

    def predict_cluster(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """Predicts cluster assignment for given feature matrix."""
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet. Call fit() first.")
        X_scaled = self.scaler.transform(X)
        return self.kmeans.predict(X_scaled)

    def compute_cluster_distance(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """
        Computes minimum Euclidean distance to assigned cluster centroid (anomaly indicator).
        """
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet. Call fit() first.")
        X_scaled = self.scaler.transform(X)
        distances = self.kmeans.transform(X_scaled)
        min_distances = np.min(distances, axis=1)
        return min_distances
