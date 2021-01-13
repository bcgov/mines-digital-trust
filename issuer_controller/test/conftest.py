import pytest, os, pprint

from app.app import create_app
from app import config, issuer

from unittest.mock import patch
from requests.models import Response
from app.config import TestConfig

@pytest.fixture(scope="session")
def app(request):
    app = create_app(TestConfig)
    return app

@pytest.fixture(scope='session')
def test_client(app):
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()