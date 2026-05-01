"""
WhatsApp Business API integration for sending OTPs.
This is a template - you need to configure with your WhatsApp Business API credentials.
"""
import requests
import os
from typing import Optional

class WhatsAppService:
    def __init__(self):
        # These need to be added to your .env file
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.base_url = "https://graph.facebook.com/v18.0"
        
    def send_otp_message(self, whatsapp_number: str, otp: str) -> bool:
        """
        Send OTP via WhatsApp Business API.
        Returns True if successful, False otherwise.
        """
        if not self.access_token or not self.phone_number_id:
            print("❌ WhatsApp credentials not configured. Using console OTP.")
            return False
            
        # Format phone number (remove +91 if present, add 91)
        formatted_number = whatsapp_number.replace('+', '').replace(' ', '')
        if not formatted_number.startswith('91'):
            formatted_number = '91' + formatted_number
            
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # WhatsApp message payload
        payload = {
            "messaging_product": "whatsapp",
            "to": formatted_number,
            "type": "template",
            "template": {
                "name": "otp_verification",  # You need to create this template
                "language": {
                    "code": "en"
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": otp
                            }
                        ]
                    }
                ]
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ OTP sent to WhatsApp: {whatsapp_number}")
                return True
            else:
                print(f"❌ WhatsApp API Error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ WhatsApp sending failed: {str(e)}")
            return False

# Alternative: Simple SMS service (like Twilio)
class SMSService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_FROM_NUMBER')
        
    def send_otp_sms(self, phone_number: str, otp: str) -> bool:
        """Send OTP via SMS using Twilio."""
        try:
            from twilio.rest import Client
            
            if not all([self.account_sid, self.auth_token, self.from_number]):
                print("❌ Twilio credentials not configured.")
                return False
                
            client = Client(self.account_sid, self.auth_token)
            
            message = client.messages.create(
                body=f"Your M&M Fashion OTP is: {otp}. Valid for 10 minutes.",
                from_=self.from_number,
                to=f"+91{phone_number}"
            )
            
            print(f"✅ SMS sent via Twilio: {message.sid}")
            return True
            
        except Exception as e:
            print(f"❌ SMS sending failed: {str(e)}")
            return False