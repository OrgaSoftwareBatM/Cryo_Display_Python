# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 20:18:48 2017

@author: Baptiste
"""
import numpy as np
from datetime import datetime,timedelta
import time
import sys,os
sys.path.append(os.getcwd()+'\Pressure')    # add the current file to Python path
sys.path.append(os.getcwd())    # add the current file to Python path
from PfeifferVacuum import MaxiGauge, MaxiGaugeError # to find PfeifferVacuum.py
import pyqtgraph as pg
from pyqtgraph import QtGui,QtCore
from pyqtgraph.dockarea import DockArea,Dock
    
class Pressure_GUI(Dock):
    def __init__(self,
                 serial_port = 'COM4',
                 refresh_time = 5.0,
                 store_time = 15.0, 
                 buffer_size = 20000.0,
                 store_folder = 'Pressure/data'
                 ):
        super(Pressure_GUI, self).__init__(name='Pressure') 

        self.addWidget(QtGui.QLabel('Serial port'),0,0)
        self.serial_port = QtGui.QLineEdit(serial_port)
        self.addWidget(self.serial_port,0,1)
        btn = QtGui.QPushButton('Set')
        btn.clicked.connect(self.open_com)
        self.addWidget(btn,0,2)

        self.addWidget(QtGui.QLabel('Storage folder'),1,0)
        self.store_folder = QtGui.QLineEdit(store_folder)
        self.addWidget(self.store_folder,1,1)
        btn = QtGui.QPushButton('Change')
        btn.clicked.connect(self.browse)
        self.addWidget(btn,1,2)
        
        self.addWidget(QtGui.QLabel('Refresh time (s)'),2,0)
        self.refresh_time = pg.SpinBox(value=refresh_time, bounds=[1., None], step=1)
        self.addWidget(self.refresh_time,2,1)
        
        self.addWidget(QtGui.QLabel('Storage time (s)'),3,0)
        self.store_time = pg.SpinBox(value=store_time, bounds=[1., None], step=1)
        self.addWidget(self.store_time,3,1)
        
        self.addWidget(QtGui.QLabel('Buffer size'),4,0)
        self.buffer_size = pg.SpinBox(value=buffer_size, bounds=[1, None], int=True)
        self.addWidget(self.buffer_size,4,1)
        
        ### Open communication
        self.open_com()
        self.data = []
        
        ### Start the timers
        self.refresh_timer = QtCore.QTimer()
        self.refresh_timer.timeout.connect(self.refresh)
        self.refresh_timer.start(self.refresh_time.value()*1000.)
        
        self.store_timer = QtCore.QTimer()
        self.store_timer.timeout.connect(self.store)
        self.store_timer.start(self.store_time.value()*1000.)
      
    def open_com(self):
        try:
            self.gauge = MaxiGauge(self.serial_port) # Start communication with Serial port (RS232)
            self.gauge_names = self.gauge.send('CID',1) # ask for channel names
            self.gauge_names = self.gauge_names[0].split(',') # format the names in a list
            self.active_gauge = [sensor.status in [0,1,2] for sensor in self.gauge.pressures()] # update active gauges
            self.Ng = len(self.gauge_names)
            return 1
        except:
            print ('Was not able to open communication with port '+self.serial_port.text())
            return 0
        
    def browse(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, 'Pick a Folder')
        if path:
            self.store_folder.setText(path)
        
    def refresh(self):
        try:
            ps = self.gauge.pressures() # Read the new pressures
        except:
            print('Pressure readout error')
            self.refresh_timer.start(self.refresh_time.value()*1000.)
            return 0
        
        self.active_gauge = [sensor.status in [0,1,2] for sensor in self.gauge.pressures()] # update active gauges
        newline = []
        newline.append(datetime.now().replace(microsecond=0).timestamp())
        newline += [sensor.pressure if sensor.status in [0,1,2]  else np.NaN for sensor in ps] # get new values
        newline = np.array(newline).reshape((1,7))
            
        if len(self.data) == 0:    # first point
            self.data = newline
        else:   # add new line
            self.data = np.concatenate((self.data,newline),0)
            
        # remove extra points if buffer is full
        if len(self.data) > self.buffer_size.value():
            self.data = self.data[-self.buffer_size.value():,:]
            
        self.refresh_timer.start(self.refresh_time.value()*1000.)
        return 1
            
    def store(self):
        if len(self.data) == 0:
            print ('Buffer empty, could not store data')
            self.store_timer.start(self.store_time.value()*1000.)
            return 0
        t = datetime.fromtimestamp(self.data[-1,0])
        str_line = t.isoformat(' ') # build string with date and time
        for i in range(1,7): # add every pressure
            str_line += ', '
            str_line += format(self.data[-1,i],'.3E')
        if not os.path.exists(self.store_folder.text()):
            print ('Store folder does not exist')
            return 0
        logfile = open(self.store_folder.text() + '/' + t.date().isoformat() + '-pressures.txt', 'a') # file to save the data
        logfile.write(str_line+'\n')
        logfile.flush()
        self.store_timer.start(self.store_time.value()*1000.)
        return 1
    

class Main_Plot_Window(QtGui.QMainWindow):
    def __init__(self):
        super(Main_Plot_Window, self).__init__()
        self.area = DockArea()
        self.setCentralWidget(self.area)
        self.area.addDock(Pressure_GUI(store_folder='data'))

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    win = Main_Plot_Window()
#    win.move(0,0)
#    win.showMaximized = True
#    win.resize(1000,500)
    win.show()
    
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        print ('HEYYYYYYYYY')
        print (sys.flags.interactive)
        QtGui.QApplication.instance().exec_()