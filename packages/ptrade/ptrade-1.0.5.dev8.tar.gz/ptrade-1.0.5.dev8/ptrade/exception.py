class __BaseError(Exception):
    name = ''

    def __init__(self, msg, *args):
        self.msg = '【%s】' % self.name
        self.msg += msg
        for arg in args:
            self.msg += str(arg)

    def __str__(self):
        return self.msg


class PriceError(__BaseError):
    name = 'PriceError'


class OrderError(__BaseError):
    name = 'orderError'


class ParamError(__BaseError):
    name = 'ParamError'


class MoneyError(__BaseError):
    name = 'MoneyError'


class PosSideParamError(ParamError):
    def __init__(self, posSide):
        msg = f'posSide={posSide}，posSide应该属于["long","short"]'
        super(PosSideParamError, self).__init__(msg=msg)


class ToModeParamError(ParamError):
    def __init__(self, toMode):
        msg = f'toMode={toMode}，toMode应该属于["cross","isolated"]'
        super(ToModeParamError, self).__init__(msg=msg)


class TraderError(__BaseError):
    name = 'TraderError'


class UnexpectError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg