import json
from json import JSONDecodeError
from typing import Callable

import attr
import pytest
from aiohttp.test_utils import make_mocked_request
from asynctest import CoroutineMock
from yarl import URL

from currency_converter.api.handler import CurrencyConverterHandler
from currency_converter.domain.currency_rate import CurrencyRate
from currency_converter.errors import CurrencyRateNotExist


@pytest.mark.asyncio
async def test_convert(
    mocker,
    create_currency_name: Callable[[], str],
    create_amount: Callable[[], float],
    create_random_float: Callable[[], float],
):
    _from = create_currency_name()
    _to = create_currency_name()
    amount = create_amount()

    result = create_random_float()
    currency_converter_service = mocker.Mock(
        convert=CoroutineMock(return_value=result)
    )

    handler = CurrencyConverterHandler(
        currency_converter_service=currency_converter_service
    )

    req = make_mocked_request(
        'GET',
        path=str(
            URL('/convert').with_query(
                [
                    ('from', str(_from)),
                    ('to', str(_to)),
                    ('amount', str(amount)),
                ]
            )
        ),
    )
    resp = await handler.convert(req)
    assert resp.status == 200
    assert resp.body == json.dumps({'result': result}).encode()
    currency_converter_service.convert.assert_called_once_with(
        _from, _to, amount
    )


@pytest.mark.asyncio
async def test_convert_not_enough_query_params(
    mocker,
    create_currency_name: Callable[[], str],
    create_amount: Callable[[], float],
    create_random_float: Callable[[], float],
):
    _from = create_currency_name()
    amount = create_amount()

    currency_converter_service = mocker.Mock()

    handler = CurrencyConverterHandler(
        currency_converter_service=currency_converter_service
    )

    req = make_mocked_request(
        'GET',
        path=str(
            URL('/convert').with_query(
                [('from', str(_from)), ('amount', str(amount))]
            )
        ),
    )
    resp = await handler.convert(req)
    assert resp.status == 400


@pytest.mark.asyncio
async def test_convert_incorrect_amount_value(
    mocker, create_currency_name: Callable[[], str]
):
    _from = create_currency_name()
    _to = create_currency_name()
    amount = 'somestring'

    currency_converter_service = mocker.Mock()

    handler = CurrencyConverterHandler(
        currency_converter_service=currency_converter_service
    )

    req = make_mocked_request(
        'GET',
        path=str(
            URL('/convert').with_query(
                [
                    ('from', str(_from)),
                    ('to', str(_to)),
                    ('amount', str(amount)),
                ]
            )
        ),
    )
    resp = await handler.convert(req)
    assert resp.status == 400


@pytest.mark.asyncio
async def test_convert_not_exist(
    mocker,
    create_currency_name: Callable[[], str],
    create_amount: Callable[[], float],
):
    _from = create_currency_name()
    _to = create_currency_name()
    amount = create_amount()

    async def fake_convert(*args, **kwargs):
        raise CurrencyRateNotExist()

    currency_converter_service = mocker.Mock(
        convert=CoroutineMock(side_effect=fake_convert)
    )

    handler = CurrencyConverterHandler(
        currency_converter_service=currency_converter_service
    )

    req = make_mocked_request(
        'GET',
        path=str(
            URL('/convert').with_query(
                [
                    ('from', str(_from)),
                    ('to', str(_to)),
                    ('amount', str(amount)),
                ]
            )
        ),
    )
    resp = await handler.convert(req)
    assert resp.status == 404
    currency_converter_service.convert.assert_called_once_with(
        _from, _to, amount
    )


@pytest.mark.asyncio
async def test_save_ok(
    mocker, create_currency_rate: Callable[[], CurrencyRate], merge: bool
):
    currency_rates = [create_currency_rate() for _ in range(10)]

    currency_converter_service = mocker.Mock(
        save=CoroutineMock(return_value=currency_rates)
    )

    handler = CurrencyConverterHandler(
        currency_converter_service=currency_converter_service
    )

    req = make_mocked_request(
        'POST',
        path=str(URL('/database').with_query([('merge', str(int(merge)))])),
    )

    mocker.patch.object(
        req,
        'json',
        CoroutineMock(
            return_value=[
                {'from': s.source, 'to': s.target, 'rate': s.value}
                for s in currency_rates
            ]
        ),
    )

    resp = await handler.save(req)
    assert resp.status == 200
    assert (
        resp.body
        == json.dumps(
            {'result': [attr.asdict(s) for s in currency_rates]}
        ).encode()
    )
    currency_converter_service.save.assert_called_once_with(
        currency_rates, merge
    )


@pytest.mark.asyncio
async def test_save_incorrect_merge_value(
    mocker, create_currency_rate: Callable[[], CurrencyRate], merge: bool
):
    currency_converter_service = mocker.Mock()

    handler = CurrencyConverterHandler(
        currency_converter_service=currency_converter_service
    )

    req = make_mocked_request(
        'POST',
        path=str(URL('/database').with_query([('merge', 'incorrect_value')])),
    )

    resp = await handler.save(req)
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_save_incorrect_json(
    mocker, create_currency_rate: Callable[[], CurrencyRate], merge: bool
):
    handler = CurrencyConverterHandler(
        currency_converter_service=mocker.Mock()
    )

    req = make_mocked_request(
        'POST',
        path=str(URL('/database').with_query([('merge', str(int(merge)))])),
    )

    async def fake_request_json():
        raise JSONDecodeError('a', 'b', 0)

    mocker.patch.object(
        req, 'json', CoroutineMock(side_effect=fake_request_json)
    )

    resp = await handler.save(req)
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_save_not_enough_keys_in_json(
    mocker, create_currency_rate: Callable[[], CurrencyRate], merge: bool
):
    currency_rates = [create_currency_rate() for _ in range(10)]

    handler = CurrencyConverterHandler(
        currency_converter_service=mocker.Mock()
    )

    req = make_mocked_request(
        'POST',
        path=str(URL('/database').with_query([('merge', str(int(merge)))])),
    )

    mocker.patch.object(
        req,
        'json',
        CoroutineMock(
            return_value=[
                {'from': s.source, 'to': s.target} for s in currency_rates
            ]
        ),
    )

    resp = await handler.save(req)
    assert resp.status_code == 400
