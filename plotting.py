#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 11:37:01 2019

@author: burr
"""

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from fileutils import getfilelist, readfile, adctoamp, adctovolt, ch0calib, ch1calib,appliancelist
import os

appliancelistforplots = ['No Load', 'Incandescent Light Bulb','Electric Kettle','Fan - Level 1','Fan - Level 2','Fan - Level 3','Microwave Oven','Microwave Oven','Microwave Oven','Laptop','Computer Monitor','Fluorescent Light','Smartphone-Charger', 'HP Idle', 'HP 1 Thread', 'HP 2 Threads', 'HP 3 Threads', 'Samsung Idle', 'Samsung 1 Thread', 'Samsung 2 Threads', 'Samsung 3 Threads', 'Samsung 4 Threads', 'Samsung Playing Video']
experimentlist = ['1_WithoutSwitchingEvents', '2_WithSwitchingEvents', '4_LaptopStates',
                  '3_MultipleDevices_Order00', '3_MultipleDevices_Order01', '3_MultipleDevices_Order02', '3_MultipleDevices_Order10', '3_MultipleDevices_Order11']

def plotforthesis(path):
    timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename = readfile(path)
    
    plt.figure()
#    plt.title("")
    plt.ylabel('Voltage [V]')
    plt.xlabel('Time [s]')
    plt.plot(timestamp_arr, (ch0_arr+ch0calib)*adctovolt, linewidth = 1, marker = '')
    
    plt.figure()
    plt.ylabel('Current [A]')
    plt.xlabel('Time [s]')
    plt.plot(timestamp_arr, (ch1_arr+ch1calib)*adctoamp, linewidth = 1)
    

def plotdata(timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename):
    
    fig, (axis1, axis2, axis3, axis4) = plt.subplots(nrows=4, sharex=True, figsize=(14,8))
#    plt.ion()

    fig.suptitle(filename)
    axis1.set_title("Voltage")
    axis1.set_ylabel('[V]')
    #axis1.set_ylim([-400, 400])
    
    axis2.set_title("Current")
    axis2.set_ylabel('[A]')
    #axis2.set_ylim([-10, 10])
    
    axis3.set_title("Power")
    axis3.set_ylabel('[W]')
        
    axis1.plot(timestamp_arr, (ch0_arr+ch0calib)*adctovolt, linewidth = 1, marker = '')
    axis2.plot(timestamp_arr, (ch1_arr+ch1calib)*adctoamp, linewidth = 1)
    
    power = pd.Series(np.multiply(((ch0_arr+ch0calib)*adctovolt),((ch1_arr+ch1calib)*adctoamp)))    
    axis3.plot(timestamp_arr, power, linewidth = 1)
    axis3.plot(timestamp_arr, power.rolling(window=int(10000/50)).mean(), linewidth = 1)
    
    if (len(label_arr)>0):
        axis2.plot(timestamp_arr,label_arr, linewidth=1)
        axis2.set_title("Current and Label")

    axis4.set_title("Marker")
    axis4.set_ylim([-1.5, 1.5])
    axis4.plot(timestamp_arr, marker_arr, linewidth = 1)
    plt.pause(0.001)
    plt.draw()
    plt.show()
    
def plotfile(path):
    timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename = readfile(path)
    plotdata(timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename)
    

    
def plotappliance(experiment, appliance):
    filelist, dirlist, namelist = getfilelist('labelled/')
    for file in filelist:
        if ((experiment in file) and (appliance in file)):
            plotfile(file)

        
def plotspectogram(path, title=1):
    timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename = readfile(path)
    plt.ioff()
    fig, ax1 = plt.subplots(nrows=1)
    if (title):
        plt.suptitle(appliancelistforplots[appliancelist.index(os.path.basename(filename).split('.')[0].split('_')[-1])])

    current = (ch1_arr+ch1calib)*adctoamp
    fs = 10000
    windowsize = 1000
    Pxx, freqs, bins, im = ax1.specgram(current, NFFT=windowsize,Fs=fs, mode='magnitude', scale='dB' , vmin=-130, vmax = 20)#, cmap=plt.cm.gist_heat)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Frequency [Hz]')
    fig.colorbar(im).set_label('Intensity [dB]')

    scenario = os.path.basename(os.path.dirname(os.path.dirname(filename)))
    scenarioinstance = os.path.basename(os.path.dirname(filename))
    saveto = os.path.join('plots', 'spectrograms', scenario, scenarioinstance)
    if not os.path.isdir(saveto):
        os.makedirs(saveto)
 
    plt.savefig(os.path.join(saveto, os.path.basename(filename).split('.')[0])+'.svg')
    plt.close()
    plt.ion()

def plotrfft(path, title=1):
    plt.ioff()
    timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename = readfile(path)
    fig, (ax1) = plt.subplots(nrows=1)
    if (title):
        fig.suptitle(appliancelistforplots[appliancelist.index(os.path.basename(filename).split('.')[0].split('_')[-1])])

    current = (ch1_arr+ch1calib)*adctoamp
    fs = 10000

    ax1.set_ylabel('Amplitude [dB]')
    ax1.set_ylim((-120, 20))
    plt.xlabel('Frequency [Hz]') 


    currentrfft = np.fft.rfft(current)
    currentrfft = currentrfft/len(currentrfft)
    
    rfftfreqs = np.fft.rfftfreq(len(current), 1/fs)
    ax1.plot(rfftfreqs, 20*np.log10(np.abs(currentrfft)))    
    
    scenario = os.path.basename(os.path.dirname(os.path.dirname(filename)))
    scenarioinstance = os.path.basename(os.path.dirname(filename))
    saveto = os.path.join('plots', 'spectra', scenario, scenarioinstance)
    if not os.path.isdir(saveto):
        os.makedirs(saveto)
 
    plt.savefig(os.path.join(saveto, os.path.basename(filename).split('.')[0])+'.svg')#, dpi=500)
    plt.close()
    plt.ion()
    

def plotappliancespectograms(experiment, appliance):
    plt.close('all')
    filelist, dirlist, namelist = getfilelist()
    for file in filelist:
        if ((experiment in file) and (appliance in file)):
            if not ('order' in file):
                plotspectogram(file)
            else:
                plotspectogram(file,title=0)
            
            
def plotappliancerffts(experiment, appliance):
    plt.close('all')
    filelist, dirlist, namelist = getfilelist()
    for file in filelist:
        if ((experiment in file) and (appliance in file)):
            if not ('order' in file):
                plotrfft(file)
            else:
                plotrfft(file,title=0)

def plotpowerandlabel(path, title=1):
    filelist, dirlist, namelist = getfilelist(path)
    plt.ioff()
    for file in filelist:
        timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename = readfile(file)
    
        fig, (axis1, axis2) = plt.subplots(nrows=2, sharex=True)
        
        if (title):
            fig.suptitle(appliancelistforplots[appliancelist.index(os.path.basename(filename).split('.')[0].split('_')[-1])])
        
        axis1.set_title("Power")
        axis1.set_ylabel('[W]')
        
        axis2.set_title("Label")
        axis2.set_xlabel('Time [s]')
    
            
        power = pd.Series(np.multiply(((ch0_arr+ch0calib)*adctovolt),((ch1_arr+ch1calib)*adctoamp)))    
#        axis1.plot(timestamp_arr, power, linewidth = 1)
        axis1.plot(timestamp_arr, power.rolling(window=int(10000/50)).mean(), linewidth = 1, color='orange')
        
#        axis1.set_xlim([0.1,0.3])
        axis1.set_ylim([-50, 1500])
        
        axis2.set_ylim([-1,23])
        axis2.plot(timestamp_arr, label_arr, color='g')
    
        scenario = os.path.basename(os.path.dirname(os.path.dirname(filename)))
        scenarioinstance = os.path.basename(os.path.dirname(filename))
        saveto = os.path.join('plots', 'powertrace', scenario, scenarioinstance)
        if not os.path.isdir(saveto):
            os.makedirs(saveto)
     
        plt.savefig(os.path.join(saveto, os.path.basename(filename).split('.')[0])+'.svg')#, dpi=500)
        plt.close()
    
    plt.ion()


if __name__ == '__main__':
#    for appliance in appliancelist:
#        plotappliancerffts('1_WithoutSwitchingEvents', appliance)
#        plotappliancerffts('2_WithSwitchingEvents', appliance)
#        plotappliancerffts('4_LaptopStates', appliance)
    
    for appliance in appliancelist:
#        plotappliancespectograms('1_WithoutSwitchingEvents', appliance)
#        plotappliancespectograms('2_WithSwitchingEvents', appliance)
#        plotappliancespectograms('4_LaptopStates', appliance)
        plotappliancespectograms('5_MassiveSwitching', appliance)

#    plotappliancespectograms('3_MultipleDevices_Order00', 'order')
#    plotappliancespectograms('3_MultipleDevices_Order01', 'order')
#    plotappliancespectograms('3_MultipleDevices_Order02', 'order')
#    plotappliancespectograms('3_MultipleDevices_Order10', 'order')
#    plotappliancespectograms('3_MultipleDevices_Order11', 'order')
        
    
    
#    plotpowerandlabel('labelled/1_WithoutSwitchingEvents/0108_1100')
#    plotpowerandlabel('labelled/2_WithSwitchingEvents/0108_1200')
#    plotpowerandlabel('labelled/4_LaptopStates/1508_1800')
    
#    plotpowerandlabel('labelled/3_MultipleDevices_Order00', title=0)
#    plotpowerandlabel('labelled/3_MultipleDevices_Order01', title=0)
#    plotpowerandlabel('labelled/3_MultipleDevices_Order02', title=0)
#    plotpowerandlabel('labelled/3_MultipleDevices_Order10', title=0)
#    plotpowerandlabel('labelled/3_MultipleDevices_Order11', title=0)
#    plotpowerandlabel('labelled/3_MultipleDevices_Order11', title=0)
    
#    plotpowerandlabel('labelled/5_MassiveSwitching')
    pass