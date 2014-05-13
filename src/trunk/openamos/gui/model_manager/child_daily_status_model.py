from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spec_abstract_dialog import *
from openamos.gui.env import *


class Child_Status_Model(QWidget):
    def __init__(self, parent=None, co=None):
        super(Child_Status_Model, self).__init__(parent)
        self.setWindowTitle('Child Daily Status')
        self.setAutoFillBackground(True)
        size =  parent.geometry()

        self.configob = co
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()

        self.color = buttonColor(self.configob)
        # Children (5-17 years)
        self.goto_school_button = QPushButton('Child goes to\nschool on\ntravel day', self)
        self.goto_school_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 460, 120, 75)
        self.goto_school_button.setStyleSheet(self.color.isUserModel(MODELKEY_SCHDAILYSTATUS))
        self.connect(self.goto_school_button, SIGNAL('clicked()'), self.goto_school)

        self.independent_to_school_button = QPushButton('Child travels to\nschool\nindependently', self)
        self.independent_to_school_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 360, 120, 75)
        self.independent_to_school_button.setStyleSheet(self.color.isUserModel(MODELKEY_SCHDAILYINDEP))
        self.connect(self.independent_to_school_button, SIGNAL('clicked()'), self.travel_independently_to_school)

#        drop_off_school1_button = QPushButton('Assign an adult drop-off event to\nhousehold', self)
#        drop_off_school1_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 - 235, 200, 50)
#        drop_off_school1_button.setStyleSheet("background-color: #FFFDD0")
#        #self.connect(drop_off_school1_button, SIGNAL('clicked()'), self.drop_off_event)

#         self.independent_from_school_button = QPushButton('Child\nindependent\nafter-school', self)
#         self.independent_from_school_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 135, 120, 75)
#         self.independent_from_school_button.setStyleSheet(self.color.isUserModel(MODELKEY_AFTSCHDAILYINDEP))
#         self.connect(self.independent_from_school_button, SIGNAL('clicked()'), self.independently_after_school)

#        after_school_activity_button = QPushButton('Is there time to\nengage in an\nafter school\nchild activity?', self)
#        after_school_activity_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 35, 120, 75)
#        after_school_activity_button.setStyleSheet("background-color: #FFFDD0")
#        #self.connect(after_school_activity_button, SIGNAL('clicked()'), self.after_school_activity)

#         self.activity_type_button = QPushButton('After-school activity type choice', self)
#         self.activity_type_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 + 90, 200, 50)
#         self.activity_type_button.setStyleSheet(self.color.isUserModel(MODELKEY_AFTSCHACTTYPEWRKR))
#         self.connect(self.activity_type_button, SIGNAL('clicked()'), self.activity_type_nonwrkr)
#
#         self.destination_button = QPushButton('After-school activity\ndestination choice', self)
#         self.destination_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 + 170, 200, 50)
#         self.destination_button.setStyleSheet(self.color.isUserModel(MODELKEY_AFTSCHACTDEST))
#         self.connect(self.destination_button, SIGNAL('clicked()'), self.activity_dest)
#
#         self.duration_button = QPushButton('After-school activity\nduration model', self)
#         self.duration_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 + 250, 200, 50)
#         self.duration_button.setStyleSheet(self.color.isUserModel(MODELKEY_AFTSCHACTDUR))
#         self.connect(self.duration_button, SIGNAL('clicked()'), self.activity_dur)

#        drop_off_school2_button = QPushButton('Assign an adult drop-off event to\nhousehold', self)
#        drop_off_school2_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 + 330, 200, 50)
#        drop_off_school2_button.setStyleSheet("background-color: #FFFDD0")
#        #self.connect(drop_off_school2_button, SIGNAL('clicked()'), self.drop_off_event)

#         self.activity_with_adult_button = QPushButton('Adult stays with child for\nactivity', self)
#         self.activity_with_adult_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 + 410, 200, 50)
#         self.activity_with_adult_button.setStyleSheet(self.color.isUserModel(MODELKEY_AFTSCHJOINTACT))
#         self.connect(self.activity_with_adult_button, SIGNAL('clicked()'), self.activity_with_adult)

        self.in_activity_independently_button = QPushButton('Child is\nindependent', self)
        self.in_activity_independently_button.setGeometry((size.width()) / 2 - 340, size.height() / 2 - 460, 120, 75)
        self.in_activity_independently_button.setStyleSheet(self.color.isUserModel(MODELKEY_HMINDEP))
        self.connect(self.in_activity_independently_button, SIGNAL('clicked()'), self.child_independent)

