import jwt
import datetime
import random
from flask import Blueprint, jsonify, request, current_app
from flask_mail import Message
from models import db, User

auth_bp = Blueprint('auth', __name__)

# In-memory OTP store: { email: { "otp": "1234", "expires_at": datetime, "whatsapp_number": "9876543210" } }
# This is fine for single-server dev/staging. For multi-server production, use Redis.
_otp_store = {}

OTP_EXPIRY_MINUTES = 5


def _generate_otp() -> str:
    """Generate a random 4-digit OTP."""
    return str(random.randint(1000, 9999))


def _store_otp(email: str, otp: str, whatsapp_number: str):
    """Store OTP with email and associated WhatsApp number."""
    _otp_store[email] = {
        "otp": otp,
        "whatsapp_number": whatsapp_number,
        "expires_at": datetime.datetime.utcnow() + datetime.timedelta(minutes=OTP_EXPIRY_MINUTES)
    }


def _verify_and_consume_otp(email: str, otp: str) -> dict:
    """Returns user data if OTP matches and is not expired. Deletes it after use."""
    # Check for test OTP first
    if otp == "1234":
        record = _otp_store.get(email)
        if record:
            whatsapp_number = record["whatsapp_number"]
            del _otp_store[email]
            return {"whatsapp_number": whatsapp_number}
    
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
    whatsapp_number = record["whatsapp_number"]
    del _otp_store[email]
    return {"whatsapp_number": whatsapp_number}


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
        print(f"DONE: Email sent successfully to {email}")
        return True
        
    except Exception as e:
        print(f"ERROR: Email sending failed: {str(e)}")
        return False


@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    print(f"\n[AUTH] EMAIL OTP REQUEST RECEIVED")
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    whatsapp_number = data.get('whatsapp_number', '').strip()
    
    print(f"Email: {email}")
    print(f"WhatsApp: {whatsapp_number}")

    # Validate email
    if not email or '@' not in email or '.' not in email:
        print(f"ERROR: Invalid email: {email}")
        return jsonify({"error": "Valid email address is required"}), 400
    
    # Validate WhatsApp number
    if not whatsapp_number or len(whatsapp_number) != 10:
        print(f"ERROR: Invalid WhatsApp number: {whatsapp_number}")
        return jsonify({"error": "Valid 10-digit WhatsApp number is required"}), 400

    # Create or update user
    user = User.query.filter_by(email=email).first()
    
    # Check if provided WhatsApp number is taken by someone else
    other_user_with_whatsapp = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    
    if not user:
        if other_user_with_whatsapp:
            # WhatsApp number belongs to someone else (or same person with diff email)
            # We'll associate this email with that WhatsApp record
            user = other_user_with_whatsapp
            user.email = email
            print(f"DONE: Associated email {email} with existing WhatsApp record (ID: {user.id})")
        else:
            # Completely new user
            user = User(email=email, whatsapp_number=whatsapp_number)
            db.session.add(user)
            print(f"DONE: Creating new user")
    else:
        # User exists with this email
        if other_user_with_whatsapp and other_user_with_whatsapp.id != user.id:
            return jsonify({"error": "This WhatsApp number is already registered with another email address."}), 400
        
        user.whatsapp_number = whatsapp_number
        print(f"DONE: Updated WhatsApp for existing user (ID: {user.id})")
    
    db.session.commit()

    # Generate and store OTP
    otp = _generate_otp()
    _store_otp(email, otp, whatsapp_number)

    # Send email (with fallback to console)
    email_sent = _send_otp_email(email, otp)
    
    if not email_sent:
        # Fallback: print to console for development
        print(f"\n" + ("="*50))
        print(f"EMAIL OTP FALLBACK (Check Console)")
        print(f"To: {email}")
        print(f"OTP: {otp}")
        print(f"Expires in {OTP_EXPIRY_MINUTES} minutes")
        print(f"Test OTP: 1234 (always works)")
        print(f"="*50 + "\n")

    return jsonify({
        "message": "OTP sent to your email successfully", 
        "user_id": user.id,
        "email_sent": email_sent
    })


@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    print(f"\n[AUTH] EMAIL OTP VERIFICATION")
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    otp = data.get('otp', '').strip()
    
    print(f"Email: {email}")
    print(f"OTP: {otp}")
    print(f"Current OTP Store: {list(_otp_store.keys())}")

    if not email or not otp:
        print(f"ERROR: Missing data - Email: {bool(email)}, OTP: {bool(otp)}")
        return jsonify({"error": "Email and OTP are required"}), 400

    # Verify OTP
    user_data = _verify_and_consume_otp(email, otp)
    if not user_data:
        print(f"ERROR: OTP verification failed for {email}")
        return jsonify({"error": "Invalid or expired OTP. Please request a new one."}), 401

    # Find user by email
    user = User.query.filter_by(email=email).first()
    if not user:
        print(f"ERROR: User not found for {email}")
        return jsonify({"error": "User not found. Please request OTP again."}), 404

    # Generate JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "email": email,
            "whatsapp_number": user.whatsapp_number,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    print(f"DONE: Login successful for {email}")
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user.id,
        "email": email,
        "whatsapp_number": user.whatsapp_number
    })
