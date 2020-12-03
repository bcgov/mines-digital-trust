from app.issuer import SendCredentialThread, app_config, ADMIN_REQUEST_HEADERS, TRACE_MSG_PCT

import random, time
from flask import jsonify, current_app


def handle_send_credential(cred_input):
    """
    # other sample data
    sample_credentials = [
        {
            "schema": "ian-registration.ian-ville",
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
                "effective_date": "2019-01-01",
                "expiry_date": ""
            }
        },
        {
            "schema": "ian-permit.ian-ville",
            "version": "1.0.0",
            "attributes": {
                "permit_id": str(uuid.uuid4()),
                "entity_name": "Ima Permit",
                "corp_num": "ABC12345",
                "permit_issued_date": "2018-01-01", 
                "permit_type": "ABC", 
                "permit_status": "OK", 
                "effective_date": "2019-01-01"
            }
        }
    ]
    """
    # construct and send the credential
    # print("Received credentials", cred_input)
    global app_config

    agent_admin_url = app_config["AGENT_ADMIN_URL"]

    start_time = time.perf_counter()
    processing_time = 0
    processed_count = 0

    # let's send a credential!
    cred_responses = []
    for credential in cred_input:
        #current_app.logger.warn(app_config['schemas'].keys())
        cred_def_key = "CRED_DEF_" + credential["schema"] + "_" + credential["version"]
        credential_definition_id = app_config["schemas"][cred_def_key]
        #TODO safe access and pretty error message

        credential_attributes = []
        for attribute in credential["attributes"]:
            credential_attributes.append({
                "name": attribute,
                "mime-type": "text/plain",
                "value": credential["attributes"][attribute]
                })
        cred_offer = {
          "schema_id": app_config["schemas"][
                    "SCHEMA_" + credential["schema"] + "_" + credential["version"]
                ],
          "schema_name": credential["schema"],
          "issuer_did": app_config["DID"],
          "schema_version": credential["version"],
          "credential_proposal": {
            "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
            "attributes": credential_attributes
          },
          "schema_issuer_did": app_config["DID"],
          "cred_def_id": credential_definition_id,
          "comment": "",
          "connection_id": app_config["TOB_CONNECTION"],
        }
        do_trace = random.randint(1, 100)
        if do_trace <= TRACE_MSG_PCT:
            cred_offer["trace"] = True
        thread = SendCredentialThread(
            credential_definition_id,
            cred_offer,
            agent_admin_url + "/issue-credential/send",
            ADMIN_REQUEST_HEADERS,
        )
        print(thread)
        thread.start()
        thread.join()
        cred_responses.append(thread.cred_response)
        processed_count = processed_count + 1

    processing_time = time.perf_counter() - start_time
    print(">>> Processed", processed_count, "credentials in", processing_time)
    print("   ", processing_time / processed_count, "seconds per credential")

    return jsonify(cred_responses)