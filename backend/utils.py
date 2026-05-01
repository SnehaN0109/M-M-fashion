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
