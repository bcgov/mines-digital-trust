import pytest, os
from app.app import Controller

from app import config, issuer


@pytest.fixture(scope="session")
def app(request):
    # Load application settings (environment)
    config_root = os.environ.get('CONFIG_ROOT', './config')
    ENV = config.load_settings(config_root=config_root)
    
    app = Controller(ENV)
    return app