from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class TaxAuthorities(Client):
    def __init__(self, **opts):
        super(TaxAuthorities, self).__init__(**{**opts, **{"resource": "settings/taxauthorities"}})
