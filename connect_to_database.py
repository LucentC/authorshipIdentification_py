import psycopg2


def execute_query(query):

    try:
        conn = psycopg2.connect("dbname = 'stylometry_v2' user = 'dickson' host = 'localhost' password = 'dickson'")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
    except:
        print "Error found"
    conn.close()
