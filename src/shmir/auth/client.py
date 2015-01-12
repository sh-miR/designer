from shmir import oauth
from shmir.auth import models as auth_models
from shmir.data import db_session


@oauth.clientgetter
def load_client(client_id):
    return db_session.query(auth_models.Client).filter_by(
        client_id=client_id).first()
