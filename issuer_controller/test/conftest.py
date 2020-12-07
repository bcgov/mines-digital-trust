import pytest, os

from app.app import create_app
from app import config, issuer


@pytest.fixture(scope="session")
def app(request):
    # Load application settings (environment)
    config_root = os.environ.get('CONFIG_ROOT', './config')
    ENV = config.load_settings(config_root=config_root)

    app = create_app(ENV)
    return app

@pytest.fixture(scope='session')
def test_client():
    config_root = os.environ.get('CONFIG_ROOT', './config')
    ENV = config.load_settings(config_root=config_root)

    app = create_app(ENV)
    
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    #print(app.url_map)
    yield client
    ctx.pop()