from ConfigParser import ConfigParser
from pkg_resources import resource_filename, Requirement

config = ConfigParser()
print resource_filename(Requirement.parse('shmir_api'), 'shmir.conf')
config.read(resource_filename(Requirement.parse('shmir_api'), 'shmir.conf'))

get_db_config = lambda option: config.get('database', option)

DB_NAME = get_db_config('name')
DB_USER = get_db_config('user')
DB_PASS = get_db_config('password')
DB_HOST = get_db_config('host')
DB_PORT = get_db_config('port')

#nucleotide type for ncbi database
NUCLEOTIDE_DB = 'nucleotide'
