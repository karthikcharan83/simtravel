from PyQt4.QtGui import *
from PyQt4.QtCore import *

from openamos.gui.misc.basic_widgets import *


class InitPage(QWizardPage):

    def __init__(self, parent=None):
        super(InitPage, self).__init__(parent)

        self.nameDummy = True
        self.locationDummy = True
        self.setTitle("Step 1: Project Details")
        pagelayout = QVBoxLayout()
        self.setLayout(pagelayout)

        self.pronamelabel = QLabel("a. Enter project name")
        self.pronameline = LineEdit()
        pagelayout.addWidget(self.pronamelabel)
        pagelayout.addWidget(self.pronameline)

        self.proloclabel = QLabel("b. Select a project location")
        self.proloccombobox = ComboBoxFolder()
        self.proloccombobox.addItems(
            [QString(""), QString("Browse to select folder...")])
        pagelayout.addWidget(self.proloclabel)
        pagelayout.addWidget(self.proloccombobox)

        self.prodesclabel = QLabel("c. Enter project description (Optional)")
        self.prodesctext = QTextEdit()
        pagelayout.addWidget(self.prodesclabel)
        pagelayout.addWidget(self.prodesctext)

        self.connect(self.pronameline, SIGNAL(
            "textEdited(const QString&)"), self.nameCheck)
        self.connect(self.proloccombobox, SIGNAL(
            "activated(int)"), self.proloccombobox.browseFolder)
        self.connect(self.proloccombobox, SIGNAL(
            "currentIndexChanged(int)"), self.locationCheck)

    def nameCheck(self, text):
        self.nameDummy = self.pronameline.check(text)
        self.emit(SIGNAL("completeChanged()"))

    def locationCheck(self, int):
        if self.proloccombobox.currentText() == '':
            self.locationDummy = False
        else:
            self.locationDummy = True
        self.emit(SIGNAL("completeChanged()"))

    def isComplete(self):
        validate = self.nameDummy and self.locationDummy
        return validate
