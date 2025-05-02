import sys
import os
import pandas as pd
from datetime import datetime
import argparse

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine, Base, SessionLocal
from app.models.electrical_data import ElectricalData

def import_csv_data(file_path, limit=None):
    """Import data from CSV file into the database"""
    print(f"Importing data from {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        return
    
    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
        print(f"Read {len(df)} rows from CSV")
        
        # Apply limit if specified
        if limit and limit > 0:
            df = df.head(limit)
            print(f"Limited to {limit} rows")
        
        # Connect to database
        db = SessionLocal()
        
        try:
            # Process each row and insert into database
            count = 0
            for _, row in df.iterrows():
                # Parse datetime
                try:
                    timestamp = datetime.strptime(row['DateTime'], '%Y-%m-%d %H:%M:%S')
                except:
                    timestamp = datetime.now()
                
                # Create new record
                record = ElectricalData(
                    timestamp=timestamp,
                    voltage=float(row['Voltage']),
                    current=float(row['Current']),
                    real_power=float(row['Real Power']),
                    reactive_power=float(row['Reactive Power']),
                    apparent_power=float(row['Apparent Power']),
                    power_factor=float(row['Power Factor']),
                    frequency=float(row['Frequency']) if not pd.isna(row['Frequency']) else None,
                    thd=float(row['THD']),
                    real_power_watt=float(row['Real Power (W)']),
                    cluster=int(row['Cluster'])
                )
                
                db.add(record)
                count += 1
                
                # Commit in batches to avoid memory issues
                if count % 1000 == 0:
                    db.commit()
                    print(f"Imported {count} rows...")
            
            # Final commit for remaining records
            db.commit()
            print(f"Successfully imported {count} records")
            
        except Exception as e:
            print(f"Error during import: {str(e)}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import electrical data from CSV file')
    parser.add_argument('"C:\Users\DELL\OneDrive\Desktop\AkshayCsio\clustered_data_full_features.csv"', help='Path to the CSV file')
    parser.add_argument('--limit', type=int, help='Limit the number of rows to import')
    
    args = parser.parse_args()
    import_csv_data(args.file_path, args.limit)