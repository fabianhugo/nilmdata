import socket
import time
import datetime
from plotting import plotdata
from fileutils import readfile


def twos_comp(val, bits): #https://stackoverflow.com/questions/1604464/twos-complement-in-python
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val  

#TCPIP_IP = "137.204.213.220"
#TCPIP_PORT = 4545 # 4545 set in router: is forwarded to 5707 on ip 192.168.1.222
TCPIP_IP = "192.168.1.222"
#TCPIP_IP = "10.42.0.44"
#TCPIP_IP = "172.20.10.5"
TCPIP_PORT = 5707
datentime = datetime.datetime.now()
#logfile = "logs/log_"+datentime.strftime("%d-%m-%y-%H-%M-%S")+".txt"
logfile = "logs/log.txt"
BUFFERSIZE = 64 #in samples of 4 byte


# CLEAR log file
with open(logfile, "w") as f:
    f.write("")

print("DATA WILL BE WRITTEN TO:", logfile)
print(datentime.strftime("%d-%m-%y-%H-%M-%S"))


sock = socket.socket(socket.AF_INET, # Internet
                   socket.SOCK_STREAM) # TCPIP
                   #socket.SOCK_DGRAM) #UDP
sock.connect((TCPIP_IP, TCPIP_PORT))
print("Connected")


starttime=time.time()
switchon = 0
samplelist = []

while 1:
    marker = 0
    data = sock.recv(BUFFERSIZE*4, socket.MSG_WAITALL) # waits for full message
    #print(data)
    for i in range (BUFFERSIZE):
        if ((int.from_bytes(data[(i*4):(i*4)+2], byteorder='big')&0b1000000000000000)==0b1000000000000000):#check for marker on ping buffer
            marker = 1;
            print('BUFFEROVERFLOW')

        if ((int.from_bytes(data[(i*4):(i*4)+2], byteorder='big')&0b0100000000000000)==0b0100000000000000):#check for marker on pong buffer
            marker = -1;
            print('BUFFEROVERFLOW')

        ch0raw = int.from_bytes(data[(i*4):(i*4)+2], byteorder='big')&0b0011111111111111
        ch1raw = int.from_bytes(data[(i*4)+2:(i*4)+4], byteorder='big')&0b0011111111111111
        samplelist.append((twos_comp(ch0raw, 14), twos_comp(ch1raw, 14), marker))

    with open(logfile, "a") as f:
        for sample in samplelist:
            f.write("%i %i %i\n" %  sample)
        samplelist.clear()

    if((time.time()-starttime > 15)&(switchon==0)):
        print(switchon+1, ' Switch', time.time())
        switchon= switchon +1
    
    if((time.time()-starttime > 30)&(switchon==1)):
        print(switchon+1, ' Switch', time.time())
        switchon= switchon +1
#        break
         #stop here for experiment 1 & 2

    if((time.time()-starttime > 45)&(switchon==2)):
        print(switchon+1, ' Switch', time.time())
        switchon= switchon +1
        
    if((time.time()-starttime > 60)&(switchon==3)):
        print(switchon+1, ' Switch', time.time())
        switchon= switchon +1
#        break
    if((time.time()-starttime > 75)&(switchon==4)):
        print(switchon+1, ' Switch', time.time())
        switchon= switchon +1
        
    if((time.time()-starttime > 90)&(switchon==5)):
        print(switchon+1, ' Switch', time.time())
        switchon= switchon +1

    if((time.time()-starttime > 105)&(switchon==6)):
        print(switchon+1, ' Switch', time.time())
        switchon= switchon +1
        
    if((time.time()-starttime > 120)&(switchon==7)):
        print(switchon+1, ' Switch', time.time())
        switchon= switchon +1

    if((time.time()-starttime > 135)&(switchon==8)):
        print(switchon+1, ' Switch', time.time())
        switchon= switchon +1
        
    if((time.time()-starttime > 150)&(switchon==9)):
        print(switchon+1, ' Switch', time.time())
        switchon= switchon +1
    
    if((time.time()-starttime > 165)&(switchon==10)):
        switchon= switchon +1
        print('Finished')
        break

timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename = readfile()
plotdata(timestamp_arr, ch0_arr, ch1_arr, marker_arr, label_arr, filename)
#sock.settimeout(1) #1s to wait
#while 1:
#    marker = 0
#    data, addr = sock.recvfrom(4) # waits for full message
#    if ((int.from_bytes(data[0:2], byteorder='big')&0b1000000000000000)==0b1000000000000000):#check for marker on ping buffer
#        marker = 1;
#    
#    if ((int.from_bytes(data[0:2], byteorder='big')&0b0100000000000000)==0b0100000000000000):#check for marker on pong buffer
#        marker = -1;
#        
#    ch0raw = int.from_bytes(data[0:2], byteorder='big')
#    ch1raw = int.from_bytes(data[2:4], byteorder='big')
#    ch0 = twos_comp(ch0raw, 14)*1.25/pow(2,13)
#    ch1 = twos_comp(ch1raw, 14)*1.25/pow(2,13)
#    with open(logfile, "a") as f:
#        f.write("%f %f %i\n" %  (ch0, ch1, marker))
##    if(time.time()-starttime > 300):
##        break
