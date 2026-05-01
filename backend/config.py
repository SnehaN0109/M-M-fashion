import os
from pathlib import Path
from sqlalchemy.engine import URL
from dotenv import load_dotenv

# Always load .env relative to this file, override any system env vars
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

def _build_db_uri():
    """Build the DB URI. Adds SSL for Aiven cloud (DB_USE_SSL=true)."""
    query = {}
    if os.getenv("DB_USE_SSL", "false").lower() == "true":
        # Aiven SSL with relaxed verification for certificate issues
        query = {
            "ssl_disabled": "false",
            "ssl_verify_cert": "false", 
            "ssl_verify_identity": "false"
        }

    return URL.create(
        "mysql+pymysql",
        username=os.getenv("DB_USERNAME", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME", "mmfashion"),
        query=query,
    )


class Config:
    SQLALCHEMY_DATABASE_URI = _build_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
