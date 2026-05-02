#!/usr/bin/env python3
"""
Quick test to verify Gmail SMTP is working.
Run this to test email sending before starting the full app.
"""
from app import create_app
from flask_mail import Message

def test_email_sending():
    """Test if Gmail SMTP credentials work."""
    print("🧪 Testing Gmail SMTP connection...")
    
    try:
        app = create_app()
        
        with app.app_context():
            mail = app.mail
            
            # Create test email
            msg = Message(
                subject="🧪 M&M Fashion Email Test",
                recipients=["vaibhavigore7@gmail.com"],  # Send to yourself
                body="""
Hello!

This is a test email from M&M Fashion backend.

If you receive this email, your Gmail SMTP setup is working perfectly! 🎉

Test OTP: 1234

Best regards,
M&M Fashion System
                """.strip()
            )
            
            print("📧 Sending test email to vaibhavigore7@gmail.com...")
            mail.send(msg)
            print("✅ Email sent successfully!")
            print("📱 Check your Gmail inbox for the test email")
            
            return True
            
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        
        # Common error diagnostics
        error_str = str(e).lower()
        if "authentication failed" in error_str:
            print("💡 Check your Gmail App Password - it might be incorrect")
        elif "smtp" in error_str:
            print("💡 Check your internet connection and Gmail SMTP settings")
        elif "535" in error_str:
            print("💡 Gmail App Password is wrong or 2FA not enabled")
        
        return False

if __name__ == "__main__":
    success = test_email_sending()
    if success:
        print("\n🎉 Gmail SMTP is ready! You can now start the full application.")
    else:
        print("\n❌ Fix the Gmail setup before proceeding.")