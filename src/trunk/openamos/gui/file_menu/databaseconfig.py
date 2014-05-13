'''
Created on Sep 13, 2010

@author: dhyou
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys, os, shutil

from lxml import etree
from openamos.gui.env import *
from openamos.gui.file_menu.init_page import *
from openamos.gui.file_menu.input_page import *

#from openamos.gui.misc.basic_widgets import *

class DatabaseConfig(QDialog):
    '''
    classdocs
    '''
    def __init__(self, configobject = None, parent = None):
        super(DatabaseConfig, self).__init__(parent)
        '''
        Constructor
        '''
        self.setWindowTitle("Database Configuration")

        pagelayout = QVBoxLayout()
        self.setLayout(pagelayout)

        self.dbinputbox = QGroupBox("Enter database connection details")
        dblayout = QGridLayout()
        self.dbinputbox.setLayout(dblayout)

        protocollabel = QLabel("DB Protocol")
        dblayout.addWidget(protocollabel,1,1)
        self.protocolline = LineEdit()
        dblayout.addWidget(self.protocolline,1,2)
        hostlabel = QLabel("DB Host")
        dblayout.addWidget(hostlabel,2,1)
        self.hostline = LineEdit()
        dblayout.addWidget(self.hostline,2,2)
        dbnamelabel = QLabel("DB Name")
        dblayout.addWidget(dbnamelabel,3,1)
        self.dbnameline = LineEdit()
        dblayout.addWidget(self.dbnameline,3,2)
        usernamelabel = QLabel("Username")
        dblayout.addWidget(usernamelabel,4,1)
        self.usernameline = LineEdit()
        dblayout.addWidget(self.usernameline,4,2)
        passwdlabel = QLabel("Password")
        dblayout.addWidget(passwdlabel,5,1)
        self.passwdline = LineEdit()
        self.passwdline.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        dblayout.addWidget(self.passwdline,5,2)
        pagelayout.addWidget(self.dbinputbox)

        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        pagelayout.addWidget(self.dialogButtonBox)

        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self.storeDatabase)
        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), SLOT("reject()"))


        self.configobject = configobject
        self.protocolline.setText(self.configobject.getConfigElement(DB_CONFIG,DB_PROTOCOL))
        self.hostline.setText(self.configobject.getConfigElement(DB_CONFIG,DB_HOST))
        self.dbnameline.setText(self.configobject.getConfigElement(DB_CONFIG,DB_NAME))
        self.usernameline.setText(self.configobject.getConfigElement(DB_CONFIG,DB_USER))
        self.passwdline.setText(self.configobject.getConfigElement(DB_CONFIG,DB_PASS))

        self.setMinimumSize(350,200)




    def storeDatabase(self):

        dataconfigelt = self.configobject.protree.find(DB_CONFIG)
        if dataconfigelt != None:
            dataconfigelt.set(DB_PROTOCOL, str(self.protocolline.text()))
            dataconfigelt.set(DB_HOST, str(self.hostline.text()))
            dataconfigelt.set(DB_NAME, str(self.dbnameline.text()))
            dataconfigelt.set(DB_USER, str(self.usernameline.text()))
            dataconfigelt.set(DB_PASS, str(self.passwdline.text()))


        QDialog.accept(self)



def main():
    app = QApplication(sys.argv)
    wizard = DatabaseConfig()
    wizard.show()
    app.exec_()

if __name__=="__main__":
    main()
