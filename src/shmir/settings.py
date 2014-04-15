from ConfigParser import ConfigParser


# Parsing config file

config = ConfigParser()
config.read('/etc/shmir.conf')

get_db_config = lambda option: config.get('database', option)

# SQLAlchemy engine

CONN_STR = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
FCONN = CONN_STR.format(
    dbname=get_db_config('name'), user=get_db_config('user'),
    password=get_db_config('password'), host=get_db_config('host'),
    port=get_db_config('port')
)


# Mfold
MFOLD_PATH = '/home/shmir/shmir/mfold/mfold'  # script path
MFOLD_FILES = '/tmp/mfold_files'  # Path where mfold fiels are generated


# nucleotide type for ncbi database
NUCLEOTIDE_DB = 'nucleotide'
