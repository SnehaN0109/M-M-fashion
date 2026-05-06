#!/usr/bin/env python3
"""Check existing columns in order table."""
import sys
sys.path.insert(0, '.')

from app import create_app
from models import db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    columns = inspector.get_columns('order')
    
    print('Current columns in "order" table:')
    print('=' * 70)
    for col in columns:
        nullable = 'NULL' if col['nullable'] else 'NOT NULL'
        default = f" DEFAULT: {col['default']}" if col['default'] else ''
        print(f"{col['name']:<30} {str(col['type']):<20} {nullable}{default}")
    
    print('\n' + '=' * 70)
    print(f'Total columns: {len(columns)}')
    
    # Check for payment fields
    column_names = [col['name'] for col in columns]
    print('\nPayment field status:')
    print(f"  payment_status: {'✅ EXISTS' if 'payment_status' in column_names else '❌ MISSING'}")
    print(f"  payment_proof:  {'✅ EXISTS' if 'payment_proof' in column_names else '❌ MISSING'}")
    print(f"  payment_method: {'✅ EXISTS' if 'payment_method' in column_names else '❌ MISSING'}")
