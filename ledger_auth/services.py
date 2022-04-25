from datetime import datetime, timedelta
from functools import lru_cache
from jwt import encode, decode
from django.conf import settings

from ledger_auth.models import RevokedToken


@lru_cache(maxsize=20)
def is_revoked(token):
    try:
        RevokedToken.objects.get(pk=token)
        return True
    except:
        return False


def generate_token(user_id):
    duration = getattr(settings, 'JWT_DURATION', 60)
    issuer = getattr(settings, 'JWT_ISSUER', None)

    iat = int(datetime.utcnow().timestamp())
    exp = int(
        (datetime.utcnow() + timedelta(minutes=duration)).timestamp())

    payload = {"user_id": user_id, "exp": exp, "iat": iat}
    if issuer is not None:
        payload['iss'] = issuer

    token = encode(payload, settings.SECRET_KEY, settings.JWT_ALGORITHM)

    return token


def revoke_token(token, exp):
    RevokedToken.objects.create(
        token=token, exp=datetime.fromtimestamp(exp / 1e3))


def decode_token(token):
    issuer = getattr(settings, 'JWT_ISSUER', None)
    token_dict = decode(
        token, settings.SECRET_KEY, issuer=issuer, algorithms=[settings.JWT_ALGORITHM])
    return token_dict