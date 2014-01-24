"""
Module for decorators
"""

from flask import request
from flask.json import dumps

import json

from shmir_api.utils import json_error


def require_json(require_data=True, required_data_words=None,
                 required_data_characters=None, jsonify=True):
    """
    Accepts only json requests and sends parsed data to the handlers

    :param require_data: checking whether json request has 'data' attribute
    """
    def wrapper(f):

        def wrapped(*args, **kwargs):
            data = request.data.decode('utf-8')
            try:
                request_json = json.loads(data)
            except (ValueError, KeyError, TypeError):
                return json_error('Use JSON to comunicate with our API')

            if not require_data:
                return f(request_json=request_json, *args, **kwargs)
            elif 'data' in request_json.keys():
                data = str(request_json['data']).strip()

                if required_data_words and len(data.split()) != \
                        required_data_words:
                    return json_error("Data must have %d word(s)!" %
                                      required_data_words)

                if required_data_characters and len(data) != \
                        required_data_characters:
                    return json_error("Data must have %d characters!" %
                                      required_data_characters)

                if jsonify:
                    return dumps(
                        f(data=data, request_json=request_json, *args,
                          **kwargs)
                    )
                return f(data=data, request_json=request_json, *args, **kwargs)

            return json_error('Data not provided')

        return wrapped
    return wrapper


def jsonify(f):
    """
    Returns JSON
    """
    def wrapped(*args, **kwargs):
        return dumps(f(*args, **kwargs))
    return wrapped
