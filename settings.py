import os

root_path = os.path.abspath(os.path.dirname(__file__))

# APP CONFIG
APP_ID = '0697782b-8967-11f0-a2f8-080027820c69'
NAME = 'Workbench'
NA_ME = 'workbench'

SSL_KEYFILE = None
SSL_CERTFILE = None
DOMAIN = 'localhost'
PORT = 8002

BASE_URL = f"{'https' if SSL_CERTFILE else 'http'}://{DOMAIN}:{PORT}"
CONFIG_WEBHOOK_URL = f'{BASE_URL}/user_group_role'
CONFIG_WEBHOOK_METHOD = 'POST'

# endpoint
PAGINATION_PER_PAGE = 50

