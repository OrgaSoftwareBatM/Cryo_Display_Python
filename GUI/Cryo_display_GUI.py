# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 10:12:10 2017

@author: baptiste.jadot
"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import DockArea,Dock
import numpy as np
from datetime import datetime,timedelta
import time

class TimeAxisItem(pg.AxisItem):
### since datetime elements are not supported by pyqtgraph,
### we use the timestamp (float) as x axis and set a custom xticklabel
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime('%H:%M') for value in values]
    
param_dict = {}
param_dict['P1'] = ['Pressure.y[:,0]','P<sub>1</sub> = {:.3e} mbar']
param_dict['PIVC'] = ['Pressure.y[:,1]','P<sub>IVC</sub> = {:.3e} mbar']
param_dict['PB1K'] = ['Pressure.y[:,2]','P<sub>B1K</sub> = {:.3e} mbar']
param_dict['PVAT'] = ['Pressure.y[:,3]','P<sub>VAT</sub> = {:.3e} mbar']
param_dict['PHE3'] = ['Pressure.y[:,4]','P<sub>HE3</sub> = {:.3e} mbar']
param_dict['P6'] = ['Pressure.y[:,5]','P<sub>6</sub> = {:.3e} mbar']
param_dict['T1'] = ['Temperature.T[:,0]','T<sub>1</sub> = {:.3f} K']
param_dict['T2'] = ['Temperature.T[:,1]','T<sub>2</sub> = {:.3f} K']
param_dict['T3'] = ['Temperature.T[:,2]','T<sub>3</sub> = {:.3f} K']
param_dict['HeR'] = ['HeLevel.y[:,0]','HeLevel = {:.1f} &Omega;']
param_dict['He%'] = ['HeLevel.y[:,1]','HeLevel = {:.1f} %']

param_keys = list(param_dict.keys())

class Option_widget(QtGui.QDialog):
    def __init__(self,parent=None):
        super(Option_widget, self).__init__()
        self.parent = parent
        main_ly = QtGui.QGridLayout()
        
        main_ly.addWidget(QtGui.QLabel('Param'),0,0)
        self.param_w = pg.QtGui.QComboBox()
        self.param_w.addItems(param_keys)
        self.param_w.setCurrentIndex(param_keys.index(self.parent.name))
        main_ly.addWidget(self.param_w,0,1,1,2)
        
        main_ly.addWidget(QtGui.QLabel('Xrange'),1,0)
        self.xrange_val = pg.SpinBox(value=1.0, bounds=[0, None])
#        self.xrange_val.setFixedWidth(80)
        main_ly.addWidget(self.xrange_val,1,1)
        self.xrange_unit = pg.QtGui.QComboBox()
        self.xrange_unit.addItems(['sec','min','hours','days'])
        self.xrange_unit.setCurrentIndex(2)
        main_ly.addWidget(self.xrange_unit,1,2)   
        
        main_ly.addWidget(QtGui.QLabel('Refresh'),2,0)
        self.refresh_rate = pg.SpinBox(value=1., bounds=[0, None])
        main_ly.addWidget(self.refresh_rate,2,1)
        main_ly.addWidget(QtGui.QLabel('sec'),2,2)
        
        main_ly.addWidget(QtGui.QLabel('Add data from'),3,0)
        self.nfiles = pg.SpinBox(value=1, bounds=[0, None])
        main_ly.addWidget(self.nfiles,3,1)
        main_ly.addWidget(QtGui.QLabel('past days'),3,2)

        self.okBtn = QtGui.QPushButton('OK',self)
        self.okBtn.clicked.connect(self.set_param)
        main_ly.addWidget(self.okBtn,5,1)
        self.setLayout(main_ly)
        
    def set_param(self):
        if self.parent.name != self.param_w.currentText():
            self.parent.change_param(self.param_w.currentText())
        unit = self.xrange_unit.currentText()
        if unit=='sec':
            self.parent.xrange = int(self.xrange_val.value())
        elif unit=='min':
            self.parent.xrange = int(self.xrange_val.value()*60)
        elif unit=='hours':
            self.parent.xrange = int(self.xrange_val.value()*3600)
        elif unit=='days':
            self.parent.xrange = int(self.xrange_val.value()*3600*24)
        else:
            print('Error : unknown xrange unit : '+unit)
        self.parent.refresh_rate = self.refresh_rate.value()  
        self.parent.nfiles = int(self.nfiles.value())
        self.parent.refresh_plot()
        self.close()
    
