#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#
import dataclasses
import logging

from injector import provider, singleton as singleton_scope
from requests import Session
from urllib3 import Retry

from ..providers.base_provider import BaseModule
from ..adapters.session_adapters import DlcAdapter


@dataclasses.dataclass
class Config:
    api_root: str
    # Defaults taken from the requests library were 10, 10. Under performance
    # tests with 250 concurrent users and 30 pods, 10 was not enough.
    pool_connections: int = 1
    pool_maxsize: int = 20
    max_retries: int = 2


class JWTDlcClient(Session):

    logger = logging.getLogger(__name__)

    def __init__(self, config):
        super().__init__()
        self.config = config

        # Pools
        # https://stackoverflow.com/questions/34837026/whats-the-meaning-of-pool-connections-in-requests-adapters-httpadapter
        # pool_maxsize = number of connections to keep around per host (this is useful for multi-threaded applications)
        # pool_connections = the number of host-pools to keep around.
        # For example, if you're connecting to 100 different hosts, and pool_connections=10, then only the latest 10
        # hosts' connections will be re-used.

        # Backoff 30 with max_retries 2 will retry after 15 seconds then if that fails retry after 30 seconds.
        # https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
        backoff_factor = 30

        # If pool_block is set to False, more connections will be created but they will not be saved once
        # they've been used.
        pool_block = True

        # HTTP status 104 is the Catalogue-API slamming down a connection from being overloaded.
        # HTTP status 408 is RequestTimeout which is when the Catalogue responses are so slow that we reach the timeout.
        # HTTP status 429 is used by the Catalogue-API as code for rate limiting.
        # HTTP status 502 is a problem with the web server or the proxies you are trying to get access through.
        # HTTP status 504 is the gateway or proxy did not get a response in time from the upstream server that it
        # needed in order to complete the request.
        status_forcelist = [104, 408, 429, 502, 504]

        # Set to a ``None`` value to retry on any verb. By default it will only retry idempotent HTTP verbs, so would
        # not retry the PAT exchange POST.
        allowed_methods = None

        adapter = DlcAdapter(
            pool_connections=self.config.pool_connections,
            pool_maxsize=self.config.pool_maxsize,
            # https://urllib3.readthedocs.io/en/latest/reference/
            # urllib3.util.html#urllib3.util.retry.Retry
            max_retries=Retry(
                total=self.config.max_retries,
                status=self.config.max_retries,
                status_forcelist=status_forcelist,
                allowed_methods=allowed_methods,
                backoff_factor=backoff_factor,
            ),
            pool_block=pool_block,
        )

        self.logger.info(f"JWTDlcClient session mount prefix '{self.config.api_root}'")
        self.mount(self.config.api_root, adapter)

    def request(self, method, url, *args, **kwargs):
        # url = urljoin(self.config.api_root, url) # this isnt going to work for a local case
        url = "".join([self.config.api_root, url])

        self.logger.debug(
            f'JWTDlcClient request using connection pool {url}',
            extra={'url': url}
        )

        return super().request(method, url, *args, **kwargs)


class JWTDependencyProvider(BaseModule):
    config_class = Config

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.session = JWTDlcClient(config=self.config)

    @singleton_scope
    @provider
    def auth_client(self) -> JWTDlcClient:
        return self.session

