"""
Handlers

"""

from flask import send_file

from shmir_api.decorators import require_json
from mfold.mfold import delegate_mfold


@require_json(jsonify=False)
def get_mfold(data=None, **kwargs):
    filename = delegate_mfold(data)

    return send_file(filename)


get_mfold.methods = ['POST']
