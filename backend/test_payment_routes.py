#!/usr/bin/env python3
"""Test payment system routes."""
import sys
sys.path.insert(0, '.')

from app import create_app
from models import db, Order, ProductVariant, User
import json
import io

app = create_app()

def create_test_order():
    """Create a test order for payment testing."""
    with app.app_context():
        variant = ProductVariant.query.filter(ProductVariant.quantity > 0).first()
        if not variant:
            return None
        
        test_payload = {
            "customer_name": "Payment Test User",
            "customer_email": "payment@test.com",
            "customer_phone": "9876543210",
            "address_line1": "123 Test Street",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400001",
            "items": [{"variant_id": variant.id, "quantity": 1}],
            "domain": "garba.shop",
            "payment_method": "UPI",
            "whatsapp_number": "9876543210"
        }
        
        with app.test_client() as client:
            response = client.post(
                '/api/orders/checkout',
                json=test_payload,
                content_type='application/json'
            )
            
            if response.status_code == 201:
                return response.get_json()['order_id']
    return None


def test_user_upload_payment_proof(order_id):
    """Test user uploading payment proof."""
    print('\n1️⃣  TEST: User Upload Payment Proof')
    print('-' * 80)
    
    with app.test_client() as client:
        # Create a fake image file
        data = {
            'payment_proof': (io.BytesIO(b'fake image content'), 'payment.jpg'),
            'whatsapp_number': '9876543210'
        }
        
        response = client.post(
            f'/api/orders/{order_id}/mark-paid',
            data=data,
            content_type='multipart/form-data'
        )
        
        print(f'Status Code: {response.status_code}')
        result = response.get_json()
        print(f'Response: {json.dumps(result, indent=2)}')
        
        if response.status_code == 200:
            print('✅ Payment proof uploaded successfully')
            if result.get('payment_status') == 'PENDING':
                print('✅ Payment status remains PENDING (awaiting verification)')
                return True
            else:
                print(f'❌ Payment status should be PENDING, got: {result.get("payment_status")}')
                return False
        else:
            print('❌ Failed to upload payment proof')
            return False


def test_get_payment_status(order_id):
    """Test getting payment status."""
    print('\n2️⃣  TEST: Get Payment Status')
    print('-' * 80)
    
    with app.test_client() as client:
        response = client.get(
            f'/api/orders/{order_id}/payment-status?whatsapp_number=9876543210'
        )
        
        print(f'Status Code: {response.status_code}')
        result = response.get_json()
        print(f'Response: {json.dumps(result, indent=2)}')
        
        if response.status_code == 200:
            print('✅ Payment status retrieved successfully')
            if result.get('has_payment_proof'):
                print('✅ Payment proof detected')
                return True
            else:
                print('⚠️  No payment proof found')
                return True
        else:
            print('❌ Failed to get payment status')
            return False


