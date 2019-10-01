import attr

from .currency_rate import CurrencyRate


@attr.s
class CurrencyConverter(object):
    def convert(self, currency_rate: CurrencyRate, amount: float) -> float:
        return currency_rate.value * amount
