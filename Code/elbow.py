# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 16:38:09 2018

@author: Ronald Scheffler
"""

 # clustering dataset
# determine k using elbow method

from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import scale


data = pd.read_csv(r"C:\Users\Ronald Scheffler\.spyder-py3\out2018.csv")

Nc = range(1, 10)

X = np.array(data.drop(['botname'], 1))
    #print(X)
X = scale(X.data)

kmeans = [KMeans(n_clusters=i) for i in Nc]

kmeans

score = [kmeans[i].fit(X).score(X) for i in range(len(kmeans))]

score

pl.plot(Nc,score)

pl.xlabel('Number of Clusters')

pl.ylabel('Score')

pl.title('Elbow Curve')

pl.show()















#x1 = np.array([3, 1, 1, 2, 1, 6, 6, 6, 5, 6, 7, 8, 9, 8, 9, 9, 8])
#x2 = np.array([5, 4, 5, 6, 5, 8, 6, 7, 6, 7, 1, 2, 1, 2, 3, 2, 3])
#
#plt.plot()
#plt.xlim([0, 10])
#plt.ylim([0, 10])
#plt.title('Dataset')
#plt.scatter(x1, x2)
#plt.show()
#
## create new plot and data
#plt.plot()
#X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
#colors = ['b', 'g', 'r']
#markers = ['o', 'v', 's']
#
## k means determine k
#distortions = []
#K = range(1,10)
#for k in K:
#    kmeanModel = KMeans(n_clusters=k).fit(X)
#    kmeanModel.fit(X)
#    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
#
## Plot the elbow
#plt.plot(K, distortions, 'bx-')
#plt.xlabel('k')
#plt.ylabel('Distortion')
#plt.title('The Elbow Method showing the optimal k')
#plt.show()