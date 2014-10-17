"""
.. module:: shmir.settings
    :synopsis: module with settings and functions which helps getting configs
"""

import os
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
    """Function which gets settings

    Args:
        section(str): section of settings
        option(str): option of settings

    Returns:
        config or default value
    """
    try:
        return config.get(section, option)
    except Error:
        return default


def get_db_config(option):
    return config.get('database', option)


def get_int(section, option, default=None):
    """Function which gets settings

    Args:
        section(str): section of settings
        option(str): option of settings

    Returns:
        config(int) or default value
    """
    try:
        return config.getint(section, option)
    except Error:
        return default


def get_bool(section, option, default=None):
    """Function which gets settings

    Args:
        section(str): section of settings
        option(str): option of settings

    Returns:
        config(bool) or default value
    """
    try:
        return config.getboolean(section, option)
    except Error:
        return default


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
    Queue('design', routing_key='design'),
    Queue('score', routing_key='score'),
    Queue('subtasks', routing_key='subtasks',
          delivery_mode=1),
    Queue('blast', routing_key='blast',
          delivery_mode=1)
)


# Mfold
MFOLD_PATH = '/home/shmir/shmir/mfold/mfold'  # script path
MFOLD_FILES = '/tmp/mfold_files'  # Path where mfold fiels are generated


# nucleotide type for ncbi database
NUCLEOTIDE_DB = 'nucleotide'
EMAIL = 'amupoznan@gmail.com'

# Cache
CACHE_TYPE = 'redis'
# for coding purposes
if DEBUG:
    CACHE_DEFAULT_TIMEOUT = get_config('cache', 'timeout', 1)
else:
    CACHE_DEFAULT_TIMEOUT = get_config('cache', 'timeout', 3600)

# Email
EMAIL_ENABLED = get_bool('email', 'enabled', default=False)
SMTP_SERVER = get_config('email', 'smtp_server', default='smtp.gmail.com')
SMTP_PORT = get_int('email', 'smtp_port', default=587)
EMAIL_FROM = get_config('email', 'email_from')
EMAIL_PASSWORD = get_config('email', 'password')

# Blast
BLAST_PATH = get_config('blast', 'path', default=os.path.expanduser('~'))
