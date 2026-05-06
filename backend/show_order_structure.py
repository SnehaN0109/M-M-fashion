#!/usr/bin/env python3
"""Show complete order table structure."""
import sys
sys.path.insert(0, '.')

from app import create_app
from models import db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    columns = inspector.get_columns('order')
    
    print('=' * 90)
    print('COMPLETE "ORDER" TABLE STRUCTURE')
    print('=' * 90)
    print(f"{'#':<4} {'Column Name':<30} {'Type':<20} {'Nullable':<10} {'Default':<15}")
    print('=' * 90)
    
    for i, col in enumerate(columns, 1):
        nullable = 'YES' if col['nullable'] else 'NO'
        default = str(col['default']) if col['default'] else '-'
        if len(default) > 15:
            default = default[:12] + '...'
        print(f"{i:<4} {col['name']:<30} {str(col['type']):<20} {nullable:<10} {default:<15}")
    
    print('=' * 90)
    print(f'Total columns: {len(columns)}')
    print('=' * 90)
    
    # Highlight payment fields
    print('\n📋 PAYMENT-RELATED FIELDS:')
    print('-' * 90)
    payment_cols = ['payment_method', 'payment_status', 'payment_proof']
    for col in columns:
        if col['name'] in payment_cols:
            nullable = 'YES' if col['nullable'] else 'NO'
            default = str(col['default']) if col['default'] else '-'
            print(f"  • {col['name']:<25} {str(col['type']):<20} Nullable: {nullable:<5} Default: {default}")
    
    # Show indexes
    print('\n🔑 INDEXES:')
    print('-' * 90)
    indexes = inspector.get_indexes('order')
    if indexes:
        for idx in indexes:
            print(f"  • {idx['name']}: {', '.join(idx['column_names'])}")
    else:
        print("  No indexes found (besides primary key)")
    
    # Show foreign keys
    print('\n🔗 FOREIGN KEYS:')
    print('-' * 90)
    fks = inspector.get_foreign_keys('order')
    if fks:
        for fk in fks:
            print(f"  • {fk['constrained_columns'][0]} → {fk['referred_table']}.{fk['referred_columns'][0]}")
    else:
        print("  No foreign keys found")
    
    print('\n' + '=' * 90)
