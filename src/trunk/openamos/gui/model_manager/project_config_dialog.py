'''
Created on Jun 21, 2011

@author: dhyou
'''
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from lxml import etree

from openamos.gui.env import *
from mixed_widgets import *
from openamos.gui.misc.basic_widgets import *
from openamos.gui.env import *


class ProjectConfigDialog(QDialog):
    '''
    classdocs
    '''

    def __init__(self,configobject,element,parent=None):
        super(ProjectConfigDialog, self).__init__(parent)

        self.configobject = configobject
        self.elt = element
        self.isMove = True

        self.setWindowTitle("")
        alllayout = QHBoxLayout()
        self.setLayout(alllayout)

        attributegb = QGroupBox("")
        attrilayout = QVBoxLayout()
        attributegb.setLayout(attrilayout)
        attrilayout.setContentsMargins(0,0,0,0)

        row1 = QWidget(self)
        row1layout = QGridLayout()
        row1.setLayout(row1layout)

        titlelabel = QLabel("Element Title: ")
        titlelabel.setAlignment(Qt.AlignLeft)
        row1layout.addWidget(titlelabel,0,0)

        self.titleline1 = QComboBox()
        self.titleline1.setMinimumWidth(250)
        self.titleline1.addItems(self.titles(str(self.elt.tag)))
        row1layout.addWidget(self.titleline1,1,0)

        dummy1 = QLabel("")
        row1layout.addWidget(dummy1,0,1)

        btnwidget = QWidget(self)
        btnlayout = QHBoxLayout()
        btnwidget.setLayout(btnlayout)
        self.btnsaveas = QPushButton('Insert')
        self.btnsaveas.setMaximumWidth(80)
        if self.titleline1.count() < 2:
            self.btnsaveas.setVisible(False)
        btnlayout.addWidget(self.btnsaveas)
        self.btnsave = QPushButton('Save')
        self.btnsave.setMaximumWidth(80)
        btnlayout.addWidget(self.btnsave)
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Close)
        btnlayout.addWidget(self.dialogButtonBox)

        self.genwidgets = AbstractMixedWidget(self)

        attrilayout.addWidget(row1)
        attrilayout.addWidget(self.genwidgets)
        attrilayout.addWidget(btnwidget)

        self.splitter = QSplitter(Qt.Horizontal)
        self.tree()
        self.splitter.addWidget(attributegb)
#        self.splitter.setSizes([350,450])

        alllayout.addWidget(self.splitter)

        items = self.attributes(str(self.elt.tag))
        self.genwidgets.attriname.addItems(items)

        self.readtree()

        self.connect(self.titleline1, SIGNAL("currentIndexChanged(int)"), self.fillAttr)
        self.connect(self.btnsaveas, SIGNAL("clicked(bool)"), self.saveAsElement)
        self.connect(self.btnsave, SIGNAL("clicked(bool)"), self.saveElement)
        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), SLOT("reject()"))

    def tree(self):
        leftwidget = QWidget()
        leftlayout = QVBoxLayout()
        leftwidget.setLayout(leftlayout)
        leftlayout.setContentsMargins(0,0,0,0)

        tools = QToolBar()
        up_action = self.createaction("",self.moveup,"arrow_up","Move up an element in the tree.")
        down_action = self.createaction("",self.movedown,"arrow_down","Move down an element in the tree.")
        remove_action = self.createaction("",self.remove_element,"delete","Delete the selected element in the tree.")
        tools.addAction(up_action)
        tools.addAction(down_action)
        tools.addAction(remove_action)
        leftlayout.addWidget(tools)

        self.treewidget = QTreeWidget()
        self.treewidget.headerItem().setText(0, "Sub-element Management")

        leftlayout.addWidget(self.treewidget)
        self.splitter.addWidget(leftwidget)

        self.connect(self.treewidget, SIGNAL('itemClicked (QTreeWidgetItem *,int)'), self.showValues)


    def createaction(self, text, slot=None, icon=None,
                     tip=None, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon("./images/%s.png" % icon))
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)

        return action


    def attributes(self,eltname):
        root = self.configobject.def_configs[0].getroot()
        items = []
        for elt in root.getiterator(eltname):
            for key in elt.keys():
                if key not in items:
                    items.append(key)

        return items

    def titles(self,eltname):
        elt = self.configobject.def_configs[0].find(eltname)
        items = []
        items.append(str(eltname))
        for subelt in elt.getchildren():
            cname1 = str(subelt.tag)
            if cname1 not in items:
                items.append(cname1)

                for subsubelt in subelt.getchildren():
                    cname2 = str(subsubelt.tag)
                    if cname2 not in items:
                        items.append(cname2)

        return items


    def showValues(self):
        curitem = self.treewidget.currentItem()
        temp = str(curitem.text(0)).split('-')
        name = temp[0]
        self.genwidgets.attriname.clear()
        self.genwidgets.attriname.addItems(self.attributes(str(curitem.text(0))))
        ind = self.titleline1.findText(name) #str(curitem.text(0)))
        self.titleline1.setCurrentIndex(ind)

        num = self.genwidgets.attritable.rowCount()
        for i in range(num):
            self.genwidgets.attritable.removeRow(0)

#        for key in curitem.attribute.keys():
        for i in range(len(curitem.sets)):
            key = curitem.sets[i]
            value = curitem.values[i]
#            value = curitem.attribute[key]

            self.genwidgets.attritable.insertRow(self.genwidgets.attritable.rowCount())
            attritem = QTableWidgetItem()
            attritem.setText(str(key))
            attritem.setFlags(attritem.flags() & ~Qt.ItemIsEditable)
            self.genwidgets.attritable.setItem(self.genwidgets.attritable.rowCount()-1, 0, attritem)

            varitem = QTableWidgetItem()
            varitem.setText(value)
            self.genwidgets.attritable.setItem(self.genwidgets.attritable.rowCount()-1, 1, varitem)


    def readtree(self):
        sets1 = []
        values1 = []
        for key in self.elt.keys():
            sets1.append(str(key))
            values1.append(str(self.elt.get(key)))

        treeelt = TreeWidgetItem(self.treewidget, sets1, values1)
        treeelt.setText(0, str(self.elt.tag))
        self.treewidget.setCurrentItem(treeelt)
        self.showValues()

        for elt1 in self.elt.getchildren():

            subtreeelt1 = self.subreadtree(elt1, treeelt)
            for subelt1 in elt1.getchildren():
                subtreeelt2 = self.subreadtree(subelt1, subtreeelt1)
#             sets2 = []
#             values2 = []
#             tlabel = str(elt1.tag) + "-"
#
#             for key in elt1.keys():
#                 sets2.append(str(key))
#                 values2.append(str(elt1.get(key)))
#                 tlabel = tlabel + str(key) + ":" + str(elt1.get(key)) + " "
#
#             subitem = TreeWidgetItem(treeelt, sets2, values2)
#             subitem.setText(0, tlabel) #str(elt1.tag))

    def subreadtree(self, elt, treeelt):

        sets2 = []
        values2 = []
        tlabel = str(elt.tag) + "-"

        for key in elt.keys():
            sets2.append(str(key))
            values2.append(str(elt.get(key)))
            tlabel = tlabel + str(key) + ":" + str(elt.get(key)) + " "

        subitem = TreeWidgetItem(treeelt, sets2, values2)
        subitem.setText(0, tlabel) #str(elt1.tag))

        return subitem



    def fillAttr(self):
        name = str(self.titleline1.currentText())
        self.genwidgets.attriname.clear()
        self.genwidgets.attriname.addItems(self.attributes(name))

        item = self.treewidget.currentItem()
        if name != str(item.text(0)):
            numrows = self.genwidgets.attritable.rowCount()
            for i in range(numrows):
                self.genwidgets.attritable.removeRow(0)


    def saveAsElement(self):

#        title = str(self.titleline1.currentText())
#        treeitem = self.treewidget.currentItem()
#        father = treeitem.parent()
#        xmlitem = self.elt
#
#        if father != None:
#            i = father.indexOfChild(treeitem)
#            childs = xmlitem.getchildren()
#            xmlitem = childs[i]
#            temp = father.parent()
#            father = temp


        title = str(self.titleline1.currentText())
        sets = []
        values = []
        element = etree.Element(title)
        tlabel = title + "-"
        for i in range(self.genwidgets.attritable.rowCount()):
            name = str((self.genwidgets.attritable.item(i,0)).text())
            value = str((self.genwidgets.attritable.item(i,1)).text())
            element.set(name,value)
            sets.append(name)
            values.append(value)
            tlabel = tlabel + name + ":" + value + " "

        item = self.treewidget.currentItem()
        father = item.parent()
        if father != None:
            item = father

        if item.text(0) != title:
            self.elt.append(element)
            treeelt = TreeWidgetItem(item,sets,values)
            treeelt.setText(0, tlabel)


    def saveElement(self):
        length = self.genwidgets.attritable.rowCount()
        if length > 0 and self.elt != None:

            item = self.treewidget.currentItem()
            temp = str(item.text(0)).split('-')
            name = str(temp[0])
            if str(self.titleline1.currentText()) == name:
#            if str(self.titleline1.currentText()) == str(item.text(0)):
                father = item.parent()
                child = self.elt
                if father != None:
                    i = father.indexOfChild(item)
                    childs = child.getchildren()
                    child = childs[i]

                sets = []
                values = []
                for i in range(self.genwidgets.attritable.rowCount()):
                    name = str((self.genwidgets.attritable.item(i,0)).text())
                    value = str((self.genwidgets.attritable.item(i,1)).text())
                    child.set(name,value)
                    sets.append(name)
                    values.append(value)

                item.sets = sets
                item.values = values


    def moveup(self):

        if self.isMove == True:
            self.isMove = False
            item = self.treewidget.currentItem()
            father = item.parent()

            if father != None:
                i = father.indexOfChild(item)
                if i > 0:
                    father.removeChild(item)
                    father.insertChild(i-1, item)
                    self.treewidget.setCurrentItem(item)

                    childs = self.elt.getchildren()
                    child = childs[i]
                    self.elt.remove(child)
                    self.elt.insert(i-1, child)

            self.isMove = True


    def movedown(self):

        if self.isMove == True:
            self.isMove = False
            item = self.treewidget.currentItem()
            father = item.parent()

            if father != None:
                i = father.indexOfChild(item)
                max_i = father.childCount()
                if i < max_i-1:
                    father.removeChild(item)
                    father.insertChild(i+1, item)
                    self.treewidget.setCurrentItem(item)

                    childs = self.elt.getchildren()
                    child = childs[i]
                    self.elt.remove(child)
                    self.elt.insert(i+1, child)

            self.isMove = True

    def remove_element(self):
        reply = QMessageBox.question(None, 'Remove', "Are you sure to remove?",
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            item = self.treewidget.currentItem()
            father = item.parent()
            if father != None:
                i = father.indexOfChild(item)
                if i >= 0:
                    self.treewidget.removeItemWidget(item,0)

                    father = self.elt
                    childs = father.getchildren()
                    child = childs[i]
                    father.remove(child)

#    def findIndex(self,item):
#        index = []
#        father = None
#
#        if item != None:
#            father = item.parent()
#
#        while father != None:
#            i = father.indexOfChild(item)
#            index.append(i)
#            item = father
#            father = father.parent()
#
#        index.reverse()
#        return index
