from PyQt4.QtGui import *
from PyQt4.QtCore import *


class SaveProject(QWizard):

    def __init__(self, parent=None):
        super(SaveProject, self).__init__(parent)
        self.setWindowTitle("Save the project")
        self.showdialog()

    def showdialog(self):
        filename = QFileDialog.getSaveFileName(self, 'Save file',
                                               '/home')
        file = open(filename)
