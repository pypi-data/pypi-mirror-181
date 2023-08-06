from .base_client import BaseClient
from .oauth_manager import OAuthManager


class Client(BaseClient):
    def __init__(self, **opts):
        self.oauth_manager = OAuthManager(**opts)
        super(Client, self).__init__(organization_id=self.oauth_manager.client.storage.get('zoho_inventory',
                                                                                           'organization_id'),
                                     region=self.oauth_manager.client.storage.get('zoho_inventory', 'region'), **opts)

    def authenticated_fetch(self, path: str = None, req: dict = None, mimetype: str = "application/json",
                            encode_json_string: bool = False):

        access_token = self.oauth_manager.get_access_token()

        if req is None:
            req = dict()

        if "headers" in req:
            headers_auth = {**req["headers"], **{"authorization": "Zoho-oauthtoken {}".format(access_token)}}
        else:
            headers_auth = {**{"authorization": "Zoho-oauthtoken {}".format(access_token)}}

        return self.fetch(path=path,
                          req={
                              "method": req.get("method", "GET"),
                              "path_params": req.get("path_params", dict()),
                              "query": req.get("query", dict()),
                              "headers": headers_auth,
                              "body": req.get("body", dict()),
                          },
                          mimetype=mimetype,
                          encode_json_string=encode_json_string
                          )

    def list(self, **options):
        return self.authenticated_fetch(path="", **options)

    def create(self, body: dict = None, path_params: dict = None, **kwargs):
        return self.authenticated_fetch(path="",
                                        req={
                                            "method": "POST",
                                            "path_params": path_params,
                                            "body": body,
                                        },
                                        mimetype=kwargs.get("mimetype", "application/x-www-form-urlencoded"),
                                        encode_json_string=kwargs.get("encode_json_string", True)
                                        )

    def get(self, id_: str = "", path_params: dict = None, **kwargs):
        return self.authenticated_fetch(path=f"{id_}/", req={"path_params": path_params},
                                        mimetype=kwargs.get("mimetype", "application/x-www-form-urlencoded"),
                                        encode_json_string=kwargs.get("encode_json_string", False))

    def update(self, id_: str = "", body: dict = None, path_params: dict = None, **kwargs):
        return self.authenticated_fetch(path=f"{id_}/",
                                        req={
                                            "method": "PUT",
                                            "path_params": path_params,
                                            "body": body,
                                        },
                                        mimetype=kwargs.get("mimetype", "application/x-www-form-urlencoded"),
                                        encode_json_string=kwargs.get("encode_json_string", True)
                                        )

    def delete(self, id_: str = "", path_params: dict = None, **kwargs):
        return self.authenticated_fetch(path=f"{id_}/",
                                        req={
                                            "method": "DELETE",
                                            "path_params": path_params,
                                        },
                                        mimetype=kwargs.get("mimetype", "application/x-www-form-urlencoded"),
                                        encode_json_string=kwargs.get("encode_json_string", False)
                                        )
