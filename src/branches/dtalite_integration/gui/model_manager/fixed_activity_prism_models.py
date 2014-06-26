from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spec_abstract_dialog import *
from openamos.gui.env import *

class FixedActivityPrismModels(QWidget):
    def __init__(self, parent=None, co=None):
        super(FixedActivityPrismModels,self).__init__(parent)
        
        self.configob = co
        self.setWindowTitle('Fixed Activity Prism Models')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        self.color = buttonColor(self.configob)
        # Earliest Day Start Time
        self.day_start1_button = QPushButton('Adult Workers', self) #COMPMODEL_DAYSTART, self)
        self.day_start1_button.setGeometry((size.width()) / 2 - 200, size.height() / 2 - 450,180, 50)
        self.day_start1_button.setStyleSheet(self.color.isUserModel(MODELKEY_DAYSTART_AW))
        self.connect(self.day_start1_button, SIGNAL('clicked()'), self.day_start_aw)
        
        self.day_start2_button = QPushButton('Adult Non-workers', self) #COMPMODEL_DAYSTART, self)
        self.day_start2_button.setGeometry((size.width()) / 2 - 200, size.height() / 2 - 370,180, 50)
        self.day_start2_button.setStyleSheet(self.color.isUserModel(MODELKEY_DAYSTART_AN))
        self.connect(self.day_start2_button, SIGNAL('clicked()'), self.day_start_nw)

        self.day_start3_button = QPushButton('Children (5-17 years) and\nAdult Students', self) #COMPMODEL_DAYSTART, self)
        self.day_start3_button.setGeometry((size.width()) / 2 - 200, size.height() / 2 - 290,180, 50)
        self.day_start3_button.setStyleSheet(self.color.isUserModel(MODELKEY_DAYSTART_NA))
        self.connect(self.day_start3_button, SIGNAL('clicked()'), self.day_start_na)

        self.day_start4_button = QPushButton('Pre-school Children\n(0-4 years)', self) #COMPMODEL_DAYSTART, self)
        self.day_start4_button.setGeometry((size.width()) / 2 - 200, size.height() / 2 - 210,180, 50)
        self.day_start4_button.setStyleSheet(self.color.isUserModel(MODELKEY_DAYSTART_PS))
        self.connect(self.day_start4_button, SIGNAL('clicked()'), self.day_start_ps)
        
        
        # Latest Day End Time
        self.day_end1_button = QPushButton('Adult Workers', self) #COMPMODEL_DAYEND, self)     
        self.day_end1_button.setGeometry((size.width()) / 2 + 350, size.height() / 2 - 450, 180, 50)
        self.day_end1_button.setStyleSheet(self.color.isUserModel(MODELKEY_DAYEND_AW))
        self.connect(self.day_end1_button, SIGNAL('clicked()'), self.day_end_aw)        

        self.day_end2_button = QPushButton('Adult Non-workers', self) #COMPMODEL_DAYEND, self)     
        self.day_end2_button.setGeometry((size.width()) / 2 + 350, size.height() / 2 - 370, 180, 50)
        self.day_end2_button.setStyleSheet(self.color.isUserModel(MODELKEY_DAYEND_AN))
        self.connect(self.day_end2_button, SIGNAL('clicked()'), self.day_end_nw)

        self.day_end3_button = QPushButton('Children (5-17 years) and\nAdult Students', self) #COMPMODEL_DAYEND, self)     
        self.day_end3_button.setGeometry((size.width()) / 2 + 350, size.height() / 2 - 290, 180, 50)
        self.day_end3_button.setStyleSheet(self.color.isUserModel(MODELKEY_DAYEND_NA))
        self.connect(self.day_end3_button, SIGNAL('clicked()'), self.day_end_na)

        self.day_end4_button = QPushButton('Pre-school Children\n(0-4 years)', self) #COMPMODEL_DAYEND, self)     
        self.day_end4_button.setGeometry((size.width()) / 2 + 350, size.height() / 2 - 210, 180, 50)
        self.day_end4_button.setStyleSheet(self.color.isUserModel(MODELKEY_DAYEND_PS))
        self.connect(self.day_end4_button, SIGNAL('clicked()'), self.day_end_ps)



        # Adult worker   
        self.num_work_episodes_button = QPushButton(COMPMODEL_WRKEPISODES, self)
        self.num_work_episodes_button.setGeometry((size.width()) / 2 - 325, size.height() / 2 - 50, 160, 50)
        self.num_work_episodes_button.setStyleSheet(self.color.isUserModel(MODELKEY_WRKEPISODES))
        self.connect(self.num_work_episodes_button, SIGNAL('clicked()'), self.num_work)

        self.work_start_button = QPushButton(COMPMODEL_WORKSTART, self)
        self.work_start_button.setGeometry((size.width()) / 2 - 125, size.height() / 2 - 50, 160, 50)
        self.work_start_button.setStyleSheet(self.color.isUserModel(MODELKEY_WORKSTART))
        self.connect(self.work_start_button, SIGNAL('clicked()'), self.work_start)

        self.work_end_button = QPushButton(COMPMODEL_WORKEND, self)
        self.work_end_button.setGeometry((size.width()) / 2 + 75, size.height() / 2 - 50, 160, 50)
        self.work_end_button.setStyleSheet(self.color.isUserModel(MODELKEY_WORKEND))
        self.connect(self.work_end_button, SIGNAL('clicked()'), self.work_end)

        self.work_start_1_button = QPushButton(COMPMODEL_WORKSTART1, self)
        self.work_start_1_button.setGeometry((size.width()) / 2 - 200, size.height() / 2 + 30, 160, 50)
        self.work_start_1_button.setStyleSheet(self.color.isUserModel(MODELKEY_WORKSTART1))
        self.connect(self.work_start_1_button, SIGNAL('clicked()'), self.work_start1)

        self.work_end_1_button = QPushButton(COMPMODEL_WORKEND1, self)
        self.work_end_1_button.setGeometry((size.width()) / 2, size.height() / 2 + 30, 160, 50)
        self.work_end_1_button.setStyleSheet(self.color.isUserModel(MODELKEY_WORKEND1))
        self.connect(self.work_end_1_button, SIGNAL('clicked()'), self.work_end1)
        
        self.work_start_2_button = QPushButton(COMPMODEL_WORKSTART2, self)
        self.work_start_2_button.setGeometry((size.width()) / 2 + 200, size.height() / 2 + 30, 160, 50)
        self.work_start_2_button.setStyleSheet(self.color.isUserModel(MODELKEY_WORKSTART2))
        self.connect(self.work_start_2_button, SIGNAL('clicked()'), self.work_start2)

        self.work_end_2_button = QPushButton(COMPMODEL_WORKEND2, self)
        self.work_end_2_button.setGeometry((size.width()) / 2 + 400, size.height() / 2 + 30, 160, 50)
        self.work_end_2_button.setStyleSheet(self.color.isUserModel(MODELKEY_WORKEND2))
        self.connect(self.work_end_2_button, SIGNAL('clicked()'), self.work_end2)

        
        # Children (5 - 17)
        self.children_arrive_button = QPushButton(COMPMODEL_SCHSTART, self)
        self.children_arrive_button.setGeometry((size.width()) / 2 - 105, size.height() / 2 + 190, 170, 50)
        self.children_arrive_button.setStyleSheet(self.color.isUserModel(MODELKEY_SCHSTART))
        self.connect(self.children_arrive_button, SIGNAL('clicked()'), self.school_start)

        self.children_depart_button = QPushButton(COMPMODEL_SCHEND, self)
        self.children_depart_button.setGeometry((size.width()) / 2 + 115, size.height() / 2 + 190, 170, 50)
        self.children_depart_button.setStyleSheet(self.color.isUserModel(MODELKEY_SCHEND))
        self.connect(self.children_depart_button, SIGNAL('clicked()'), self.school_end)


        # Children (0 - 4)
        self.presch_arrive_button = QPushButton(COMPMODEL_PRESCHSTART, self)
        self.presch_arrive_button.setGeometry((size.width()) / 2 - 105, size.height() / 2 + 350, 170, 50)
        self.presch_arrive_button.setStyleSheet(self.color.isUserModel(MODELKEY_PRESCHSTART))
        self.connect(self.presch_arrive_button, SIGNAL('clicked()'), self.preschool_start)

        self.presch_depart_button = QPushButton(COMPMODEL_PRESCHEND, self)
        self.presch_depart_button.setGeometry((size.width()) / 2 + 115, size.height() / 2 + 350, 170, 50)
        self.presch_depart_button.setStyleSheet(self.color.isUserModel(MODELKEY_PRESCHEND))
        self.connect(self.presch_depart_button, SIGNAL('clicked()'), self.preschool_end)

        
        Dummy  = QPushButton('', self)
        Dummy.setGeometry(0, size.height() - 4, 1140, 2)



  
    def day_start_aw(self):
        diagtitle = COMPMODEL_DAYSTART
        modelkey = MODELKEY_DAYSTART_AW
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.day_start1_button.setStyleSheet(self.color.isUserModel(modelkey))
        
    def day_start_nw(self):
        diagtitle = COMPMODEL_DAYSTART
        modelkey = MODELKEY_DAYSTART_AN
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.day_start2_button.setStyleSheet(self.color.isUserModel(modelkey))
        
    def day_start_na(self):
        diagtitle = COMPMODEL_DAYSTART
        modelkey = MODELKEY_DAYSTART_NA
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.day_start3_button.setStyleSheet(self.color.isUserModel(modelkey))
        
    def day_start_ps(self):
        diagtitle = COMPMODEL_DAYSTART
        modelkey = MODELKEY_DAYSTART_PS
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.day_start4_button.setStyleSheet(self.color.isUserModel(modelkey))
        
        
    def day_end_aw(self):
        diagtitle = COMPMODEL_DAYEND
        modelkey = MODELKEY_DAYEND_AW
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.day_end1_button.setStyleSheet(self.color.isUserModel(modelkey))
        
    def day_end_nw(self):
        diagtitle = COMPMODEL_DAYEND
        modelkey = MODELKEY_DAYEND_AN
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.day_end2_button.setStyleSheet(self.color.isUserModel(modelkey))
        
    def day_end_na(self):
        diagtitle = COMPMODEL_DAYEND
        modelkey = MODELKEY_DAYEND_NA
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.day_end3_button.setStyleSheet(self.color.isUserModel(modelkey))
        
    def day_end_ps(self):
        diagtitle = COMPMODEL_DAYEND
        modelkey = MODELKEY_DAYEND_PS
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.day_end4_button.setStyleSheet(self.color.isUserModel(modelkey))
        
        
    def num_work(self):
        diagtitle = COMPMODEL_WRKEPISODES
        modelkey = MODELKEY_WRKEPISODES
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.num_work_episodes_button.setStyleSheet(self.color.isUserModel(modelkey))
        

    def work_start(self):
        diagtitle = COMPMODEL_WORKSTART
        modelkey = MODELKEY_WORKSTART
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.work_start_button.setStyleSheet(self.color.isUserModel(modelkey))
        
        
    def work_end(self):
        diagtitle = COMPMODEL_WORKEND
        modelkey = MODELKEY_WORKEND
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.work_end_button.setStyleSheet(self.color.isUserModel(modelkey))
        
        
    def work_start1(self):
        diagtitle = COMPMODEL_WORKSTART1
        modelkey = MODELKEY_WORKSTART1
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.work_start_1_button.setStyleSheet(self.color.isUserModel(modelkey))
        
        
    def work_end1(self):
        diagtitle = COMPMODEL_WORKEND1
        modelkey = MODELKEY_WORKEND1
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.work_end_1_button.setStyleSheet(self.color.isUserModel(modelkey))
        

    def work_start2(self):
        diagtitle = COMPMODEL_WORKSTART2
        modelkey = MODELKEY_WORKSTART2
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.work_start_2_button.setStyleSheet(self.color.isUserModel(modelkey))
        
        
    def work_end2(self):
        diagtitle = COMPMODEL_WORKEND2
        modelkey = MODELKEY_WORKEND2
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.work_end_2_button.setStyleSheet(self.color.isUserModel(modelkey))
        
        
    def school_start(self):
        diagtitle = COMPMODEL_SCHSTART
        modelkey = MODELKEY_SCHSTART
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.children_arrive_button.setStyleSheet(self.color.isUserModel(modelkey))
        
        
    def school_end(self):
        diagtitle = COMPMODEL_SCHEND
        modelkey = MODELKEY_SCHEND
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.children_depart_button.setStyleSheet(self.color.isUserModel(modelkey))
        
        
#    def non_worker(self):
#        diagtitle = COMPMODEL_NONWORKER
#        modelkey = MODELKEY_NONWORKER
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        
        
