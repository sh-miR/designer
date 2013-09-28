from flask import jsonify


def json_result(result):
    return jsonify(result=result)


def json_error(error):
    return jsonify(error=error)
