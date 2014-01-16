Backbone RNA database
==========================

How to use it:

### Add data to PostgreSQL:
```
sudo -u postgres psql < shmirdesignercreate.sql
```
### Install requirements:
```
pip install -r requirements.txt
```
### Create file named settings.py which contains global variables: DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT:
```
DB_NAME = 'shmird'
DB_USER = 'postgres'
DB_PASS = 'mypassword'
DB_HOST = '127.0.0.1'
DB_PORT = '5432'
```
### Run server:
```
./main.py
```
RESTful API will be available at http://127.0.0.1:5000/

Methods - all require POST request and answer with JSON data:
* /get_all
* /get_by_name/data
* /get_by_mirna_s/data - only two first letters
* /mfold/data

### Set up new urls in:
* shmir_designer/mfold.py:
```
URL = 'http://127.0.0.1:5000/mfold'
```
* shmir_designer/backbone.py:
```
HOST = 'http://127.0.0.1:5000/'
```

## Deploying

sh-miR API deploy is exatcly the same as in the other Flask based generic app.

As in the development way, you should have dedicated virtualenv, install requirements, put sqldump to PostgreSQL. But you mustn't run main.py! Never use built-in servers in production.

Instead of this, you should configure nginx to work with uwsgi:

```
location / { try_files $uri @yourapplication; }
location @yourapplication {
    include uwsgi_params;
    uwsgi_pass unix:/<path_to_shmir_instance>/uwsgi.sock;
}
```

Run uwsgi:
```
uwsgi -s uwsgi.sock -w main:app
```
give the proper rights to socket:
```
chmod 707 uwsgi.sock
```

[Back](../README.md)
