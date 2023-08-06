from ..client import Client


class ContactPersons(Client):
    def __init__(self, **opts):
        super(ContactPersons, self).__init__(**{**opts, **{'resource': 'contactpersons', 'path': 'contacts/contactpersons'}})

    def list(self, **options):
        return self.authenticated_fetch(path='', **options)

    def get(self, id_: str = "", path_params: dict = None, **kwargs):
        return self.authenticated_fetch(path=f"contacts/:contact_id/contactpersons/{id_}/",
                                        req={"path_params": path_params},
                                        mimetype=kwargs.get("mimetype", "application/x-www-form-urlencoded"),
                                        encode_json_string=kwargs.get("encode_json_string", False))

    def mark_as_primary(self, id_: str = None):
        return self.authenticated_fetch(path=f"{id_}/primary/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )
