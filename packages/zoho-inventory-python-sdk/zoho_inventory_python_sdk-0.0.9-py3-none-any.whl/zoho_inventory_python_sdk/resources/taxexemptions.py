from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class TaxExemptions(Client):
    def __init__(self, **opts):
        super(TaxExemptions, self).__init__(**{**opts, **{"resource": "settings/taxexemptions"}})
