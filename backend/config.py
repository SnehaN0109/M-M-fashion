import os
from pathlib import Path
from sqlalchemy.engine import URL
from dotenv import load_dotenv

# Load .env from the backend directory regardless of where python is launched from
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

class Config:
    SQLALCHEMY_DATABASE_URI = URL.create(
        "mysql+pymysql",
        username=os.getenv("DB_USERNAME", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME", "mmfashion")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    # Aiven cloud MySQL requires SSL
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {}
        }
    }
