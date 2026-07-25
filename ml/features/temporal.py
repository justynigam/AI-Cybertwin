import numpy as np
import pandas as pd

def engineer_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms raw timestamps into continuous, cyclical ML features.
    """
    print("Engineering temporal features...")
    
    # 1. Convert to Datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 2. Extract standard temporal data
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # 3. Cyclical Encoding (The Staff Engineer way)
    # 24 hours in a day
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24.0)
    
    # 7 days in a week
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7.0)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7.0)
    
    return df

def engineer_behavioral_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates stateful features like 'time since last event'.
    Requires sorting by User and Time first!
    """
    print("Engineering stateful behavioral features...")
    
    # MUST sort to calculate sequential behavior correctly
    df = df.sort_values(by=['user_id', 'timestamp'])
    
    # Calculate time difference between events for the SAME user
    df['time_since_last_event_seconds'] = df.groupby('user_id')['timestamp'].diff().dt.total_seconds()
    
    # Fill the first event for a user with -1 (Cold Start indicator)
    df['time_since_last_event_seconds'] = df['time_since_last_event_seconds'].fillna(-1)
    
    # Example: Rolling count of events per user in the last hour
    # Note: In production real-time, this is fetched from Redis. Here we simulate it.
    df = df.set_index('timestamp')
    df['events_last_1hr'] = df.groupby('user_id')['event_id'].rolling('1h').count().reset_index(level=0, drop=True)
    df = df.reset_index()

    return df

# --- Usage Example ---
if __name__ == "__main__":
    # Load raw data from Phase 6
    df = pd.read_json('../../synthetic_data/output/events.json', lines=True)
    
    # Apply pipelines
    df = engineer_temporal_features(df)
    df = engineer_behavioral_features(df)
    
    print(df[['user_id', 'timestamp', 'hour_sin', 'time_since_last_event_seconds', 'events_last_1hr']].head())