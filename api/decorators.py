from flask import jsonify
from flask import request

import json


def require_json(require_data=True):
    """
    Accepts only json requests and sends parsed data to handlers

    :param require_data: checking whether request json has 'data' attribute

    """

    def decorator(f):

        def decorated(*args, **kwargs):
            try:
                request_json = json.loads(request.data)
            except (ValueError, KeyError, TypeError):
                return jsonify(error='Use JSON to comunicate with our API')

            if not require_data or 'data' in request_json.keys():
                return f(request_json=request_json, *args, **kwargs)

            return jsonify(error='Data not provided')

        return decorated
    return decorator
