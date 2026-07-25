"""
Spatial feature extraction module for CyberTwin AI.
Calculates Haversine distance, travel velocity math, and coordinate resolution.
"""
import hashlib
import numpy as np
import pandas as pd


EARTH_RADIUS_KM = 6371.0


def haversine_distance(
    lat1: pd.Series | float,
    lon1: pd.Series | float,
    lat2: pd.Series | float,
    lon2: pd.Series | float
) -> pd.Series | float:
    """
    Computes the Haversine distance between pairs of (latitude, longitude) coordinates in kilometers.

    Args:
        lat1, lon1: Coordinates of initial point(s) in degrees.
        lat2, lon2: Coordinates of destination point(s) in degrees.

    Returns:
        Distance in kilometers.
    """
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)

    a = np.sin(delta_phi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2.0) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))

    return EARTH_RADIUS_KM * c


def resolve_geo_coordinates(
    df: pd.DataFrame,
    location_col: str = "geo_location",
    ip_col: str = "ip_address"
) -> pd.DataFrame:
    """
    Resolves location strings or IP addresses into deterministic (latitude, longitude) coordinates.
    Uses string hashing for consistent synthetic coordinate lookup.

    Args:
        df: Input DataFrame.
        location_col: City or region column.
        ip_col: IP address column.

    Returns:
        DataFrame with 'lat' and 'lon' float columns added.
    """
    df = df.copy()

    def string_to_lat_lon(val: str) -> tuple[float, float]:
        if not val or pd.isna(val):
            return (0.0, 0.0)
        h = int(hashlib.md5(str(val).encode('utf-8')).hexdigest(), 16)
        # Map hash to valid latitude (-90 to +90) and longitude (-180 to +180)
        lat = ((h % 1800000) / 10000.0) - 90.0
        lon = (((h // 1800000) % 3600000) / 10000.0) - 180.0
        return (lat, lon)

    locations = df[location_col].fillna(df[ip_col].astype(str))
    coords = locations.apply(string_to_lat_lon)

    df["lat"] = [c[0] for c in coords]
    df["lon"] = [c[1] for c in coords]

    return df


def calculate_spatial_velocity(
    df: pd.DataFrame,
    group_col: str = "user_id",
    timestamp_col: str = "timestamp",
    lat_col: str = "lat",
    lon_col: str = "lon"
) -> pd.DataFrame:
    """
    Calculates spatial distance (km) and travel velocity (km/h) between consecutive events for each user.

    Args:
        df: Input DataFrame containing lat, lon, timestamp, and group_col.
        group_col: Column to group user sessions/events by.
        timestamp_col: Timestamp column.
        lat_col: Latitude column.
        lon_col: Longitude column.

    Returns:
        DataFrame with 'distance_km', 'velocity_kmh', and 'is_impossible_travel' columns.
    """
    df = df.copy()
    
    # Ensure lat/lon exist
    if lat_col not in df.columns or lon_col not in df.columns:
        df = resolve_geo_coordinates(df)

    timestamps = pd.to_datetime(df[timestamp_col])
    df["_temp_dt"] = timestamps
    df = df.sort_values(by=[group_col, "_temp_dt"])

    # Shifted coordinates within user groups
    prev_lat = df.groupby(group_col)[lat_col].shift(1)
    prev_lon = df.groupby(group_col)[lon_col].shift(1)
    prev_dt = df.groupby(group_col)["_temp_dt"].shift(1)

    # Compute distance
    dist = haversine_distance(prev_lat, prev_lon, df[lat_col], df[lon_col]).fillna(0.0)
    df["distance_km"] = dist

    # Compute time delta in hours
    time_delta_hours = (df["_temp_dt"] - prev_dt).dt.total_seconds() / 3600.0
    time_delta_hours = time_delta_hours.fillna(0.0)

    # Compute velocity (km/h) safely
    velocity = np.where(time_delta_hours > 0, dist / time_delta_hours, 0.0)
    df["velocity_kmh"] = np.nan_to_num(velocity, nan=0.0, posinf=0.0, neginf=0.0)

    # Flag velocity anomalies (> 800 km/h commercial flight threshold)
    df["is_impossible_travel_math"] = (df["velocity_kmh"] > 800.0).astype(int)

    df = df.drop(columns=["_temp_dt"])
    return df
