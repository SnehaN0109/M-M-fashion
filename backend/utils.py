import random
import string
from datetime import datetime

# ─── Tracking Number Generation ───────────────────────────────────────────────

def generate_tracking_number(order_id: int) -> str:
    """
    Generate a unique tracking number.
    Format: MM<YEAR><6 random digits>
    Example: MM2026483920

    Uniqueness is enforced by the caller (assign_tracking_number).
    """
    year = datetime.utcnow().year
    random_digits = random.randint(100000, 999999)
    return f"MM{year}{random_digits}"


def assign_tracking_number(order, db_session) -> str:
    """
    Assign a unique tracking number to an order if it doesn't already have one.
    Loops until a number not already in the DB is found.
    Idempotent — returns existing tracking number if already set.
    Commits nothing — caller must commit.
    """
    if order.tracking_number:
        return order.tracking_number

    # Import here to avoid circular imports at module level
    from models import Order

    while True:
        candidate = generate_tracking_number(order.id)
        existing = Order.query.filter_by(tracking_number=candidate).first()
        if not existing:
            order.tracking_number = candidate
            return candidate


# ─── Domain → Price Key mapping (single source of truth) ─────────────────────
# This must NEVER be derived from client input.
# The domain value comes from the request, but the price_key is resolved here.

DOMAIN_PRICE_MAP = {
    'garba.shop':   'price_b2c',
    'ttd.in':       'price_b2b_ttd',
    'maharashtra':  'price_b2b_maharashtra',
}

# Domains that are B2B — used to enforce WHOLESALER role check
B2B_DOMAINS = ('ttd.in', 'ttd', 'maharashtra', 'maha')


def resolve_price_key(domain: str) -> str:
    """
    Given a domain string, return the correct price column name.
    Falls back to price_b2c for any unknown domain.
    """
    if not domain:
        return 'price_b2c'

    domain = domain.lower().strip()

    if 'ttd.in' in domain or domain == 'ttd':
        return 'price_b2b_ttd'
    if 'maharashtra' in domain or 'maha' in domain:
        return 'price_b2b_maharashtra'
    if 'garba.shop' in domain:
        return 'price_b2c'

    # localhost dev — check if it matches a known key directly
    return DOMAIN_PRICE_MAP.get(domain, 'price_b2c')


def is_b2b_domain(domain: str) -> bool:
    """Returns True if the domain is a B2B wholesale domain."""
    if not domain:
        return False
    domain = domain.lower().strip()
    return any(b2b in domain for b2b in B2B_DOMAINS)
