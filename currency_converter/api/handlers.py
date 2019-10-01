from json import JSONDecodeError

import attr
from aiohttp import web

from currency_converter.di_container import di_container
from currency_converter.domain.currency_rate import CurrencyRate
from currency_converter.errors import CurrencyRateNotExist
from currency_converter.services.currency_converter_service import (
    CurrencyConverterService,
)

currency_converter_service: CurrencyConverterService = di_container.provide(
    CurrencyConverterService
)


async def convert(request: web.BaseRequest):
    source = request.query.get('from')
    target = request.query.get('to')
    amount = request.query.get('amount')
    if not all([source, target, amount]):
        return web.HTTPBadRequest()
    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return web.HTTPBadRequest()

    try:
        result = await currency_converter_service.convert(
            source, target, amount
        )
    except CurrencyRateNotExist:
        return web.HTTPNotFound()

    return web.json_response({'result': result})


async def save(request: web.BaseRequest):
    try:
        merge = bool(int(request.query.get('merge')))
    except (ValueError, TypeError):
        return web.HTTPBadRequest
    try:
        serialized_currency_rates = await request.json()
    except JSONDecodeError:
        return web.HTTPBadRequest
    try:
        currency_rates = [
            CurrencyRate(
                source=serialized_currency_rate['from'],
                target=serialized_currency_rate['to'],
                value=serialized_currency_rate['rate'],
            )
            for serialized_currency_rate in serialized_currency_rates
        ]
    except KeyError:
        return web.HTTPBadRequest
    saved_currency_rates = await currency_converter_service.save(
        currency_rates, merge
    )

    return web.json_response(
        {'result': [attr.asdict(r) for r in saved_currency_rates]}
    )
