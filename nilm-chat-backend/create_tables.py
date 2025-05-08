# create_tables.py
from app.database import Base, engine
from app.models.electrical_data import ElectricalData  # Import your model

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")

if __name__ == "__main__":
    create_tables()