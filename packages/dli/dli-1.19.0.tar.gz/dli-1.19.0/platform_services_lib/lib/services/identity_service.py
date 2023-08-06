from typing import Optional

from injector import inject
import logging

from ..providers.oidc_provider import JWTEncoded
from ..providers.catalogue_provider import JWTDlcClient
from ..services.abstract_external_service import ExternalService

logger = logging.getLogger(__name__)


class IdentityService(ExternalService):
    """
    Data Lake interface service, for interfacing
    with said interface.

    The JWTIdentityDlcClient should ONLY be responsible
    for authentication and connection pooling. This class
    should be responsible for implementation of high level
    interfacing with the interface component.
    """
    @inject
    def __init__(
        self,
        # Identity and Catalogue services have merged, so we will use the same connection pool for both classes.
        identity_session: JWTDlcClient
    ):
        logger.debug('Init IdentityService')
        self.identity_session = identity_session

    def get_visible_organisations(self):
        logger.debug('CALL CATALOGUE get_visible_organisations')
        return self.identity_session.get(
            '/__api_v2/organisations/visible',
            hooks=self._make_hook('No visible organisations.')
        ).json()

    def me(self, jwt_encoded: Optional[JWTEncoded] = None):
        logger.debug('CALL CATALOGUE /me')
        kwargs = {'hooks': self._make_hook(f'Cannot access identity/me')}
        if jwt_encoded:
            # we must avoid 'current_app' in the adapter when working outside flask context (middleware)
            kwargs['headers'] = {'Authorization': f'Bearer {jwt_encoded}'}

        return self.identity_session.get(
            '/__api_v2/me',
            **kwargs
        ).json()