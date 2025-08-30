from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load environment-specific .env file
env = os.getenv("ENV", "local")
if env == "prod":
	load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env.prod"))
else:
	load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env.local"))

# Get DB config from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()