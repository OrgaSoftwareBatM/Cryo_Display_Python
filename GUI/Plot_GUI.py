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
<<<<<<< HEAD
#        font = QtGui.QFont('toto',pointSize = 12.)
#        self.setTickFont(font)
        pen = pg.mkPen(width=1.5) 
        self.setPen(pen)
=======
>>>>>>> origin/master

    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime('%H:%M') for value in values]
    
<<<<<<< HEAD
class YAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        font = QtGui.QFont('toto',pointSize = 12)
#        self.setTickFont(font)
#        self.setStyle(tickTextOffset=12)
        pen = pg.mkPen(width=1.5) 
        self.setPen(pen)
        self.setStyle(tickTextWidth=30)
        self.setStyle(tickTextHeight=20)
#        self.setWidth(30)
#        self.setHeight(12)

    
param_dict = {}
param_dict['P1'] = ['Pressure',1,'P1 = {:.3e} mbar']
param_dict['PIVC'] = ['Pressure',2,'PIVC = {:.3e} mbar']
param_dict['PB1K'] = ['Pressure',3,'PB1K = {:.3e} mbar']
param_dict['PVAT'] = ['Pressure',4,'PVAT = {:.3e} mbar']
param_dict['PHE3'] = ['Pressure',5,'PHE3 = {:.3e} mbar']
param_dict['P6'] = ['Pressure',6,'P6 = {:.3e} mbar']
param_dict['T1'] = ['Temperature',2,'T1 = {:.3f} K']
param_dict['T2'] = ['Temperature',4,'T2 = {:.3f} K']
param_dict['T3'] = ['Temperature',6,'T3 = {:.3f} K']
=======
param_dict = {}
param_dict['P1'] = ['Pressure',1,'P<sub>1</sub> = {:.3e} mbar']
param_dict['PIVC'] = ['Pressure',2,'P<sub>IVC</sub> = {:.3e} mbar']
param_dict['PB1K'] = ['Pressure',3,'P<sub>B1K</sub> = {:.3e} mbar']
param_dict['PVAT'] = ['Pressure',4,'P<sub>VAT</sub> = {:.3e} mbar']
param_dict['PHE3'] = ['Pressure',5,'P<sub>HE3</sub> = {:.3e} mbar']
param_dict['P6'] = ['Pressure',6,'P<sub>6</sub> = {:.3e} mbar']
param_dict['T1'] = ['Temperature',2,'T<sub>1</sub> = {:.3f} K']
param_dict['T2'] = ['Temperature',4,'T<sub>2</sub> = {:.3f} K']
param_dict['T3'] = ['Temperature',6,'T<sub>3</sub> = {:.3f} K']
>>>>>>> origin/master
param_dict['HeR'] = ['HeLevel',1,'HeLevel = {:.1f} &Omega;']
param_dict['He%'] = ['HeLevel',2,'HeLevel = {:.1f} %']

param_keys = list(param_dict.keys())

class Plot_Dock(Dock):
    def __init__(self,
                 parent = None,
                 param='Dock',
                 loc='left',
                 rel_to=None,
<<<<<<< HEAD
                 refresh_rate = 5.,
                 use_files = False,
=======
                 refresh_rate = 1.,
                 nfiles = 0.,
>>>>>>> origin/master
                 xrange = 3600,
                 ):
        super(Plot_Dock, self).__init__(name=param,size=(1,1))
        self.param = param
        self.parent = parent
        self.loc = loc
        self.rel_to = rel_to
        self.refresh_rate = refresh_rate
<<<<<<< HEAD
        self.use_files = use_files
=======
        self.nfiles = nfiles
>>>>>>> origin/master
        self.xrange = xrange
        
        if param not in param_dict.keys():
            print ('Unknow source of data : '+param)
            return
        self.type = param_dict[param][0]
        self.col = param_dict[param][1]
        self.title_format = param_dict[param][2]
        
<<<<<<< HEAD
        self.wplot = pg.PlotWidget(title=self.param,axisItems={'bottom': TimeAxisItem(orientation='bottom'),'left': YAxisItem(orientation='left')})
#        self.wplot.updateQtGui.QFont(pointSize = 20.) 
        self.wplot.setTitle('<font size=10>'+self.title_format.format(0.)+'</font>')
        pen = pg.mkPen(width=2)
        self.curve = self.wplot.plot([datetime.now().timestamp()-3600.,datetime.now().timestamp()],[1.,1.],pen=pen) # init graph with dummy data
        if self.type == 'Pressure':
            self.wplot.setLogMode(y=True)
=======
        self.wplot = pg.PlotWidget(title=self.param,axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.curve = self.wplot.plot([datetime.now().timestamp()-3600.,datetime.now().timestamp()],[0.,0.]) # init graph with dummy data
>>>>>>> origin/master
        self.addWidget(self.wplot,0,0,10,10)
        
        self.optbtn = QtGui.QPushButton('Options')
        self.optbtn.clicked.connect(self.optfunc)
        self.toto=self.addWidget(self.optbtn,0,9)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh_plot)
        self.timer.start(self.refresh_rate*1000.)
<<<<<<< HEAD
        
        self.ow = Option_Widget(parent = self)
        self.ow.setWindowTitle(self.param + ' - Options')
        self.ow.setFixedSize(self.ow.minimumSize())
            
=======
    
>>>>>>> origin/master
        self.refresh_plot()
        
    def refresh_plot(self):
        x,y = self.get_data()
<<<<<<< HEAD
#        print (len(x),len(y))
        if len(x) == 0 or len(y) == 0:
            self.timer.start(self.refresh_rate*1000.)
            return 0
        elif len(x) != len(y):
            self.timer.start(self.refresh_rate*1000.)
            return 0
        else:
            self.curve.setData(x,y)
            self.wplot.setTitle('<font size=10>'+self.title_format.format(y[-1])+'</font>')
        self.timer.start(self.refresh_rate*1000.)
        return 1
=======
        print (len(x),len(y))
        if len(x) == 0 or len(y) == 0:
            print ('got empty data to plot')
        elif len(x) != len(y):
            print ('got data with different dimensions to plot')
        else:
            print ('cas3')
            self.curve.setData(x,y)
            self.wplot.setTitle(self.title_format.format(y[-1]))
#            self.wplot.update()
        self.timer.start(self.refresh_rate*1000.)
>>>>>>> origin/master
    
    def get_data(self):
        try:
            if self.type =='Pressure':
                x = self.parent.pressure_thread.data[:,0]
                y = self.parent.pressure_thread.data[:,self.col]
            elif self.type =='Temperature':
                x = self.parent.temperature_thread.data[:,0]
                y = self.parent.temperature_thread.data[:,self.col]
            elif self.type =='HeLevel':
                x = self.parent.helevel_thread.data[:,0]
                y = self.parent.helevel_thread.data[:,self.col]
        except:
#            t = np.linspace(-1.,0,101)
#            x = np.array([(datetime.now()+timedelta(hours=ti)).timestamp() for ti in t])
#            y = np.random.normal(size=101)
#            return x,y
            return [],[]
        xmin = (datetime.now()-timedelta(seconds=self.xrange)).timestamp()
<<<<<<< HEAD
        xmin_buffer = np.min(x)
        if xmin_buffer < xmin:  # data needs to be truncated
            to_display = x>xmin
            x = x[to_display]
            y = y[to_display]
        elif self.use_files:      # data needs to be completed with file
            try:
                to_display = np.logical_and(self.saved_data[:,0]>xmin,self.saved_data[:,0]<xmin_buffer)
                x = np.concatenate((self.saved_data[to_display,0],x))
                y = np.concatenate((self.saved_data[to_display,1],y))
            except:
                print ('Error : no saved data has been loaded')
        return x,y
        
    def load_data_from_file(self,xmin,xmax):
        dates = [datetime.fromtimestamp(xmin).date()]
        while datetime.fromtimestamp(xmax).date() not in dates:
            dates.append(dates[-1]+timedelta(days=1))
        if self.type =='Pressure':
            folder = self.parent.pressure_thread.store_folder.text()
            filenames = [folder + '/' + date.isoformat() + '-pressures.txt' for date in dates]
        elif self.type =='Temperature':
            folder = self.parent.temperature_thread.store_folder.text()
            filenames = [folder + '/' + date.isoformat() + '-temperature.txt' for date in dates]
        elif self.type =='HeLevel':
            folder = self.parent.helevel_thread.store_folder.text()
            filenames = [folder + '/' + date.isoformat() + '-helevel.txt' for date in dates]
        else:
            print ('Type not understood')
            return []
        
        x = []
        y = []
        for filename in filenames:
            try:
                f = open(filename,'r')
                for line in f.readlines():
                    t = datetime.strptime(line.split(', ')[0],'%Y-%m-%d %H:%M:%S')
                    x.append(t.timestamp())
                    y.append(float(line.split(', ')[self.col]))
            except:
                print ('Could not load from '+filename)
        return np.array([x,y]).T
=======
        to_display = x>xmin
        x = x[to_display]
        y = y[to_display]
        return x,y
>>>>>>> origin/master
    
    def change_param(self,newparam):
        if newparam not in param_dict.keys():
            print ('Unknow source of data : '+newparam)
            return
        self.param = newparam
        self.type = param_dict[newparam][0]
        self.col = param_dict[newparam][1]
        self.title_format = param_dict[newparam][2]
        self.setTitle(newparam)
    
    def optfunc(self):
<<<<<<< HEAD
        if not hasattr(self, 'ow'):
            self.ow = Option_Widget(parent = self)
            self.ow.setWindowTitle(self.param + ' - Options')
            self.ow.setFixedSize(self.ow.minimumSize())
=======
        print ('Options')
        if not hasattr(self, 'ow'):
            self.ow = Option_Widget(parent = self)
            self.ow.setWindowTitle(self.param + ' - Options')
>>>>>>> origin/master
        self.ow.show()

class Option_Widget(QtGui.QDialog):
    def __init__(self,parent=None):
        super(Option_Widget, self).__init__() 
        self.parent = parent
<<<<<<< HEAD
        
        grid_ly = QtGui.QGridLayout()
        
        grid_ly.addWidget(QtGui.QLabel('Param'),1,1)
        self.param_w = pg.QtGui.QComboBox()
        self.param_w.addItems(param_keys)
        self.param_w.setCurrentIndex(param_keys.index(self.parent.param))
        grid_ly.addWidget(self.param_w,1,2)
        
        grid_ly.addWidget(QtGui.QLabel('Xrange'),2,1)
        self.xrange_val = pg.SpinBox(value=self.parent.xrange/3600., bounds=[0, None])
        grid_ly.addWidget(self.xrange_val,2,2)
        self.xrange_unit = pg.QtGui.QComboBox()
        self.xrange_unit.addItems(['sec','min','hours','days'])
        self.xrange_unit.setCurrentIndex(2)
        grid_ly.addWidget(self.xrange_unit,2,3)   
        
        grid_ly.addWidget(QtGui.QLabel('Refresh (s)'),3,1)
        self.refresh_rate = pg.SpinBox(value=self.parent.refresh_rate, bounds=[0, None])
        grid_ly.addWidget(self.refresh_rate,3,2)
        
        grid_ly.addWidget(QtGui.QLabel('Complete buffer with file data'),4,2,1,2)
        self.use_files = QtGui.QCheckBox()
        self.use_files.setChecked(self.parent.use_files)
        grid_ly.addWidget(self.use_files,4,1)

        self.okBtn = QtGui.QPushButton('OK',self)
        self.okBtn.clicked.connect(self.set_param)
        grid_ly.addWidget(self.okBtn,5,2)
        
        grid_ly.setColumnStretch(0,50)
        grid_ly.setColumnStretch(4,50)   
        grid_ly.setRowStretch(0,50)
        grid_ly.setRowStretch(6,50)
        grid_ly.setSpacing(10.)
        for i in range(grid_ly.count()):
            grid_ly.itemAt(i).setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.setLayout(grid_ly)
