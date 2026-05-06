import re

def format_phone_number(phone):
    """
    Normalizes phone numbers to E.164 format (+91...).
    Defaults to Indian (+91) if 10 digits are provided.
    """
    if not phone:
        return ""
    
    # Remove all non-numeric characters
    clean = re.sub(r'\D', '', str(phone))
    
    # If 10 digits, assume India
    if len(clean) == 10:
        return f"+91{clean}"
    
    # If starts with 0 and has 11 digits (e.g. 09876543210), treat as India
    if len(clean) == 11 and clean.startswith('0'):
        return f"+91{clean[1:]}"
    
    # If already has country code but no +, add it
    if len(clean) > 10:
        return f"+{clean}"
    
    return f"+{clean}" # Fallback
