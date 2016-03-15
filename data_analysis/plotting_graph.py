import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from data_analysis import calculate_principle_component
from data_analysis import calculate_linear_discriminant


def draw_2D_graph(authors, features):
    fig = plt.figure(1, figsize=(4, 3))

    # X = PCA_reduce_dimensionality(features)
    X = calculate_linear_discriminant.LDA_reduce_dimensionality(authors, features)
    y = np.choose(authors, [0, 1, 2]).astype(np.float)

    plt.scatter(X[:, 0], X[:, 1], c=y)
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.autoscale(enable=True, axis=u'both', tight=False)
    plt.show()


def draw_3D_graph(authors, features):
    fig = plt.figure(1, figsize=(4, 3))

    X = calculate_principle_component.PCA_reduce_dimensionality(features)
    y = np.choose(authors, [0, 1, 2]).astype(np.float)

    plt.clf()
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    plt.cla()
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y)
    ax.set_xlabel('PCA1')
    ax.set_ylabel('PCA2')
    ax.set_zlabel('PCA3')

    plt.show()
