import psycopg2
from settings import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT

def connect():
    global conn
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER,\
            password=DB_PASS, host=DB_HOST, port=DB_PORT)

def disconnect():
    conn.close()

def execute(query, var=None):
    with conn.cursor() as cur:
        cur.execute(query, var)

def execute_with_one_response(query, var=None):
    with conn.cursor() as cur:
        cur.execute(query, var)
        data = cur.fetchone()
    return data
    
def execute_with_response(query, var=None):
    cur = conn.cursor()
    cur.execute(query, var)
    data = cur.fetchall()
    cur.close()
    return data

def add(name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s, loop_a,\
        miRNA_s, mirRNA_a, miRNA_length, miRNA_min, miRNA_max, structure,\
        homogeneity, miRBase_link):
    query = "INSERT INTO backbone VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %d, %d, %d, %s, %d, %s);"
    var = (name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s, loop_a,\
            miRNA_s, mirRNA_a, miRNA_length, miRNA_min, miRNA_max, structure,\
            homogeneity, miRBase_link)
    execute(query, var)

def get_by_name(name):
    query = "SELECT name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s,"\
            "loop_a, miRNA_s, miRNA_a, miRNA_length, miRNA_min, miRNA_max,"\
            "structure, homogeneity, miRBase_link FROM backbone WHERE LOWER(name) = LOWER(%s);"
    data = execute_with_one_response(query, (name,))
    return serialize(*data) if data else {}

def get_all():
    query = "SELECT name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s,"\
            "loop_a, miRNA_s, miRNA_a, miRNA_length, miRNA_min, miRNA_max,"\
            "structure, homogeneity, miRBase_link FROM backbone;"
    return get_multirow_by_query(query)

def get_by_miRNA_s(letters):
    query = "SELECT name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s,"\
            "loop_a, miRNA_s, miRNA_a, miRNA_length, miRNA_min, miRNA_max,"\
            "structure, homogeneity, miRBase_link FROM backbone WHERE miRNA_s LIKE %s;"
    return get_multirow_by_query(query, (letters.upper() + "%",))

def get_multirow_by_query(query, var=None):
    data = execute_with_response(query, var)
    backbones = []
    for row in data:
        backbones.append(serialize(*row))
    return backbones

def serialize(name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s,\
        loop_a, miRNA_s, miRNA_a, miRNA_length, miRNA_min, miRNA_max,\
        structure, homogeneity, miRBase_link):
    return {
        'name': name,
        'flanks3_s': flanks3_s,
        'flanks3_a': flanks3_a,
        'flanks5_s': flanks5_s,
        'flanks5_a': flanks5_a,
        'loop_s': loop_s,
        'loop_a': loop_a,
        'miRNA_s': miRNA_s,
        'miRNA_a': miRNA_a,
        'miRNA_length': miRNA_length,
        'miRNA_min': miRNA_min,
        'miRNA_max': miRNA_max,
        'structure': structure,
        'homogeneity': homogeneity,
        'miRBase_link': miRBase_link
    }
