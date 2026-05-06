# from flask import Blueprint, jsonify, request
# from whatsapp_service import send_whatsapp_message
# 
# test_whatsapp_bp = Blueprint('test_whatsapp', __name__)
# 
# @test_whatsapp_bp.route('/whatsapp', methods=['POST'])
# def test_whatsapp():
#     """
#     Test endpoint to send a WhatsApp message using Meta Cloud API.
#     Request body: { "phone": "919876543210", "message": "Optional message" }
#     """
#     data = request.json or {}
#     phone = data.get('phone')
#     message = data.get('message', 'Hello! This is a test message from M&M Fashion via Meta WhatsApp Cloud API.')
# 
#     if not phone:
#         return jsonify({"error": "Phone number is required"}), 400
# 
#     result = send_whatsapp_message(phone, message)
#     
#     if result.get("success"):
#         return jsonify({
#             "status": "success",
#             "message": f"Test message sent to {phone}",
#             "response": result.get("data")
#         }), 200
#     else:
#         return jsonify({
#             "status": "error",
#             "message": "Failed to send WhatsApp message",
#             "detail": result.get("detail")
#         }), 500
# 
# @test_whatsapp_bp.route('/test-whatsapp', methods=['GET', 'POST'])
# def test_whatsapp_hardcoded():
#     """
#     Simpler test endpoint that sends a message to a hardcoded number.
#     Usage: GET /api/test/test-whatsapp
#     """
#     # Replace with your actual testing number
#     hardcoded_number = "919876543210" 
#     message = "🎉 Meta Cloud API Test: Your WhatsApp integration is working!"
#     
#     result = send_whatsapp_message(hardcoded_number, message)
#     
#     return jsonify({
#         "info": "Attempted to send to hardcoded number",
#         "number": hardcoded_number,
#         "result": result
#     })
