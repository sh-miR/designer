import re
import json
import os

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Unicode,
    event,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    relationship,
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)

from shmir.settings import (
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
    regexp = Column(Unicode(1000))

    def template(self, siRNAstrand_1, siRNAstrand_2):
        """Returns the template of DNA (sh-miR)"""
        return (self.flanks5_s + siRNAstrand_1 + self.loop_s +
                siRNAstrand_2 + self.flanks3_s).upper()

    def generate_regexp(self):
        """Function creates regexps based on active_strand
        and saves it to the database.

        active_strand: if is equal to 3, function use miRNA_a;
                       if is equal to 1 or 5, function use miRNA_s
                       if is equal to 0, function use both
        """
        if not self.regexp:

            seq_list = []
            if self.active_strand in (0, 3):
                seq_list.append(self.miRNA_a)

            if self.active_strand in (0, 1, 5):
                seq_list.append(self.miRNA_s)

            self.regexp = create_regexp(seq_list)

    @classmethod
    def generate_regexp_all(cls):
        for row in db_session.query(cls).all():
            row.generate_regexp()

        db_session.commit()


class Immuno(Base):
    """
    Immuno motives class
    """
    __tablename__ = 'immuno'
    id = Column(Integer, primary_key=True)
    sequence = Column(Unicode(10), nullable=False)
    receptor = Column(Unicode(15))
    link = Column(Unicode(100), nullable=False)

    @classmethod
    def check_is_in_sequence(cls, input_sequence):
        return bool(db_session.execute(
            "SELECT COUNT(*) FROM immuno WHERE :input_sequence LIKE "
            "'%'||sequence||'%';", {'input_sequence': input_sequence}
        ).first()[0])


class InputData(Base):
    """
    Table storing input data to sh-miR algorithm
    """
    __tablename__ = 'input_data'

    id = Column(Integer, primary_key=True)
    transcript_name = Column(Unicode(20), nullable=False)
    minimum_CG = Column(Integer, nullable=False)
    maximum_CG = Column(Integer, nullable=False)
    maximum_offtarget = Column(Integer, nullable=False)
    scaffold = Column(Unicode(10), default=u'all')
    stimulatory_sequences = Column(Unicode(15), default=u'no_difference')
    results = relationship('Result', backref='input_data')


class Result(Base):
    """
    sh-miR results
    """
    __tablename__ = 'result'

    id = Column(Integer, primary_key=True)
    sh_mir = Column(Unicode(300), nullable=False)
    score = Column(Integer, nullable=False)
    pdf = Column(Unicode(150), nullable=False)
    sequence = Column(Unicode(30), nullable=False)
    backbone = Column(Integer, ForeignKey(Backbone.id))
    input_id = Column(Integer, ForeignKey('input_data.id'))

    def as_json(self):
        return {
            'sh_mir': str(self.sh_mir),
            'score': self.score,
            'pdf': str(self.pdf),
            'sequence': str(self.sequence),
            'backbone': str(
                db_session.query(Backbone.name).filter(
                    Backbone.id == self.backbone
                ).one()[0]
            ),
        }

    def get_task_id(self):
        return os.path.basename(os.path.dirname(self.pdf))


# Creating tables which does not exist
Base.metadata.create_all(engine)


@event.listens_for(Backbone, 'before_insert')
def generate_regexp_on_insert(mapper, connection, target):
    target.generate_regexp()


def create_regexp(seq_list):
    """Function for generating regular expresions for given miRNA sequence
    according to the schema below:

    example miRNA sequence: UGUAAACAUCCUCGACUGGAAG
    U... (weight 1): the first nucleotide
    U...G (weight 2): the first and the last nucleotides
    UG... (weight 2): two first nucleotides
    UG...G (weight 3): two first and the last nucleotides
    UG...AG (weight 4): two first and two last nucleotides
    """

    acids = '[UTGCA]'  # order is important: U should always be next to T
    generic = r'{1}{2}[UTGCA]{{{0}}}{3}{4}'

    ret = {i: [] for i in xrange(1, 5)}
    for seq_ in seq_list[:]:
        seq = seq_.upper()
        begin = [
            {
                'acid': re.sub('[UT]', '[UT]', letter),
                'excluded': acids.replace('UT' if letter in 'UT' else letter, '')
            }
            for letter in seq[:2]]

        end = [
            {
                'acid': re.sub('[UT]', '[UT]', letter),
                'excluded': acids.replace('UT' if letter in 'UT' else letter, '')
            }
            for letter in seq[-2:]]

        ret[1].extend([generic.format(i, begin[0]['acid'], begin[1]['excluded'],
                                      end[0]['excluded'], end[1]['excluded'])
                       for i in range(15, 18)])

        ret[2].extend([generic.format(i, begin[0]['acid'], begin[1]['excluded'],
                                      end[0]['excluded'], end[1]['acid'])
                       for i in range(15, 18)])

        ret[2].extend([generic.format(i, begin[0]['acid'], begin[1]['acid'],
                                      end[0]['excluded'], end[1]['excluded'])
                       for i in range(15, 18)])

        ret[3].extend([generic.format(i, begin[0]['acid'], begin[1]['acid'],
                                      end[0]['excluded'], end[1]['acid'])
                       for i in range(15, 18)])

        ret[4].extend([generic.format(i, begin[0]['acid'], begin[1]['acid'],
                                      end[0]['acid'], end[1]['acid'])
                       for i in range(15, 18)])

    return json.dumps(ret)
