import math
import numpy as np
import psycopg2
from sklearn.neighbors import DistanceMetric
from scipy import spatial


def get_hausdorff_distance(lA, lB):
    min_distance = []
    for list_from_lA in lA:
        min_val = None
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            if min_val is None:
                min_val = dis
                break
            if dis < min_val:
                min_val = dis
        min_distance.append(min_val)
    return np.average(min_distance)


try:
    conn = psycopg2.connect("dbname = 'stylometry_v2' user = 'dickson' host = 'localhost' password = 'dickson'")
    cur = conn.cursor()
    #cur.execute("SELECT feature_value FROM fact WHERE doc_id = 9 AND para_id = 1617 AND (feature_id = 1 OR feature_id = 2 OR feature_id = 3 OR feature_id = 4 OR feature_id = 5 OR feature_id = 16 OR feature_id = 29 OR feature_id = 30);") #add ordered by feature_id
    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 1 AND para_id = 10;") #add ordered by feature_id

    rows = cur.fetchall()
    print rows
    l1 = []
    for row in rows:
        l1.append(row[0])

    #cur.execute("SELECT feature_value FROM fact WHERE doc_id = 9 AND para_id = 1620 AND (feature_id = 1 OR feature_id = 2 OR feature_id = 3 OR feature_id = 4 OR feature_id = 5 OR feature_id = 16 OR feature_id = 29 OR feature_id = 30);")
    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 2 AND para_id = 500;")

    rows = cur.fetchall()
    l2 = []
    for row in rows:
        l2.append(row[0])

    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 11 AND para_id = 1771 AND (feature_id = 1 OR feature_id = 2 OR feature_id = 3 OR feature_id = 4 OR feature_id = 5 OR feature_id = 16 OR feature_id = 29 OR feature_id = 30);")

    rows = cur.fetchall()
    l3 = []
    for row in rows:
        l3.append(row[0])

    #cur.execute("SELECT feature_value FROM fact WHERE doc_id = 1 AND (feature_id = 1 OR feature_id = 2 OR feature_id = 3 OR feature_id = 4 OR feature_id = 5 OR feature_id = 16 OR feature_id = 29 OR feature_id = 30);")
    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 1 ORDER BY para_id;")

    rows = cur.fetchall()
    l4 = []
    l = []
    count = 0
    for row in rows:
        if count is 57:
            count = 0
            l4.append(l)
            l = []
        count += 1
        l.append(row[0])


    #cur.execute("SELECT feature_value FROM fact WHERE doc_id = 2 AND (feature_id = 1 OR feature_id = 2 OR feature_id = 3 OR feature_id = 4 OR feature_id = 5 OR feature_id = 16 OR feature_id = 29 OR feature_id = 30);")
    cur.execute("SELECT feature_value FROM fact WHERE doc_id = 63 ORDER BY para_id;")

    rows = cur.fetchall()
    l5 = []
    l = []
    count = 0
    for row in rows:
        if count is 57:
            count = 0
            l5.append(l)
            l = []
        count += 1
        l.append(row[0])

    for i in l4:
        print i
    print "\n"
    for i in l5:
        print i
    print
    print get_hausdorff_distance(l4, l5)
    # print spatial.distance.euclidean(l1, l2)
    # print spatial.distance.cosine(l1, l2)

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
