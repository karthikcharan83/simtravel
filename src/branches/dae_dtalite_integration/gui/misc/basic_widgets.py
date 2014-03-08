from PyQt4.QtCore import *
from PyQt4.QtGui import *

import re

from openamos.gui.errors import *

class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)

    def check(self, text):
        text = self.text()
        try:
            if len(text) == 0:
                raise TextError, "Enter a non-empty string"
            if not re.match("[A-Za-z]",text[0]):
                text = text[1:]
                raise TextError, "First character has to be a alphabet"

            for i in text[1:]:
                if not re.match("[A-Za-z_0-9]", i):
                    text.replace(i, '')
                    raise TextError, "Name can only comprise of alphabets and an underscore (_)"
        except TextError, e:
            QMessageBox.information(self, "Warning",
                                    "%s" %e,
                                    QMessageBox.Ok)
            self.setText(text)
            self.selectAll()
            self.setFocus()
        return True

class ComboBoxFolder(QComboBox):
    def __init__(self, parent=None):
        super(ComboBoxFolder, self).__init__(parent)

    def browseFolder(self, index):
        if index  == self.count()-1:
            location = QFileDialog.getExistingDirectory(self, QString("Project Location"), "/home", QFileDialog.ShowDirsOnly)
            if not location.isEmpty():
                indexOfFolder = self.isPresent(location)
                if indexOfFolder is None:
                    self.insertItem(0, QString(location))
                    self.setCurrentIndex(0)
                else:
                    self.setCurrentIndex(indexOfFolder)
            else:
                self.setCurrentIndex(0)

    def isPresent(self, location):
        for i in range(self.count()):
            if location == self.itemText(i):
                return i
        return None
    
class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, sets, values):
        super(TreeWidgetItem, self).__init__(parent)
#        self.attribute = attr
        self.sets = sets
        self.values = values