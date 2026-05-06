import os
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

def send_whatsapp_message(phone_number, message):
    """
    Sends a WhatsApp message using the Meta WhatsApp Cloud API.
    
    Args:
        phone_number (str): Recipient's phone number (with country code, no +)
        message (str): The text message content
    
    Returns:
        dict: Success status and response details
    """
    # Authorization token from environment variable
    token = os.getenv("WHATSAPP_TOKEN")
    # Phone Number ID from environment variable
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    
    if not token or not phone_number_id:
        logger.error("WhatsApp Cloud API credentials missing (WHATSAPP_TOKEN or WHATSAPP_PHONE_NUMBER_ID)")
        return {"success": False, "detail": "Credentials missing"}

    # Meta Graph API endpoint
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    from phone_utils import format_phone_number
    
    # Normalize to E.164 format (+91...)
    e164_phone = format_phone_number(phone_number)
    
    # Meta API expects the number with country code but usually without leading '+'
    clean_phone = e164_phone.replace("+", "")

    # Construct payload for text-only message
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": clean_phone,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    }

    # Debug logging before sending
    print(f"Sending WhatsApp via META API for order_id: {clean_phone}") # Note: basic send doesn't have order_id, wrappers do.
    
    try:
        logger.info(f"Sending WhatsApp message to {clean_phone}...")
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        # Print status for debug as requested
        print(f"Meta API Response Status: {response.status_code}")

        try:
            response_data = response.json()
        except ValueError:
            response_data = {"raw_response": response.text}

        if response.status_code == 200:
            logger.info(f"WhatsApp message sent successfully. ID: {response_data.get('messages', [{}])[0].get('id')}")
            return {"success": True, "data": response_data}
        else:
            logger.error(f"WhatsApp API Error ({response.status_code}): {response_data}")
            return {
                "success": False, 
                "detail": response_data, 
                "status_code": response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"WhatsApp Request failed: {str(e)}")
        return {"success": False, "detail": str(e)}

# ─── Existing Integration Wrappers ───────────────────────────────────────────
# These maintain compatibility with the existing order flow

def send_order_confirmation(order):
    """Wrapper for CONFIRMED status."""
    message_body = "🎉 Order Confirmed!\nYour M&M Fashion order has been placed successfully."
    return _resolve_and_send(order, message_body)

def send_payment_rejection(order, reason=""):
    """Wrapper for REJECTED status."""
    message_body = "❌ Order Rejected\nYour payment/order could not be verified."
    if reason:
        message_body += f"\nReason: {reason}"
    return _resolve_and_send(order, message_body)

def send_payment_received(order):
    """Wrapper for PAID status."""
    message_body = "💰 Payment Received\nWe are verifying your payment. You will be notified soon."
    return _resolve_and_send(order, message_body)

import threading

def _resolve_and_send(order, message_body):
    """Internal helper to resolve phone number and send message asynchronously."""
    raw_phone = getattr(order, 'effective_whatsapp_number', None)
    order_id = getattr(order, 'id', 'Unknown')

    if not raw_phone:
        logger.error(f"[Order #{order_id}] No phone number found")
        return {"success": False, "detail": "No phone number"}

    # Run in a background thread so it doesn't block the API response
    # def run_async():
    #     # Debug logging as requested
    #     print(f"Sending WhatsApp via META API for order_id: {order_id}")
    #     
    #     logger.info(f"[Order #{order_id}] Triggering background WhatsApp notification...")
    #     result = send_whatsapp_message(raw_phone, message_body)
    #     if result["success"]:
    #         logger.info(f"[Order #{order_id}] WhatsApp notification SUCCESS")
    #     else:
    #         logger.error(f"[Order #{order_id}] WhatsApp notification FAILED: {result.get('detail')}")

    # thread = threading.Thread(target=run_async)
    # thread.start()
    
    # Return immediately to avoid blocking
    return {"success": True, "detail": "WhatsApp disabled"}
