#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 20:54:59 2019

@author: burr
"""

from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from fileutils import appliancelist
from learningfunctions import readfeatures
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC



def gridsearchsvm(X, y):
    Cs = [0.001, 0.01, 0.1, 1, 10, 100]
    gammas = [0.0001, 0.001, 0.01, 0.1, 1, 10]
    kernels = ['rbf', 'linear']
    param_grid = {'C': Cs, 'gamma' : gammas, 'kernel' : kernels}
    grid_search = GridSearchCV(SVC(), param_grid, cv=2)
    grid_search.fit(X, y)
    print(grid_search.best_params_,'@', grid_search.best_score_)
    return grid_search
    
def gridsearchrf(X, y):
    n_estimators = [10,100,1000]
    min_samples_leafs=[1, 10, 50]
    max_leaf_nodes=[ 2, 10, 50]
    param_grid = {'n_estimators' : n_estimators, 'min_samples_leaf' : min_samples_leafs, 'max_leaf_nodes' : max_leaf_nodes}
    grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=2)
    grid_search.fit(X,y)
    print(grid_search.best_params_,'@', grid_search.best_score_)
    return grid_search

def gridsearchknn(X, y):
    algorithm = ['auto', 'ball_tree', 'kd_tree', 'brute']
    n_neighbors =  [1, 5, 10, 20, 50]
    leaf_size  = [10, 30, 60, 100]
    param_grid = {'algorithm' : algorithm, 'n_neighbors' : n_neighbors, 'leaf_size' : leaf_size}
    grid_search = GridSearchCV(KNeighborsClassifier(), param_grid, cv=2)
    grid_search.fit(X,y)
    print(grid_search.best_params_,'@', grid_search.best_score_)
    return grid_search

def gridsearchmlp(X, y):
    hidden_layer_sizes = [(50,), (100,), (20, 20), (50,50), (100,100), (50, 50, 50), (10, 50), (20, 20, 20, 20)]
    param_grid = {'hidden_layer_sizes' : hidden_layer_sizes}
    grid_search = GridSearchCV(MLPClassifier(), param_grid, cv=2)
    grid_search.fit(X,y)
    print(grid_search.best_params_,'@', grid_search.best_score_)
    return grid_search


appliancesublist = [x for x in appliancelist if 'laptop' not in x]

df1 = readfeatures('data/1_WithoutSwitchingEvents/featurescomplete', appliancelist)
#df2 = readfeatures('data/2_WithSwitchingEvents/featurescomplete', appliancelist)
#df300 = readfeatures('data/3_MultipleDevices_Order00/featurescomplete', ['0order00', '1order00'])
#df301 = readfeatures('data/3_MultipleDevices_Order01/featurescomplete', ['0order01', '1order10'])
#df302 = readfeatures('data/3_MultipleDevices_Order02/featurescomplete', ['0order02', '1order20'])
#df310 = readfeatures('data/3_MultipleDevices_Order10/featurescomplete', ['0order10', '1order10'])
#df311 = readfeatures('data/3_MultipleDevices_Order11/featurescomplete', ['0order11', '1order11'])
df4 = readfeatures('data/4_LaptopStates/featurescomplete', appliancelist)
#df5 = readfeatures('data/5_MassiveSwitching/featurescomplete', appliancelist)



dfmodel = df1.append(df4)

y = dfmodel.label.astype(int).values 
dfmodel = dfmodel.drop(['label'], axis=1)#, 'real_power', 'apparent_power', 'nonactive_power'], axis=1)

dfmodel = dfmodel[['apparent_power', 'real_power', 'nonactive_power',
'imag01', 'imag03', 'imag05', 'imag07', 'imag09',
'imag11', 'imag13', 'imag15', 'imag17', 'imag19',
#'imag21', 'imag23', 'imag25', 'imag27', 'imag29',
#'imag31', 'imag33', 'imag35', 'imag37', 'imag39',
#'imag41', 'imag43', 'imag45', 'imag47', 'imag49',
#'imag51', 'imag53', 'imag55', 'imag57', 'imag59',
#
#
'real01', 'real03', 'real05', 'real07', 'real09',
'real11', 'real13', 'real15', 'real17', 'real19',
#'real21', 'real23', 'real25', 'real27', 'real29',
#'real31', 'real33', 'real35', 'real37', 'real39',
#'real41', 'real43', 'real45', 'real47', 'real49',
#'real51', 'real53', 'real55', 'real57', 'real59',
#
]]

X = dfmodel
X = X.values

X_train = X
y_train = y
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=12)

gridsearch1 = gridsearchsvm(X_train, y_train)
gridsearch2 = gridsearchrf(X_train, y_train)
gridsearch3 = gridsearchknn(X_train, y_train)
gridsearch4 = gridsearchmlp(X_train, y_train)

    
# 10 Fold Validation
NFOLDS = 10
np.random.seed(10)
kf = KFold(n_splits=NFOLDS,shuffle=True, random_state=1) #leave one out cross validation, on all samples
Accuracy = 0
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
#    model1 = RandomForestClassifier(n_estimators =1000,min_samples_leaf=1, max_leaf_nodes=50,random_state=10)
#    model1 = KNeighborsClassifier(n_neighbors=1)
    model1 = SVC(C=1, gamma = 0.0001, kernel='linear')
#    model1 = MLPClassifier()
        
    model1.fit( X_train, y_train)
    Acc = model1.score(X_test,y_test)
    Accuracy = Accuracy + Acc
Accuracy = Accuracy/float(NFOLDS)
print ('AccuracyKFOLD = %.2f \n' % (Accuracy*100))




