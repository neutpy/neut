from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    roles: List[str]
    mfa_enabled: bool
    email_verified: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

class SocialLogin(BaseModel):
    provider: str
    access_token: str

class MFASetup(BaseModel):
    mfa_code: str

class MFALogin(BaseModel):
    email: EmailStr
    password: str
    mfa_code: str