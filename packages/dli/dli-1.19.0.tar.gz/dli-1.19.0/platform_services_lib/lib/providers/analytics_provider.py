import logging
import os
import time
import jwt
import requests
from typing import Optional
from injector import singleton as singleton_scope, provider

from requests import Session

from ..providers.oidc_provider import JWTEncoded, JWT
from ..authentication.auth import _sam_app_flow
from ..context.environments import _Environment
from ..context.pool import create_catalogue_session
from ..handlers.analytics_handler import AnalyticsHandler, AnalyticsSender
from ..providers.base_provider import BaseModule


TIME_TO_LIVE_BUFFER = 600

logger = logging.getLogger(__name__)


class AnalyticsDependencyProvider(BaseModule):
    """
    This is currently used by the s3-proxy for analytics. If you want to use it for other services then you will need
    to override the `app_name` in the config dict.
    """

    def __init__(self,  *args, **kwargs):
        super().__init__(**kwargs)
        config = {
            'version': 'latest',
            'app_name': 's3proxy',
            'consumption_env': os.environ.get('CONSUMPTION_API_URL'),
            'strict': False,
        }

        catalogue_url = os.environ.get('CATALOGUE_API_URL')  # 'https://catalogue-qa.udpmarkit.net'
        self._environment = _Environment(catalogue_url)

        # If DLI_ACCESS_KEY_ID and DLI_SECRET_ACCESS_KEY is not valid we cannot retrieve a JWT from SAM so we cannot
        # send analytics!
        self._current_encoded_token: Optional[JWTEncoded] = self._get_encoded_token()

        if self._current_encoded_token is None:
            session_func = AnalyticsDependencyProvider._no_session
        else:
            session_func = self._new_session

        rest_analytics_sender = AnalyticsSender(config, session_func)
        self._analytics_handler = AnalyticsHandler(rest_analytics_sender)

    @staticmethod
    def _decode_token_without_verifying(token: JWTEncoded) -> JWT:
        """
        This function does not verify the token. This is needed when we want to get details from a token that may have
        expired e.g. to get the expiry time!

        :param token: A JWT encoded token.
        """
        options = {
            'verify_signature': False,
            'verify_aud': False,
            'verify_exp': False,
            'verify_nbf': False,
            'verify_iat': False,
            'verify_iss': False
        }
        return jwt.decode(
            token,
            algorithms=["HS256"],
            options=options,
        )

    @staticmethod
    def __token_is_expired(token):
        """
        We deem token expired if life-left-to-live is less than 10 minutes. This is so that we do not start a session
        with a token that is near the expiry time.

        :param token:
        :return:
        """
        exp = token['exp']
        return exp - time.time() - TIME_TO_LIVE_BUFFER < 0

    def _get_sam_app_flow_token(self) -> JWTEncoded:
        return _sam_app_flow(
            self._environment,
            os.environ.get('DLI_ACCESS_KEY_ID'),
            os.environ.get('DLI_SECRET_ACCESS_KEY')
        )

    def _get_encoded_token(self) -> Optional[JWTEncoded]:
        try:
            return self._get_sam_app_flow_token()
        except Exception as e:
            logger.exception('_get_encoded_token failed')
            return None

    def _new_session(self) -> Optional[requests.Session]:
        self.current_decoded_token = self._decode_token_without_verifying(self._current_encoded_token)
        if self.__token_is_expired(self.current_decoded_token):
            self._current_encoded_token = self._get_encoded_token()

        # TODO scott: The session should be using a connection pool with a Retry adapter similar to MR !124. The
        #  current code will be creating a new connection each time and events are more likely to be lost when the
        #  downstream service is under load.
        session: requests.Session = Session()
        session.headers.update({'Authorization': f"Bearer {self._current_encoded_token}"})
        return session

    @staticmethod
    def _no_session() -> Optional[requests.Session]:
        return None

    @singleton_scope
    @provider
    def analytics_handler(self) -> AnalyticsHandler:
        return self._analytics_handler
