import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
#import time 
from fileutils import getfilelist, readfile, adctoamp, adctovolt, ch0calib, ch1calib
SLIDING_WINDOW_SIZE = 30

style.use('fivethirtyeight')

fig = plt.figure(figsize=(14,8))
axis1 = fig.add_subplot(3, 1, 1)
axis1.set_title("CH1")
axis1.set_ylim([-400, 400])
axis2 = fig.add_subplot(3, 1, 2)
axis2.set_title("CH2")
axis2.set_ylim([-9, 9])
axis3 = fig.add_subplot(3, 1, 3)
axis3.set_title("Marker")
axis3.set_ylim([-1.5, 1.5])

#f= open('logs/log_24-06-15-58-21.txt', 'r')
f= open('logs/log.txt', 'r')



ch0_arr = []
ch1_arr = []
freq_arr = []
timestamp_arr = []
marker_arr = []
faketime = 0;


# plot empty lines
line1, = axis1.plot(timestamp_arr, ch0_arr, color='blue', linewidth=1)
line2, = axis2.plot(timestamp_arr, ch1_arr, color='blue', linewidth=1)    
line3, = axis3.plot(timestamp_arr, marker_arr, color='blue', linewidth =1)


def animate(i):
    global faketime
    
    data_lines=f.readlines()
    for data_line in data_lines:
        if len(data_line) > 1:
            ch0, ch1, marker = data_line.split(" ")
            ch0_arr.append((int(ch0)+ch0calib)*adctovolt)
            ch1_arr.append((int(ch1)+ch1calib)*adctoamp)
            marker_arr.append(int(marker))
            timestamp_arr.append(faketime)
            faketime+=np.float(1.0/10000)

    
    axis1.set_xlim([timestamp_arr[len(timestamp_arr)-10000], timestamp_arr[len(timestamp_arr)-1]])
    axis2.set_xlim([timestamp_arr[len(timestamp_arr)-10000], timestamp_arr[len(timestamp_arr)-1]])
    axis3.set_xlim([timestamp_arr[len(timestamp_arr)-10000], timestamp_arr[len(timestamp_arr)-1]])
    

#    axis1.set_xbound(timestamp_arr[len(timestamp_arr)-100], timestamp_arr[len(timestamp_arr)-1])
#    axis2.set_xbound(timestamp_arr[len(timestamp_arr)-100], timestamp_arr[len(timestamp_arr)-1])
#    axis3.set_xbound(timestamp_arr[len(timestamp_arr)-100], timestamp_arr[len(timestamp_arr)-1])
    
    
    line1.set_data(timestamp_arr[len(timestamp_arr)-10000:len(timestamp_arr)], ch0_arr[len(timestamp_arr)-10000:len(timestamp_arr)])
    line2.set_data(timestamp_arr[len(timestamp_arr)-10000:len(timestamp_arr)], ch1_arr[len(timestamp_arr)-10000:len(timestamp_arr)])
    line3.set_data(timestamp_arr[len(timestamp_arr)-10000:len(timestamp_arr)], marker_arr[len(timestamp_arr)-10000:len(timestamp_arr)])
    
    return line1,line2,line3, 

ani = animation.FuncAnimation(fig, animate, interval=100, blit=True)#, init_func=init, interval=1)#, blit=True)
plt.show()