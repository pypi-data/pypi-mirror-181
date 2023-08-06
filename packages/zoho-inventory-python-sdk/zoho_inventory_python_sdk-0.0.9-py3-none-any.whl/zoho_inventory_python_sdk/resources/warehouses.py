from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class Warehouses(Client):
    def __init__(self, **opts):
        super(Warehouses, self).__init__(**{**opts, **{"resource": "warehouses"}})

    def list(self, **options):
        raise Exception("Warehouses cannot be listed through this API Endpoint.")

    def create(self, body: dict = None, path_params: dict = None, **kwargs):
        raise Exception("Warehouses cannot be created through this API Endpoint.")

    def update(self, id_: str = "", body: dict = None, path_params: dict = None, **kwargs):
        raise Exception("Warehouses cannot be updated through this API Endpoint.")

    def get(self, id_: str = "", path_params: dict = None, **kwargs):
        raise Exception("Warehouses cannot be retrieved through this API Endpoint.")

    def delete(self, id_: str = "", path_params: dict = None, **kwargs):
        raise Exception("Warehouses cannot be deleted through this API Endpoint.")

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
