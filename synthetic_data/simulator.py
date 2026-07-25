import os
import random
import uuid
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

# Initialize Faker
fake = Faker()

# Configuration
NUM_USERS = 500  # Scaled down for quick testing; increase to 5000 later
DAYS_TO_SIMULATE = 5
OUTPUT_DIR = "output"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_mock_users(num_users):
    """Generates a base list of synthetic users."""
    users = []
    for _ in range(num_users):
        users.append({
            'id': str(uuid.uuid4()),
            'primary_device_id': str(uuid.uuid4()),
            'home_ip': fake.ipv4_public(),
            'home_city': fake.city()
        })
    return users

def generate_normal_login(user, current_time):
    """Generates a routine authentication log."""
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": user['id'],
        "device_id": user['primary_device_id'],
        "event_type": "AUTHENTICATION",
        "action": "LOGIN_SUCCESS",
        "timestamp": current_time.isoformat(),
        "ip_address": user['home_ip'],
        "geo_location": user['home_city'],
        "is_attack": False,
        "attack_category": "None"
    }

def inject_impossible_travel(user, current_time):
    """Injects an anomaly: User logs in from across the world 5 mins later."""
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": user['id'],
        "device_id": str(uuid.uuid4()), # Unrecognized device
        "event_type": "AUTHENTICATION",
        "action": "LOGIN_SUCCESS",
        "timestamp": (current_time + timedelta(minutes=5)).isoformat(),
        "ip_address": fake.ipv4_public(), # Malicious IP
        "geo_location": fake.city(),      # Malicious Location
        "is_attack": True,
        "attack_category": "Impossible Travel"
    }

def run_simulation(users):
    """The main time-series event loop."""
    events = []
    start_date = datetime.now() - timedelta(days=DAYS_TO_SIMULATE)
    
    print(f"Simulating data for {len(users)} users over {DAYS_TO_SIMULATE} days...")
    
    for user in users:
        # Simulate a daily morning login for each day
        for day in range(DAYS_TO_SIMULATE):
            current_time = start_date + timedelta(days=day, hours=random.randint(7, 10))
            
            # Normal Login
            events.append(generate_normal_login(user, current_time))
            
            # Inject anomaly (2% chance per day per user)
            if random.random() < 0.02: 
                events.append(inject_impossible_travel(user, current_time))
                
    return pd.DataFrame(events)

if __name__ == "__main__":
    # 1. Generate Base Entities
    print("Generating users...")
    mock_users = generate_mock_users(NUM_USERS)
    
    # 2. Run Simulation
    df_events = run_simulation(mock_users)
    
    # 3. Export to JSON (Line-delimited for streaming simulation)
    output_path = os.path.join(OUTPUT_DIR, "events.json")
    df_events.to_json(output_path, orient="records", lines=True)
    
    print(f"Successfully generated {len(df_events)} events.")
    print(f"Data saved to {output_path}")