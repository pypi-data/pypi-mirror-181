from datetime import timedelta, datetime
import freezegun
import time
import jwt
from unittest.mock import patch
from lib.providers.analytics_provider import AnalyticsDependencyProvider, TIME_TO_LIVE_BUFFER


JWT_SECRET_KEY = 'secret'
JWT_AUDIENCE = 'datalake-dev-0000000000'
TOKEN_LIFE = 2 + TIME_TO_LIVE_BUFFER


def get_token(self):
    payload = {
        "sub": "a.user@ihsmarkit.com",
        "aud": JWT_AUDIENCE,
        "azp": JWT_AUDIENCE,
        "exp": int(time.time() + TOKEN_LIFE),
        "datalake": {
            "user_id": "bfb92613-0000-0000-0000-7594bd8c8d16",
            "organisation_id": "9516c0ba-0000-0000-0000-000c6c0a981f"
        },
        "email": "a.user@ihsmarkit.com",
        "name": "a user"
    }
    decoded_token = jwt.encode(
        payload,
        key=JWT_SECRET_KEY,
        algorithm="HS256",
    )
    return decoded_token


class TestAnalyticsSessionRefresh:
    @patch("lib.providers.analytics_provider.AnalyticsDependencyProvider._get_encoded_token", get_token)
    def test_session_is_refreshed_on_expiration(self):

        analytics_provider = AnalyticsDependencyProvider()
        ct = analytics_provider._current_encoded_token
        decoded_token = analytics_provider._decode_token_without_verifying(ct)

        # token is still valid:
        current_time = time.time()
        seconds_to_expire = decoded_token['exp'] - current_time
        assert 0 < seconds_to_expire < TOKEN_LIFE

        # token will be deemed expired after its life time is over
        future_time_when_token_expired = current_time + (2 * TOKEN_LIFE)

        # asserting in current time token is still in valid state - more than 1s left of token lifetime
        assert future_time_when_token_expired - current_time > 0

        t1 = datetime.fromtimestamp(future_time_when_token_expired)
        with freezegun.freeze_time(t1):  # NOTE: this 1h delta makes it == to now
            # Asserting freezegun virtual time is equal to when token is about to expire
            frozen_current_time = time.time()
            seconds_to_expire_for_old_token = decoded_token['exp'] - frozen_current_time
            assert seconds_to_expire_for_old_token < 0

            # Handler gets called
            analytics_provider._new_session()
            # assert the provider refreshes the session when token is expired
            seconds_to_expire_for_refreshed_token = decoded_token['exp'] - frozen_current_time
            assert 0 > seconds_to_expire_for_refreshed_token  # Asserting token has now expired

            new_decoded_token = analytics_provider._decode_token_without_verifying(analytics_provider._current_encoded_token)
            assert new_decoded_token != decoded_token
            seconds_to_expire = new_decoded_token['exp'] - frozen_current_time
            assert 0 < seconds_to_expire < TOKEN_LIFE
