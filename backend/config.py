import os
from sqlalchemy.engine import URL

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    SQLALCHEMY_DATABASE_URI = URL.create(
        "mysql+pymysql",
        username="root",
        password="Sneharoot@123",
        host="localhost",
        port=3306,
        database="mmfashion"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False