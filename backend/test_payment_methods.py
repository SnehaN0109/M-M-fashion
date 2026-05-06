#!/usr/bin/env python3
"""Test all payment methods in checkout."""
import sys
sys.path.insert(0, '.')

from app import create_app
from models import db, Order, ProductVariant
import json

app = create_app()

def test_payment_method(method_name):
    """Test checkout with specific payment method."""
    
    with app.app_context():
        variant = ProductVariant.query.filter(ProductVariant.quantity > 0).first()
        if not variant:
            return False, "No variants available"
        
        test_payload = {
            "customer_name": f"Test {method_name}",
            "customer_email": "test@example.com",
            "customer_phone": "9876543210",
            "address_line1": "123 Test Street",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400001",
            "items": [{"variant_id": variant.id, "quantity": 1}],
            "domain": "garba.shop",
            "payment_method": method_name,
            "whatsapp_number": "9876543210"
        }
        
        with app.test_client() as client:
            response = client.post(
                '/api/orders/checkout',
                json=test_payload,
                content_type='application/json'
            )
            
            if response.status_code == 201:
                response_data = response.get_json()
                order_id = response_data.get('order_id')
                order = Order.query.get(order_id)
                
                # Verify
                checks = {
                    'payment_method_correct': order.payment_method == method_name,
                    'payment_status_pending': order.payment_status == 'PENDING',
                    'status_pending_payment': order.status == 'PENDING_PAYMENT',
                    'response_has_order_id': 'order_id' in response_data,
                    'response_has_payment_status': 'payment_status' in response_data,
                    'response_has_payment_method': 'payment_method' in response_data,
                }
                
                # Clean up
                db.session.delete(order)
                db.session.commit()
                
                return all(checks.values()), checks
            else:
                return False, {"error": response.get_json()}

def main():
    print('=' * 80)
    print('PAYMENT METHODS TEST SUITE')
    print('=' * 80)
    
    payment_methods = ['COD', 'UPI', 'BANK_TRANSFER', 'CARD']
    results = {}
    
    for method in payment_methods:
        print(f'\n📋 Testing: {method}')
        print('-' * 80)
        
        success, details = test_payment_method(method)
        results[method] = success
        
        if success:
            print(f'✅ {method}: PASSED')
            print('   All checks passed:')
            for check, passed in details.items():
                print(f'     • {check}: {"✅" if passed else "❌"}')
        else:
            print(f'❌ {method}: FAILED')
            print(f'   Details: {details}')
    
    # Summary
    print('\n' + '=' * 80)
    print('TEST SUMMARY')
    print('=' * 80)
    
    passed = sum(results.values())
    total = len(results)
    
    for method, success in results.items():
        status = '✅ PASS' if success else '❌ FAIL'
        print(f'{method:<20} {status}')
    
    print('-' * 80)
    print(f'Total: {passed}/{total} passed')
    
    if passed == total:
        print('\n✅ ALL PAYMENT METHODS WORKING CORRECTLY')
        return True
    else:
        print(f'\n⚠️  {total - passed} payment method(s) failed')
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
