import pandas as pd
import numpy as np
from tqdm import tqdm
import logging
from sqlalchemy.exc import IntegrityError

def import_csv_data(file_path, limit=None, batch_size=1000):
    from app.database import SessionLocal
    from app.models.electrical_data import ElectricalData

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    db = None
    try:
        # Read CSV with optimized data types
        df = pd.read_csv(
            file_path.strip().strip('"'),
            parse_dates=['DateTime'],
            dtype={
                'Voltage': 'float32',
                'Current': 'float32',
                'Real Power': 'float32',
                'Reactive Power': 'float32',
                'Apparent Power': 'float32',
                'Power Factor': 'float32',
                'Frequency': 'float32',
                'THD': 'float32',
                'Real Power (Watt)': 'float32',
                'Cluster': 'int32',
                'Device_State': 'string'
            }
        )

        if limit:
            df = df.head(limit)

        # Clean and validate data
        df['Device_State'] = df['Device_State'].str.strip()
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)  # drop rows with missing values

        df['Power Factor'] = df['Power Factor'].clip(-1, 1)
        df['Frequency'] = df['Frequency'].clip(45, 55)

        # Batch import
        db = SessionLocal()
        success_count = 0

        with tqdm(total=len(df), desc="Importing") as pbar:
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                records = [
                    ElectricalData(
                        timestamp=row['DateTime'],
                        voltage=row['Voltage'],
                        current=row['Current'],
                        real_power=row['Real Power'],
                        reactive_power=row['Reactive Power'],
                        apparent_power=row['Apparent Power'],
                        power_factor=row['Power Factor'],
                        frequency=row['Frequency'],
                        thd=row['THD'],
                        real_power_watt=row['Real Power (W)'],
                        cluster=int(row['Cluster']),
                        device_state=row['Device_State']
                    ) for _, row in batch.iterrows()
                ]
                try:
                    db.bulk_save_objects(records)
                    db.commit()
                    success_count += len(records)
                except IntegrityError as e:
                    db.rollback()
                    logger.error(f"Batch failed due to integrity error: {e}")
                except Exception as e:
                    db.rollback()
                    logger.error(f"Batch failed: {e}")
                pbar.update(len(batch))

        logger.info(f"✅ Success: {success_count}/{len(df)} rows")
        return success_count

    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        return 0
    finally:
        if db:
            db.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter the path to your CSV file: ").strip().strip('"')

    limit = None
    batch_size = 1000

    print(f"Starting import from: {file_path}")
    rows_imported = import_csv_data(file_path, limit, batch_size)
    print(f"Import complete. {rows_imported} rows imported successfully.")
