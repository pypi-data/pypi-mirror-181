from ..client import Client


'''
TODO: Override or refactor Client methods create and update to accept query parameters.
'''


class Packages(Client):
    def __init__(self, **opts):
        super(Packages, self).__init__(**{**opts, **{"resource": "packages"}})

    def print(self, **kwargs):
        return self.authenticated_fetch(path=f"print/",
                                        req={
                                            "query": kwargs.get("query", {})
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )
