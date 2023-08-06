from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class PurchaseOrders(Client):
    def __init__(self, **opts):
        super(PurchaseOrders, self).__init__(**{**opts, **{"resource": "purchaseorders"}})

    def mark_as_issued(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/status/issued/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def mark_as_cancelled(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/status/cancelled/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )