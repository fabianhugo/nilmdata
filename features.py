#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 13:58:23 2019

@author: burr
"""

from fileutils import readfile, getfilelist, adctoamp, adctovolt, ch0calib, ch1calib
import numpy as np
import pandas as pd
import os
import time

columns = {'apparent_power', 'real_power', 'nonactive_power',
'imag01', 'imag03', 'imag05', 'imag07', 'imag09',
'imag11', 'imag13', 'imag15', 'imag17', 'imag19',
'imag21', 'imag23', 'imag25', 'imag27', 'imag29',
'imag31', 'imag33', 'imag35', 'imag37', 'imag39',
'imag41', 'imag43', 'imag45', 'imag47', 'imag49',
'imag51', 'imag53', 'imag55', 'imag57', 'imag59',
'imag61', 'imag63', 'imag65', 'imag67', 'imag69',
'imag71', 'imag73', 'imag75', 'imag77', 'imag79',
'imag81', 'imag83', 'imag85', 'imag87', 'imag89',
'imag91', 'imag93', 'imag95', 'imag97', 'imag99',
'real01', 'real03', 'real05', 'real07', 'real09',
'real11', 'real13', 'real15', 'real17', 'real19',
'real21', 'real23', 'real25', 'real27', 'real29',
'real31', 'real33', 'real35', 'real37', 'real39',
'real41', 'real43', 'real45', 'real47', 'real49',
'real51', 'real53', 'real55', 'real57', 'real59',
'real61', 'real63', 'real65', 'real67', 'real69',
'real71', 'real73', 'real75', 'real77', 'real79',
'real81', 'real83', 'real85', 'real87', 'real89',
'real91', 'real93', 'real95', 'real97', 'real99',


'label'} 



def concatenatedf(path):
    filelist, dirlist, filenamelist = getfilelist(path)

    li = []

    for filename in filelist:
        df = pd.read_csv(filename, index_col=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv(os.path.join(path, 'all.csv'))
    print ('concatenated to ', os.path.join(path, 'all.csv'))

    

                

def savefeaturestocsv(path, saveto):
    filelist, dirlist, namelist = getfilelist(path)
    
    for file in filelist:
        outputfile = os.path.join(saveto, os.path.basename(os.path.dirname(file)), os.path.splitext(os.path.basename(file))[0] + '.csv')
        data = extractfeatures(file)
        if not os.path.isdir(os.path.join(saveto,os.path.basename(os.path.dirname(file)))):
            os.makedirs(os.path.join(saveto,os.path.basename(os.path.dirname(file))))
        data.to_csv(outputfile)
    

    
        
def extractfeatures(file):
    fs=10000
    data = pd.DataFrame(columns=columns)
    
    timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename = readfile(file)
            
    voltage = (ch0_arr+ch0calib)*adctovolt
    current = (ch1_arr+ch1calib)*adctoamp
    window = int(fs/10)
    starttime=time.time()

    for i in range(int(len(ch0_arr)/window)):    
        currentwindowed = current[i*window:(i+1)*window]
        voltagewindowed = voltage[i*window:(i+1)*window]
        currentrfft = np.fft.rfft(currentwindowed)#*np.hanning(len(currentwindowed)))
                
        voltagerms = np.sqrt(np.sum(pow(voltagewindowed,2))/len(voltagewindowed))
        currentrms = np.sqrt(np.sum(pow(currentwindowed,2))/len(currentwindowed))
                
        instpower = np.multiply(currentwindowed,voltagewindowed)
        realpower = np.sum(instpower)/len(instpower)
        apparentpower = voltagerms*currentrms
        nonactivepower=np.sqrt(apparentpower**2/realpower**2)
                
        data.loc[i] = pd.Series({
                        
                'apparent_power': apparentpower, 
                'real_power': realpower, 
                'nonactive_power': nonactivepower, 
                
                'real01': np.abs(np.real((currentrfft[ 5]))), 
                'real03': np.abs(np.real((currentrfft[15]))), 
                'real05': np.abs(np.real((currentrfft[25]))), 
                'real07': np.abs(np.real((currentrfft[35]))), 
                'real09': np.abs(np.real((currentrfft[45]))), 
                'real11': np.abs(np.real((currentrfft[55]))), 
                'real13': np.abs(np.real((currentrfft[65]))), 
                'real15': np.abs(np.real((currentrfft[75]))), 
                'real17': np.abs(np.real((currentrfft[85]))), 
                'real19': np.abs(np.real((currentrfft[95]))), 
                'real21': np.abs(np.real((currentrfft[105]))), 
                'real23': np.abs(np.real((currentrfft[115]))), 
                'real25': np.abs(np.real((currentrfft[125]))), 
                'real27': np.abs(np.real((currentrfft[135]))), 
                'real29': np.abs(np.real((currentrfft[145]))), 
                'real31': np.abs(np.real((currentrfft[155]))), 
                'real33': np.abs(np.real((currentrfft[165]))), 
                'real35': np.abs(np.real((currentrfft[175]))), 
                'real37': np.abs(np.real((currentrfft[185]))), 
                'real39': np.abs(np.real((currentrfft[195]))), 
                'real41': np.abs(np.real((currentrfft[205]))), 
                'real43': np.abs(np.real((currentrfft[215]))), 
                'real45': np.abs(np.real((currentrfft[225]))), 
                'real47': np.abs(np.real((currentrfft[235]))), 
                'real49': np.abs(np.real((currentrfft[245]))), 
                'real51': np.abs(np.real((currentrfft[255]))), 
                'real53': np.abs(np.real((currentrfft[265]))), 
                'real55': np.abs(np.real((currentrfft[275]))), 
                'real57': np.abs(np.real((currentrfft[285]))), 
                'real59': np.abs(np.real((currentrfft[295]))), 
                'real61': np.abs(np.real((currentrfft[305]))), 
                'real63': np.abs(np.real((currentrfft[315]))), 
                'real65': np.abs(np.real((currentrfft[325]))), 
                'real67': np.abs(np.real((currentrfft[335]))), 
                'real69': np.abs(np.real((currentrfft[345]))), 
                'real71': np.abs(np.real((currentrfft[355]))), 
                'real73': np.abs(np.real((currentrfft[365]))), 
                'real75': np.abs(np.real((currentrfft[375]))), 
                'real77': np.abs(np.real((currentrfft[385]))), 
                'real79': np.abs(np.real((currentrfft[395]))), 
                'real81': np.abs(np.real((currentrfft[405]))), 
                'real83': np.abs(np.real((currentrfft[415]))), 
                'real85': np.abs(np.real((currentrfft[425]))), 
                'real87': np.abs(np.real((currentrfft[435]))), 
                'real89': np.abs(np.real((currentrfft[445]))), 
                'real91': np.abs(np.real((currentrfft[455]))), 
                'real93': np.abs(np.real((currentrfft[465]))), 
                'real95': np.abs(np.real((currentrfft[475]))), 
                'real97': np.abs(np.real((currentrfft[485]))), 
                'real99': np.abs(np.real((currentrfft[495]))), 
                
                'imag01': np.abs(np.imag((currentrfft[ 5]))), 
                'imag03': np.abs(np.imag((currentrfft[15]))), 
                'imag05': np.abs(np.imag((currentrfft[25]))), 
                'imag07': np.abs(np.imag((currentrfft[35]))), 
                'imag09': np.abs(np.imag((currentrfft[45]))), 
                'imag11': np.abs(np.imag((currentrfft[55]))), 
                'imag13': np.abs(np.imag((currentrfft[65]))), 
                'imag15': np.abs(np.imag((currentrfft[75]))), 
                'imag17': np.abs(np.imag((currentrfft[85]))), 
                'imag19': np.abs(np.imag((currentrfft[95]))), 
                'imag21': np.abs(np.imag((currentrfft[105]))), 
                'imag23': np.abs(np.imag((currentrfft[115]))), 
                'imag25': np.abs(np.imag((currentrfft[125]))), 
                'imag27': np.abs(np.imag((currentrfft[135]))), 
                'imag29': np.abs(np.imag((currentrfft[145]))), 
                'imag31': np.abs(np.imag((currentrfft[155]))), 
                'imag33': np.abs(np.imag((currentrfft[165]))), 
                'imag35': np.abs(np.imag((currentrfft[175]))), 
                'imag37': np.abs(np.imag((currentrfft[185]))), 
                'imag39': np.abs(np.imag((currentrfft[195]))), 
                'imag41': np.abs(np.imag((currentrfft[205]))), 
                'imag43': np.abs(np.imag((currentrfft[215]))), 
                'imag45': np.abs(np.imag((currentrfft[225]))), 
                'imag47': np.abs(np.imag((currentrfft[235]))), 
                'imag49': np.abs(np.imag((currentrfft[245]))), 
                'imag51': np.abs(np.imag((currentrfft[255]))), 
                'imag53': np.abs(np.imag((currentrfft[265]))), 
                'imag55': np.abs(np.imag((currentrfft[275]))), 
                'imag57': np.abs(np.imag((currentrfft[285]))), 
                'imag59': np.abs(np.imag((currentrfft[295]))), 
                'imag61': np.abs(np.imag((currentrfft[305]))), 
                'imag63': np.abs(np.imag((currentrfft[315]))), 
                'imag65': np.abs(np.imag((currentrfft[325]))), 
                'imag67': np.abs(np.imag((currentrfft[335]))), 
                'imag69': np.abs(np.imag((currentrfft[345]))), 
                'imag71': np.abs(np.imag((currentrfft[355]))), 
                'imag73': np.abs(np.imag((currentrfft[365]))), 
                'imag75': np.abs(np.imag((currentrfft[375]))), 
                'imag77': np.abs(np.imag((currentrfft[385]))), 
                'imag79': np.abs(np.imag((currentrfft[395]))), 
                'imag81': np.abs(np.imag((currentrfft[405]))), 
                'imag83': np.abs(np.imag((currentrfft[415]))), 
                'imag85': np.abs(np.imag((currentrfft[425]))), 
                'imag87': np.abs(np.imag((currentrfft[435]))), 
                'imag89': np.abs(np.imag((currentrfft[445]))), 
                'imag91': np.abs(np.imag((currentrfft[455]))), 
                'imag93': np.abs(np.imag((currentrfft[465]))), 
                'imag95': np.abs(np.imag((currentrfft[475]))), 
                'imag97': np.abs(np.imag((currentrfft[485]))), 
                'imag99': np.abs(np.imag((currentrfft[495]))), 
               
                'label': label_arr[int(i)*window]

               })
    print(file,'converted in %4f'% (time.time()-starttime))
    return data

        


if __name__ == '__main__':
    savefeaturestocsv(path='labelled/1_WithoutSwitchingEvents', saveto='data/1_WithoutSwitchingEvents/featurescomplete/')

    savefeaturestocsv(path='labelled/2_WithSwitchingEvents', saveto='data/2_WithSwitchingEvents/featurescomplete')

    savefeaturestocsv(path='labelled/3_MultipleDevices_Order00', saveto='data/3_MultipleDevices_Order00/featurescomplete')
    savefeaturestocsv(path='labelled/3_MultipleDevices_Order01', saveto='data/3_MultipleDevices_Order01/featurescomplete')
    savefeaturestocsv(path='labelled/3_MultipleDevices_Order02', saveto='data/3_MultipleDevices_Order02/featurescomplete')
    savefeaturestocsv(path='labelled/3_MultipleDevices_Order10/', saveto = 'data/3_MultipleDevices_Order10/featurescomplete')
    savefeaturestocsv(path='labelled/3_MultipleDevices_Order11/', saveto = 'data/3_MultipleDevices_Order11/featurescomplete')

    savefeaturestocsv(path='labelled/4_LaptopStates/', saveto = 'data/4_LaptopStates/featurescomplete')

    savefeaturestocsv(path='labelled/5_MassiveSwitching/', saveto = 'data/5_MassiveSwitching/featurescomplete')

