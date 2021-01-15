import json
import os
import threading
import time
import random
import pprint
import requests

from flask import jsonify

from app import config, logging

from app.credential import SendCredentialThread, credential_requests, set_credential_thread_id, add_credential_response,add_credential_problem_report

AGENT_ADMIN_API_KEY = os.environ.get("AGENT_ADMIN_API_KEY")
ADMIN_REQUEST_HEADERS = {"Content-Type": "application/json"}
if AGENT_ADMIN_API_KEY is not None and 0 < len(AGENT_ADMIN_API_KEY):
    ADMIN_REQUEST_HEADERS["x-api-key"] = AGENT_ADMIN_API_KEY

TOB_ADMIN_API_KEY = os.environ.get("TOB_ADMIN_API_KEY")
TOB_REQUEST_HEADERS = {}
if TOB_ADMIN_API_KEY is not None and 0 < len(TOB_ADMIN_API_KEY):
    TOB_REQUEST_HEADERS = {"x-api-key": TOB_ADMIN_API_KEY}

# percentage of credential exchanges to trace, between 0 and 100
TRACE_MSG_PCT = int(os.getenv("TRACE_MSG_PCT", "0"))
TRACE_MSG_PCT = max(min(TRACE_MSG_PCT, 100), 0)

ACK_ERROR_PCT = int(os.getenv("ACK_ERROR_PCT", "0"))
ACK_ERROR_PCT = max(min(ACK_ERROR_PCT, 100), 0)


# list of cred defs per schema name/version
app_config = {}
app_config["schemas"] = {}
app_config["running"] = True
app_config["config_services"] = {}
synced = {}

MAX_RETRIES = 3


def agent_post_with_retry(url, payload, headers=None):
    retries = 0
    while True:
        try:
            # test code to test exception handling
            # if retries < MAX_RETRIES:
            #    raise Exception("Fake exception!!!")
            response = requests.post(
                url,
                payload,
                headers=headers,
            )
            response.raise_for_status()
            return response
        except Exception as e:
            logging.LOGGER.error("Error posting %s %s", url, str(e))
            retries = retries + 1
            if retries > MAX_RETRIES:
                raise e
            time.sleep(5)


def agent_schemas_cred_defs(agent_admin_url):
    ret_schemas = {}

    # get loaded cred defs and schemas
    response = requests.get(
        agent_admin_url + "/schemas/created",
        headers=ADMIN_REQUEST_HEADERS,
    )
    response.raise_for_status()
    schemas = response.json()["schema_ids"]
    for schema_id in schemas:
        response = requests.get(
            agent_admin_url + "/schemas/" + schema_id,
            headers=ADMIN_REQUEST_HEADERS,
        )
        response.raise_for_status()
        schema = response.json()["schema"]
        if schema:
            schema_key = schema["name"] + "::" + schema["version"]
            ret_schemas[schema_key] = {
            "schema": schema,
            "schema_id": str(schema["seqNo"])
        }

    response = requests.get(
        agent_admin_url + "/credential-definitions/created",
        headers=ADMIN_REQUEST_HEADERS,
    )
    response.raise_for_status()
    cred_defs = response.json()["credential_definition_ids"]
    for cred_def_id in cred_defs:
        response = requests.get(
            agent_admin_url + "/credential-definitions/" + cred_def_id,
            headers=ADMIN_REQUEST_HEADERS,
        )
        response.raise_for_status()
        cred_def = response.json()["credential_definition"]
        for schema_key in ret_schemas:
            if ret_schemas[schema_key]["schema_id"] == cred_def["schemaId"]:
                ret_schemas[schema_key]["cred_def"] = cred_def
                break

    return ret_schemas

def register_issuer_with_orgbook(connection_id):
    global app_config
    if connection_id in synced and synced[connection_id]:
        return
    app_config["TOB_CONNECTION"] = connection_id
    synced[connection_id] = False
    config_root = app_config["config_root"]
    config_services = app_config["config_services"]
    agent_admin_url = app_config["AGENT_ADMIN_URL"]

    for issuer_name, issuer_info in config_services["issuers"].items():
        # register ourselves (issuer, schema(s), cred def(s)) with TOB
        issuer_config = {
            "name": issuer_name,
            "did": app_config["DID"],
            "config_root": config_root,
        }
        issuer_config.update(issuer_info)
        issuer_spec = config.assemble_issuer_spec(issuer_config)

        credential_types = []
        for credential_type in issuer_info["credential_types"]:
            schema_name = credential_type["schema"]
            schema_info = app_config["schemas"]["SCHEMA_" + schema_name]
            ctype_config = {
                "schema_name": schema_name,
                "schema_version": schema_info["version"],
                "issuer_url": issuer_config["url"],
                "config_root": config_root,
                "credential_def_id": app_config["schemas"][
                    "CRED_DEF_" + schema_name + "_" + schema_info["version"]
                ],
            }
            credential_type['attributes'] = schema_info["attributes"]
            ctype_config.update(credential_type)
            ctype = config.assemble_credential_type_spec(ctype_config, schema_info.get("attributes"))
            if ctype is not None:
                credential_types.append(ctype)

        issuer_request = {
            "connection_id": app_config["TOB_CONNECTION"],
            "issuer_registration": {
                "credential_types": credential_types,
                "issuer": issuer_spec,
            },
        }

        response = requests.post(
            agent_admin_url + "/issuer_registration/send",
            json.dumps(issuer_request),
            headers=ADMIN_REQUEST_HEADERS,
        )
        response.raise_for_status()
        response.json()
        print("Registered issuer: ", issuer_name)

    synced[connection_id] = True
    print("Connection {} is synchronized".format(connection_id))


