"""
Database migration to add email column to user table.
Run this once to add email support to existing users.
Usage: python migrate_email.py
"""
from app import create_app
from models import db
from sqlalchemy import text

def migrate_email_column():
    """Add email column to user table if it doesn't exist."""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if email column already exists
            result = db.session.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'user' 
                AND COLUMN_NAME = 'email'
                AND TABLE_SCHEMA = DATABASE()
            """))
            
            if result.fetchone():
                print("✅ Email column already exists in user table")
                return
            
            # Add email column
            print("📧 Adding email column to user table...")
            db.session.execute(text("""
                ALTER TABLE user 
                ADD COLUMN email VARCHAR(120) NULL UNIQUE
            """))
            db.session.commit()
            
            print("✅ Email column added successfully!")
            print("📋 Updated user table schema:")
            
            # Show updated table structure
            result = db.session.execute(text("""
                DESCRIBE user
            """))
            
            for row in result:
                print(f"   {row[0]}: {row[1]} {row[2]} {row[3]}")
                
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    migrate_email_column()