"""
.. module:: shmir.data
    :synopsis: Module to handle data
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)

from shmir.settings import FCONN

engine = create_engine(FCONN)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine
))
