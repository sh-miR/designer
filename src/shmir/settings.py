from ConfigParser import (
    ConfigParser,
    Error
)

from kombu import Queue


# Parsing config file

config = ConfigParser()
config.read('/etc/shmir.conf')

# Config getters


def get_config(section, option, default=None):
    try:
        return config.get(section, option)
    except Error:
        return default


#get_db_config = lambda option: get_config('database', option)


def get_db_config(option):
    return config.get('database', option)


# RabbitMQ will be default broker and result backend if they're not defined
# get_celery_config = lambda option: get_config('celery', option) or 'amqp://'

DEBUG = True

# SQLAlchemy engine

CONN_STR = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
try:
    FCONN = CONN_STR.format(
        dbname=get_db_config('name'), user=get_db_config('user'),
        password=get_db_config('password'), host=get_db_config('host'),
        port=get_db_config('port', default='5432')
    )
except Error:
    FCONN = 'sqlite:///:memory:'

# Celery
# CELERY_BROKER = get_celery_config('broker')
# CELERY_RESULT_BACKEND = get_celery_config('result_backend')
CELERY_BROKER = 'amqp://'
CELERY_RESULT_BACKEND = 'redis://'
CELERYD_FORCE_EXECV = True
CELERY_QUEUES = (
    Queue('celery', routing_key='celery'),
    Queue('subtasks', routing_key='transient',
          delivery_mode=1),
)


# Mfold
MFOLD_PATH = '/home/shmir/shmir/mfold/mfold'  # script path
MFOLD_FILES = '/tmp/mfold_files'  # Path where mfold fiels are generated


# nucleotide type for ncbi database
NUCLEOTIDE_DB = 'nucleotide'
EMAIL = 'amupoznan@gmail.com'

# Cache
CACHE_TYPE = 'redis'
CACHE_DEFAULT_TIMEOUT = get_config('cache', 'timeout', 3600)
