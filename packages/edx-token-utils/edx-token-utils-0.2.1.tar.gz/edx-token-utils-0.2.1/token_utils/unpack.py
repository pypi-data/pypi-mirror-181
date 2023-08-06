"""
Token unpacking and verifying functions.
"""

from time import time

from django.conf import settings
from jwkest import Expired, Invalid, MissingKey, jwk
from jwkest.jws import JWS


def unpack_jwt(token, lms_user_id, now=None):
    """
    Unpack and verify an encoded JWT.

    Validate the user and expiration.

    Arguments:
        token (string): The token to be unpacked and verified.
        lms_user_id (int): LMS user ID this token should match with.
        now (int): Optional now value for testing.

    Returns a valid, decoded json payload (string).
    """
    now = now or int(time())
    payload = _unpack_and_verify(token)

    if "lms_user_id" not in payload:
        raise MissingKey("LMS user id is missing")
    if "exp" not in payload:
        raise MissingKey("Expiration is missing")
    if payload["lms_user_id"] != lms_user_id:
        raise Invalid("User does not match")
    if payload["exp"] < now:
        raise Expired("Token is expired")

    return payload


def _unpack_and_verify(token):
    """
    Unpack and verify the provided token.

    The signing key and algorithm are pulled from settings.
    """
    keys = jwk.KEYS()
    keys.load_jwks(settings.TOKEN_SIGNING['JWT_PUBLIC_SIGNING_JWK_SET'])
    decoded = JWS().verify_compact(token.encode('utf-8'), keys)
    return decoded
