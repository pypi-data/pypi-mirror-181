from ._version import get_versions
from .client import Client
from .base_client import BaseClient
from .oauth_manager import OAuthManager
from .oauth import OAuth
from .utils import load_configuration, load_zoho_configuration, load_oauth_configuration, read_json_file, \
    demand_configuration

from .resources import *

from .aws import *

__version__ = get_versions()['version']
del get_versions
