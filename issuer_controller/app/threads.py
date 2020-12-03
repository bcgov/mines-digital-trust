import threading

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

        log_timing_event("issue_credential", {}, start_time, None, False)
        LOGGER.info("Sending credential offer: %s", json.dumps(self.cred_offer))

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
                LOGGER.error(
                    "Got credential TIMEOUT: %s %s %s",
                    cred_data["thread_id"],
                    cred_data["credential_exchange_id"],
                    cred_data["connection_id"],
                )
                end_time = time.perf_counter()
                log_timing_method(method, start_time, end_time, False, 
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
                log_timing_method(method, start_time, end_time, True)
                success = True
                outcome = "success"

            # there should be some form of response available
            self.cred_response = get_credential_response(
                cred_data["credential_exchange_id"]
            )

        except Exception as exc:
            LOGGER.error("got credential exception: %s", str(exc))
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
            log_timing_method(method, start_time, end_time, False,
                data=data
            )

            # don't re-raise; we want to log the exception as the credential error response
            self.cred_response = {"success": False, "result": str(exc)}

        processing_time = end_time - start_time
        message = {"thread_id": self.cred_response["result"]}
        log_timing_event("issue_credential", message, start_time, end_time, success, outcome=outcome)