class StartupProcessingThread(threading.Thread):
    global app_config

    def __init__(self, ENV):
        threading.Thread.__init__(self)
        self.ENV = ENV

    def run(self):
        # read configuration files
        config_root = self.ENV.get("CONFIG_ROOT", "../config")
        config_schemas = config.load_config(config_root + "/schemas.yml", env=self.ENV)
        config_services = config.load_config(
            config_root + "/services.yml", env=self.ENV
        )
        app_config["config_root"] = config_root
        app_config["config_services"] = config_services

        agent_admin_url = self.ENV.get("AGENT_ADMIN_URL")
        if not agent_admin_url:
            raise RuntimeError(
                "Error AGENT_ADMIN_URL is not specified, can't connect to Agent."
            )
        app_config["AGENT_ADMIN_URL"] = agent_admin_url

        # get public DID from our agent
        response = requests.get(
            agent_admin_url + "/wallet/did/public",
            headers=ADMIN_REQUEST_HEADERS,
        )
        result = response.json()
        did = result["result"]
        logging.LOGGER.info("Fetched DID from agent: %s", did)
        app_config["DID"] = did["did"]

        # determine pre-registered schemas and cred defs
        existing_schemas = agent_schemas_cred_defs(agent_admin_url)

        # register schemas and credential definitions
        for schema in config_schemas:
            schema_name = schema["name"]
            schema_version = schema["version"]
            schema_key = schema_name + "::" + schema_version
            if schema_key not in existing_schemas:
                schema_attrs = []
                schema_descs = {}
                if isinstance(schema["attributes"], dict):
                    # each element is a dict
                    for attr, desc in schema["attributes"].items():
                        schema_attrs.append(attr)
                        schema_descs[attr] = desc
                else:
                    # assume it's an array
                    for attr in schema["attributes"]:
                        schema_attrs.append(attr)

                # register our schema(s) and credential definition(s)
                schema_request = {
                    "schema_name": schema_name,
                    "schema_version": schema_version,
                    "attributes": schema_attrs,
                }
                response = agent_post_with_retry(
                    agent_admin_url + "/schemas",
                    json.dumps(schema_request),
                    headers=ADMIN_REQUEST_HEADERS,
                )
                response.raise_for_status()
                schema_id = response.json()
            else:
                schema_id = {"schema_id": existing_schemas[schema_key]["schema"]["id"]}
            app_config["schemas"]["SCHEMA_" + schema_name] = schema
            app_config["schemas"][
                "SCHEMA_" + schema_name + "_" + schema_version
            ] = schema_id["schema_id"]
            logging.LOGGER.info("Registered schema: %s", schema_id)

            if (
                schema_key not in existing_schemas
                or "cred_def" not in existing_schemas[schema_key]
            ):
                cred_def_request = {"schema_id": schema_id["schema_id"]}
                response = agent_post_with_retry(
                    agent_admin_url + "/credential-definitions",
                    json.dumps(cred_def_request),
                    headers=ADMIN_REQUEST_HEADERS,
                )
                response.raise_for_status()
                credential_definition_id = response.json()
            else:
                credential_definition_id = {
                    "credential_definition_id": existing_schemas[schema_key][
                        "cred_def"
                    ]["id"]
                }
            app_config["schemas"][
                "CRED_DEF_" + schema_name + "_" + schema_version
            ] = credential_definition_id["credential_definition_id"]
            logging.LOGGER.info("Registered credential definition: %s", credential_definition_id)

        # what is the TOB connection name?
        tob_connection_params = config_services["verifiers"]["bctob"]

        # check if we have a TOB connection
        response = requests.get(
            agent_admin_url + "/connections?alias=" + tob_connection_params["alias"],
            headers=ADMIN_REQUEST_HEADERS,
        )
        response.raise_for_status()
        connections = response.json()["results"]
        tob_connection = None
        for connection in connections:
            # check for TOB connection
            if connection["alias"] == tob_connection_params["alias"]:
                tob_connection = connection

        if not tob_connection:
            # if no tob connection then establish one (if we can)
            # (agent_admin_url is provided if we can directly ask the TOB agent for an invitation,
            #   ... otherwise the invitation has to be provided manually through the admin api
            #   ... WITH THE CORRECT ALIAS)
            if ("agent_admin_url" in tob_connection_params["connection"]
                and tob_connection_params["connection"]["agent_admin_url"]
            ):
                tob_agent_admin_url = tob_connection_params["connection"]["agent_admin_url"]
                response = requests.post(
                    tob_agent_admin_url + "/connections/create-invitation",
                    headers=TOB_REQUEST_HEADERS,
                )
                response.raise_for_status()
                invitation = response.json()

                response = requests.post(
                    agent_admin_url
                    + "/connections/receive-invitation?alias="
                    + tob_connection_params["alias"],
                    json.dumps(invitation["invitation"]),
                    headers=ADMIN_REQUEST_HEADERS,
                )
                response.raise_for_status()
                tob_connection = response.json()

                logging.LOGGER.info("Established tob connection: %s", json.dumps(tob_connection))
                time.sleep(5)

        # if we have a connection to the TOB agent, we can register our issuer
        if tob_connection:
            register_issuer_with_orgbook(tob_connection["connection_id"])
        else:
            print("No TOB connection found or established, awaiting invitation to connect to TOB ...")


