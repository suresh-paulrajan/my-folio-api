from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Local Config
# DB_USER = os.getenv("DB_USER", "root")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "P%40ssw0rd")
# DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
# DB_NAME = os.getenv("DB_NAME", "myfolio")

# PROD Config
DB_USER = os.getenv("DB_USER", "catalvka_bizbot_poc_dba")
DB_PASSWORD = os.getenv("DB_PASSWORD", "BahV3s#7^Q&E")
DB_HOST = os.getenv("DB_HOST", "162.241.123.136")
DB_NAME = os.getenv("DB_NAME", "catalvka_bizbot_poc")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()