=======
        main_ly = QtGui.QGridLayout()
        
        main_ly.addWidget(QtGui.QLabel('Param'),0,0)
        self.param_w = pg.QtGui.QComboBox()
        self.param_w.addItems(param_keys)
        self.param_w.setCurrentIndex(param_keys.index(self.parent.param))
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
>>>>>>> origin/master
        
    def set_param(self):
        if self.parent.param != self.param_w.currentText():
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
<<<<<<< HEAD
        self.parent.use_files = self.use_files.isChecked()
        if self.use_files.isChecked():
            now = datetime.now().timestamp()
            self.parent.saved_data = self.parent.load_data_from_file(now-self.parent.xrange,now)
        self.parent.refresh_plot()
        self.close()
    
    
=======
        self.parent.nfiles = int(self.nfiles.value())
        self.parent.refresh_plot()
        self.close()
    
>>>>>>> origin/master
class Option_For_All(Dock):
    def __init__(self,parent=None):
        super(Option_For_All, self).__init__(name='Settings',size=(1,1))
        self.parent = parent
<<<<<<< HEAD
        
        self.addWidget(QtGui.QLabel('Xrange'),1,1)
        self.xrange_val = pg.SpinBox(value=1.0, bounds=[0, None])
        self.addWidget(self.xrange_val,1,2)
        self.xrange_unit = pg.QtGui.QComboBox()
        self.xrange_unit.addItems(['sec','min','hours','days'])
        self.xrange_unit.setCurrentIndex(2)
        self.addWidget(self.xrange_unit,1,3)   
        
        self.addWidget(QtGui.QLabel('Refresh (s)'),2,1)
        self.refresh_rate = pg.SpinBox(value=5.0, bounds=[0, None])
        self.addWidget(self.refresh_rate,2,2)
        
        self.addWidget(QtGui.QLabel('Complete buffer with file data'),3,2,1,2)
        self.use_files = QtGui.QCheckBox()
        self.addWidget(self.use_files,3,1)

        self.okBtn = QtGui.QPushButton('Set for all',self)
        self.okBtn.clicked.connect(self.set_param)
        self.addWidget(self.okBtn,4,2)

        self.addBtn = QtGui.QPushButton('Add dock',self)
        self.addBtn.clicked.connect(self.add_dock)
        self.addWidget(self.addBtn,4,3)
        
        self.layout.setColumnStretch(0,50)
        self.layout.setColumnStretch(4,50)   
        self.layout.setRowStretch(0,50)
        self.layout.setRowStretch(5,50)
        self.layout.setSpacing(10.)
        for i in range(self.layout.count()):
            self.layout.itemAt(i).setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
=======
    
#        main_ly = QtGui.QGridLayout()
        
        self.addWidget(QtGui.QLabel('Xrange'),1,0)
        self.xrange_val = pg.SpinBox(value=1.0, bounds=[0, None])
#        self.xrange_val.setFixedWidth(80)
        self.addWidget(self.xrange_val,1,1)
        self.xrange_unit = pg.QtGui.QComboBox()
        self.xrange_unit.addItems(['sec','min','hours','days'])
        self.xrange_unit.setCurrentIndex(2)
        self.addWidget(self.xrange_unit,1,2)   
        
        self.addWidget(QtGui.QLabel('Refresh'),2,0)
        self.refresh_rate = pg.SpinBox(value=15.0, bounds=[0, None])
        self.addWidget(self.refresh_rate,2,1)
        self.addWidget(QtGui.QLabel('sec'),2,2)
        
        self.addWidget(QtGui.QLabel('Add data from'),3,0)
        self.nfiles = pg.SpinBox(value=1, bounds=[0, None])
        self.addWidget(self.nfiles,3,1)
        self.addWidget(QtGui.QLabel('past days'),3,2)

        self.okBtn = QtGui.QPushButton('Set for all',self)
        self.okBtn.clicked.connect(self.set_param)
        self.addWidget(self.okBtn,4,1)

        self.addBtn = QtGui.QPushButton('Add dock',self)
        self.addBtn.clicked.connect(self.add_dock)
        self.addWidget(self.addBtn,4,2)
        
