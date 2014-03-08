'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from openamos.core.run.simulation_manager_cursor import SimulationManager
from openamos.gui.env import *

import subprocess
import sys, time, threading


class SimDialog(QDialog):

    def __init__(self, proconfig, parent=None):
        super(SimDialog, self).__init__(parent)

        self.setWindowTitle("Run Simulation")
        self.setWindowIcon(QIcon("./images/run.png"))
        self.setMinimumSize(800,600)

        self.proconfig = proconfig

        alllayout = QHBoxLayout()
        self.setLayout(alllayout)
        
        self.splitter = QSplitter(Qt.Horizontal)

        self.treewidget = QTreeWidget()
        self.treewidget.setColumnCount(3)
        self.treewidget.setHeaderLabels(["Component", "Completed", "Skip"])
        self.treewidget.setColumnWidth(0, 230)
        self.treewidget.setColumnWidth(1, 60)
        self.treewidget.setColumnWidth(2, 25)
        self.treewidget.setMinimumSize(330,50)
        self.setTreeWidget()
        
        self.splitter.addWidget(self.treewidget)
        alllayout.addWidget(self.splitter)
        
        leftwidget = QGroupBox("")
        leftlayout = QVBoxLayout()
        leftwidget.setLayout(leftlayout)
        
        

#        self.gLayout = QGridLayout()
#        self.complist = ['VehicleOwnershipModel','VehicleAttributeModels','WorkEpisodes']
#        
#        for comp in self.complist:
#            compwidget = CompStatWidget(comp,self.proconfig)
#            vLayout.addWidget(compwidget)
            
        outputLabel = QLabel("Simulation Outputs")
        leftlayout.addWidget(outputLabel)
        self.outputWindow = QTextEdit()
        leftlayout.addWidget(self.outputWindow)
        
        
        self.runbutton = QPushButton("Run")
        self.runbutton.setDefault(True)
        
        self.cancelbutton = QPushButton("Cancel")
        self.cancelbutton.setDefault(True)
        
        dialogButtonBox = QDialogButtonBox(Qt.Horizontal)
        dialogButtonBox.addButton(self.runbutton, QDialogButtonBox.ActionRole)
        dialogButtonBox.addButton(self.cancelbutton, QDialogButtonBox.ActionRole)
        
#        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)
        leftlayout.addWidget(dialogButtonBox)
        
        self.splitter.addWidget(leftwidget)
        self.splitter.setStretchFactor(0,0)
        self.splitter.setStretchFactor(1,1)
        alllayout.addWidget(self.splitter)

        self.mythread = None
        self.connect(self.runbutton, SIGNAL("clicked(bool)"), self, SLOT("accept()"))
        self.connect(self.cancelbutton, SIGNAL("clicked(bool)"), self, SLOT("reject()"))

#        self.index = 0
#        
        #runWarning = QLabel("""<font color = blue>Note: Select geographies by clicking on the <b>Select Geographies</b> button """
        #                    """and then click on <b>Run Synthesizer</b> to start synthesizing population.</font>""")
        #runWarning.setWordWrap(True)

#        self.thread = Worker()
#        self.connect(self.thread, SIGNAL("output(QString)"), self.update)
#        self.connect(self.thread, SIGNAL("finished()"), self.updateUi)
        
#        self.proc = QProcess()
#        self.connect(self.proc, SIGNAL("readyReadStandardOutput()"), self.sendOutput)
#        self.connect(self.proc, SIGNAL("readyReadStandardError()"), self.sendError)
#        self.connect(self.proc, SIGNAL("finished(int)"), self.updateUi)


    def setTreeWidget(self):
        if self.proconfig != None:
            #compelts = self.proconfig.getComponents()
            compelts = self.proconfig.getModelConfigChildren()
            for comp in compelts:
                
                if comp.tag == COMP:

                    comtitle = str(comp.get(NAME))
                    component_term = QTreeWidgetItem(self.treewidget)
                    component_term.setText(0, comtitle) 
                    component_term.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
                    
                    for key in comp.keys():
                        self.sub_setTreeWidget(comp, key, component_term)
