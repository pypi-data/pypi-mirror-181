#
# Copyright (C) 2019 IHS Markit.
# All Rights Reserved
#
import dataclasses
import os
import logging
import hashlib
import re
from typing import Optional

import jwt
from botocore.exceptions import ClientError
from flask import current_app
from functools import wraps
from pymemcache.client.hash import HashClient
from injector import inject, provider, singleton as singleton_scope

from .oidc_provider import JWTEncoded
from ..providers.base_provider import BaseModule
from ..clients.refreshing_hashclient import RefreshingHashClient


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Config:
    elasticache_config_node_url: str
    # Discovery timeout - probably will never need to be changed.
    time_to_timeout: int = 5
    # Defaults taken from the requests library were 10, 10. Under performance
    default_ttl: int = 3600


class MemcachedDependencyProvider(BaseModule):
    config_class = Config

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @singleton_scope
    @provider
    def memcached_client(self) -> HashClient:
        # NOTA BENE: DO NOT CHANGE THIS RETURN TYPE, even though we are not a HashClient, you will break injectors
        # as everywhere will be looking for the Provider of "HashClient" when we are really extending the type
        # by way of a HAS_A pass-through type: i.e. for our intents and purposes it acts like a HashClient.
        hashclient = RefreshingHashClient(self.config)
        return hashclient


def cleanse(value, key: Optional[str]):
    # For certain values, a key value in the cache may need to respect different rules.
    #
    # One such instance is the case of JWTs. The middleware receives a different JWT back from the Catalogue,
    # even for the same user on every request via the middleware, when using PAT or APP credentials.
    # This allows S3Proxy to receive a brand new token with a maximual amount of time left on the token.

    # What this means though is a call made to a method of the CachedFetcherService will bear
    # different arguments on each call (whereas previously a JWT=JWT), and therefore end up cache missing
    # and necessitating making the real call on the second request by the same user, and moreover, the third etc.

    # Because jwt can be passed as a kwarg or an arg by the application, we don't really have a choice, but to
    # go through the received values of the args and kwargs, check if they are a jwt or not, and if they are
    # convert that value (which composes a part of the cache key) to the common value of the JWT,
    # such that the cached first request is cache-hit by the second until expiry.

    # Dependent on whether the JWT is from a OIDC, PAT, or APP flow,
    # the clean value is pulled from a slightly different place in the JWT.

    def extract_sub_if_present(dict_type: dict):
        if dict_type.get("sub"):
            return dict_type["sub"]
        else:
            return dict_type

    if key and (key == 'jwt' or key == 'jwt_encoded'):
        # It's an arg so we don't have a key, do a cheap match to see if this is a JWT.
        regex_jwt = r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$"
        if type(value) is dict:
            # If it's a jwt that has already been decoded to a dict.
            return extract_sub_if_present(value)
        elif (type(value) is JWTEncoded or type(value) is str) and re.match(regex_jwt, value):
            try:
                options = {
                    "verify_signature": True,
                    "verify_aud": False,
                    "verify_exp": False,
                }
                jwt_decoded = jwt.decode(
                    jwt=value,
                    key=os.environ["JWT_SECRET_KEY"],
                    algorithms='HS256',
                    options=options
                )
                return extract_sub_if_present(jwt_decoded)
            except jwt.DecodeError as e:
                logger.warning('Problem decoding using JWT', exc_info=e)
                return value
        else:
            return value
    else:
        return value


def get_key_val(key, cache_func_name, *args, **kwargs):
    if key:
        # If a key parameter was provided, we do not do any skipping
        # of arguments. The caller has provided a key function so we
        # pass on all of the arguments and let the caller decide what
        # to do. This is important as the wrapper could be around a
        # static function that does not have `self` or `client` as the
        # first parameter, so skipping may cause us to miss an
        # important parameter.
        key_val = f'consumption-{cache_func_name}-' + \
                  key(*args, **kwargs)
    else:
        # Else, no key parameter was provided. This is treated as the
        # case for an annotation around a non-static or stateful
        # method. Such a method will start with `self` or `client`,
        # which is a value that breaks the caching so must be skipped.
        # The [1:] skips the `self` argument.
        a = '-'.join(str(cleanse(key=None, value=a)) for a in args[1:])
        k = '-'.join(f'{k}-{cleanse(key=k, value=v)}' for k, v in kwargs.items())
        # Use the commit ID so that when we do a deployment we start with a fresh cache.
        # This is useful for development.
        commit_id = os.environ.get(
            'CI_COMMIT_SHORT_SHA',
            'unknown'
        )
        key_val = f'consumption-{cache_func_name}-args:{a}:kwargs-{k}-' \
                  f'commit_id:{commit_id}'

    return key_val


