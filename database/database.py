import psycopg2

DB_NAME = ''
DB_USER = ''
DB_PASS = ''
DB_HOST = ''
DB_PORT = 5432

def connect():
    global conn
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)

def disconnect():
    conn.close()

def execute(query):
    cur = conn.cursor()
    cur.execute(query)
    cur.close()

def init():
    query = '''CREATE TABLE IF NOT EXISTS backbone (
    id SERIAL,
    name VARCHAR(10),
    flanks3_s VARCHAR(80),
    flanks3_a VARCHAR(80),
    flanks5_s VARCHAR(80),
    flanks5_a VARCHAR(80),
    loop_s VARCHAR(30),
    loop_a VARCHAR(30),
    miRNA_s VARCHAR(30),
    miRNA_a VARCHAR(30),
    miRNA_length INT,
    miRNA_min INT,
    miRNA_max INT,
    structure VARCHAR(200),
    homogeneity INT,
    miRBase_link VARCHAR(200)
    );'''
    execute(query)
