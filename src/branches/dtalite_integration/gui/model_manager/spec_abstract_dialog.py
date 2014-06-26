'''
Created on Apr 19, 2010

@author: bsana
'''

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from copy import deepcopy

from lxml import etree

from openamos.gui.env import *
from spec_model_widgets import *

from openamos.core.database_management.database_connection import *
from openamos.core.database_management.database_configuration import *


class AbtractSpecDialog(QDialog):

    '''
    classdocs
    '''

    def __init__(self, configobject, key, title='', index=None, parent=None):
        super(AbtractSpecDialog, self).__init__(parent)

        self.setWindowTitle(title)
        self.setMinimumSize(800, 550)

        self.configobject = configobject
        self.modelkey = key
        self.modelindex = index

        if index == None:
            model = self.configobject.modelSpecInConfig(self.modelkey)
        if index != None:
            model = self.configobject.getElement(index)

        self.themodel = model
        self.populateFromDatabase()

        wholelayout = QVBoxLayout()
        self.setLayout(wholelayout)
#        wholewidget = QWidget()
#        self.glayout = QGridLayout()
#        wholewidget.setLayout(self.glayout)

        self.modeltypegb = QGroupBox("")  # "Model Type")
        modeltypegblayout = QGridLayout()
        self.modeltypegb.setMaximumHeight(60)
        self.modeltypegb.setLayout(modeltypegblayout)
        modeltypelb = QLabel("Model Type: ")
        self.modeltypecb = QComboBox()
        self.modeltypecb.addItems([QString(PROB_MODEL), QString(COUNT_MODEL),
                                   QString(LINEAR_MODEL), QString(
                                       SF_MODEL), QString(LOGREG_MODEL),
                                   QString(GC_MNL_MODEL), QString(MNL_MODEL),
                                   QString(ORD_MODEL), QString(
                                       NL_MODEL), QString(LOGSF_MODEL),
                                   QString(RECON_SCHEDULE), QString(
                                       FIXEDACT_SCHEDULE),
                                   QString(AGGACT_SCHEDULE), QString(CHILD_ALLOCAT), QString(
                                       CHILD_ALLOCAT_TERM), QString(CHILD_DEPEND), QString(PERS_TRIP_ARRIVAL),
                                   QString(SCH_ADJUST), QString(IDEN_UNIQUE), QString(IDEN_INDIVIDUAL)])

        self.specialmodel = [IDEN_INDIVIDUAL, RECON_SCHEDULE, FIXEDACT_SCHEDULE, AGGACT_SCHEDULE, CHILD_ALLOCAT,
                             CHILD_ALLOCAT_TERM, CHILD_DEPEND, PERS_TRIP_ARRIVAL, IDEN_UNIQUE, SCH_ADJUST, ]

        dependentlb = QLabel("Dependent Variable: ")
        self.dependentcb = QComboBox()
        self.dependentcb.addItems(self.dependents())
        modeltypegblayout.addWidget(modeltypelb, 0, 0)
        modeltypegblayout.addWidget(self.modeltypecb, 1, 0)
        modeltypegblayout.addWidget(dependentlb, 0, 1)
        modeltypegblayout.addWidget(self.dependentcb, 1, 1)

        self.attributegb = QGroupBox("")
        attributegblayout = QGridLayout()  # QHBoxLayout()
        self.attributegb.setLayout(attributegblayout)
        self.attributegb.setVisible(False)

        attriwidget1 = QWidget()
        attrilayout1 = QGridLayout()
        attriwidget1.setLayout(attrilayout1)
        namelb = QLabel("Model Name: ")
        vertexlb = QLabel("Vertex: ")
        lowerlb = QLabel("Lower Threshold: ")
        upperlb = QLabel("Upper Threshold: ")
        attributegblayout.addWidget(namelb, 0, 0)
        attributegblayout.addWidget(vertexlb, 1, 0)
        attributegblayout.addWidget(lowerlb, 2, 0)
        attributegblayout.addWidget(upperlb, 3, 0)

        self.nametxt = LineEdit()
        self.vertexcb = QComboBox()
        self.lowertxt = LineEdit()
        self.uppertxt = LineEdit()
        self.nametxt.setMaximumWidth(250)
        self.vertexcb.setMaximumWidth(250)
        self.lowertxt.setMaximumWidth(250)
        self.uppertxt.setMaximumWidth(250)

        attributegblayout.addWidget(self.nametxt, 0, 1)
        attributegblayout.addWidget(self.vertexcb, 1, 1)
        attributegblayout.addWidget(self.lowertxt, 2, 1)
        attributegblayout.addWidget(self.uppertxt, 3, 1)

#        self.attrinamecb = QComboBox()
#        attrilayout1.addWidget(attriname,0,0)
#        attrilayout1.addWidget(self.attrinamecb,0,1)
#
#        selectvalue = QLabel("Select Attribute Value: ")
#        self.attrivaluecb = QComboBox()
#        entervalue = QLabel("or Enter Attribute Value: ")
#        self.attrivaluetxt = LineEdit()
#        attrilayout1.addWidget(selectvalue,1,0)
#        attrilayout1.addWidget(self.attrivaluecb,1,1)
#        attrilayout1.addWidget(entervalue,2,0)
#        attrilayout1.addWidget(self.attrivaluetxt,2,1)
#
#        attriwidget2 = QWidget()
#        attrilayout2 = QVBoxLayout()
#        attriwidget2.setLayout(attrilayout2)
#        self.addbutton = QPushButton('>>')
#        self.addbutton.setMaximumWidth(80)
#        attrilayout2.addWidget(self.addbutton)
#        self.delbutton = QPushButton('<<')
#        self.delbutton.setMaximumWidth(80)
#        attrilayout2.addWidget(self.delbutton)
#
#        self.attritable = QTableWidget(self)
#        self.attritable.setRowCount(0)
#        self.attritable.setColumnCount(2)
#        self.attritable.setHorizontalHeaderLabels(['Attribute', 'Value'])
# self.choicetable.setSelectionBehavior(QAbstractItemView.SelectRows)
#        self.attritable.setSelectionMode(QAbstractItemView.SingleSelection)
#        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
#        self.attritable.setSizePolicy(sizePolicy)
#        self.attritable.horizontalHeader().setResizeMode(0,1)
#        self.attritable.horizontalHeader().setResizeMode(1,1)
#
#        attributegblayout.addWidget(attriwidget1)
#        attributegblayout.addWidget(attriwidget2)
#        attributegblayout.addWidget(self.attritable)
#        self.glayout.addWidget(self.attributegb,2,0)
        self.fill_attribute(model)

        self.filters = FilterWidget("Sub-Population", self)
        self.filters.setVisible(False)
#        self.glayout.addWidget(self.filters,4,0)

        tool3 = QToolBar()
        tool3.setMaximumHeight(30)
        show_action3 = self.createaction("", self.showgb3, "arrow", "")
        tool3.addAction(show_action3)
#        self.glayout.addWidget(tool3,5,0)

        self.untilcondition = FilterWidget("Run Condition", self)
        self.untilcondition.setVisible(False)
#        self.glayout.addWidget(self.untilcondition,6,0)

        self.modwidget = QWidget()
#        self.glayout.addWidget(self.modwidget,8,0)

        buttonwidget = QWidget(self)
        buttonlayout = QHBoxLayout()
        buttonlayout.setContentsMargins(0, 11, 0, 11)
        buttonwidget.setLayout(buttonlayout)
        self.defaultbutton = QPushButton("Default Model")
        buttonlayout.addWidget(self.defaultbutton)
        self.dialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonlayout.addWidget(self.dialogButtonBox)

        self.tabwidget = QTabWidget()
        self.tabwidget.addTab(self.attributegb, "Model Attributes")
        self.tabwidget.addTab(self.filters, "Sub-Population")
        self.tabwidget.addTab(self.untilcondition, "Run Conditions")