#        assign_hh_button = QPushButton('Assign an adult stay-\nhome event to household', self)
#        assign_hh_button.setGeometry((size.width()) / 2 - 500, size.height() / 2 - 360, 200, 50)
#        assign_hh_button.setStyleSheet("background-color: #FFFDD0")
#        #self.connect(assign_hh_button, SIGNAL('clicked()'), self.assign_hh)
#
#        travel_mode_school_button = QPushButton('Simulate mode\nchoice dynamically', self)
#        travel_mode_school_button.setGeometry(widgetwidth/2 - 360, widgetheight/2 - 123, 160, 50)
#        travel_mode_school_button.setStyleSheet("background-color: #FFFDD0")
#        #self.connect(generate_travel_pattern_button, SIGNAL('clicked()'), self.generate_travel_pattern)
#
#        pick_up_school_button = QPushButton('Assign an adult pick-up event to\nhousehold', self)
#        pick_up_school_button.setGeometry((size.width()) / 2 - 380, size.height() / 2 - 23, 200, 50)
#        pick_up_school_button.setStyleSheet("background-color: #FFFDD0")
#        #self.connect(pick_up_school_button, SIGNAL('clicked()'), self.pick_up_event)




        # Pre-school Children
        # Child goes to\npre-school on\n travel day
        self.goto_preschool_button0 = QPushButton('0 Year Old', self)
        self.goto_preschool_button0.setGeometry((size.width()) / 2 + 160, size.height() / 2 - 420, 120, 20)
        self.goto_preschool_button0.setStyleSheet(self.color.isUserModel(MODELKEY_SCHSTATUSAGE0))
        self.connect(self.goto_preschool_button0, SIGNAL('clicked()'), self.goto_preschool0)

        self.goto_preschool_button1 = QPushButton('1 Year Old', self)
        self.goto_preschool_button1.setGeometry((size.width()) / 2 + 160, size.height() / 2 - 395, 120, 20)
        self.goto_preschool_button1.setStyleSheet(self.color.isUserModel(MODELKEY_SCHSTATUSAGE1))
        self.connect(self.goto_preschool_button1, SIGNAL('clicked()'), self.goto_preschool1)

        self.goto_preschool_button2 = QPushButton('2 Years Old', self)
        self.goto_preschool_button2.setGeometry((size.width()) / 2 + 160, size.height() / 2 - 370, 120, 20)
        self.goto_preschool_button2.setStyleSheet(self.color.isUserModel(MODELKEY_SCHSTATUSAGE2))
        self.connect(self.goto_preschool_button2, SIGNAL('clicked()'), self.goto_preschool2)

        self.goto_preschool_button3 = QPushButton('3 Years Old', self)
        self.goto_preschool_button3.setGeometry((size.width()) / 2 + 160, size.height() / 2 - 345, 120, 20)
        self.goto_preschool_button3.setStyleSheet(self.color.isUserModel(MODELKEY_SCHSTATUSAGE3))
        self.connect(self.goto_preschool_button3, SIGNAL('clicked()'), self.goto_preschool3)

        self.goto_preschool_button4 = QPushButton('4 Years Old', self)
        self.goto_preschool_button4.setGeometry((size.width()) / 2 + 160, size.height() / 2 - 320, 120, 20)
        self.goto_preschool_button4.setStyleSheet(self.color.isUserModel(MODELKEY_SCHSTATUSAGE4))
        self.connect(self.goto_preschool_button4, SIGNAL('clicked()'), self.goto_preschool4)

        # Work Status
        self.work_status1_button = QPushButton('Adult Work Status -\nfirst episode', self)
        self.work_status1_button.setGeometry((size.width()) / 2 + 395, size.height() / 2 - 100,180, 50)
        self.work_status1_button.setStyleSheet(self.color.isUserModel(MODELKEY_WRKSTATUSADL1))
        self.connect(self.work_status1_button, SIGNAL('clicked()'), self.work_status1)

        self.work_status2_button = QPushButton('Adult Work Status -\nsecond episode', self)
        self.work_status2_button.setGeometry((size.width()) / 2 + 395, size.height() / 2 - 20,180, 50)
        self.work_status2_button.setStyleSheet(self.color.isUserModel(MODELKEY_WRKSTATUSADL2))
        self.connect(self.work_status2_button, SIGNAL('clicked()'), self.work_status2)

        self.nonadult_work_status_button = QPushButton('Non-Adult Work Status', self)
        self.nonadult_work_status_button.setGeometry((size.width()) / 2 + 395, size.height() / 2 + 60,180, 50)
        self.nonadult_work_status_button.setStyleSheet(self.color.isUserModel(MODELKEY_WRKSTATUSNON))
        self.connect(self.nonadult_work_status_button, SIGNAL('clicked()'), self.nonadult_work)

        Dummy  = QPushButton('', self)
        Dummy.setGeometry(0, size.height() - 4, 1140, 2)


    def goto_school(self):
        diagtitle = COMPMODEL_SCHSTATUSNON
        modelkey = MODELKEY_SCHSTATUSNON

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.goto_school_button.setStyleSheet(self.color.isUserModel(modelkey))


    def goto_preschool0(self):
        diagtitle = COMPMODEL_SCHSTATUSAGE
        modelkey = MODELKEY_SCHSTATUSAGE0

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.goto_preschool_button0.setStyleSheet(self.color.isUserModel(modelkey))

    def goto_preschool1(self):
        diagtitle = COMPMODEL_SCHSTATUSAGE
        modelkey = MODELKEY_SCHSTATUSAGE1

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.goto_preschool_button1.setStyleSheet(self.color.isUserModel(modelkey))

    def goto_preschool2(self):
        diagtitle = COMPMODEL_SCHSTATUSAGE
        modelkey = MODELKEY_SCHSTATUSAGE2

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.goto_preschool_button2.setStyleSheet(self.color.isUserModel(modelkey))

    def goto_preschool3(self):
        diagtitle = COMPMODEL_SCHSTATUSAGE
        modelkey = MODELKEY_SCHSTATUSAGE3

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.goto_preschool_button3.setStyleSheet(self.color.isUserModel(modelkey))

    def goto_preschool4(self):
        diagtitle = COMPMODEL_SCHSTATUSAGE
        modelkey = MODELKEY_SCHSTATUSAGE4

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.goto_preschool_button4.setStyleSheet(self.color.isUserModel(modelkey))


    def child_independent(self):
        diagtitle = COMPMODEL_KIDINDEPENDENT
        modelkey = MODELKEY_KIDDEPENDENT

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.in_activity_independently_button.setStyleSheet(self.color.isUserModel(modelkey))

    def travel_independently_to_school(self):
        diagtitle = COMPMODEL_KIDINDEPENDENT
        modelkey = MODELKEY_KIDDEPENDENT

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.independent_to_school_button.setStyleSheet(self.color.isUserModel(modelkey))

    def independently_after_school(self):
        diagtitle = COMPMODEL_AFTSCHDAILYINDEP
        modelkey = MODELKEY_AFTSCHDAILYINDEP

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.independent_from_school_button.setStyleSheet(self.color.isUserModel(modelkey))


    def activity_type_nonwrkr(self):
        diagtitle = COMPMODEL_AFTSCHACTTYPE
        modelkey = MODELKEY_AFTSCHACTTYPENONWRKR

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.activity_type_button.setStyleSheet(self.color.isUserModel(modelkey))

    def activity_type_with_work(self):
        diagtitle = COMPMODEL_AFTSCHACTTYPE
        modelkey = MODELKEY_AFTSCHACTTYPEWRKR

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.activity_type_button.setStyleSheet(self.color.isUserModel(modelkey))

    def activity_dest(self):
        diagtitle = COMPMODEL_AFTSCHACTDEST
        modelkey = MODELKEY_AFTSCHACTDEST

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.destination_button.setStyleSheet(self.color.isUserModel(modelkey))

    def activity_dur(self):
        diagtitle = COMPMODEL_AFTSCHACTDUR
        modelkey = MODELKEY_AFTSCHACTDUR

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.duration_button.setStyleSheet(self.color.isUserModel(modelkey))

    def activity_with_adult(self):
        diagtitle = COMPMODEL_AFTSCHJOINTACT
        modelkey = MODELKEY_AFTSCHJOINTACT

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()

        self.activity_with_adult_button.setStyleSheet(self.color.isUserModel(modelkey))

    def work_status1(self):
        diagtitle = COMPMODEL_WRKSTATUSADL
        modelkey = MODELKEY_WRKSTATUSADL1

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.work_status1_button.setStyleSheet(self.color.isUserModel(modelkey))

    def work_status2(self):
        diagtitle = COMPMODEL_WRKSTATUSADL
        modelkey = MODELKEY_WRKSTATUSADL2

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.work_status2_button.setStyleSheet(self.color.isUserModel(modelkey))

    def nonadult_work(self):
        diagtitle = COMPMODEL_WRKSTATUSNON
        modelkey = MODELKEY_WRKSTATUSNON

        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        self.nonadult_work_status_button.setStyleSheet(self.color.isUserModel(modelkey))

    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)

        # Children (5-17 years)
        line.drawLine(widgetwidth / 2 - 40, widgetheight / 2 - 520, widgetwidth / 2 - 40, widgetheight / 2 + 0)
        line.drawLine(widgetwidth / 2 - 280, widgetheight / 2 - 400, widgetwidth / 2 - 280, widgetheight / 2 - 270)
        #line.drawLine(widgetwidth / 2 - 280, widgetheight / 2 - 3, widgetwidth / 2 - 280, widgetheight / 2 + 67)

        line.drawLine(widgetwidth / 2 - 230, widgetheight / 2 - 423, widgetwidth / 2 - 90, widgetheight / 2 - 423)
        line.drawLine(widgetwidth / 2 - 170, widgetheight / 2 - 110, widgetwidth / 2 - 90, widgetheight / 2 - 110) #line.drawLine(widgetwidth / 2 - 230, widgetheight / 2 - 98, widgetwidth / 2 - 90, widgetheight / 2 - 98)
        #line.drawLine(widgetwidth / 2 - 230, widgetheight / 2 + 3, widgetwidth / 2 - 90, widgetheight / 2 + 3)

        line.drawLine(widgetwidth / 2 - 330, widgetheight / 2 - 423, widgetwidth / 2 - 400, widgetheight / 2 - 423)
        line.drawLine(widgetwidth / 2 - 400, widgetheight / 2 - 423, widgetwidth / 2 - 400, widgetheight / 2 - 350)

