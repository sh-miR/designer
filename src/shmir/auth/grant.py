import datetime

import redis

from shmir import (
    oauth,
    settings
)


conn = redis.Redis(settings.CACHE_REDIS_HOST)


class Grant(object):

    def __init__(self, code):
        self.code = code

    def delete(self):
        conn.delete(self.code)


@oauth.grantgetter
def load_grant(client_id, code):
    grant = conn.hgetall(code)

    if grant.get('client_id') == client_id:
        return Grant(code)


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    _code = code['code']
    expires = datetime.datetime.utcnow() + datetime.timedelta(days=7)

    conn.hset(_code, 'client_id', client_id)
    conn.hset(_code, 'redirect_uri', request.redirect_uri)
    conn.hset(_code, 'scopes', ' '.join(request.scopes))
    conn.hset(_code, 'expires', expires)