def test_admin_get_payment_proof(order_id, admin_token):
    """Test admin getting payment proof."""
    print('\n3️⃣  TEST: Admin Get Payment Proof')
    print('-' * 80)
    
    with app.test_client() as client:
        response = client.get(
            f'/api/admin/payment-proof/{order_id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        print(f'Status Code: {response.status_code}')
        result = response.get_json()
        print(f'Response: {json.dumps(result, indent=2)}')
        
        if response.status_code == 200:
            print('✅ Admin retrieved payment proof successfully')
            if result.get('payment_proof'):
                print(f'✅ Payment proof URL: {result.get("payment_proof")}')
                return True
            else:
                print('⚠️  No payment proof URL')
                return True
        else:
            print('❌ Failed to get payment proof')
            return False


def test_admin_verify_payment(order_id, admin_token):
    """Test admin verifying payment."""
    print('\n4️⃣  TEST: Admin Verify Payment')
    print('-' * 80)
    
    with app.test_client() as client:
        response = client.post(
            f'/api/admin/orders/{order_id}/payment-action',
            json={'action': 'verify'},
            headers={'Authorization': f'Bearer {admin_token}'},
            content_type='application/json'
        )
        
        print(f'Status Code: {response.status_code}')
        result = response.get_json()
        print(f'Response: {json.dumps(result, indent=2)}')
        
        if response.status_code == 200:
            print('✅ Payment verified successfully')
            if result.get('payment_status') == 'VERIFIED':
                print('✅ Payment status set to VERIFIED')
            if result.get('status') == 'PLACED':
                print('✅ Order status set to PLACED')
            return result.get('payment_status') == 'VERIFIED' and result.get('status') == 'PLACED'
        else:
            print('❌ Failed to verify payment')
            return False


def test_admin_reject_payment(order_id, admin_token):
    """Test admin rejecting payment."""
    print('\n5️⃣  TEST: Admin Reject Payment')
    print('-' * 80)
    
    with app.test_client() as client:
        response = client.post(
            f'/api/admin/orders/{order_id}/payment-action',
            json={'action': 'reject', 'reason': 'Invalid payment proof'},
            headers={'Authorization': f'Bearer {admin_token}'},
            content_type='application/json'
        )
        
        print(f'Status Code: {response.status_code}')
        result = response.get_json()
        print(f'Response: {json.dumps(result, indent=2)}')
        
        if response.status_code == 200:
            print('✅ Payment rejected successfully')
            if result.get('payment_status') == 'FAILED':
                print('✅ Payment status set to FAILED')
                return True
            else:
                print(f'❌ Payment status should be FAILED, got: {result.get("payment_status")}')
                return False
        else:
            print('❌ Failed to reject payment')
            return False


def get_admin_token():
    """Get admin JWT token."""
    with app.test_client() as client:
        response = client.post(
            '/api/admin/login',
            json={'password': app.config['ADMIN_PASSWORD']},
            content_type='application/json'
        )
        
        if response.status_code == 200:
            return response.get_json()['token']
    return None


def cleanup_test_order(order_id):
    """Delete test order."""
    with app.app_context():
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()


def main():
    print('=' * 80)
    print('PAYMENT SYSTEM ROUTES TEST')
    print('=' * 80)
    
    # Get admin token
    print('\n🔐 Getting admin token...')
    admin_token = get_admin_token()
    if not admin_token:
        print('❌ Failed to get admin token')
        return False
    print('✅ Admin token obtained')
    
    # Create test order
    print('\n📦 Creating test order...')
    order_id = create_test_order()
    if not order_id:
        print('❌ Failed to create test order')
        return False
    print(f'✅ Test order created: ID={order_id}')
    
    try:
        # Run tests
        results = []
        
        # Test 1: User upload payment proof
        results.append(test_user_upload_payment_proof(order_id))
        
        # Test 2: Get payment status
        results.append(test_get_payment_status(order_id))
        
        # Test 3: Admin get payment proof
        results.append(test_admin_get_payment_proof(order_id, admin_token))
        
        # Test 4: Admin verify payment
        results.append(test_admin_verify_payment(order_id, admin_token))
        
        # Create another order for rejection test
        print('\n📦 Creating second test order for rejection test...')
        order_id_2 = create_test_order()
        if order_id_2:
            print(f'✅ Second test order created: ID={order_id_2}')
            test_user_upload_payment_proof(order_id_2)
            results.append(test_admin_reject_payment(order_id_2, admin_token))
            cleanup_test_order(order_id_2)
        
        # Summary
        print('\n' + '=' * 80)
        print('TEST SUMMARY')
        print('=' * 80)
        
        passed = sum(results)
        total = len(results)
        
        print(f'Tests Passed: {passed}/{total}')
        
        if passed == total:
            print('\n✅ ALL TESTS PASSED')
            print('✅ Payment system is working correctly')
            return True
        else:
            print(f'\n⚠️  {total - passed} test(s) failed')
            return False
    
    finally:
        # Cleanup
        print('\n🧹 Cleaning up test data...')
        cleanup_test_order(order_id)
        print('✅ Cleanup complete')


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
