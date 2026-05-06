#!/usr/bin/env python3
"""Verify payment fields in order table and test with sample data."""
import sys
sys.path.insert(0, '.')

from app import create_app
from models import db, Order
from sqlalchemy import inspect, text

app = create_app()
with app.app_context():
    print('=' * 80)
    print('PAYMENT FIELDS VERIFICATION REPORT')
    print('=' * 80)
    
    # 1. Check database schema
    inspector = inspect(db.engine)
    columns = inspector.get_columns('order')
    column_dict = {col['name']: col for col in columns}
    
    print('\n1. DATABASE SCHEMA CHECK')
    print('-' * 80)
    
    payment_fields = ['payment_method', 'payment_status', 'payment_proof']
    for field in payment_fields:
        if field in column_dict:
            col = column_dict[field]
            nullable = 'NULL' if col['nullable'] else 'NOT NULL'
            default = f" (default: {col['default']})" if col['default'] else ''
            print(f"✅ {field:<20} {str(col['type']):<20} {nullable}{default}")
        else:
            print(f"❌ {field:<20} MISSING")
    
    # 2. Check SQLAlchemy model
    print('\n2. SQLALCHEMY MODEL CHECK')
    print('-' * 80)
    
    model_columns = Order.__table__.columns
    for field in payment_fields:
        if field in model_columns:
            col = model_columns[field]
            col_type = str(col.type)
            nullable = 'NULL' if col.nullable else 'NOT NULL'
            default = f" (default: {col.default.arg if col.default else 'None'})" if col.default else ''
            print(f"✅ {field:<20} {col_type:<20} {nullable}{default}")
        else:
            print(f"❌ {field:<20} MISSING")
    
    # 3. Check existing orders
    print('\n3. EXISTING ORDERS CHECK')
    print('-' * 80)
    
    total_orders = Order.query.count()
    print(f"Total orders in database: {total_orders}")
    
    if total_orders > 0:
        # Check sample orders
        sample_orders = Order.query.limit(5).all()
        print(f"\nSample orders (showing first {len(sample_orders)}):")
        print(f"{'Order ID':<10} {'Payment Method':<15} {'Payment Status':<15} {'Has Proof':<10}")
        print('-' * 80)
        for order in sample_orders:
            has_proof = 'Yes' if order.payment_proof else 'No'
            print(f"{order.id:<10} {order.payment_method or 'N/A':<15} {order.payment_status or 'N/A':<15} {has_proof:<10}")
        
        # Statistics
        print('\nPayment Statistics:')
        cod_count = Order.query.filter_by(payment_method='COD').count()
        upi_count = Order.query.filter_by(payment_method='UPI').count()
        pending_count = Order.query.filter_by(payment_status='PENDING').count()
        verified_count = Order.query.filter_by(payment_status='VERIFIED').count()
        
        print(f"  COD orders: {cod_count}")
        print(f"  UPI orders: {upi_count}")
        print(f"  Pending payment: {pending_count}")
        print(f"  Verified payment: {verified_count}")
    else:
        print("No orders found in database.")
    
    # 4. Final verdict
    print('\n' + '=' * 80)
    print('FINAL VERDICT')
    print('=' * 80)
    
    all_exist = all(field in column_dict for field in payment_fields)
    model_match = all(field in model_columns for field in payment_fields)
    
    if all_exist and model_match:
        print('✅ SUCCESS: All payment fields exist in both database and model')
        print('✅ No migration needed - schema is up to date')
    else:
        print('❌ ISSUE: Some payment fields are missing')
        print('⚠️  Migration required')
    
    print('=' * 80)
