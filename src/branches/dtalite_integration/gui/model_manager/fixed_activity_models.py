# -*- coding: cp936 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spec_abstract_dialog import *
from openamos.gui.env import *


class FixedActivityModels(QWidget):

    def __init__(self, parent=None, co=None):
        super(FixedActivityModels, self).__init__(parent)

        self.setWindowTitle('Fixed Activity Location Choice Generator')
        self.setAutoFillBackground(True)
        size = parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()


#        workers_button = QPushButton('Workers', self)
#        workers_button.setGeometry((size.width()) / 4 - 100, size.height() / 2 - 400,200, 50)
# self.connect(workersbutton, SIGNAL('clicked()'), qApp, SLOT('Close()'))
#
#        children_adult_button = QPushButton("Students \n(Children 5-14 years)\n+ (Adults)", self)
#        children_adult_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 400, 200, 50)
#
#
#        children_button = QPushButton('Preschoolers \n(Children 0-4 years)', self)
#        children_button.setGeometry((size.width()) * 3 / 4 - 100, size.height() / 2 - 400, 200, 50)
#
#
#        work_loc_button = QPushButton('Identify Primary Work Location \n\n\nSimulate Choice Sets \nWithin 90-120 mins \nTravel from Residence', self)
#        work_loc_button.setGeometry((size.width()) / 4 - 100, size.height() / 2 - 320, 200, 400)
#        self.connect(work_loc_button, SIGNAL('clicked()'), self.work_loc)
#
#
#        school_loc_button = QPushButton('School Location \n\n\nSimulate Choice Sets \nWithin 60 mins \nTravel from Residence', self)
#        school_loc_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 320, 200, 400)
#        self.connect(school_loc_button, SIGNAL('clicked()'), self.school_loc)
#
#
#        preschool_loc_button = QPushButton('Pre-school Location \n\n\nSimulate Choice Sets \nWithin 20 mins \nTravel from either \nWork or Residence', self)
#        preschool_loc_button.setGeometry((size.width()) * 3 / 4 - 100, size.height() / 2 - 320, 200, 400)
#        self.connect(preschool_loc_button, SIGNAL('clicked()'), self.preschool_loc)
#
#
#        activity_loc_button = QPushButton('Fixed Activity Locations for the Population', self)
#        activity_loc_button.setGeometry((size.width()) / 4 - 100, size.height() / 2 + 110, (size.width()) / 2 + 200, 50)

        Dummy = QPushButton('', self)
        Dummy.setGeometry(0, size.height() - 4, 1140, 2)

        self.configob = co

    def work_loc(self):
        diagtitle = COMPMODEL_WORKLOC
        modelkey = MODELKEY_WORKLOC

        diag = AbtractSpecDialog(self.configob, modelkey, diagtitle)
        diag.exec_()

    def school_loc(self):
        diagtitle = COMPMODEL_SCHLOC1
        modelkey = MODELKEY_SCHLOC1

        diag = AbtractSpecDialog(self.configob, modelkey, diagtitle)
        diag.exec_()

    def preschool_loc(self):
        diagtitle = COMPMODEL_PRESCHLOC
        modelkey = MODELKEY_PRESCHLOC

        diag = AbtractSpecDialog(self.configob, modelkey, diagtitle)
        diag.exec_()

    def paintEvent(self, parent=None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 4, widgetheight / 2 - 350,
                      widgetwidth / 4, widgetheight / 2 - 320)
        line.drawLine(widgetwidth / 4, widgetheight / 2 + 80,
                      widgetwidth / 4, widgetheight / 2 + 110)
        line.drawLine(widgetwidth / 2, widgetheight / 2 - 350,
                      widgetwidth / 2, widgetheight / 2 - 320)
        line.drawLine(widgetwidth / 2, widgetheight / 2 + 80,
                      widgetwidth / 2, widgetheight / 2 + 110)
        line.drawLine(widgetwidth * 3 / 4, widgetheight / 2 -
                      350, widgetwidth * 3 / 4, widgetheight / 2 - 320)
        line.drawLine(widgetwidth * 3 / 4, widgetheight / 2 + 80,
                      widgetwidth * 3 / 4, widgetheight / 2 + 110)
        line.end()
        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()
        point.setX(widgetwidth / 4)
        point.setY(widgetheight / 2 - 320)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 4)
        point.setY(widgetheight / 2 + 110)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 2)
        point.setY(widgetheight / 2 - 320)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 2)
        point.setY(widgetheight / 2 + 110)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth / 4)
        point.setY(widgetheight / 2 + 110)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth * 3 / 4)
        point.setY(widgetheight / 2 - 320)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        point.setX(widgetwidth * 3 / 4)
        point.setY(widgetheight / 2 + 110)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(), point.y()), QPoint(
            point.x() - 4, point.y() - 13), QPoint(point.x() + 4, point.y() - 13))

        arrow.setBrush(QColor("#F0F0F0"))
        arrow.drawRoundedRect(
            widgetwidth / 4 - 100, widgetheight / 2 - 400, 200, 50, 15.0, 15.0)
        arrow.drawRoundedRect(
            widgetwidth / 2 - 100, widgetheight / 2 - 400, 200, 50, 15.0, 15.0)
        arrow.drawRoundedRect(
            widgetwidth * 3 / 4 - 100, widgetheight / 2 - 400, 200, 50, 15.0, 15.0)
        arrow.drawRoundedRect(
            widgetwidth / 4 - 100, widgetheight / 2 - 320, 200, 400, 15.0, 15.0)
        arrow.drawRoundedRect(
            widgetwidth / 2 - 100, widgetheight / 2 - 320, 200, 400, 15.0, 15.0)
        arrow.drawRoundedRect(
            widgetwidth * 3 / 4 - 100, widgetheight / 2 - 320, 200, 400, 15.0, 15.0)
        arrow.drawRoundedRect(
            widgetwidth / 4 - 100, widgetheight / 2 + 110, widgetwidth / 2 + 200, 50, 15.0, 15.0)

        arrow.end()

        # Drawing text
        text = QPainter()
        text.begin(self)
        point = QPoint()

        temp = QRect(widgetwidth / 4 - 100, widgetheight / 2 - 400, 200, 50)
        text.drawText(temp, Qt.AlignCenter, 'Workers')

        temp = QRect(widgetwidth / 2 - 100, widgetheight / 2 - 400, 200, 50)
        text.drawText(
            temp, Qt.AlignCenter, 'Students \n(Children 5-14 years)\n+ (Adults)')

        temp = QRect(
            widgetwidth * 3 / 4 - 100, widgetheight / 2 - 400, 200, 50)
        text.drawText(
            temp, Qt.AlignCenter, 'Preschoolers \n(Children 0-4 years)')

        temp = QRect(widgetwidth / 4 - 100, widgetheight / 2 - 320, 200, 400)
        text.drawText(
            temp, Qt.AlignCenter, 'Identify Primary Work Location \n\n\nSimulate Choice Sets \nWithin 90-120 mins \nTravel from Residence')

        temp = QRect(widgetwidth / 2 - 100, widgetheight / 2 - 320, 200, 400)
        text.drawText(
            temp, Qt.AlignCenter, 'School Location \n\n\nSimulate Choice Sets \nWithin 60 mins \nTravel from Residence')

        temp = QRect(
            widgetwidth * 3 / 4 - 100, widgetheight / 2 - 320, 200, 400)
        text.drawText(
            temp, Qt.AlignCenter, 'Pre-school Location \n\n\nSimulate Choice Sets \nWithin 20 mins \nTravel from either \nWork or Residence')

        temp = QRect(
            widgetwidth / 4 - 100, widgetheight / 2 + 110, widgetwidth / 2 + 200, 50)
        text.drawText(
            temp, Qt.AlignCenter, 'Fixed Activity Locations for the Population')

        text.end()