#        wholelayout.addWidget(scrollArea)
        wholelayout.addWidget(self.modeltypegb)
        wholelayout.addWidget(self.tabwidget)
        wholelayout.addWidget(buttonwidget)

        self.connect(self.modeltypecb, SIGNAL(
            "currentIndexChanged(int)"), self.changeModelWidget)
        self.connect(
            self.dialogButtonBox, SIGNAL("accepted()"), self.storeSpec)
        self.connect(
            self.dialogButtonBox, SIGNAL("rejected()"), SLOT("reject()"))
        self.connect(
            self.defaultbutton, SIGNAL("clicked(bool)"), self.defaultModel)
        self.connect(self.dependentcb, SIGNAL(
            "currentIndexChanged(int)"), self.addDependent)

        if model.tag != COMP:
            self.loadFromConfigObject2(model)
        else:
            self.modeltypecb.setCurrentIndex(0)
            self.changeModelWidget()

        # In order to compare between previous and current model
        self.models = []

    def fill_attribute(self, model):
        elements = self.configobject.getDElements("Model")
        values = []
        values.append("")
        for elt in elements:
            for key in elt.keys():
                if key == VERTEX:
                    value = str(elt.get(key)).lower()
                    if value not in values:
                        values.append(value)

        self.vertexcb.addItems(values)

        if model.tag != COMP:
            self.nametxt.setText(str(model.get(NAME)))
            if VERTEX in model.keys():
                value = str(model.get(VERTEX))
                ind = self.vertexcb.findText(value)
                self.vertexcb.setCurrentIndex(ind)
            if "lower_threshold" in model.keys():
                self.lowertxt.setText(str(model.get("lower_threshold")))
            if "upper_threshold" in model.keys():
                self.uppertxt.setText(str(model.get("upper_threshold")))

    def addDependent(self):
        current = str(self.dependentcb.currentText())
        if current == "Other":
            dvalue, ok = QInputDialog.getText(
                self, "", "Enter dependent variable name:")
            if ok:
                self.dependentcb.addItem(str(dvalue))
                ind = self.dependentcb.findText(str(dvalue))
                self.dependentcb.setCurrentIndex(ind)

    def dependents(self):
        elements = self.configobject.getElements(DEPVARIABLE)
        items = []
        for elt in elements:
            value = elt.get(COLUMN)
            if value not in items:
                items.append(value)
        items.append("Other")

        return items

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

    def showgb1(self):
        self.attributegb.setVisible(True)
        self.filters.setVisible(False)
        self.untilcondition.setVisible(False)
        self.modwidget.setVisible(False)

    def showgb2(self):
        self.attributegb.setVisible(False)
        self.filters.setVisible(True)
        self.untilcondition.setVisible(False)
        self.modwidget.setVisible(False)

    def showgb3(self):
        self.attributegb.setVisible(False)
        self.filters.setVisible(False)
        self.untilcondition.setVisible(True)
        self.modwidget.setVisible(False)

    def showgb4(self):
        self.attributegb.setVisible(False)
        self.filters.setVisible(False)
        self.untilcondition.setVisible(False)
        self.modwidget.setVisible(True)

    def loadFromConfigObject1(self):
        modelspecified = self.configobject.modelSpecInConfig(self.modelkey)
        # self.loadFromConfigObject2(modelspecified)

    def loadFromConfigObject2(self, modelspecified):

        if modelspecified is not None:
            form = modelspecified.get(FORMULATION)
            if form == MODELFORM_REG:
                type = modelspecified.get(MODELTYPE)
                if type == SF_MODEL:
                    modtxt = SF_MODEL
                elif type == LOGREG_MODEL:
                    modtxt = LOGREG_MODEL
                elif type == LOGSF_MODEL:
                    modtxt = LOGSF_MODEL
                elif type == LINEAR_MODEL:
                    modtxt = LINEAR_MODEL
            elif form == MODELFORM_CNT:
                modtxt = MODELFORM_CNT
                type = modelspecified.get(MODELTYPE)
            elif form == MODELFORM_ORD:
                modtxt = ORD_MODEL
                type = modelspecified.get(MODELTYPE)
            elif form == MODELFORM_MNL:
                type = modelspecified.get(MODELTYPE)
                if type == ALTSPEC:
                    modtxt = MNL_MODEL
                else:
                    modtxt = GC_MNL_MODEL
            elif form == MODELFORM_NL:
                modtxt = NL_MODEL
            elif form == MODELFORM_PD:
                modtxt = PROB_MODEL
            elif form == RECON_SCHEDULE:
                modtxt = RECON_SCHEDULE
            elif form == FIXEDACT_SCHEDULE:
                modtxt = FIXEDACT_SCHEDULE
            elif form == AGGACT_SCHEDULE:
                modtxt = AGGACT_SCHEDULE
            elif form == CHILD_ALLOCAT:
                modtxt = CHILD_ALLOCAT
            elif form == CHILD_ALLOCAT_TERM:
                modtxt = CHILD_ALLOCAT_TERM
            elif form == CHILD_DEPEND:
                modtxt = CHILD_DEPEND
            elif form == SCH_ADJUST:
                modtxt = SCH_ADJUST
            elif form == PERS_TRIP_ARRIVAL:
                modtxt = PERS_TRIP_ARRIVAL
            elif form == IDEN_UNIQUE:
                modtxt = IDEN_UNIQUE
            elif form == IDEN_INDIVIDUAL:
                modtxt = IDEN_INDIVIDUAL

            ind = self.modeltypecb.findText(modtxt)
            self.modeltypecb.setCurrentIndex(ind)

            print "%s - %s" % (modtxt, ind)

        self.changeModelWidget()
#        self.populateColumns()

        if modelspecified is not None:
            self.populateDependent(modelspecified)
            self.populateRununtilWidget(modelspecified)
            self.populateFilterWidget(modelspecified)
            seed = int(modelspecified.get(SEED))
            self.modwidget.seedline.setValue(seed)
            formtext = self.modeltypecb.currentText()

            if formtext == PROB_MODEL:
                self.populateAltsWidget(modelspecified)
                self.populateVarsWidget(modelspecified)
            if formtext == SF_MODEL:
                self.populateVarsWidget(modelspecified)
                for varianceelt in modelspecified.getiterator(VARIANCE):
                    if MODELTYPE in varianceelt.keys():
                        self.modwidget.varianceuline.setText(
                            varianceelt.get(VALUE))
                    else:
                        self.modwidget.variancevline.setText(
                            varianceelt.get(VALUE))
            if formtext == LOGSF_MODEL:
                self.populateVarsWidget(modelspecified)
                for varianceelt in modelspecified.getiterator(VARIANCE):
                    if MODELTYPE in varianceelt.keys():
                        self.modwidget.varianceuline.setText(
                            varianceelt.get(VALUE))
                    else:
                        self.modwidget.variancevline.setText(
                            varianceelt.get(VALUE))
            if formtext == LOGREG_MODEL or self.modeltypecb.currentText() == LINEAR_MODEL or formtext == IDEN_UNIQUE:
                self.populateVarsWidget(modelspecified)
                for varianceelt in modelspecified.getiterator(VARIANCE):
                    self.modwidget.variancevline.setText(
                        varianceelt.get(VALUE))
            if formtext == COUNT_MODEL:
                self.populateVarsWidget(modelspecified)
                self.populateAltsWidget(modelspecified)
                if type == NEGBIN_MODEL:
                    varianceelt = modelspecified.find(VARIANCE)
                    self.modwidget.odline.setText(varianceelt.get(VALUE))
                else:
                    self.modwidget.poiradio.setChecked(True)
            if formtext == ORD_MODEL:
                self.populateVarsWidget(modelspecified)
                self.populateOrdAltsWidget(modelspecified)
                if type == PROBIT:
                    self.modwidget.probradio.setChecked(True)
            if formtext == GC_MNL_MODEL:
                self.populateVarsWidget(modelspecified)
                self.populateAltsWidget(modelspecified)
            if formtext == MNL_MODEL:
                self.populateAltsWidget(modelspecified)
                self.modwidget.specs = {}
                for altelt in modelspecified.getiterator(ALTERNATIVE):
                    altspecs = []
                    for varelt in altelt.getiterator(VARIABLE):
                        varspec = []
                        varspec.append(varelt.get(TABLE))
                        varspec.append(varelt.get(COLUMN))
                        varspec.append(varelt.get(COEFF))
                        altspecs.append(varspec)
                    self.modwidget.specs[altelt.get(ID)] = altspecs
            if formtext == NL_MODEL:
                self.modwidget.specs = {}
                for altelt in modelspecified.getiterator(ALTERNATIVE):
                    altstable = self.modwidget.choicetable
                    altstable.insertRow(altstable.rowCount())

                    altitem = QTableWidgetItem()
                    alt = altelt.get(ID)
                    altbranch = altelt.get(BRANCH)
                    if altbranch != 'root':
                        alt = (altbranch.split('/', 1))[1] + '/' + alt
                    altitem.setText(alt)
                    altstable.setItem(altstable.rowCount() - 1, 0, altitem)

                    altspecs = []
                    for varelt in altelt.getiterator(VARIABLE):
                        varspec = []
                        varspec.append(varelt.get(TABLE))
                        varspec.append(varelt.get(COLUMN))
                        varspec.append(varelt.get(COEFF))
                        altspecs.append(varspec)
                    self.modwidget.specs[alt] = altspecs
                for neselt in modelspecified.getiterator(BRANCH):
                    nestable = self.modwidget.nesttable
                    nestable.insertRow(nestable.rowCount())
                    nesname = QTableWidgetItem()
                    nesname.setText(neselt.get(NAME))
                    nestable.setItem(nestable.rowCount() - 1, 0, nesname)
                    nescoeff = QTableWidgetItem()
                    nescoeff.setText(neselt.get(COEFF))
                    nestable.setItem(nestable.rowCount() - 1, 1, nescoeff)
            if formtext == RECON_SCHEDULE or formtext == FIXEDACT_SCHEDULE or formtext == AGGACT_SCHEDULE or formtext == CHILD_ALLOCAT or \
                    formtext == SCH_ADJUST or formtext == PERS_TRIP_ARRIVAL or formtext == IDEN_INDIVIDUAL or formtext == CHILD_ALLOCAT_TERM or formtext == CHILD_DEPEND:
                i = 0
                for altelt in modelspecified.getchildren():
                    if altelt.tag != "DependentVariable":
                        if altelt.tag == "ActivityAttributes":
                            key = "Activity Attributes"
                        elif altelt.tag == "DailyStatus":
                            key = "Daily Status"
                        else:
                            key = str(altelt.tag)

                        altspecs = []
                        for varelt in altelt.getchildren():
                            print "%s - %s" % (key, varelt.tag)
                            varspec = []
                            varspec.append(str(varelt.tag))
                            varspec.append(varelt.get(TABLE))
                            varspec.append(varelt.get(COLUMN))
                            altspecs.append(varspec)
                        self.modwidget.specs[key] = altspecs
                        i = i + 1

    def populateDependent(self, modelelt):
        set = modelelt.find(DEPVARIABLE)
        if set <> None:
            value = str(set.get(COLUMN))
            ind = self.dependentcb.findText(value)
            self.dependentcb.setCurrentIndex(ind)

    def populateRununtilWidget(self, modelelt):
        set = modelelt.find(RUNUNTILSET)
        if set <> None:
            if set.get(MODELTYPE) == 'and':
                self.untilcondition.logical.setCurrentIndex(0)
            else:
                self.untilcondition.logical.setCurrentIndex(1)

        conditions = modelelt.findall(RUNUNTIL)
        if len(conditions) > 0:
            self.untilcondition.remove()
            for i in range(len(conditions)):
                self.untilcondition.addFiter()
            i = 0
            for filt in modelelt.getiterator(RUNUNTIL):
                tempkey = filt.keys()
                ind = self.untilcondition.conditions[
                    i].subpoptab.findText(filt.get(TABLE))
                self.untilcondition.conditions[
                    i].subpoptab.setCurrentIndex(ind)
                if str(filt.get(TABLE)) != "runtime":
                    self.untilcondition.conditions[
                        i].subpopvartext.setDisabled(True)
                    self.untilcondition.conditions[
                        i].subpopvartext.setVisible(False)
                    self.untilcondition.conditions[
                        i].subpopvar.setDisabled(False)
                    self.untilcondition.conditions[
                        i].subpopvar.setVisible(True)
                    ind = self.untilcondition.conditions[
                        i].subpopvar.findText(filt.get(COLUMN))
                    self.untilcondition.conditions[
                        i].subpopvar.setCurrentIndex(ind)
                else:
                    self.untilcondition.conditions[
                        i].subpopvartext.setDisabled(False)
                    self.untilcondition.conditions[
                        i].subpopvartext.setVisible(True)
                    self.untilcondition.conditions[
                        i].subpopvar.setDisabled(True)
                    self.untilcondition.conditions[
                        i].subpopvar.setVisible(False)
                    self.untilcondition.conditions[
                        i].subpopvartext.setText(filt.get(COLUMN))
                ind = self.untilcondition.conditions[
                    i].subpopop.findText(filt.get(COND))
                self.untilcondition.conditions[i].subpopop.setCurrentIndex(ind)
                if VALUE in tempkey:
                    self.untilcondition.conditions[
                        i].isEnableValue.setChecked(True)
                    self.untilcondition.conditions[
                        i].subpopval.setText(filt.get(VALUE))
                else:
                    self.untilcondition.conditions[
                        i].isEnableValue.setChecked(False)
                    ind = self.untilcondition.conditions[
                        i].subpopvtab.findText(filt.get(VTABLE))
                    self.untilcondition.conditions[
                        i].subpopvtab.setCurrentIndex(ind)
                    if str(filt.get(VTABLE)) != "runtime":
                        self.untilcondition.conditions[
                            i].subpopvalvartext.setDisabled(True)
                        self.untilcondition.conditions[
                            i].subpopvalvartext.setVisible(False)
                        self.untilcondition.conditions[
                            i].subpopvalvar.setDisabled(False)
                        self.untilcondition.conditions[
                            i].subpopvalvar.setVisible(True)
                        ind = self.untilcondition.conditions[
                            i].subpopvalvar.findText(filt.get(VCOLUMN))
                        self.untilcondition.conditions[
                            i].subpopvalvar.setCurrentIndex(ind)
                    else:
                        self.untilcondition.conditions[
                            i].subpopvalvartext.setDisabled(False)
                        self.untilcondition.conditions[
                            i].subpopvalvartext.setVisible(True)
                        self.untilcondition.conditions[
                            i].subpopvalvar.setDisabled(True)
                        self.untilcondition.conditions[
                            i].subpopvalvar.setVisible(False)
                        self.untilcondition.conditions[
                            i].subpopvalvartext.setText(filt.get(VCOLUMN))
                i = i + 1
            self.untilcondition.setChecked(True)
        else:
            self.untilcondition.setChecked(False)

    def populateFilterWidget(self, modelelt):
        set = modelelt.find(FILTERSET)
        if set <> None:
            if set.get(MODELTYPE) == 'and':
                self.filters.logical.setCurrentIndex(0)
            else:
                self.filters.logical.setCurrentIndex(1)

        filters = modelelt.findall(FILTER)
        if len(filters) > 0:
            self.filters.remove()
            for i in range(len(filters)):
                self.filters.addFiter()

            i = 0
            for filt in modelelt.getiterator(FILTER):
                tempkey = filt.keys()
                ind = self.filters.conditions[
                    i].subpoptab.findText(filt.get(TABLE))
                self.filters.conditions[i].subpoptab.setCurrentIndex(ind)
                if str(filt.get(TABLE)) != "runtime":
                    self.filters.conditions[i].subpopvartext.setDisabled(True)
                    self.filters.conditions[i].subpopvartext.setVisible(False)
                    self.filters.conditions[i].subpopvar.setDisabled(False)
                    self.filters.conditions[i].subpopvar.setVisible(True)
                    ind = self.filters.conditions[
                        i].subpopvar.findText(filt.get(COLUMN))
                    self.filters.conditions[i].subpopvar.setCurrentIndex(ind)
                else:
                    self.filters.conditions[i].subpopvartext.setDisabled(False)
                    self.filters.conditions[i].subpopvartext.setVisible(True)
                    self.filters.conditions[i].subpopvar.setDisabled(True)
                    self.filters.conditions[i].subpopvar.setVisible(False)
                    self.filters.conditions[
                        i].subpopvartext.setText(filt.get(COLUMN))
                ind = self.filters.conditions[
                    i].subpopop.findText(filt.get(COND))
                self.filters.conditions[i].subpopop.setCurrentIndex(ind)
                if VALUE in tempkey:
                    self.filters.conditions[i].isEnableValue.setChecked(True)
                    self.filters.conditions[
                        i].subpopval.setText(filt.get(VALUE))
                else:
                    self.filters.conditions[i].isEnableValue.setChecked(False)
                    ind = self.filters.conditions[
                        i].subpopvtab.findText(filt.get(VTABLE))
                    self.filters.conditions[i].subpopvtab.setCurrentIndex(ind)
                    if str(filt.get(VTABLE)) != "runtime":
                        self.filters.conditions[
                            i].subpopvalvartext.setDisabled(True)
                        self.filters.conditions[
                            i].subpopvalvartext.setVisible(False)
                        self.filters.conditions[
                            i].subpopvalvar.setDisabled(False)
                        self.filters.conditions[
                            i].subpopvalvar.setVisible(True)
                        ind = self.filters.conditions[
                            i].subpopvalvar.findText(filt.get(VCOLUMN))
                        self.filters.conditions[
                            i].subpopvalvar.setCurrentIndex(ind)
                    else:
                        self.filters.conditions[
                            i].subpopvalvartext.setDisabled(False)
                        self.filters.conditions[
                            i].subpopvalvartext.setVisible(True)
                        self.filters.conditions[
                            i].subpopvalvar.setDisabled(True)
                        self.filters.conditions[
                            i].subpopvalvar.setVisible(False)
                        self.filters.conditions[
                            i].subpopvalvartext.setText(filt.get(VCOLUMN))
                i = i + 1
            self.filters.setChecked(True)
        else:
            self.filters.setChecked(False)

