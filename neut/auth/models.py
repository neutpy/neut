from datetime import datetime
from sqlalchemy import JSON, Column
from sqlmodel import Relationship, SQLModel, Field
from typing import Optional, List
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    roles: List[str] = Field(default=[], sa_column=Column(JSON))
    mfa_secret: Optional[str] = None
    mfa_enabled: bool = Field(default=False)
    email_verified: bool = Field(default=False)
    social_accounts: List["SocialAccount"] = Relationship(back_populates="user")

class SocialAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    provider: str
    provider_user_id: str
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="social_accounts")

class PasswordReset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str = Field(unique=True, index=True)
    expires_at: datetime

class EmailVerification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str = Field(unique=True, index=True)
    expires_at: datetime

class Token(SQLModel):
    access_token: str
    token_type: str