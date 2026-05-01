import jwt
import datetime
import random
from flask import Blueprint, jsonify, request, current_app
from models import db, User

auth_bp = Blueprint('auth', __name__)

# In-memory OTP store: { whatsapp_number: { "otp": "123456", "expires_at": datetime } }
# This is fine for single-server dev/staging. For multi-server production, use Redis.
_otp_store = {}

OTP_EXPIRY_MINUTES = 10


def _generate_otp() -> str:
    """Generate a random 6-digit OTP."""
    return str(random.randint(100000, 999999))


def _store_otp(whatsapp_number: str, otp: str):
    _otp_store[whatsapp_number] = {
        "otp": otp,
        "expires_at": datetime.datetime.utcnow() + datetime.timedelta(minutes=OTP_EXPIRY_MINUTES)
    }


def _verify_and_consume_otp(whatsapp_number: str, otp: str) -> bool:
    """Returns True if OTP matches and is not expired. Deletes it after use."""
    record = _otp_store.get(whatsapp_number)
    if not record:
        return False
    if datetime.datetime.utcnow() > record["expires_at"]:
        del _otp_store[whatsapp_number]
        return False
    if record["otp"] != otp:
        return False
    # Consume — one-time use
    del _otp_store[whatsapp_number]
    return True


@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    print(f"\n🔔 SEND-OTP REQUEST RECEIVED")
    data = request.get_json(silent=True) or {}
    whatsapp_number = data.get('whatsapp_number', '').strip()
    print(f"📱 WhatsApp Number: {whatsapp_number}")

    if not whatsapp_number or len(whatsapp_number) != 10:
        print(f"❌ Invalid WhatsApp number: {whatsapp_number}")
        return jsonify({"error": "Valid 10-digit WhatsApp number is required"}), 400

    # Create user if not exists
    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        user = User(whatsapp_number=whatsapp_number)
        db.session.add(user)
        db.session.commit()
        print(f"✅ New user created with ID: {user.id}")
    else:
        print(f"✅ Existing user found with ID: {user.id}")

    otp = _generate_otp()
    _store_otp(whatsapp_number, otp)

    # TODO: Replace this print with real WhatsApp Business API call
    # e.g. send_whatsapp_message(whatsapp_number, f"Your OTP is {otp}")
    print(f"\n{'🔥'*50}")
    print(f"🔐 YOUR OTP FOR {whatsapp_number}: {otp}")
    print(f"⏰ Expires in {OTP_EXPIRY_MINUTES} minutes")
    print(f"{'🔥'*50}\n")

    return jsonify({"message": "OTP sent successfully", "user_id": user.id})


@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    print(f"\n🔍 VERIFY-OTP REQUEST RECEIVED")
    data = request.get_json(silent=True) or {}
    whatsapp_number = data.get('whatsapp_number', '').strip()
    otp = data.get('otp', '').strip()
    
    print(f"📱 WhatsApp Number: {whatsapp_number}")
    print(f"🔐 OTP Provided: {otp}")
    print(f"📋 Current OTP Store: {_otp_store}")

    if not whatsapp_number or not otp:
        print(f"❌ Missing data - WhatsApp: {bool(whatsapp_number)}, OTP: {bool(otp)}")
        return jsonify({"error": "whatsapp_number and otp are required"}), 400

    if not _verify_and_consume_otp(whatsapp_number, otp):
        print(f"❌ OTP verification failed for {whatsapp_number}")
        return jsonify({"error": "Invalid or expired OTP. Please request a new one."}), 401

    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        print(f"❌ User not found for {whatsapp_number}")
        return jsonify({"error": "User not found. Please request OTP again."}), 404

    # Generate JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "whatsapp_number": whatsapp_number,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    print(f"✅ Login successful for {whatsapp_number}")
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user.id,
        "whatsapp_number": whatsapp_number
    })
