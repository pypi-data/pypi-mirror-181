from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class WarehouseSettings(Client):
    def __init__(self, **opts):
        super(WarehouseSettings, self).__init__(**{**opts, **{"resource": "settings/warehouses"}})

    def mark_as_primary(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/markasprimary/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )
