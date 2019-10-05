#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 11:26:45 2019

@author: burr
"""

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import sklearn as sk

import pandas as pd
from matplotlib import pyplot as plt
from fileutils import labellist
from learningfunctions import Kfold_validation, evaluate, normalize, print_top5, plotfeatureimportance, decodelabels
from learningfunctions import extractdifffeaturevectors, changelabeltoeventbased
from features import columns
plt.close('all')
    
df = pd.DataFrame(columns=columns)
appliancesublist = ['laptop', 'heatbulb', 'fluorescentlight', 'kettle', 'fan2']

y5, df5 = extractdifffeaturevectors('data/5_MassiveSwitching/featurescomplete', appliancesublist) 
y5 = changelabeltoeventbased(y5)

y2, df2 = extractdifffeaturevectors('data/2_WithSwitchingEvents/featurescomplete', appliancesublist)
y2 = changelabeltoeventbased(y2)

y5.extend(y2)
dfmodel = df5.append(df2, ignore_index=True)

y = y5


#X = dfmodel.drop(['label'], axis=1)
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
X_train, X_test, y_train, y_test = sk.model_selection.train_test_split(X, y, test_size=0.33, random_state=12)

model1 = RandomForestClassifier(n_estimators =1000,min_samples_leaf=1, max_leaf_nodes=50,random_state=10)
#model1 = KNeighborsClassifier(n_neighbors=1, leaf_size=10)
#model1 = SVC(C=0.001, gamma=0.0001, kernel='linear')

model1.fit(X_train, y_train)
y_pred = model1.predict(X_test)
print('On Model Dataset')
evaluate(y_test, y_pred, labellist, plotconfusionmatrix="2OnModel2")
#print_top5(dfmodel.columns, axis=1).columns, model1)
#plotfeatureimportance(model1, dfmodel)

#
yunseen1, dfunseen1 = extractdifffeaturevectors('data/3_MultipleDevices_Order10/featurescomplete', ['0order'])
yunseen2, dfunseen2 = extractdifffeaturevectors('data/3_MultipleDevices_Order10/featurescomplete', ['1order'])
yunseen3, dfunseen3 = extractdifffeaturevectors('data/3_MultipleDevices_Order11/featurescomplete', ['0order'])
yunseen4, dfunseen4 = extractdifffeaturevectors('data/3_MultipleDevices_Order11/featurescomplete', ['1order'])
yunseen1.extend(yunseen2)
yunseen1.extend(yunseen3)
yunseen1.extend(yunseen4)
yunseen=yunseen1

dfunseen1=dfunseen1.append(dfunseen2, ignore_index=True)#.append(dfunseen3, ignore_index=True).append(dfunseen4, ignore_index=True)
dfunseen1=dfunseen1.append(dfunseen3, ignore_index=True)
dfunseen1=dfunseen1.append(dfunseen4, ignore_index=True)
dfunseen=dfunseen1
#Xunseen = dfunseen.drop(['label'],axis=1)

dfunseen = dfunseen[['apparent_power', 'real_power', 'nonactive_power',
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
Xunseen = dfunseen

Xunseen = Xunseen.values


y_unseenpred = model1.predict(Xunseen)
evaluate(yunseen, y_unseenpred, labellist, plotconfusionmatrix="2OnUnseen31")