#         line.drawLine(widgetwidth / 2 - 350, widgetheight / 2 - 255, widgetwidth / 2 - 400, widgetheight / 2 - 255)
#         line.drawLine(widgetwidth / 2 - 400, widgetheight / 2 - 255, widgetwidth / 2 - 400, widgetheight / 2 - 98)
#         line.drawLine(widgetwidth / 2 - 350, widgetheight / 2 - 98, widgetwidth / 2 - 400, widgetheight / 2 - 98)

        line.drawLine(widgetwidth / 2 - 90, widgetheight / 2 - 323, widgetwidth / 2 - 170, widgetheight / 2 - 323)
        line.drawLine(widgetwidth / 2 - 170, widgetheight / 2 - 323, widgetwidth / 2 - 170, widgetheight / 2 - 110)

#         line.drawLine(widgetwidth / 2 - 50, widgetheight / 2 - 98, widgetwidth / 2 + 90, widgetheight / 2 - 98)
#         line.drawLine(widgetwidth / 2 + 90, widgetheight / 2 - 98, widgetwidth / 2 + 90, widgetheight / 2 + 435)
#         line.drawLine(widgetwidth / 2 + 30, widgetheight / 2 + 435, widgetwidth / 2 + 90, widgetheight / 2 + 435)

        # Pre-school Children
        line.drawLine(widgetwidth / 2 + 220, widgetheight / 2 - 520, widgetwidth / 2 + 220, widgetheight / 2 - 175)
        line.drawLine(widgetwidth / 2 + 270, widgetheight / 2 - 363, widgetwidth / 2 + 370, widgetheight / 2 - 363)

        # Work Statue
        line.drawLine(widgetwidth / 2 + 352, widgetheight / 2 - 75, widgetwidth / 2 + 352, widgetheight / 2 + 85)
        line.drawLine(widgetwidth / 2 + 310, widgetheight / 2 - 75, widgetwidth / 2 + 395, widgetheight / 2 - 75)
        line.drawLine(widgetwidth / 2 + 352, widgetheight / 2 + 5, widgetwidth / 2 + 395, widgetheight / 2 + 5)
        line.drawLine(widgetwidth / 2 + 352, widgetheight / 2 + 85, widgetwidth / 2 + 395, widgetheight / 2 + 85)

        line.end()



        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 2 - 40)
        point.setY(widgetheight / 2 - 460)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 40)
        point.setY(widgetheight / 2 - 360)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 40)
        point.setY(widgetheight / 2 - 235)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 40)
        point.setY(widgetheight / 2 - 135)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 40)
        point.setY(widgetheight / 2 - 35)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

