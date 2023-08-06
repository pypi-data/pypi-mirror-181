from ..client import Client


class Bundles(Client):
    def __init__(self, **opts):
        super(Bundles, self).__init__(**{**opts, **{"resource": "bundles"}})
