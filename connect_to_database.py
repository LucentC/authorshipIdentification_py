import psycopg2

conn = psycopg2.connect("dbname = 'stylometry_v2' user = 'dickson' host = 'localhost' password = 'dickson'")


def execute_query(query):

    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except:
        print "Error found"
    conn.close()
