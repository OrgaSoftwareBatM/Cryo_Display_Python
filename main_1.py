# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:31:25 2017

@author: manip.batm
"""

import sys,os
sys.path.append(os.getcwd())    # add the current file to Python path
from Pressure.Pressure_main import PressureThread
from HeLevel.HeLevel_main import HeLevelThread
from Temperature.temperature_main import TemperatureThread
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
import time
from datetime import datetime,timedelta
import threading
import warnings
warnings.filterwarnings("ignore",".*GUI is implemented.*")
warnings.filterwarnings("ignore",".*deprecated.*")
 
class PlottingWindow(threading.Thread):
    def __init__(self,Pressure,Temperature,HeLevel,pressure_range=3600.0,temperature_range=3600.0,helevel_range=3600.0,refresh_time=1.0):
        threading.Thread.__init__(self)
        self.Pressure = Pressure
        self.Temperature = Temperature
        self.HeLevel = HeLevel
        self.pressure_range = pressure_range # in sec
        self.temperature_range = temperature_range  
        self.helevel_range = helevel_range
        self.refresh_time = refresh_time # in sec
        self.quit_code = False
        
        self.fig = plt.figure(figsize=(16,9)) # create figure and subplots
        self.axes = []
        self.axes.append(plt.subplot(4,2,1))
        self.axes.append(plt.subplot(4,2,3,sharex=self.axes[0]))
        self.axes.append(plt.subplot(4,2,5,sharex=self.axes[0]))
        self.axes.append(plt.subplot(4,2,7,sharex=self.axes[0]))
        self.axes.append(plt.subplot(4,2,2))
        self.axes.append(plt.subplot(4,2,4,sharex=self.axes[4]))
        self.axes.append(plt.subplot(4,2,6))
        
        self.fig.tight_layout()
        self.lines = []
        formatter = DateFormatter('%H:%M')
        for ax in self.axes[0:6]:
            ax.xaxis.set_major_formatter(formatter) 
            
        for i,graph_name in enumerate(['PIVC','PB1K','PVAT','PHE3']):
            self.axes[i].set_title(graph_name)
            self.axes[i].set_yscale('log')
            self.axes[i].grid(True)
#            self.axes[i].yaxis.set_tick_params(which='minor')
            self.lines.append(self.axes[i].plot([],[])[0])  
            
        
        self.lines.append(self.axes[4].plot([],[])[0])
        self.lines.append(self.axes[5].plot([],[])[0])
        self.axes[6].set_title('Helium Level')
        self.lines.append(self.axes[6].plot([],[])[0]) 
        plt.draw()
          
    def run(self):
        last_refresh = 0
        while True:  
            if self.quit_code:
                plt.close(self.fig)
                plt.pause(0.1)
                break
            if time.time()-last_refresh > self.refresh_time:
                self.refresh()
                last_refresh = time.time()
            time.sleep(0.1)
            
    def refresh(self):
        xmin = datetime.now().replace(microsecond=0) - timedelta(seconds=self.pressure_range)
        to_display = self.Pressure.x>xmin
        x = self.Pressure.x[to_display]
        y = self.Pressure.y[to_display,:]
        if np.sum(to_display)>1:
            for i,graph_name in enumerate(['PIVC','PB1K','PVAT','PHE3']):
                self.lines[i].set_xdata(x)
                self.lines[i].set_ydata(y[:,i+1])
                ymin = np.min(y[:,i+1])
                ymax = np.max(y[:,i+1])
                if (np.log10(ymax)-np.log10(ymin)) < 1.0: # min scale : 1 decade
                    margin = 0.5*(1.0-(np.log10(ymax)-np.log10(ymin)));
                else:
                    margin = 0.1;
                ymin = ymin * 10**(-margin)
                ymax = ymax * 10**(+margin)
                self.axes[i].set_ylim([ymin,ymax])
                self.axes[i].set_title(graph_name+' = '+format(self.Pressure.y[-1,i+1],'.3e')+' mbar')
            self.axes[0].set_xlim([np.min(x),np.max(x)])
            
        xmin = datetime.now().replace(microsecond=0) - timedelta(seconds=self.temperature_range)
        to_display = self.Temperature.x>xmin
        x = self.Temperature.x[to_display]
        y = self.Temperature.T[to_display,:]
        if np.sum(to_display)>1:
            self.lines[4].set_xdata(x)
            self.lines[4].set_ydata(y[:,1])
            ymin = np.min(y[:,1])
            ymax = np.max(y[:,1])
            self.axes[4].set_ylim([ymin,ymax])
            self.axes[4].set_title('TB1K = '+format(self.Temperature.T[-1,1],'.3f')+' K')
            
            self.lines[5].set_xdata(x)
            self.lines[5].set_ydata(y[:,2])
            ymin = np.min(y[:,2])
            ymax = np.max(y[:,2])
            self.axes[5].set_ylim([ymin,ymax])
            if self.Temperature.T[-1,2] < 1.0:
                self.axes[5].set_title('THE3 = '+format(self.Temperature.T[-1,2]*1000,'.1f')+' mK')
            else:
                self.axes[5].set_title('THE3 = '+format(self.Temperature.T[-1,2],'.3f')+' K')
            self.axes[4].set_xlim([np.min(x),np.max(x)])
            
        xmin = datetime.now().replace(microsecond=0) - timedelta(seconds=self.helevel_range)
        to_display = self.HeLevel.x>xmin
        x = self.HeLevel.x[to_display]
        y = self.HeLevel.y[to_display,:]
        if np.sum(to_display)>1:
            self.lines[6].set_xdata(x)
            self.lines[6].set_ydata(y[:,0])
            ymin = np.min(y[:,0])
            ymax = np.max(y[:,0])
            self.axes[6].set_xlim([np.min(x),np.max(x)])
            self.axes[6].set_ylim([ymin,ymax])
            self.axes[6].set_title('Helium Level = '+format(self.HeLevel.y[-1,0],'.1f')+'')
        
        plt.draw() # refresh the subplots
        plt.pause(self.refresh_time)
     
serial_port = 'COM4'
refresh_time = 5.0
store_time = 10.0
buffer_size = 20000.0
Pressure = PressureThread(serial_port,refresh_time,store_time,buffer_size)
Pressure.start()

ip_address = '192.168.1.100'
refresh_time = 5.0
store_time = 10.0
buffer_size = 20000.0
Temperature = TemperatureThread(ip_address,refresh_time,store_time,buffer_size)
Temperature.start()

#serial_port = 'COM3'
#heating_current = 0.15
#heating_time = 5
#meas_current= 0.1
#meas_time = 10
#normal_refresh= 7200.0
#transfer_refresh= 15.0
#store_time = 60.0
#buffer_size = 20000
#HeLevel = HeLevelThread(serial_port,heating_current,heating_time,meas_current,meas_time,normal_refresh,transfer_refresh,store_time,buffer_size)
#HeLevel.start()
#HeLevel.transfer_mode = True

#plt.ion()
#time.sleep(20)
#Plot = PlottingWindow(Pressure,Temperature,HeLevel,pressure_range=2*3600.0,temperature_range=2*3600.0,helevel_range=12*3600.0,refresh_time=5.0)
#Plot.start()

#Plot.pressure_range = 24*3600.0
#Plot.temperature_range = 24*3600.0
#Plot.helevel_range = 24*3600.0


#HeLevel.refresh()
#Plot.pressure_range = 15*60.0
#Plot.temperature_range = 15*60.0