#    def populateFilterWidget(self,modelelt):
#        temp = modelelt.find(FILTER)
#        if temp <> None:
#            for filt in modelelt.getiterator(FILTER):
#                ind = self.subpoptab.findText(filt.get(TABLE))
#                self.subpoptab.setCurrentIndex(ind)
#                ind = self.subpopvar.findText(filt.get(COLUMN))
#                self.subpopvar.setCurrentIndex(ind)
#                ind = self.subpopop.findText(filt.get(COND))
#                self.subpopop.setCurrentIndex(ind)
#                self.subpopval.setText(filt.get(VALUE))
#        else:
#            self.subpopgb.setChecked(False)

    def populateVarsWidget(self, modelelt):
        for varelt in modelelt.getiterator(VARIABLE):
            varstable = self.modwidget.varstable
            varstable.insertRow(varstable.rowCount())

            tableitem = QTableWidgetItem()
            tableitem.setText(varelt.get(TABLE))
            tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
            varstable.setItem(varstable.rowCount() - 1, 0, tableitem)

            varitem = QTableWidgetItem()
            varitem.setText(varelt.get(COLUMN))
            varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
            varstable.setItem(varstable.rowCount() - 1, 1, varitem)

            coeffitem = QTableWidgetItem()
            coeffitem.setText(varelt.get(COEFF))
            varstable.setItem(varstable.rowCount() - 1, 2, coeffitem)

    def populateAltsWidget(self, modelelt):
        for altelt in modelelt.getiterator(ALTERNATIVE):
            altstable = self.modwidget.choicetable
            altstable.insertRow(altstable.rowCount())

            altitem = QTableWidgetItem()
            altitem.setText(altelt.get(ID))
            altstable.setItem(altstable.rowCount() - 1, 0, altitem)

            altvalue = QTableWidgetItem()
            altvalue.setText(altelt.get(VALUE))
            altstable.setItem(altstable.rowCount() - 1, 1, altvalue)

    def populateOrdAltsWidget(self, modelelt):
        i = 0
        for altelt in modelelt.getiterator(ALTERNATIVE):
            altstable = self.modwidget.choicetable
            altstable.insertRow(altstable.rowCount())

            altitem1 = QTableWidgetItem()
            altitem1.setText(altelt.get(ID))
            altstable.setItem(altstable.rowCount() - 1, 0, altitem1)
            altitem2 = QTableWidgetItem()
            altitem2.setText(altelt.get(VALUE))
            altstable.setItem(altstable.rowCount() - 1, 1, altitem2)
            if i > 0:
                thitem = QTableWidgetItem()
                thitem.setText(altelt.get(THRESHOLD))
                altstable.setItem(altstable.rowCount() - 1, 2, thitem)
            else:
                altstable.setItem(0, 2, QTableWidgetItem())
                disableitem = altstable.item(0, 2)
                disableitem.setFlags(disableitem.flags() & ~Qt.ItemIsEnabled)
                disableitem.setBackgroundColor(Qt.darkGray)
            i = i + 1

    def changeModelWidget(self, idx=0):

        self.modwidget.setParent(None)
        formtext = self.modeltypecb.currentText()
        if formtext == PROB_MODEL:
            self.modwidget = ProbModWidget(self)
        elif formtext == COUNT_MODEL:
            self.modwidget = CountModWidget(self)
        elif formtext == MNL_MODEL:
            self.modwidget = MNLogitModWidget(self)
        elif formtext == GC_MNL_MODEL:
            self.modwidget = GCMNLogitModWidget(self)
        elif formtext == SF_MODEL:
            self.modwidget = SFModWidget(self)
        elif formtext == LOGSF_MODEL:
            self.modwidget = SFModWidget(self)
        elif formtext == LOGREG_MODEL or formtext == LINEAR_MODEL or formtext == IDEN_UNIQUE:
            self.modwidget = LogRegModWidget(self)
        elif formtext == ORD_MODEL:
            self.modwidget = OrderedModWidget(self)
        elif formtext == NL_MODEL:
            self.modwidget = NLogitModWidget(self)
        elif formtext == RECON_SCHEDULE or formtext == FIXEDACT_SCHEDULE or formtext == AGGACT_SCHEDULE or formtext == CHILD_ALLOCAT or \
                formtext == PERS_TRIP_ARRIVAL or formtext == SCH_ADJUST or formtext == IDEN_INDIVIDUAL or formtext == CHILD_ALLOCAT_TERM or formtext == CHILD_DEPEND:
            self.modwidget = SchduleModWidget(self)

#        self.glayout.addWidget(self.modwidget,8,0)
        self.tabwidget.tabRemoved(3)
        self.tabwidget.addTab(self.modwidget, "Model Specification")
        self.tabwidget.setCurrentIndex(3)
        self.update()


#    def populateColumns(self, idx=0):
#        self.subpopvar.clear()
#        seltab = str(self.subpoptab.currentText())
#        self.subpopvar.addItems(self.coldict[seltab])

    def storeSpec(self):
        if self.checkInputs():
            #modelmap = MODELMAP[self.modelkey]
            #modelkey = modelmap[1]
            #modelkey = self.modelkey

            #modelelt = None
            #model = self.configobject.modelSpecInConfig(self.modelkey)

            if self.themodel.tag == COMP:
                model = etree.SubElement(self.themodel, MODEL)
            else:
                model = self.themodel

