from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class Currencies(Client):
    def __init__(self, **opts):
        super(Currencies, self).__init__(**{**opts, **{"resource": "settings/currencies"}})
