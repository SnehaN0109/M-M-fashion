import requests
import os
import logging
import threading
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def send_sms(phone_number, message):
    try:
        # Clean phone number - extract last 10 digits only
        phone = str(phone_number).strip()
        phone = phone.replace('+', '').replace('-', '').replace(' ', '')
        if phone.startswith('91') and len(phone) == 12:
            phone = phone[2:]
        phone = phone[-10:]
        
        if len(phone) != 10:
            print(f"SMS Error: Invalid phone number: {phone_number}")
            return None
        
        key = os.getenv('FAST2SMS_API_KEY')
        if not key:
            print("SMS Error: FAST2SMS_API_KEY not found in environment")
            return None
        
        url = "https://www.fast2sms.com/dev/bulkV2"
        payload = {
            "route": "q",
            "message": message,
            "language": "english",
            "flash": 0,
            "numbers": phone
        }
        headers = {
            "authorization": key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        result = response.json()
        
        if result.get('return') == True:
            print(f"✅ SMS sent successfully to {phone}")
        else:
            print(f"❌ SMS failed: {result}")
        
        return result
        
    except requests.exceptions.Timeout:
        print(f"❌ SMS timeout - Fast2SMS took too long")
        return None
    except Exception as e:
        print(f"❌ SMS Exception: {str(e)}")
        return None


# ─── Integration Wrappers ─────────────────────────────────────────────────────

def send_order_confirmation_sms(order):
    """Wrapper for Order Confirmed."""
    message = f"🎉 Order Confirmed!\nYour M&M Fashion order #{order.id} has been placed successfully."
    return _resolve_and_send_sms(order, message)

def send_payment_rejection_sms(order, reason=""):
    """Wrapper for Order Rejected."""
    message = f"❌ Order Rejected\nYour payment for order #{order.id} could not be verified."
    if reason:
        message += f"\nReason: {reason}"
    return _resolve_and_send_sms(order, message)

def send_payment_received_sms(order):
    """Wrapper for Payment Verified (PAID status)."""
    message = f"💰 Payment Received\nWe are verifying your payment for order #{order.id}. You will be notified soon."
    return _resolve_and_send_sms(order, message)

def _resolve_and_send_sms(order, message):
    """Internal helper to resolve phone number and send SMS asynchronously."""
    # Resolve the best phone number from the model property
    raw_phone = getattr(order, 'effective_notification_number', None)
    order_id = getattr(order, 'id', 'Unknown')

    if not raw_phone:
        logger.error(f"[Order #{order_id}] No phone number found for SMS")
        return {"success": False, "detail": "No phone number"}

    def run_async():
        logger.info(f"Sending SMS via Fast2SMS for order_id: {order_id}")
        result = send_sms(raw_phone, message)
        if result and result.get("return"):
            logger.info(f"[Order #{order_id}] SMS notification SUCCESS")
        else:
            detail = result.get('message') if result else "No response"
            logger.error(f"[Order #{order_id}] SMS notification FAILED: {detail}")

    thread = threading.Thread(target=run_async)
    thread.start()
    
    return {"success": True, "detail": "SMS queued in background"}
