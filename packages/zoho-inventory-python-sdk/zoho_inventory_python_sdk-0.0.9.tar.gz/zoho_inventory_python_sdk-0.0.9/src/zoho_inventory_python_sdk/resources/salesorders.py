from ..client import Client


class SalesOrders(Client):
    def __init__(self, **opts):
        super(SalesOrders, self).__init__(**{**opts, **{"resource": "salesorders"}})

    def mark_as_confirmed(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/status/confirmed/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def mark_as_void(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/status/void/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )
