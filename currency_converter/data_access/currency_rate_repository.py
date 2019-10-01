from typing import List

import aioredis
import attr

from currency_converter.domain.abstract_currency_rate_repository import (
    AbstractCurrencyRateRepository,
)
from currency_converter.domain.currency_rate import CurrencyRate
from currency_converter.errors import CurrencyRateNotExist


@attr.s
class CurrencyRateRepository(AbstractCurrencyRateRepository):
    redis = attr.ib(type=aioredis.Redis)
    currency_rates_hash_key = 'currency_rates'

    def __get_currency_rate_key(self, source: str, target: str) -> str:
        return '{}:{}'.format(source, target)

    async def get(self, source: str, target: str) -> CurrencyRate:
        rates = await self.redis.hmget(
            self.currency_rates_hash_key,
            self.__get_currency_rate_key(source, target),
        )
        if rates[0] is None:
            raise CurrencyRateNotExist()
        return CurrencyRate(source=source, target=target, value=float(rates[0]))

    async def update(self, currency_rate: CurrencyRate) -> CurrencyRate:
        await self.redis.hmset_dict(
            self.currency_rates_hash_key,
            {
                self.__get_currency_rate_key(
                    currency_rate.source, currency_rate.target
                ): currency_rate.value
            },
        )
        return currency_rate

    async def update_many(
            self, currency_rates: List[CurrencyRate]
    ) -> List[CurrencyRate]:
        await self.redis.hmset_dict(
            self.currency_rates_hash_key,
            {
                self.__get_currency_rate_key(
                    currency_rate.source, currency_rate.target
                ): currency_rate.value
                for currency_rate in currency_rates
            },
        )
        return currency_rates

    async def replace_all(
            self, currency_rates: List[CurrencyRate]
    ) -> List[CurrencyRate]:
        tr = self.redis.multi_exec()
        tr.delete(self.currency_rates_hash_key)
        tr.hmset_dict(
            self.currency_rates_hash_key,
            {
                self.__get_currency_rate_key(
                    currency_rate.source, currency_rate.target
                ): currency_rate.value
                for currency_rate in currency_rates
            },
        )
        await tr.execute()
        return currency_rates
