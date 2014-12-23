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

    return db_session.query(Backbone).filter(
        func.lower(Backbone.name) == scaffold.lower()
    ).all()


def store_results(
    transcript_name, minimum_CG, maximum_CG, maximum_offtarget, scaffold, immuno,
    results
):
    db_results = [Result(
        score=result_dict['score'],
        sh_mir=result_dict['frame'].template(),
        pdf=result_dict['folding']['path_id'],
        backbone=result_dict['frame'].id,
        sequence=result_dict['found_sequence'],
    ) for result_dict in results]

    db_input = InputData(
        transcript_name=transcript_name,
        minimum_CG=minimum_CG,
        maximum_CG=maximum_CG,
        maximum_offtarget=maximum_offtarget,
        scaffold=scaffold,
        immunostimulatory=immuno,
        results=db_results
    )

    db_session.add(db_input)
    db_session.add_all(db_results)
    db_session.commit()

    return db_results
