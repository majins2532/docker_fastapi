from dotenv import load_dotenv
import os

load_dotenv('.config.env')

## Config Base
URL_API_MP = os.getenv('url_api')
PROXY_PATH_ROOT = os.getenv('proxy_path_root')
MAIN_API_PREFIX = f"{PROXY_PATH_ROOT}/api"
ROUTE_PREFIX_V1 = "/v1"
CUS_PREFIX = os.getenv('customer')
SERVER_URL=[
    {"url": f"{os.getenv('domain_server_docs')}", "description": "environment"},
]
VERSION = "0.0.1"

# Default FastAPI
TAGS_METADATA = [
    {
        "name": "Check",
        "description": "Check Server Connect to Odoo and Mongodb",
    }
]
DESCRIPTION = f"""
API APP. 🚀
## API-TOKEN-KEY

You can **API-TOKEN-KEY** : {os.getenv('API_TOKEN_KEY')}
"""

## Config Default
API_TOKEN_KEY = os.getenv('API_TOKEN_KEY')

## Token JWT
from passlib.context import CryptContext
ACCESS_TOKEN_EXPIRE_MINUTES = 0
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "20b99e47adff34058007e61bcafe34d37c2eb84b4acbd0e408e7c9ffd97ff683"
ALGORITHM = "HS256"
USER_API = {
    "ofm": {
        "client_name": "ofm",
        "client_secret": pwd_context.hash("6e79770a20e5c06cff4c895821161d0ff6cb1c71a9c8d631f374704cdfe1601c"),
        "client_type": 1,
        "disabled": False,
    }
}

KEYGOOGLE = {}