#    def pre_sch(self):
#        diagtitle = COMPMODEL_ARRIVALDEPARTPRESCH
#        modelkey = MODELKEY_ARRIVALDEPARTPRESCH
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        
        
    def preschool_start(self):
        diagtitle = COMPMODEL_PRESCHSTART
        modelkey = MODELKEY_PRESCHSTART
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.presch_arrive_button.setStyleSheet(self.color.isUserModel(modelkey))
        
        
    def preschool_end(self):
        diagtitle = COMPMODEL_PRESCHEND
        modelkey = MODELKEY_PRESCHEND
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.presch_depart_button.setStyleSheet(self.color.isUserModel(modelkey))
        
        
#    def t_s_prism_vertices(self):
#        diagtitle = COMPMODEL_TIMESPACE
#        modelkey = MODELKEY_TIMESPACE
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()


   
    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)

        line.drawLine(widgetwidth / 2 - 243, widgetheight / 2 - 425, widgetwidth / 2 - 243, widgetheight / 2 - 185)
        line.drawLine(widgetwidth / 2 - 285, widgetheight / 2 - 425, widgetwidth / 2 - 200, widgetheight / 2 - 425)
        line.drawLine(widgetwidth / 2 - 243, widgetheight / 2 - 345, widgetwidth / 2 - 200, widgetheight / 2 - 345)
        line.drawLine(widgetwidth / 2 - 243, widgetheight / 2 - 265, widgetwidth / 2 - 200, widgetheight / 2 - 265)
        line.drawLine(widgetwidth / 2 - 243, widgetheight / 2 - 185, widgetwidth / 2 - 200, widgetheight / 2 - 185)

        line.drawLine(widgetwidth / 2 + 307, widgetheight / 2 - 425, widgetwidth / 2 + 307, widgetheight / 2 - 185)
        line.drawLine(widgetwidth / 2 + 265, widgetheight / 2 - 425, widgetwidth / 2 + 350, widgetheight / 2 - 425)
        line.drawLine(widgetwidth / 2 + 307, widgetheight / 2 - 345, widgetwidth / 2 + 350, widgetheight / 2 - 345)
        line.drawLine(widgetwidth / 2 + 307, widgetheight / 2 - 265, widgetwidth / 2 + 350, widgetheight / 2 - 265)
        line.drawLine(widgetwidth / 2 + 307, widgetheight / 2 - 185, widgetwidth / 2 + 350, widgetheight / 2 - 185)

        line.drawLine(widgetwidth / 2 - 245, widgetheight / 2, widgetwidth / 2 - 245, widgetheight / 2 + 55)
        line.drawLine(widgetwidth / 2 - 365, widgetheight / 2 - 25, widgetwidth / 2 + 75, widgetheight / 2 - 25)
        line.drawLine(widgetwidth / 2 - 245, widgetheight / 2 + 55, widgetwidth / 2 + 400, widgetheight / 2 + 55)
        
        line.drawLine(widgetwidth / 2 - 365, widgetheight / 2 + 215, widgetwidth / 2 + 115, widgetheight / 2 + 215)
        line.drawLine(widgetwidth / 2 - 365, widgetheight / 2 + 375, widgetwidth / 2 + 115, widgetheight / 2 + 375)


        line.end()
        
        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()


        # Earliest Day Start Time
        point.setX(widgetwidth / 2 - 200)  
        point.setY(widgetheight / 2 - 425)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 - 200)  
        point.setY(widgetheight / 2 - 345)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 - 200)  
        point.setY(widgetheight / 2 - 265)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 - 200)  
        point.setY(widgetheight / 2 - 185)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))


        # Latest Day End Time
        point.setX(widgetwidth / 2 + 350)  
        point.setY(widgetheight / 2 - 425)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 + 350)  
        point.setY(widgetheight / 2 - 345)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 + 350)  
        point.setY(widgetheight / 2 - 265)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 + 350)  
        point.setY(widgetheight / 2 - 185)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        
        # Adult Workers
        point.setX(widgetwidth / 2 - 325)  
        point.setY(widgetheight / 2 - 25)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 - 125)  
        point.setY(widgetheight / 2 - 25)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 + 75)  
        point.setY(widgetheight / 2 - 25)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 - 200)  
        point.setY(widgetheight / 2 + 55)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 + 55)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 + 200)  
        point.setY(widgetheight / 2 + 55)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 + 400)  
        point.setY(widgetheight / 2 + 55)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        
        # Children (5-17 years)
        point.setX(widgetwidth / 2 - 315)  
        point.setY(widgetheight / 2 + 215)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 - 105)  
        point.setY(widgetheight / 2 + 215)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 + 115)  
        point.setY(widgetheight / 2 + 215)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        # Children (5-17 years)
        point.setX(widgetwidth / 2 - 315)  
        point.setY(widgetheight / 2 + 375)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 - 105)  
        point.setY(widgetheight / 2 + 375)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        point.setX(widgetwidth / 2 + 115)  
        point.setY(widgetheight / 2 + 375)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        
        
        arrow.setBrush(QColor("#1e90ff"))
        arrow.drawRoundedRect(widgetwidth/2 - 525, widgetheight/2 - 50, 160, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 - 525, widgetheight/2 + 190, 170, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 - 525, widgetheight/2 + 350, 170, 50, 15.0, 15.0)
        arrow.setBrush(QColor("#F0F0F0"))
        arrow.drawRoundedRect(widgetwidth/2 - 465, widgetheight/2 - 450, 180, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 + 85, widgetheight/2 - 450, 180, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 - 315, widgetheight/2 + 190, 170, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 - 315, widgetheight/2 + 350, 170, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 + 410, widgetheight/2 + 250, 150, 150, 15.0, 15.0)
        
        arrow.end()


        text = QPainter()
        text.begin(self)
        point = QPoint()
        
        point.setX(widgetwidth / 2 - 160)  
        point.setY(widgetheight / 2 - 30)
        text.drawText(point, "One")

        point.setX(widgetwidth / 2 - 270)  
        point.setY(widgetheight / 2 + 30)
        text.drawText(point, "Two")
        
        temp = QRect(widgetwidth/2 - 465, widgetheight/2 - 450, 180, 50)
        text.drawText(temp, Qt.AlignCenter, 'Earliest Day Start Time')
        
        temp = QRect(widgetwidth/2 + 85, widgetheight/2 - 450, 180, 50)
        text.drawText(temp, Qt.AlignCenter, 'Latest Day End Time')

        temp = QRect(widgetwidth/2 - 525, widgetheight/2 - 50, 160, 50)
        text.drawText(temp, Qt.AlignCenter, 'Adult Workers')

        temp = QRect(widgetwidth/2 - 525, widgetheight/2 + 190, 170, 50)
        text.drawText(temp, Qt.AlignCenter, 'Children (5-17 years)')
        
        temp = QRect(widgetwidth/2 - 315, widgetheight/2 + 190, 170, 50)
        text.drawText(temp, Qt.AlignCenter, 'Daily School Episode')
        
        temp = QRect(widgetwidth/2 - 525, widgetheight/2 + 350, 170, 50)
        text.drawText(temp, Qt.AlignCenter, 'Pre-school Children\n(0-4 years)')
        
        temp = QRect(widgetwidth/2 - 315, widgetheight/2 + 350, 170, 50)
        text.drawText(temp, Qt.AlignCenter, 'Daily Pre-school Episode')
        
        temp = QRect(widgetwidth/2 + 410, widgetheight/2 + 250, 150, 150)
        text.drawText(temp, Qt.AlignCenter, 'Pre-school arrival and\ndeparture times are\ndependent on the adult\n(worker/non-worker)\nthat the kid is\nassigned to')

        text.end()


        
