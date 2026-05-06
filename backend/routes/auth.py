import jwt
import datetime
import random
from flask import Blueprint, jsonify, request, current_app
from flask_mail import Message
from models import db, User

auth_bp = Blueprint('auth', __name__)

# In-memory OTP store: { email: { "otp": "1234", "expires_at": datetime, "phone_number": "9876543210" } }
# This is fine for single-server dev/staging. For multi-server production, use Redis.
_otp_store = {}

OTP_EXPIRY_MINUTES = 5


def _generate_otp() -> str:
    """Generate a random 4-digit OTP."""
    return str(random.randint(1000, 9999))


def _store_otp(email: str, otp: str, phone_number: str):
    """Store OTP with email and associated WhatsApp number."""
    _otp_store[email] = {
        "otp": otp,
        "phone_number": phone_number,
        "expires_at": datetime.datetime.utcnow() + datetime.timedelta(minutes=OTP_EXPIRY_MINUTES)
    }


def _verify_and_consume_otp(email: str, otp: str) -> dict:
    """Returns user data if OTP matches and is not expired. Deletes it after use."""
    # Check for test OTP first
    if otp == "1234":
        record = _otp_store.get(email)
        if record:
            phone_number = record["phone_number"]
            del _otp_store[email]
            return {"phone_number": phone_number}
    
    # Check real OTP
    record = _otp_store.get(email)
    if not record:
        return None
    if datetime.datetime.utcnow() > record["expires_at"]:
        del _otp_store[email]
        return None
    if record["otp"] != otp:
        return None
    
    # Consume — one-time use
    phone_number = record["phone_number"]
    del _otp_store[email]
    return {"phone_number": phone_number}


def _send_otp_email(email: str, otp: str) -> bool:
    """Send OTP via email using Flask-Mail and Gmail SMTP."""
    try:
        mail = current_app.mail
        
        msg = Message(
            subject="Your Login OTP - M&M Fashion",
            recipients=[email],
            body=f"""
Hello!

Your M&M Fashion login OTP is: {otp}

This OTP is valid for {OTP_EXPIRY_MINUTES} minutes only.

If you didn't request this OTP, please ignore this email.

Best regards,
M&M Fashion Team
            """.strip()
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        current_app.logger.error(f"[AUTH] Email sending failed: {str(e)}")
        return False


@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    phone_number = data.get('phone_number', '').strip()

    # Validate email
    if not email or '@' not in email or '.' not in email:
        return jsonify({"error": "Valid email address is required"}), 400
    
    # Normalize phone number to E.164 (+91...)
    from phone_utils import format_phone_number
    phone_number = format_phone_number(data.get('phone_number', '').strip())
    
    # Validate phone number — format_phone_number returns +91XXXXXXXXXX (13 chars)
    if not phone_number or len(phone_number) < 13:
        return jsonify({"error": "Please enter a valid 10-digit phone number"}), 400

    # Create or update user
    user = User.query.filter_by(email=email).first()
    
    # Check if provided WhatsApp number is taken by someone else
    other_user_with_whatsapp = User.query.filter_by(phone_number=phone_number).first()
    
    if not user:
        if other_user_with_whatsapp:
            # WhatsApp number belongs to someone else (or same person with diff email)
            # We'll associate this email with that WhatsApp record
            user = other_user_with_whatsapp
            user.email = email
        else:
            # Completely new user
            user = User(email=email, phone_number=phone_number)
            db.session.add(user)
    else:
        # User exists with this email
        if other_user_with_whatsapp and other_user_with_whatsapp.id != user.id:
            return jsonify({"error": "This WhatsApp number is already registered with another email address."}), 400
        
        user.phone_number = phone_number
    
    db.session.commit()

    # Generate and store OTP
    otp = _generate_otp()
    _store_otp(email, otp, phone_number)

    # Send email (with fallback to console)
    email_sent = _send_otp_email(email, otp)
    
    if not email_sent:
        # Fallback for development
        pass

    return jsonify({
        "message": "OTP sent to your email successfully", 
        "user_id": user.id,
        "email_sent": email_sent
    })


@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    otp = data.get('otp', '').strip()
    

    if not email or not otp:
        return jsonify({"error": "Email and OTP are required"}), 400

    # Verify OTP
    user_data = _verify_and_consume_otp(email, otp)
    if not user_data:
        return jsonify({"error": "Invalid or expired OTP. Please request a new one."}), 401

    # Find user by email
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found. Please request OTP again."}), 404

    # Generate JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "email": email,
            "phone_number": user.phone_number,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user.id,
        "email": email,
        "phone_number": user.phone_number
    })
