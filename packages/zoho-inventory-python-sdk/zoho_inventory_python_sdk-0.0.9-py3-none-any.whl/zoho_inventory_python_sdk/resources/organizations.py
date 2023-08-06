from ..client import Client


class Organizations(Client):
    def __init__(self, **opts):
        super(Organizations, self).__init__(**{**opts, **{"resource": "organizations"}})