#            self.setModelAttribute(model)
            self.addDepVarToElt(model)
            self.setFilterToElt(model)
            self.setRununtilToElt(model)
            #tempmodel = deepcopy(model)
            formtext = self.modeltypecb.currentText()

            if formtext == SF_MODEL:
                self.setModeltoElt(model, MODELFORM_REG, SF_MODEL)
                self.setVariance2(model)
                self.saveVariables(model)

            elif formtext == LOGSF_MODEL:
                self.setModeltoElt(model, MODELFORM_REG, LOGSF_MODEL)
                self.setVariance2(model)
                self.saveVariables(model)

            elif formtext == COUNT_MODEL:
                self.setModeltoElt(model, MODELFORM_CNT, COUNT_MODEL)
                if self.modwidget.nbradio.isChecked():
                    model.set(MODELTYPE, NEGBIN_MODEL)
                else:
                    model.set(MODELTYPE, POI_MODEL)

                if type == NEGBIN_MODEL:
                    variance = model.find(VARIANCE)
                    variance.set(VALUE, str(self.modwidget.odline.text()))
                    variance.set(MODELTYPE, 'Overdispersion')
                self.saveVariables(model)

            elif formtext == ORD_MODEL:
                if self.modwidget.probradio.isChecked():
                    self.setModeltoElt(model, MODELFORM_ORD, PROBIT)
                else:
                    self.setModeltoElt(model, MODELFORM_ORD, LOGIT)
                self.saveAlternatives(model)
                self.saveVariables(model)

            elif formtext == GC_MNL_MODEL:
                self.saveVariables(model)

            elif formtext == MNL_MODEL:
                self.modwidget.storeVarsTable(
                    self.modwidget.choicetable.currentRow())

                self.setModeltoElt(model, MODELFORM_MNL, ALTSPEC)
                for alter in model.findall(ALTERNATIVE):
                    model.remove(alter)

                numrows = self.modwidget.choicetable.rowCount()
                specs = self.modwidget.specs
                for i in range(numrows):
                    altname = str(
                        (self.modwidget.choicetable.item(i, 0)).text())
                    altvalue = str(
                        (self.modwidget.choicetable.item(i, 1)).text())
                    altelt = etree.SubElement(model, ALTERNATIVE)
                    altelt.set(ID, altname)
                    altelt.set(VALUE, altvalue)
                    altspecs = specs[altname]
                    numvars = len(altspecs)
                    for j in range(numvars):
                        specrow = altspecs[j]
                        self.addVariabletoElt(
                            altelt, specrow[0], specrow[1], specrow[2])
                    model.append(altelt)

            elif formtext == NL_MODEL:
                self.modwidget.storeVarsTable(
                    self.modwidget.choicetable.currentItem())
                self.setModeltoElt(model, MODELFORM_NL, NL_MODEL)

                for alter in model.findall(ALTERNATIVE):
                    model.remove(alter)

                numrows = self.modwidget.choicetable.rowCount()
                specs = self.modwidget.specs
                for i in range(numrows):
                    altname = str(
                        (self.modwidget.choicetable.item(i, 0)).text())
                    altdet = altname.rsplit('/', 1)
                    l = len(altdet)
                    if l == 1:
                        altid = altdet[0]
                        altbr = 'root'
                    if l > 1:
                        altid = altdet[1]
                        altbr = 'root/' + altdet[0]
                    altelt = etree.SubElement(model, ALTERNATIVE)
                    altelt.set(ID, altid)
                    altelt.set(BRANCH, altbr)
                    altspecs = specs[altname]
                    numvars = len(altspecs)
                    for i in range(numvars):
                        specrow = altspecs[i]
                        self.addVariabletoElt(
                            altelt, specrow[0], specrow[1], specrow[2])
                    model.append(altelt)

                for branch in model.findall(BRANCH):
                    model.remove(branch)

                numnests = self.modwidget.nesttable.rowCount()
                for i in range(numnests):
                    nestname = str(
                        (self.modwidget.nesttable.item(i, 0)).text())
                    nestiv = str((self.modwidget.nesttable.item(i, 1)).text())
                    neselt = etree.SubElement(model, BRANCH)
                    neselt.set(NAME, nestname)
                    neselt.set(COEFF, nestiv)
                    model.append(neselt)

            elif formtext == LOGREG_MODEL:
                self.setModeltoElt(model, MODELFORM_REG, LOGREG_MODEL)
                self.setVariance(model)
                self.saveVariables(model)

            elif formtext == LINEAR_MODEL:
                self.setModeltoElt(model, MODELFORM_REG, LINEAR_MODEL)
                self.setVariance(model)
                self.saveVariables(model)

            elif formtext == IDEN_UNIQUE:
                self.setModeltoElt(model, IDEN_UNIQUE)
                self.setVariance(model)
                self.saveVariables(model)

            elif formtext == PROB_MODEL:
                self.setModeltoElt(model, PROB_MODEL)
                for alter in model.findall(ALTERNATIVE):
                    model.remove(alter)

                numrows = self.modwidget.choicetable.rowCount()
                for i in range(numrows):
                    altname = str(
                        (self.modwidget.choicetable.item(i, 0)).text())
                    altvalue = str(
                        (self.modwidget.choicetable.item(i, 1)).text())
                    altelt = etree.SubElement(model, ALTERNATIVE)
                    altelt.set(ID, altname)
                    altelt.set(VALUE, altvalue)

                    valtable = str(
                        (self.modwidget.varstable.item(i, 0)).text())
                    valname = str((self.modwidget.varstable.item(i, 1)).text())
                    valcoff = str((self.modwidget.varstable.item(i, 2)).text())
                    self.addVariabletoElt(altelt, valtable, valname, valcoff)
                    model.append(altelt)

            elif formtext == RECON_SCHEDULE or formtext == FIXEDACT_SCHEDULE or formtext == AGGACT_SCHEDULE or formtext == CHILD_ALLOCAT \
                    or formtext == PERS_TRIP_ARRIVAL or formtext == SCH_ADJUST or formtext == IDEN_INDIVIDUAL or formtext == CHILD_ALLOCAT_TERM or formtext == CHILD_DEPEND:
                if formtext == RECON_SCHEDULE:
                    self.setModeltoElt(model, RECON_SCHEDULE)
                elif formtext == FIXEDACT_SCHEDULE:
                    self.setModeltoElt(model, FIXEDACT_SCHEDULE)
                elif formtext == AGGACT_SCHEDULE:
                    self.setModeltoElt(model, AGGACT_SCHEDULE)
                elif formtext == CHILD_ALLOCAT:
                    self.setModeltoElt(model, CHILD_ALLOCAT)
                elif formtext == PERS_TRIP_ARRIVAL:
                    self.setModeltoElt(model, PERS_TRIP_ARRIVAL)
                elif formtext == SCH_ADJUST:
                    self.setModeltoElt(model, SCH_ADJUST)

                for elt in model.getchildren():
                    if elt.tag == "ActivityAttributes" or elt.tag == "DailyStatus" or elt.tag == "Dependency" or \
                            elt.tag == "OccupancyInvalid" or elt.tag == "ArrivalTime" or elt.tag == "PersonsArrivedAttributes" or elt.tag == "Id":
                        model.remove(elt)

                self.modwidget.storeVarsTable(
                    self.modwidget.choicelist.currentItem())
                numrows = self.modwidget.choicelist.count()
                specs = self.modwidget.specs
                print specs
                keys = ["Activity Attributes", "Daily Status", "Dependency",
                        "OccupancyInvalid", "ArrivalTime", "PersonsArrivedAttributes", "Id"]
                for key in keys:
                    alter = str(key)
                    if key == "Activity Attributes":
                        alter = "ActivityAttributes"
                    elif key == "Daily Status":
                        alter = "DailyStatus"

                    isPut = False
                    altelt = etree.Element(alter)
                    catagories = specs[key]
                    for item in catagories:
                        title = str(item[0])
                        table = str(item[1])
                        column = str(item[2])
                        subelt = etree.SubElement(altelt, title)
                        subelt.set(TABLE, table)
                        subelt.set(COLUMN, column)
                        if table != "" and column != "":
                            isPut = True

                    if isPut:
                        model.append(altelt)

            if self.themodel.tag == COMP:
                father = self.parent()
                item = father.currentItem()
                element_term = QTreeWidgetItem(item)
                element_term.setText(0, MODEL)

#            if not self.configobject.comparemodels(self.modelkey):
#                print 'Successful to change'
#                model.set(DMODEL,'True')

            QDialog.accept(self)


# def setModelAttribute(self,model): #(self,name,formulation,type,otherattr=None):
#        keys = model.keys()
#        numrows = self.attritable.rowCount()
#        for i in range(numrows):
#            key = str((self.attritable.item(i,0)).text())
#            value = str((self.attritable.item(i,1)).text())
#            model.set(key,value)
#            if key in keys:
#                keys.remove(key)
#
#        for i in keys:
#            del model.attrib[i]

#        elt = etree.Element(MODEL)
#        elt.set(NAME,name)
#        elt.set(FORMULATION,formulation)
#        if type != '':
#            elt.set(MODELTYPE,type)
#        if otherattr != None:
#            elt.set(otherattr[0],otherattr[1])
#        elt.set(SEED,'1')
#        return elt

    def setModeltoElt(self, elt, formular, type='', thresh=''):
        keys = elt.keys()
        elt.set(NAME, str(self.nametxt.text()))
        elt.set(FORMULATION, str(formular))
        if type != '':
            elt.set(MODELTYPE, str(type))
        else:
            if elt.get(MODELTYPE) != None:
                elt.set(MODELTYPE, '')

        value = str(self.vertexcb.currentText())
        if value == "":
            if VERTEX in keys:
                del elt.attrib[VERTEX]
        else:
            elt.set(VERTEX, value)

        value = str(self.lowertxt.text())
        if value == "":
            if "lower_threshold" in keys:
                del elt.attrib["lower_threshold"]
        else:
            elt.set("lower_threshold", value)

        value = str(self.uppertxt.text())
        if value == "":
            if "upper_threshold" in keys:
                del elt.attrib["upper_threshold"]
        else:
            elt.set("upper_threshold", value)

        value = str(self.modwidget.seedline.value())
        elt.set(SEED, value)

#        seed = str(elt.get(SEED))
#        user = str(elt.get(DMODEL))
#        del elt.attrib[SEED]
#        del elt.attrib[DMODEL]
#
#        elt.set(SEED,seed)
#        elt.set(DMODEL,user)

    def addDepVarToElt(self, model):
        value = str(self.dependentcb.currentText())
        depend = model.find(DEPVARIABLE)
        if depend <> None:
            depend.set(COLUMN, value)
        else:
            elt = etree.SubElement(model, DEPVARIABLE)
            elt.set(COLUMN, value)