def tob_connection_synced():
    return (
        ("TOB_CONNECTION" in app_config)
        and (app_config["TOB_CONNECTION"] in synced)
        and (synced[app_config["TOB_CONNECTION"]])
    )


def tob_connection_active():
    """
    Return True if there are pending credential requests, False otherwise.
    Note this will return False if the TOB connection is not yet sync'ed.
    """
    if not tob_connection_synced():
        return False
    return (0 < len(list(credential_requests.keys())))


def issuer_liveness_check():
    """
    Check if we can shut down the container - if we have received a shutdown request and there are
    no outstanding credential requests.
    """
    global app_config

    if app_config["running"]:
        # return True until we get a shutdown request
        return True

    # return True until the work queue is cleared
    return tob_connection_active()


class ShutdownProcessingThread(threading.Thread):
    def run(self):
        while issuer_liveness_check():
            logging.LOGGER.error("... Waiting for work queue to clear before shutdown ...")
            time.sleep(1)


def signal_issuer_shutdown(signum, frame):
    """
    Tell the issuer to do a clean shutdown (finish work queue first).
    """
    global app_config

    logging.LOGGER.error(">>> Received shutdown signal!")
    app_config["running"] = False
    thread = ShutdownProcessingThread()
    thread.start()
    thread.join()
    logging.LOGGER.error(">>> Shutting down issuer controller process.")


def startup_init(ENV):
    global app_config

    thread = StartupProcessingThread(ENV)
    thread.start()
    return thread


TOPIC_CONNECTIONS = "connections"
TOPIC_CONNECTIONS_ACTIVITY = "connections_actvity"
TOPIC_CREDENTIALS = "issue_credential"
TOPIC_PRESENTATIONS = "presentations"
TOPIC_GET_ACTIVE_MENU = "get-active-menu"
TOPIC_PERFORM_MENU_ACTION = "perform-menu-action"
TOPIC_ISSUER_REGISTRATION = "issuer_registration"
TOPIC_PROBLEM_REPORT = "problem_report"


def handle_connections(state, message):
    # if TOB connection becomes "active" then register our issuer
    # what is the TOB connection name?
    config_services = app_config["config_services"]
    tob_connection_params = config_services["verifiers"]["bctob"]
    # check this is the TOB connection
    if "alias" in message and message["alias"] == tob_connection_params["alias"]:
        if state == "active":
            register_issuer_with_orgbook(message["connection_id"])

    return jsonify({"message": state})

def handle_credentials(state, message):
    start_time = time.perf_counter()
    method = "Handle callback:" + state
    logging.log_timing_event(method, message, start_time, None, False)

    if "thread_id" in message:
        set_credential_thread_id(
            message["credential_exchange_id"], message["thread_id"]
        )
    else:
        pass
    if state == "credential_acked":
        # raise 10% errors
        do_error = random.randint(1, 100)
        if do_error <= ACK_ERROR_PCT:
            raise Exception("Fake exception to test error handling: " + message["thread_id"])
        response = {"success": True, "result": message["credential_exchange_id"]}
        add_credential_response(message["credential_exchange_id"], response)

    end_time = time.perf_counter()
    processing_time = end_time - start_time
    logging.log_timing_event(method, message, start_time, end_time, True, outcome=str(state))

    return jsonify({"message": state})


def handle_presentations(state, message):
    # TODO auto-respond to proof requests
    return jsonify({"message": state})


def handle_get_active_menu(message):
    # TODO add/update issuer info?
    return jsonify({})


def handle_perform_menu_action(message):
    # TODO add/update issuer info?
    return jsonify({})


def handle_register_issuer(message):
    # TODO add/update issuer info?
    return jsonify({})


def handle_problem_report(message):
    logging.LOGGER.error("handle_problem_report() %s", json.dumps(message))

    msg = message["~thread"]["thid"] + "::" + message["explain-ltxt"]
    response = {"success": False, "result": msg}
    add_credential_problem_report(message["~thread"]["thid"], response)

    return jsonify({})


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
        thread.start()
        thread.join()
        cred_responses.append(thread.cred_response)
        processed_count = processed_count + 1

    processing_time = time.perf_counter() - start_time
    print(">>> Processed", processed_count, "credentials in", processing_time)
    print("   ", processing_time / processed_count, "seconds per credential")

    return jsonify(cred_responses)
