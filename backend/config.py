import os
from pathlib import Path
from sqlalchemy.engine import URL
from dotenv import load_dotenv

# Load .env from the backend directory regardless of where python is launched from, override any system env vars
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

def _build_db_uri():
    """Build the DB URI. Adds SSL for Aiven cloud (DB_USE_SSL=true)."""
    return URL.create(
        "mysql+pymysql",
        username=os.getenv("DB_USERNAME", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME", "mmfashion"),
    )


class Config:
    SQLALCHEMY_DATABASE_URI = _build_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # Aiven cloud MySQL SSL configuration
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ssl_verify_cert": False,
                "ssl_verify_identity": False
            } if os.getenv("DB_USE_SSL", "false").lower() == "true" else {}
        }
    }
    
    # Flask-Mail configuration for Gmail SMTP
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')
    MAIL_DEFAULT_SENDER = os.getenv('EMAIL_USER')
