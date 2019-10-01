from aiohttp import web

from . import handlers

app = web.Application()
app.add_routes(
    [
        web.get('/convert', handlers.convert),
        web.post('/database', handlers.save),
    ]
)
