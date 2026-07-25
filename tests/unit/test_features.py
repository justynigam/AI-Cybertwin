"""
Unit tests for ML feature engineering transformations.
"""
import numpy as np
import pandas as pd
from ml.features.temporal import engineer_temporal_features
from ml.features.spatial import haversine_distance, calculate_spatial_velocity
from ml.features.categorical import FeatureHasher


def test_temporal_feature_encoding():
    df = pd.DataFrame([{
        "timestamp": "2026-07-25T12:00:00Z"
    }])
    encoded_df = engineer_temporal_features(df)

    assert "hour_sin" in encoded_df.columns
    assert "hour_cos" in encoded_df.columns
    assert "day_sin" in encoded_df.columns
    assert "day_cos" in encoded_df.columns

    # 12:00 UTC corresponds to sin(pi) ~ 0, cos(pi) ~ -1
    assert np.isclose(encoded_df["hour_sin"].iloc[0], 0.0, atol=1e-5)
    assert np.isclose(encoded_df["hour_cos"].iloc[0], -1.0, atol=1e-5)


def test_haversine_distance_calculation():
    # New York (40.7128, -74.0060) to London (51.5074, -0.1278) ~ 5570 km
    dist = haversine_distance(40.7128, -74.0060, 51.5074, -0.1278)
    assert 5500 < dist < 5650


def test_feature_hasher():
    hasher = FeatureHasher(num_features=100)
    hashed_val1 = hasher.transform_column(pd.Series(["192.168.1.1"])).iloc[0]
    hashed_val2 = hasher.transform_column(pd.Series(["192.168.1.1"])).iloc[0]

    assert 0 <= hashed_val1 < 100
    assert hashed_val1 == hashed_val2
