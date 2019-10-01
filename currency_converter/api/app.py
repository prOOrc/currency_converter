from aiohttp import web

from currency_converter.di_container import di_container
from .handler import CurrencyConverterHandler

handler: CurrencyConverterHandler = di_container.provide(
    CurrencyConverterHandler
)

app = web.Application()
app.add_routes(
    [web.get('/convert', handler.convert), web.post('/database', handler.save)]
)
