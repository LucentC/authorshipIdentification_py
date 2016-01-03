import psycopg2


def execute_insert_query(query):

    try:
        print "Connecting to database..."
        conn = psycopg2.connect("dbname = 'stylometry_v2' user = 'dickson' host = 'localhost' password = 'dickson'")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
        print "Finished running insert query"
    except psycopg2.DatabaseError as e:
        print "Cannot connect to database"
        print e.pgerror
    conn.close()
