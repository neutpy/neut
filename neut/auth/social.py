from social_core.backends.google import GoogleOAuth2
from social_core.backends.facebook import FacebookOAuth2
from social_core.exceptions import AuthException
from fastapi import Request
from neut.core.settings import settings
from neut.auth.models import User, SocialAccount
from sqlmodel import Session, select

class NeutGoogleOAuth2(GoogleOAuth2):
    @classmethod
    def get_key_and_secret(cls):
        return settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

class NeutFacebookOAuth2(FacebookOAuth2):
    @classmethod
    def get_key_and_secret(cls):
        return settings.SOCIAL_AUTH_FACEBOOK_KEY, settings.SOCIAL_AUTH_FACEBOOK_SECRET

SOCIAL_AUTH_BACKENDS = {
    'google-oauth2': NeutGoogleOAuth2,
    'facebook': NeutFacebookOAuth2,
}

async def social_auth(request: Request, backend: str, session: Session):
    if backend not in SOCIAL_AUTH_BACKENDS:
        raise ValueError("Invalid social auth backend")

    backend_class = SOCIAL_AUTH_BACKENDS[backend]
    strategy = request.app.state.strategy
    backend = backend_class(strategy, settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL)

    try:
        user_data = await backend.auth_complete(request)
    except AuthException as e:
        return {"error": str(e)}

    if user_data:
        social_id = user_data.get('id')
        email = user_data.get('email')

        social_account = session.exec(select(SocialAccount).where(
            SocialAccount.provider == backend,
            SocialAccount.provider_user_id == social_id
        )).first()

        if social_account:
            user = social_account.user
        else:
            user = session.exec(select(User).where(User.email == email)).first()
            if not user:
                user = User(email=email, is_active=True, email_verified=True)
                session.add(user)
                session.commit()

            social_account = SocialAccount(provider=backend, provider_user_id=social_id, user_id=user.id)
            session.add(social_account)
            session.commit()

        return user
    else:
        return {"error": "Authentication failed"}