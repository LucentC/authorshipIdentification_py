import numpy as np
from sklearn import preprocessing


def get_normalized_data(features):
    # mean = sum(x)/len(x)
    # std_dev = (1/len(x) * sum([ (x_i - mean)**2 for x_i in x]))**0.5
    # z_scores = [(x_i - mean)/std_dev for x_i in x]
    X = np.array(features)
    return preprocessing.scale(X)



