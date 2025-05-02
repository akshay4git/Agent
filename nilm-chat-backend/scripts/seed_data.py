import sys
import os
import pandas as pd
from datetime import datetime, timedelta
import random

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine, Base, SessionLocal
from app.models.electrical_data import ElectricalData

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Generate sample data
def generate_sample_data(num_rows=1000):
    db = SessionLocal()
    
    try:
        # Base timestamp (start from 24 hours ago)
        base_timestamp = datetime.now() - timedelta(days=1)
        
        # Define cluster parameters (simplified version)
        clusters = {
            0: {"power_range": (5, 30), "thd_range": (1, 3), "pf_range": (0.95, 1.0)},   # Background power
            1: {"power_range": (80, 200), "thd_range": (3, 8), "pf_range": (0.65, 0.85)},  # Refrigerator
            2: {"power_range": (10, 100), "thd_range": (10, 25), "pf_range": (0.5, 0.95)},  # Lighting
            3: {"power_range": (30, 150), "thd_range": (15, 35), "pf_range": (0.6, 0.9)},   # Electronics
            4: {"power_range": (500, 1500), "thd_range": (5, 15), "pf_range": (0.8, 0.95)},  # Kitchen appliances
            5: {"power_range": (800, 2500), "thd_range": (2, 10), "pf_range": (0.7, 0.9)},   # HVAC
            6: {"power_range": (1500, 4000), "thd_range": (1, 5), "pf_range": (0.9, 1.0)},   # Water heating
            7: {"power_range": (300, 2000), "thd_range": (5, 20), "pf_range": (0.6, 0.85)}   # Large appliances
        }
        
        # Generate data rows
        for i in range(num_rows):
            # Select random cluster (weighted to have more common devices)
            weights = [0.2, 0.15, 0.15, 0.15, 0.1, 0.1, 0.1, 0.05]
            cluster = random.choices(list(clusters.keys()), weights=weights)[0]
            
            # Get parameters for this cluster
            params = clusters[cluster]
            
            # Generate power in watts
            power_watts = random.uniform(*params["power_range"])
            
            # Calculate other values
            voltage = random.uniform(215, 235)
            power_factor = random.uniform(*params["pf_range"])
            thd = random.uniform(*params["thd_range"])
            
            # Calculate derived values
            real_power = power_watts / 1000  # Convert to kW
            apparent_power = real_power / power_factor if power_factor > 0 else 0
            reactive_power = (apparent_power**2 - real_power**2)**0.5 if apparent_power > real_power else 0
            current = (apparent_power * 1000) / voltage if voltage > 0 else 0
            
            # Create timestamp with some randomness
            timestamp = base_timestamp + timedelta(
                seconds=i * 5 + random.randint(-2, 2)
            )
            
            # Create record
            record = ElectricalData(
                timestamp=timestamp,
                voltage=voltage,
                current=current,
                real_power=real_power,
                reactive_power=reactive_power,
                apparent_power=apparent_power,
                power_factor=power_factor,
                frequency=50 + random.uniform(-0.2, 0.2),
                thd=thd,
                real_power_watt=power_watts,
                cluster=cluster
            )
            
            db.add(record)
        
        # Commit all records
        db.commit()
        print(f"Added {num_rows} sample electrical records")
        
    except Exception as e:
        print(f"Error seeding data: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Default to 1000 rows if no argument is provided
    num_rows = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    generate_sample_data(num_rows)