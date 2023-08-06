from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class Bills(Client):
    def __init__(self, **opts):
        super(Bills, self).__init__(**{**opts, **{"resource": "bills"}})

    def mark_as_open(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/status/open/",
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