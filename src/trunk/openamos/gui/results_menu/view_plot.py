'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys, time
import random
import numpy as np
from copy import deepcopy
from openamos.gui.env import *
from openamos.core.database_management.cursor_database_connection import *
from openamos.core.database_management.database_configuration import *
from openamos.core.database_management.cursor_query_browser import *

from pylab import *
#from core_plot import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as plot
from matplotlib.patches import Patch, Rectangle
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MakeResultPlot(QDialog):
    def __init__(self, config, parent=None):
        QDialog.__init__(self, parent)

        self.trips_r_temp = ["trippurpose","starttime","endtime","tripmode","miles","occupancy","duration"]
        self.schedule_r_temp = ["activitytype","starttime","endtime","duration"]

        self.setMinimumSize(QSize(900,800))
        self.setWindowTitle("Profile of Activity Travel Pattern")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setWindowIcon(QIcon("./images/run.png"))

        self.table = 'households'
        self.out_table = 'schedule_r'
        self.data = []
        self.figs = []
        self.sketches = []
        self.axes = []
        self.toolbars = []

        self.new_obj = None
        self.project = None
        self.valid = False
        self.connects(config)
        self.cursor = self.new_obj.cursor


        self.tabs = QTabWidget()
        self.tabs.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabs.setMinimumHeight(300)
        self.connect(self.tabs, SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel)

        self.show_nhts = QCheckBox("Check if you would show NHTS results instead of OpenAmos")
        if not (self.new_obj.check_if_table_exists("schedule_nhts") and self.new_obj.check_if_table_exists("trips_nhts") \
            and self.new_obj.check_if_table_exists("households_nhts") and self.new_obj.check_if_table_exists("persons_nhts")):
            self.show_nhts.setDisabled(True)

        radiowidget = QWidget(self)
        radiolayout = QHBoxLayout()
        radiowidget.setLayout(radiolayout)
        segment = QGroupBox(self)
        #segment.setStyleSheet("border:0px;")
        addsegment = QHBoxLayout()
        segment.setLayout(addsegment)
        self.tripradio = QRadioButton("Travel Characteristics")
        self.tripradio.setChecked(True)
        self.actiradio = QRadioButton("Activity Characteristics")
        addsegment.addWidget(self.tripradio)
        addsegment.addWidget(self.actiradio)
        radiolayout.addWidget(segment)

        filter = QGroupBox(self)
        addfilter = QHBoxLayout()
        filter.setLayout(addfilter)
        var1 = QLabel("Variable 1")
        self.choicevar1 = QComboBox()
        self.choicevar1.setMinimumWidth(150)
        var2 = QLabel("Variable 2")
        self.choicevar2 = QComboBox()
        self.choicevar2.setMinimumWidth(150)
        addfilter.addWidget(var1)
        addfilter.addWidget(self.choicevar1)
        addfilter.addWidget(var2)
        addfilter.addWidget(self.choicevar2)
        radiolayout.addWidget(filter)
        radiolayout.setContentsMargins(0,0,0,0)
