"""
Token creation and signing functions.
"""

import json
from time import time

from django.conf import settings
from jwkest import jwk
from jwkest.jws import JWS


def create_jwt(lms_user_id, expires_in_seconds, additional_token_claims, now=None):
    """
    Produce an encoded JWT (string) indicating some temporary permission for the indicated user.

    What permission that is must be encoded in additional_claims.
    Arguments:
        lms_user_id (int): LMS user ID this token is being generated for
        expires_in_seconds (int): Time to token expiry, specified in seconds.
        additional_token_claims (dict): Additional claims to include in the token.
        now(int): optional now value for testing
    """
    now = now or int(time())

    payload = {
        'lms_user_id': lms_user_id,
        'exp': now + expires_in_seconds,
        'iat': now,
        'iss': settings.TOKEN_SIGNING['JWT_ISSUER'],
        'version': settings.TOKEN_SIGNING['JWT_SUPPORTED_VERSION'],
    }
    payload.update(additional_token_claims)
    return _encode_and_sign(payload)


def _encode_and_sign(payload):
    """
    Encode and sign the provided payload.

    The signing key and algorithm are pulled from settings.
    """
    keys = jwk.KEYS()

    serialized_keypair = json.loads(settings.TOKEN_SIGNING['JWT_PRIVATE_SIGNING_JWK'])
    keys.add(serialized_keypair)
    algorithm = settings.TOKEN_SIGNING['JWT_SIGNING_ALGORITHM']

    data = json.dumps(payload)
    jws = JWS(data, alg=algorithm)
    return jws.sign_compact(keys=keys)