class Plot_dock():
    def __init__(self,
                 name='Dock',
                 loc='left',
                 rel_to=None,
                 refresh_rate = 1.,
                 nfiles = 0.,
                 xrange = 3600,
                 ):
        self.loc = loc
        self.rel_to = rel_to
        self.refresh_rate = refresh_rate
        self.nfiles = nfiles
        self.xrange = xrange
        
        self.name = name
        if name not in param_dict.keys():
            print ('Unknow source of data : '+name)
            return
        self.source = param_dict[name][0]
        self.title_format = param_dict[name][1]
        
        self.dock = Dock(self.name, size=(1, 1))
        self.wplot = pg.PlotWidget(title=self.name,axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.curve = self.wplot.plot([],[])
        self.dock.addWidget(self.wplot,0,0,10,10)
        
        self.optbtn = QtGui.QPushButton('Options')
        self.optbtn.clicked.connect(self.optfunc)
        self.toto=self.dock.addWidget(self.optbtn,0,9)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh_plot)
        self.timer.start(self.refresh_rate*1000.)
    
        self.refresh_plot()
        
    def refresh_plot(self):
        x,y = self.get_data()
        self.curve.setData(x,y)
        self.wplot.setTitle(self.title_format.format(y[-1]))
        self.timer.start(self.refresh_rate*1000.)
    
    def get_data(self):
        t = np.linspace(-1.,0,101)
        x = np.array([(datetime.now()+timedelta(hours=ti)).timestamp() for ti in t])
        y = np.random.normal(size=101)
        
        xmin = (datetime.now()-timedelta(seconds=self.xrange)).timestamp()
        to_display = x>xmin
        x = x[to_display]
        y = y[to_display]
        return x,y
    
    def change_param(self,newname):
        if newname not in param_dict.keys():
            print ('Unknow source of data : '+newname)
            return
        self.name = newname
        self.source = param_dict[newname][0]
        self.title_format = param_dict[newname][1]
        self.dock.setTitle(newname)
    
    def optfunc(self):
        print ('Options')
        if not hasattr(self, 'ow'):
            self.ow = Option_widget(parent = self)
            self.ow.setWindowTitle(self.name + ' - Options')
        self.ow.show()
        
            
class Option_for_all(QtGui.QWidget):
    def __init__(self,area=None,docks=None):
        super(Option_for_all, self).__init__()
        self.area = area
        self.docks = docks
    
        main_ly = QtGui.QGridLayout()
        
        main_ly.addWidget(QtGui.QLabel('Xrange'),1,0)
        self.xrange_val = pg.SpinBox(value=1.0, bounds=[0, None])
#        self.xrange_val.setFixedWidth(80)
        main_ly.addWidget(self.xrange_val,1,1)
        self.xrange_unit = pg.QtGui.QComboBox()
        self.xrange_unit.addItems(['sec','min','hours','days'])
        self.xrange_unit.setCurrentIndex(2)
        main_ly.addWidget(self.xrange_unit,1,2)   
        
        main_ly.addWidget(QtGui.QLabel('Refresh'),2,0)
        self.refresh_rate = pg.SpinBox(value=15.0, bounds=[0, None])
        main_ly.addWidget(self.refresh_rate,2,1)
        main_ly.addWidget(QtGui.QLabel('sec'),2,2)
        
        main_ly.addWidget(QtGui.QLabel('Add data from'),3,0)
        self.nfiles = pg.SpinBox(value=1, bounds=[0, None])
        main_ly.addWidget(self.nfiles,3,1)
        main_ly.addWidget(QtGui.QLabel('past days'),3,2)

        self.okBtn = QtGui.QPushButton('Set for all',self)
        self.okBtn.clicked.connect(self.set_param)
        main_ly.addWidget(self.okBtn,4,1)

        self.addBtn = QtGui.QPushButton('Add dock',self)
        self.addBtn.clicked.connect(self.add_dock)
        main_ly.addWidget(self.addBtn,4,2)
        
        hly = QtGui.QHBoxLayout()       
        hly.addStretch()
        hly.addLayout(main_ly)
        hly.addStretch()
        self.setLayout(hly)
        
    def set_param(self):
        unit = self.xrange_unit.currentText()
        if unit=='sec':
            xrange = int(self.xrange_val.value())
        elif unit=='min':
            xrange = int(self.xrange_val.value()*60)
        elif unit=='hours':
            xrange = int(self.xrange_val.value()*3600)
        elif unit=='days':
            xrange = int(self.xrange_val.value()*3600*24)
        else:
            print('Error : unknown xrange unit : '+unit)
        refresh_rate = self.refresh_rate.value()  
        nfiles = int(self.nfiles.value())
        for d in docks:
            d.xrange = xrange
            d.refresh_rate = refresh_rate
            d.nfiles = nfiles
            d.refresh_plot()
            
    def add_dock(self):
        newdock = Plot_dock(name='PIVC',loc='bottom',rel_to=self.docks[-1].dock)
        self.docks.append(newdock)
        self.area.addDock(newdock.dock)
         

    
app = QtGui.QApplication([])
win = QtGui.QMainWindow()
area = DockArea()
win.setCentralWidget(area)
win.resize(1000,500)
win.setWindowTitle('Cryo Display')

docks = []
docks.append(Plot_dock(name='PIVC',loc='left',rel_to=None))
docks.append(Plot_dock(name='PB1K',loc='bottom',rel_to=docks[-1].dock))
docks.append(Plot_dock(name='PVAT',loc='bottom',rel_to=docks[-1].dock))
docks.append(Plot_dock(name='PHE3',loc='bottom',rel_to=docks[-1].dock))
docks.append(Plot_dock(name='T2',loc='right',rel_to=None))
docks.append(Plot_dock(name='T3',loc='bottom',rel_to=docks[-1].dock))
docks.append(Plot_dock(name='HeR',loc='bottom',rel_to=docks[-1].dock))

for d in docks:
    area.addDock(d.dock,d.loc,d.rel_to)

settings_dock = Dock('Settings', size=(1, 1))
settings_dock.addWidget(Option_for_all(area=area,docks=docks))
area.addDock(settings_dock,'bottom',docks[-1].dock)

win.show()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        print ('HEYYYYYYYYY')
        print (sys.flags.interactive)
        QtGui.QApplication.instance().exec_()
        

