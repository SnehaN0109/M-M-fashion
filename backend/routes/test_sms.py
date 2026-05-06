from flask import Blueprint, jsonify, request
from sms_service import send_sms

test_sms_bp = Blueprint('test_sms', __name__)

@test_sms_bp.route('/sms', methods=['POST'])
def test_sms_flexible():
    """
    Test endpoint to send an SMS using Fast2SMS API.
    Request body: { "phone": "9876543210", "message": "Test message" }
    """
    data = request.json or {}
    phone = data.get('phone')
    message = data.get('message', 'Hello! This is a test SMS from M&M Fashion via Fast2SMS.')

    if not phone:
        return jsonify({"error": "Phone number is required"}), 400

    result = send_sms(phone, message)
    
    if result and result.get("return") is True:
        return jsonify({
            "status": "success",
            "message": f"Test SMS sent to {phone}",
            "response": result
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to send SMS",
            "detail": result
        }), 500

@test_sms_bp.route('/test-sms', methods=['GET', 'POST'])
def test_sms_hardcoded():
    """
    Simpler test endpoint that sends an SMS to a hardcoded number.
    Usage: GET /api/test/test-sms
    """
    # Replace with your actual testing number
    hardcoded_number = "8799878598" 
    message = "🎉 Fast2SMS Test: Your SMS integration for M&M Fashion is working!"
    
    result = send_sms(hardcoded_number, message)
    
    return jsonify({
        "info": "Attempted to send SMS to hardcoded number",
        "number": hardcoded_number,
        "result": result
    })
