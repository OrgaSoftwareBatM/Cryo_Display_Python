# -*- coding: utf-8 -*-

import numpy as np
import threading
import datetime
import time
import pyvisa
import os

#serial_port = 'COM3'
#heating_current = 0.15
#heating_time = 5
#meas_current= 0.1
#meas_time = 10
#normal_refresh= 7200.0
#transfer_refresh= 15.0
#store_time = 60.0
#buffer_size = 200

class HeLevelThread(threading.Thread):
    def __init__(self,serial_port,heating_current,heating_time,meas_current,meas_time,normal_refresh,transfer_refresh,store_time,buffer_size):
        threading.Thread.__init__(self)
        self.serial_port = serial_port
        self.heating_current = heating_current
        self.heating_time = heating_time
        self.meas_current = meas_current
        self.meas_time = meas_time
        self.normal_refresh = normal_refresh
        self.transfer_refresh = transfer_refresh
        self.store_time = store_time
        self.buffer_size = buffer_size
        self.x = []
        self.y = []
        self.quit_code = False
        self.transfer_mode = False
        
        rm = pyvisa.ResourceManager()
        self.device = rm.open_resource(self.serial_port)
        self.device.write('VOLT:RANG LOW')

    def run(self):
        last_refresh = 0
        last_store = 0
        tm_on = False
        while True:  
            if self.quit_code:
                self.device.close() 
                break
            if self.transfer_mode and not tm_on: # transfer mode has been activated
                self.device.write('CURR '+str(self.heating_current))
                self.device.write('OUTP ON')
                time.sleep(self.heating_time)
                self.device.write('CURR '+str(self.meas_current))
                tm_on = True
                time.sleep(self.meas_time)        
            if not self.transfer_mode and tm_on: # transfer mode has been desactivated
                self.device.write('OUTP OFF')
                tm_on = False
            if self.transfer_mode and time.time()-last_refresh > self.transfer_refresh:
                self.refresh()
                last_refresh = time.time()
            if not self.transfer_mode and time.time()-last_refresh > self.normal_refresh:
                self.refresh()
                last_refresh = time.time()
            if time.time()-last_store > self.store_time:
                self.store()
                last_store = time.time()
            time.sleep(0.1)
            
    def refresh(self):
        if self.transfer_mode:
            readout = self.device.query('MEAS:VOLT?') 
        else:
            if self.heating_time > 0:
                self.device.write('CURR '+str(self.heating_current))
                self.device.write('OUTP ON')
                time.sleep(self.heating_time)
            self.device.write('CURR '+str(self.meas_current))
            self.device.write('OUTP ON')
            time.sleep(self.meas_time)
            readout = self.device.query('MEAS:VOLT?')
            self.device.write('OUTP OFF')
        R = float(readout) / self.meas_current 
        hours_left = self.convert(R)
        newy = np.zeros((1,2))
        newy[:] = [R,hours_left]
        if len(self.x) >= self.buffer_size: # buffer already at max size
            self.x[0:-1] = self.x[1:]   # remove the oldest value from buffer
            self.y[0:-1,:] = self.y[1:,:]
            self.x[-1] = datetime.datetime.now().replace(microsecond = 0) # add new values
            self.y[-1,:] = newy 
        else:
            self.x = np.append(self.x,datetime.datetime.now().replace(microsecond = 0)) # add new x value
            if self.y == []:
                self.y = newy
            else:
                self.y = np.concatenate((self.y,newy),0)
            
    def store(self):
        t = self.x[-1]
        str_line = t.isoformat(' ') + ', ' # build string with date and time
        str_line += ', '.join([format(val,'.1f') for val in self.y[-1,:]])
        t = t.date()
        logfile = open('HeLevel/data/' + t.isoformat() + '-helevel.txt', 'a') # file to save the data
        logfile.write(str_line+'\n')
        logfile.flush()
        
        
    def convert(self,R):        
        calfile = open('HeLevel/etal_helevel.txt')
        cal = []
        for line in calfile.readlines():
            cal.append([float(elmt) for elmt in line.split('\t')])
        calfile.close()
        cal = np.array(cal)
        hoursleft = np.interp(R,cal[:,0],cal[:,1])
        return hoursleft


#Helevel = HeLevelThread(serial_port,heating_current,heating_time,meas_current,meas_time,normal_refresh,transfer_refresh,store_time,buffer_size)
#Helevel.start()