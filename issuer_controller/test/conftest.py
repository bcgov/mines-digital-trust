import pytest
import app

@pytest.fixture(scope="session")
def app(request):
    return app