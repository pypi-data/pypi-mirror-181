"""
Tests for token creation and signing
"""
import unittest

from django.conf import settings
from jwkest import BadSignature, jwk
from jwkest.jws import JWS

from token_utils import api
from token_utils.sign import create_jwt

test_user_id = 121
test_timeout = 60
test_now = 1661432902
test_claims = {"foo": "bar", "baz": "quux", "meaning": 42}
expected_full_token = {
    "lms_user_id": test_user_id,
    "iat": test_now,
    "exp": test_now + test_timeout,
    "iss": "token-test-issuer",  # these lines from test_settings.py
    "version": "1.2.0",  # these lines from test_settings.py
}


class TestSign(unittest.TestCase):
    def test_create_jwt(self):
        token = create_jwt(test_user_id, test_timeout, {}, test_now)

        decoded = _verify_jwt(token)
        self.assertEqual(expected_full_token, decoded)

    def test_create_jwt_with_claims(self):
        token = create_jwt(test_user_id, test_timeout, test_claims, test_now)

        expected_token_with_claims = expected_full_token.copy()
        expected_token_with_claims.update(test_claims)

        decoded = _verify_jwt(token)
        self.assertEqual(expected_token_with_claims, decoded)

    def test_malformed_token(self):
        token = create_jwt(test_user_id, test_timeout, test_claims, test_now)
        token = token + "a"

        expected_token_with_claims = expected_full_token.copy()
        expected_token_with_claims.update(test_claims)

        with self.assertRaises(BadSignature):
            _verify_jwt(token)

    def test_sign_api_hooked_up(self):
        api_token = api.sign_token_for(test_user_id, test_timeout, test_claims)
        decoded = _verify_jwt(api_token)
        # we've verified full token flow above and have no now access via the API
        # so just check that an item we know we put in came through properly
        self.assertEqual(42, decoded['meaning'])
        # and an item from config came through properly
        self.assertEqual('token-test-issuer', decoded['iss'])


def _verify_jwt(jwt_token):
    """
    Helper function which verifies the signature and decodes the token
    from string back to claims form
    """
    keys = jwk.KEYS()
    keys.load_jwks(settings.TOKEN_SIGNING['JWT_PUBLIC_SIGNING_JWK_SET'])
    decoded = JWS().verify_compact(jwt_token.encode('utf-8'), keys)
    return decoded
