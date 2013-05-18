import psycopg2
from models import Backbone

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

def execute_with_one_response(query):
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchone()
    cur.close()
    return data
    
def execute_with_response(query):
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

def add(name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s, loop_a, miRNA_s, mirRNA_a, miRNA_length, miRNA_min, miRNA_max, structure, homogeneity, miRBase_link):
    query = "INSERT INTO backbone VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %d, %d, %d, %s, %d, %s);" % (name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s, loop_a, miRNA_s, mirRNA_a, miRNA_length, miRNA_min, miRNA_max, structure, homogeneity, miRBase_link)
    execute(query)

def get_by_name(name):
    query = "SELECT name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s, loop_a, miRNA_s, mirRNA_a, miRNA_length, miRNA_min, miRNA_max, structure, homogeneity, miRBase_link FROM backbone WHERE name = %s;" % name
    data = execute_with_one_response(query) #nie jestem pewien czy to nie bedzie pierwszy element listy
    return Backbone(*data)

def get_all():
    query = "SELECT name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s, loop_a, miRNA_s, mirRNA_a, miRNA_length, miRNA_min, miRNA_max, structure, homogeneity, miRBase_link FROM backbone;"
    data = execute_with_response(query)
    backbones = []
    for row in data:
        backbones.append(Backbone(*row))
    return backbones