#         point.setX(widgetwidth / 2 - 40)
#         point.setY(widgetheight / 2 + 90)
#         arrow.setBrush(QColor("black"))
#         arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

#         point.setX(widgetwidth / 2 - 40)
#         point.setY(widgetheight / 2 + 170)
#         arrow.setBrush(QColor("black"))
#         arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
#
#         point.setX(widgetwidth / 2 - 40)
#         point.setY(widgetheight / 2 + 250)
#         arrow.setBrush(QColor("black"))
#         arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
#
#         point.setX(widgetwidth / 2 - 40)
#         point.setY(widgetheight / 2 + 330)
#         arrow.setBrush(QColor("black"))
#         arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
#
#         point.setX(widgetwidth / 2 - 40)
#         point.setY(widgetheight / 2 + 410)
#         arrow.setBrush(QColor("black"))
#         arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 280)
        point.setY(widgetheight / 2 - 280)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

#         point.setX(widgetwidth / 2 - 280)
#         point.setY(widgetheight / 2 + 57)
#         arrow.setBrush(QColor("black"))
#         arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
#
        point.setX(widgetwidth / 2 - 400)
        point.setY(widgetheight / 2 - 360)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        # Arrow for west
        point.setX(widgetwidth / 2 - 220)
        point.setY(widgetheight / 2 - 423)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13,point.y() + 4))

        point.setX(widgetwidth / 2 - 100)
        point.setY(widgetheight / 2 - 110)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        #arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13,point.y() + 4))

