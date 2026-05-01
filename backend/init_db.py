"""
Run this once to create all tables in the mmfashion database.
Usage: python init_db.py
"""
from app import create_app
from models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("All tables created successfully in mmfashion database.")
    
    # List created tables
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")
