"""
WhatsApp integration for M&M Fashion — powered by Twilio.

Credentials required in backend/.env:
  TWILIO_ACCOUNT_SID      — from https://console.twilio.com
  TWILIO_AUTH_TOKEN       — from https://console.twilio.com
  TWILIO_WHATSAPP_FROM    — e.g. whatsapp:+14155238886 (Twilio sandbox number)
"""
import os
from datetime import datetime


# ── Phone normalisation ───────────────────────────────────────────────────────

def _format_phone(raw: str) -> str:
    """
    Normalise any Indian phone number to E.164 digits without '+'.
    '9876543210'       -> '919876543210'
    '+91 98765 43210'  -> '919876543210'
    '919876543210'     -> '919876543210'
    """
    digits = "".join(c for c in raw if c.isdigit())
    if len(digits) == 10:
        return "91" + digits
    if len(digits) == 12 and digits.startswith("91"):
        return digits
    return digits  # fallback — let Twilio surface the error


# ── Message builder ───────────────────────────────────────────────────────────

def build_order_confirmation(order) -> str:
    """Build a human-readable order confirmation from an Order model instance."""
    now = datetime.utcnow()
    date_str = now.strftime("%d %b %Y, %I:%M %p") + " UTC"

    item_lines = []
    for item in order.items:
        variant = item.variant
        name    = variant.product.name if variant and variant.product else "Item"
        qty     = item.quantity
        price   = float(item.price_at_purchase) * qty
        item_lines.append(f"  • {name} x{qty} — Rs.{price:,.0f}")

    items_block = "\n".join(item_lines) if item_lines else "  (no items)"

    return "\n".join([
        "Order Confirmed!",
        "",
        f"Order ID       : #{order.id}",
        f"Tracking No.   : {order.tracking_number or 'Generating...'}",
        f"Status         : {order.status.replace('_', ' ').title()}",
        "",
        "Items Ordered:",
        items_block,
        "",
        f"Total    : Rs.{float(order.total_amount):,.0f}",
        f"Payment  : {order.payment_method}",
        f"Date     : {date_str}",
        "",
        "Thank you for shopping with M&M Fashion!",
        "We'll notify you when your order is shipped.",
    ])


# ── Core send ─────────────────────────────────────────────────────────────────

def send_whatsapp_text(to_number: str, message: str) -> dict:
    """
    Send a WhatsApp message via Twilio.

    Args:
        to_number : raw phone number (will be normalised to E.164)
        message   : plain text body

    Returns:
        dict — { success: bool, sid: str|None, detail: str }
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
    auth_token  = os.getenv("TWILIO_AUTH_TOKEN",  "").strip()
    from_number = os.getenv("TWILIO_WHATSAPP_FROM", "").strip()

    if not account_sid or not auth_token or not from_number:
        print("[WhatsApp] Twilio credentials not configured — skipping send.")
        return {"success": False, "sid": None, "detail": "credentials_not_configured"}

    phone     = _format_phone(to_number)
    to_wa     = f"whatsapp:+{phone}"

    try:
        from twilio.rest import Client
        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            from_=from_number,
            to=to_wa,
            body=message,
        )
        print("[WhatsApp] Sent to {} - SID: {}".format(to_wa, msg.sid))
        return {"success": True, "sid": msg.sid, "detail": "sent"}

    except Exception as e:
        print("[WhatsApp] Error: {}".format(str(e).encode("ascii", "replace").decode("ascii")))
        return {"success": False, "sid": None, "detail": str(e)}


# ── Convenience wrapper ───────────────────────────────────────────────────────

def send_order_confirmation(order) -> dict:
    """
    Send an order confirmation WhatsApp to the customer.
    Resolves phone from order.customer_phone, falling back to linked user.
    Always returns a result dict — never raises.
    """
    # Resolve phone: prefer customer_phone on order, fall back to linked user
    phone = (order.customer_phone or "").strip()
    if not phone and order.user:
        phone = (order.user.whatsapp_number or "").strip()

    if not phone:
        print("[WhatsApp] No phone number for order #{} - skipping.".format(order.id))
        return {"success": False, "sid": None, "detail": "no_phone_on_order"}

    message = build_order_confirmation(order)
    return send_whatsapp_text(phone, message)
