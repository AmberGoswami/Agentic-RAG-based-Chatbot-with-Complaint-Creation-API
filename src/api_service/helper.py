import random
import string

def generate_complaint_id() -> str:
    prefix = "CMP"
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{suffix}"