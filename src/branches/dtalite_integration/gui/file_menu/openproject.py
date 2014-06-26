from PyQt4.QtGui import *
from PyQt4.QtCore import *


class OpenProject(QFileDialog):

    def __init__(self, parent=None):
        super(OpenProject, self).__init__(parent)
        self.file = self.getOpenFileName(parent, "Browse to select a project configuration file", "../configs/mag_zone/",
                                         "XML File (*.xml)")