#        depvarelt = etree.SubElement(elt,DEPVARIABLE)
# if col in PERSON_TABLE_MODELS:
##            tab = TABLE_PER
# elif col in HH_TABLE_MODELS:
##            tab = TABLE_HH
# depvarelt.set(TABLE,tab)
#        depvarelt.set(COLUMN,col.lower())

    def setFilterToElt(self, model):
        for elt in model.getchildren():
            if elt.tag == FILTER or elt.tag == FILTERSET:
                model.remove(elt)

        if self.filters.isChecked():
            if len(self.filters.conditions) > 1:
                self.subFilterset(model)
                self.subFilter(model)
            else:
                self.subFilter(model)

    def subFilterset(self, model):
        runelt = etree.SubElement(model, FILTERSET)
        runelt.set(MODELTYPE, str(self.filters.logical.currentText()).lower())

    def subFilter(self, model):
        for i in range(len(self.filters.conditions)):
            runelt = etree.SubElement(model, FILTER)
            table = str(self.filters.conditions[i].subpoptab.currentText())
            runelt.set(TABLE, table)
            if table != "runtime":
                runelt.set(
                    COLUMN, str(self.filters.conditions[i].subpopvar.currentText()))
            else:
                runelt.set(
                    COLUMN, str(self.filters.conditions[i].subpopvartext.text()))
            runelt.set(
                COND, str(self.filters.conditions[i].subpopop.currentText()))

            if self.filters.conditions[i].isEnableValue.isChecked():
                value = str(self.filters.conditions[i].subpopval.text())
                runelt.set(VALUE, value)
            else:
                vtable = str(
                    self.filters.conditions[i].subpopvtab.currentText())
                runelt.set(VTABLE, vtable)
                if vtable != "runtime":
                    vcolumn = str(
                        self.filters.conditions[i].subpopvalvar.currentText())
                    runelt.set(VCOLUMN, vcolumn)
                else:
                    vcolumn = str(
                        self.filters.conditions[i].subpopvalvartext.text())
                    runelt.set(VCOLUMN, vcolumn)

    def setRununtilToElt(self, model):
        for elt in model.getchildren():
            if elt.tag == RUNUNTIL or elt.tag == RUNUNTILSET:
                model.remove(elt)

        if self.untilcondition.isChecked():
            if len(self.untilcondition.conditions) > 1:
                self.subRununtilset(model)
                self.subRununtil(model)
            else:
                self.subRununtil(model)

    def subRununtilset(self, model):
        runelt = etree.SubElement(model, RUNUNTILSET)
        runelt.set(
            MODELTYPE, str(self.untilcondition.logical.currentText()).lower())

    def subRununtil(self, model):
        for i in range(len(self.untilcondition.conditions)):
            runelt = etree.SubElement(model, RUNUNTIL)
            table = str(
                self.untilcondition.conditions[i].subpoptab.currentText())
            runelt.set(TABLE, table)
            if table != "runtime":
                runelt.set(
                    COLUMN, str(self.untilcondition.conditions[i].subpopvar.currentText()))
            else:
                runelt.set(
                    COLUMN, str(self.untilcondition.conditions[i].subpopvartext.text()))
            runelt.set(
                COND, str(self.untilcondition.conditions[i].subpopop.currentText()))

            if self.untilcondition.conditions[i].isEnableValue.isChecked():
                value = str(self.untilcondition.conditions[i].subpopval.text())
                runelt.set(VALUE, value)
            else:
                vtable = str(
                    self.untilcondition.conditions[i].subpopvtab.currentText())
                runelt.set(VTABLE, vtable)
                if vtable != "runtime":
                    vcolumn = str(
                        self.untilcondition.conditions[i].subpopvalvar.currentText())
                    runelt.set(VCOLUMN, vcolumn)
                else:
                    vcolumn = str(
                        self.untilcondition.conditions[i].subpopvalvartext.text())
                    runelt.set(VCOLUMN, vcolumn)

    def setVariance(self, model):
        for elt in model.getchildren():
            if elt.tag == VARIANCE:
                model.remove(elt)

        elt = etree.SubElement(model, VARIANCE)
        value = str(self.modwidget.variancevline.text())
        elt.set(VALUE, value)

    def setVariance2(self, model):
        for elt in model.getchildren():
            if elt.tag == VARIANCE:
                model.remove(elt)

        elt = etree.SubElement(model, VARIANCE)
        value = str(self.modwidget.variancevline.text())
        elt.set(VALUE, value)

        elt = etree.SubElement(model, VARIANCE)
        value = str(self.modwidget.varianceuline.text())
        elt.set(VALUE, value)
        elt.set(MODELTYPE, "Half Normal")
#    def addFiltToElt(self,elt):
#        for set in elt.findall(FILTERSET):
#            elt.remove(set)
#        for filter in elt.findall(FILTER):
#            elt.remove(filter)
#
#        if self.subpopgb.isChecked():
#            if len(self.filter1) > 1:
#                fset = etree.SubElement(elt,FILTERSET)
#                if self.logical.currentIndex() == 0:
#                    fset.set(MODELTYPE,'and')
#                else:
#                    fset.set(MODELTYPE,'or')
#
#            i = 0
#            while i < len(self.filter1):
#                if (str(self.filter4[i].text()) != ''):
#                    filter = etree.SubElement(elt,FILTER)
#                    filter.set(TABLE,str(self.filter1[i].currentText()))
#                    filter.set(COLUMN,str(self.filter2[i].currentText()))
#                    filter.set(COND,str(self.filter3[i].currentText()))
#                    filter.set(VALUE,str(self.filter4[i].text()))
#                i = i + 1

    def saveAlternatives(self, elt):
        for alter in elt.findall(ALTERNATIVE):
            elt.remove(alter)
        self.addAlternatives(elt)

    def addAlternatives(self, elt):
        numrows = self.modwidget.choicetable.rowCount()
        for i in range(numrows):
            altname = (self.modwidget.choicetable.item(i, 0)).text()
            altvalue = (self.modwidget.choicetable.item(i, 1)).text()
            altelt = etree.SubElement(elt, ALTERNATIVE)
            altelt.set(ID, str(altname))
            altelt.set(VALUE, str(altvalue))
            if self.modeltypecb.currentText() == ORD_MODEL:
                if i > 0:
                    threshold = (self.modwidget.choicetable.item(i, 2)).text()
                    altelt.set(THRESHOLD, str(threshold))

    def saveVariables(self, elt):
        for vari in elt.findall(VARIABLE):
            elt.remove(vari)
        self.addVariables(elt)

    def addVariables(self, elt):
        numrows = self.modwidget.varstable.rowCount()
        for i in range(numrows):
            tablename = (self.modwidget.varstable.item(i, 0)).text()
            colname = (self.modwidget.varstable.item(i, 1)).text()
            coeff = (self.modwidget.varstable.item(i, 2)).text()
            self.addVariabletoElt(elt, tablename, colname, coeff)

    def addVariabletoElt(self, elt, tablename, colname, coeff):
        variableelt = etree.SubElement(elt, VARIABLE)
        variableelt.set(TABLE, str(tablename))
        variableelt.set(COLUMN, str(colname))
        variableelt.set(COEFF, str(coeff))

    def populateFromDatabase(self):
        self.protocol = self.configobject.getConfigElement(
            DB_CONFIG, DB_PROTOCOL)
        self.user_name = self.configobject.getConfigElement(DB_CONFIG, DB_USER)
        self.password = self.configobject.getConfigElement(DB_CONFIG, DB_PASS)
        self.host_name = self.configobject.getConfigElement(DB_CONFIG, DB_HOST)
        self.database_name = self.configobject.getConfigElement(
            DB_CONFIG, DB_NAME)
        self.database_config_object = DataBaseConfiguration(
            self.protocol, self.user_name, self.password, self.host_name, self.database_name)

        new_obj = DataBaseConnection(self.database_config_object)
        new_obj.new_connection()
        tables = new_obj.get_table_list()

        self.tablelist = []
        self.coldict = {}
        for table in tables:
            self.tablelist.append(QString(table))
            cols = new_obj.get_column_list(table)
            varlist = []
            if cols is not None:
                for col in cols:
                    varlist.append(QString(col))
                self.coldict[table] = varlist
        self.tablelist.append("runtime")

    def defaultModel(self):
        print "Model Key - %s" % (self.modelkey)
        if self.modelkey != '':
            modelspecified = self.configobject.modelSpecInDefault(
                self.modelkey)
            self.loadFromConfigObject2(modelspecified)
        if self.modelindex != None:
            modelspecified = self.configobject.getDElement(self.modelindex)
            self.loadFromConfigObject2(modelspecified)

    def checkFloat(self, num):
        res = False
        try:
            temp = float(num)
            res = True
        except:
            res = False

        return res

    def checkInput_table1(self):
        numrows = self.modwidget.choicetable.rowCount()
        for i in range(numrows):

            if self.modwidget.choicetable.item(i, 1) == None:
                QMessageBox.warning(
                    self, "Warning", "The value of an alternative must be numeric.")
                return False

            coeff = unicode((self.modwidget.choicetable.item(i, 1)).text())
            if not self.checkFloat(coeff):
                QMessageBox.warning(
                    self, "Warning", "The value of an alternative must be numeric.")
                return False
