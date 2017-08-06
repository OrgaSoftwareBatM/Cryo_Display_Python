# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 14:42:54 2017

@author: Baptiste
"""
import numpy as np
from datetime import datetime,timedelta
import sys,os
sys.path.append(os.getcwd()+'\Temperature')    # add the current file to Python path
sys.path.append(os.getcwd())    # add the current file to Python path
from mmr3 import MMR3 # to find mmr3.py
import pyqtgraph as pg
from pyqtgraph import QtGui,QtCore
from pyqtgraph.dockarea import DockArea,Dock
    
class Temperature_GUI(Dock):
    def __init__(self,
                 ip_address = '192.168.1.100',
                 refresh_time = 5.0,
                 store_time = 15.0, 
                 buffer_size = 20000.0,
                 store_folder = 'Temperature/data'
                 ):
        super(Temperature_GUI, self).__init__(name='Temperature') 

        self.addWidget(QtGui.QLabel('IP address'),0,0)
        self.ip_address = QtGui.QLineEdit(ip_address)
        self.addWidget(self.ip_address,0,1)
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
            self.mmr3 = MMR3(self.ip_address.text()) # Start communication with MMR3
            return 1
        except:
            print ('Was not able to open communication with IP '+self.ip_address.text())
            return 0
        
    def browse(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, 'Pick a Folder')
        if path:
            self.store_folder.setText(path)
        
    def refresh(self):
        try:
            newR = np.array([self.mmr3.chan1.R , self.mmr3.chan2.R , self.mmr3.chan3.R]) # get new values
        except:
            print('MMR3 timeout error')
            self.refresh_timer.start(self.refresh_time.value()*1000.)
            return 0
        newT = self.convert(newR)
        newline = []
        newline.append(datetime.now().replace(microsecond=0).timestamp())
        for i in range(3):
            newline.append(newR[i])
            newline.append(newT[i])
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
        for i in range(1,7): # add the resistances & temperatures
            str_line += ', '
            str_line += format(self.data[-1,i],'.3E')
        if not os.path.exists(self.store_folder.text()):
            print ('Store folder does not exist')
            return 0
        logfile = open(self.store_folder.text() + '/' + t.date().isoformat() + '-temperature.txt', 'a') # file to save the data
        logfile.write(str_line+'\n')
        logfile.flush()
        self.store_timer.start(self.store_time.value()*1000.)
        return 1
        
    def convert(self,R):
        cal_names = ['R25_table.tbl','R2_AB_Table_v2.txt','R25_table.tbl']
        cal_names = ['Temperature/'+cal_name for cal_name in cal_names]
        if not hasattr(self,'convert_tables'):  # not loaded yet
            self.convert_tables = []
            for cal_name in cal_names:
                if os.path.isfile(cal_name):
                    cal_file = open(cal_name)
                else:
                    print ('Could not open cal file')
                    return [0,0,0]
                cal = []
                for line in cal_file.readlines():
                    cal.append([float(elmt) for elmt in line.split('\t')])
                cal_file.close()
                self.convert_tables.append(np.array(cal))
                                
        T = np.zeros_like(R)
        for i,table in enumerate(self.convert_tables):
            T[i] = np.interp(abs(R[i]),table[:,1],table[:,0])
        return T   
    

class Main_Plot_Window(QtGui.QMainWindow):
    def __init__(self):
        super(Main_Plot_Window, self).__init__()
        self.area = DockArea()
        self.setCentralWidget(self.area)
        self.area.addDock(Temperature_GUI(store_folder='data'))

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