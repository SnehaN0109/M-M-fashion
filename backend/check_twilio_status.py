"""
Check Twilio message delivery status.
Run: python check_twilio_status.py
"""
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

import os
from twilio.rest import Client

sid   = os.getenv("TWILIO_ACCOUNT_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")

print(f"SID:   {sid[:10]}..." if sid else "SID: NOT SET")
print(f"Token: {token[:6]}..." if token else "Token: NOT SET")

client = Client(sid, token)

print("\nLast 5 WhatsApp messages sent:")
try:
    messages = client.messages.list(limit=5)
    for m in messages:
        print(f"  to={m.to} status={m.status} error_code={m.error_code} error_msg={m.error_message}")
except Exception as e:
    print(f"  Error fetching messages: {e}")

print("\nAccount info:")
try:
    account = client.api.accounts(sid).fetch()
    print(f"  Account name: {account.friendly_name}")
    print(f"  Status: {account.status}")
except Exception as e:
    print(f"  Error: {e}")
