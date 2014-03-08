'''
Created on May 30, 2011

@author: dhyou
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import copy

from openamos.gui.misc.basic_widgets import *
from openamos.gui.env import *

from openamos.core.database_management.database_connection import *
from openamos.core.database_management.database_configuration import *

class AbstractMixedWidget(QWidget):
    '''
    classdocs
    '''
    def __init__(self,parent=None):
        super(AbstractMixedWidget, self).__init__(parent)
        
        self.populateFromDatabase()
        
        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)
        
        row1 = QWidget(self)
        row1layout = QGridLayout()
        row1.setLayout(row1layout)
        
        tableslabel = QLabel('Tables')
        row1layout.addWidget(tableslabel,0,0)
        
        self.tableswidget = QListWidget()
        self.tableswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableswidget.addItems(self.tablelist)
        self.tableswidget.setMaximumSize(250,150)
        row1layout.addWidget(self.tableswidget,1,0)
        
        self.addTable = QPushButton('Value')
        self.addTable.setMaximumWidth(50)
        row1layout.addWidget(self.addTable,2,0)

        varslabel = QLabel('Columns')
        row1layout.addWidget(varslabel,0,1)
        
        self.colswidget = QListWidget()
        self.colswidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.colswidget.setMaximumSize(250,150)
        row1layout.addWidget(self.colswidget,1,1)
        
        self.addColumn = QPushButton('Value')
        self.addColumn.setMaximumWidth(50)
        row1layout.addWidget(self.addColumn,2,1)
        
        
        row3 = QWidget(self)
        row3layout = QGridLayout()
        row3.setLayout(row3layout)
        
        selectlabel = QLabel("Attribute Name: ")
        self.attriname = QComboBox()
        self.attriname.setMinimumWidth(220)      
        attrivaluelabel = QLabel("Attribute Value: ")
        self.valueline = LineEdit()
        self.valueline.setMinimumWidth(220)
        
        row3layout.addWidget(selectlabel,0,0)
        row3layout.addWidget(self.attriname,1,0)
        row3layout.addWidget(attrivaluelabel,0,1)
        row3layout.addWidget(self.valueline,1,1)
            
        row4 = QWidget(self)
        row4layout = QHBoxLayout()
        row4.setLayout(row4layout)
    
        btnwidget1 = QWidget(self)
        btnlayout1 = QHBoxLayout()
        btnwidget1.setLayout(btnlayout1) 
        btnlayout1.setContentsMargins(0,0,0,0)
        self.addbutton = QPushButton('Add')
        self.addbutton.setMaximumWidth(120)
        self.delbutton = QPushButton('Delete')
        self.delbutton.setMaximumWidth(120) 
        btnlayout1.addWidget(self.addbutton)
        btnlayout1.addWidget(self.delbutton)
          
        row4layout.addWidget(btnwidget1)
        dummy = QLabel("")
        row4layout.addWidget(dummy)

        row5 = QWidget(self)
        row5layout = QVBoxLayout()
        row5.setLayout(row5layout)
        row5layout.setContentsMargins(10,0,10,0)
        self.attritable = QTableWidget(self)
        self.attritable.setRowCount(0)
        self.attritable.setColumnCount(2)
        self.attritable.setHorizontalHeaderLabels(['Attribute', 'Value'])
        self.attritable.setSelectionMode(QAbstractItemView.SingleSelection)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.attritable.setSizePolicy(sizePolicy)
        self.attritable.horizontalHeader().setResizeMode(0,1)
        self.attritable.horizontalHeader().setResizeMode(1,1)
        row5layout.addWidget(self.attritable)
        
        mainlayout.addWidget(row1)
        mainlayout.addWidget(row3)
        mainlayout.addWidget(row4)
        mainlayout.addWidget(row5)
        
        self.connect(self.tableswidget, SIGNAL("itemClicked (QListWidgetItem *)"), self.populateColumns)
        self.connect(self.addbutton, SIGNAL("clicked(bool)"), self.addAttribute)
        self.connect(self.delbutton, SIGNAL("clicked(bool)"), self.delAttribute)
        self.connect(self.addTable, SIGNAL("clicked(bool)"), self.fillValueT)
        self.connect(self.addColumn, SIGNAL("clicked(bool)"), self.fillValueC)
        


    def populateColumns(self, item):
        self.colswidget.clear()
        seltab = str(item.text())
        self.colswidget.addItems(self.coldict[seltab])
        
    def addAttribute(self):
        name = str(self.attriname.currentText())
        value = str(self.valueline.text())

        if (name != "") & (value != ""):
            self.attritable.insertRow(self.attritable.rowCount())
            tableitem = QTableWidgetItem()
            tableitem.setText(name)
            tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
            self.attritable.setItem(self.attritable.rowCount()-1, 0, tableitem)
            
            varitem = QTableWidgetItem()
            varitem.setText(value)
            self.attritable.setItem(self.attritable.rowCount()-1, 1, varitem)  
            
    def delAttribute(self):
        self.attritable.removeRow(self.attritable.currentRow())
        
    def fillValueT(self):
        temp = self.tableswidget.currentItem()
        if temp != None:
            value = str(temp.text())
            self.valueline.setText(value)
            
    def fillValueC(self):
        items = self.colswidget.selectedItems()
        length = len(items)
        if length > 0:
            value = ""
            for i in range(len(items)-1):
                value = value + str(items[i].text()) + ","
            value = value + str(items[length-1].text())
            self.valueline.setText(value)

    def populateFromDatabase(self):
        father = self.parent()
        configobject = father.configobject
        
        protocol = configobject.getConfigElement(DB_CONFIG,DB_PROTOCOL)        
        user_name = configobject.getConfigElement(DB_CONFIG,DB_USER)
        password = configobject.getConfigElement(DB_CONFIG,DB_PASS)
        host_name = configobject.getConfigElement(DB_CONFIG,DB_HOST)
        database_name = configobject.getConfigElement(DB_CONFIG,DB_NAME)
        self.database_config_object = DataBaseConfiguration(protocol, user_name, password, host_name, database_name)
        
        new_obj = DataBaseConnection(self.database_config_object)
        new_obj.new_connection()
        tables = new_obj.get_table_list()
        
        self.tablelist = []
        self.coldict = {}
        for table in tables:
            self.tablelist.append(QString(table))
            cols = new_obj.get_column_list(table)
            varlist = []
            if cols is not None:
                for col in cols:
                    varlist.append(QString(col))
                self.coldict[table] = varlist
        self.tablelist.append("runtime")
        self.coldict["runtime"] = []
              
        
        
        