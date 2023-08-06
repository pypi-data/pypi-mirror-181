from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class SalesReturns(Client):
    def __init__(self, **opts):
        super(SalesReturns, self).__init__(**{**opts, **{"resource": "salesreturns"}})