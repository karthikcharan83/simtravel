'''
Created on Apr 19, 2010

@author: bsana
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import copy

from openamos.gui.misc.basic_widgets import *
from openamos.gui.env import *

class AbstractModWidget(QGroupBox):
    '''
    classdocs
    '''
    def __init__(self, parent=None):
        super(AbstractModWidget, self).__init__(parent)
        self.setTitle("") #"Specification")
        self.mainlayout = QGridLayout()
        self.setLayout(self.mainlayout)
        self.fatherdialog = self.parent()

    def makeProbChoiceWidget(self):
        self.choicewidget = QWidget(self)
        self.choicelayout = QVBoxLayout()
        self.choicewidget.setLayout(self.choicelayout)
        
        self.choicebuttonwidget = QWidget(self)
        choicebuttonlayout = QHBoxLayout()
        self.choicebuttonwidget.setLayout(choicebuttonlayout)
        self.choiceaddbutton = QPushButton('Add Alternative')
        choicebuttonlayout.addWidget(self.choiceaddbutton)
        self.choicedelbutton = QPushButton('Delete Alternative')
        choicebuttonlayout.addWidget(self.choicedelbutton)
        self.choicelayout.addWidget(self.choicebuttonwidget)
        
        self.choicetable = QTableWidget(0,2,self) #3,self)
        self.choicetable.setHorizontalHeaderLabels(['Alternative', 'Value']) #, 'Probability'])
        self.choicetable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.choicetable.horizontalHeader().setResizeMode(0,1)
        self.choicetable.horizontalHeader().setResizeMode(1,1)
        
        #self.choicetable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.choicelayout.addWidget(self.choicetable)
    
        self.mainlayout.addWidget(self.choicewidget,1,0,1,1)
        
        self.connect(self.choiceaddbutton, SIGNAL("clicked(bool)"), self.addChoice) 
        self.connect(self.choicedelbutton, SIGNAL("clicked(bool)"), self.delChoice)

    def addChoice(self):
        self.choicetable.insertRow(self.choicetable.rowCount())
        
    def delChoice(self):
        self.choicetable.removeRow(self.choicetable.currentRow())
    
    def makeChoiceWidget(self,x=0,y=0):
        self.choicewidget = QWidget(self)
        self.choicelayout = QVBoxLayout()
        self.choicewidget.setLayout(self.choicelayout)
        
        self.choicebuttonwidget = QWidget(self)
        choicebuttonlayout = QHBoxLayout()
        self.choicebuttonwidget.setLayout(choicebuttonlayout)
        self.choiceaddbutton = QPushButton('Add Alternative')
        choicebuttonlayout.addWidget(self.choiceaddbutton)
        self.choicedelbutton = QPushButton('Delete Alternative')
        choicebuttonlayout.addWidget(self.choicedelbutton)
        self.choicelayout.addWidget(self.choicebuttonwidget)
        
        self.choicetable = QTableWidget(self)
        self.choicetable.setRowCount(0)
        self.choicetable.setColumnCount(2)
        self.choicetable.setHorizontalHeaderLabels(['Alternative', 'Value'])
        #self.choicetable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.choicetable.setSelectionMode(QAbstractItemView.SingleSelection)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.choicetable.setSizePolicy(sizePolicy)
        self.choicetable.horizontalHeader().setResizeMode(0,1)
        self.choicelayout.addWidget(self.choicetable)
        
        self.mainlayout.addWidget(self.choicewidget,x,y,1,1)
        
        self.connect(self.choiceaddbutton, SIGNAL("clicked(bool)"), self.addChoice)
        self.connect(self.choicedelbutton, SIGNAL("clicked(bool)"), self.delChoice)


    def makeSeedWidget(self,x=0,y=1):
        self.seedlabel = QLabel('Seed')
        self.seedline = QSpinBox()
        self.seedline.setFixedWidth(100)
        self.seedline.setMinimum(1)
        self.seedline.setMaximum(100)
        seedlayout = QHBoxLayout()
        seedlayout.addWidget(self.seedlabel)
        seedlayout.addWidget(self.seedline)
        self.seedwidget = QWidget(self)
        self.seedwidget.setLayout(seedlayout)
        
        self.mainlayout.addWidget(self.seedwidget,x,y,1,1,Qt.AlignLeft)


    def makeVarsWidget(self,x=0,y=1):
        self.varswidget = QWidget(self)
        self.varslayout = QGridLayout()
        self.varswidget.setLayout(self.varslayout)
        
        tableslabel = QLabel('Tables')
        self.varslayout.addWidget(tableslabel,0,0)
        
        self.tableswidget = QListWidget()
        self.tableswidget.setSelectionMode(QAbstractItemView.SingleSelection)
#        parentdialog = self.parent()
        self.tableswidget.addItems(self.fatherdialog.tablelist) #parentdialog.tablelist)
        self.tableswidget.setMaximumWidth(180)
        self.varslayout.addWidget(self.tableswidget,1,0)
        
        varslabel = QLabel('Columns')
        self.varslayout.addWidget(varslabel,0,1)
        
        self.colswidget = QListWidget()
        self.colswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.colswidget.setMaximumWidth(180)
        self.varslayout.addWidget(self.colswidget,1,1)        
        
        self.varsbutton = QPushButton('>>')
        self.varslayout.addWidget(self.varsbutton,1,2)

        self.buttonwidget = QWidget(self)
        buttonlayout = QHBoxLayout()
        self.buttonwidget.setLayout(buttonlayout)
        self.intbutton = QPushButton('Add Interaction')
        buttonlayout.addWidget(self.intbutton)
        self.delbutton = QPushButton('Delete Row')
        buttonlayout.addWidget(self.delbutton)
        
        
        self.varslayout.addWidget(self.buttonwidget,0,3)
        
        self.varstable = QTableWidget(0,3,self)
        self.varstable.setHorizontalHeaderLabels(['Table', 'Column', 'Coefficient'])
        self.varstable.setSelectionBehavior(QAbstractItemView.SelectRows)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.varstable.setSizePolicy(sizePolicy)
        self.varstable.horizontalHeader().setResizeMode(0,1)
        self.varstable.horizontalHeader().setResizeMode(1,1)
        self.varstable.horizontalHeader().setResizeMode(2,1)
        self.varslayout.addWidget(self.varstable,1,3)
        
        self.mainlayout.addWidget(self.varswidget,x,y,1,10)
        self.mainlayout.setColumnStretch(y,5)
        
        self.connect(self.tableswidget, SIGNAL("itemClicked (QListWidgetItem *)"), self.populateFields)
        self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addVariable)
        self.connect(self.delbutton, SIGNAL("clicked(bool)"), self.delVariable)
        self.connect(self.intbutton, SIGNAL("clicked(bool)"), self.makeIntVar) 

    def populateFields(self,item):
        self.colswidget.clear()
        seltab = str(item.text())
#        parentdialog = self.parent()
        if seltab != "runtime":
            self.colswidget.addItems(self.fatherdialog.coldict[seltab]) # parentdialog.coldict[seltab])

    def addVariable(self):     
        if (self.tableswidget.currentItem() != None) & (self.colswidget.currentItem() != None):
            self.varstable.insertRow(self.varstable.rowCount())
            currtable = (self.tableswidget.currentItem()).text()
            tableitem = QTableWidgetItem()
            tableitem.setText(currtable)
            tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
            self.varstable.setItem(self.varstable.rowCount()-1, 0, tableitem)
            
            currvar = (self.colswidget.currentItem()).text()
            varitem = QTableWidgetItem()
            varitem.setText(currvar)
            varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
            self.varstable.setItem(self.varstable.rowCount()-1, 1, varitem)
        else:
            if (self.tableswidget.currentItem() != None):
                item = self.tableswidget.currentItem()
                if item.text() == "runtime":
                    self.varstable.insertRow(self.varstable.rowCount())
                    currtable = (self.tableswidget.currentItem()).text()
                    tableitem = QTableWidgetItem()
                    tableitem.setText(currtable)
                    tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
                    self.varstable.setItem(self.varstable.rowCount()-1, 0, tableitem)
                    
            else:
                msg = "Please select a Table and a Column"
                QMessageBox.information(self, "Warning",
                                        msg,
                                        QMessageBox.Ok)            

    def delVariable(self):
        self.varstable.removeRow(self.varstable.currentRow())

    def makeNestWidget(self):
        self.nestwidget = QWidget(self)
        self.nestlayout = QVBoxLayout()
        self.nestwidget.setLayout(self.nestlayout)
        
        self.nestbuttonwidget = QWidget(self)
        nestbuttonlayout = QHBoxLayout()
        self.nestbuttonwidget.setLayout(nestbuttonlayout)
        self.nesteaddbutton = QPushButton('Add Nest')
        nestbuttonlayout.addWidget(self.nesteaddbutton)
        self.nestdelbutton = QPushButton('Delete Nest')
        nestbuttonlayout.addWidget(self.nestdelbutton)
        self.nestlayout.addWidget(self.nestbuttonwidget)
        
        self.nesttable = QTableWidget(0,2,self)
        self.nesttable.setHorizontalHeaderLabels(['Nest', 'IV Parameter'])
        self.nesttable.horizontalHeader().setResizeMode(0,1)
        self.nesttable.horizontalHeader().setResizeMode(1,1)
        self.nestlayout.addWidget(self.nesttable)
        
        self.mainlayout.addWidget(self.nestwidget,1,0,1,1)
        
        self.connect(self.nesteaddbutton, SIGNAL("clicked(bool)"), self.addNest) 
        self.connect(self.nestdelbutton, SIGNAL("clicked(bool)"), self.delNest)

    def addNest(self):
        self.nesttable.insertRow(self.nesttable.rowCount())

    def delNest(self):
        self.nesttable.removeRow(self.nesttable.currentRow())
    
    def makeVarianceWidget(self):
        self.variancevwidget = QWidget(self)
        self.variancevlayout = QHBoxLayout()
        self.variancevwidget.setLayout(self.variancevlayout)

        self.variancevlabel = QLabel('Variance')
        self.variancevlayout.addWidget(self.variancevlabel)

        self.variancevline = LineEdit()
        self.variancevline.setFixedWidth(100)
        self.variancevlayout.addWidget(self.variancevline)

        self.mainlayout.addWidget(self.variancevwidget,0,0,1,1,Qt.AlignLeft)
 
        
    def makeSFVarianceWidget(self):
        self.variancevwidget = QWidget(self)
        #self.varianceuwidget = QWidget(self)
        self.variancevlayout = QHBoxLayout()
        #self.varianceulayout = QHBoxLayout()
        self.variancevwidget.setLayout(self.variancevlayout)
        #self.varianceuwidget.setLayout(self.varianceulayout)
        

        self.variancevlabel = QLabel('Variance (v) - Normal')
        self.variancevlayout.addWidget(self.variancevlabel)
        self.variancevline = LineEdit()
        self.variancevline.setFixedWidth(100)
        self.variancevlayout.addWidget(self.variancevline)
        
        self.varianceulabel = QLabel('   Variance (u) - Half Normal')
        self.variancevlayout.addWidget(self.varianceulabel)
        self.varianceuline = LineEdit()
        self.varianceuline.setFixedWidth(100)
        self.variancevlayout.addWidget(self.varianceuline)
        
        self.mainlayout.addWidget(self.variancevwidget,0,0,1,1,Qt.AlignLeft)
        #self.mainlayout.addWidget(self.varianceuwidget,0,1,1,1,Qt.AlignLeft)

   
    def makeIntVar(self):
        selectedrows = []
        for modindex in self.varstable.selectedIndexes():
            row = modindex.row()
            col = modindex.column()
            if col == 0:
                selectedrows.append(row) 

        if len(selectedrows) == 2:
            table1 = str((self.varstable.item(selectedrows[0],0)).text())
            col1 = str((self.varstable.item(selectedrows[0],1)).text())
            table2 = str((self.varstable.item(selectedrows[1],0)).text())
            col2 = str((self.varstable.item(selectedrows[1],1)).text())
            
            if len(table1.split(',')) > 1 or len(table2.split(',')) > 1:
                msg = "Please select only non-interacted variables"
                QMessageBox.information(self, "Warning",
                                        msg,
                                        QMessageBox.Ok) 
            else:  
                selectedrows.sort()
                self.varstable.removeRow(selectedrows[0])
                self.varstable.removeRow(selectedrows[1]-1)
                self.varstable.insertRow(self.varstable.rowCount())
    
                tableitem = QTableWidgetItem()
                tableitem.setText(table1 + ',' + table2)
                tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
                self.varstable.setItem(self.varstable.rowCount()-1, 0, tableitem)
                
                varitem = QTableWidgetItem()
                varitem.setText(col1 + ',' + col2)
                varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
                self.varstable.setItem(self.varstable.rowCount()-1, 1, varitem)
        else:
            msg = "Please select only two variables"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
            
    def makeScheduleWidget(self,x=0,y=0):
        choicewidget = QWidget(self)
        choicelayout = QVBoxLayout()
        choicewidget.setLayout(choicelayout)
        
#        dummywidget = QWidget()
#        dummylayout = QVBoxLayout()
#        dummywidget.setLayout(dummylayout)
#        labelwidget = QLabel('Catagory')
#        dummylayout.addWidget(labelwidget)
#        dummylayout.setContentsMargins(0,15,0,14)
#        choicelayout.addWidget(dummywidget)
        
        labelwidget = QLabel('Catagory')
        self.choicelist = QListWidget()
        self.choicelist.setSelectionMode(QAbstractItemView.SingleSelection)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.choicelist.setSizePolicy(sizePolicy)
        choicelayout.addWidget(labelwidget)
        choicelayout.addWidget(self.choicelist)
        
        self.mainlayout.addWidget(choicewidget,x,y,1,1)
        

    def genChecks(self):
        res = True
        return res
        

class ProbModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(ProbModWidget, self).__init__(parent)
        self.makeProbChoiceWidget()
        self.makeSeedWidget(0,0)
        self.makeVarsWidget(1,1) #(0,1)
        self.intbutton.setVisible(False)
        #self.delbutton.setVisible(False)
    
    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class CountModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(CountModWidget, self).__init__(parent) 
        self.makeCountTypeWidget()
        self.makeSeedWidget(0,2)
        self.makeChoiceWidget(1,0) 
        self.makeVarsWidget(1,1) 

    def makeCountTypeWidget(self):
        self.poiradio = QRadioButton(POI_MODEL)
        self.nbradio = QRadioButton(NEGBIN_MODEL)
        self.nbradio.setChecked(True)
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.poiradio)
        buttonlayout.addWidget(self.nbradio)
        self.counttypewidget = QWidget(self)
        self.counttypewidget.setLayout(buttonlayout)
        
        self.odwidget = QWidget(self)
        odlayout = QHBoxLayout()
        self.odwidget.setLayout(odlayout)
        self.odlabel = QLabel("Overdispersion")
        odlayout.addWidget(self.odlabel)
        self.odline = LineEdit()
        self.odline.setFixedWidth(100) 
        odlayout.addWidget(self.odline)
               
        self.mainlayout.addWidget(self.counttypewidget,0,0,1,1,Qt.AlignLeft)
        self.mainlayout.addWidget(self.odwidget,0,1,1,1,Qt.AlignLeft)
        
        self.connect(self.nbradio, SIGNAL("toggled(bool)"), self.ctypeAction)
         
    def ctypeAction(self, checked):
        if checked:
            self.odline.setEnabled(True) 
        else:
            self.odline.setEnabled(False)
        self.emit(SIGNAL("completeChanged()"))  

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class OrderedModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(OrderedModWidget, self).__init__(parent) 
        self.makeOrdTypeWidget()
        self.makeSeedWidget(0,1)
        self.makeOrdChoiceWidget(1,0)
        self.makeVarsWidget(1,1) 

    def makeOrdTypeWidget(self):
        self.logradio = QRadioButton(LOGIT)
        self.probradio = QRadioButton(PROBIT)
        self.logradio.setChecked(True)
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.logradio)
        buttonlayout.addWidget(self.probradio)
        self.ordtypewidget = QWidget(self)
        self.ordtypewidget.setLayout(buttonlayout)
               
        self.mainlayout.addWidget(self.ordtypewidget,0,0,1,1,Qt.AlignLeft)


    def makeOrdChoiceWidget(self,x=0,y=0):
        self.choicewidget = QWidget(self)
        self.choicelayout = QVBoxLayout()
        self.choicewidget.setLayout(self.choicelayout)
        
        self.choicebuttonwidget = QWidget(self)
        choicebuttonlayout = QHBoxLayout()
        self.choicebuttonwidget.setLayout(choicebuttonlayout)
        self.choiceaddbutton = QPushButton('Add Alternative')
        choicebuttonlayout.addWidget(self.choiceaddbutton)
        self.choicedelbutton = QPushButton('Delete Alternative')
        choicebuttonlayout.addWidget(self.choicedelbutton)
        self.choicelayout.addWidget(self.choicebuttonwidget)
        
        self.choicetable = QTableWidget(0,3,self)
        self.choicetable.setHorizontalHeaderLabels(['Alternative', 'Value', 'Threshold'])
        self.choicelayout.addWidget(self.choicetable)
        
        self.mainlayout.addWidget(self.choicewidget,x,y,1,1)
        
        self.connect(self.choiceaddbutton, SIGNAL("clicked(bool)"), self.addOrdChoice) 
        self.connect(self.choicedelbutton, SIGNAL("clicked(bool)"), self.delOrdChoice) 

    def addOrdChoice(self):
        self.choicetable.insertRow(self.choicetable.rowCount())
        self.choicetable.setItem(0,2,QTableWidgetItem())
        disableitem = self.choicetable.item(0, 2)
        disableitem.setFlags(disableitem.flags() & ~Qt.ItemIsEnabled)
        disableitem.setBackgroundColor(Qt.darkGray)

    def delOrdChoice(self):
        self.choicetable.removeRow(self.choicetable.currentRow())
        self.choicetable.setItem(0,2,QTableWidgetItem())
        disableitem = self.choicetable.item(0, 2)
        if disableitem != None:
            disableitem.setFlags(disableitem.flags() & ~Qt.ItemIsEnabled)
            disableitem.setBackgroundColor(Qt.darkGray)

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res
        
class SFModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(SFModWidget, self).__init__(parent) 
        self.makeSFVarianceWidget()
        self.makeSeedWidget(0,1)
        self.makeVarsWidget(1,0)  

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res    

class MNLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(MNLogitModWidget, self).__init__(parent)
        self.alternatives = []
        self.specs = {}
        self.curralt = None
        self.makeSeedWidget(0,0)
        self.makeChoiceWidget(1,0)
        self.makeVarsWidget(1,1) 
        self.connect(self.choicetable, SIGNAL("currentCellChanged (int,int,int,int)"), self.showVarsTable)

        
    def addVariable(self):
        sellist = self.choicetable.selectedIndexes() 
        if(len(sellist)!=1):
            msg = "Please select ONE alternative"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
        else:
            selaltitem = self.choicetable.itemFromIndex(sellist[0])
            if selaltitem == None:
                msg = "Please specify the selected alternative"
                QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
            else:
                selalt = selaltitem.text()
                if selalt not in self.alternatives:
                    self.alternatives.append(selalt)
                super(MNLogitModWidget,self).addVariable()

    def showVarsTable(self,currrow,currcol,prevrow,prevcol):
        self.storeVarsTable(prevrow)
        #print 'change var table'
        self.varstable.clearContents()
        self.varstable.setRowCount(0)
        curritem = self.choicetable.item(currrow, 0)
        if curritem != None:
            selalt = str(curritem.text())
            self.curralt = selalt
            altspecs = self.specs[selalt]
            self.varstable.setRowCount(len(altspecs))
            i = 0
            while i < self.varstable.rowCount():
                altspecrow = altspecs[i]
                tableitem = QTableWidgetItem()
                tableitem.setText(altspecrow[0])
                self.varstable.setItem(i,0,tableitem)
                varitem = QTableWidgetItem()
                varitem.setText(altspecrow[1])
                self.varstable.setItem(i,1,varitem)
                coeffitem = QTableWidgetItem()
                coeffitem.setText(altspecrow[2])
                self.varstable.setItem(i,2,coeffitem)
                i = i + 1
        else:
            pass  

    def storeVarsTable(self,prevrow):
        #print 'store var table'
        storeitem = self.choicetable.item(prevrow, 0)
        if storeitem != None:
            selalt = str(storeitem.text())
            altspecs = []
            i = 0
            while i < self.varstable.rowCount():
                if self.varstable.item(i, 2) != None:
                    var = []
                    tab = (self.varstable.item(i, 0)).text()
                    col = (self.varstable.item(i, 1)).text()
                    coeff = (self.varstable.item(i, 2)).text()
                    var.append(tab)
                    var.append(col)
                    var.append(coeff)
                    altspecs.append(var)
                i = i + 1
            self.specs[selalt] = altspecs
        else:
            print 'storeitem is None'


    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class GCMNLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(GCMNLogitModWidget, self).__init__(parent) 
        #self.makeChoiceWidget()
        self.makeSeedWidget(0,0)
        self.makeVarsWidget(1,0) 
        
    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class LogRegModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(LogRegModWidget, self).__init__(parent) 
        self.makeVarianceWidget()
        self.makeSeedWidget(0,1)
        self.makeVarsWidget(1,0) 

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class NLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(NLogitModWidget, self).__init__(parent) 
        self.alternatives = []
        self.specs = {}
        self.curralt = None
        self.makeNestWidget()
        self.makeSeedWidget(0,0)
        self.makeChoiceWidget(1, 1)
        self.makeVarsWidget(1, 2) 
        self.connect(self.choicetable, SIGNAL("currentItemChanged (QTableWidgetItem *,QTableWidgetItem *)"), self.showVarsTable) 
        #self.connect(self.varstable, SIGNAL("itemSelectionChanged()"), self.printSelection) 

    def addVariable(self):
        sellist = self.choicetable.selectedIndexes() 
        if(len(sellist)!=1):
            msg = "Please select ONE alternative"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
        else:
            selaltitem = self.choicetable.itemFromIndex(sellist[0])
            if selaltitem == None:
                msg = "Please specify the selected alternative"
                QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
            else:
                selalt = selaltitem.text()
                if selalt not in self.alternatives:
                    self.alternatives.append(selalt)
                super(NLogitModWidget,self).addVariable()

    def showVarsTable(self,curritem,previtem):
        self.storeVarsTable(previtem)
        print 'change var table'
        self.varstable.clearContents()
        self.varstable.setRowCount(0)
        if curritem != None:
            selalt = str(curritem.text())
            self.curralt = selalt
            altspecs = self.specs[selalt]
            self.varstable.setRowCount(len(altspecs))
            i = 0
            while i < self.varstable.rowCount():
                altspecrow = altspecs[i]
                tableitem = QTableWidgetItem()
                tableitem.setText(altspecrow[0])
                self.varstable.setItem(i,0,tableitem)
                varitem = QTableWidgetItem()
                varitem.setText(altspecrow[1])
                self.varstable.setItem(i,1,varitem)
                coeffitem = QTableWidgetItem()
                coeffitem.setText(altspecrow[2])
                self.varstable.setItem(i,2,coeffitem)
                i = i + 1
        else:
            pass    

    def storeVarsTable(self,storeitem):
        print 'store var table'
        if storeitem != None:
            selalt = str(storeitem.text())
            altspecs = []
            i = 0
            while i < self.varstable.rowCount():
                if self.varstable.item(i, 2) != None:
                    var = []
                    tab = (self.varstable.item(i, 0)).text()
                    col = (self.varstable.item(i, 1)).text()
                    coeff = (self.varstable.item(i, 2)).text()
                    var.append(tab)
                    var.append(col)
                    var.append(coeff)
                    altspecs.append(var)
                i = i + 1
            self.specs[selalt] = altspecs


    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        
        ivnests = []
        cnests = []
        i = 0
        while i < self.nesttable.rowCount():
            ivnests.append(str((self.nesttable.item(i, 0)).text()))
            i = i + 1         
        print ivnests
        i = 0
        while i < self.choicetable.rowCount():
            ch = (self.choicetable.item(i, 0)).text()
            chdet = ch.split('/')
            if len(chdet)>1:
                for j in range(len(chdet)-1):
                    cnests.append(str(chdet[j]))
            i = i + 1
        print cnests
        
        if len(cnests) == 0:
            self.errmsg = 'The choices do not have a nested structure\n'
            return False   
                
        badn = []
        for cn in cnests:
            if cn not in ivnests:
                badn.append(cn)
        if len(badn) > 0:
            self.errmsg = 'Please specify the IV parameters for the following nests:\n' + str(badn) + '\n'
            return False

        badn = []
        for ivn in ivnests:
            if ivn not in cnests:
                badn.append(ivn)
        if len(badn) > 0:
            self.errmsg = 'Please specify the following nests in the alternatives table:\n' + str(badn) + '\n'
            return False

        return res    


class SchduleModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(SchduleModWidget, self).__init__(parent)
        self.alternatives = []
        self.specs = {}
        self.curralt = None
        self.makeSeedWidget(0,0)
        self.makeScheduleWidget(1,0)
        self.makeVarsWidget(1,1)

        self.choicelist.addItem("Activity Attributes")
        self.choicelist.addItem("Daily Status")
        self.choicelist.addItem("Dependency")
        self.choicelist.addItem("ArrivalTime")
        self.choicelist.addItem("OccupancyInvalid")
        self.choicelist.addItem("Id")
        self.choicelist.addItem("PersonsArrivedAttributes")
        
        varspec1 = [["HouseholdIdName","",""],["PersonIdName","",""],["ScheduleIdName","",""],["ActivityTypeName","",""],
                   ["LocationIdName","",""],["StartTimeName","",""],["EndTimeName","",""],["DurationName","",""],
                   ["DependentPersonName","",""]]
        self.specs["Activity Attributes"] = varspec1

        varspec2 = [["DailySchoolStatus","",""],["DailyWorkStatus","",""]]
        self.specs["Daily Status"] = varspec2

        varspec3 = [["ChildDependency","",""]]
        self.specs["Dependency"] = varspec3
        
        varspec4 = [["DependentPersonId","",""],["Actual","",""],["Expected","",""]]
        self.specs["ArrivalTime"] = varspec4
        
        varspec5 = [["TripInd","",""],["StartTime","",""]]
        self.specs["OccupancyInvalid"] = varspec5
        
        varspec6 = [["HouseId","",""],["PersonId","",""]]
        self.specs["Id"] = varspec6
        
        varspec7 = [["TripDependentPersonIdName","",""],["TripCountName1","",""],["TripCountName","",""],["ActDependentPersonIdName","",""]]
        self.specs["PersonsArrivedAttributes"] = varspec7
                    
        self.connect(self.choicelist, SIGNAL("currentItemChanged (QListWidgetItem *,QListWidgetItem *)"), self.showVarsTable)


    def showVarsTable(self,currItem,preItem):
        self.storeVarsTable(preItem)
        #print 'change var table'
        self.varstable.clearContents()
        self.varstable.setRowCount(0)
        if currItem != None:
            selalt = str(currItem.text())
            self.curralt = selalt
            altspecs = self.specs[selalt]
            self.varstable.setRowCount(len(altspecs))
            i = 0
            while i < self.varstable.rowCount():
                altspecrow = altspecs[i]
                tableitem = QTableWidgetItem()
                tableitem.setText(altspecrow[0])
                self.varstable.setItem(i,0,tableitem)
                varitem = QTableWidgetItem()
                varitem.setText(altspecrow[1])
                self.varstable.setItem(i,1,varitem)
                coeffitem = QTableWidgetItem()
                coeffitem.setText(altspecrow[2])
                self.varstable.setItem(i,2,coeffitem)
                i = i + 1
        else:
            pass  

    def storeVarsTable(self,preItem):
        if preItem != None:
            selalt = str(preItem.text())
            altspecs = []
            i = 0
            while i < self.varstable.rowCount():
                if self.varstable.item(i, 2) != None:
                    var = []
                    tab = (self.varstable.item(i, 0)).text()
                    col = (self.varstable.item(i, 1)).text()
                    coeff = (self.varstable.item(i, 2)).text()
                    var.append(tab)
                    var.append(col)
                    var.append(coeff)
                    altspecs.append(var)
                i = i + 1
            self.specs[selalt] = altspecs
        else:
            print 'storeitem is None'


    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res
                
    def makeVarsWidget(self,x=0,y=1):
        varswidget = QWidget(self)
        varslayout = QGridLayout()
        varswidget.setLayout(varslayout)
        
        tableslabel = QLabel('Tables')
        varslayout.addWidget(tableslabel,0,0)
        
        self.tableswidget = QListWidget()
        self.tableswidget.setSelectionMode(QAbstractItemView.SingleSelection)
#        parentdialog = self.parent()
        self.tableswidget.addItems(self.fatherdialog.tablelist) #parentdialog.tablelist)
        self.tableswidget.setMaximumWidth(180)
        varslayout.addWidget(self.tableswidget,1,0)
        
        varslabel = QLabel('Columns')
        varslayout.addWidget(varslabel,0,1)
        
        self.colswidget = QListWidget()
        self.colswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.colswidget.setMaximumWidth(180)
        varslayout.addWidget(self.colswidget,1,1)        
        
        btnwidget = QWidget()
        btnlayout = QVBoxLayout()
        btnwidget.setLayout(btnlayout)
        self.varsbutton = QPushButton('>>')
        btnlayout.addWidget(self.varsbutton)
        self.delbutton = QPushButton('<<')
        btnlayout.addWidget(self.delbutton)
        varslayout.addWidget(btnwidget,1,2)
        
        self.varstable = QTableWidget(0,3,self)
        self.varstable.setHorizontalHeaderLabels(['Name', 'Table', 'Column'])
        self.varstable.setSelectionBehavior(QAbstractItemView.SelectRows)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.varstable.setSizePolicy(sizePolicy)
        self.varstable.horizontalHeader().setResizeMode(0,1)
        self.varstable.horizontalHeader().setResizeMode(1,1)
        self.varstable.horizontalHeader().setResizeMode(2,1)
        varslayout.addWidget(self.varstable,1,3)
        
        self.mainlayout.addWidget(varswidget,x,y,1,10)
        self.mainlayout.setColumnStretch(y,5)
        
        self.connect(self.tableswidget, SIGNAL("itemClicked (QListWidgetItem *)"), self.populateFields)
        self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addVariable)
        self.connect(self.delbutton, SIGNAL("clicked(bool)"), self.delVariable)

    def populateFields(self,item):
        self.colswidget.clear()
        seltab = str(item.text())
#        parentdialog = self.parent()
        self.colswidget.addItems(self.fatherdialog.coldict[seltab]) # parentdialog.coldict[seltab])
        
    def addVariable(self):
#        sellist = self.varstable.selectedIndexes() 
#        if(len(sellist)!=1):
#            msg = "Please select ONE category"
#            QMessageBox.information(self, "Warning",
#                                    msg,
#                                    QMessageBox.Ok)
#        else:
        tableitem = self.tableswidget.currentItem()
        colitem = self.colswidget.currentItem()
        if tableitem == None or colitem == None:
            msg = "Please select a table and a column"
            QMessageBox.information(self, "Warning",
                                msg,
                                QMessageBox.Ok)
        else:
            row = self.varstable.currentRow()
            if row >= 0:
                table = tableitem.text()
                tableitem1 = QTableWidgetItem()
                tableitem1.setText(table)
                tableitem1.setFlags(tableitem1.flags() & ~Qt.ItemIsEditable)
                self.varstable.setItem(row, 1, tableitem1)
                
                column = colitem.text()
                tableitem2 = QTableWidgetItem()
                tableitem2.setText(column)
                tableitem2.setFlags(tableitem2.flags() & ~Qt.ItemIsEditable)
                self.varstable.setItem(row, 2, tableitem2)
            else:
                msg = "Please select a row in the table of right side"
                QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
                            
    def delVariable(self):
        row = self.varstable.currentRow()
        tableitem1 = QTableWidgetItem()
        tableitem1.setText("")
        tableitem1.setFlags(tableitem1.flags() & ~Qt.ItemIsEditable)
        tableitem2 = QTableWidgetItem()
        tableitem2.setText("")
        tableitem2.setFlags(tableitem2.flags() & ~Qt.ItemIsEditable)
        self.varstable.setItem(row, 1, tableitem1)
        self.varstable.setItem(row, 2, tableitem2)
        
        
        
        