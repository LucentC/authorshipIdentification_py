import numpy as np
from scipy import spatial


def get_standard_hausdorff_distance(lA, lB):
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
    print "Distance between lA and lB is ", max(min_distance)
    return max(min_distance)


def get_min_of_max_hausdorff_distance(lA, lB):
    max_distance = []
    for list_from_lA in lA:
        max_val = None
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            if max_val is None:
                max_val = dis
                break
            if dis > max_val:
                max_val = dis
        max_distance.append(max_val)
    return min(max_distance)


def get_avg_of_max_hausdorff_distance(lA, lB):
    max_distance = []
    for list_from_lA in lA:
        max_val = None
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            if max_val is None:
                max_val = dis
                break
            if dis > max_val:
                max_val = dis
        max_distance.append(max_val)
    return np.average(max_distance)


def get_max_of_max_hausdorff_distance(lA, lB):
    max_distance = []
    for list_from_lA in lA:
        max_val = None
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            if max_val is None:
                max_val = dis
                break
            if dis > max_val:
                max_val = dis
        max_distance.append(max_val)
    return max(max_distance)


def get_min_of_avg_hausdorff_distance(lA, lB):
    avg_distance = []
    for list_from_lA in lA:
        total_val = 0
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            total_val += dis
        avg_distance.append(total_val / len(lB))
    return min(avg_distance)


def get_percent_hausdorff_distance(lA, lB, percentage):
    temp_list = []
    for list_from_lA in lA:
        temp = []
        for list_from_lB in lB:
            dis = spatial.distance.euclidean(list_from_lA, list_from_lB)
            temp.append(dis)
        value = sum(temp.sort()[:len(temp) * (percentage / 100)])/float(len(temp))
        temp_list.append(value)
    return max(temp_list)
