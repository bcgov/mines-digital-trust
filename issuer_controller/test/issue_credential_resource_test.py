import pytest,threading,json

from time import sleep

from unittest.mock import MagicMock, patch, PropertyMock
from app import issuer, handle

test_send_credential = [
    {
        "schema": "my-registration.empr",
        "version": "1.0.0",
        "attributes": {
            "corp_num": "ABC12345",
            "registration_date": "2018-01-01", 
            "entity_name": "Ima Permit",
            "entity_name_effective": "2018-01-01", 
            "entity_status": "ACT", 
            "entity_status_effective": "2019-01-01",
            "entity_type": "ABC", 
            "registered_jurisdiction": "BC", 
            "addressee": "A Person",
            "address_line_1": "123 Some Street",
            "city": "Victoria",
            "country": "Canada",
            "postal_code": "V1V1V1",
            "province": "BC",
            "effective_date": "2019-01-01",
            "expiry_date": ""
        }
    },
    {
        "schema": "bcgov-mines-act-permit.empr",
        "version": "1.0.0",
        "attributes": {
            "permit_id": "MYPERMIT12345",
            "entity_name": "Ima Permit",
            "corp_num": "ABC12345",
            "permit_issued_date": "2018-01-01", 
            "permit_type": "ABC", 
            "permit_status": "OK", 
            "effective_date": "2019-01-01"
        }
    }
]


def test_liveness_method(app):
    val = issuer.issuer_liveness_check()
    assert val


def test_liveness_route(test_client):
    print(test_client.__dict__)
    get_resp = test_client.get(f'/liveness')
    assert get_resp.status_code == 200


class MockSendCredentialThread(threading.Thread):
    def __init__(self,*args):
        threading.Thread.__init__(self)
        self.cred_response = {"success": True, "result":"MOCK_RESPONSE"}
        return

    def run(self):
        return    

def test_issue_credential_spawns_thread(app):
    #mock_SendCredentialThread_class()
    with patch('app.handle.SendCredentialThread',new=MockSendCredentialThread) as mock:
        res = handle.handle_send_credential(test_send_credential)
        assert res.status_code == 200
        assert len(json.loads(res.response[0])) == 2