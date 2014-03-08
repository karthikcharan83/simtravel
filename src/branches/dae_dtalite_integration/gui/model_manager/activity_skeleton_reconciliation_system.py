from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spec_abstract_dialog import *
from openamos.gui.env import *



class Skeleton_Reconciliation_System(QWidget):
    def __init__(self, parent=None, co=None):
        super(Skeleton_Reconciliation_System, self).__init__(parent)
        
        self.setWindowTitle('Activity Skeleton Reconciliation System')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        skeleton_reconciliation_button = QPushButton('Activity \nSkeleton Reconciliation', self)
        skeleton_reconciliation_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 350, 200, 80)
        skeleton_reconciliation_button.setStyleSheet("background-color: #00C5CD")
        #self.connect(skeleton_reconciliation_button, SIGNAL('clicked()'), self.skeleton_reconciliation)
        #self.connect(workersbutton, SIGNAL('clicked()'), qApp, SLOT('Close()'))
        
        person_constraints_1_button = QPushButton("Within person constraints", self)     
        person_constraints_1_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 240, 200, 80)
        person_constraints_1_button.setStyleSheet("background-color: #00C5CD")
        #self.connect(person_constraints_1_button, SIGNAL('clicked()'), self.person_constraints_1)

        
        adjustment_1_button = QPushButton('Adjustments to the activity \nskeleton based on expected \nTravel Time from previous day', self)
        adjustment_1_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 130, 200, 80)
        adjustment_1_button.setStyleSheet("background-color: #00C5CD")
        #self.connect(adjustment_1_button, SIGNAL('clicked()'), self.adjustment_1)

        
        Dummy  = QPushButton('', self)
        Dummy.setGeometry(0, size.height() - 4, 1140, 2)
        
        self.configob = co
        
        
#    def skeleton_reconciliation(self):
#        diagtitle = COMPMODEL_ASRECONCIL
#        modelkey = MODELKEY_ASRECONCIL
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def person_constraints_1(self):
#        diagtitle = COMPMODEL_ASCONST
#        modelkey = MODELKEY_ASCONST
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def adjustment_1(self):
#        diagtitle = COMPMODEL_ASADJUST
#        modelkey = MODELKEY_ASADJUST
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def pattern_reconciliation(self):
#        diagtitle = COMPMODEL_ATRECONCIL
#        modelkey = MODELKEY_ATRECONCIL
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def person_constraints_2(self):
#        diagtitle = COMPMODEL_ATPERCONST
#        modelkey = MODELKEY_ATPERCONST
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def hhold_constraints(self):
#        diagtitle = COMPMODEL_ATHOUCONST
#        modelkey = MODELKEY_ATHOUCONST
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def adjustment_2(self):
#        diagtitle = COMPMODEL_ATADJUST
#        modelkey = MODELKEY_ATADJUST
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        
        

    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 2, widgetheight / 2 - 270, widgetwidth / 2, widgetheight / 2 - 130)
        #line.drawLine(widgetwidth / 2 + 200, widgetheight / 2 - 140, widgetwidth / 2 + 200, widgetheight / 2 + 110)
        line.end()
        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()
        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 240)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 130)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))


        arrow.end()


 


