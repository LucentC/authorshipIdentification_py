import math
import psycopg2
from sklearn.neighbors import DistanceMetric

def square_rooted(x):
    return round(math.sqrt(sum([a*a for a in x])),3)


def cosine_similarity(x,y):
    numerator = sum(a*b for a,b in zip(x,y))
    denominator = square_rooted(x)*square_rooted(y)
    return round(numerator/float(denominator),3)


try:
    conn = psycopg2.connect("dbname = 'stylometry_v2' user = 'dickson' host = 'localhost' password = 'dickson'")
    cur = conn.cursor()
    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 4 AND para_id = 1491;")

    rows = cur.fetchall()
    l1 = []
    for row in rows:
        l1.append(row[0])

    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 4 AND para_id = 1492;")

    rows = cur.fetchall()
    l2 = []
    for row in rows:
        l2.append(row[0])

    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 4 AND para_id = 1493;")

    rows = cur.fetchall()
    l3 = []
    for row in rows:
        l3.append(row[0])

    dist = DistanceMetric.get_metric('euclidean')
    X = [l1, l2]
    print dist.pairwise(X)

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
