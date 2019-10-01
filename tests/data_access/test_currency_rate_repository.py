from typing import Callable

import pytest
from asynctest import CoroutineMock

from currency_converter.data_access.currency_rate_repository import (
    CurrencyRateRepository,
)
from currency_converter.domain.currency_rate import CurrencyRate
from currency_converter.errors import CurrencyRateNotExist


@pytest.mark.asyncio
async def test_get_exist(
    mocker,
    create_currency_name: Callable[[], str],
    create_currency_rate_value: Callable[[], float],
):
    source = create_currency_name()
    target = create_currency_name()
    currency_rate_value = create_currency_rate_value()
    redis = mocker.Mock(
        hmget=CoroutineMock(return_value=[str(currency_rate_value).encode()])
    )

    currency_rate_repository = CurrencyRateRepository(redis=redis)
    result = await currency_rate_repository.get(source, target)
    assert result.value == currency_rate_value
    redis.hmget.assert_called()


@pytest.mark.asyncio
async def test_get_not_exist(mocker, create_currency_name: Callable[[], str]):
    source = create_currency_name()
    target = create_currency_name()
    redis = mocker.Mock(hmget=CoroutineMock(return_value=[None]))

    currency_rate_repository = CurrencyRateRepository(redis=redis)
    with pytest.raises(CurrencyRateNotExist):
        await currency_rate_repository.get(source, target)
    redis.hmget.assert_called()


@pytest.mark.asyncio
async def test_update(mocker, currency_rate: CurrencyRate):
    redis = mocker.Mock(hmset_dict=CoroutineMock())

    currency_rate_repository = CurrencyRateRepository(redis=redis)
    result = await currency_rate_repository.update(currency_rate)
    assert result == currency_rate
    redis.hmset_dict.assert_called()


@pytest.mark.asyncio
async def test_update_many(
    mocker, create_currency_rate: Callable[[], CurrencyRate]
):
    currency_rates = [create_currency_rate() for _ in range(10)]

    redis = mocker.Mock(hmset_dict=CoroutineMock())

    currency_rate_repository = CurrencyRateRepository(redis=redis)
    result = await currency_rate_repository.update_many(currency_rates)
    assert result == currency_rates
    redis.hmset_dict.assert_called()


@pytest.mark.asyncio
async def test_replace_all(
    mocker, create_currency_rate: Callable[[], CurrencyRate]
):
    currency_rates = [create_currency_rate() for _ in range(10)]

    multi_exec = mocker.Mock(
        delete=mocker.Mock(), hmset_dict=mocker.Mock(), execute=CoroutineMock()
    )

    redis = mocker.Mock(multi_exec=mocker.Mock(return_value=multi_exec))
    currency_rate_repository = CurrencyRateRepository(redis=redis)
    result = await currency_rate_repository.replace_all(currency_rates)
    assert result == currency_rates
    multi_exec.delete.assert_called_once_with(
        currency_rate_repository.currency_rates_hash_key
    )
    multi_exec.hmset_dict.assert_called()
    multi_exec.execute.assert_called()
