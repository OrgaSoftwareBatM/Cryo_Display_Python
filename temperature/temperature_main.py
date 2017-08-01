# -*- coding: utf-8 -*-

import numpy as np
import threading
import datetime
import time
import sys,os
sys.path.append(os.getcwd()+'\Temperature')    # add the current file to Python path
from mmr3 import MMR3 # to find mmr3.py

class TemperatureThread(threading.Thread):
    def __init__(self,ip_address,refresh_time,store_time,buffer_size):
        threading.Thread.__init__(self)
        self.ip_address = ip_address
        self.refresh_time = refresh_time
        self.store_time = store_time
        self.buffer_size = buffer_size
        self.x = []
        self.R = []
        self.T = []
        self.quit_code = False
        self.mmr3 = MMR3(ip_address) # Start communication with MMR3
        
    def run(self):
        last_refresh = 0
        last_store = 0
        while True:  
            if self.quit_code:
                break
            if time.time()-last_refresh > self.refresh_time:
                self.refresh()
                last_refresh = time.time()
            if time.time()-last_store > self.store_time:
                self.store()
                last_store = time.time()
            time.sleep(0.1)
            
    def refresh(self):
        try:
            newR = np.array([self.mmr3.chan1.R , self.mmr3.chan2.R , self.mmr3.chan3.R]) # get new values
        except:
            print('MMR3 timeout error')
            return 0
        newT = self.convert(newR)
        newR = newR.reshape((1,3))
        newT = newT.reshape((1,3))
        if len(self.x) == 0:    # first point
            self.x = np.append(self.x,datetime.datetime.now().replace(microsecond = 0))
            self.R = newR
            self.T = newT
        elif len(self.x) >= self.buffer_size: # buffer already at max size
            self.x[0:-1] = self.x[1:]   # remove the oldest values from buffer
            self.R[0:-1,:] = self.R[1:,:]
            self.T[0:-1,:] = self.T[1:,:]
            self.x[-1] = datetime.datetime.now().replace(microsecond = 0) # add new values
            self.R[-1,:] = newR
            self.T[-1,:] = newT
        else:
            self.x = np.append(self.x,datetime.datetime.now().replace(microsecond = 0)) # add new x value
            self.R = np.concatenate((self.R,newR),0)
            self.T = np.concatenate((self.T,newT),0)
            
    def store(self):
        t = self.x[-1]
        str_line = t.isoformat(' ') + ', ' # build string with date and time
        for i in range(3): # add the resistances & temperatures
            str_line += format(self.R[-1,i],'.3E')
            str_line += ', '
            str_line += format(self.T[-1,i],'.3E')
            str_line += ', '
        str_line = str_line[0:-2] # omit the last comma and space
        t = t.date() 
        logfile = open('Temperature/data/' + t.isoformat() + '-temperature.txt', 'a') # file to save the data
        logfile.write(str_line+'\n')
        logfile.flush()
        
    def convert(self,R):        
        calnames = ['R25_table.tbl','R2_AB_Table_v2.txt','R25_table.tbl']
        T = np.zeros_like(R)
        for i,calname in enumerate(calnames):
            calfile = open('Temperature/'+calname)
            cal = []
            for line in calfile.readlines():
                cal.append([float(elmt) for elmt in line.split('\t')])
            calfile.close()
            cal = np.array(cal)
            T[i] = np.interp(abs(R[i]),cal[:,1],cal[:,0])
        return T
        
#ip_address = '192.168.1.100'
#refresh_time = 5.0
#store_time = 10.0
#buffer_size = 20000.0
#Temperature = TemperatureThread(ip_address,refresh_time,store_time,buffer_size)
#Temperature.start()