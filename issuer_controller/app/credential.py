import threading, time, os, json, requests

from app import logging

USE_LOCK = os.getenv('USE_LOCK', 'True').lower() == 'true'
# max 15 second wait for a credential response (prevents blocking forever)
MAX_CRED_RESPONSE_TIMEOUT = int(os.getenv('MAX_CRED_RESPONSE_TIMEOUT', '120'))


credential_lock = threading.Lock()
credential_requests = {}
credential_responses = {}
credential_threads = {}


def set_credential_thread_id(cred_exch_id, thread_id):
    start_time = time.perf_counter()
    if USE_LOCK:
        credential_lock.acquire()
    try:
        # add 2 records so we can x-ref
        credential_threads[thread_id] = cred_exch_id
        credential_threads[cred_exch_id] = thread_id
    finally:
        if USE_LOCK:
            credential_lock.release()
    processing_time = time.perf_counter() - start_time
    if processing_time > 0.001:
        logging.LOGGER.warn(">>> lock time = %s", str(processing_time))


def add_credential_request(cred_exch_id):
    start_time = time.perf_counter()
    if USE_LOCK:
        credential_lock.acquire()
    try:
        # short circuit if we already have the response
        if cred_exch_id in credential_responses:
            return None

        result_available = threading.Event()
        credential_requests[cred_exch_id] = result_available
        return result_available
    finally:
        if USE_LOCK:
            credential_lock.release()
    processing_time = time.perf_counter() - start_time
    if processing_time > 0.001:
        logging.LOGGER.warn(">>> lock time = %s", str(processing_time))


def add_credential_response(cred_exch_id, response):
    start_time = time.perf_counter()
    if USE_LOCK:
        credential_lock.acquire()
    try:
        credential_responses[cred_exch_id] = response
        if cred_exch_id in credential_requests:
            result_available = credential_requests[cred_exch_id]
            result_available.set()
            del credential_requests[cred_exch_id]
    finally:
        if USE_LOCK:
            credential_lock.release()
    processing_time = time.perf_counter() - start_time
    if processing_time > 0.001:
        logging.LOGGER.warn(">>> lock time = %s", str(processing_time))


def add_credential_problem_report(thread_id, response):
    logging.LOGGER.error("get problem report for thread %s %s", thread_id, str(len(credential_requests)))
    if thread_id in credential_threads:
        cred_exch_id = credential_threads[thread_id]
        logging.LOGGER.error(" ... cred_exch_id is %s: %s", cred_exch_id, str(response))
        add_credential_response(cred_exch_id, response)
    else:
        logging.LOGGER.error("thread_id not found %s", thread_id)
        # hack for now
        if 1 == len(list(credential_requests.keys())):
            cred_exch_id = list(credential_requests.keys())[0]
            add_credential_response(cred_exch_id, response)
        elif 0 == len(list(credential_requests.keys())):
            logging.LOGGER.error("NO outstanding requests, can't map problem report to request :-(")
            logging.LOGGER.error(credential_requests)
        else:
            logging.LOGGER.error("Too many outstanding requests, can't map problem report to request :-(")
            logging.LOGGER.error(credential_requests)


def add_credential_timeout_report(cred_exch_id, thread_id):
    logging.LOGGER.error("add timeout report for cred %s %s", thread_id, cred_exch_id)
    response = {"success": False, "result": thread_id + "::Error thread timeout"}
    add_credential_response(cred_exch_id, response)


def add_credential_exception_report(cred_exch_id, exc):
    logging.LOGGER.error("add exception report for cred %s", cred_exch_id)
    response = {"success": False, "result": cred_exch_id + "::" + str(exc)}
    add_credential_response(cred_exch_id, response)


def get_credential_response(cred_exch_id):
    start_time = time.perf_counter()
    if USE_LOCK:
        credential_lock.acquire()
    try:
        if cred_exch_id in credential_responses:
            thread_id = None
            response = credential_responses[cred_exch_id]
            del credential_responses[cred_exch_id]
            if cred_exch_id in credential_threads:
                thread_id = credential_threads[cred_exch_id]
                del credential_threads[cred_exch_id]
                del credential_threads[thread_id]
                # override returned id with thread_id, if we have it (unless we have received a problem report)
                if not "::" in response["result"]:
                    response["result"] = thread_id
            return response
        else:
            return None
    finally:
        if USE_LOCK:
            credential_lock.release()
    processing_time = time.perf_counter() - start_time
    if processing_time > 0.001:
        logging.LOGGER.warn(">>> lock time = %s", str(processing_time))



class SendCredentialThread(threading.Thread):
    def __init__(self, credential_definition_id, cred_offer, url, headers):
        threading.Thread.__init__(self)
        self.credential_definition_id = credential_definition_id
        self.cred_offer = cred_offer
        self.url = url
        self.headers = headers

    def run(self):
        start_time = time.perf_counter()
        method = "submit_credential.credential"

        logging.log_timing_event("issue_credential", {}, start_time, None, False)
        logging.LOGGER.info("Sending credential offer: %s", json.dumps(self.cred_offer))

        cred_data = None
        try:
            response = requests.post(
                self.url, json.dumps(self.cred_offer), headers=self.headers
            )
            response.raise_for_status()
            cred_data = response.json()
            if "credential_exchange_id" in cred_data:
                result_available = add_credential_request(
                    cred_data["credential_exchange_id"]
                )
            else:
                raise Exception(json.dumps(cred_data))

            # wait for confirmation from the agent, which will include the credential exchange id
            if result_available and not result_available.wait(
                MAX_CRED_RESPONSE_TIMEOUT
            ):
                add_credential_timeout_report(cred_data["credential_exchange_id"], cred_data["thread_id"])
                logging.LOGGER.error(
                    "Got credential TIMEOUT: %s %s %s",
                    cred_data["thread_id"],
                    cred_data["credential_exchange_id"],
                    cred_data["connection_id"],
                )
                end_time = time.perf_counter()
                logging.log_timing_method(method, start_time, end_time, False, 
                    data={
                        'thread_id':cred_data["thread_id"], 
                        'credential_exchange_id':cred_data["credential_exchange_id"], 
                        'Error': 'Timeout',
                        'elapsed_time': (end_time-start_time)
                    }
                )
                success = False
                outcome = "timeout"
            else:
                # response was received for this cred exchange via a web hook
                end_time = time.perf_counter()
                logging.log_timing_method(method, start_time, end_time, True)
                success = True
                outcome = "success"

            # there should be some form of response available
            self.cred_response = get_credential_response(
                cred_data["credential_exchange_id"]
            )

        except Exception as exc:
            logging.LOGGER.error("got credential exception: %s", str(exc))
            # if cred_data is not set we don't have a credential to set status for
            end_time = time.perf_counter()
            success = False
            outcome = str(exc)
            if cred_data:
                add_credential_exception_report(
                    cred_data["credential_exchange_id"], exc
                )
                data = {
                    "thread_id": cred_data["thread_id"],
                    "credential_exchange_id": cred_data["credential_exchange_id"],
                    "Error": str(exc),
                    "elapsed_time": (end_time - start_time),
                }
            else:
                data = {
                "Error": str(exc),
                "elapsed_time": (end_time - start_time)
            }
            logging.log_timing_method(method, start_time, end_time, False,
                data=data
            )

            # don't re-raise; we want to log the exception as the credential error response
            self.cred_response = {"success": False, "result": str(exc)}

        processing_time = end_time - start_time
        message = {"thread_id": self.cred_response["result"]}
        logging.log_timing_event("issue_credential", message, start_time, end_time, success, outcome=outcome)