#         point.setX(widgetwidth / 2 - 180)
#         point.setY(widgetheight / 2 + 3)
#         arrow.setBrush(QColor("black"))
#         arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13,point.y() + 4))
#
#         point.setX(widgetwidth / 2 + 20)
#         point.setY(widgetheight / 2 - 98)
#         arrow.setBrush(QColor("black"))
#         arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13,point.y() + 4))

        # Arrow for east
#         point.setX(widgetwidth / 2 - 360)
#         point.setY(widgetheight / 2 - 255)
#         arrow.setBrush(QColor("black"))
#         arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))



        # Pre-school Children (0-4 years)
        point.setX(widgetwidth / 2 + 220)
        point.setY(widgetheight / 2 - 460)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 220)
        point.setY(widgetheight / 2 - 255)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 220)
        point.setY(widgetheight / 2 - 175)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 360)
        point.setY(widgetheight / 2 -363)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))


        # Work Status Arrows
        point.setX(widgetwidth / 2 + 395)
        point.setY(widgetheight / 2 - 75)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))

        point.setX(widgetwidth / 2 + 395)
        point.setY(widgetheight / 2 + 5)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))

        point.setX(widgetwidth / 2 + 395)
        point.setY(widgetheight / 2 + 85)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))


        arrow.setBrush(QColor("#1e90ff"))
        arrow.drawRoundedRect(widgetwidth/2 - 120, widgetheight/2 - 560, 160, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 + 140, widgetheight/2 - 560, 160, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 + 130, widgetheight/2 - 100, 180, 50, 15.0, 15.0)

        arrow.setBrush(QColor("#F0F0F0"))
        # arrow.drawRoundedRect(widgetwidth/2 - 360, widgetheight/2 + 57, 160, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 - 360, widgetheight/2 - 280, 160, 50, 15.0, 15.0)

        arrow.drawRoundedRect(widgetwidth/2 - 140, widgetheight/2 - 235, 200, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 - 100, widgetheight/2 - 135, 120, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 - 140, widgetheight/2 - 35, 200, 50, 15.0, 15.0)
        # arrow.drawRoundedRect(widgetwidth/2 - 140, widgetheight/2 + 330, 200, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 - 500, widgetheight/2 - 360, 200, 50, 15.0, 15.0)
#         arrow.drawRoundedRect(widgetwidth/2 - 360, widgetheight/2 - 123, 160, 50, 15.0, 15.0)
        # arrow.drawRoundedRect(widgetwidth/2 - 380, widgetheight/2 - 23, 200, 50, 15.0, 15.0)

        arrow.drawRoundedRect(widgetwidth/2 + 360, widgetheight/2 - 388, 160, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 + 130, widgetheight/2 - 460, 180, 170, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 + 130, widgetheight/2 - 255, 180, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 + 130, widgetheight/2 - 175, 180, 50, 15.0, 15.0)

        arrow.end()

        # Drawing text
        text = QPainter()
        text.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 2 - 60)
        point.setY(widgetheight / 2 - 375)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 - 160)
        point.setY(widgetheight / 2 - 428)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 275)
        point.setY(widgetheight / 2 - 330)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 - 400)
        point.setY(widgetheight / 2 - 428)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 170)
        point.setY(widgetheight / 2 - 328)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 - 57)
        point.setY(widgetheight / 2 - 260)
        text.drawText(point, "No")

