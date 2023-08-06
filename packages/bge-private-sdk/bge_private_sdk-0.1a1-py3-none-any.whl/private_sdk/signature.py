#-*- coding: utf-8 -*-

from base64 import b64encode
from datetime import datetime, timezone, timedelta
from uuid import uuid4
try:
    from urllib import quote, quote_plus
except ImportError:
    from urllib.parse import quote, quote_plus

import string
import hmac


class Signature(object):

    salt = string.ascii_letters

    def __init__(self, client_secret, expiration_time=300):
        self.client_secret = client_secret
        self.expiration_time = expiration_time

    def get_timestamp(self):
        return datetime.now(tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    def is_expired(self, timestamp):
        now = datetime.now(tz=timezone.utc)
        timestamp = datetime.strptime(
            timestamp, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        return now > (timestamp + timedelta(seconds=self.expiration_time))

    def get_sign_nonce(self):
        return uuid4().hex

    def _get_stringtosign(self, params):
        t = []
        items = list(params.items())
        items.sort(key=lambda i: i[0])
        for key, value in items:
            if value is None:
                continue
            key = quote_plus(key)
            value = quote_plus(str(value))
            value = value.replace('%7E', '~').replace('+', '%20')
            t.append('%s=%s' % (key, value))
        qs = '&'.join(t)
        qs = quote_plus(qs).replace('%7E', '~').replace('+', '%20')
        return qs

    def _make_signed_string(self, params):
        text = self._get_stringtosign(params)
        message = '&'.join([self.salt, text])
        key = (self.client_secret + '&').encode('utf-8')
        message = message.encode('utf-8')
        h = hmac.new(key, message, digestmod='sha1')
        return b64encode(h.digest()).decode('utf-8')

    def sign(self, params):
        return self._make_signed_string(params)

    def verify(self, params, signed_string):
        timestamp = params['timestamp']
        if self.is_expired(timestamp):
            return False
        return self._make_signed_string(params) == signed_string
