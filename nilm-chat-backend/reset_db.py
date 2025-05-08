# reset_db.py

from app.database import engine
from app.models.electrical_data import ElectricalData
from sqlalchemy.orm import declarative_base

Base = ElectricalData.__bases__[0]

def reset_table():
    print("Dropping and recreating the 'electrical_data' table...")
    ElectricalData.__table__.drop(bind=engine, checkfirst=True)
    ElectricalData.__table__.create(bind=engine, checkfirst=True)
    print("✅ Table recreated successfully.")

if __name__ == "__main__":
    reset_table()
