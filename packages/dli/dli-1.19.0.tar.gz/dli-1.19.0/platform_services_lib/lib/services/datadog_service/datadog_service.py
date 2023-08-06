#
# Copyright (C) 2022 IHS Markit.
# All Rights Reserved
#
import os
from injector import inject
from datadog import initialize, statsd
from ..cached_fetcher_service import CachedFetcherService


class DataDogService:
    @inject
    def __init__(
        self,
        cached_fetcher_service: CachedFetcherService,
    ):
        self.cached_fetcher_service = cached_fetcher_service
        settings = {
            'statsd_host': '127.0.0.1',  # this is a node-port in kubernetes, needs to remain localhost
            'statsd_port': 8125,
            'statsd_disable_buffering': True,
            'disable_buffering': True
        }
        initialize(**settings)

    @staticmethod
    def send_metric(metric_name: str, content_size_bytes: str, uname, email, organisation_name, path, method):
        statsd.distribution(
            metric_name,
            content_size_bytes,
            tags=[
                f'application:{os.environ.get("DD_APPLICATION_NAME", "Unknown")}',
                f'user:{uname}',
                f'email:{email}',
                f'organisation: {organisation_name}',
                f'path: {path}',
                f'method: {method}',
            ],
            sample_rate=1.0
        )
