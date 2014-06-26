from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spec_abstract_dialog import *
from openamos.gui.env import *


class Adult_Model(QWidget):

    def __init__(self, parent=None, co=None):
        super(Adult_Model, self).__init__(parent)
        self.setWindowTitle('Adult Daily Status Model')
        self.setAutoFillBackground(True)
        size = parent.geometry()

        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()

        children_assigned_button = QPushButton(
            "Dependent events assigned to household? \n(Stay-home and/or Chauffeuring)", self)
        children_assigned_button.setGeometry(
            (size.width()) / 2 - 150, 40, 300, 60)
        children_assigned_button.setStyleSheet("background-color: #00C5CD")
        self.connect(children_assigned_button, SIGNAL(
            'clicked()'), self.children_assigned)

#        children_stay_home_button = QPushButton("Households with dependent \nstay-home events", self)
#        children_stay_home_button.setGeometry((size.width()) / 2 - 100, 140, 200, 50)
# children_stay_home_button.setStyleSheet("background-color: #FFFDD0")
#
#        children_chauffeuring_button = QPushButton("Households with dependent \nchauffeuring events", self)
#        children_chauffeuring_button.setGeometry((size.width()) * 3 / 4 - 100, 140, 200, 50)
# children_chauffeuring_button.setStyleSheet("background-color: #FFFDD0")

        nonworking_adult_button = QPushButton(
            'Households with at least \none non-working adult', self)
        nonworking_adult_button.setGeometry(
            (size.width()) / 2 - 100, 220, 200, 50)
        nonworking_adult_button.setStyleSheet("background-color: #00C5CD")
        self.connect(
            nonworking_adult_button, SIGNAL('clicked()'), self.nonworking_adult)

        all_working_adult_button = QPushButton(
            'Households with all \nworking adults', self)
        all_working_adult_button.setGeometry(
            (size.width()) / 4 - 100, 220, 200, 50)
        all_working_adult_button.setStyleSheet("background-color: #00C5CD")
        self.connect(all_working_adult_button, SIGNAL(
            'clicked()'), self.all_working_adult)

        assign_children_3_button = QPushButton(
            'Assign each dependent child \nto a household adult subject \nto the fixed activity schedule', self)
        assign_children_3_button.setGeometry(
            (size.width()) * 3 / 4 - 100, 220, 200, 80)
        assign_children_3_button.setStyleSheet("background-color: #00C5CD")
        self.connect(assign_children_3_button, SIGNAL(
            'clicked()'), self.assign_children_3)

        assign_children_1_button = QPushButton(
            'Assign all dependent \nchildren to a working adult', self)
        assign_children_1_button.setGeometry(
            (size.width()) / 4 - 100, 300, 200, 50)
        assign_children_1_button.setStyleSheet("background-color: #00C5CD")
        self.connect(assign_children_1_button, SIGNAL(
            'clicked()'), self.assign_children_1)

        assign_children_2_button = QPushButton(
            'Assign all dependent \nchildren to one \nnon-working adult', self)
        assign_children_2_button.setGeometry(
            (size.width()) / 2 - 100, 300, 200, 50)
        assign_children_2_button.setStyleSheet("background-color: #00C5CD")
        self.connect(assign_children_2_button, SIGNAL(
            'clicked()'), self.assign_children_2)

#        adult_work_button = QPushButton('This adult works from home', self)
#        adult_work_button.setGeometry((size.width()) / 4 - 100, 380, 200, 50)
# adult_work_button.setStyleSheet("background-color: #FFFDD0")
# self.connect(adult_work_button, SIGNAL('clicked()'), self.adult_work)

        check_adult_button = QPushButton('Adult work status', self)
        check_adult_button.setGeometry((size.width()) / 2 - 100, 470, 200, 50)
        check_adult_button.setStyleSheet("background-color: #00C5CD")
        self.connect(check_adult_button, SIGNAL('clicked()'), self.check_adult)

        work_today_button = QPushButton(
            'Adult worker going to \nwork on travel day?', self)
        work_today_button.setGeometry((size.width()) / 4 - 100, 550, 200, 50)
        work_today_button.setStyleSheet("background-color: #00C5CD")
        self.connect(work_today_button, SIGNAL('clicked()'), self.work_today)

#        work_from_home_button = QPushButton('Work from home', self)
#        work_from_home_button.setGeometry((size.width()) / 4 - 100, 630, 200, 50)
#
#        go_to_work_button = QPushButton('Go to work', self)
#        go_to_work_button.setGeometry((size.width()) / 2 - 100, 630, 200, 50)
#
#        no_work_episodes_button = QPushButton('No work episodes', self)
#        no_work_episodes_button.setGeometry((size.width()) * 3 / 4 - 100, 630, 200, 50)

        Dummy = QPushButton('', self)
        Dummy.setGeometry(0, size.height() - 4, 1140, 2)

        self.configob = co

    def children_assigned(self):
        diagtitle = COMPMODEL_ASISDEPEND
        modelkey = MODELKEY_ASISDEPEND

        diag = AbtractSpecDialog(self.configob, modelkey, diagtitle)
        diag.exec_()

    def nonworking_adult(self):
        diagtitle = COMPMODEL_ASONENWORKER
        modelkey = MODELKEY_ASONENWORKER

        diag = AbtractSpecDialog(self.configob, modelkey, diagtitle)
        diag.exec_()

    def all_working_adult(self):
        diagtitle = COMPMODEL_ASHOUSEWORKER
        modelkey = MODELKEY_ASHOUSEWORKER

        diag = AbtractSpecDialog(self.configob, modelkey, diagtitle)
        diag.exec_()

    def assign_children_3(self):
        diagtitle = COMPMODEL_ASASSIGNHOUSE
        modelkey = MODELKEY_ASASSIGNHOUSE

        diag = AbtractSpecDialog(self.configob, modelkey, diagtitle)
        diag.exec_()

    def assign_children_1(self):
        diagtitle = COMPMODEL_ASDEPENDWORKER
        #modelkey = MODELKEY_ASDEPENDWORKER
        modelkey = MODELKEY_WRKEPISODES

        diag = AbtractSpecDialog(self.configob, modelkey, diagtitle)
        diag.exec_()

    def assign_children_2(self):
        diagtitle = COMPMODEL_ASDEPENDNONWORK
        #modelkey = MODELKEY_ASDEPENDNONWORK
        modelkey = MODELKEY_WRKSTATUSNON

        diag = AbtractSpecDialog(self.configob, modelkey, diagtitle)
        diag.exec_()

    def check_adult(self):
        diagtitle = COMPMODEL_ASISWORKER
        #modelkey = MODELKEY_ASISWORKER
        modelkey = MODELKEY_WRKSTATUSADL1

        diag = AbtractSpecDialog(self.configob, modelkey, diagtitle)
        diag.exec_()

    def work_today(self):
        diagtitle = COMPMODEL_WRKDAILYSTATUS
        modelkey = MODELKEY_WRKSTATUSADL2

        diag = AbtractSpecDialog(self.configob, modelkey, diagtitle)
        diag.exec_()


