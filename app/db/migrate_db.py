from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.model.model import Base
from app.config import INIT_DATABASE_URL

engine = create_engine(INIT_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def reset_database():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    if "users" in existing_tables:
        print("✅ Database already initialized. Skipping reset.")
        return
    
    print("📦 Resetting database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_database()
