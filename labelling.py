#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:10:44 2019

@author: burr
"""

from plotting import plotdata, plotfile
from fileutils import readfile, getfilelist, labellist
from matplotlib import pyplot as plt

import os
import numpy as np
    

def labelSingleAppliancesWithoutSwitchingEvents(relativepath):
    
    filelist, dirlist, namelist = getfilelist(relativepath)
    for file in filelist: 
        if 'microwave' not in file: #microwaves are statemachine operated devices, therefore need to be theated differently
            label=labellist.index(file.split('/')[-1].split('_')[-1].split('.')[0])
            
            timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename = readfile(file)
            label_arr = []
                
            for timestamp in timestamp_arr:
                    label_arr.append(label)

            saveto = os.path.join('labelled/'+file.split('/')[1]+'/'+file.split('/')[2])                    
            if not os.path.isdir(saveto): # only directory of file starting from working directory/logs
                os.makedirs(saveto)
                
            
            with open(os.path.join(saveto, file.split('/')[3]), 'w') as g:
                g.write('')
                for i in range(len(ch0_arr)):
                    g.write("%i %i %i %i\n" % (ch0_arr[i], ch1_arr[i], marker_arr[i], label_arr[i]))
                
            g.close()
            print('Labbeled', file)


def labelSingleAppliancesWithSwitchingEvents():
    path = 'logs/2_WithSwitchingEvents/'
    filelist, dirlist, namelist = getfilelist(path)
    for file in filelist:
    #file = filelist[7]    
        label=labellist.index(file.split('/')[-1].split('_')[-1].split('.')[0])
        
        timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename = readfile(file)
        label_arr = []
            
        if not 'nothing' in file:
            fig = plt.figure(figsize=(40, 20))
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(timestamp_arr, ch1_arr)
            ready = 0
            while not ready:
                ready = plt.waitforbuttonpress()
            ready = 0
            while not ready:
                ready = plt.waitforbuttonpress()
                
            [(timeofswitch, y)] = plt.ginput(1)
            plt.close()
            
            for timestamp in timestamp_arr:
                if timestamp < timeofswitch:
                    label_arr.append(0)
                    
                else:
                    label_arr.append(label)#'Appliancelabel of file')
            
        else:
            for timestamp in timestamp_arr:
                label_arr.append(0)
                
        if not os.path.isdir('labelled/'+file.split('/')[1]+'/'+file.split('/')[2]): # only directory of file starting from working directory/logs
            os.makedirs('labelled/'+file.split('/')[1]+'/'+file.split('/')[2])
            
        with open('labelled/'+file.split('/')[1]+'/'+file.split('/')[2] + '/' + file.split('/')[3], 'w') as g:
            g.write('')
            for i in range(len(ch0_arr)):
                g.write("%i %i %i %i\n" % (ch0_arr[i], ch1_arr[i], marker_arr[i], label_arr[i]))
            
        g.close()
        print(file+' labelled')
        
        #plot result:
#        if not 'nothing' in file:
#            #plot file
#            timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename = readfile('labelled/'+file.split('/')[1]+'/'+file.split('/')[2] + '/' + file.split('/')[3])
#            plotdata(timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename)
#            ready=0
#            while not ready:
#                ready = plt.waitforbuttonpress()
#            ready = 0
#            while not ready:
#                ready = plt.waitforbuttonpress()
#            plt.close()
        


           
def labelSingleAppliancesMicrowave(relativepath):
    filelist, dirlist, namelist = getfilelist(relativepath)
    for file in filelist:
        saveto= os.path.join('labelled/',file.split('/')[1],file.split('/')[2])
        if 'microwave' in file:
#            print ('%20s %i \n%20s %i \n%20s %i \n%20s %i' % ('microwaveon ', labellist.index('microwaveon'), 'microwaveidle ', labellist.index('microwaveidle'), 'microwavestarting ', labellist.index('microwavestarting'), 'nothing ', labellist.index('nothing')))
            labelMultipleApplianceStates(file, saveto)

def labelMultipleApplianceExperiments(relativepath):
    filelist, dirlist, namelist = getfilelist(relativepath)
    for file in filelist:
        saveto= os.path.join('labelled/',file.split('/')[1],file.split('/')[2])
        labelMultipleApplianceStates(file, saveto)
            
def labelMultipleApplianceStates(file, saveto):
    if not os.path.exists(os.path.join(saveto,file.split('/')[3])):
        timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename = readfile(file)
        label_arr = []
        
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(timestamp_arr, ch1_arr)
        fig.suptitle(file)
        timeofswitch_arr = []
        ready = 0
        plt.pause(1)
        
        a = int(input('How many sections of different appliance states does this recording have?'))
        for i in range(a-1):
            print('Find the %i of %i switching event(s). Do two button presses before selecting with mousebutton. O-Key is zoom'% (i+1, a-1))
            ready = 0
            while not ready:
                ready = plt.waitforbuttonpress()
            ready = 0
            while not ready:
                ready = plt.waitforbuttonpress()
        
            [(timeofswitch, y)] = plt.ginput(1)
            timeofswitch_arr.append(timeofswitch)
            plt.axvline(timeofswitch, color='r')
            print('Event recorded at:', timeofswitch)
        
        
        plt.close()
        plt.figure(figsize=(10, 5))
        plt.plot(timestamp_arr, ch1_arr)
        plt.show()
        plt.pause(1)
        
        for label in labellist[0:13]:
            print ("%20s %i" %(label, labellist.index(label)))
        cursor=0
        for j in range(a-1):
            
            labelinput=input('Label till %f :?'% timeofswitch_arr[j])
            
            for k in range(len(ch0_arr[cursor:np.nonzero(timestamp_arr>timeofswitch_arr[j])[0][0]])):
                label_arr.append(int(labelinput))
            cursor=np.nonzero(timestamp_arr>timeofswitch_arr[j])[0][0]
        
        
        if (a>1):
            labelinput=input('Label after %f :?'% timeofswitch_arr[j])
            for j in range(len(ch0_arr[cursor:])):
                label_arr.append(int(labelinput))
        else: # Only one label
            labelinput=input('Label of the recording?')
            for j in range(len(timestamp_arr)):
                label_arr.append(int(labelinput))
            
            
        if not os.path.isdir(saveto): # only directory of file starting from working directory/logs
            os.makedirs(saveto)
        
        with open(os.path.join(saveto,file.split('/')[3]), 'w') as g:
            g.write('')
            for i in range(len(ch0_arr)):
                g.write("%i %i %i %i\n" % (ch0_arr[i], ch1_arr[i], marker_arr[i], label_arr[i]))
        
        print('Labbeled', file, 'to:', os.path.join(saveto,file.split('/')[3]))
        g.close()
        plt.close()


if __name__ == '__main__':
    labelSingleAppliancesWithoutSwitchingEvents('logs/1_WithoutSwitchingEvents')
    labelSingleAppliancesMicrowave('logs/1_WithoutSwitchingEvents')
    
    labelSingleAppliancesWithSwitchingEvents('logs/2_WithSwitchingEvents')
    labelSingleAppliancesMicrowave('logs/2_WithSwitchingEvents')

    labelMultipleApplianceExperiments('logs/3_MultipleDevices_Order00')
    labelMultipleApplianceExperiments('logs/3_MultipleDevices_Order01')    
    labelMultipleApplianceExperiments('logs/3_MultipleDevices_Order02')

    labelMultipleApplianceExperiments('logs/3_MultipleDevices_Order10')
    labelMultipleApplianceExperiments('logs/3_MultipleDevices_Order11')

    labelSingleAppliancesWithoutSwitchingEvents('logs/4_LaptopStates/2008_1200/')
    
    labelMultipleApplianceExperiments('logs/5_MassiveSwitching')            
