from ..client import Client


class Items(Client):
    def __init__(self, **opts):
        super(Items, self).__init__(**{**opts, **{"resource": "items"}})

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

    def get_item_image(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/image/",
                                        req={
                                            "method": "GET"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def delete_item_image(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/image/",
                                        req={
                                            "method": "DELETE"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def get_price_book_rate(self, query: dict = None):
        return self.authenticated_fetch(path=f"pricebookrate/",
                                        req={
                                            "method": "POST",
                                            "query": query or {}
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )