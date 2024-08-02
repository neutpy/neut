import secrets
import string

def secure_token(length: int = 32, symbols: bool = True):
    """
    Generates a secure random key/token
    """
    characters = f"{string.ascii_letters}{string.digits}{'!@#$%^&*()_' if symbols else ''}"
    return ''.join(secrets.choice(characters ) for i in range(length))