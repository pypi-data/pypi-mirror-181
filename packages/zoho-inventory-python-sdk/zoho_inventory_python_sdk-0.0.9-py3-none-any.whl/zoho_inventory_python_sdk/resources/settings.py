from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class Settings(Client):
    def __init__(self, **opts):
        super(Settings, self).__init__(**{**opts, **{"resource": "settings"}})

    def list(self, **options):
        raise Exception("Settings cannot be listed.")

    def create(self, body: dict = None, path_params: dict = None, **kwargs):
        raise Exception("Settings cannot be created.")

    def update(self, id_: str = "", body: dict = None, path_params: dict = None, **kwargs):
        raise Exception("Settings cannot be updated.")

    def get(self, id_: str = "", path_params: dict = None, **kwargs):
        raise Exception("Settings cannot be retrieved.")

    def delete(self, id_: str = "", path_params: dict = None, **kwargs):
        raise Exception("Settings cannot be deleted.")

    def enable_multiwarehouse(self):
        return self.authenticated_fetch(path=f"multiwarehouse/enable/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )
