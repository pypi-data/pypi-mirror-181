import os
import requests
from requests import Session
from requests.adapters import Retry
from ..adapters.session_adapters import BaseAdapter


def create_catalogue_session(mount_prefix: str) -> Session:
    """
    Create the external session once and mount the Catalogue URL. Add retry logic to handle rate limiting.

    :param mount_prefix: The Catalogue URL.
    """

    session = requests.Session()

    # Pools
    # https://stackoverflow.com/questions/34837026/whats-the-meaning-of-pool-connections-in-requests-adapters-httpadapter
    # pool_maxsize = number of connections to keep around per host (this is useful for multi-threaded applications)
    # pool_connections = the number of host-pools to keep around.
    # For example, if you're connecting to 100 different hosts, and pool_connections=10, then only the latest 10
    # hosts' connections will be re-used.

    # The number of urllib3 connection pools to cache. We only connect to the Catalogue so only need one pool.
    pool_connections = int(os.environ.get('DLC_CLIENT_CONNECTION_POOL_NUM_CONNECTION_POOLS', 1))
    # The maximum number of connections to save in the pool.
    pool_maxsize = int(os.environ.get('DLC_CLIENT_CONNECTION_POOL_MAXSIZE', 20))

    # Configure the Locust connection pool that is used to track the duration of the requests.
    # The Catalogue API specifies that when it is under load it will return HTTP status 429 to signal the client
    # that they are being throttled, so the client should backoff and retry later. See the comments for
    # `backoff_factor` below to see how the retries wait for a backoff.
    max_retries = int(os.environ.get('DLC_CLIENT_CONNECTION_POOL_MAX_RETRIES', 2))

    # The backoff happens after the downstream service returns a HTTP status that is in the `status_forcelist`. It
    # applies this formula to calculate the amount of time until the retry:
    #
    # {backoff factor} * (2 ** ({number of total retries} - 1))
    #
    # Backoff = 30 with max_retries = 2 will retry after 15 seconds...
    # then if that also fails it will retry after 30 seconds.
    # https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
    backoff_factor = int(os.environ.get('DLC_CLIENT_CONNECTION_POOL_BACKOFF_FACTOR', 30))

    # If pool_block is set to False, more connections will be created, but they will not be saved once
    # they've been used. Blocking makes sure we do not overload the downstream service.
    pool_block = bool(os.environ.get('DLC_CLIENT_CONNECTION_POOL_BLOCK', True))

    # HTTP status 104 is the Catalogue-API slamming down a connection from being overloaded.
    # HTTP status 408 is RequestTimeout which is when the Catalogue responses are so slow that we reach the timeout.
    # HTTP status 429 is used by the Catalogue-API as code for rate limiting.
    # HTTP status 502 is a problem with the web server or the proxies you are trying to get access through.
    # HTTP status 504 is the gateway or proxy did not get a response in time from the upstream server that it
    # needed in order to complete the request.
    status_forcelist = [104, 408, 429, 502, 504]

    # Set to a ``None`` value to retry on any verb. By default, it will only retry idempotent HTTP verbs, so would
    # not retry the PAT exchange POST.
    allowed_methods = None

    adapter = BaseAdapter(
        pool_connections=pool_connections,
        pool_maxsize=pool_maxsize,
        # https://urllib3.readthedocs.io/en/latest/reference/
        # urllib3.util.html#urllib3.util.retry.Retry
        max_retries=Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=allowed_methods,
        ),
        pool_block=pool_block,
    )

    # Register the adapter to the prefix.
    session.mount(mount_prefix, adapter)

    return session