#    def work_from_home(self):
#        diagtitle = COMPMODEL_WORKATHOME
#        modelkey = MODELKEY_WORKATHOME
#
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#
#    def go_to_work(self):
#        diagtitle = COMPMODEL_ASGOTOWORK
#        modelkey = MODELKEY_ASGOTOWORK
#
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#
#
#    def no_work_episodes(self):
#        diagtitle = COMPMODEL_ASNWORKEPISO
#        modelkey = MODELKEY_ASNWORKEPISO
#
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()

    def paintEvent(self, parent=None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 2, 100, widgetwidth / 2, 470)
        line.drawLine(widgetwidth / 2, 120, widgetwidth * 3 / 4, 120)
        line.drawLine(widgetwidth * 3 / 4, 120, widgetwidth * 3 / 4, 450)
        line.drawLine(widgetwidth / 4 - 200, 450, widgetwidth * 3 / 4, 450)
        line.drawLine(widgetwidth / 4 - 200, 450, widgetwidth / 4 - 200, 70)
        line.drawLine(widgetwidth / 2, 70, widgetwidth / 4 - 200, 70)
        line.drawLine(widgetwidth / 2, 205, widgetwidth / 4, 205)
        line.drawLine(widgetwidth / 4, 450, widgetwidth / 4, 205)
        line.drawLine(widgetwidth * 3 / 4, 495, widgetwidth / 4, 495)
        line.drawLine(widgetwidth / 4, 630, widgetwidth / 4, 495)
        line.drawLine(widgetwidth * 3 / 4, 630, widgetwidth * 3 / 4, 495)
        line.drawLine(widgetwidth / 4, 575, widgetwidth / 2, 575)
        line.drawLine(widgetwidth / 2, 630, widgetwidth / 2, 575)
        line.end()

        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 2)
        point.setY(140)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth * 3 / 4)
        point.setY(140)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth * 3 / 4)
        point.setY(220)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 4)
        point.setY(220)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 2)
        point.setY(220)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 4)
        point.setY(300)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 2)
        point.setY(300)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 4)
        point.setY(380)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 2)
        point.setY(470)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 4)
        point.setY(550)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 4)
        point.setY(630)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth * 3 / 4)
        point.setY(630)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 2)
        point.setY(630)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        arrow.setBrush(QColor("#F0F0F0"))
        arrow.drawRoundedRect(widgetwidth / 4 - 100, 630, 200, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth / 2 - 100, 630, 200, 50, 15.0, 15.0)
        arrow.drawRoundedRect(
            widgetwidth * 3 / 4 - 100, 630, 200, 50, 15.0, 15.0)

        arrow.drawRoundedRect(widgetwidth / 2 - 100, 140, 200, 50, 15.0, 15.0)
        arrow.drawRoundedRect(
            widgetwidth * 3 / 4 - 100, 140, 200, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth / 4 - 100, 380, 200, 50, 15.0, 15.0)

        arrow.end()

        # Drawing text
        text = QPainter()
        text.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 4 - 40)
        point.setY(65)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 25)
        point.setY(115)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 4 - 20)
        point.setY(490)
        text.drawText(point, "Worker")

        point.setX(widgetwidth * 3 / 4 - 30)
        point.setY(490)
        text.drawText(point, "Non-Worker")

        point.setX(widgetwidth / 4 - 20)
        point.setY(615)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 110)
        point.setY(570)
        text.drawText(point, "Yes")

        temp = QRect(widgetwidth / 4 - 100, 630, 200, 50)
        text.drawText(temp, Qt.AlignCenter, 'Work from home')

        temp = QRect(widgetwidth / 2 - 100, 630, 200, 50)
        text.drawText(temp, Qt.AlignCenter, 'Go to work')

        temp = QRect(widgetwidth * 3 / 4 - 100, 630, 200, 50)
        text.drawText(temp, Qt.AlignCenter, 'No work episodes')

        temp = QRect(widgetwidth / 2 - 100, 140, 200, 50)
        text.drawText(
            temp, Qt.AlignCenter, "Households with dependent \nstay-home events")

        temp = QRect(widgetwidth * 3 / 4 - 100, 140, 200, 50)
        text.drawText(
            temp, Qt.AlignCenter, "Households with dependent \nchauffeuring events")

        temp = QRect(widgetwidth / 4 - 100, 380, 200, 50)
        text.drawText(temp, Qt.AlignCenter, 'This adult works from home')

        text.end()