#            else:
#                if float(coeff) < 0.0:
#                    QMessageBox.warning(self, "Warning", "The value of an alternative must be greater than or equal to zero.")
#                    return False

        return True

    def checkInput_table2(self):
        numrows = self.modwidget.varstable.rowCount()
        for i in range(numrows):

            if self.modwidget.varstable.item(i, 2) == None:
                QMessageBox.warning(
                    self, "Warning", "Coefficient must be numeric.")
                return False

            coeff = unicode((self.modwidget.varstable.item(i, 2)).text())
            if not self.checkFloat(coeff):
                QMessageBox.warning(
                    self, "Warning", "Coefficient must be numeric.")
                return False
#            else:
#                if float(coeff) < 0.0:
#                    QMessageBox.warning(self, "Warning", "Coefficient must be greater than or equal to zero.")
#                    return False

        return True

    def checkInputs(self):
        res = True

        if self.filters.isChecked():
            for i in range(len(self.filters.conditions)):
                value = str(self.filters.conditions[i].subpopval.text())
                if value != "":
                    if not self.checkFloat(value):
                        QMessageBox.warning(
                            self, "Warning", "The value of an alternative must be numeric.")
                        return False
                else:
                    vtable = str(
                        self.filters.conditions[i].subpopvtab.currentText())
                    vcolumn1 = str(
                        self.filters.conditions[i].subpopvalvar.currentText())
                    vcolumn2 = str(
                        self.filters.conditions[i].subpopvalvartext.text())
                    if vtable == "" or (vcolumn1 == "" and vcolumn2 == ""):
                        QMessageBox.warning(
                            self, "Warning", "Value Table and Value Variable should be filled in Sub-Population.")
                        return False

        if self.untilcondition.isChecked():
            for i in range(len(self.untilcondition.conditions)):
                value = str(self.untilcondition.conditions[i].subpopval.text())
                if value != "":
                    if not self.checkFloat(value):
                        QMessageBox.warning(
                            self, "Warning", "The value of an alternative must be numeric.")
                        return False
                else:
                    vtable = str(
                        self.untilcondition.conditions[i].subpopvtab.currentText())
                    vcolumn1 = str(
                        self.untilcondition.conditions[i].subpopvalvar.currentText())
                    vcolumn2 = str(
                        self.untilcondition.conditions[i].subpopvalvartext.text())
                    if vtable == "" or (vcolumn1 == "" and vcolumn2 == ""):
                        QMessageBox.warning(
                            self, "Warning", "Value Table and Value Variable should be filled in Run Condition.")
                        return False

        if self.modeltypecb.currentText() == PROB_MODEL:
            numrows = self.modwidget.choicetable.rowCount()
            for i in range(numrows):

                if self.modwidget.choicetable.item(i, 1) == None:
                    QMessageBox.warning(
                        self, "Warning", "The value of an alternative must be entered as a number.")
                    return False

                colname = unicode(
                    (self.modwidget.choicetable.item(i, 1)).text())
                if not self.checkFloat(colname):
                    QMessageBox.warning(
                        self, "Warning", "The value of an alternative must be numeric.")
                    return False
                else:
                    if float(colname) < 0.0:
                        QMessageBox.warning(
                            self, "Warning", "The value of an alternative must be greater than or equal to zero.")
                        return False

#                if self.modwidget.choicetable.item(i,2) == None:
#                    QMessageBox.warning(self, "Warning", "Probability must be entered between 0.0 and 1.0.")
#                    return False

                coeff = unicode((self.modwidget.varstable.item(i, 2)).text())
                if self.checkFloat(coeff):
                    coeff1 = float(coeff)
                    if coeff1 < 0.0 or coeff1 > 1.0:
                        QMessageBox.warning(
                            self, "Warning", "Probability must be between 0.0 and 1.0.")
                        return False
                else:
                    QMessageBox.warning(
                        self, "Warning", "Probability must be numeric.")
                    return False

        elif self.modeltypecb.currentText() == COUNT_MODEL:

            dispersion = unicode(self.modwidget.odline.text())
            if self.modwidget.odline.isEnabled():
                if not self.checkFloat(dispersion):
                    QMessageBox.warning(
                        self, "Warning", "Overdispersion must be numeric.")
                    return False
                else:
                    if float(dispersion) < 0.0:
                        QMessageBox.warning(
                            self, "Warning", "Overdispersion must be greater than or equal to zero.")
                        return False

            if not self.checkInput_table1():
                return False

            if not self.checkInput_table2():
                return False

        elif self.modeltypecb.currentText() == SF_MODEL:

            variancev = unicode(self.modwidget.variancevline.text())
            if not self.checkFloat(variancev):
                QMessageBox.warning(
                    self, "Warning", "Variance (v) - Normal must be numeric.")
                return False
            else:
                if float(variancev) < 0.0:
                    QMessageBox.warning(
                        self, "Warning", "Variance (v) - Normal must be greater than or equal to zero.")
                    return False

            varianceu = unicode(self.modwidget.varianceuline.text())
            if not self.checkFloat(varianceu):
                QMessageBox.warning(
                    self, "Warning", "Variance (u) - Half Normal must be numeric.")
                return False
            else:
                if float(varianceu) < 0.0:
                    QMessageBox.warning(
                        self, "Warning", "Variance (u) - Half Normal must be greater than or equal to zero.")
                    return False

            if not self.checkInput_table2():
                return False

        elif self.modeltypecb.currentText() == GC_MNL_MODEL:

            if not self.checkInput_table2():
                return False

        elif self.modeltypecb.currentText() == MNL_MODEL:

            if not self.checkInput_table1():
                return False

#            if not self.checkInput_table2():
#                return False

            numrows = self.modwidget.choicetable.rowCount()
            specs = self.modwidget.specs
            for i in range(numrows):
                altname = str((self.modwidget.choicetable.item(i, 0)).text())
                altspecs = specs[altname]
                numvars = len(altspecs)
                for i in range(numvars):
                    specrow = altspecs[i]
                    # print specrow[2]
                    if not self.checkFloat(specrow[2]):
                        QMessageBox.warning(
                            self, "Warning", "The value of a coefficient must be numeric.")
                        return False

        elif self.modeltypecb.currentText() == ORD_MODEL:

            numrows = self.modwidget.choicetable.rowCount()
            for i in range(numrows):

                if self.modwidget.choicetable.item(i, 1) == None:
                    QMessageBox.warning(
                        self, "Warning", "The value of an alternative must be entered as a number.")
                    return False

                value = unicode((self.modwidget.choicetable.item(i, 1)).text())
                if not self.checkFloat(value):
                    QMessageBox.warning(
                        self, "Warning", "The value of an alternative must be numeric.")
                    return False
                else:
                    if float(value) < 0.0:
                        QMessageBox.warning(
                            self, "Warning", "The value of an alternative must be greater than or equal to zero.")
                        return False

#                if self.modwidget.choicetable.item(i,2) == None:
#                    QMessageBox.warning(self, "Warning", "Threshold must be entered as a number greater than 0.0.")
#                    return False

                if i > 0:
                    thresh = unicode(
                        (self.modwidget.choicetable.item(i, 2)).text())
                    if self.checkFloat(thresh):
                        if float(thresh) < 0.0:
                            QMessageBox.warning(
                                self, "Warning", "Threshold must be greater than or equal to 0.0.")
                            return False
#                        else:
#                            QMessageBox.warning(self, "Warning", "Threshold must be numeric.")
#                            return False
                    else:
                        QMessageBox.warning(
                            self, "Warning", "Threshold must be numeric.")
                        return False

            if not self.checkInput_table2():
                return False

        elif self.modeltypecb.currentText() == NL_MODEL:

            if not self.checkInput_table1():
                return False

            if not self.checkInput_table2():
                return False

        elif self.modeltypecb.currentText() == LOGREG_MODEL:

            if not self.checkInput_table2():
                return False

        return res
#        res = False
#        if self.modwidget.checkInputs():
#            res = True
#        return res


