import pytest, os, pprint

from app.app import create_app
from app import config, issuer


from app.config import TestConfig

@pytest.fixture(scope="session")
def app(request):
    # Load application settings (environment)
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