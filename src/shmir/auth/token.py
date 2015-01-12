import datetime

import redis

from shmir import (
    oauth,
    settings
)


conn = redis.Redis(settings.CACHE_REDIS_HOST)


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    token = conn.hgetall()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    client_id = request.client.client_id
    conn.delete(client_id)

    expires_in = token.pop('expires_in')
    expires = datetime.datetime.utcnow() + \
        datetime.timedelta(seconds=expires_in)

    conn.hset(client_id, 'access_token', token['access_token'])
    conn.hset(client_id, 'refresh_token', token['refresh_token'])
    conn.hset(client_id, 'token_type', token['token_type'])
    conn.hset(client_id, 'scopes', token['scope'])
    conn.hset(client_id, 'expires', expires)
