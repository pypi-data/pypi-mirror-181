import re
import requests
import json


class BaseClient:
    def __init__(self, resource: str = None, path: str = None, origin: str = None, organization_id: str = None,
                 region: str = 'com', **opts):
        self.resource = resource
        self.path = path or resource
        self.origin = origin or "https://inventory.zoho.{}/api/v1".format(region)
        self.url = re.sub(r"\/$", "", self.origin) + "/" + self.path + "/"

        self.headers = {}

        self.query = {
            'organization_id': organization_id
        }

    def fetch(self, path: str = None, req: dict = None, mimetype: str = "application/json",
              encode_json_string: bool = False):
        if "method" not in req:
            req["method"] = "GET"
        if "path_params" not in req:
            req["path_params"] = {}
        if "query" not in req:
            req["query"] = {}
        if "body" not in req:
            req["body"] = {}
        if "headers" not in req:
            req["headers"] = {}

        if encode_json_string:
            req["body"] = self.form_encode(req.get("body"))

        req.get('query', {}).update(self.query)
        target = self._replace_path(self.url + path, req["path_params"])

        headers = {**self.headers, **{"content-type": mimetype}, **req["headers"]}

        response = requests.request(req["method"], target.rstrip("/"), headers=headers, params=req["query"],
                                    data=req["body"])

        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response

    @staticmethod
    def _replace_path(path: str = None, path_params: dict = None) -> str:
        if path_params is None:
            path_params = {}
        new_path = path
        for key in path_params:
            new_path = new_path.replace(':' + key, path_params[key])
        return new_path

    @staticmethod
    def form_encode(body: str = None) -> dict:
        form = {'JSONString': json.dumps(body, separators=(',', ':'))}
        return form
