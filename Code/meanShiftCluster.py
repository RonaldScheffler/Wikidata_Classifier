# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 18:01:37 2018

@author: Ronald Scheffler
"""


# Scale Variables!
# Estimate number of Centroids / Clusters

import numpy as np
import pandas as pd
from sklearn.cluster import MeanShift
from sklearn.preprocessing import scale
from sklearn.metrics.cluster import silhouette_score
from sklearn import metrics

def cluster(csv):
    
    data = pd.read_csv(csv) 
    # X Features
    X = np.array(data.drop(['botname'], 1))
    #print(X)

    X = scale(X.data)
    
    # Wähle Anzahl der Cluster, Random State seed für Reproduktion der Ergebnisse
    clustering = MeanShift()
    
    clustering.fit(X)
#    print(X_scaled)
    X_scaled = X
    #print(X_scaled)

    result = clustering.fit_predict(X)    
    
    data['Cluster'] = result
    data = data.sort_values(['Cluster'])
    
    data.to_csv(r"C:\Users\Ronald Scheffler\.spyder-py3\meanshiftresult.csv")
    # Auswertung: 
    # Silhouette Score?
    print(silhouette_score(X_scaled, result))
    print(data)
    # CLass Prediction for Trainingsset
    from sklearn.model_selection import train_test_split
    X = np.array(data.drop(['botname'], 1))
    y = data['Cluster'] # Klassen?
    X_train, X_test, y_train, y_test = train_test_split(X,y, random_state = 0)
    print(X_test)
    print(y)
    #y_pred_class = clustering.predict(X_test)
    # Calculate Accuracy
    #print('Accuracy :' ,metrics.accuracy_score(y_test, y_pred_class)) 
    
    
cluster(r"C:\Users\Ronald Scheffler\.spyder-py3\clustermergemin5.csv")

        
