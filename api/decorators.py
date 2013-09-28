from flask import jsonify
from flask import request

import json


def require_json(require_data=True, required_data_words=None,
                 required_data_characters=None):
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

            if not require_data:
                return f(request_json=request_json, *args, **kwargs)
            elif 'data' in request_json.keys():
                data = str(request_json['data'])

                if required_data_words:
                    if len(data.split()) != required_data_words:
                        return jsonify(error="Data must have %d words!" %
                                       required_data_words)

                if required_data_characters:
                    if len(data) != required_data_characters:
                        return jsonify(error="Data must have %d characters!" %
                                       required_data_characters)

                return f(data=data, request_json=request_json, *args, **kwargs)

            return jsonify(error='Data not provided')

        return decorated
    return decorator
