from ..client import Client


class Contacts(Client):
    def __init__(self, **opts):
        super(Contacts, self).__init__(**{**opts, **{"resource": "contacts"}})

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

    def send_email_statement(self, id_: str = "", body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f"{id_}/statements/email/",
                                        req={
                                            "method": "POST",
                                            "body": body,
                                            "query": query,
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True
                                        )

    def get_email_statement(self, id_: str = "", query: dict = None):
        return self.authenticated_fetch(path=f"{id_}/statements/email/",
                                        req={
                                            "method": "GET",
                                            "query": query,
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def send_email(self, id_: str = "", body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f"{id_}/email/",
                                        req={
                                            "method": "POST",
                                            "body": body,
                                            "query": query,
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True
                                        )

    def list_comments(self, id_: str = "", query: dict = None):
        return self.authenticated_fetch(path=f"{id_}/comments/",
                                        req={
                                            "method": "GET",
                                            "query": query,
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def list_contact_persons(self, id_: str = '', **options):
        return self.authenticated_fetch(path=f"{id_}/contactpersons/", **options)
