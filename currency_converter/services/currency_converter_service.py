from typing import List

import attr

from currency_converter.domain.abstract_currency_rate_repository import (
    AbstractCurrencyRateRepository,
)
from currency_converter.domain.currency_converter import CurrencyConverter
from currency_converter.domain.currency_rate import CurrencyRate


@attr.s
class CurrencyConverterService(object):
    currency_rate_repository = attr.ib(type=AbstractCurrencyRateRepository)
    currency_converter = attr.ib(type=CurrencyConverter)

    async def convert(self, source: str, target: str, amount: float) -> float:
        currency_rate = await self.currency_rate_repository.get(source, target)
        return self.currency_converter.convert(currency_rate, amount)

    async def save(
        self, currency_rates: List[CurrencyRate], merge=True
    ) -> List[CurrencyRate]:
        if merge:
            return await self.currency_rate_repository.update_many(
                currency_rates
            )
        else:
            return await self.currency_rate_repository.replace_all(
                currency_rates
            )
