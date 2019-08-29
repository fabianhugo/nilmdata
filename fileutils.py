#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:01:12 2019

@author: burr
"""


import os
from shutil import copy2
import numpy as np

appliancelist = ['nothing', 'heatbulb','kettle','fan1','fan2','fan3','microwave1','microwave2','microwave3','laptop','monitor','fluorescentlight','cellphonecharger', 'idlehp', '1threadhp', '2threadshp', '3threadshp', 'idlesamsung', '1threadsamsung', '2threadssamsung', '3threadssamsung', '4threadssamsung', 'videosamsung']
labellist = ['no load', 'heatbulb','kettle','fan1','fan2','fan3','microwaveon','microwaveidle','microwavestarting','laptop','monitor','fluorescentlight','cellphonecharger', 'idlehp', '1threadhp', '2threadshp', '3threadshp', 'idlesamsung', '1threadsamsung', '2threadssamsung', '3threadssamsung', '4threadssamsung', 'videosamsung']
labeldict = {
0:'no load',
1:'heatbulb',
2:'kettle',
3:'fan1',
4:'fan2',
5:'fan3',
6:'microwaveon',
7:'microwaveidle',
8:'microwavestarting',
9:'laptop',
10:'monitor',
11:'fluorescentlight',
12:'cellphonecharger',
13:'idlehp',
14:'1threadhp',
15:'2threadshp',
16:'3threadshp',
17:'idlesamsung',
18:'1threadsamsung',
19:'2threadssamsung',
20:'3threadssamsung',
21:'4threadssamsung',
22:'videosamsung'}


adctovolt = 1203.3*1203.3 * 1.25 / (pow(2,13) *3.3 *1203.3) #sorted to multiplications first), reciprocal of voltage divider and non inverting amplifier
adctoamp =  -150 * 1.25 /(pow(2,13) *22) #inverting amplifier
ch0calib = +41
ch1calib = -84


def readfile(path='logs/log.txt', ):
    ch0_arr = []
    ch1_arr = []
    marker_arr = []
    timestamp_arr = []
    faketime = 0;
    label_arr = []
    
    i=0
    f= open(path, 'r')

    if (len(f.readline().split(' '))==4):
        labelled=True
    else:
        labelled=False
    f.seek(0)
    
    data_line=f.readline()
    
    while(len(data_line) > 0):
        if labelled:
            ch0, ch1, marker, label = data_line.split(" ")
            label_arr.append(int(label))

        else:
            ch0, ch1, marker = data_line.split(" ")

        ch0_arr.append(int(ch0))
        ch1_arr.append(int(ch1))
        marker_arr.append(int(marker))
        timestamp_arr.append(faketime)
        faketime+=np.float(1.0/10000)
        data_line=f.readline()
        i=i+1
        

    f.close()
    return np.array(timestamp_arr), np.array(ch0_arr), np.array(ch1_arr), marker_arr, label_arr, path



def getfilelist(path='logs'):# Get filenames and save them to filelist   
    filelist = []
    filenamelist = []
    dirlist = []
    for (path, dirs, files) in os.walk(path):
        for file in files:
            if (file!='00_report.txt'):
                filelist.append((os.path.join(path, file)))
                dirlist.append(path)
                filenamelist.append(file)


    return filelist, dirlist, filenamelist

def renameall(filelist, dirlist, filenamelist, oldname, newname):
    counter = 0
    for (i,file) in enumerate(filelist):
        if (filenamelist[i] == oldname):
            os.rename(filelist[i], (dirlist[i]+ '/' + newname))
            print(filelist[i])
            print(dirlist[i]+ '/' + newname)
            counter=counter+1

    print("Renamed Files:", counter)






