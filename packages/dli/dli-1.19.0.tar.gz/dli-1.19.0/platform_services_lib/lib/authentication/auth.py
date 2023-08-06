import logging
import os
import re
from enum import Enum

import jwt
from urllib.parse import urljoin
from typing import Optional

import requests
from requests import Session

from ..context.environments import _Environment
from ..context.urls import identity_urls
from ..providers.oidc_provider import JWTEncoded
from ..services.view_exceptions import Unauthorized, TooManyRequests, InternalServerError, BadRequest, Forbidden
from ..context.dev_mode_testing import _get_token

logger = logging.getLogger(__name__)

uuid_regex = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")


class ClientCredentialsAuthenticationMethod(str, Enum):
    pat = 'pat'
    application = 'application'

    def __str__(self):
        return self.value


def _default_external_session() -> Session:
    """
    This creates a default session if one is not provided as a parameter in _sam_app_flow. This will not have any of
    the advantages of connection pools with retry. This is only necessary for backwards compatibility with older SDK
    code that is not expecting to pass `external_session` to _sam_app_flow, otherwise ETL (which uses the SDK) fails.
    """
    return requests.Session()


def _sam_app_flow(environment: _Environment, user_id: str, user_secret: str, external_session: Session = None, origin=None) -> JWTEncoded:
    """Exchange the Application user's credentials provided by the user for a Catalogue token in the form of a JWT"""

    logger.info("Exchanging application user credentials")

    if external_session is None:
        external_session = _default_external_session()

    return __token_exchange(
        environment=environment,
        user_id=user_id,
        user_secret=user_secret,
        authentication_method=ClientCredentialsAuthenticationMethod.application,
        external_session=external_session,
    )


def _sam_pat_flow(environment: _Environment, user_id: str, user_secret: str, external_session: Session) -> JWTEncoded:
    """Exchange the PAT user's credentials provided by the user for a Catalogue token in the form of a JWT"""

    logger.info("Exchanging PAT user credentials")

    return __token_exchange(
        environment=environment,
        user_id=user_id,
        user_secret=user_secret,
        authentication_method=ClientCredentialsAuthenticationMethod.pat,
        external_session=external_session,
    )


def __token_exchange(
    environment: _Environment,
    user_id: str,
    user_secret: str,
    authentication_method: ClientCredentialsAuthenticationMethod,
    external_session: Session,
) -> JWTEncoded:
    """Exchange the credentials provided by the user for a Catalogue token in the form of a JWT"""

    logger.info("Exchanging credentials for a Catalogue token", extra={'authentication_method': authentication_method})

    if user_id is None:
        logger.warning("User ID is not set")

    if user_secret is None:
        logger.warning("User Secret is not set")

    if environment.catalogue is None:
        logger.warning("Catalogue Endpoint is not set")

    token_exchange_url = urljoin(environment.catalogue, identity_urls.identity_token_exchange)  # type: ignore

    dl_payload = {
        'username': user_id,
        'password': user_secret,
        'auth_method': authentication_method.value,  # Must send the string value not the enum.
    }

    if os.environ.get('DEV_MODE'):
        # Dev test mode, returns a test jwt that will authenticate against test containers.
        # This represents the token exchange. This allows for writing integration tests with App and PAT users.
        # TODO We would like to change this block to be an interface on auth.py to remove this from production code
        return _get_token(os.environ.get('JWT_SECRET_KEY', 'secret'))

    else:
        # Set a timeout so that an individual request cannot be running (or idle) forever. We expect Nginx to perform
        # a cutoff at around 60 seconds of being idle, so the number must be under 60 seconds.
        catalogue_timeout = int(os.environ.get('DLC_CLIENT_REQUEST_TIMEOUT', 30))

        resp = external_session.post(token_exchange_url, json=dl_payload, timeout=catalogue_timeout)

        status_code = resp.status_code

        # We do not want to return too many details to the user in the message for security.
        failure_message = f'{resp.status_code} Could not exchange user credentials for JWT access token via the ' \
                          f'Catalogue with auth_method=:{authentication_method.value}'
        failure_extra = {
            'response_status_code': resp.status_code,
            'response_content': resp.text,
            'authentication_method': authentication_method.value,
        }

        if status_code == 200:
            response_jwt: JWTEncoded = resp.json()['access_token']
            return response_jwt

        elif status_code == 400:
            logger.warning(failure_message, extra=failure_extra)
            raise BadRequest(failure_message)

        elif status_code == 401:
            logger.warning(failure_message, extra=failure_extra)
            raise Unauthorized(failure_message)

        elif status_code == 403:
            logger.warning(failure_message, extra=failure_extra)
            raise Forbidden(failure_message)

        elif status_code == 429:
            logger.warning(f'429 Rate limited by the Catalogue on the PAT exchange', extra=failure_extra)
            failure_message = f"Too many requests per minute. Downstream services are now rate limiting your requests. " \
                      f"Message from downstream service: {resp.text}"
            raise TooManyRequests(failure_message)

        else:
            logger.exception(failure_message, extra=failure_extra)
            raise InternalServerError(failure_message)


def decode_token(key):

    __pyjwt_algorithms = [
        # `HS256` is the value returned by the JWT from prod, but pyjwt seems
        # to complain about the signature.
        'HS256',
        'HS512', 'ES256', 'ES384', 'ES512', 'RS256', 'RS384',
        'RS512', 'PS256', 'PS384', 'PS512',
    ]

    return jwt.decode(
        jwt=key,
        algorithms=__pyjwt_algorithms,
        options={
            "verify_signature": False,
            "verify_aud": False,
            "verify_exp": False
        }
    )


def _pre_request_get_token(environment: _Environment, user_id: str, user_secret: str, hint: Optional[str], external_session: Session) -> JWTEncoded:

    _PAT = "PAT"
    _JWT = "JWT"
    _APP = "APP"

    if user_id is None or user_secret is None:
        logger.debug('401 _pre_request_get_token no user_id or user_secret')
        raise Unauthorized()

    if not hint or hint == _PAT:
        # we think it's a PAT or want to check it matches a UUID (which indicates it is)
        # is this a uuid as only PATs are UUIDs? - if it is it can be parse to UUID type
        if uuid_regex.fullmatch(user_id):
            return _sam_pat_flow(environment, user_id, user_secret, external_session=external_session)
        else:
            message = f"doesn't look like a PAT {user_id}"
            logging.debug(message)
            if hint == _PAT:
                raise ValueError(message)

    if not hint or hint == _JWT:
        # we think its already a JWT or want to check its valid
        try:
            # is this a JWT? - if it is it can be decoded
            decode_token(user_id)
            return JWTEncoded(user_id)  # the JWT
        except jwt.DecodeError as e:
            logging.debug(f"{e} - doesn't look like a JWT {user_id}", exc_info=e)
            if hint == _JWT:
                raise e

    if not hint or hint == _APP:
        # this seems to be an APP user, since its not a UUID or JWT
        try:
            return JWTEncoded(_sam_app_flow(environment, user_id, user_secret, external_session=external_session))
        except Exception as e:
            logging.debug(f"{e} - doesn't look like an APP {user_id}", exc_info=e)
            if hint == _APP:
                raise e

    logger.debug('401 _pre_request_get_token not a JWT, PAT or app cred')
    raise Unauthorized()
