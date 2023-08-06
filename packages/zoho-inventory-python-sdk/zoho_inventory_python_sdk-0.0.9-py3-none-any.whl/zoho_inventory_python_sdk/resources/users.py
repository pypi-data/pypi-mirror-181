from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class Users(Client):
    def __init__(self, **opts):
        super(Users, self).__init__(**{**opts, **{"resource": "users"}})

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

    def get_current_user(self):
        return self.authenticated_fetch(path=f"me/",
                                        req={
                                            "method": "GET"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def invite(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/invite/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )