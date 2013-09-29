Baza danych szkieletów RNA
==========================

Sposób użycia:

1. Dodaj dane do bazy PostgreSQL:
```
sudo -u postgres psql < shmirdesignercreate.sql
```
2. Zainstaluj requirementsy:
```
pip install -r requirements.txt
```
3. Stwórz plik settings.py z ustawieniami twojej isntacji PostgreSQL w zmiennych DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT:
```
DB_NAME = 'shmird'
DB_USER = 'postgres'
DB_PASS = 'mypassword'
DB_HOST = '127.0.0.1'
DB_PORT = '5432'
```
4. Odpal serwer:
```
python main.py
```

API będzie dostępne na http://127.0.0.1:5000

Dostępne metody, które wymagają zapytania POST w formacie JSON:
* get_all
* get_by_name (wymaga parametru 'data')
* get_by_mirna_s (wymaga parametru 'data')

Przykład zapytania:
```
import requests
import json

req = requests.post('http://127.0.0.1:5000/get_by_name', json.dumps({'data': 'example'}), headers={'content-type': 'application/json'})
data = json.loads(req.content)
```