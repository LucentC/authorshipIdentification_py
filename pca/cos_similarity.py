import math
import psycopg2
from sklearn.neighbors import DistanceMetric
from scipy import spatial


def get_hausdorff_distance(lA, lB):
    min_distance = []
    for list_from_lA in lA:
        min_val = -1
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            if min_val is -1:
                min_val = dis
                break
            if dis < min_val:
                min_val = dis
        min_distance.append(min_val)
    return max(min_distance)


try:
    conn = psycopg2.connect("dbname = 'stylometry_v2' user = 'dickson' host = 'localhost' password = 'dickson'")
    cur = conn.cursor()
    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 1 AND para_id = 1 ORDER BY feature_id;") #add ordered by feature_id

    rows = cur.fetchall()
    l1 = []
    for row in rows:
        l1.append(row[0])

    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 1 AND para_id = 60 ORDER BY feature_id;")

    rows = cur.fetchall()
    l2 = []
    for row in rows:
        l2.append(row[0])

    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 2 AND para_id = 210 ORDER BY feature_id;")

    rows = cur.fetchall()
    l3 = []
    for row in rows:
        l3.append(row[0])

    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 1;")

    rows = cur.fetchall()
    l4 = []
    l = []
    count = 0
    for row in rows:
        if count is 36:
            count = 0
            l4.append(l)
            l = []
        count += 1
        l.append(row[0])

    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 2;")

    rows = cur.fetchall()
    l5 = []
    l = []
    count = 0
    for row in rows:
        if count is 36:
            count = 0
            l5.append(l)
            l = []
        count += 1
        l.append(row[0])

    print get_hausdorff_distance(l4, l5)

    #print spatial.distance.euclidean(l1, l2)
    #print spatial.distance.cosine(l1, l2)

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
