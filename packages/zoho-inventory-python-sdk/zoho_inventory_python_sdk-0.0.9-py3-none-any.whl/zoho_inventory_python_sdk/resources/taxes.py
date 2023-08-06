from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class Taxes(Client):
    def __init__(self, **opts):
        super(Taxes, self).__init__(**{**opts, **{"resource": "settings/taxes"}})
