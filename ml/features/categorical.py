"""
Categorical feature engineering module for CyberTwin AI.
Provides feature hashing trick, ordinal indexing, and categorical encoding utilities.
"""
import zlib
import numpy as np
import pandas as pd


class FeatureHasher:
    """
    Implements deterministic feature hashing (Hashing Trick) for high-cardinality discrete columns.
    Maps string tokens into fixed-size integer slots [0, num_features - 1].
    """

    def __init__(self, num_features: int = 1024):
        self.num_features = num_features

    def _hash_str(self, val: str) -> int:
        if pd.isna(val) or val is None:
            val = "__UNKNOWN__"
        return zlib.crc32(str(val).encode("utf-8")) % self.num_features

    def transform_column(self, series: pd.Series, col_name: str = "") -> pd.Series:
        """Hashes a pandas Series into integer bin indices."""
        prefix = f"{col_name}:" if col_name else ""
        return series.apply(lambda x: self._hash_str(f"{prefix}{x}"))


class OrdinalCategoricalEncoder:
    """
    Fits and maps string category labels into dense integer indices with handling for unknown tokens.
    """

    def __init__(self, unknown_index: int = 0):
        self.unknown_index = unknown_index
        self.mapping: dict[str, int] = {}
        self.reverse_mapping: dict[int, str] = {}

    def fit(self, series: pd.Series) -> "OrdinalCategoricalEncoder":
        """Fits vocabulary from categorical series."""
        unique_vals = series.dropna().astype(str).unique()
        self.mapping = {val: idx + 1 for idx, val in enumerate(sorted(unique_vals))}
        self.reverse_mapping = {idx: val for val, idx in self.mapping.items()}
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        """Transforms series using fitted mapping."""
        return series.astype(str).map(self.mapping).fillna(self.unknown_index).astype(int)

    def fit_transform(self, series: pd.Series) -> pd.Series:
        return self.fit(series).transform(series)


def encode_categorical_features(
    df: pd.DataFrame,
    categorical_cols: list[str] | None = None,
    num_hash_bins: int = 256
) -> pd.DataFrame:
    """
    Hashes specified categorical columns into hashed numerical columns.

    Args:
        df: Input DataFrame.
        categorical_cols: List of column names to encode. If None, defaults to common event fields.
        num_hash_bins: Number of hash bins for modulo hashing.

    Returns:
        DataFrame with added `<col>_hash` columns.
    """
    df = df.copy()
    if categorical_cols is None:
        categorical_cols = ["event_type", "action", "ip_address", "device_id", "geo_location"]

    hasher = FeatureHasher(num_features=num_hash_bins)

    for col in categorical_cols:
        if col in df.columns:
            df[f"{col}_hash"] = hasher.transform_column(df[col], col_name=col)

    return df
