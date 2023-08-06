#-*- coding: utf-8 -*-

import json
import logging

from datetime import datetime
from six.moves import http_client

from .signature import Signature


def new_logger(name, verbose=False):
    logging.basicConfig()
    if verbose:
        http_client.HTTPConnection.debuglevel = 0
        requests_log = logging.getLogger("urllib3")
        requests_log.setLevel(logging.INFO)
        requests_log.propagate = False
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        return logger
    else:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        return logger


def human_byte(size, dot=2):
    size = float(size)
    if size < pow(1024, 2):
        size = str(round(size / pow(1024, 1), dot)) + 'KB'
    elif pow(1024, 2) <= size < pow(1024, 3):
        size = str(round(size / pow(1024, 2), dot)) + 'MB'
    else:
        size = str(round(size / pow(1024, 3), dot)) + 'GB'
    return size


def make_sign(app_key, app_secret, **kwargs):
    now = datetime.now()
    timestamp = datetime.strftime(now, "%Y-%m-%dT%H:%M:%SZ")
    data = {}
    data.update(kwargs)
    signature = Signature(app_secret)
    signature_nonce = signature.get_sign_nonce()
    data.update({
        'app_key': app_key,
        'signature_nonce': signature_nonce,
        'timestamp': timestamp
    })
    sign = signature.sign(data)
    data['sign'] = sign
    return data
