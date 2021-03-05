
import os, threading, time, json, logging, requests
from datetime import datetime

TRACE_EVENTS = os.getenv("TRACE_EVENTS", "True").lower() == "true"
TRACE_LABEL = os.getenv("TRACE_LABEL", "bcreg.controller")
TRACE_TAG = os.getenv("TRACE_TAG", "acapy.events")
TRACE_LOG_TARGET = "log"
TRACE_TARGET = os.getenv("TRACE_TARGET", TRACE_LOG_TARGET)
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING').upper()


# need to specify an env variable RECORD_TIMINGS=True to get method timings
RECORD_TIMINGS = os.getenv('RECORD_TIMINGS', 'False').lower() == 'true'

timings = {}
timing_lock = threading.Lock()

LOGGER = logging.getLogger(__name__)
if TRACE_EVENTS and TRACE_TARGET == TRACE_LOG_TARGET:
    LOGGER.setLevel(logging.INFO)
elif LOG_LEVEL and 0 < len(LOG_LEVEL):
    LOGGER.setLevel(LOG_LEVEL)
DT_FMT = '%Y-%m-%d %H:%M:%S.%f%z'


def clear_stats():
    global timings
    timing_lock.acquire()
    try:
        timings = {}
    finally:
        timing_lock.release()

def get_stats():
    timing_lock.acquire()
    try:
        return timings
    finally:
        timing_lock.release()

def log_timing_method(method, start_time, end_time, success, data=None):
    if not RECORD_TIMINGS:
        return

    timing_lock.acquire()
    try:
        elapsed_time = end_time - start_time
        if not method in timings:
            timings[method] = {
                "total_count": 1,
                "success_count": 1 if success else 0,
                "fail_count": 0 if success else 1,
                "min_time": elapsed_time,
                "max_time": elapsed_time,
                "total_time": elapsed_time,
                "avg_time": elapsed_time,
                "data": {},
            }
        else:
            timings[method]["total_count"] = timings[method]["total_count"] + 1
            if success:
                timings[method]["success_count"] = timings[method]["success_count"] + 1
            else:
                timings[method]["fail_count"] = timings[method]["fail_count"] + 1
            if elapsed_time > timings[method]["max_time"]:
                timings[method]["max_time"] = elapsed_time
            if elapsed_time < timings[method]["min_time"]:
                timings[method]["min_time"] = elapsed_time
            timings[method]["total_time"] = timings[method]["total_time"] + elapsed_time
            timings[method]["avg_time"] = (
                timings[method]["total_time"] / timings[method]["total_count"]
            )
        if data:
            timings[method]["data"][str(timings[method]["total_count"])] = data
    finally:
        timing_lock.release()


def log_timing_event(method, message, start_time, end_time, success, outcome=None):
    """Record a timing event in the system log or http endpoint."""

    if (not TRACE_EVENTS) and (not message.get("trace")):
        return
    if not TRACE_TARGET:
        return

    msg_id = "N/A"
    thread_id = message["thread_id"] if message.get("thread_id") else "N/A"
    handler = TRACE_LABEL
    ep_time = time.time()
    str_time = datetime.utcfromtimestamp(ep_time).strftime(DT_FMT)
    if end_time:
        str_outcome = method + ".SUCCESS" if success else ".FAIL"
    else:
        str_outcome = method + ".START"
    if outcome:
        str_outcome = str_outcome + "." + outcome
    event = {
        "msg_id": msg_id,
        "thread_id": thread_id if thread_id else msg_id,
        "traced_type": method,
        "timestamp": ep_time,
        "str_time": str_time,
        "handler": str(handler),
        "ellapsed_milli": int(1000 * (end_time - start_time)) if end_time else 0,
        "outcome": str_outcome,
    }
    event_str = json.dumps(event)

    try:
        if TRACE_TARGET == TRACE_LOG_TARGET:
            # write to standard log file
            LOGGER.error(" %s %s", TRACE_TAG, event_str)
        else:
            # should be an http endpoint
            _ = requests.post(
                TRACE_TARGET + TRACE_TAG,
                data=event_str,
                headers={"Content-Type": "application/json"}
            )
    except Exception as e:
        LOGGER.error(
            "Error logging trace target: %s tag: %s event: %s",
            TRACE_TARGET,
            TRACE_TAG,
            event_str
        )
        LOGGER.exception(e)
