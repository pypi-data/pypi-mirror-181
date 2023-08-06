import requests

TIMEOUT=2

def _log(logger, msg):
    if logger is None: return
    logger.info(msg)

def send_post(url, json_body, logger=None):
    s = requests.Session()
    s.trust_env=False

    _log(logger, "Sending post")
    try:
        r = s.post(url, json=json_body, verify=False, timeout=TIMEOUT)
    except Exception:
        return None

    return r

def send_post_raw(url, body, logger=None, custom_headers = {}):
    s = requests.Session()
    s.trust_env=False

    _log(logger, "Sending post")
    try:
        r = s.post(url, data=body, verify=False, headers=custom_headers, timeout=TIMEOUT)
    except Exception:
        return None

    return r

def send_post_file(url, file, logger=None):
    s = requests.Session()
    s.trust_env=False

    files = {'file': open(file, 'rb')}
    _log(logger, "Sending post file")

    r = s.post(url, files=files)

    return r