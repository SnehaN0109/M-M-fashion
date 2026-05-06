"""
Check Twilio sandbox configuration and get join instructions.
Run: python check_sandbox.py
"""
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

import os
from twilio.rest import Client

sid   = os.getenv("TWILIO_ACCOUNT_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(sid, token)

print("=" * 55)
print("Twilio Sandbox Configuration")
print("=" * 55)

# Error code meanings
print("\nError codes found in your messages:")
print("  63015 = Recipient has NOT opted in (not in sandbox whitelist)")
print("  63016 = Recipient is NOT in sandbox whitelist")
print("\nBOTH mean the same thing: the phone number needs to")
print("send a WhatsApp message to join your sandbox first.")

# Get sandbox info
try:
    sandbox = client.messaging.v1.services.list(limit=5)
    for s in sandbox:
        print(f"\nService: {s.friendly_name} SID={s.sid}")
except Exception as e:
    print(f"\nCould not fetch services: {e}")

# Try to get sandbox keyword
try:
    from twilio.rest.messaging.v1.service import ServiceInstance
    sandboxes = client.messaging.v1.services.list()
    for s in sandboxes:
        print(f"Sandbox: {s.friendly_name}")
except:
    pass

print("\n" + "=" * 55)
print("HOW TO FIX:")
print("=" * 55)
print("\nOption 1 — Sandbox (Free, for testing):")
print("  Each recipient must WhatsApp this number: +14155238886")
print("  And send the message: join <your-sandbox-keyword>")
print("  Find your keyword at: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")
print("\nOption 2 — Production (Paid, no opt-in needed):")
print("  Apply for a WhatsApp Business API number at:")
print("  https://console.twilio.com/us1/develop/sms/senders/whatsapp-senders")
print("  This removes the sandbox restriction entirely.")
print("\nOption 3 — Use a different service (Free alternative):")
print("  Use wa.me link to open WhatsApp with pre-filled message")
print("  (user clicks send themselves)")