#                         if key == "skip" or key == "completed":
#                             attr = "%s"%(comp.get(key))
#                             if key == "skip":
#                                 if attr == "True":
#                                     component_term.setText(2, "Yes")
#                                     component_term.setTextColor(2,QColor("green"))
#                                     component_term.setTextAlignment(2,Qt.AlignHCenter)
#                                 else:
#                                     component_term.setText(2, "No")
#                                     component_term.setTextColor(2,QColor("red")) 
#                                     component_term.setTextAlignment(2,Qt.AlignHCenter)                 
#                             else:
#                                 if attr == "True":
#                                     component_term.setText(1, "Yes")
#                                     component_term.setTextColor(1,QColor("green"))
#                                     component_term.setTextAlignment(1,Qt.AlignHCenter)
#                                 else:
#                                     component_term.setText(1, "No")
#                                     component_term.setTextColor(1,QColor("red")) 
#                                     component_term.setTextAlignment(1,Qt.AlignHCenter)
                                    
                elif comp.tag.lower() == "componentlist":
                    comtitle = comp.tag
                    component_term = QTreeWidgetItem(self.treewidget)
                    component_term.setText(0, comtitle) 
                    
                    subcompelts = comp.getchildren()
                    for subcomp in subcompelts:
                        if subcomp.tag.lower() == SUBCOMP.lower():
                            
                            subcomtitle = str(subcomp.get(NAME))
                            subcomponent_term = QTreeWidgetItem(component_term)
                            subcomponent_term.setText(0, subcomtitle) 
                            subcomponent_term.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
                            
                            for key in subcomp.keys():
                                self.sub_setTreeWidget(subcomp, key, subcomponent_term)
                            

    def sub_setTreeWidget(self, comp, key, component_term):
        
        if key == "skip" or key == "completed":
            attr = "%s"%(comp.get(key))
            if key == "skip":
                if attr == "True":
#                                component_term.setCheckState(2, Qt.Checked)
                    component_term.setText(2, "Yes")
                    component_term.setTextColor(2,QColor("green"))
                    component_term.setTextAlignment(2,Qt.AlignHCenter)
                else:
#                                component_term.setCheckState(2, Qt.Unchecked)
                    component_term.setText(2, "No")
                    component_term.setTextColor(2,QColor("red")) 
                    component_term.setTextAlignment(2,Qt.AlignHCenter)                 
            else:
#                            component_term.setIcon(1, QIcon("./images/%s" %(attr)))
                if attr == "True":
                    component_term.setText(1, "Yes")
                    component_term.setTextColor(1,QColor("green"))
                    component_term.setTextAlignment(1,Qt.AlignHCenter)
                else:
                    component_term.setText(1, "No")
                    component_term.setTextColor(1,QColor("red")) 
                    component_term.setTextAlignment(1,Qt.AlignHCenter)
        
        

    def reject(self):
        if self.mythread != None:
            self.mythread.terminate()
            self.mythread = None
        QDialog.accept(self)

    def accept(self):
        self.outputWindow.clear()
#        fileloc = self.proconfig.getConfigElement(PROJECT,LOCATION)
#        pname = self.proconfig.getConfigElement(PROJECT,NAME)
#        cmd = "python ../core/openamos_run.py %s/%s.xml" %(fileloc,pname)
        fileloc1 = self.proconfig.fileloc
        cmd = "python ../core/openamos_run.py -file %s" %(fileloc1)
        
        self.runbutton.setDisabled(True)
        self.cancelbutton.setDisabled(True)
        self.mythread = Worker(self,cmd)
        self.mythread.progress.connect(self.write_meg)
        self.mythread.start()


    def write_meg(self,s):
        self.outputWindow.append(s)

#    def update(self,out):
#        self.outputWindow.append(out)
#
#    def updateUi(self,ec):
#        self.dialogButtonBox.button(QDialogButtonBox.Ok).setEnabled(True)
#        self.outputWindow.append('Process finished with exit code - %s' %ec)

#    def sendOutput(self):
#        self.index = self.index + 1
#        self.outputWindow.append(QString(self.proc.readAllStandardOutput()))        
#
#    def sendError(self):
#        self.outputWindow.append(QString(self.proc.readAllStandardError()))  

    

