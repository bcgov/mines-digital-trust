import pytest, os, pprint

from app.app import init_app
from app import config, issuer

from unittest.mock import patch
from requests.models import Response
from app.config import TestConfig

@pytest.fixture(scope="session")
def app(request):
    app = init_app(TestConfig)
    return app

@pytest.fixture(scope="session")
def secured_app(request):
    conf = TestConfig.copy()
    conf['ISSUER_SECRET_KEY'] = 'TEST_KEY'
    app = init_app(conf)
    return app

@pytest.fixture(scope='session')
def test_client(app):
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()

@pytest.fixture(scope='session')
def test_secured_client(secured_app):
    client = secured_app.test_client()
    ctx = secured_app.app_context()
    ctx.push()
    yield client
    ctx.pop()
