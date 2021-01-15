import pytest,threading,json, random

from time import sleep

from unittest.mock import MagicMock, patch, PropertyMock
from app.routes import secret_key_required



def test_auth_blocked(secured_app,test_secured_client):
    get_resp = test_secured_client.get(f'/status/reset')
    assert get_resp.status_code == 401

def test_auth_allowed(secured_app,test_secured_client):
    get_resp = test_secured_client.get(f'/status/reset', headers={"Secret-Key":"TEST_KEY"})
    assert get_resp.status_code == 200
