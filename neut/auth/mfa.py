import pyotp

from neut.core.settings import settings

def generate_mfa_secret():
    return pyotp.random_base32()

def get_mfa_uri(secret: str, email: str):
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=settings.PROJECT_NAME)

def verify_mfa_code(secret: str, code: str):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)