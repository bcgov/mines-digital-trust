import pytest, os, pprint

from app.app import create_app
from app import config, issuer

from unittest.mock import patch
from requests.models import Response
from app.config import TestConfig

@pytest.fixture(scope="session")
def app(request):
    # # Load application settings (environment)
    # mock_tob_connection_response = Response(_content=json.dumps(mock_tob_connection_json))
    # with patch('app.issuer.requests.get', side_effect=[response])as mock:
    config_root = os.environ.get('CONFIG_ROOT', './config')
    ENV = config.load_settings(config_root=config_root)
    app = create_app(TestConfig)
    return app

@pytest.fixture(scope='session')
def test_client(app):
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    #print(app.url_map)
    yield client
    ctx.pop()