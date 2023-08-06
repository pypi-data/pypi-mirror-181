from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class TaxGroups(Client):
    def __init__(self, **opts):
        super(TaxGroups, self).__init__(**{**opts, **{"resource": "settings/taxgroups"}})
