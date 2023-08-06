from ..client import Client


'''
TODO: Override or refactor Client methods create and update to accept query parameters.
'''


class TransferOrders(Client):
    def __init__(self, **opts):
        super(TransferOrders, self).__init__(**{**opts, **{"resource": "transferorders"}})

    def mark_as_transferred(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/markastransferred/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )
