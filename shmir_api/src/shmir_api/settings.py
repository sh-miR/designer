from configparser import ConfigParser
from os import environ

config = ConfigParser()
config.readfp(open(environ['SHMIR_API_SETTINGS']))
config = config['database']

DB_NAME = config['name']
DB_USER = config['user']
DB_PASS = config['password']
DB_HOST = config['host']
DB_PORT = config['port']

#nucleotide type for ncbi database
NUCLEOTIDE_DB = 'nucleotide'
