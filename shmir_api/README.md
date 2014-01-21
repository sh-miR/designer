Backbone RNA database
==========================

How to use it:

### Add data to PostgreSQL:
```
sudo -u postgres psql < shmirdesignercreate.sql
```
### Create file named local.cfg which contains following stuff and your real password instead of **mypassword**:
```
[buildout]
extends = buildout.cfg

[settings_database]
password = mypassword
```
### Build application
Run these commands to build API serving data from database and mfold results:
```
python3.3 bootstrap.py
bin/buildout -c local.cfg
```
### Run server:
```
bin/runserver
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
bin/uwsgi --xml parts/uwsgi/uwsgi.xml
```
give the proper rights to socket:
```
chmod 707 /tmp/uwsgi.sock
```

[Back](../README.md)
