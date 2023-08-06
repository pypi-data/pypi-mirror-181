from ..client import Client


class CompositeItems(Client):
    def __init__(self, **opts):
        super(CompositeItems, self).__init__(**{**opts, **{"resource": "compositeitems"}})

    def mark_as_active(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/active/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def mark_as_inactive(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/inactive/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    