#        hly = QtGui.QHBoxLayout()       
#        hly.addStretch()
#        hly.addLayout(main_ly)
#        hly.addStretch()
#        self.setLayout(hly)
>>>>>>> origin/master
        
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
<<<<<<< HEAD
        use_files = self.use_files.isChecked()
        for d in self.parent.docks:
            d.xrange = xrange
            d.refresh_rate = refresh_rate
            d.use_files = use_files
            if use_files:
                now = datetime.now().timestamp()
                d.saved_data = d.load_data_from_file(now-xrange,now)
            d.refresh_plot()
            
    def add_dock(self):
=======
        nfiles = int(self.nfiles.value())
        for d in self.parent.docks:
            d.xrange = xrange
            d.refresh_rate = refresh_rate
            d.nfiles = nfiles
            d.refresh_plot()
            
    def add_dock(self):
        print ('add dock')
>>>>>>> origin/master
        newdock = Plot_Dock(parent=self.parent,param='PIVC')
        print (hasattr(self.parent, 'docks'))
        print (hasattr(self.parent, 'plot_area'))
        self.parent.docks.append(newdock)
        self.parent.plot_area.addDock(newdock)
         
class Main_Plot_Window(QtGui.QMainWindow):
    def __init__(self):
        super(Main_Plot_Window, self).__init__()
<<<<<<< HEAD
        self.plot_area = DockArea()
=======
        self.area = DockArea()
        self.setCentralWidget(self.area)
        
>>>>>>> origin/master
        self.docks = []
        self.docks.append(Plot_Dock(parent=self,param='PIVC',loc='left',rel_to=None))
        self.docks.append(Plot_Dock(parent=self,param='PB1K',loc='bottom',rel_to=self.docks[-1]))
        self.docks.append(Plot_Dock(parent=self,param='PVAT',loc='bottom',rel_to=self.docks[-1]))
        self.docks.append(Plot_Dock(parent=self,param='PHE3',loc='bottom',rel_to=self.docks[-1]))
        self.docks.append(Plot_Dock(parent=self,param='T2',loc='right',rel_to=None))
        self.docks.append(Plot_Dock(parent=self,param='T3',loc='bottom',rel_to=self.docks[-1]))
        self.docks.append(Plot_Dock(parent=self,param='HeR',loc='bottom',rel_to=self.docks[-1]))
<<<<<<< HEAD
        for d in self.docks:
            self.plot_area.addDock(d,d.loc,d.rel_to)
#        self.settings_dock = Dock('Settings', size=(1, 1))
        self.settings_dock = Option_For_All(parent=self)
        self.plot_area.addDock(self.settings_dock,'bottom',self.docks[-1])
        
        self.tab = QtGui.QTabWidget()
        self.tab.addTab(self.plot_area,'Plot')
        self.setCentralWidget(self.tab)
        
=======
        
        for d in self.docks:
            self.area.addDock(d,d.loc,d.rel_to)
        
        self.settings_dock = Dock('Settings', size=(1, 1))
        self.settings_dock.addWidget(Option_For_All(area=self.area,docks=self.docks))
        self.area.addDock(self.settings_dock,'bottom',self.docks[-1])

>>>>>>> origin/master
## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    win = Main_Plot_Window()
<<<<<<< HEAD
#    print (win.addTab)
=======
>>>>>>> origin/master
#    win.move(0,0)
#    win.showMaximized = True
    win.resize(1000,500)
    win.show()
    
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        print ('HEYYYYYYYYY')
        print (sys.flags.interactive)
        QtGui.QApplication.instance().exec_()
        

