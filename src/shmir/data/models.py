from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Unicode
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)

from settings import (
    FCONN
)


engine = create_engine(FCONN)

db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine
))
Base = declarative_base()


class Backbone(Base):
    """
    pri-miRNA class
    """
    __tablename__ = 'backbone'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(10), nullable=False)
    flanks3_s = Column(Unicode(80), nullable=False)
    flanks3_a = Column(Unicode(80), nullable=False)
    flanks5_s = Column(Unicode(80), nullable=False)
    flanks5_a = Column(Unicode(80), nullable=False)
    loop_s = Column(Unicode(30), nullable=False)
    loop_a = Column(Unicode(30), nullable=False)
    miRNA_s = Column(Unicode(30), nullable=False)
    miRNA_a = Column(Unicode(30), nullable=False)
    miRNA_length = Column(Integer, nullable=False)
    miRNA_min = Column(Integer, nullable=False)
    miRNA_max = Column(Integer, nullable=False)
    miRNA_end_5 = Column(Integer, nullable=False)
    miRNA_end_3 = Column(Integer, nullable=False)
    structure = Column(Unicode(200), nullable=False)
    homogeneity = Column(Integer, nullable=False)
    miRBase_link = Column(Unicode(200), nullable=False)
    active_strand = Column(Integer, nullable=False)

    def template(self, siRNAstrand_1, siRNAstrand_2):
        """Returns the template of DNA (sh-miR)"""
        return (self.flanks5_s + siRNAstrand_1 + self.loop_s +
                siRNAstrand_2 + self.flanks3_s).upper()


class Immuno(Base):
    """
    Immuno motives class
    """
    __tablename__ = 'immuno'
    id = Column(Integer, primary_key=True)
    sequence = Column(Unicode(10), nullable=False)
    receptor = Column(Unicode(15))
    link = Column(Unicode(100), nullable=False)
