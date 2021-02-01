import pytest,threading,json, random

from time import sleep

from unittest.mock import MagicMock, patch, PropertyMock
from app import issuer, credential

TOPIC_CONNECTIONS = "connections"
TOPIC_CONNECTIONS_ACTIVITY = "connections_actvity"
TOPIC_CREDENTIALS = "issue_credential"
TOPIC_PRESENTATIONS = "presentations"
TOPIC_GET_ACTIVE_MENU = "get-active-menu"
TOPIC_PERFORM_MENU_ACTION = "perform-menu-action"
TOPIC_ISSUER_REGISTRATION = "issuer_registration"
TOPIC_PROBLEM_REPORT = "problem_report"



def test_agent_callback_missing_json(test_client):
    get_resp = test_client.post(f'/api/agentcb/topic/random-action/')
    assert get_resp.status_code == 400


def test_agent_callback_invalid_topic(test_client):
    data = {
        "test":"value"
    }
    get_resp = test_client.post(f'/api/agentcb/topic/random-action/', json=data)
    assert get_resp.status_code == 400

def test_agent_callback_TOPIC_CONNECTIONS_empty(test_client):
    data = {
        "test":"value"
    }
    get_resp = test_client.post(f'/api/agentcb/topic/'+issuer.TOPIC_CONNECTIONS+'/', json=data)
    assert get_resp.status_code == 200
    get_data = json.loads(get_resp.data.decode())
    assert get_data == {}

def test_agent_callback_TOPIC_CONNECTIONS_ACTIVITY_empty(test_client):
    data = {
        "test":"value"
    }
    get_resp = test_client.post(f'/api/agentcb/topic/'+issuer.TOPIC_CONNECTIONS_ACTIVITY+'/', json=data)
    assert get_resp.status_code == 200
    get_data = json.loads(get_resp.data.decode())
    assert get_data == {}

    
def test_agent_callback_TOPIC_CREDENTIALS_empty(test_client):
    data = {
        "test":"value"
    }
    get_resp = test_client.post(f'/api/agentcb/topic/'+issuer.TOPIC_CREDENTIALS+'/', json=data)
    assert get_resp.status_code == 200
    get_data = json.loads(get_resp.data.decode())
    assert get_data == {}

   
def test_agent_callback_TOPIC_PRESENTATIONS_empty(test_client):
    data = {
        "test":"value"
    }
    get_resp = test_client.post(f'/api/agentcb/topic/'+issuer.TOPIC_PRESENTATIONS+'/', json=data)
    assert get_resp.status_code == 200
    get_data = json.loads(get_resp.data.decode())
    assert get_data == {}

   
def test_agent_callback_TOPIC_GET_ACTIVE_MENU_empty(test_client):
    data = {
        "test":"value"
    }
    get_resp = test_client.post(f'/api/agentcb/topic/'+issuer.TOPIC_GET_ACTIVE_MENU+'/', json=data)
    assert get_resp.status_code == 200
    get_data = json.loads(get_resp.data.decode())
    assert get_data == {}


def test_agent_callback_TOPIC_PERFORM_MENU_ACTION_empty(test_client):
    data = {
        "test":"value"
    }
    get_resp = test_client.post(f'/api/agentcb/topic/'+issuer.TOPIC_PERFORM_MENU_ACTION+'/', json=data)
    assert get_resp.status_code == 200
    get_data = json.loads(get_resp.data.decode())
    assert get_data == {}

   
def test_agent_callback_TOPIC_ISSUER_REGISTRATION_empty(test_client):
    data = {
        "test":"value"
    }
    get_resp = test_client.post(f'/api/agentcb/topic/'+issuer.TOPIC_ISSUER_REGISTRATION+'/', json=data)
    assert get_resp.status_code == 200
    get_data = json.loads(get_resp.data.decode())
    assert get_data == {}

def test_agent_callback_TOPIC_PROBLEM_REPORT_empty(test_client):
    data = {
        "test":"value"
    }
    get_resp = test_client.post(f'/api/agentcb/topic/'+issuer.TOPIC_PROBLEM_REPORT+'/', json=data)
    assert get_resp.status_code == 500
    # empty is not valid

   
# def test_agent_callback_TOPIC_CONNECTIONS_calls_handle_connections(test_client):
#     data = {
#         "state":"value"
#     }
#     with patch('app.routes.issuer.handle_connections') as mock:
#         get_resp = test_client.post(f'/api/agentcb/topic/connections/', json=data, headers={"Content-Type": "application/json"})
#         assert get_resp.status_code == 200
#         get_data = json.loads(get_resp.data.decode())
#         mock.assert_called_with(data["state"], data)