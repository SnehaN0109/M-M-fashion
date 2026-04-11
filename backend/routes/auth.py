from flask import Blueprint, jsonify, request
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/whatsapp-login', methods=['POST'])
def whatsapp_login():
    data = request.json
    whatsapp_number = data.get('whatsapp_number')
    
    if not whatsapp_number:
        return jsonify({"error": "WhatsApp number is required"}), 400
        
    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        user = User(whatsapp_number=whatsapp_number)
        db.session.add(user)
        db.session.commit()
        
    # In a real scenario, implement JWT or session based token
    return jsonify({"message": "Login successful", "user_id": user.id})
