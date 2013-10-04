Backbone RNA database
==========================

How to use it:

1. Add data to PostgreSQL:
```
sudo -u postgres psql < shmirdesignercreate.sql
```
2. Install requirements:
```
pip install -r requirements.txt
```
3. Create file named settings.py which contains global variables: DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT:
```
DB_NAME = 'shmird'
DB_USER = 'postgres'
DB_PASS = 'mypassword'
DB_HOST = '127.0.0.1'
DB_PORT = '5432'
```
4. Run server:
```
./main.py
```

RESTful API will be available at http://127.0.0.1:5000/

Methods - all require POST request and answer with JSON data:
* /get_all
* /get_by_name/data
* /get_by_mirna_s/data - only two first letters
* /mfold/data

5. Set up new urls in:
* shmir_designer/mfold.py:
```
URL = 'http://127.0.0.1:5000/mfold'
```
* shmir_designer/backbone.py:
```
HOST = 'http://127.0.0.1:5000/'
```