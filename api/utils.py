from flask import jsonify

def json_error(error):
    return jsonify(error=error)
