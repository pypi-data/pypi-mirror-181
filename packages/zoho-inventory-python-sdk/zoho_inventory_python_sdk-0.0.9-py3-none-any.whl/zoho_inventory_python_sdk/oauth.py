import json
import os
import time
from datetime import datetime, timedelta

from .base_client import BaseClient
from .aws import SecretsManagerClient, SecretsManagerStorage, MissingSetting


class OAuth(BaseClient):
    def __init__(self, **opts):

        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_secretsmanager_secret_name = os.getenv('AWS_SM_ZOHO_INVENTORY_SECRET_NAME')
        self.aws_secretsmanager_region = os.getenv('AWS_DEFAULT_REGION')

        self.secretsmanager_client = SecretsManagerClient.get_instance(
            self.aws_access_key, self.aws_secret_key,
            region_name=self.aws_secretsmanager_region,
        )

        self.secretsmanager_client.name = self.aws_secretsmanager_secret_name

        self.storage = SecretsManagerStorage(secretsmanager_client=self.secretsmanager_client,
                                             name=self.secretsmanager_client.name)

        self.storage.read_config()

        super(OAuth, self).__init__(resource="oauth", path="oauth/v2", origin="https://accounts.zoho.{}".format(
            self.storage.get('zoho_inventory', 'region')))

        self.client_id = self.storage.get('zoho_inventory', 'client_id')
        self.client_secret = self.storage.get('zoho_inventory', 'client_secret')
        self.refresh_token = self.storage.get('zoho_inventory', 'refresh_token')

        try:
            self.expiry_time = self.storage.get('zoho_inventory', 'expiry_time')
        except MissingSetting:
            self.storage.set('zoho_inventory', 'expiry_time', str(time.mktime(datetime(1970, 1, 1, 0, 0,
                                                                                       1).timetuple())))
            self.expiry_time = self.storage.get('zoho_inventory', 'expiry_time')

        try:
            self.access_token = self.storage.get('zoho_inventory', 'access_token')
        except MissingSetting:
            self.refresh_access_token()
            self.access_token = self.storage.get('zoho_inventory', 'access_token')

    def refresh_access_token(self):
        token = self.fetch(
            path="token",
            req={
                "method": "POST",
                "query": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": self.refresh_token,
                    "grant_type": "refresh_token"
                }
            }
        )

        self.access_token = token.get('access_token')
        self.storage.set('zoho_inventory', 'access_token', self.access_token)

        expiry_time = datetime.now() + timedelta(seconds=token.get("expires_in", 0))
        self.expiry_time = time.mktime(datetime(expiry_time.year, expiry_time.month, expiry_time.day,
                                                expiry_time.hour, expiry_time.minute, expiry_time.second).timetuple())
        self.storage.set('zoho_inventory', 'expiry_time', str(self.expiry_time))
        print(self.storage.get('zoho_inventory', 'expiry_time'))

        print('Saving token: {}'.format(
            {s: dict(self.storage.items(s)) for s in self.storage.sections()}))
        self.secretsmanager_client.put_value(
            secret_value=json.dumps(
                {s: dict(self.storage.items(s)) for s in self.storage.sections()}))

        return token

    def revoke_token(self):
        return self.fetch(
            path="token/revoke",
            req={
                "method": "POST",
                "body": {
                    "refresh_token": self.refresh_token
                }
            }
        )