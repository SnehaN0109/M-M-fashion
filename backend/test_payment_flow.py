#!/usr/bin/env python3
"""Test payment flow in checkout endpoint."""
import sys
sys.path.insert(0, '.')

from app import create_app
from models import db, Order, ProductVariant
import json

app = create_app()

def test_checkout_payment_flow():
    """Test that checkout properly handles payment fields."""
    
    print('=' * 80)
    print('PAYMENT FLOW TEST')
    print('=' * 80)
    
    with app.app_context():
        # 1. Check if we have products with variants
        print('\n1. CHECKING TEST DATA AVAILABILITY')
        print('-' * 80)
        
        variant = ProductVariant.query.filter(ProductVariant.quantity > 0).first()
        if not variant:
            print('❌ No variants with stock available for testing')
            return False
        
        print(f'✅ Found test variant: ID={variant.id}, Stock={variant.quantity}')
        print(f'   Product: {variant.product.name}')
        print(f'   Color: {variant.color}, Size: {variant.size}')
        print(f'   Price B2C: ₹{variant.price_b2c}')
        
        # 2. Test checkout request payload
        print('\n2. TESTING CHECKOUT REQUEST')
        print('-' * 80)
        
        test_payload = {
            "customer_name": "Test Customer",
            "customer_email": "test@example.com",
            "customer_phone": "9876543210",
            "address_line1": "123 Test Street",
            "address_line2": "Apt 4B",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400001",
            "items": [
                {
                    "variant_id": variant.id,
                    "quantity": 1
                }
            ],
            "domain": "garba.shop",
            "payment_method": "UPI",  # Testing UPI payment
            "whatsapp_number": "9876543210"
        }
        
        print('Request payload:')
        print(json.dumps(test_payload, indent=2))
        
        # 3. Simulate checkout
        print('\n3. SIMULATING CHECKOUT')
        print('-' * 80)
        
        with app.test_client() as client:
            response = client.post(
                '/api/orders/checkout',
                json=test_payload,
                content_type='application/json'
            )
            
            print(f'Response Status: {response.status_code}')
            
            if response.status_code == 201:
                response_data = response.get_json()
                print('✅ Checkout successful!')
                print('\nResponse data:')
                print(json.dumps(response_data, indent=2))
                
                # 4. Verify order in database
                print('\n4. VERIFYING ORDER IN DATABASE')
                print('-' * 80)
                
                order_id = response_data.get('order_id')
                order = Order.query.get(order_id)
                
                if order:
                    print(f'✅ Order found in database: ID={order.id}')
                    print(f'\nOrder details:')
                    print(f'  Customer: {order.customer_name}')
                    print(f'  Email: {order.customer_email}')
                    print(f'  Phone: {order.customer_phone}')
                    print(f'  Total: ₹{order.total_amount}')
                    print(f'  Payment Method: {order.payment_method}')
                    print(f'  Payment Status: {order.payment_status}')
                    print(f'  Order Status: {order.status}')
                    print(f'  Created: {order.created_at}')
                    
                    # 5. Verify payment fields
                    print('\n5. VERIFYING PAYMENT FIELDS')
                    print('-' * 80)
                    
                    checks = []
                    
                    # Check payment_method
                    if order.payment_method == 'UPI':
                        print('✅ payment_method: UPI (correct)')
                        checks.append(True)
                    else:
                        print(f'❌ payment_method: {order.payment_method} (expected UPI)')
                        checks.append(False)
                    
                    # Check payment_status
                    if order.payment_status == 'PENDING':
                        print('✅ payment_status: PENDING (correct)')
                        checks.append(True)
                    else:
                        print(f'❌ payment_status: {order.payment_status} (expected PENDING)')
                        checks.append(False)
                    
                    # Check status
                    if order.status == 'PENDING_PAYMENT':
                        print('✅ status: PENDING_PAYMENT (correct)')
                        checks.append(True)
                    else:
                        print(f'❌ status: {order.status} (expected PENDING_PAYMENT)')
                        checks.append(False)
                    
                    # Check response includes required fields
                    if 'order_id' in response_data:
                        print('✅ Response includes: order_id')
                        checks.append(True)
                    else:
                        print('❌ Response missing: order_id')
                        checks.append(False)
                    
                    if 'payment_status' in response_data:
                        print('✅ Response includes: payment_status')
                        checks.append(True)
                    else:
                        print('❌ Response missing: payment_status')
                        checks.append(False)
                    
                    if 'payment_method' in response_data:
                        print('✅ Response includes: payment_method')
                        checks.append(True)
                    else:
                        print('❌ Response missing: payment_method')
                        checks.append(False)
                    
                    # Clean up test order
                    print('\n6. CLEANING UP TEST DATA')
                    print('-' * 80)
                    db.session.delete(order)
                    db.session.commit()
                    print('✅ Test order deleted')
                    
                    # Final verdict
                    print('\n' + '=' * 80)
                    print('FINAL VERDICT')
                    print('=' * 80)
                    
                    if all(checks):
                        print('✅ ALL TESTS PASSED')
                        print('✅ Payment flow is working correctly')
                        return True
                    else:
                        print(f'❌ SOME TESTS FAILED ({sum(checks)}/{len(checks)} passed)')
                        return False
                else:
                    print('❌ Order not found in database')
                    return False
            else:
                print(f'❌ Checkout failed with status {response.status_code}')
                print('Response:', response.get_json())
                return False

if __name__ == '__main__':
    success = test_checkout_payment_flow()
    sys.exit(0 if success else 1)