def memcached_method(
    cache_getter,
    cache_func_name: Optional[str] = None,
    key=None,
    ttl=None,
    force_cache_refresh: bool = False,
):
    """
    Cache a call.

    :param cache_getter:
    :param key: func for generating the key used on the cache.

        If a key parameter was provided, we do not do any skipping
        of arguments. The caller hasprovided a key function so we
        pass on all of the arguments and let the caller decide what
        to do. This is important as the wrapper could be around a
        static function that does not have `self` or `client` as the
        first parameter, so skipping may cause us to miss an
        important parameter.

        Else, no key parameter was provided. This is treated as the
        case for an annotation around a non-static or stateful
        method. Such a method will start with `self` or `client`,
        which is a value that breaks the caching so must be skipped.
        The [1:] skips the `self` argument.

    :param ttl: Override the `ttl` found in the config file.
    :param cache_func_name: a name to add to the cache key so that:
     1. two functions with similar arguments do not have a name clash.
     2. if a property suce as the common prefixes have changes, then
     including them in the cache key will cause us to not hit the old cache
     key during pagination.
    :param force_cache_refresh: When False, will use standard cache
            behaviour of checking if a value is in cache, then return from
            cache, else  make a real call. When True, will make a real call
            and replace the values in the cache.
    :return: List of S3 files.
    """
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal ttl
            nonlocal cache_func_name
            if args:
                # a class needing to be initialized or a function needing to be called to get the client
                mem_cache: HashClient = cache_getter(args[0])
            else:
                # a hashclient or equivalent with get/set methods
                mem_cache: HashClient = cache_getter()

            if cache_func_name is None:
                # If you are using cachedmethod as a decorator, then we can
                # get the name of the function the decorator is wrapping.
                # Otherwise, you need to explicitly provide a name.
                cache_func_name = func.__name__

            key_val = get_key_val(key, cache_func_name, *args, **kwargs)
            # TODO scott: in python 3.9 they add the parameter `usedforsecurity`. When we upgrade
            #  to Python 3.9 then set the parameter to False for a speed boost as we only use
            #  this for generating cache keys.
            key_hashed = hashlib.sha1(key_val.encode()).hexdigest()
            if len(key_hashed) > 250:
                # Guard against sending a key that is too long for memcached (limit 250
                # characters).
                #   SHA1 produces 40 characters hex encoded.
                #   MD5 produces 32 characters hex encoded.
                #   SHA-256 produces 64 characters hex encoded.
                logger.error(
                    'key_hashed is too long to be used as a key in memcached'
                )

            def _real_call(mem_cache_expiry, reason):
                logger.debug(f'Make real call to {func} - {reason}')
                # Make a real call.
                result_from_real_call = func(*args, **kwargs)

                # Save/replace the result in the cache.
                # Do not use memcached `.add` as it fails if the key already
                # exists on server. Use `set` instead.
                if mem_cache:
                    if not mem_cache_expiry:
                        mem_cache_expiry = int(os.environ.get(
                            'DEFAULT_CACHE_TTL', 3600
                        ))

                    result_code = mem_cache.set(
                        key_hashed,
                        result_from_real_call,
                        # noreply=False moved to refreshing_hashclient.py
                        expire=mem_cache_expiry
                    )

                    if not result_code:
                        logger.warning(
                            'Failed to set cache value!',
                            extra={
                                'key_hashed': key_hashed,
                                'mem_cache_expiry': mem_cache_expiry,
                                'result_code': result_code,
                                'reason': reason,
                                'ttl': mem_cache_expiry,
                            }
                        )

                return result_from_real_call

            force_cache_refresh_override = os.environ.get('CACHE_DISABLED', force_cache_refresh)
            if force_cache_refresh_override:
                return _real_call(ttl, "because the ttl_cache is being forced to refresh")
            else:
                if mem_cache:
                    result_from_cache = mem_cache.get(key_hashed)
                    if result_from_cache:
                        # Result already in cache, so return it.
                        logger.debug(
                            f'Cache hit {key_val} - hash {key_hashed[:250]}'
                        )

                        if type(result_from_cache) != dict or not result_from_cache.get("error"):
                            return result_from_cache
                        else:
                            if result_from_cache.get("error") == "CLIENT_ERROR":
                                raise ClientError(result_from_cache.get("response"), result_from_cache.get("operation_name"))
                            else:
                                raise Exception()
                    else:
                        # Result not in cache, make a real call.
                        logger.debug(
                            f'Cache miss {key_val} - hash {key_hashed[:250]}'
                        )
                        return _real_call(ttl, "because the value is not in the ttl_cache")
                else:
                    # there is no cache
                    return _real_call(ttl, "because there is no ttl_cache attached")

        return wrapper

    return decorator