class FilterWidget(QGroupBox):

    '''
    classdocs
    '''

    def __init__(self, title, parent=None):
        super(FilterWidget, self).__init__(parent)
        father = self.parent()
        self.tablelist = father.tablelist
        self.coldict = father.coldict

        self.setTitle(title)
        self.setCheckable(True)
        self.setChecked(False)
        self.setVisible(True)
        subpoplayout = QVBoxLayout()
        self.setLayout(subpoplayout)

        upwidget = QWidget(self)
        upwidgetlayout = QHBoxLayout()
        upwidget.setLayout(upwidgetlayout)
        self.logical = QComboBox()
        self.logical.addItems([QString(OP_AND), QString(OP_OR)])
        upwidgetlayout.addWidget(self.logical)

        btnwidget = QWidget(self)
        btnwidgetlayout = QHBoxLayout()
        btnwidget.setLayout(btnwidgetlayout)
        self.addbutton = QPushButton('Add')
        btnwidgetlayout.addWidget(self.addbutton)
        self.delbutton = QPushButton('Delete')
        btnwidgetlayout.addWidget(self.delbutton)
        upwidgetlayout.addWidget(btnwidget)

        dummylabel1 = QLabel("")
        upwidgetlayout.addWidget(dummylabel1)
        dummylabel2 = QLabel("")
        upwidgetlayout.addWidget(dummylabel2)
        subpoplayout.addWidget(upwidget)

        conditionwidget = QWidget()
        self.conditionlayout = QVBoxLayout()
        conditionwidget.setLayout(self.conditionlayout)
        self.conditionlayout.setContentsMargins(0, 0, 0, 0)

        self.conditions = []
#         condition = ConditionWidget(self)
#         self.conditions.append(condition)
#         self.conditionlayout.addWidget(condition)
        subpoplayout.addWidget(conditionwidget)

        dummylabel3 = QLabel("")
        subpoplayout.addWidget(dummylabel3)

        self.connect(self.addbutton, SIGNAL("clicked(bool)"), self.addFiter)
        self.connect(self.delbutton, SIGNAL("clicked(bool)"), self.deleteFiter)

    def addFiter(self):
        #        temp = QVBoxLayout()
        #        temp = self.layout()
        #
        #        numrow = temp.count()
        condition = ConditionWidget(self)
        self.conditions.append(condition)
#        temp.addWidget(condition)
        self.conditionlayout.addWidget(condition)

    def deleteFiter(self):
        #        temp = QVBoxLayout()
        #        temp = self.layout()
        numrow = len(self.conditions)

        if numrow > 1:
            self.conditionlayout.removeWidget(self.conditions[numrow - 1])
#            temp.removeWidget(self.conditions[numrow - 1])
            f1 = self.conditions.pop(numrow - 1)
            f1.hide()
            f1.destroy()

        self.conditionlayout.update()
#        temp.update()

    def remove(self):

        numrow = len(self.conditions)
        i = numrow
        while i > 0:
            print "i: %s" % (i)
            self.conditionlayout.removeWidget(self.conditions[i - 1])

            f1 = self.conditions.pop(i - 1)
            f1.hide()
            f1.destroy()

            i -= 1

        self.conditionlayout.update()

    def reset(self):
        self.logical.setCurrentIndex(0)
        for i in range(len(self.conditions)):
            self.conditions[i].reset()


class ConditionWidget(QWidget):

    '''
    classdocs
    '''

    def __init__(self, parent=None):
        super(ConditionWidget, self).__init__(parent)
        father = self.parent()
        self.tablelist = father.tablelist
        self.coldict = father.coldict

        conditionlayout = QGridLayout()
        self.setLayout(conditionlayout)

        tablelabel = QLabel("Table")
        conditionlayout.addWidget(tablelabel, 1, 0)
        self.subpoptab = QComboBox()
        self.subpoptab.addItems(self.tablelist)
        conditionlayout.addWidget(self.subpoptab, 2, 0)

        varlabel = QLabel("Column")
        conditionlayout.addWidget(varlabel, 1, 1)
        self.subpopvar = QComboBox()
        conditionlayout.addWidget(self.subpopvar, 2, 1)
        self.subpopvartext = LineEdit()
        self.subpopvartext.setDisabled(True)
        self.subpopvartext.setVisible(False)
        conditionlayout.addWidget(self.subpopvartext, 2, 1)

        oplabel = QLabel("Operator")
        conditionlayout.addWidget(oplabel, 1, 2)
        self.subpopop = QComboBox()
        self.subpopop.addItems([QString(OP_EQUAL), QString(OP_NOTEQUAL),
                                QString(OP_GT), QString(OP_LT),
                                QString(OP_GTE), QString(OP_LTE)])
        conditionlayout.addWidget(self.subpopop, 2, 2)

        #vallabel = QLabel("Value")
        self.isEnableValue = QCheckBox("Value")
        self.isEnableValue.setChecked(True)
        conditionlayout.addWidget(self.isEnableValue, 1, 3)
        self.subpopval = LineEdit()
        conditionlayout.addWidget(self.subpopval, 2, 3)

        vtablelabel = QLabel("Value Table")
        conditionlayout.addWidget(vtablelabel, 1, 4)
        self.subpopvtab = QComboBox()
        self.subpopvtab.addItem("")
        self.subpopvtab.addItems(father.tablelist)
        self.subpopvtab.setDisabled(True)
        conditionlayout.addWidget(self.subpopvtab, 2, 4)

        valvarlabel = QLabel("Value Variable")
        conditionlayout.addWidget(valvarlabel, 1, 5)
        self.subpopvalvar = QComboBox()
        self.subpopvalvar.setDisabled(True)
        conditionlayout.addWidget(self.subpopvalvar, 2, 5)
        self.subpopvalvartext = LineEdit()
        self.subpopvalvartext.setDisabled(True)
        self.subpopvalvartext.setVisible(False)
        conditionlayout.addWidget(self.subpopvalvartext, 2, 5)

        conditionlayout.setColumnStretch(0, 1)
        conditionlayout.setColumnStretch(1, 1)
        conditionlayout.setColumnStretch(2, 1)
        conditionlayout.setColumnStretch(3, 1)
        conditionlayout.setColumnStretch(4, 1)
        conditionlayout.setColumnStretch(5, 1)

        self.connect(self.subpoptab, SIGNAL(
            "currentIndexChanged(int)"), self.populateColumns1)
        self.connect(self.subpopvtab, SIGNAL(
            "currentIndexChanged(int)"), self.populateColumns2)
        self.connect(
            self.isEnableValue, SIGNAL("stateChanged(int)"), self.enableValue)

    def populateColumns1(self, idx=0):
        self.subpopvar.clear()
        seltab = str(self.subpoptab.currentText())
        if seltab != "" and seltab != "runtime":
            self.subpopvartext.setDisabled(True)
            self.subpopvartext.setVisible(False)
            self.subpopvar.setDisabled(False)
            self.subpopvar.setVisible(True)
            self.subpopvar.addItems(self.coldict[seltab])
        else:
            self.subpopvartext.setDisabled(False)
            self.subpopvartext.setVisible(True)
            self.subpopvar.setDisabled(True)
            self.subpopvar.setVisible(False)

    def populateColumns2(self, idx=0):
        self.subpopvalvar.clear()
        seltab = str(self.subpopvtab.currentText())
        if seltab != "" and seltab != "runtime":
            self.subpopvalvartext.setDisabled(True)
            self.subpopvalvartext.setVisible(False)
            self.subpopvalvar.setDisabled(False)
            self.subpopvalvar.setVisible(True)
            self.subpopvalvar.addItems(self.coldict[seltab])
        else:
            self.subpopvalvartext.setDisabled(False)
            self.subpopvalvartext.setVisible(True)
            self.subpopvalvar.setDisabled(True)
            self.subpopvalvar.setVisible(False)

    def enableValue(self):
        if self.isEnableValue.isChecked() == True:
            self.subpopval.setDisabled(False)
            self.subpopvtab.setDisabled(True)
            self.subpopvalvar.setDisabled(True)
            self.subpopvalvartext.setDisabled(True)
        else:
            self.subpopval.setDisabled(True)
            self.subpopvtab.setDisabled(False)
            self.subpopvalvar.setDisabled(False)
            self.subpopvalvartext.setDisabled(False)

    def reset(self):
        self.subpoptab.setCurrentIndex(0)
        self.subpopvar.clear()
        self.subpopop.setCurrentIndex(0)
        self.subpopval.clear()
        self.subpopvtab.setCurrentIndex(0)
        self.subpopvalvar.clear()


class buttonColor:

    def __init__(self, configobject, parent=None):
        self.configob = configobject

    def isUserModel(self, modelkey):
        if self.configob <> None:
            if not self.configob.comparemodels(modelkey):
                return "background-color: #cd853f"  # 8FBC8F"

        return "background-color: #00C5CD"  # FFFDD0"


def main():
    app = QApplication(sys.argv)
    config = None
    diag = AbtractSpecDialog(config)
    diag.show()
    app.exec_()

if __name__ == "__main__":
    main()
