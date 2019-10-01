import asyncio
import os

import aioredis
import pinject

from currency_converter.data_access.currency_rate_repository import (
    CurrencyRateRepository,
)
from currency_converter.domain.currency_converter import CurrencyConverter
from currency_converter.services.currency_converter_service import (
    CurrencyConverterService,
)


class CurrencyConverterBindingSpec(pinject.BindingSpec):
    def provide_redis(self, redis_url: str) -> aioredis.Redis:
        loop = asyncio.get_event_loop()
        redis = loop.run_until_complete(aioredis.create_redis_pool(redis_url))
        return redis

    def configure(self, bind):
        bind(
            'redis_url',
            to_instance=os.getenv('REDIS_URL', 'redis://localhost'),
        )
        bind('currency_converter', to_class=CurrencyConverter)
        bind('currency_converter_service', to_class=CurrencyConverterService)
        bind('currency_rate_repository', to_class=CurrencyRateRepository)


di_container = pinject.new_object_graph(
    binding_specs=[CurrencyConverterBindingSpec()], modules=None
)