#         point.setX(widgetwidth / 2 - 150)
#         point.setY(widgetheight / 2 - 103)
#         text.drawText(point, "Yes")

#         point.setX(widgetwidth / 2 - 57)
#         point.setY(widgetheight / 2 - 50)
#         text.drawText(point, "No")

#         point.setX(widgetwidth / 2 - 60)
#         point.setY(widgetheight / 2 + 65)
#         text.drawText(point, "Yes")

#         point.setX(widgetwidth / 2 - 140)
#         point.setY(widgetheight / 2 - 2)
#         text.drawText(point, "No")


        # Pre-school Children
        point.setX(widgetwidth / 2 + 200)
        point.setY(widgetheight / 2 - 275)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 + 320)
        point.setY(widgetheight / 2 - 368)
        text.drawText(point, "No")

        temp = QRect(widgetwidth/2 - 120, widgetheight/2 - 560, 160, 50)
        text.drawText(temp, Qt.AlignCenter, 'Children\n(5-17 years)')

        temp = QRect(widgetwidth/2 + 140, widgetheight/2 - 560, 160, 50)
        text.drawText(temp, Qt.AlignCenter, 'Pre-school Children\n(0-4 years)')

        # temp = QRect(widgetwidth/2 - 360, widgetheight/2 + 57, 160, 50)
        # text.drawText(temp, Qt.AlignCenter, 'Return home')

        temp = QRect(widgetwidth/2 - 360, widgetheight/2 - 280, 160, 50)
        text.drawText(temp, Qt.AlignCenter, 'Simulate activity\ntravel patterns for\nchild dynamically')

        temp = QRect(widgetwidth/2 - 140, widgetheight/2 - 235, 200, 50)
        text.drawText(temp, Qt.AlignCenter, 'Assign an adult drop-off event to\nhousehold')

        temp = QRect(widgetwidth/2 - 100, widgetheight/2 - 135, 120, 50)
        text.drawText(temp, Qt.AlignCenter, 'Arrive School')

        temp = QRect(widgetwidth/2 - 140, widgetheight/2 - 35, 200, 50)
        text.drawText(temp, Qt.AlignCenter, 'After School Activity')
        #text.drawText(temp, Qt.AlignCenter, 'Is there time to\nengage in an\nafter school\nchild activity?')

        # temp = QRect(widgetwidth/2 - 140, widgetheight/2 + 330, 200, 50)
        # text.drawText(temp, Qt.AlignCenter, 'Assign an adult drop-off event to\nhousehold')

        temp = QRect(widgetwidth/2 - 500, widgetheight/2 - 360, 200, 50)
        text.drawText(temp, Qt.AlignCenter, 'Assign an adult stay-\nhome event to household')

#         temp = QRect(widgetwidth/2 - 360, widgetheight/2 - 123, 160, 50)
#         text.drawText(temp, Qt.AlignCenter, 'Simulate mode\nchoice dynamically')

        # temp = QRect(widgetwidth/2 - 380, widgetheight/2 - 23, 200, 50)
        # text.drawText(temp, Qt.AlignCenter, 'Assign an adult pick-up event to\nhousehold')

        temp = QRect(widgetwidth/2 + 360, widgetheight/2 - 388, 160, 50)
        text.drawText(temp, Qt.AlignCenter, 'Assign an adult stay-\nhome event to household')

        temp = QRect(widgetwidth/2 + 130, widgetheight/2 - 460, 180, 50)
        text.drawText(temp, Qt.AlignCenter, 'Child goes to pre-school\non travel day')

        temp = QRect(widgetwidth/2 + 130, widgetheight/2 - 255, 180, 50)
        text.drawText(temp, Qt.AlignCenter, 'Assign an adult drop-off event to\nhousehold')

        temp = QRect(widgetwidth/2 + 130, widgetheight/2 - 175, 180, 50)
        text.drawText(temp, Qt.AlignCenter, 'Assign an adult pick-up event to \nhousehold')


        temp = QRect(widgetwidth/2 + 130, widgetheight/2 - 100, 180, 50)
        text.drawText(temp, Qt.AlignCenter, 'Work Status')

        text.end()
