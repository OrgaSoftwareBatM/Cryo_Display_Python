# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 22:17:52 2017

@author: manip.batm
"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import DockArea,Dock
import sys,os
sys.path += [os.getcwd()+sub for sub in ['','\GUI','\Temperature','\Pressure','\HeLevel']]    # add the current file to Python path
from Plot_GUI import Plot_Dock,Option_For_All
from Pressure_GUI import Pressure_GUI
from Temperature_GUI import Temperature_GUI
from HeLevel_GUI import HeLevel_GUI


class Main_Plot_Window(QtGui.QMainWindow):
    def __init__(self):
        super(Main_Plot_Window, self).__init__()
        self.plot_area = DockArea()
        self.docks = []
        self.docks.append(Plot_Dock(parent=self,param='PIVC',loc='left',rel_to=None))
        self.docks.append(Plot_Dock(parent=self,param='PB1K',loc='bottom',rel_to=self.docks[-1]))
        self.docks.append(Plot_Dock(parent=self,param='PVAT',loc='bottom',rel_to=self.docks[-1]))
        self.docks.append(Plot_Dock(parent=self,param='PHE3',loc='bottom',rel_to=self.docks[-1]))
        self.docks.append(Plot_Dock(parent=self,param='T2',loc='right',rel_to=None))
        self.docks.append(Plot_Dock(parent=self,param='T3',loc='bottom',rel_to=self.docks[-1]))
        self.docks.append(Plot_Dock(parent=self,param='HeR',loc='bottom',rel_to=self.docks[-1]))
        for d in self.docks:
            self.plot_area.addDock(d,d.loc,d.rel_to)
<<<<<<< HEAD
=======
#        self.settings_dock = Dock('Settings', size=(1, 1))
>>>>>>> origin/master
        self.settings_dock = Option_For_All(parent=self)
        self.plot_area.addDock(self.settings_dock,'bottom',self.docks[-1])

        self.meas_area = DockArea()
        self.pressure_thread = Pressure_GUI(serial_port = 'COM4',
<<<<<<< HEAD
                                            refresh_time = 5.0,
=======
                                            refresh_time = 500.0,
>>>>>>> origin/master
                                            store_time = 1500.0, 
                                            buffer_size = 20000.0,
                                            store_folder = 'Pressure/data')
        self.meas_area.addDock(self.pressure_thread)
        self.temperature_thread = Temperature_GUI(ip_address = '192.168.1.100',
                                                  refresh_time = 5.0,
                                                  store_time = 15.0, 
                                                  buffer_size = 20000.0,
                                                  store_folder = 'Temperature/data')
<<<<<<< HEAD
        self.meas_area.addDock(self.temperature_thread,'bottom')
=======
        self.meas_area.addDock(self.temperature_thread,'right')
>>>>>>> origin/master
        self.helevel_thread = HeLevel_GUI(serial_port = 'COM3',
                                          heating_current = 0.15,
                                          heating_time = 5,
                                          meas_current= 0.1,
                                          meas_time = 10,
                                          normal_refresh= 7200.0,
                                          transfer_refresh= 15.0,
                                          store_time = 60.0,
                                          buffer_size = 20000,
                                          store_folder = 'HeLevel/data')
        self.meas_area.addDock(self.helevel_thread,'right')
<<<<<<< HEAD
        self.meas_area.addDock(Dock(name='empty',hideTitle=True),'right')
        self.meas_area.addDock(Dock(name='empty2',hideTitle=True),'bottom')
        
        self.pressure_thread.setOrientation(o='horizontal')
        self.temperature_thread.setOrientation(o='horizontal')
=======
>>>>>>> origin/master
        
        self.tab = QtGui.QTabWidget()
        self.tab.addTab(self.plot_area,'Plot')
        self.tab.addTab(self.meas_area,'Acquisition')
        self.setCentralWidget(self.tab)
        
## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    win = Main_Plot_Window()
#    print (win.addTab)
#    win.move(0,0)
#    win.showMaximized = True
    win.resize(1000,500)
    win.show()
    
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        print ('HEYYYYYYYYY')
        print (sys.flags.interactive)
        QtGui.QApplication.instance().exec_()