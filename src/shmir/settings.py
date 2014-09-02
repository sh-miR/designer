from ConfigParser import ConfigParser


# Parsing config file

config = ConfigParser()
# config.read('/etc/shmir.conf')

# get_db_config = lambda option: config.get('database', option)

# SQLAlchemy engine
DB_NAME = 'shmird'
DB_USER = 'ja'
DB_PASS = 'dupa'
DB_HOST = '127.0.0.1'
DB_PORT = '5432'

CONN_STR = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
FCONN = CONN_STR.format(
    dbname=DB_NAME, user=DB_NAME,
    password=DB_PASS, host=DB_HOST,
    port=DB_PORT
)


# Mfold
MFOLD_PATH = '/home/shmir/shmir/mfold/mfold'  # script path
MFOLD_FILES = '/tmp/mfold_files'  # Path where mfold fiels are generated
