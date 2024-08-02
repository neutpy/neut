from fastapi import BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from neut.core.router import NeutRouter
from neut.db.base import get_session
from neut.auth import schemas, services, models, dependencies, social, mfa, email
from neut.core.settings import settings
from datetime import datetime, timedelta

router = NeutRouter(prefix="/auth")

@router.post("/register", response_model=schemas.UserOut)
async def register_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(models.User.select().where(models.User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = services.create_user(user, session)
    verification_token = services.create_email_verification_token(new_user, session)
    await email.send_verification_email(new_user.email, verification_token)
    return new_user

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = services.authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not user.email_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified")
    if user.mfa_enabled:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="MFA required", headers={"Location": "/auth/mfa"})
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/mfa-setup", response_model=schemas.UserOut)
async def setup_mfa(mfa_setup: schemas.MFASetup, current_user: models.User = Depends(dependencies.get_current_active_user), session: Session = Depends(get_session)):
    if current_user.mfa_enabled:
        raise HTTPException(status_code=400, detail="MFA already enabled")
    if not mfa.verify_mfa_code(current_user.mfa_secret, mfa_setup.mfa_code):
        raise HTTPException(status_code=400, detail="Invalid MFA code")
    current_user.mfa_enabled = True
    session.commit()
    return current_user

@router.post("/mfa-login", response_model=schemas.Token)
async def mfa_login(mfa_login: schemas.MFALogin, session: Session = Depends(get_session)):
    user = services.authenticate_user(mfa_login.email, mfa_login.password, session)
    if not user or not user.mfa_enabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not mfa.verify_mfa_code(user.mfa_secret, mfa_login.mfa_code):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid MFA code")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/password-reset-request")
async def request_password_reset(
    reset_request: schemas.PasswordResetRequest, 
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    user = session.exec(models.User.select().where(models.User.email == reset_request.email)).first()
    if user:
        token = services.create_password_reset_token(user, session)
        background_tasks.add_task(email.send_password_reset_email, user.email, token)
    return {"message": "If an account with this email exists, a password reset link has been sent."}

@router.post("/password-reset-confirm")
async def confirm_password_reset(
    reset_confirm: schemas.PasswordResetConfirm,
    session: Session = Depends(get_session)
):
    reset = session.exec(models.PasswordReset.select().where(models.PasswordReset.token == reset_confirm.token)).first()
    if not reset or reset.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = session.exec(models.User.select().where(models.User.id == reset.user_id)).first()
    user.hashed_password = services.get_password_hash(reset_confirm.new_password)
    session.delete(reset)
    session.commit()
    return {"message": "Password has been reset successfully"}

@router.get("/verify-email/{token}")
async def verify_email(token: str, session: Session = Depends(get_session)):
    verification = session.exec(models.EmailVerification.select().where(models.EmailVerification.token == token)).first()
    if not verification or verification.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = session.exec(models.User.select().where(models.User.id == verification.user_id)).first()
    user.email_verified = True
    session.delete(verification)
    session.commit()
    return {"message": "Email verified successfully"}

@router.post("/resend-verification-email")
async def resend_verification_email(
    email_request: schemas.EmailStr,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    user = session.exec(models.User.select().where(models.User.email == email_request)).first()
    if user and not user.email_verified:
        token = services.create_email_verification_token(user, session)
        background_tasks.add_task(email.send_verification_email, user.email, token)
    return {"message": "If an unverified account with this email exists, a verification email has been sent."}

@router.get("/social/login/{backend}")
async def login(request: Request, backend: str, session: Session = Depends(get_session)):
    try:
        user = await social.social_auth(request, backend, session)
        if isinstance(user, dict) and "error" in user:
            raise HTTPException(status_code=400, detail=user["error"])
        access_token = services.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/social/complete/{backend}")
async def complete_login(request: Request, backend: str, session: Session = Depends(get_session)):
    try:
        user = await social.social_auth(request, backend, session)
        if isinstance(user, dict) and "error" in user:
            raise HTTPException(status_code=400, detail=user["error"])
        access_token = services.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/social/success")
async def social_auth_success():
    return {"message": "Social authentication successful"}

@router.get("/social/error")
async def social_auth_error():
    return {"message": "Social authentication failed"}