#        self.fill_item1()

        stablewidget = QWidget(self)
        stablelayout = QHBoxLayout()
        stablewidget.setLayout(stablelayout)

        tools = QToolBar()
        tools.setMaximumWidth(150)
        home_action = self.createaction("Go Home",self.gohome,"home","")
        zoom_action = self.createaction("Zoom",self.zoom,"viewmag+","")
        pan_action = self.createaction("Pan",self.panzoom,"pan")
        tools.addAction(home_action)
        tools.addAction(zoom_action)
        tools.addAction(pan_action)
        stablelayout.addWidget(tools)

        output = QGroupBox(self)
        addoutput = QHBoxLayout()
        output.setLayout(addoutput)
        self.freq = QRadioButton("Frequency     ")
        self.freq.setChecked(True)
        self.percent = QRadioButton("Percent(%) ")
        addoutput.addWidget(self.freq)
        addoutput.addWidget(self.percent)
        addoutput.setAlignment(Qt.AlignCenter)
        stablelayout.addWidget(output)

        self.selecttable = QGroupBox(self)
        selecttablelayout = QHBoxLayout()
        self.selecttable.setLayout(selecttablelayout)
        stablelabel = QLabel('Schedule Type')
        self.stablecombo = QComboBox()
        self.hasTables()
        self.stablecombo.setMinimumWidth(250)
        selecttablelayout.addWidget(stablelabel)
        selecttablelayout.addWidget(self.stablecombo)
        stablelayout.addWidget(self.selecttable)

        substablewidget = QWidget(self)
        substablelayout = QHBoxLayout()
        substablewidget.setLayout(substablelayout)
        substablelayout.setAlignment(Qt.AlignLeft)
        stablelayout.addWidget(substablewidget)
        self.resetbutton = QPushButton('Reset')
        self.resetbutton.setFixedWidth(80)
        stablelayout.addWidget(self.resetbutton)
        self.showbutton = QPushButton('Show Plot')
        self.showbutton.setFixedWidth(80)
        stablelayout.addWidget(self.showbutton)
        stablelayout.setContentsMargins(0,0,0,0)

        progresswidget = QWidget(self)
        progresslayout = QHBoxLayout()
        progresswidget.setLayout(progresslayout)
        self.progresslabel = QLabel("")
        self.progresslabel.setMinimumWidth(150)
        progresslayout.addWidget(self.progresslabel)
        progresslayout.addWidget(self.dialogButtonBox)
        progresslayout.setContentsMargins(0,0,0,0)


        self.makeVarsWidget1()
        filter_widget = QWidget(self)
        filterlayout = QVBoxLayout()
        filter_widget.setLayout(filterlayout)
        filterlayout.addWidget(self.show_nhts)
        filterlayout.addWidget(radiowidget)
        filterlayout.addWidget(self.socio)
        filterlayout.addWidget(self.tripfilter)

        scrollArea = QScrollArea()
        scrollArea.setWidget(filter_widget)
        scrollArea.setMaximumHeight(550)
        scrollArea.setWidgetResizable(True)

        tempwidget = QWidget(self)
        templayout = QVBoxLayout()
        tempwidget.setLayout(templayout)
        templayout.addWidget(stablewidget)
        templayout.addWidget(self.tabs)
        templayout.addWidget(progresswidget)
        templayout.setStretch(1,1)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(scrollArea)
        splitter.addWidget(tempwidget)
        splitter.setSizes([350,450])

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(splitter)
#        self.vbox.setStretch(0,1)
        self.setLayout(self.vbox)
        self.fill_item1()

        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), SLOT("reject()")) #self.disconnects)
        self.connect(self.resetbutton, SIGNAL("clicked(bool)"), self.reset_all)
        self.connect(self.showbutton, SIGNAL("clicked(bool)"), self.draw_plot)
        self.connect(self.tripradio, SIGNAL("clicked(bool)"), self.fill_item1)
        self.connect(self.actiradio, SIGNAL("clicked(bool)"), self.fill_item1)
        self.connect(self.choicevar1, SIGNAL("currentIndexChanged(int)"), self.manage_combo)
        self.connect(self.choicevar2, SIGNAL("currentIndexChanged(int)"), self.set_disable)
        self.connect(self.stablecombo, SIGNAL("currentIndexChanged(const QString&)"), self.selected_table)
        self.connect(self.show_nhts, SIGNAL("stateChanged(int)"), self.initTables)



    def makeVarsWidget1(self):

        self.socio = QGroupBox("")
        varslayout = QGridLayout()
        self.socio.setLayout(varslayout)

        segment = QGroupBox(self)
        segment.setStyleSheet("border:0px;")
        addsegment = QVBoxLayout()
        segment.setLayout(addsegment)
        self.segment1 = QRadioButton("Households")
        self.segment1.setChecked(True)
        self.segment2 = QRadioButton("Persons")
        addsegment.addWidget(self.segment1)
        addsegment.addWidget(self.segment2)
        varslayout.addWidget(segment,1,0)
        segment.setContentsMargins(0,0,0,0)

        tableslabel = QLabel('Columns')
        varslayout.addWidget(tableslabel,0,1)
        self.colswidget = QListWidget()
        self.colswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        if self.columnName() <> None:
            self.colswidget.addItems(self.columnName())
        self.colswidget.setMaximumWidth(160)
        self.colswidget.setMinimumHeight(150)
        varslayout.addWidget(self.colswidget,1,1)

        varslabel = QLabel('Values')
        varslayout.addWidget(varslabel,0,2)
        self.valwidget = QListWidget()
        self.valwidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.valwidget.setMaximumWidth(160)
        self.valwidget.setMinimumHeight(150)
        varslayout.addWidget(self.valwidget,1,2)

        buttonwidget1 = QWidget(self)
        buttonlayout1 = QVBoxLayout()
        buttonwidget1.setLayout(buttonlayout1)
        self.selbutton1 = QPushButton('>>')
        self.selbutton1.setFixedWidth(60)
        buttonlayout1.addWidget(self.selbutton1)
        self.delbutton = QPushButton('<<')
        self.delbutton.setFixedWidth(60)
        buttonlayout1.addWidget(self.delbutton)
        varslayout.addWidget(buttonwidget1,1,3)

        self.varstable = QTableWidget(0,2,self)
        self.varstable.setHorizontalHeaderLabels(['Column', 'Value'])
        self.varstable.setSelectionBehavior(QAbstractItemView.SelectRows)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.varstable.setSizePolicy(sizePolicy)
        self.varstable.horizontalHeader().setResizeMode(0,1)
        self.varstable.horizontalHeader().setResizeMode(1,1)
        self.varstable.setMaximumWidth(300)
        self.varstable.setMinimumHeight(150)
        varslayout.addWidget(self.varstable,1,4)

        workwidget = QWidget(self)
        worklayout = QVBoxLayout()
        workwidget.setLayout(worklayout)
        worklabel = QLabel("Work Status:")
        self.cmbworkstatus = QComboBox()
        self.cmbworkstatus.addItems([QString("All"),QString("Worker"),
                                 QString("Non-worker")])
        self.cmbworkstatus.setMinimumWidth(120)
        worklayout.addWidget(worklabel)
        worklayout.addWidget(self.cmbworkstatus)
        workwidget.setContentsMargins(0,0,0,40)
        varslayout.addWidget(workwidget,1,5)

        self.tripfilter = QGroupBox("")
        tripfilterlayout = QGridLayout()
        self.tripfilter.setLayout(tripfilterlayout)

        self.activitylabel = QLabel("Trip Purpose")
        self.activitychoice = QListWidget()
        self.activitychoice.setSelectionMode(QAbstractItemView.MultiSelection)
        self.activitychoice.setFixedWidth(170)
        self.activitychoice.setMinimumHeight(150)

        startlabel = QLabel("Start Time")
        self.startchoice = QListWidget()
        self.startchoice.setSelectionMode(QAbstractItemView.MultiSelection)
        self.startchoice.setFixedWidth(140)
        self.startchoice.setMinimumHeight(150)

        endlabel = QLabel("End Time")
        self.endchoice = QListWidget()
        self.endchoice.setSelectionMode(QAbstractItemView.MultiSelection)
        self.endchoice.setFixedWidth(140)
        self.endchoice.setMinimumHeight(150)

        duralabel = QLabel("Duration")
        self.durachoice = QListWidget()
        self.durachoice.setSelectionMode(QAbstractItemView.MultiSelection)
        self.durachoice.setFixedWidth(140)
        self.durachoice.setMinimumHeight(150)

        self.modelabel = QLabel("Trip Mode")
        self.modechoice = QListWidget()
        self.modechoice.setSelectionMode(QAbstractItemView.MultiSelection)
        self.modechoice.setFixedWidth(140)
        self.modechoice.setMinimumHeight(150)

        self.occuplabel = QLabel("Occupancy")
        self.occupchoice = QListWidget()
        self.occupchoice.setSelectionMode(QAbstractItemView.MultiSelection)
        self.occupchoice.setFixedWidth(140)
        self.occupchoice.setMinimumHeight(150)


        self.fill_item2(1,self.trip_labels("trippurpose"))
        self.fill_item2(2,self.trip_labels("starttime"))
        self.fill_item2(3,self.trip_labels("endtime"))
        self.fill_item2(4,self.trip_labels("duration"))
        self.fill_item2(5,self.trip_labels("tripmode"))
        self.fill_item2(6,self.trip_labels("occupancy"))

        tripfilterlayout.addWidget(self.activitylabel,0,0)
        tripfilterlayout.addWidget(self.activitychoice,1,0)
        tripfilterlayout.addWidget(startlabel,0,1)
        tripfilterlayout.addWidget(self.startchoice,1,1)
        tripfilterlayout.addWidget(endlabel,0,2)
        tripfilterlayout.addWidget(self.endchoice,1,2)
        tripfilterlayout.addWidget(duralabel,0,3)
        tripfilterlayout.addWidget(self.durachoice,1,3)
        tripfilterlayout.addWidget(self.modelabel,0,4)
        tripfilterlayout.addWidget(self.modechoice,1,4)
        tripfilterlayout.addWidget(self.occuplabel,0,5)
        tripfilterlayout.addWidget(self.occupchoice,1,5)

        self.connect(self.colswidget, SIGNAL("itemClicked (QListWidgetItem *)"), self.populateValues)
        self.connect(self.selbutton1, SIGNAL("clicked(bool)"), self.selValue)
        self.connect(self.delbutton, SIGNAL("clicked(bool)"), self.delValue)
        self.connect(self.segment1, SIGNAL("clicked(bool)"), self.initTables)
        self.connect(self.segment2, SIGNAL("clicked(bool)"), self.initTables)

    def hasTables(self):

        tables = []
        if self.new_obj.check_if_table_exists("schedule_r"):
            tables.append("Schedules: Non-reconciled")
        if self.new_obj.check_if_table_exists("schedule_cleanfixedactivityschedule_r"):
            tables.append("Schedules: Cleaned to Account for Daily Status")
        if self.new_obj.check_if_table_exists("schedule_ltrec_r"):
            tables.append("Schedules: Reconciled including Full Child Episodes")
        if self.new_obj.check_if_table_exists("schedule_childreninctravelrec_r"):
            tables.append("Schedules: Reconciled Including Travel Episodes")
        if self.new_obj.check_if_table_exists("schedule_cleanaggregateactivityschedule_r"):
            tables.append("Schedules: Aggregated in Home Schedule for Children")
        if self.new_obj.check_if_table_exists("schedule_dailyallocrec_r"):
            tables.append("Schedules: Daily Pattern with Child Allocation")
        if self.new_obj.check_if_table_exists("schedule_inctravelrec_r"):
            tables.append("Schedules: Reconciled Daily Pattern Skeleton with Child Allocation")
        if self.new_obj.check_if_table_exists("schedule_aggregatefinal_r"):
            tables.append("Schedules: Aggregated in Home Final Schedules")
        if self.new_obj.check_if_table_exists("schedule_full_r"):
            tables.append("Schedules: Full Schedules")


        self.stablecombo.addItems(tables)


    def selected_table(self, cur_text):
        if cur_text == "Schedules: Non-reconciled":
            self.out_table = "schedule_r"
        elif cur_text == "Schedules: Cleaned to Account for Daily Status":
            self.out_table = "schedule_cleanfixedactivityschedule_r"
        elif cur_text == "Schedules: Reconciled including Full Child Episodes":
            self.out_table = "schedule_ltrec_r"
        elif cur_text == "Schedules: Reconciled Including Travel Episodes":
            self.out_table = "schedule_childreninctravelrec_r"
        elif cur_text == "Schedules: Aggregated in Home Schedule for Children":
            self.out_table = "schedule_cleanaggregateactivityschedule_r"
        elif cur_text == "Schedules: Daily Pattern with Child Allocation":
            self.out_table = "schedule_dailyallocrec_r"
        elif cur_text == "Schedules: Reconciled Daily Pattern Skeleton with Child Allocation":
            self.out_table = "schedule_inctravelrec_r"
        elif cur_text == "Schedules: Aggregated in Home Final Schedules":
            self.out_table = "schedule_aggregatefinal_r"
        else:
            self.out_table = "schedule_full_r"


    def createaction(self, text, slot=None, icon=None,
                     tip=None, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon("./images/%s.png" % icon))
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)

        return action


    def on_context_menu(self,point):
        menubar = QMenu(self)
        one = menubar.addAction("Show Plot")
        two = menubar.addAction("Remove Plot")
        three = menubar.addAction("Save Plot as PNG")

        self.connect(one,SIGNAL("triggered()"),self.draw_plot)
        self.connect(two,SIGNAL("triggered()"),self.removeTab)
        self.connect(three,SIGNAL("triggered()"),self.saveimg)
        menubar.popup(self.tabs.mapToGlobal(point))

    def saveimg(self):
        dialog = QFileDialog()
        filename = dialog.getSaveFileName(self,"Save Image","","PNG image (*.png)")
        if str(filename) != "":
            index = self.tabs.currentIndex()
            index = index//2
            fig = self.figs[index]
            fig.savefig(str(filename))

    def draw_plot(self):
        if self.choicevar1.currentText() != "" and self.choicevar2.currentText() != "":
            self.on_draw2()
        elif self.choicevar1.currentText() != "":
            self.on_draw1()

    def makePlotTab(self,chart):
        page1 = QWidget()
        vbox = QVBoxLayout()
        page1.setLayout(vbox)
        vbox.addWidget(chart)
        chartname = ""
        index = -1
        if self.tabs.count() > 0:
            index = self.tabs.count() - 1
            tabtitle = self.tabs.tabText(index)
            numtab = int(tabtitle.split(" ")[1]) + 1
            chartname = "Chart %s" %(numtab)
        else:
            chartname = "Chart 1"
        self.tabs.addTab(page1, chartname)
        index = index + 1
        self.tabs.setCurrentIndex(index)

    def makeTableTab(self,stable):
        page1 = QWidget()
        vbox = QVBoxLayout()
        page1.setLayout(vbox)
        vbox.addWidget(stable)
        chartname = ""
        index = -1
        if self.tabs.count() > 0:
            index = self.tabs.count() - 1
            tabtitle = self.tabs.tabText(index)
            numtab = int(tabtitle.split(" ")[1])
            chartname = "Table %s" %(numtab)
        else:
            chartname = "Table 1"
        self.tabs.addTab(page1, chartname)
        #index = index + 1
        #self.tabs.setCurrentIndex(index)

    def removeTab(self):
        index = self.tabs.currentIndex()
        reply = QMessageBox.information(self,"Warning","Do you really want to remove?",QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes and index >= 0:
            tabtitle = self.tabs.tabText(index)
            name = str(tabtitle.split(" ")[0])
            if name == "Table":
                self.tabs.removeTab(index)
                self.tabs.removeTab(index-1)
            else:
                self.tabs.removeTab(index+1)
                self.tabs.removeTab(index)

            i = index//2
            self.figs.pop(i)
            self.sketches.pop(i)
            self.axes.pop(i)
            self.toolbars.pop(i)

    def reset_all(self):
        reply = QMessageBox.information(self,"Warning","Do you really want to remove?",QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:



            self.tabs.clear()
            self.figs = []
            self.sketches = []
            self.axes = []
            self.toolbars = []

            self.colswidget.clear()
            self.valwidget.clear()
            self.delRow()
            if self.columnName() <> None:
                self.colswidget.addItems(self.columnName())

            self.choicevar1.setCurrentIndex(0)
            self.fill_item2(1,self.trip_labels("trippurpose"))
            self.fill_item2(2,self.trip_labels("starttime"))
            self.fill_item2(3,self.trip_labels("endtime"))
            self.fill_item2(4,self.trip_labels("duration"))
            self.fill_item2(5,self.trip_labels("tripmode"))
            self.fill_item2(6,self.trip_labels("occupancy"))


    def createCanvas(self):
#        mydpi = 100
#        myfig = Figure((5.0, 4.5), dpi=mydpi)
        myfig = plt.figure()
        self.figs.append(myfig)
        sketch = FigureCanvas(myfig)
        myfig.subplots_adjust(left=0.08,right=0.85)
        myaxes = myfig.add_subplot(111)

        myCanvas = []
        myCanvas.append(sketch)
        myCanvas.append(myaxes)
        self.sketches.append(sketch)
        self.axes.append(myaxes)

        tool = NavigationToolbar(sketch,self)
        self.toolbars.append(tool)

        return myCanvas

    # Put a label on the bottom and right corner of the plot to show the sample size
    def fig_text(self,total):
        sample = "Sample Size: %d"%(total)
        fig = self.figs[len(self.figs)-1]
        fig.text(0.863,0.03,sample,fontsize=11,ha='left',va='bottom')

#    def mousePressEvent(self, ev):
#        QApplication.restoreOverrideCursor()

    def onleave(self,ev):
        QApplication.restoreOverrideCursor()

    def connects(self,configobject):

        protocol = configobject.getConfigElement(DB_CONFIG,DB_PROTOCOL)
        user_name = configobject.getConfigElement(DB_CONFIG,DB_USER)
        password = configobject.getConfigElement(DB_CONFIG,DB_PASS)
        host_name = configobject.getConfigElement(DB_CONFIG,DB_HOST)
        database_name = configobject.getConfigElement(DB_CONFIG,DB_NAME)

        self.database_config_object = DataBaseConfiguration(protocol, user_name, password, host_name, database_name)
        self.new_obj = DataBaseConnection(self.database_config_object)
        self.qb_obj = QueryBrowser(self.database_config_object)
        self.new_obj.new_connection()

#        #assigning the connection and cursor to the qb_obj
#        self.qb_obj.dbcon_obj.connection = self.new_obj.connection
#        self.qb_obj.dbcon_obj.cursor = self.new_obj.cursor
#
#        table_list = ['trips_r', 'schedule_final_r']
#        #create indexes on all the variables
#        t1 = time.time()
#        #for trip_r
#        table_name = 'trips_r'
#        for each in self.trips_r_temp:
#            col_name = []
#            index_name = 'plot'
#            col_name.append(each)
#            index_name = index_name + '_' + each + '_' + table_name
#            self.qb_obj.create_index(table_name, col_name, index_name)
#            result = self.qb_obj.cluster_index(table_name, index_name)
#
#        #for schedule_final_r
#        table_name = 'schedule_final_r'
#        for each in self.schedule_ltrec_r_temp:
#            col_name = []
#            index_name = 'plot'
#            col_name.append(each)
#            index_name = index_name + '_' + each + '_' + table_name
#            self.qb_obj.create_index(table_name, col_name, index_name)
#            result = self.qb_obj.cluster_index(table_name, index_name)
#        t2 = time.time()
#        print 'Time taken to create all indexes --> %s'%(t2-t1)


    def reject(self): #disconnects(self):
#        #delete all indexes
#        t1 = time.time()
#        #for trip_r
#        table_name = 'trips_r'
#        for each in self.trips_r_temp:
#            index_name = 'plot'
#            index_name = index_name + '_' + each + '_' + table_name
#            self.qb_obj.delete_index(table_name, index_name)
#
#        #for schedule_final_r
#        table_name = 'schedule_final_r'
#        for each in self.schedule_ltrec_r_temp:
#            index_name = 'plot'
#            index_name = index_name + '_' + each + '_' + table_name
#            self.qb_obj.delete_index(table_name, index_name)
#        t2 = time.time()
#        print 'Time taken to create all indexes --> %s'%(t2-t1)

        self.new_obj.close_connection()
        QDialog.accept(self)


    def fill_item1(self):
        self.choicevar1.clear()
        self.choicevar2.clear()
        vars = [""]

        if self.tripradio.isChecked():
            self.selecttable.setVisible(False)

            for i in self.trips_r_temp:
                if self.checkColumnExists("trips_full_r",i):# or i == "duration":
                    vars.append(i)

            vars.append("trip episode rates")
            self.activitylabel.setText("Trip Purpose")
            self.modelabel.setVisible(True)
            self.modechoice.setVisible(True)
            self.occuplabel.setVisible(True)
            self.occupchoice.setVisible(True)

        else:
            self.selecttable.setVisible(True)

            for i in self.schedule_r_temp:
                if self.checkColumnExists(self.out_table,i):
                    vars.append(i)


            vars.append("activity episode rates")
            self.activitylabel.setText("Activity Type")
            self.modelabel.setVisible(False)
            self.modechoice.setVisible(False)
            self.occuplabel.setVisible(False)
            self.occupchoice.setVisible(False)

        self.choicevar1.addItems(vars)

    def fill_item2(self,index,items):
        item_key = items.keys()
        item_key.sort()

        vars = []
        for key in item_key:
            item = items[key]
            vars.append(item)

        if index == 1:
            self.activitychoice.clear()
            self.activitychoice.addItems(vars)
        elif index == 2:
            self.startchoice.clear()
            self.startchoice.addItems(vars)
        elif index == 3:
            self.endchoice.clear()
            self.endchoice.addItems(vars)
        elif index == 4:
            self.durachoice.clear()
            self.durachoice.addItems(vars)
        elif index == 5:
            self.modechoice.clear()
            self.modechoice.addItems(vars)
        else:
            self.occupchoice.clear()
            self.occupchoice.addItems(vars)


    def manage_combo(self):
        self.choicevar2.clear()
        vars = [""]
        if self.tripradio.isChecked():
            text = self.choicevar1.currentText()
            if text == "trippurpose":
                temp = ["tripmode","starttime","endtime","miles","occupancy","duration"]
                for i in temp:
                    if self.checkColumnExists("trips_full_r",i): # or i == "duration":
                        vars.append(i)
            elif text != "trippurpose" and text != "" and text != "trip episode rates":
                temp = ["trippurpose"]
                for i in temp:
                    if self.checkColumnExists("trips_full_r",i):
                        vars.append(i)
        else:
            text = self.choicevar1.currentText()
            if text == "activitytype":
                temp = ["starttime","endtime","duration"]
                for i in temp:
                    if self.checkColumnExists(self.out_table,i):
                        vars.append(i)

            elif text != "activitytype" and text != "" and text != "activity episode rates":
                temp = ["activitytype"]
                for i in temp:
                    if self.checkColumnExists(self.out_table,i):
                        vars.append(i)


        self.choicevar2.addItems(vars)


    def set_disable(self):
        if self.choicevar2.currentText() != "":
            self.percent.setChecked(True)
            self.freq.setEnabled(False)
        else:
            self.freq.setEnabled(True)

    def columnName(self):
        tablename = self.table
        if self.show_nhts.isChecked():
            tablename = tablename + "_nhts"

        if self.new_obj.check_if_table_exists(tablename): #self.table):
            cols = self.new_obj.get_column_list(tablename) #self.table)
            columns = []
            for col in cols:

                columns.append(QString(col))
            return columns
        else:
            return None

    def populateValues(self, item):

        try:
            values = []
            temp = None
            vars = str(item.text())

            tablename = self.table
            if self.show_nhts.isChecked():
                tablename = tablename + "_nhts"

            order = str(item.text())

            self.cursor.execute("""SELECT DISTINCT %s FROM %s ORDER BY %s"""%(vars,tablename,order))
            temp = self.cursor.fetchall()

            for i in temp:
                value = str(i[0])
                values.append(value)

            self.valwidget.clear()
            self.valwidget.addItems(values)

        except Exception, e:
            print '\tError while creating the table %s'%self.table_name
            print e


    def selValue(self):
        if (self.colswidget.currentItem() != None) & (self.valwidget.currentItem() != None):
            currcolumn = (self.colswidget.currentItem()).text()
            currvar = (self.valwidget.currentItem()).text()
            if not self.isExist(currcolumn,currvar):
                self.varstable.insertRow(self.varstable.rowCount())
                tableitem = QTableWidgetItem()
                tableitem.setText(currcolumn)
                tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
                self.varstable.setItem(self.varstable.rowCount()-1, 0, tableitem)

                varitem = QTableWidgetItem()
                varitem.setText(currvar)
                varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
                self.varstable.setItem(self.varstable.rowCount()-1, 1, varitem)

        else:
            msg = "Please select a Column and a Value"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)


    def isExist(self, ccolumn, cvalue):
        numrows = self.varstable.rowCount()
        for i in range(numrows):
            column = str((self.varstable.item(i,0)).text())
            value = str((self.varstable.item(i,1)).text())
            if (column == ccolumn) & (value == cvalue):
                return True

        return False


    def delValue(self):
        self.varstable.removeRow(self.varstable.currentRow())


    def initTables(self):

        if self.segment1.isChecked(): #and self.table != 'households':
            self.colswidget.clear()
            self.valwidget.clear()
            self.delRow()
            self.table = 'households'
            if self.columnName() <> None:
                self.colswidget.addItems(self.columnName())
        if self.segment2.isChecked(): #and self.table != 'persons':
            self.colswidget.clear()
            self.valwidget.clear()
            self.delRow()
            self.table = 'persons'
            if self.columnName() <> None:
                self.colswidget.addItems(self.columnName())


    def delRow(self):
        numrows = self.varstable.rowCount() - 1
        while numrows > -1:
            self.varstable.removeRow(numrows)
            numrows = numrows - 1

    def selectedResults(self):
        sindex = self.idwidget.selectedIndexes()
        sdata = []
        for i in sindex:
            temp = self.data[i.row()]
            sdata.append(temp)

        return sdata


    def x_label(self):
        xtitle_trip = {'trippurpose':'Trip Purpose','starttime':'Trip Start Time','endtime':'Trip End Time',
                       'tripmode':'Trip Mode','occupancy':'Occupancy','duration':'Trip Time (mins)','miles':'Trip Length (miles)',
                       'trip episode rates':'Trips'}
        xtitle_acti = {'activitytype':'Activity Type','starttime':'Start Time','endtime':'End Time',
                  'duration':'Activity Duration (mins)','activity episode rates':'Activities'}

        column1 = str(self.choicevar1.currentText())
        column2 = str(self.choicevar2.currentText())

        if self.tripradio.isChecked():
            if column2 != "":
                return xtitle_trip[column2]
            else:
                return xtitle_trip[column1]
        else:
            if column2 != "":
                return xtitle_acti[column2]
            else:
                return xtitle_acti[column1]


    def plot_title(self):
        xtitle_trip = {'trippurpose':'Trip Purpose','starttime':'Trip Start Time','endtime':'Trip End Time',
                       'tripmode':'Trip Mode','occupancy':'Occupancy','duration':'Trip Time (mins)','miles':'Trip Length (miles)',
                       'trip episode rates':'Trip Episode Rates'}
        xtitle_acti = {'activitytype':'Activity Type','starttime':'Start Time','endtime':'End Time',
                  'duration':'Activity Duration (mins)','activity episode rates':'Activity Episode Rates'}

        column1 = str(self.choicevar1.currentText())
        column2 = str(self.choicevar2.currentText())

        title = ""
        if self.tripradio.isChecked():
            title = xtitle_trip[column1]
        else:
            title = xtitle_acti[column1]

        if column2 != "":
            title = title + " by "
            if self.tripradio.isChecked():
                title = title + xtitle_trip[column2]
            else:
                title = title + xtitle_acti[column2]

        return title


    def work_sql(self):
        if self.show_nhts.isChecked():
            table = "persons_daily_status_nhts"
        else:
            #table = "persons_daily_status_r"
            table = "persons_r"

        if self.cmbworkstatus.currentIndex() == 1:
            state = "(select * from %s where wrkdailystatus = 1 order by houseid, personid) as c" %(table)
        elif self.cmbworkstatus.currentIndex() == 2:
            state = "(select * from %s where wrkdailystatus = 0 order by houseid, personid) as c" %(table)
        else:
            state = ""

        return state


    def socio_sql(self):
        table1 = ""
        if self.segment1.isChecked():
            table1 = "households"
        else:
            table1 = "persons"

        if self.show_nhts.isChecked():
            table1 = table1 + "_nhts"

        vars = ''
        if self.segment1.isChecked():
            vars = 'houseid'
        else:
            vars = 'houseid, personid'

        filter = ''
        col_list = []
        numrows = self.varstable.rowCount()
        if numrows < 1:
            return "" #"WHERE"

        for i in range(numrows):
            column = str((self.varstable.item(i,0)).text())
            col = str(column)
            col_list.append(col)
            value = str((self.varstable.item(i,1)).text())
            filter = filter + "%s = %s and " %(column,value)
        filter = filter[0:len(filter)-5]
#        state = "join (SELECT %s FROM %s WHERE %s) AS B on" %(vars,table1,filter)
        state = "(select %s from %s where %s order by %s) as b" %(vars,table1,filter,vars)

        return state



    def time_categroy(self,column):
        #time = {1:[0,120],2:[120,300],3:[300,480],4:[480,660],5:[660,900],6:[900,1440]}
        time = {1:[0,60],2:[60,120],3:[120,180],4:[180,240],5:[240,300],6:[300,360],
                7:[360,420],8:[420,480],9:[480,540],10:[540,600],11:[600,660],12:[660,720],
                13:[720,780],14:[780,840],15:[840,900],16:[900,960],17:[960,1020],18:[1020,1440]}
        mode = {1:[1],2:[2],3:[3],4:[4],5:[5],6:[6],7:[7],8:[8],9:[9],10:[10],11:[11]}
        duration = {1:[0,10],2:[10,20],3:[20,30],4:[30,50],5:[50,70],
                    6:[70,100],7:[100,150],8:[150,200],9:[200,250],10:[250,1440]}
        miles = {1:[0,5],2:[5,10],3:[10,15],4:[15,20],5:[20,25],
                 6:[25,30],7:[30,40],8:[40,50],9:[50,30000]}
        occupancy = {1:[0],2:[1],3:[2],4:[3],5:[4],6:[5,30000]}
#        activitytype = {100:[100],101:[101],150:[150],151:[151],200:[200],201:[201],300:[300],301:[301],411:[411],
#                        412:[412],415:[415],416:[416],461:[461],462:[462],465:[465],466:[466],513:[513],514:[514],
#                        597:[597],598:[598],600:[600],601:[601],599:[599]}
        activitytype = {1:[100],2:[101,200],3:[200,300],4:[300,400],5:[400,500],
                        6:[500,597],7:[597,599],8:[600],9:[601],10:[599]}

        if column == "starttime" or column == "endtime":
            return time
        elif column == "tripmode":
            return mode
        elif column == "duration":
            return duration
        elif column == "miles":
            return miles
        elif column == "occupancy":
            return occupancy
        elif column == "activitytype" or column == "trippurpose":
            return activitytype


    def trip_labels(self, column):
#        activitytype = {100:'IH-Sojourn',101:'IH',150:'IH-Dependent Sojourn',151:'IH-Dependent',200:'OH-Work',201:'Work',300:'OH-School',
#                        301:'School',411:'OH-Pers Buss',
#                        412:'OH-Shopping',415:'OH-Meal',416:'OH-Serve Passgr',461:'OH-Dependent Pers Buss',462:'OH-Dependent Shopping',
#                        465:'OH-Dependent Meal',466:'OH-Dependent Serve Passgr',513:'OH-Social Visit',514:'OH-Sports/Rec',597:'Filler',
#                        598:'Anchor',600:'Pick-up',601:'Drop-off',599:'Other'}
        activitytype = {1:'Home',2:'In-Home',3:'Work',4:'School',5:'Maintenance',6:'Discretionary',
                        7:'Anchor',8:'Pick Up',9:'Drop Off',10:'OH-Other'}
        modedict = {1:'Car',2:'Van',3:'SUV',4:'Pickup Truck',5:'Bus',6:'Train',7:'School Bus',8:'Bike',9:'Walk',
                    10:'Taxi',11:'Other'}
        starttime = {1:'4am-5am',2:'5am-6am',3:'6am-7am',4:'7am-8am',5:'8am-9am',6:'9am-10am',
                    7:'10am-11am',8:'11am-12pm',9:'12pm-1pm',10:'1pm-2pm',11:'2pm-3pm',12:'3pm-4pm',
                    13:'4pm-5pm',14:'5pm-6pm',15:'6pm-7pm',16:'7pm-8pm',17:'8pm-9pm',18:'After 9pm'}
        endtime = {1:'4am-5am',2:'5am-6am',3:'6am-7am',4:'7am-8am',5:'8am-9am',6:'9am-10am',
                   7:'10am-11am',8:'11am-12pm',9:'12pm-1pm',10:'1pm-2pm',11:'2pm-3pm',12:'3pm-4pm',
                   13:'4pm-5pm',14:'5pm-6pm',15:'6pm-7pm',16:'7pm-8pm',17:'8pm-9pm',18:'After 9pm'}
        occupancy = {1:'0',2:'1',3:'2',4:'3',5:'4',6:'5 or more'}
        duration = {1:'0-10',2:'10-20',3:'20-30',4:'30-50',5:'50-70',
                    6:'70-100',7:'100-150',8:'150-200',9:'200-250',10:'>= 250'}
        miles = {1:'0-5',2:'5-10',3:'10-15',4:'15-20',5:'20-25',
                 6:'25-30',7:'30-40',8:'40-50',9:'>= 50'}

        if column == "activitytype" or column == "trippurpose":
            return activitytype
        if column == "tripmode":
            return modedict
        if column == "starttime":
            return starttime
        if column == "endtime":
            return endtime
        if column == "occupancy":
            return occupancy
        if column == "duration":
            return duration
        if column == "miles":
            return miles

    def checkColumnExists(self, tablename, columnname):
        columns = self.new_obj.get_column_list(tablename)
        try:
            columns.index(columnname)
        except:
            return False
        return True

    def sub_where_trip(self,column,indexes,dict):
        filter1 = ""
        if len(indexes) >= 1:
            filter1 = "("
            for i in indexes:
                value = dict[i.row()+1]
                if len(value) > 1:
                    filter1 = filter1 + "(%s >= %s AND %s < %s) or "%(column,value[0],column,value[1])
                else:
                    filter1 = filter1 + "%s = %s or "%(column,value[0])
            filter1 = filter1[0:len(filter1)-4] + ")"

        if len(indexes)==1:
            filter1 = filter1[1:len(filter1)-1]
        return filter1

    def where_trip(self):
#        trippurpose = {1:[100],2:[101],3:[150],4:[151],5:[200],6:[201],7:[300],8:[301],9:[411],
#                        10:[412],11:[415],12:[416],13:[461],14:[462],15:[465],16:[466],17:[513],18:[514],
#                        19:[597],20:[598],21:[600],22:[601],23:[599]}
        trippurpose = self.time_categroy("trippurpose")
        setime = self.time_categroy("starttime")
        duration = self.time_categroy("duration")
        tripmode = self.time_categroy("tripmode")
#        occup = self.time_categroy("occupancy")

        index1 = self.activitychoice.selectedIndexes()
        index2 = self.startchoice.selectedIndexes()
        index3 = self.endchoice.selectedIndexes()
        index4 = self.durachoice.selectedIndexes()
        index5 = self.modechoice.selectedIndexes()
#        index6 = self.occupchoice.selectedIndexes()

        filter1 =""
        if self.tripradio.isChecked():
            filter1 = self.sub_where_trip("trippurpose",index1,trippurpose)
        else:
            filter1 = self.sub_where_trip("activitytype",index1,trippurpose)

        filter2 = self.sub_where_trip("starttime",index2,setime)
        filter3 = self.sub_where_trip("endtime",index3,setime)
        filter4 = self.sub_where_trip("duration",index4,duration) #"A.endtime - A.starttime",index4,duration)
        filter5 = self.sub_where_trip("tripmode",index5,tripmode)

        filter = ""
        if filter1 != "":
            filter = filter1
        if filter2 != "":
            if filter != "":
                filter = "%s and %s"%(filter,filter2)
            else:
                filter = filter2
        if filter3 != "":
            if filter != "":
                filter = "%s and %s"%(filter,filter3)
            else:
                filter = filter3
        if filter4 != "":
            if filter != "":
                filter = "%s and %s"%(filter,filter4)
            else:
                filter = filter4
        if filter5 != "":
            if filter != "":
                filter = "%s and %s"%(filter,filter5)
            else:
                filter = filter5

        return filter



    def retrieveResult(self):
        table = self.tableName()

        column = self.choicevar1.currentText()
        if column == "":
            return False

        t1 = time.time()
        filter = ""
        socio = str(self.socio_sql())
        if socio != "":
            if self.segment1.isChecked():
                filter = "a.houseid = b.houseid"
            else:
                filter = "a.houseid = b.houseid and a.personid = b.personid"

        work = self.work_sql()
        if work != "":
            if filter != "":
                filter = "%s and "%(filter)

#            if self.segment1.isChecked():
#                filter = filter + "a.houseid = c.houseid"
#            else:
            filter = filter + "a.houseid = c.houseid and a.personid = c.personid"

        charact = ""
        if self.where_trip() != "":
            charact = " and %s"%(self.where_trip())

        try:
            self.total = 0.0
            cond = self.time_categroy(column)


            temp = cond.keys()
            temp.sort()
            for key in temp: #cond.keys():
                lowhigh = cond[key]

#                sql = ""
                sql = "select count(*) from "
                if len(lowhigh) > 1:
                    sql = "%s(select houseid, personid from %s where %s >= %d and %s < %d%s order by houseid, personid) as a" %(sql,table,column,lowhigh[0],column,lowhigh[1],charact)
                else:
                    sql = "%s(select houseid, personid from %s where %s = %d%s) as a" %(sql,table,column,lowhigh[0],charact)

                if socio != "":
                    sql = "%s,%s"%(sql,socio)

                if work != "":
                    sql = "%s,%s"%(sql,work)

                if filter != "":
                    sql = "%s where %s"%(sql,filter)

                print sql
                self.cursor.execute(sql)
                data = self.cursor.fetchall()
                for j in data:
                    if j[0] > 0:
                        self.err1.append(key)
                        self.err2.append(j[0])
                        self.total = self.total + j[0]

            if self.percent.isChecked():
                for i in range(len(self.err1)):
                    if self.total > 0.0:
                        self.err2[i] = round(100*float(self.err2[i])/self.total,2)
                    else:
                        self.err2[i] = 0.0

            t2 = time.time()
            print 'time taken --> %s'%(t2-t1)
            return True
        except Exception, e:
            print sql
            print '\tError while fetching the columns from the table'
            print e

        return False

    def on_draw1(self):
        """ Redraws the figure
        """
        #if not self.selectvar2.isChecked() and int(self.choicevar1.currentIndex())>0:
        self.progresslabel.setText("Processing....")
        self.repaint()

        self.err1 = []
        self.err2 = []
        isRetrieve = True
        if self.choicevar1.currentText() != "trip episode rates" and self.choicevar1.currentText() != "activity episode rates":
            isRetrieve = self.retrieveResult()
        else:
            isRetrieve = self.numPersons()

        if isRetrieve:
        # clear the axes and redraw the plot anew

            Sketch = self.createCanvas()
            Canvas = Sketch[0]
            axes = Sketch[1]

            axes.clear()
            axes.grid(True)
            N=len(self.err1)
            ind = np.arange(N)

            axes.set_title(self.plot_title())
            axes.bar(ind, self.err2, 0.4, color='green', align='center')
            axes.set_xlabel(str(self.x_label()))
            if self.percent.isChecked():
                axes.set_ylabel("Percent (%)")
            else:
                if self.choicevar1.currentText() != "trip episode rates" and self.choicevar1.currentText() != "activity episode rates":
                    axes.set_ylabel("Frequencies")
                else:
                    axes.set_ylabel("Number of Persons")
            #axes.set_ylim(0,100)

            labelsdict = self.trip_labels(str(self.choicevar1.currentText()))
            labels = []
            if labelsdict != None:
                for label in self.err1:
                    temp = label
                    if label in labelsdict.keys():
                        temp = labelsdict[label]
                    labels.append(temp)
            else:
                labels = self.err1

            axes.set_xticks(ind)
            if len(labels) >= 13:
                axes.set_xticklabels(labels, size='xx-small')
            elif (len(labels) >= 7):
                axes.set_xticklabels(labels, size='x-small')
            else:
                axes.set_xticklabels(labels)


            self.makePlotTab(Canvas)
            Canvas.draw()
            Canvas.mpl_connect('figure_enter_event', self.onleave)
            self.fig_text(self.total)


        vtable = CustomTable(self)
        #vtable.setSelectionMode(QAbstractItemView.MultiSelection)
        vtable.setColumnCount(2)
        header = QTableWidgetItem(str(self.choicevar1.currentText()))
        vtable.setHorizontalHeaderItem(0,header)
        if self.freq.isChecked():
            header = QTableWidgetItem(str("Frequency"))
            vtable.setHorizontalHeaderItem(1,header)
        else:
            header = QTableWidgetItem(str("Percent(%)"))
            vtable.setHorizontalHeaderItem(1,header)
        vtable.setRowCount(len(self.err2))
        for i in range(len(self.err2)):
            temp = self.err1[i]
            if labelsdict != None:
                temp = labelsdict[temp]
            header = QTableWidgetItem(str(temp))
            vtable.setItem(i,0,header)
            values = QTableWidgetItem(str(self.err2[i]))
            vtable.setItem(i,1,values)

        self.makeTableTab(vtable)
        self.progresslabel.setText("")
        self.repaint()

    def colors(self, index):
        colorpool = ['#0000FF','#FFFF00','#7B68EE','#FF4500','#1E90FF','#F0E68C','#87CEFA','#FFFACD',
                     '#FFD700','#4169E1','#FFA500','#6495ED','#BDB76B','#00BFFF','#FF6347','#B0E0E6',
                     '#F4A460','#808080','#32CD32','#CD853F','#00FA9A','#DCDCDC','#228B22','#006400',
                     '#696969','#00FF00','#A9A9A9','#98FB98','#D3D3D3','#3CB371','#C0C0C0','#ADFF2F']
        return colorpool[index]


    def on_draw2(self):
        """ Redraws the figure
        """

        self.progresslabel.setText("Processing....")
        self.repaint()

        column1 = self.choicevar1.currentText()
        column2 = self.choicevar2.currentText()

        isExchange = False
        if column1 == "activitytype" or column1 == "trippurpose":
            temp = column1
            column1 = column2
            column2 = temp
            isExchange = True

        category2 = []
        cond = self.time_categroy(column2)
        for key in cond.keys():
            category2.append(key)

        category2.sort()
        if len(category2) > 0:

            table = self.tableName()
            category1 = self.time_categroy(column1)

            Sketch = self.createCanvas()
            Canvas = Sketch[0]
            axes = Sketch[1]

            axes.clear()
            axes.grid(True)
            axes.set_title(self.plot_title())

            bars = []
            cumulate = []
            if isExchange == False:
                for j in range(len(category2)):
                    cumulate.append(0)

            filter = ""
            socio = str(self.socio_sql())
            if socio != "":
                if self.segment1.isChecked():
                    filter = "a.houseid = b.houseid"
                else:
                    filter = "a.houseid = b.houseid and a.personid = b.personid"

            work = self.work_sql()
            if work != "":
                if filter != "":
                    filter = "%s and "%(filter)

#                if self.segment1.isChecked():
#                    filter = filter + "a.houseid = c.houseid"
#                else:
                filter = filter + "a.houseid = c.houseid and a.personid = c.personid"

            charact = ""
            if self.where_trip() != "":
                charact = " and %s"%(self.where_trip())

            yvalue = []
            previous = []
            t1 = time.time()
            for key in category1.keys():

                lowhigh1 = category1[key]
                xvalue = []
                for j in range(len(category2)):
                    xvalue.append(0)

                try:


                    sql = "select count(*), a.%s from "%(column2)
                    if len(lowhigh1) > 1:
                        sql = "%s(select houseid, personid, %s from %s where %s >= %d and %s < %d%s order by houseid, personid) as a" %(sql,column2,table,column1,lowhigh1[0],column1,lowhigh1[1],charact)
                    else:
                        sql = "%s(select houseid, personid, %s from %s where %s = %d%s) as a" %(sql,column2,table,column1,lowhigh1[0],charact)

                    if socio != "":
                        sql = "%s,%s"%(sql,socio)

                    if work != "":
                        sql = "%s,%s"%(sql,work)

                    if filter != "":
                        sql = "%s where %s"%(sql,filter)

                    sql = "%s group by a.%s order by a.%s"%(sql,column2,column2)

                    print sql
                    self.cursor.execute(sql)
                    data = self.cursor.fetchall()

                    if isExchange:
                        total = 0
                        for t in data:
                            if self.purpose_index(int(t[1])) > 0:
                                index = category2.index(self.purpose_index(int(t[1]))) #int(t[1]))
                                xvalue[index] = xvalue[index] + int(t[0])
                                total = total+int(t[0])

                        cumulate.append(total)
                        yvalue.append(xvalue)
                    else:
                        for t in data:
                            if self.purpose_index(int(t[1])) > 0:
                                index = category2.index(self.purpose_index(int(t[1]))) #int(t[1]))
                                xvalue[index] = xvalue[index] + int(t[0])
                                cumulate[index] = cumulate[index] + int(t[0])

                        yvalue.append(xvalue)
                        previous.append(deepcopy(cumulate))


                except Exception, e:
                    print '\tError while fetching the columns from the table'
                    print e

            t2 = time.time()
            print 'time taken is ---> %s'%(t2-t1)

            labels = []
            if isExchange:
                labels = self.plot_legend(category1.keys(),str(self.choicevar2.currentText()))
            else:
                labels = self.plot_legend(category2,str(self.choicevar2.currentText()))

            ###########################################
            # Remove zero from the plot
            i = len(cumulate) - 1
            while i >= 0:
                if cumulate[i] <= 0.0:
                    cumulate.pop(i)
                    labels.pop(i)
                    if isExchange:
                        yvalue.pop(i)
                    else:
                        for j in range(len(previous)):
                            previous[j].pop(i)
                            yvalue[j].pop(i)
                i = i-1
            ############################################

            self.total = 0
            if isExchange:
                cum = []
                N=len(yvalue)
                ind = np.arange(N)
                for i in range(len(yvalue)):
                    cum.append(0)
                for i in range(len(yvalue[0])):
                    xvalue = []
                    temp = deepcopy(cum)
                    for j in range(len(yvalue)):
                        if cumulate[j] != 0:
                            value= 100.0*yvalue[j][i]/cumulate[j]
                            xvalue.append(value)
                            cum[j] = cum[j]+value
                        else:
                            xvalue.append(0)
                            cum[j]=0

                    colors = self.colors(i)
                    if i == 0:
                        temp = axes.bar(ind, xvalue, 0.5, color=colors, align='center')
                        bars.append(temp[0])
                    else:
                        temp = axes.bar(ind, xvalue, 0.5, color=colors, align='center', bottom=temp)
                        bars.append(temp[0])

                for j in range(len(yvalue)):
                    self.total = self.total+cumulate[j]
            else:
                N=len(yvalue[0])
                ind = np.arange(N)
                for i in range(len(yvalue)):
                    for j in range(len(yvalue[i])):
                        if cumulate[j] != 0:
                            yvalue[i][j] = 100.0*yvalue[i][j]/cumulate[j]
                            previous[i][j] = 100.0*previous[i][j]/cumulate[j]

                    colors = self.colors(i)
                    if i == 0:
                        temp = axes.bar(ind, yvalue[i], 0.5, color=colors, align='center')
                        bars.append(temp[0])
                    else:
                        temp = axes.bar(ind, yvalue[i], 0.5, color=colors, align='center', bottom=previous[i-1])
                        bars.append(temp[0])

                for j in range(len(yvalue[i])):
                    self.total = self.total+cumulate[j]


            prop = matplotlib.font_manager.FontProperties(size=8)
            axes.set_xticks(ind)
            if len(labels) >= 13:
                axes.set_xticklabels(labels, size='xx-small')
            elif (len(labels) >= 7):
                axes.set_xticklabels(labels, size='x-small')
            else:
                axes.set_xticklabels(labels)

            legendlabel = []
            if isExchange:
                legendlabel = self.plot_legend(category2,str(self.choicevar1.currentText()))
            else:
                legendlabel = self.plot_legend(category1.keys(),str(self.choicevar1.currentText()))

            axes.legend(bars,legendlabel,prop=prop,bbox_to_anchor=(1.01, 1),loc=2,borderaxespad=0.)
            axes.set_xlabel(str(self.x_label()))
            axes.set_ylabel("Percent (%)")
            axes.set_ylim(0,100)


            self.makePlotTab(Canvas)
            Canvas.draw()
            Canvas.mpl_connect('figure_enter_event', self.onleave)
            self.fig_text(self.total)

        self.create_table(isExchange,yvalue,cumulate,labels,legendlabel)
        self.progresslabel.setText("")
        self.repaint()

    def purpose_index(self, key):

        index = 0
        if key == 100:
            index = 1
        elif key >= 101 and key < 200:
            index = 2
        elif key >= 200 and key < 300:
            index = 3
        elif key >= 300 and key < 400:
            index = 4
        elif key >= 400 and key < 500:
            index = 5
        elif key >= 500 and key < 597:
            index = 6
        elif key >= 597 and key <=598:
            index = 7
        elif key == 600:
            index = 8
        elif key == 601:
            index = 9
        elif key == 599:
            index = 10

        return index

    def create_table(self,isExchange,yvalue,cumulate,labels,legendlabel):
        vtable = CustomTable(self)
        #vtable.setSelectionMode(QAbstractItemView.MultiSelection)
        if isExchange:
            vtable.setColumnCount(len(yvalue))
            vtable.setRowCount(len(yvalue[0]))
            for i in range(len(yvalue)):
                xvalue = yvalue[i]
                for j in range(len(xvalue)):
                    temp = 0.0
                    if cumulate[i] != 0:
                        temp = 100.0*xvalue[j]/cumulate[i]
                    else:
                        temp = 0.0

                    if i==0:
                        header = QTableWidgetItem(str(legendlabel[j]))
                        vtable.setVerticalHeaderItem(j,header)

                    if j==0:
                        header = QTableWidgetItem(str(labels[i]))
                        vtable.setHorizontalHeaderItem(i,header)

                    value = QTableWidgetItem(str(round(temp,2)))
                    vtable.setItem(j,i,value)
        else:
            vtable.setColumnCount(len(yvalue[0]))
            vtable.setRowCount(len(yvalue))
            for i in range(len(yvalue)):
                xvalue = yvalue[i]
                for j in range(len(xvalue)):
                    temp = xvalue[j]
                    if i==0:
                        header = QTableWidgetItem(str(labels[j]))
                        vtable.setHorizontalHeaderItem(j,header)

                    if j==0:
                        header = QTableWidgetItem(str(legendlabel[i]))
                        vtable.setVerticalHeaderItem(i,header)

                    value = QTableWidgetItem(str(round(temp,2)))
                    vtable.setItem(i,j,value)

        self.makeTableTab(vtable)


    def plot_legend(self,category,column):
        legenddict = self.trip_labels(str(column))
        legendlabel = []
        category.sort()
        for label in category:
            temp = label
            if label in legenddict.keys():
                temp = legenddict[label]
            legendlabel.append(temp)


        return legendlabel



    def gohome(self):
        index = self.tabs.currentIndex()
        index = index//2
        if index >= 0:
            tool = self.toolbars[index]
            tool.home()

    def zoom(self):
        index = self.tabs.currentIndex()
        index = index//2
        if index >= 0:
            tool = self.toolbars[index]
            tool.zoom()

    def panzoom(self):
        index = self.tabs.currentIndex()
        index = index//2
        if index >= 0:
            tool = self.toolbars[index]
            tool.pan()

    '''
    Retrieve the number of persons by trip frequencies
    '''
    def numPersons(self):

        if self.show_nhts.isChecked():
            table1 = "persons_nhts as p, households_nhts as h"
        else:
            table1 = "persons as p, households as h"

        base = ""
        if self.cmbworkstatus.currentIndex() > 0:
            if self.show_nhts.isChecked():
                table1 = "%s, persons_daily_status_nhts as w"%(table1)
            else:
                table1 = "%s, persons_daily_status_r as w"%(table1)

            if self.cmbworkstatus.currentIndex() == 1:
                base = " AND p.houseid = w.houseid AND p.personid = w.personid AND w.wrkdailystatus = 1"
            else:
                base = " AND p.houseid = w.houseid AND p.personid = w.personid AND w.wrkdailystatus = 0"

        table2 = self.tableName()
        socio = ""
        numrows = self.varstable.rowCount()
        if numrows > 0:
            socio = " AND "
        for i in range(numrows):
            column = str((self.varstable.item(i,0)).text())
            value = str((self.varstable.item(i,1)).text())
            if self.segment1.isChecked():
                socio = socio + "h.%s = '%s' AND " %(column,value)
            else:
                socio = socio + "p.%s = '%s' AND " %(column,value)
        if numrows > 0:
            socio = socio[0:len(socio)-5]


        t1 = time.time()
        try:
            self.total = 0.0
            character = "WHERE houseid > 0"
            if self.where_trip() != "":
                character = character + " AND " + self.where_trip()
            sql = "SELECT b.freq, count(*) FROM (SELECT p.houseid, p.personid FROM %s \
                  WHERE p.houseid = h.houseid%s%s) as a LEFT JOIN  \
                  (SELECT houseid, personid, count(*) as freq FROM %s %s GROUP BY houseid, personid) as b \
                  ON a.houseid = b.houseid AND a.personid = b.personid \
                  GROUP BY b.freq ORDER BY b.freq" %(table1,base,socio,table2,character)

            print sql
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            for j in data:
                self.err1.append(j[0])
                self.err2.append(j[1])
                self.total = self.total + j[1]

            if self.err1[len(self.err1)-1] == None:
                self.err1.pop()
                tmp = self.err2.pop()
                self.total = self.total - tmp
#                self.err1.insert(0,0)
#                self.err2.insert(0,tmp)

            if self.percent.isChecked() and self.total > 0.0:
                for i in range(len(self.err1)):
                    self.err2[i] = round(100*float(self.err2[i])/self.total,2)


            t2 = time.time()
            print 'time taken --> %s'%(t2-t1)
            return True
        except Exception, e:
            print '\tError while fetching the columns from the table'
            print e

        return False

    def tableName(self):

        table = ""
        if not self.show_nhts.isChecked():
            if self.tripradio.isChecked():
                table = "trips_full_r"
            else:
                table = self.out_table
        else:
            if self.tripradio.isChecked():
                table = "trips_nhts"
            else:
                table = "schedule_nhts"

        return table


class CustomTable(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        if parent:
            self.parent = parent
        self.__initActions__()
        self.__initContextMenus__()

    def __initActions__(self):
        self.copyAction = QAction("Copy",  self)
        self.copyAction.setShortcut("Ctrl+C")
        self.addAction(self.copyAction)
        self.connect(self.copyAction, SIGNAL("triggered()"), self.copyCells)

    def __initContextMenus__(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self, SIGNAL("customContextMenuRequested(QPoint)"), self.tableWidgetContext)

    def tableWidgetContext(self, point):
        '''Create a menu for the tableWidget and associated actions'''
        tw_menu = QMenu("Menu", self)
        tw_menu.addAction(self.copyAction)
        tw_menu.exec_(self.mapToGlobal(point))

    def copyCells(self):
        selRange  = self.selectedRanges()[0]#just take the first range
        topRow = selRange.topRow()
        bottomRow = selRange.bottomRow()
        rightColumn = selRange.rightColumn()
        leftColumn = selRange.leftColumn()
        #item = self.tableWidget.item(topRow, leftColumn)
        clipStr = QString()
        for row in xrange(topRow, bottomRow+1):
            for col in xrange(leftColumn, rightColumn+1):
                cell = self.item(row, col)
                if cell:
                    clipStr.append(cell.text())
                else:
                    clipStr.append(QString(""))
                clipStr.append(QString("\t"))
            clipStr.chop(1)
            clipStr.append(QString("\r\n"))

        cb = QApplication.clipboard()
        cb.setText(clipStr)


def main():
    app = QApplication(sys.argv)
    diag = MakeResultPlot(None, None)
    diag.show()
    app.exec_()

if __name__ == "__main__":
    main()
