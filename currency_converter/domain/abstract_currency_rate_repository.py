from abc import ABCMeta, abstractmethod
from typing import List

from .currency_rate import CurrencyRate


class AbstractCurrencyRateRepository(object, metaclass=ABCMeta):

    @abstractmethod
    async def get(self, source: str, target: str) -> CurrencyRate:
        pass

    @abstractmethod
    async def update(self, currency_rate: CurrencyRate) -> CurrencyRate:
        pass

    @abstractmethod
    async def update_many(self, currency_rates: List[CurrencyRate]) -> List[CurrencyRate]:
        pass

    @abstractmethod
    async def replace_all(self, currency_rates: List[CurrencyRate]) -> List[CurrencyRate]:
        pass
