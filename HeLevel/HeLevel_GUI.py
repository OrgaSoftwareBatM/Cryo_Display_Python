# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 19:07:06 2017

@author: Baptiste
"""
import numpy as np
from datetime import datetime,timedelta
import time
import sys,os
sys.path.append(os.getcwd()+'\HeLevel')    # add the current file to Python path
sys.path.append(os.getcwd())    # add the current file to Python path
import pyvisa
import pyqtgraph as pg
from pyqtgraph import QtGui,QtCore
from pyqtgraph.dockarea import DockArea,Dock
    
class HeLevel_GUI(Dock):
    def __init__(self,
                 serial_port = 'COM3',
                 heating_current = 0.15,
                 heating_time = 5,
                 meas_current= 0.1,
                 meas_time = 10,
                 normal_refresh= 7200.0,
                 transfer_refresh= 15.0,
                 store_time = 60.0,
                 buffer_size = 20000,
                 store_folder = 'HeLevel/data',
                 ):
        super(HeLevel_GUI, self).__init__(name='HeLevel') 

<<<<<<< HEAD
        self.addWidget(QtGui.QLabel('Serial port'),1,1)
        self.serial_port = QtGui.QLineEdit(serial_port)
        self.addWidget(self.serial_port,1,2)
        btn = QtGui.QPushButton('Connect')
        btn.clicked.connect(self.open_com)
        self.addWidget(btn,1,3)

        self.addWidget(QtGui.QLabel('Storage folder'),2,1)
        self.store_folder = QtGui.QLineEdit(store_folder)
        self.addWidget(self.store_folder,2,2)
        btn = QtGui.QPushButton('Change')
        btn.clicked.connect(self.browse)
        self.addWidget(btn,2,3)
        
        self.addWidget(QtGui.QLabel('Heating current (A)'),3,1)
        self.heating_current = pg.SpinBox(value=heating_current, bounds=[0., 0.8], step=0.01)
        self.addWidget(self.heating_current,3,2)
        
        self.addWidget(QtGui.QLabel('Heating time (s)'),4,1)
        self.heating_time = pg.SpinBox(value=heating_time, bounds=[0., None], step=1)
        self.addWidget(self.heating_time,4,2)
        
        self.addWidget(QtGui.QLabel('Measure current (A)'),5,1)
        self.meas_current = pg.SpinBox(value=meas_current, bounds=[0., 0.8], step=0.01)
        self.addWidget(self.meas_current,5,2)
        
        self.addWidget(QtGui.QLabel('Measure time (s)'),6,1)
        self.meas_time = pg.SpinBox(value=meas_time, bounds=[0., None], step=1)
        self.addWidget(self.meas_time,6,2)
        
        self.addWidget(QtGui.QLabel('Normal refresh (s)'),7,1)
        self.normal_refresh = pg.SpinBox(value=normal_refresh, bounds=[1., None], step=1)
        self.addWidget(self.normal_refresh,7,2)
        
        self.addWidget(QtGui.QLabel('Transfer mode refresh (s)'),8,1)
        self.transfer_refresh = pg.SpinBox(value=transfer_refresh, bounds=[1., None], step=1)
        self.addWidget(self.transfer_refresh,8,2)
        
        self.addWidget(QtGui.QLabel('Storage time (s)'),9,1)
        self.store_time = pg.SpinBox(value=store_time, bounds=[1., None], step=1)
        self.addWidget(self.store_time,9,2)
        
        self.addWidget(QtGui.QLabel('Buffer size'),10,1)
        self.buffer_size = pg.SpinBox(value=buffer_size, bounds=[1, None], int=True)
        self.addWidget(self.buffer_size,10,2)
=======
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
        
        self.addWidget(QtGui.QLabel('Heating current (A)'),2,0)
        self.heating_current = pg.SpinBox(value=heating_current, bounds=[0., 0.8], step=0.01)
        self.addWidget(self.heating_current,2,1)
        
        self.addWidget(QtGui.QLabel('Heating time (s)'),3,0)
        self.heating_time = pg.SpinBox(value=heating_time, bounds=[0., None], step=1)
        self.addWidget(self.heating_time,3,1)
        
        self.addWidget(QtGui.QLabel('Measure current (A)'),4,0)
        self.meas_current = pg.SpinBox(value=meas_current, bounds=[0., 0.8], step=0.01)
        self.addWidget(self.meas_current,4,1)
        
        self.addWidget(QtGui.QLabel('Measure time (s)'),5,0)
        self.meas_time = pg.SpinBox(value=meas_time, bounds=[0., None], step=1)
        self.addWidget(self.meas_time,5,1)
        
        self.addWidget(QtGui.QLabel('Normal refresh (s)'),6,0)
        self.normal_refresh = pg.SpinBox(value=normal_refresh, bounds=[1., None], step=1)
        self.addWidget(self.normal_refresh,6,1)
        
        self.addWidget(QtGui.QLabel('Transfer mode refresh (s)'),7,0)
        self.transfer_refresh = pg.SpinBox(value=transfer_refresh, bounds=[1., None], step=1)
        self.addWidget(self.transfer_refresh,7,1)
        
        self.addWidget(QtGui.QLabel('Storage time (s)'),8,0)
        self.store_time = pg.SpinBox(value=store_time, bounds=[1., None], step=1)
        self.addWidget(self.store_time,8,1)
        
        self.addWidget(QtGui.QLabel('Buffer size'),9,0)
        self.buffer_size = pg.SpinBox(value=buffer_size, bounds=[1, None], int=True)
        self.addWidget(self.buffer_size,9,1)
>>>>>>> origin/master
        
        self.tm_btn = QtGui.QPushButton('Transfer mode OFF')
        self.tm_btn.setCheckable(True)
        self.tm_btn.clicked[bool].connect(self.toggle_tm)
<<<<<<< HEAD
        self.addWidget(self.tm_btn,11,1)
=======
        self.addWidget(self.tm_btn,10,1)
>>>>>>> origin/master
        self.transfer_mode = False
        
        btn = QtGui.QPushButton('Refresh')
        btn.clicked.connect(self.refresh)
<<<<<<< HEAD
        self.addWidget(btn,11,3)
        
        self.layout.setColumnMinimumWidth(0,20)
        self.layout.setColumnMinimumWidth(4,20)   
        self.layout.setRowMinimumHeight(0,20)
        self.layout.setRowMinimumHeight(13,20)
        self.layout.setSpacing(20.)
=======
        self.addWidget(btn,11,1)
>>>>>>> origin/master
        
        ### Open communication
        self.open_com()
        self.data = []

        ### Start the timers
        self.refresh_timer = QtCore.QTimer()
        self.refresh_timer.timeout.connect(self.refresh)
        self.refresh_timer.start(self.normal_refresh.value()*1000.)
        
        self.refresh()
                
        self.store_timer = QtCore.QTimer()
        self.store_timer.timeout.connect(self.store)
        self.store_timer.start(self.store_time.value()*1000.)
      
    def open_com(self):
        try:
            rm = pyvisa.ResourceManager()
            self.device = rm.open_resource(self.serial_port.text())
            self.device.write('VOLT:RANG LOW')
            return 1
        except:
            print ('Was not able to open communication with port '+self.serial_port.text())
            return 0
        
    def browse(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, 'Pick a Folder')
        if path:
            self.store_folder.setText(path)
            
    def toggle_tm(self,order):
<<<<<<< HEAD
        if order:   # turn on TM  
            self.transfer_mode = True
            self.tm_btn.setText('Transfer mode ON')
            if self.heating_current.value() > 0:
                self.heating_pulse()
            else:
                self.meas_pulse()
        else:   # turn off TM
            self.transfer_mode = False
            self.tm_btn.setText('Transfer mode OFF')
            self.read_point()
    
    def heating_pulse(self):
        self.device.write('CURR '+str(self.heating_current.value()))
        self.device.write('OUTP ON')
        self.temp_timer = QtCore.QTimer.singleShot(self.heating_time.value()*1000.,self.meas_pulse)
    
    def meas_pulse(self):
        self.device.write('CURR '+str(self.meas_current.value()))
        self.device.write('OUTP ON')
        self.temp_timer = QtCore.QTimer.singleShot(self.meas_time.value()*1000.,self.read_point)
        
    def refresh(self):
        try:
            if self.transfer_mode:  # permanent mode
                self.read_point()
            elif self.heating_current.value() > 0:  # heating then meas pulse
                self.heating_pulse()
            else:
                self.meas_pulse()
=======
        self.tm_btn.setText('Transfer mode --')
        self.tm_btn.repaint()
        if order:   # turn on TM
            if self.heating_current.value() > 0:
                self.device.write('CURR '+str(self.heating_current.value()))
                self.device.write('OUTP ON')
                time.sleep(self.heating_time.value())
            self.device.write('CURR '+str(self.meas_current.value()))
            time.sleep(self.meas_time.value())   
            self.transfer_mode = True
            self.tm_btn.setText('Transfer mode ON')
            self.refresh()
        else:   # turn off TM
            self.device.write('OUTP OFF') 
            self.transfer_mode = False
            self.refresh_timer.stop()
            self.refresh_timer.start(self.normal_refresh.value()*1000.)
            self.tm_btn.setText('Transfer mode OFF')
        
    def refresh(self):
        try:
            if self.transfer_mode:
                Vread = self.device.query('MEAS:VOLT?') 
            else:
                if self.heating_current.value() > 0:
                    self.device.write('CURR '+str(self.heating_current.value()))
                    self.device.write('OUTP ON')
                    time.sleep(self.heating_time.value())
                self.device.write('CURR '+str(self.meas_current.value()))
                time.sleep(self.meas_time.value())   
                Vread = self.device.query('MEAS:VOLT?') 
                self.device.write('OUTP OFF')
>>>>>>> origin/master
        except:
            print('Device timeout error')
            self.refresh_timer.start(self.normal_refresh.value()*1000.)
            return 0
        
<<<<<<< HEAD
    def read_point(self):
        try:
            Vread = self.device.query('MEAS:VOLT?') 
            if not self.transfer_mode:
                self.device.write('OUTP OFF')
        except:
            print('Could not get helevel point')
            return 0
=======
>>>>>>> origin/master
        newR = float(Vread)/self.meas_current.value()
        hours_left = self.convert(newR)
        newline = []
        newline.append(datetime.now().replace(microsecond=0).timestamp())
        newline.append(newR)
        newline.append(hours_left)
        newline = np.array(newline).reshape((1,3))
            
        if len(self.data) == 0:    # first point
            self.data = newline
        else:   # add new line
            self.data = np.concatenate((self.data,newline),0)
            
        # remove extra points if buffer is full
        if len(self.data) > self.buffer_size.value():
            self.data = self.data[-self.buffer_size.value():,:]
        
        if self.transfer_mode:
            self.refresh_timer.start(self.transfer_refresh.value()*1000.)
        else:
            self.refresh_timer.start(self.normal_refresh.value()*1000.)
        return 1
            
    def store(self):
        if len(self.data) == 0:
            print ('Buffer empty, could not store data')
            self.store_timer.start(self.store_time.value()*1000.)
            return 0
        t = datetime.fromtimestamp(self.data[-1,0])
        str_line = t.isoformat(' ') # build string with date and time
        for i in range(1,3): # add the resistance & hoursleft
            str_line += ', '
            str_line += format(self.data[-1,i],'.3f')
        if not os.path.exists(self.store_folder.text()):
            print ('Store folder does not exist')
            return 0
        logfile = open(self.store_folder.text() + '/' + t.date().isoformat() + '-helevel.txt', 'a') # file to save the data
        logfile.write(str_line+'\n')
        logfile.flush()
        self.store_timer.start(self.store_time.value()*1000.)
        return 1
        
    def convert(self,R):
        cal_name = 'HeLevel/etal_helevel.txt'
#        cal_name = 'etal_helevel.txt'
        if not hasattr(self,'convert_table'):  # not loaded yet
            self.convert_table = []
            if os.path.isfile(cal_name):
                cal_file = open(cal_name)
            else:
                print ('Could not open cal file')
                return [0]
            cal = []
            for line in cal_file.readlines():
                cal.append([float(elmt) for elmt in line.split('\t')])
            cal_file.close()
            self.convert_table = np.array(cal)
                                
        hoursleft = np.interp(R,self.convert_table[:,0],self.convert_table[:,1])
        return hoursleft  
    

class Main_Plot_Window(QtGui.QMainWindow):
    def __init__(self):
        super(Main_Plot_Window, self).__init__()
        self.area = DockArea()
        self.setCentralWidget(self.area)
        self.dock = HeLevel_GUI(store_folder='data')
        self.area.addDock(self.dock)

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