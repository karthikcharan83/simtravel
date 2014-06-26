from PyQt4.QtGui import *
from PyQt4.QtCore import *
from lxml import etree
import sys
import os
import shutil

from openamos.gui.env import *
from openamos.gui.file_menu.init_page import *
from openamos.gui.file_menu.input_page import *

from openamos.core.config import *


class NewProject(QWizard):

    def __init__(self, parent=None):
        super(NewProject, self).__init__(parent)
        self.setWindowTitle("Project Setup Wizard")
        self.setWizardStyle(QWizard.ClassicStyle)

        self.page1 = InitPage()
        self.addPage(self.page1)
        self.page2 = InputPage()
        self.addPage(self.page2)

        self.configtree = None

    def reject(self):
        reply = QMessageBox.warning(None, "Project Setup Wizard",
                                    QString(
                                        "Would you like to exit project setup?"),
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QWizard.reject(self)
            return None

    def accept(self):
        self.createProConfig()
        QWizard.accept(self)

    def createProConfig(self):
        masterconfig = '../configs/mag_zone/config_before_malta.xml'
        proconfig = ConfigObject(configfileloc=masterconfig)

        proelt = proconfig.getConfigElt(PROJECT)
        proelt.set(NAME, str(self.page1.pronameline.text()))
        proelt.set(
            LOCATION, str(self.page1.proloccombobox.currentText()) + '/' + proelt.get(NAME))

        dbelt = proconfig.getConfigElt(DB_CONFIG)
        dbelt.set(DB_HOST, str(self.page2.hostnameline.text()))
        dbelt.set(DB_USER, str(self.page2.usernameline.text()))
        dbelt.set(DB_PASS, str(self.page2.passwdline.text()))
        if self.page2.inputdbradio.isChecked():
            dbelt.set(DB_NAME, str(self.page2.inputdbline.text()))
#        configroot = etree.Element(PROJECT_CONFIG)
#        configtree = etree.ElementTree(configroot)
#
#        project = etree.SubElement(configroot, PROJECT)
#        project.set(NAME, str(self.page1.pronameline.text()))
#        project.set(LOCATION, str(self.page1.proloccombobox.currentText()) + '/' + project.get(NAME))
#        project.set(SEED, SEED_DEF)
#        project.set(SUBSAMPLE, SUBSAMPLE_DEF)
        #projectname = etree.SubElement(configroot, PROJECT_NAME)
        #projectname.text = str(self.page1.pronameline.text())

        #projecthome = etree.SubElement(configroot, PROJECT_HOME)
        #projecthome.text = str(self.page1.proloccombobox.currentText())

#        dbconfig = etree.SubElement(configroot, DB_CONFIG)
#        dbconfig.set(DB_PROTOCOL, POSTGRES)
#        dbconfig.set(DB_HOST, str(self.page2.hostnameline.text()))
#        dbconfig.set(DB_USER, str(self.page2.usernameline.text()))
#        dbconfig.set(DB_PASS, str(self.page2.passwdline.text()))
#
#        if self.page2.inputdbradio.isChecked():
#            dbconfig.set(DB_NAME, str(self.page2.inputdbline.text()))
            #inputdb = etree.SubElement(configroot, DB_NAME)
            #inputdb.text = str(self.page2.inputdbline.text())

#        dbtables = etree.SubElement(configroot, DB_TABLES)
#        self.create_table_element(dbtables,TABLE_PER,'houseid,personid','1')
#        self.create_table_element(dbtables,TABLE_HH,'houseid','2')
#        self.create_table_element(dbtables,'households_r','houseid')
#        self.create_table_element(dbtables,'vehicles_r','houseid',countkey='vehid')
#        self.create_table_element(dbtables,'tsp_r','houseid,personid')
#        self.create_table_element(dbtables,'schedule_r','houseid,personid',countkey='scheduleid')

#        configpath = proelt.get(LOCATION)
#        if not os.path.exists(configpath):
#            os.mkdir(configpath)
#        configfileloc = configpath + os.path.sep + proelt.get(NAME) + '.xml'
        #configfile = open(configfileloc, 'w')
        #configtree.write(configfileloc, pretty_print=True)
        # configfile.close()

        proconfig.write()
        self.configtree = proconfig.protree

#    def create_table_element(self,parelt,table,key,order=None,countkey=None):
#        tab = etree.SubElement(parelt, TABLEELT)
#        tab.set(TABLE,table)
#        tab.set(KEY,key)
#        if order!=None:
#            tab.set(ORDER,order)
#        elif countkey!=None:
#            tab.set(COUNT_KEY,countkey)


def main():
    app = QApplication(sys.argv)
    wizard = NewProject()
    wizard.show()
    app.exec_()

if __name__ == "__main__":
    main()
