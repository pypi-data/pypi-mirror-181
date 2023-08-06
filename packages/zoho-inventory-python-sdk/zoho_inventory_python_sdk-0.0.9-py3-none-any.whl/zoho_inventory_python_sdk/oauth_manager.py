import os
from datetime import datetime

from .oauth import OAuth

from zoho_inventory_python_sdk.aws import MissingSetting


class OAuthManager:
    def __init__(self, **opts):
        self.client = OAuth(**opts)

    def get_access_token(self):
        if self.client.access_token and not self.is_access_token_expired():
            return self.client.access_token

        token = self.client.refresh_access_token()

        return token.get("access_token")

    def is_access_token_expired(self):
        if not self.client.access_token:
            return True

        now = datetime.now()

        if now >= datetime.fromtimestamp(float(self.client.expiry_time)):
            return True

        return False
