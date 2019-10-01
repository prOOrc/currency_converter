import attr


@attr.s
class CurrencyRate(object):
    source = attr.ib(type=str)
    target = attr.ib(type=str)
    value = attr.ib(type=float)
