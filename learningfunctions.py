#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 11:21:18 2019

@author: burr
"""
import numpy as np

from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from matplotlib import pyplot as plt
import scikitplot as skplt
import pandas as pd
from fileutils import getfilelist, labeldict, labellist
from features import columns

from os import path, makedirs

def Kfold_validation(X_new,Y_new, model = 'LDA'):
    NFOLDS = 10#X_new.shape[0] # x is examples
    np.random.seed(10)
    kf = KFold(n_splits=NFOLDS,shuffle=True, random_state=1) #leave one out cross validation, on all samples
    Accuracy = 0
    for train_index, test_index in kf.split(X_new):
        X_train, X_test = X_new[train_index], X_new[test_index]
        y_train, y_test = Y_new[train_index], Y_new[test_index]
        if model == 'LDA':
            model1 = LinearDiscriminantAnalysis()
        elif model == 'RF':
            model1 = RandomForestClassifier(n_estimators =10,min_samples_leaf=4, max_leaf_nodes=12,random_state=10)
        elif model == 'KNN':
            model1 = KNeighborsClassifier(n_neighbors=1)
        elif model == 'SVM':
            model1 = SVC(C=100, gamma = 0.01, kernel='rbf')
        elif model == 'MLP':
            model1 = MLPClassifier()
            
        model1.fit( X_train, y_train)
        Acc = model1.score(X_test,y_test)
        #model1.predict
        Accuracy = Accuracy + Acc
        #metrics to evaluate the algorithm. See the corresponding class.
    Accuracy = Accuracy/float(NFOLDS)
    print ('AccuracyKFOLD = %.2f \n' % (Accuracy*100))
    
    
def evaluate(y_true, y_pred, labellist, plotconfusionmatrix=False, cmfontsize=7):
    precision, recall, fbeta, support = precision_recall_fscore_support(y_true, y_pred, average='weighted', warn_for='')
    Acc = accuracy_score(y_true, y_pred)
    print ('Accuracy= %.2f' % (Acc*100))
    print ('Preccision= %.2f' % (precision*100))
    print ('Recall = %.2f' % (recall*100))
    print ('Fbeta = %.2f' % (fbeta*100))
    if len(plotconfusionmatrix)>0:
        plt.ioff()
        fig, ax = plt.subplots(figsize=(11,10))#, dpi=300)

        skplt.metrics.plot_confusion_matrix(decodelabels(y_true), decodelabels(y_pred), normalize=True, text_fontsize = cmfontsize, x_tick_rotation=90, title=' ',ax=ax)
        ax.images[-1].colorbar.remove()
        saveto = path.join('plots','cm')
        if not path.isdir(saveto):
            makedirs(saveto)
        fig.savefig(path.join(saveto,plotconfusionmatrix+'.svg'),bbox_inches = 'tight',)#, dpi=300)
        plt.ion()
#        plt.show()

    
def scatterplot(df):
    labelsublist = [x for x in labellist if 'samsung' not in x and 'no load' not in x and 'hp' not in x and 'microwave' not in x]
#    labelsublist = ['laptop', 'idlehp', '1threadhp', '2threadshp', '3threadshp', 'idlesamsung', '1threadsamsung', '2threadssamsung', '3threadssamsung', '4threadssamsung', 'videosamsung']
    fig, ax = plt.subplots()
    hsv = plt.get_cmap('hsv')
    colors = hsv(np.linspace(0, 1.0, len(labelsublist)))
    for i,label in enumerate(labelsublist):
        ax.scatter(df[df['label']==labellist.index(label)].real01, df[df['label']==labellist.index(label)].imag01, label=label, color=colors[i])
        ax.legend()
    plt.xlabel('Active Power [W]')
    plt.ylabel('Reactive Power [var]')
    plt.show()

def scatterplot1d(df):
    labelsublist = labellist[0:13]
#    labelsublist = [x for x in labelsublist if 'no load' not in x]
    fig, ax = plt.subplots(figsize=(10,4))
    hsv = plt.get_cmap('hsv')
    colors = hsv(np.linspace(0, 0.9, len(labelsublist)))
    for i,label in enumerate(labelsublist):
        ax.scatter(df[df['label']==labellist.index(label)].real_power, np.zeros(len(df[df['label']==labellist.index(label)].real_power)), label=label, color=colors[i], linewidths = 0.01)#, marker='.')
        ax.legend(ncol =4)
    plt.xlabel('Active Power [W]')
    ax.get_yaxis().set_visible(False)
    plt.show()

def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result
    

     
def print_top5(feature_names, model):
    """Prints features with the highest coefficient values, per class"""
    for i, class_label in enumerate(model.classes_):
        top10 = np.argsort(abs(model.coef_[i]))[-5:]
        print("%s: %s" % (labeldict[class_label],
              " ".join(feature_names[j] for j in top10)))


def plotfeatureimportance(model, df):
    #only for linear SVM Classifier
    plt.ioff()
    for i, class_label in enumerate(model.classes_):
        fig = plt.figure(figsize=(10,6))
        fig.suptitle(labeldict[class_label])
        pd.Series(abs(model.coef_[i]), index=df.columns).nlargest(10).plot(kind='barh')
        plt.savefig(path.join('plots',labeldict[class_label]+'.png'), dpi=200)

    plt.ion()
#        plt.show()
        


def readfeatures(path, appliances):    
    df = pd.DataFrame(columns=columns)
    dfs = []
    filelist, dirlist, filenamelist = getfilelist(path)
    for file in filelist:
        for appliance in appliances:
            if appliance in file:
                dfs.append(pd.read_csv(file, index_col=0))
    df = pd.concat(dfs, axis=0, ignore_index=True)
    return df

def decodelabels(labels):
    return list(map(lambda i: labeldict[i], labels)) 

def detectswitchingevents(real_power, threshold = 5, hysteresis =100 ):

    triggered = 0
    events  = []
    real_powerold = 0
    i = 0
    while i < len(real_power):
        if(abs(real_power[i]-real_powerold))>threshold and not triggered:    
            triggered = 1
            events.append(i)
        
        if triggered:
            if i > events[-1]+hysteresis:
                triggered=0
    
        real_powerold=real_power[i]
        
        i+=1

    print(events, len(events))
    return events


def calculatedifffeaturevector(df):
    y=df.label.astype(int).values
    difffeaturevector = pd.DataFrame(columns=columns)
    ydifffeatvector = []
    
    events = detectswitchingevents(df.real_power, threshold=5, hysteresis=50)
    
    for event in events:    
        a = calculatedifffeatures(df, event)
        difffeaturevector = difffeaturevector.append(a, ignore_index=True)

        ydifffeatvector.append(y[event+20])
        

    return events, difffeaturevector, ydifffeatvector




def extractdifffeaturevectors(path, appliances):
    difffeaturevectorall = pd.DataFrame(columns=columns)
    y = []
    filelist, dirlist, filenamelist = getfilelist(path)
    
    for file in filelist:
        if not 'nothing' in file:
            for appliance in appliances:
                if appliance in file:
                    df = pd.read_csv(file, index_col=0)
                    print(file.split('/')[-2],file.split('/')[-1], end=' ')
                    events, difffeaturevector, yd = calculatedifffeaturevector(df)
                    
                    if (len(events) > 0):
                        difffeaturevectorall = difffeaturevectorall.append(difffeaturevector, ignore_index=True)
                        y.extend(yd)
                 

        if 'nothing' in file and 'nothing' in appliances:
            df = pd.read_csv(file, index_col=0)
            yd = df.label.astype(int).values[100]
            difffeaturevector = calculatedifffeatures(df, 100)
            difffeaturevectorall = difffeaturevectorall.append(difffeaturevector, ignore_index=True)
            y.append(yd)
    
    return y, difffeaturevectorall 





def changelabeltoeventbased(labels):
    #Use this if labels dont follow the label pattern for eventbased load detection. (1 0 2 0 3 0 -> 1 1 2 2 3 3)
    
    labelnew = []
    for i, y in enumerate(labels):
        if y ==0:
            y=labels[i-1]
        labelnew.append(y)
        
    return labelnew
    


def calculatedifffeatures(X,i):
#    return abs(X.loc[i+20] - X.loc[i-20])
#    return abs(((X.loc[i+1]+X.loc[i+2])/2 - (X.loc[i-1]+X.loc[i-2])/2))
    return abs(((X.loc[i+1]+X.loc[i+20]+X.loc[i+10])/3 - (X.loc[i-1]+X.loc[i-20]+X.loc[i-10])/3))
#    return abs(((X.loc[i+30]+X.loc[i+20]+X.loc[i+10])/3 - (X.loc[i-30]+X.loc[i-20]+X.loc[i-10])/3))
    
