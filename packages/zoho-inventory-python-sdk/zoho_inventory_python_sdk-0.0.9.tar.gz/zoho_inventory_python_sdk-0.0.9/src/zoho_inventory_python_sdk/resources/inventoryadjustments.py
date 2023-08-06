from ..client import Client


class InventoryAdjustments(Client):
    def __init__(self, **opts):
        super(InventoryAdjustments, self).__init__(**{**opts, **{"resource": "inventoryadjustments"}})
