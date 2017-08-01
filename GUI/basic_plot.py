# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from matplotlib import lines
import threading
import datetime
import time
from datetime import datetime,timedelta
import numpy as np
from random import random

class PlotWindow():
    def __init__(self,xrange=60.0,refresh_time=1.0):
        self.xrange = xrange  # in sec
        self.refresh_time = refresh_time # in sec

        self.fig, self.axes = plt.subplots(nrows=4, ncols=2,figsize=(6,9),sharex=True) # create figure and subplots
        self.fig.tight_layout()
        self.lines = []
        for i,graph_name in enumerate(['PIVC','PB1K','PVAT','PHE3']):
            self.axes[i,0].set_title(graph_name)
            self.axes[i,0].set_yscale('log')
            self.axes[i,0].grid(True)
            self.axes[i,0].yaxis.set_tick_params(which='minor')
            self.lines.append(self.axes[i,0].plot([],[])[0])  
#        plt.draw()
            
    def refresh(self,Pressure,HeLevel):
        xmin = datetime.now().replace(microsecond=0) - timedelta(seconds=self.xrange)
        for i,graph_name in enumerate(['PIVC','PB1K','PVAT','PHE3']):
            to_display = Pressure.x>xmin
            self.lines[i].set_xdata(Pressure.x[to_display])
#            helper = np.vectorize(lambda x: x.seconds)
#            delta_t = helper(Pressure.x[to_display]-datetime.now())
#            self.lines[i].set_xdata(delta_t)
            self.lines[i].set_ydata(Pressure.y[to_display,i+1])
            self.axes[i,0].set_xlim([np.min(Pressure.x[to_display]),np.max(Pressure.x[to_display])])
#            self.axes[i,0].set_xlim([np.min(delta_t),np.max(delta_t)])
            self.axes[i,0].set_ylim([np.min(Pressure.y[to_display,i+1]),np.max(Pressure.y[to_display,i+1])])
            self.axes[i,0].set_title(graph_name+' = '+format(Pressure.y[-1,i+1],'.3e')+' mbar')
        plt.draw() # refresh the subplots
        
class SelfUpdatingArray(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.x = [datetime.now().replace(microsecond=0)]
        self.y = np.zeros((1,6))
        self.y[:] = [random() for i in range(6)]
        self.quit_code = False
    def run(self):
        last_refresh = 0
        while True:
            if self.quit_code:
                break
            if time.time()-last_refresh > 0.5:
                self.x = np.append(self.x,datetime.now().replace(microsecond=0))
                newy = np.zeros((1,6))
                newy[:] = [random() for i in range(6)]
                self.y = np.concatenate((self.y,newy),axis=0)
                last_refresh = time.time()
            time.sleep(0.1)
      
plt.ion()
a = SelfUpdatingArray()
a.start()
time.sleep(1)
Plot = PlotWindow()
last_refresh = 0
refresh_time = 1.0
k=0
while k<1000:  
    k += 1
    Plot.refresh(a,[])
    plt.draw()
    last_refresh = time.time()
    plt.pause(refresh_time)
