# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 12:36:33 2018

@author: Ronald Scheffler
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
import sklearn.metrics as sm
from sklearn.metrics.cluster import silhouette_score

def cluster(csv, k):
    
    data = pd.read_csv(csv) 
    # X Features
    X = np.array(data.drop(['botname'], 1))
    X = scale(X.data)   
    # Wähle Anzahl der Cluster, Startpunk der Centroids, Iterationen 
    # Random State seed für Reproduktion der Ergebnisse
    clustering = KMeans(n_clusters = k,init ='k-means++',n_init= 10,random_state = 6)
    
    clustering.fit(X)
    
    X_scaled = X

    result = clustering.fit_predict(X)    
    
    data['Cluster'] = result
    data = data.sort_values(['Cluster'])
    
    data.to_csv(r"C:\Users\Ronald Scheffler\.spyder-py3\clusterresult"+str(k)+".csv")

    print(silhouette_score(X_scaled, result))    
    
cluster(r"C:\Users\Ronald Scheffler\.spyder-py3\clustermergemin5.csv", 5)

        
