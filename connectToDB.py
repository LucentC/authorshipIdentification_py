import psycopg2

conn = psycopg2.connect("dbname = 'stylometry' user = 'dickson' host = 'localhost' password = 'dickson'")
cursor = conn.cursor()

# SQL queries to extract stylometric feature from database
SQL_ONE = "SELECT * FROM author;"

try:
    cursor.execute(SQL_ONE)
except:
    print "Error found"

conn.close()
