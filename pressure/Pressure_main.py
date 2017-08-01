# -*- coding: utf-8 -*-

import numpy as np
import threading
import datetime
import time
import sys,os
sys.path.append(os.getcwd()+'\Pressure')    # add the current file to Python path
from PfeifferVacuum import MaxiGauge, MaxiGaugeError # to find PfeifferVacuum.py

class PressureThread(threading.Thread):
    def __init__(self,serial_port,refresh_time,store_time,buffer_size):
        threading.Thread.__init__(self)
        self.serial_port = serial_port
        self.refresh_time = refresh_time
        self.store_time = store_time
        self.buffer_size = buffer_size
        self.x = []
        self.y = []
        self.quit_code = False
        self.gauge = MaxiGauge(self.serial_port) # Start communication with Serial port (RS232)
        self.gauge_names = self.gauge.send('CID',1) # ask for channel names
        self.gauge_names = self.gauge_names[0].split(',') # format the names in a list
        self.active_gauge = [sensor.status in [0,1,2] for sensor in self.gauge.pressures()] # update active gauges
        self.Ng = len(self.gauge_names)
        
    def run(self):
        last_refresh = 0
        last_store = 0
        while True:  
            if self.quit_code:
                self.gauge.disconnect()
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
            ps = self.gauge.pressures() # Read the new pressures
        except MaxiGaugeError as mge:
            print(mge)
            return 0
        self.active_gauge = [sensor.status in [0,1,2] for sensor in self.gauge.pressures()] # update active gauges
        newy = np.zeros((1,self.Ng))
        newy[:] = [sensor.pressure if sensor.status in [0,1,2]  else np.NaN for sensor in ps] # get new values
        if len(self.x) == 0:    # first point
            self.x = np.append(self.x,datetime.datetime.now().replace(microsecond = 0))
            self.y = newy
        elif len(self.x) >= self.buffer_size: # buffer already at max size
            self.x[0:-1] = self.x[1:]   # remove the oldest values from buffer
            self.y[0:-1,:] = self.y[1:,:]
            self.x[-1] = datetime.datetime.now().replace(microsecond = 0) # add new values
            self.y[-1,:] = newy
        else:
            self.x = np.append(self.x,datetime.datetime.now().replace(microsecond = 0)) # add new x value
            self.y = np.concatenate((self.y,newy),0)
                
            
    def store(self):
        t = self.x[-1]
        str_line = t.isoformat(' ') + ', ' # build string with date and time
        for i in range(self.Ng): # add the pressure of the active gauges (blanks otherwise)
            if self.active_gauge[i]:
                str_line += '%.3E' % self.y[-1,i]
            str_line += ', '
        str_line = str_line[0:-2] # omit the last comma and space
        t = t.date() 
        logfile = open('Pressure/data/' + t.isoformat() + '-pressures.txt', 'a') # file to save the data
        logfile.write(str_line+'\n')
        logfile.flush()
#        
#serial_port = 'COM4'
#refresh_time = 5.0
#store_time = 10.0
#buffer_size = 200.0
#Pressure = PressureThread(serial_port,refresh_time,store_time,buffer_size)
#Pressure.start()