#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 11:26:45 2019

@author: burr
"""


from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split


from matplotlib import pyplot as plt
from fileutils import labellist
from learningfunctions import Kfold_validation, evaluate, normalize, print_top5, plotfeatureimportance, decodelabels

from learningfunctions import extractdifffeaturevectors, changelabeltoeventbased, readfeatures
from fileutils import appliancelist

plt.close('all')

appliancesublist = [x for x in appliancelist if 'laptop' not in x]

df1 = readfeatures('data/1_WithoutSwitchingEvents/featurescomplete', appliancelist)
#df2 = readfeatures('data/2_WithSwitchingEvents/featurescomplete', appliancelist)
df300 = readfeatures('data/3_MultipleDevices_Order00/featurescomplete', ['0order00', '1order00'])
df301 = readfeatures('data/3_MultipleDevices_Order01/featurescomplete', ['0order01', '1order10'])
df302 = readfeatures('data/3_MultipleDevices_Order02/featurescomplete', ['0order02', '1order20'])
#df310 = readfeatures('data/3_MultipleDevices_Order10/featurescomplete', ['0order10', '1order10'])
#df311 = readfeatures('data/3_MultipleDevices_Order11/featurescomplete', ['0order11', '1order11'])
#df4 = readfeatures('data/4_LaptopStates/featurescomplete', appliancelist)
#df5 = readfeatures('data/5_MassiveSwitching/featurescomplete', appliancelist)


dfmodel = df1
dfunseen = df300.append(df301).append(df302)

y = dfmodel.label.astype(int).values 

#df1 = df1.drop(['label'], axis=1)#, 'real_power', 'apparent_power', 'reactive_power'], axis=1)
dfmodel = dfmodel[['apparent_power', 'real_power', 'reactive_power',
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
X = dfmodel.values

X_train = X
y_train = y
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=12)

#Kfold_validation(X_train, y_train, model='MLP')

#model1 = RandomForestClassifier(n_estimators =1000,min_samples_leaf=1, max_leaf_nodes=10,random_state=10)
#model1 = KNeighborsClassifier(n_neighbors=20, leaf_size=10)
model1 = SVC(C=1, gamma=0.0001, kernel='linear')
#model1 = LinearDiscriminantAnalysis()
#model1 = MLPClassifier()



model1.fit(X_train, y_train)
y_pred = model1.predict(X_test)
print('On Model Dataset')
evaluate(y_test, y_pred, labellist, plotconfusionmatrix="1OnModel1")
#print_top5(dfmodel.columns, model1)
#plotfeatureimportance(model1, dfmodel)

#
yu = dfunseen.label.astype(int).values 
#dfunseen = dfunseen.drop(['label'], axis=1)
dfunseen = dfunseen[['apparent_power', 'real_power', 'reactive_power',
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
Xu = dfunseen.values

X_trainu = Xu
y_trainu = yu
X_trainu, X_testu, y_trainu, y_testu = train_test_split(Xu, yu, test_size=0.33, random_state=12)



y_predu = model1.predict(X_testu)
print('On Unseen Dataset')
evaluate(y_testu, y_predu, labellist, plotconfusionmatrix="1OnUnseen3")

