from ConfigParser import (
    ConfigParser,
    Error
)


# Parsing config file

config = ConfigParser()
config.read('/etc/shmir.conf')

# Config getters


def get_config(section, option):
    try:
        return config.get(section, option)
    except Error:
        return None


get_db_config = lambda option: get_config('database', option)
# RabbitMQ will be default broker and result backend if they're not defined
# get_celery_config = lambda option: get_config('celery', option) or 'amqp://'

# SQLAlchemy engine

CONN_STR = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
FCONN = CONN_STR.format(
    dbname=get_db_config('name'), user=get_db_config('user'),
    password=get_db_config('password'), host=get_db_config('host'),
    port=get_db_config('port')
)

# Celery
# CELERY_BROKER = get_celery_config('broker')
# CELERY_RESULT_BACKEND = get_celery_config('result_backend')
CELERY_BROKER = 'amqp://'
CELERY_RESULT_BACKEND = 'redis://'

# Mfold
MFOLD_PATH = '/home/shmir/shmir/mfold/mfold'  # script path
MFOLD_FILES = '/tmp/mfold_files'  # Path where mfold fiels are generated


# nucleotide type for ncbi database
NUCLEOTIDE_DB = 'nucleotide'
EMAIL = 'amupoznan@gmail.com'
