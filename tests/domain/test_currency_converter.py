import pytest

from currency_converter.domain.currency_converter import CurrencyConverter
from currency_converter.domain.currency_rate import CurrencyRate


@pytest.mark.parametrize('currency_rate, amount, expected_result', [
    (CurrencyRate('RUB', 'USD', 65.5), 35, 2292.5),
    (CurrencyRate('USD', 'RUB', 0.165), 5523, 911.3),
])
def test_convert_ok(currency_rate: CurrencyRate, amount: float, expected_result: float):
    converter = CurrencyConverter()
    result = converter.convert(currency_rate, amount)
    assert round(result, 2) == round(expected_result, 2)
