import psycopg2
from data_etl.db_schema_classes.author import Author


def execute_insert_query(query):

    try:
        print "Connecting to database..."
        conn = psycopg2.connect("dbname = 'stylometry_v2' user = 'dickson' host = 'localhost' password = 'dickson'")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
        print "Finished running insert query"
        conn.close()
    except psycopg2.DatabaseError as e:
        print "Cannot connect to database"
        print e.pgerror


def test_if_author_exists(author):
     author.get_author_name()