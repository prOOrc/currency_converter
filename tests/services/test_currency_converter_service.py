from typing import Callable

import pytest
from asynctest import CoroutineMock

from currency_converter.domain.currency_rate import CurrencyRate
from currency_converter.services.currency_converter_service import (
    CurrencyConverterService,
)


@pytest.mark.asyncio
async def test_convert(
        mocker,
        currency_rate: CurrencyRate,
        create_amount: Callable[[], float],
        create_random_float: Callable[[], float],
):
    expected_result = create_random_float()
    amount = create_amount()
    currency_rate_repository = mocker.Mock(
        get=CoroutineMock(return_value=currency_rate)
    )
    currency_converter = mocker.Mock(
        convert=mocker.Mock(return_value=expected_result)
    )

    currency_convert_service = CurrencyConverterService(
        currency_rate_repository=currency_rate_repository,
        currency_converter=currency_converter,
    )
    result = await currency_convert_service.convert(
        currency_rate.source, currency_rate.target, amount
    )
    assert result == expected_result
    currency_rate_repository.get.assert_called_once_with(
        currency_rate.source, currency_rate.target
    )
    currency_converter.convert.assert_called_once_with(currency_rate, amount)


@pytest.mark.asyncio
async def test_save(
        mocker,
        create_currency_rate: Callable[[], CurrencyRate],
        create_amount: Callable[[], float],
        create_random_float: Callable[[], float],
        merge: bool,
):
    currency_rates = [create_currency_rate() for _ in range(10)]
    if merge:
        currency_rate_repository = mocker.Mock(
            update_many=CoroutineMock(return_value=currency_rates)
        )
    else:
        currency_rate_repository = mocker.Mock(
            replace_all=CoroutineMock(return_value=currency_rates)
        )
    currency_convert_service = CurrencyConverterService(
        currency_rate_repository=currency_rate_repository,
        currency_converter=mocker.Mock(),
    )
    result = await currency_convert_service.save(
        currency_rates, merge
    )
    assert result == currency_rates
    if merge:
        currency_rate_repository.update_many.assert_called_once_with(
            currency_rates
        )
    else:
        currency_rate_repository.replace_all.assert_called_once_with(
            currency_rates
        )
