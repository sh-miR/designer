from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Unicode,
    UnicodeText
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    backref,
    relationship
)

from shmir.data import engine


Base = declarative_base()


class User(Base):
    """
    API user
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(Unicode(40), unique=True)


class Client(Base):
    """
    API Client
    """
    __tablename__ = 'client'

    client_id = Column(Unicode(40), primary_key=True)
    secret = Column(Unicode(55), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref('client'))
    _redirect_uris = Column(UnicodeText)
    _scopes = Column(UnicodeText)

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self.redirect_uris.split()
        return []

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Grant(Base):
    __tablename__ = 'grant'

    id = Column(Integer, primary_key=True)


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True)


Base.metadata.create_all(engine)
