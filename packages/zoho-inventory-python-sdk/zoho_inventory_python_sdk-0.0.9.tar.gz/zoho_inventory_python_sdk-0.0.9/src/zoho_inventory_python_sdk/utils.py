import os
import json
from jsonmerge import merge


def load_configuration(oauth_config_path: str = None, zoho_config_path: str = None) -> dict:
    return {
        'oauth_config': load_oauth_configuration(oauth_config_path),
        'zoho_config': load_zoho_configuration(zoho_config_path)
    }


def load_oauth_configuration(path: str = None) -> dict:
    env = {
        'client_id': os.getenv('ZOHO_CLIENT_ID'),
        'client_secret': os.getenv('ZOHO_CLIENT_SECRET'),
        'refresh_token': os.getenv('ZOHO_REFRESH_TOKEN'),
        'redirect_uri': os.getenv('ZOHO_REDIRECT_URI'),
        'scope': os.getenv('ZOHO_SCOPE'),
    }

    config = merge(env, read_json_file(path))

    if 'client_id' not in config:
        demand_configuration(path, 'client_id', 'ZOHO_CLIENT_ID')
    if 'client_secret' not in config:
        demand_configuration(path, 'client_secret', 'ZOHO_CLIENT_SECRET')
    if 'refresh_token' not in config:
        demand_configuration(path, 'refresh_token', 'ZOHO_REFRESH_TOKEN')

    print(config)
    return config


def load_zoho_configuration(path: str = None) -> dict:
    env = {
        'region': os.getenv('ZOHO_REGION'),
        'organization_id': os.getenv('ZOHO_ORGANIZATION_ID')
    }

    config = merge(env, read_json_file(path))

    if 'region' not in config:
        demand_configuration(path, 'region', 'ZOHO_REGION')
    if 'organization_id' not in config:
        demand_configuration(path, 'organization_id', 'ZOHO_ORGANIZATION_ID')

    return config


def demand_configuration(path: str = None, key: str = None, env: str = None):
    raise Exception("Missing required config {}. Either:\n\
    1. Update {} in {}\n\
    2. Set {} in environment variables".format(key, key, path, env))


def read_json_file(path: str = None) -> dict:
    json_dict = {}
    if path:
        with open(path, "r", encoding="utf-8") as json_file:
            json_dict = json.load(json_file)

    return json_dict