#    def accept(self):
#        self.outputWindow.clear()
#        fileloc = self.proconfig.getConfigElement(PROJECT,LOCATION)
#        pname = self.proconfig.getConfigElement(PROJECT,NAME)
#        cmd = "python ../core/openamos_run.py %s/%s.xml" %(fileloc,pname)
#        
##        self.process = Popen(cmd, shell = True,
##                  stdout = PIPE,
##                  stderr = PIPE)
#        #"python ../core/openamos_run.py C:/mag_zone/mag_zone.xml"
#        
#        #self.proc.start(QString(cmd))
#        #print self.proc.started()
#        #self.thread.initiate(cmd)
#        
#        self.dialogButtonBox.button(QDialogButtonBox.Ok).setEnabled(False)
#
##        if not self.process.startDetached (QString(cmd)):
##            self.outputWindow.setText(QString("*** Failed to run ***"))
##            return
#        
##        stdout, stderr= subprocess.Popen(cmd, shell = True, 
##                                         stdout = subprocess.PIPE,
##                                         stderr = subprocess.PIPE).communicate()
#
#        p = subprocess.Popen(cmd, shell = True,
#                                         stdout = subprocess.PIPE,
#                                         stderr = subprocess.STDOUT)
#
#        while True:
#            line = p.stdout.readline()
#            if not line: break
#            self.outputWindow.append(QString(line))
#            sys.stdout.flush()

        
#    def enqueue_output(self, out, queue):
#        for line in iter(out.readline, ''):
#            queue.put(line)
#        out.close()



class Worker(QThread):
    progress = pyqtSignal(QString)
    
    def __init__(self, parent = None, cmd=None):
        QThread.__init__(self, parent)
        self.cmd = cmd
        #self.process = QProcess()
        #self.connect(self.process, SIGNAL("readyReadStdout()"), self.sendOutput)
        #self.connect(self.process, SIGNAL("readyReadStderr()"), self.sendErrors)
     
        
    def initiate(self,cmd,output):
        self.cmd = cmd
        self.outputWindow = output
#        self.start()

    def run(self):

#        stdout,stderr = subprocess.Popen(self.cmd, shell = False,bufsize=0, 
#                                         stdout = subprocess.PIPE,
#                                         stderr = subprocess.STDOUT ).communicate()

        self.p = subprocess.Popen(self.cmd, shell = True, 
                                         stdout = subprocess.PIPE,
                                         stderr = subprocess.STDOUT )

        while True:
            line = self.p.stdout.readline()
            if not line: break
            self.progress.emit(line)
            sys.stdout.flush()

        father = self.parent()
        father.runbutton.setVisible(False)
        father.cancelbutton.setText("Finish")
        father.cancelbutton.setEnabled(True)
        
#        p = Popen(self.cmd, shell = True,
#                                         stdout = PIPE,
#                                         stderr = STDOUT)


#        while True:
#            print 'in loop'
#            line = self.proc.stdout.readline()
#            print 'after read'
#            if not line: break
#            self.emit(SIGNAL("output(QString)"),QString(line))
#            sys.stdout.flush()

#        while self.proc.poll() is None:
#            print 'in loop'
#            line = self.proc.stdout.readline()
#            self.emit(SIGNAL("output(QString)"),QString(line)) 
#            self.proc.stdout.flush()          
#        self.proc = QProcess()
#        print "created a QProcess"
#        self.connect(self.proc, SIGNAL("readyReadStdout()"), self.sendOutput)
#        #self.connect(self.proc, SIGNAL("readyReadStderr()"), self.sendErrors)
#        print "created connections"
#        self.proc.start(QString(self.cmd))
#        print "started process..."
#
#    def sendOutput(self):
#        print "someoutput from thread"
#        self.emit(SIGNAL("output(QString)"),QString(self.process.readStdout()))
#
#    def sendErrors(self):
#        print "someerror from thread"
#        self.emit(SIGNAL("output(QString)"),QString(self.process.readLineStderr()))    
        


#class CompStatWidget(QWidget):
#    def __init__(self, compname, proconfig, parent=None):
#        super(CompStatWidget, self).__init__(parent)
#        hlayout = QHBoxLayout()
#        self.setLayout(hlayout)
#        complabel = QLabel(compname)
#        hlayout.addWidget(complabel)
#        compsimstat = proconfig.getCompSimStatus(compname)
#        completedlabel = QLabel()
#        self.skipbox = QCheckBox()
#        if compsimstat != None:
#            completedlabel.setPixmap(QPixmap("./images/%s" %(compsimstat[0])))
#            self.skipbox.setCheckState(compsimstat[1])
#            self.skipbox.setEnabled(compsimstat[0]) 
#        else:
#            completedlabel.setPixmap(QPixmap("./images/false"))
#            self.skipbox.setCheckState(False)
#            self.skipbox.setEnabled(False)          
#        hlayout.addWidget(completedlabel)
#        hlayout.addWidget(self.skipbox)


