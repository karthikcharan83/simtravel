'''
Created on Nov 9, 2010

@author: dhyou
'''
import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from openamos.gui.env import *
from openamos.core.database_management.cursor_database_connection import *
from openamos.core.database_management.database_configuration import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

class Matplot(QDialog):
    
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setMinimumSize(QSize(900,500))
        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        #
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.new_obj = None
        self.project = None
        self.dpi = 100
        self.fig = Figure((5.0, 4.5), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        # Since we have only one plot, we can use add_axes
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)
        
        self.addfilter = QWidget(self)
        addfilterlayout = QGridLayout()
        self.addfilter.setLayout(addfilterlayout)
        
        filter = QGroupBox(self)
        addfilter = QGridLayout()
        filter.setLayout(addfilter)
        var1 = QLabel("Variable 1")
        self.choicevar1 = QComboBox()
        self.choicevar1.setMinimumWidth(200)
        self.selectvar2 = QCheckBox("Check to enable variable 2")
        var2 = QLabel("Variable 2")
        self.choicevar2 = QComboBox()
        self.choicevar2.setMinimumWidth(200)
        self.choicevar2.setEnabled(False)
        addfilter.addWidget(var1,0,0)
        addfilter.addWidget(var2,1,0)
        addfilter.addWidget(self.choicevar1,0,1)
        addfilter.addWidget(self.selectvar2,0,2)
        addfilter.addWidget(self.choicevar2,1,1)
        addfilterlayout.addWidget(filter,0,0)
        
#        segment = QGroupBox(self)
#        addsegment = QGridLayout()
#        segment.setLayout(addsegment)
#        self.segment1 = QRadioButton("Adult Worker")
#        self.segment2 = QRadioButton("Adult Non-worker")
#        self.segment3 = QRadioButton("Non-adult (5-17)")
#        self.segment4 = QRadioButton("Preschool (0-4)")
#        addsegment.addWidget(self.segment1,0,0)
#        addsegment.addWidget(self.segment2,0,1)
#        addsegment.addWidget(self.segment3,1,0)
#        addsegment.addWidget(self.segment4,1,1)
#        addfilterlayout.addWidget(segment,0,1)
        
        addfilterlayout.setColumnStretch(0,3)
        addfilterlayout.setColumnStretch(1,2)
        

        self.vbox = QVBoxLayout()
        self.vbox.setStretch(0,1)
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        
        
        #self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        #self.connect(self, SIGNAL('triggered()'),self.closeEvent)
        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self.disconnects)
        

 
    def connects(self,configobject):
        
        protocol = configobject.getConfigElement(DB_CONFIG,DB_PROTOCOL)        
        user_name = configobject.getConfigElement(DB_CONFIG,DB_USER)
        password = configobject.getConfigElement(DB_CONFIG,DB_PASS)
        host_name = configobject.getConfigElement(DB_CONFIG,DB_HOST)
        database_name = configobject.getConfigElement(DB_CONFIG,DB_NAME)
        
        self.database_config_object = DataBaseConfiguration(protocol, user_name, password, host_name, database_name)
        self.new_obj = DataBaseConnection(self.database_config_object)
        self.new_obj.new_connection()

        
    def disconnects(self):
        self.new_obj.close_connection()
        self.close()

        
    
    def isValid(self):
        pass

    def on_draw(self):
        pass


    def executeSelectQuery(self, cursor, vars, tablename, filter="", group ="", order =""):
#        if self.checkIfTableExists(tablename):
        try:
            temp = None
            if filter != "" and group != "" and order != "":
                cursor.execute("""SELECT %s FROM %s WHERE %s GROUP BY %s ORDER BY %s"""%(vars,tablename,filter,group,order))
                temp = cursor.fetchall()
            elif filter != "" and group == "":
                cursor.execute("""SELECT %s FROM %s WHERE %s ORDER BY %s"""%(vars,tablename,filter,order))
                temp = cursor.fetchall()
            elif filter == "" and group != "":
                cursor.execute("""SELECT %s FROM %s GROUP BY %s ORDER BY %s"""%(vars,tablename,group,order))
                temp = cursor.fetchall()
            else:
                cursor.execute("""SELECT %s FROM %s ORDER BY %s"""%(vars,tablename,order))
                temp = cursor.fetchall()
            

            return temp
        
        except Exception, e:
            print '\tError while creating the table %s'%self.table_name
            print e
            return False      
#        else:
#            QMessageBox.warning(self, "Results", "A table with name - %s does not exist." %(tablename), QMessageBox.Ok)
#            return False


    def checkIfTableExists(self, tablename):
        tables = self.tableList()
        try:
            tables.index(tablename)
        except:
            return False
        return True

    def tableList(self):
        tables = self.new_obj.get_table_list()
        return tables
    
    def checkColumnExists(self, tablename, columnname):
        columns = self.new_obj.get_column_list(tablename)
        try:
            columns.index(columnname)
        except:
            return False
        return True


    def fill_variable1(self,tablename):
        vars = [""]
        if tablename == "trips_r":
            temp = ["starttime","endtime","tripmode","miles","occupancy","duration"]
            for i in temp:
                if self.checkColumnExists(tablename,i):
                    vars.append(i)
        else:
            temp = ["activitytype","starttime","endtime","duration"]
            for i in temp:
                if self.checkColumnExists(tablename,i):
                    vars.append(i)
            
        self.choicevar1.addItems(vars)
        self.choicevar2.addItems(vars)
                
                
#    def fill_variable2(self,pattern):
#        
#        self.choicevar2.clear()
#        vars = []
#        if pattern == "trips":
#            vars = ["purpose","strttime","endtime","mode","occupancy"]
#            temp = vars.remove(str(self.choicevar1.currentText()))
#            print "%s deleted"%(temp)
#        else:
#            vars = ["purpose","strttime","endtime","mode","occupancy"]
#            vars.remove(str(self.choicevar1.currentText()))
#        
#        self.choicevar2.addItems(vars)




class LabComboBox(QWidget):
    def __init__(self, label, list, parent=None):
        QDialog.__init__(self, parent)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(label)
        self.combobox = QComboBox()
        self.list = list
        self.combobox.addItems(self.list)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combobox)
        self.connect(self.combobox, SIGNAL("currentIndexChanged(const QString&)"), self.emitSignal)
        self.label.setFixedWidth(70)
        self.setFixedWidth(300)

    def emitSignal(self):
        self.emit(SIGNAL("currSelChanged"))

    def getCurrentText(self):
        return self.combobox.currentText()
    
    def getCurrentIndex(self):
        return self.combobox.currentIndex()

    def setCurrentText(self,txt):
        self.combobox.setCurrentIndex(self.list.index(txt))
         
    
def main():
    app = QApplication(sys.argv)
    diag = Matplot()
    diag.show()
    app.exec_()


if __name__ == "__main__":
    main()