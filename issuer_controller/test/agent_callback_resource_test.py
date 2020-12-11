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


def test_agent_callback_unknown_topic(test_client):
    get_resp = test_client.post(f'/api/agentcb/topic/random-action/')
    assert get_resp.status_code == 400