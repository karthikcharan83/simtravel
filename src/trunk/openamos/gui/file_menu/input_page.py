from PyQt4.QtGui import *
from PyQt4.QtCore import *

from openamos.gui.misc.basic_widgets import *

class InputPage(QWizardPage):
    def __init__(self, parent=None):
        super(InputPage, self).__init__(parent)

        self.setTitle("Step 2: Data Input Source")
        pagelayout = QVBoxLayout()
        self.setLayout(pagelayout)

        self.dbinputbox = QGroupBox("a. Enter database connection details")
        dblayout = QGridLayout()
        self.dbinputbox.setLayout(dblayout)
        hostnamelabel = QLabel("Hostname")
        dblayout.addWidget(hostnamelabel,1,1)
        self.hostnameline = LineEdit()
        dblayout.addWidget(self.hostnameline,1,2)
        usernamelabel = QLabel("Username")
        dblayout.addWidget(usernamelabel,2,1)
        self.usernameline = LineEdit()
        dblayout.addWidget(self.usernameline,2,2)
        passwdlabel = QLabel("Password")
        dblayout.addWidget(passwdlabel,3,1)
        self.passwdline = LineEdit()
        self.passwdline.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        dblayout.addWidget(self.passwdline,3,2)
        pagelayout.addWidget(self.dbinputbox)

        inputgroupbox= QGroupBox("b. Will you provide a database as input?")
        self.inputdbradio = QRadioButton("Yes")
        self.inputfilesradio = QRadioButton("No")
        self.inputdbradio.setChecked(True)
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.inputdbradio)
        buttonlayout.addWidget(self.inputfilesradio)
        buttonwidget = QWidget()
        buttonwidget.setLayout(buttonlayout)
        inputboxlayout = QVBoxLayout()
        inputgroupbox.setLayout(inputboxlayout)
        inputboxlayout.addWidget(buttonwidget)
        pagelayout.addWidget(inputgroupbox)


        inputdblabel = QLabel("Enter the name of input database")
        self.inputdbline = LineEdit()
        inputboxlayout.addWidget(inputdblabel)
        inputboxlayout.addWidget(self.inputdbline)
        inputfileslabel = QLabel("Select the location of input files")
        self.inputcombobox = ComboBoxFolder()
        self.inputcombobox.addItems([QString(""), QString("Browse to select folder...")])
        inputboxlayout.addWidget(inputfileslabel)
        inputboxlayout.addWidget(self.inputcombobox)
        self.inputcombobox.setEnabled(False)

        self.connect(self.inputfilesradio, SIGNAL("toggled(bool)"), self.inputAction)
        self.connect(self.inputcombobox, SIGNAL("activated(int)"), self.inputcombobox.browseFolder)

    def inputAction(self, checked):
        if checked:
            self.inputdbline.setEnabled(False)
            self.inputcombobox.setEnabled(True)
        else:
            self.inputdbline.setEnabled(True)
            self.inputcombobox.setEnabled(False)

        self.emit(SIGNAL("completeChanged()"))
