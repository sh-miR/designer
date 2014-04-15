from ConfigParser import ConfigParser

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Parsing config file

config = ConfigParser()
config.read('/etc/shmir.conf')

get_db_config = lambda option: config.get('database', option)

# SQLAlchemy engine

conn_str = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
fconn = conn_str.format(
    dbname=get_db_config('name'), user=get_db_config('user'),
    password=get_db_config('password'), host=get_db_config('host'),
    port=get_db_config('port')
)

engine = create_engine(fconn)

db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine
))
Base = declarative_base()

# Mfold
MFOLD_PATH = '/home/shmir/shmir/mfold/mfold'  # script path
MFOLD_FILES = '/tmp/mfold_files'  # Path where mfold fiels are generated


# nucleotide type for ncbi database
NUCLEOTIDE_DB = 'nucleotide'
