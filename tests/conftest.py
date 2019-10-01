import random
import string

import pytest

from currency_converter.domain.currency_rate import CurrencyRate


@pytest.fixture
def create_currency_name():
    def _create_currency_name(**kwargs):
        kwargs.setdefault('k', 3)
        kwargs.setdefault('population', string.ascii_uppercase)
        return ''.join(random.choices(**kwargs))

    return _create_currency_name


@pytest.fixture
def currency_name(create_currency_name):
    return create_currency_name()


@pytest.fixture
def create_currency_rate_value():
    def _create_currency_rate_value():
        return random.uniform(0.01, 500.0)

    return _create_currency_rate_value


@pytest.fixture
def create_random_float():
    def _create_random_float():
        return random.uniform(0.01, 50000.0)

    return _create_random_float


@pytest.fixture
def create_amount():
    def _create_amount():
        return random.randint(100, 1000)

    return _create_amount


@pytest.fixture
def create_currency_rate(create_currency_name, create_currency_rate_value):
    def _create_currency_rate(**kwargs):
        kwargs.setdefault('source', create_currency_name())
        kwargs.setdefault('target', create_currency_name())
        kwargs.setdefault('value', create_currency_rate_value())
        return CurrencyRate(**kwargs)

    return _create_currency_rate


@pytest.fixture
def currency_rate(create_currency_rate):
    return create_currency_rate()


@pytest.fixture(params=[True, False])
def merge(request):
    return request.param
