"""
.. module:: shmir.data.db_api
    :synopsis: Module for functions to work with database
"""
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func
from shmir.data.models import (
    InputData,
    Result,
    Backbone,
    db_session,
)


def get_results(
    transcript_name, minimum_CG, maximum_CG, maximum_offtarget,
    scaffold, immunostimulatory
):
    try:
        stored_input = db_session.query(InputData).filter(
            func.lower(InputData.transcript_name) == transcript_name.lower(),
            InputData.minimum_CG == minimum_CG,
            InputData.maximum_CG == maximum_CG,
            InputData.maximum_offtarget == maximum_offtarget,
            func.lower(InputData.scaffold) == scaffold.lower(),
            func.lower(InputData.immunostimulatory) == immunostimulatory.lower()
        ).outerjoin(InputData.results).one()
    except NoResultFound:
        return None
    return [result.as_json() for result in stored_input.results]


def frames_by_scaffold(scaffold):
    if scaffold == 'all':
        return db_session.query(Backbone).all()
    else:
        return db_session.query(Backbone).filter(
            func.lower(Backbone.name) == scaffold.lower()
        ).all()
