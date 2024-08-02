from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlmodel import Session, select
from neut.core.settings import settings
from neut.auth.models import User, SocialAccount, PasswordReset, EmailVerification
from neut.auth.schemas import UserCreate, SocialLogin
import pyotp
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str, session: Session):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(token: str, session: Session):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
    user = session.exec(select(User).where(User.email == email)).first()
    return user

def create_user(user: UserCreate, session: Session):
    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def create_social_account(user: User, social_login: SocialLogin, session: Session):
    social_account = SocialAccount(
        provider=social_login.provider,
        provider_user_id=social_login.access_token,  # This should be the user ID from the provider, not the access token
        user_id=user.id
    )
    session.add(social_account)
    session.commit()
    return social_account

def generate_mfa_secret():
    return pyotp.random_base32()

def verify_mfa_code(secret: str, code: str):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)

def create_password_reset_token(user: User, session: Session):
    token = secrets.token_urlsafe()
    reset = PasswordReset(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    session.add(reset)
    session.commit()
    return token

def create_email_verification_token(user: User, session: Session):
    token = secrets.token_urlsafe()
    verification = EmailVerification(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    session.add(verification)
    session.commit()
    return token