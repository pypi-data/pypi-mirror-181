from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class PurchaseReceives(Client):
    def __init__(self, **opts):
        super(PurchaseReceives, self).__init__(**{**opts, **{"resource": "purchasereceives"}})

    def list(self, **options):
        raise Exception("Purchase Receives cannot be listed.")
