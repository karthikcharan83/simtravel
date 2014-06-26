'''
Created on Mar 3, 2011

@author: dhyou
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from openamos.gui.env import *
from openamos.core.database_management.cursor_database_connection import *
from openamos.core.database_management.database_configuration import *

import time
from datetime import date
import csv


class Import_NHTS(QDialog):

    '''
    classdocs
    '''

    def __init__(self, configobject=None, parent=None):
        #        QDialog.__init__(self, parent)
        QDialog.__init__(self, parent)
        '''
        Constructor
        '''
#        kmz_file = "C:\Documents and Settings\dhyou\Desktop\kkkk.kmz"
#        kml_file = "C:\Documents and Settings\dhyou\Desktop\ddd.kml"
#        fileObj = zipfile.ZipFile(kmz_file,'w')
#        fileObj.write(kml_file, os.path.basename( kml_file ) ,zipfile.ZIP_DEFLATED)
#        fileObj.close()

        self.connects(configobject)
        self.setWindowTitle("Import NHTS to OpenAmos")
        self.setMinimumSize(QSize(300, 200))
        alllayout = QVBoxLayout()
        self.setLayout(alllayout)

        nhtsinputbox = QGroupBox("")
        nhtslayout = QVBoxLayout()
        nhtsinputbox.setLayout(nhtslayout)

        tablenamelabel = QLabel("Select a table")
        nhtslayout.addWidget(tablenamelabel)

        self.nhtstable = QComboBox()
        self.nhtstable.addItems([QString("NHTS Persons"), QString("NHTS Households"),
                                 QString("NHTS Trips")])
        nhtslayout.addWidget(self.nhtstable)

        csvnamelabel = QLabel("Select a CSV file")
        nhtslayout.addWidget(csvnamelabel)

        filewidget = QWidget()
        filelayout = QHBoxLayout()
        filewidget.setLayout(filelayout)
        self.csvname = QLineEdit()
        filelayout.addWidget(self.csvname)
        self.openfilebutton = QPushButton('...')
        self.openfilebutton.setMaximumWidth(30)
        filelayout.addWidget(self.openfilebutton)
        nhtslayout.addWidget(filewidget)

        self.dialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        alllayout.addWidget(nhtsinputbox)
        alllayout.addWidget(self.dialogButtonBox)

        self.connect(
            self.openfilebutton, SIGNAL("clicked(bool)"), self.open_folder)
        self.connect(
            self.dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(
            self.dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
        self.connect(
            self.nhtstable, SIGNAL("currentIndexChanged(int)"), self.clear_line)

    def reject(self):
        self.disconnects()
        QDialog.accept(self)

    def accept(self):
        self.dialogButtonBox.setDisabled(True)

        filename = str(self.csvname.text())
        if filename != "":
            if self.nhtstable.currentIndex() == 0:
                self.import_person(filename)
            elif self.nhtstable.currentIndex() == 1:
                self.import_house(filename)
            elif self.nhtstable.currentIndex() == 2:
                if self.new_obj.check_if_table_exists(str("persons_nhts")):
                    isNext = self.import_trip(filename)
                    if isNext:
                        self.import_schedule(filename)
                else:
                    QMessageBox.warning(self, "Import NHTS dataset...",
                                        QString(
                                            """After importing NHTS Person, you can import it."""),
                                        QMessageBox.Ok)
#            else:
#                self.import_schedule(filename)

        self.dialogButtonBox.setEnabled(True)

    def checkTable(self, table):
        if self.new_obj.check_if_table_exists(str(table)):

            ret = QMessageBox.warning(self, "Import NHTS dataset...",
                                      QString(
                                          """Already, the database contains the NHTS dataset.\nDo you still want to import it?"""),
                                      QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.Yes:
                ssql = "DROP TABLE %s" % (table)
                self.new_obj.cursor.execute(ssql)
                self.new_obj.connection.commit()
            else:
                return False

        return True

    def import_person(self, filename):

        try:

            table = self.table_name_db()
            input = open(filename, 'rb')
            csvReader = csv.reader(input)
            headers = csvReader.next()
            firstrow = csvReader.next()

            if self.checkTable(table):

                if self.isvalid(headers):
                    index = self.index_person(headers)
                    i = 0
                    ssql = "CREATE TABLE %s (" % (table)
                    for name in headers:
                        lname = name.lower()
                        dtype = self.data_type(firstrow[i])
                        if lname == "cmpltpct":
                            dtype = "decimal"

                        if lname == "houseid" or lname == "personid" or lname == "tdcaseid":
                            if lname == "houseid" or lname == "tdcaseid":
                                ssql = "%s%s %s NOT NULL," % (
                                    ssql, lname, dtype)
                            else:
                                ssql = "%s%s %s NOT NULL," % (
                                    ssql, lname, dtype)
                        else:
                            ssql = "%s%s %s," % (ssql, lname, dtype)

                        i += 1

                    ssql = "%s)" % (ssql[0:len(ssql) - 1])
                    self.new_obj.cursor.execute(ssql)

                    if self.new_obj.check_if_table_exists("persons_daily_status_nhts"):
                        ssql = "DROP TABLE persons_daily_status_nhts"
                        self.new_obj.cursor.execute(ssql)
                        self.new_obj.connection.commit()

                    ssql = "CREATE TABLE persons_daily_status_nhts (houseid bigint NOT NULL, personid integer NOT NULL, wrkdailystatus integer)"
                    self.new_obj.cursor.execute(ssql)

                    input.seek(0)
                    csvReader.next()
                    for row in csvReader:
                        ssql = "INSERT INTO %s VALUES(" % (table)
                        for value in row:
                            ssql = "%s'%s'," % (ssql, value)
                        ssql = "%s)" % (ssql[0:len(ssql) - 1])
                        self.new_obj.cursor.execute(ssql)

                        hid = row[index[0]]
                        pid = row[index[1]]
                        ssql = "INSERT INTO persons_daily_status_nhts VALUES(%s,%s,%d)" % (
                            hid, pid, 0)
                        self.new_obj.cursor.execute(ssql)

                    self.new_obj.connection.commit()

                    QMessageBox.information(self, "",
                                            QString(
                                                """Data importing is successful!"""),
                                            QMessageBox.Yes)

                else:
                    QMessageBox.warning(self, "Import NHTS dataset...",
                                        QString(
                                            """You select an incorrect file."""),
                                        QMessageBox.Yes)
            input.close()

        except Exception, e:
            QMessageBox.warning(self, "Import NHTS dataset...",
                                QString(
                                    """Error while inserting rows into the table.\nNull or text is not allowed."""),
                                QMessageBox.Yes)
            input.close()
            print e

    def import_house(self, filename):

        try:

            table = self.table_name_db()
            input = open(filename, 'rb')
            csvReader = csv.reader(input)
            headers = csvReader.next()
            firstrow = csvReader.next()

            if self.checkTable(table):

                if self.isvalid(headers):

                    i = 0
                    ssql = "CREATE TABLE %s (" % (table)
                    for name in headers:
                        lname = name.lower()
                        dtype = self.data_type(firstrow[i])
                        if lname == "cmpltpct":
                            dtype = "decimal"

                        if lname == "houseid" or lname == "personid" or lname == "tdcaseid":
                            if lname == "houseid" or lname == "tdcaseid":
                                ssql = "%s%s %s NOT NULL," % (
                                    ssql, lname, dtype)
                            else:
                                ssql = "%s%s %s NOT NULL," % (
                                    ssql, lname, dtype)
                        else:
                            ssql = "%s%s %s," % (ssql, lname, dtype)

                        i += 1

                    ssql = "%s)" % (ssql[0:len(ssql) - 1])
                    self.new_obj.cursor.execute(ssql)

                    input.seek(0)
                    csvReader.next()
                    for row in csvReader:
                        ssql = "INSERT INTO %s VALUES(" % (table)
                        for value in row:
                            ssql = "%s'%s'," % (ssql, value)
                        ssql = "%s)" % (ssql[0:len(ssql) - 1])
                        self.new_obj.cursor.execute(ssql)

                    self.new_obj.connection.commit()

                    QMessageBox.information(self, "",
                                            QString(
                                                """Data importing is successful!"""),
                                            QMessageBox.Yes)

                else:
                    QMessageBox.warning(self, "Import NHTS dataset...",
                                        QString(
                                            """You select an incorrect file."""),
                                        QMessageBox.Yes)
            input.close()

        except Exception, e:
            QMessageBox.warning(self, "Import NHTS dataset...",
                                QString(
                                    """Error while inserting rows into the table.\nNull or text is not allowed."""),
                                QMessageBox.Yes)
            input.close()
            print e

    def import_trip(self, filename):

        t1 = time.time()
        try:
            table = self.table_name_db()
            input = open(filename, 'rb')
            csvReader = csv.reader(input)
            headers = csvReader.next()

            if self.checkTable(table) and self.isvalid(headers):

                index = self.index_trip(headers)
                if not self.new_obj.check_if_table_exists("trips_nhts"):
                    ssql = "CREATE TABLE trips_nhts (tripid bigint NOT NULL, \
                            houseid bigint NOT NULL, \
                            personid integer NOT NULL, \
                            starttime integer, \
                            endtime integer, \
                            duration integer, \
                            trippurpose integer, wttrdfin decimal)"
                    self.new_obj.cursor.execute(ssql)
                    self.new_obj.connection.commit()
                else:
                    ssql = 'DELETE FROM trips_nhts WHERE tripid >= 0'
                    self.new_obj.cursor.execute(ssql)
                    self.new_obj.connection.commit()

                hid1 = "-1"
                pid1 = "-1"
                hid2 = "-1"
                pid2 = "-1"
                prow = []  # Store previous row of the csv file
                for row in csvReader:

                    hid2 = str(row[index[1]])
                    pid2 = str(row[index[2]])
                    if hid1 != hid2 or pid1 != pid2:
                        hid1 = hid2
                        pid1 = pid2
                        isworker = True
                        ith = 1  # 0: middle of trips (101), 1:last trip (100)

                    if len(prow) > 0:
                        self.import_trip2(prow, ith, index)

                    prow = row
                    if ith == 1:
                        ith = 0

                    wto = int(row[index[5]])
                    if wto >= 10 and wto <= 12 and isworker:
                        ssql = "UPDATE persons_daily_status_nhts SET wrkdailystatus=1 WHERE houseid = %s and personid = %s" % (
                            hid2, pid2)
                        self.new_obj.cursor.execute(ssql)
                        isworker = False

                ith = 1  # last trip
                self.import_trip2(prow, ith, index)
                self.new_obj.connection.commit()

#                QMessageBox.information(self, "",
#                            QString("""Data importing is successful!"""),
#                            QMessageBox.Yes)

            else:
                QMessageBox.warning(self, "Import NHTS dataset...",
                                    QString(
                                        """You select an incorrect file."""),
                                    QMessageBox.Yes)
                return False

            input.close()

        except Exception, e:
            QMessageBox.warning(self, "Import NHTS dataset...",
                                QString(
                                    """Error while inserting rows into the table.\nNull or text is not allowed."""),
                                QMessageBox.Yes)
            input.close()
            print e
            return False

        t2 = time.time()
        print 'time taken is ---> %s' % (t2 - t1)
        return True

    def import_trip2(self, row, ith, index):

        hid2 = str(row[index[1]])
        pid2 = str(row[index[2]])
        etime = self.change_time(row[index[4]])
        stime = self.change_time(row[index[3]])
        if stime >= 0 and etime >= 0:
            duration = etime - stime
        else:
            duration = -99

        wto = self.activity_type(row[index[5]])
        if wto == 100 and ith == 0:
            wto = 101

        trip_sql = "INSERT INTO trips_nhts VALUES(%s,%s,%s,%d,%d,%d,%d,%s)" % (
            row[index[0]], hid2, pid2, stime, etime, duration, wto, row[index[6]])
        self.new_obj.cursor.execute(trip_sql)

    def import_schedule(self, filename):

        t1 = time.time()
        try:
            table = "schedule_nhts"
            input = open(filename, 'rb')
            csvReader = csv.reader(input)
            headers = csvReader.next()
            rownum = 1
            hid1 = "-1"
            pid1 = "-1"
            hid2 = "-1"
            pid2 = "-1"
            prow = ""

#            o = open('C:\\Documents and Settings\\dhyou\\Desktop\\Distributions\\temp.csv','w')
#            header = "SCHEDULEID,HOUSEID,PERSONID,activitytype,starttime,endtime,duration\n"
#            o.write(header)

            if self.isvalid(headers):

                if self.new_obj.check_if_table_exists(str(table)):
                    ssql = "DROP TABLE %s" % (table)
                    self.new_obj.cursor.execute(ssql)
                    self.new_obj.connection.commit()

                i = self.index_schedule(headers)
                if not self.new_obj.check_if_table_exists("schedule_nhts"):
                    ssql = "CREATE TABLE schedule_nhts (scheduleid bigint NOT NULL, \
                            houseid bigint NOT NULL, \
                            personid integer NOT NULL, \
                            activitytype integer NOT NULL, \
                            starttime integer, \
                            endtime integer, \
                            duration integer)"
                    self.new_obj.cursor.execute(ssql)
                    self.new_obj.connection.commit()
                else:
                    ssql = 'DELETE FROM schedule_nhts WHERE scheduleid >= 0'
                    self.new_obj.cursor.execute(ssql)
                    self.new_obj.connection.commit()

                for row in csvReader:

                    hid2 = str(row[i[0]])
                    pid2 = str(row[i[1]])

                    if hid1 != hid2 or pid1 != pid2:
                        if hid1 != "-1" and pid1 != "-1":
                            wto = self.activity_type(prow[i[6]])
                            stime = self.change_time(prow[i[4]])
                            etime = 1439

                            if stime >= 0:
                                duration = etime - stime
                            else:
                                duration = -99
    #                            output = "%s,%s,%s,%s,%d,%d,%d\n" %(str(rownum),hid1,pid1,wto,stime,etime,duration)
    #                            o.write(output)
                            ssql = 'INSERT INTO %s VALUES' % (
                                table) + "('%s', '%s', '%s', '%d', '%d', '%d', '%d');" % (str(rownum), hid1, pid1, wto, stime, etime, duration)
                            self.new_obj.cursor.execute(ssql)
                            rownum += 1

                        wfrom = self.activity_type(row[i[5]])
                        stime = 0
                        etime = self.change_time(row[i[3]])
                        if etime >= 0:
                            duration = etime - stime
                        else:
                            duration = -99

                        ssql = 'INSERT INTO %s VALUES' % (table) + "('%s', '%s', '%s', '%d', '%d', '%d', '%d');" % (
                            str(rownum), hid2, pid2, wfrom, stime, etime, duration)
                        self.new_obj.cursor.execute(ssql)

                    else:
                        wfrom = self.activity_type(row[i[5]])
                        if wfrom == 100:
                            wfrom = 101
                        stime = self.change_time(prow[i[4]])
                        etime = self.change_time(row[i[3]])
                        if stime >= 0 and etime >= 0 and etime >= stime:
                            duration = etime - stime
                        else:
                            duration = -99

                        ssql = 'INSERT INTO %s VALUES' % (table) + "('%s', '%s', '%s', '%d', '%d', '%d', '%d');" % (
                            str(rownum), hid2, pid2, wfrom, stime, etime, duration)
                        self.new_obj.cursor.execute(ssql)

                    rownum += 1
                    hid1 = hid2
                    pid1 = pid2
                    prow = row

                wto = self.activity_type(prow[i[6]])
                stime = self.change_time(prow[i[4]])
                etime = 1439
                if stime >= 0 and etime >= stime:
                    duration = etime - stime
                else:
                    duration = -99

                ssql = 'INSERT INTO %s VALUES' % (
                    table) + "('%s', '%s', '%s', '%d', '%d', '%d', '%d');" % (str(rownum), hid1, pid1, wto, stime, etime, duration)
                self.new_obj.cursor.execute(ssql)
                self.new_obj.connection.commit()

                QMessageBox.information(self, "",
                                        QString(
                                            """Inserting NHTS data is successful"""),
                                        QMessageBox.Yes)

            else:
                QMessageBox.warning(self, "Import NHTS dataset...",
                                    QString(
                                        """You select an incorrect file."""),
                                    QMessageBox.Yes)

            input.close()

        except Exception, e:
            print '\tError while inserting the rows into the table '
            print e
            input.close()

        t2 = time.time()
        print 'time taken is ---> %s' % (t2 - t1)

    def open_folder(self):
        dialog = QFileDialog()
        temp = dialog.getOpenFileName(
            self, "Browse to select a csv file", "", "Comma Delimit (*.csv)")
        self.csvname.setText(temp)

    def data_type(self, value):
        isnumeric = self.isDecimal(value)
        isint = str(value).isdigit()

        if isnumeric and isint:
            if len(value) > 3:
                return "bigint"
            else:
                return "integer"
        elif isnumeric and not isint:
            return "decimal"
        else:
            return "character(25)"

    def isDecimal(self, value):
        try:
            float(value)
            return True
        except Exception, e:
            return False

    def isvalid(self, headers):

        columns = []
        if self.nhtstable.currentIndex() == 0:
            columns = ["houseid", "personid", "wtperfin"]
        elif self.nhtstable.currentIndex() == 1:
            columns = ["houseid"]
        elif self.nhtstable.currentIndex() == 2:
            columns = ['tdcaseid', 'houseid', 'personid',
                       'strttime', 'endtime', 'whyfrom', 'whyto', 'wttrdfin']
        else:
            columns = ['houseid', 'personid', 'tdcaseid',
                       'strttime', 'endtime', 'whyfrom', 'whyto']

        for name in columns:
            if (not name.upper() in headers) and (not name.lower() in headers):
                return False

        return True

    def table_name_db(self):
        if self.nhtstable.currentIndex() == 0:
            return "persons_nhts"
        elif self.nhtstable.currentIndex() == 1:
            return "households_nhts"
        elif self.nhtstable.currentIndex() == 2:
            return "trips_nhts"
        else:
            return "schedule_nhts"

    def index_person(self, headers):
        columns = ['houseid', 'personid']
        index = []
        i = 0
        for header in headers:
            headers[i] = header.lower()
            i += 1

        for column in columns:
            low = headers.index(column)
            index.append(low)

        return index

    def index_trip(self, headers):
        columns = ['tdcaseid', 'houseid', 'personid',
                   'strttime', 'endtime', 'whyto', 'wttrdfin']
        index = []
        i = 0
        for header in headers:
            headers[i] = header.lower()
            i += 1

        for column in columns:
            low = headers.index(column)
            index.append(low)

        return index

    def index_schedule(self, headers):
        columns = ['houseid', 'personid', 'tdcaseid',
                   'strttime', 'endtime', 'whyfrom', 'whyto']
        index = []
        i = 0
        for header in headers:
            headers[i] = header.lower()
            i += 1

        for column in columns:
            low = headers.index(column)
            index.append(low)

        return index

    def activity_type(self, value):
        if str(value).isdigit():
            act = int(value)
            if act == 1:
                return 100
            elif act >= 10 and act <= 14:
                return 200
            elif act >= 20 and act <= 24:
                return 300
            elif act >= 60 and act <= 65:
                return 411
            elif act >= 40 and act <= 43:
                return 412
            elif act == 80 or act == 82 or act == 83:
                return 415
            elif act == 50 or act == 53 or act == 81:
                return 513
            elif act == 51 or act == 54 or act == 55:
                return 514
            elif act == 70 or act == 71:
                return 600
            elif act == 72 or act == 73:
                return 601

        return 599

    def change_time(self, value):
        if int(value) >= 0:
            if len(value) == 3:
                min = int(value[-2:])
                hr = int(value[0])
            elif len(value) == 4:
                min = int(value[-2:])
                hr = int(value[0:2])
            else:
                min = int(value)
                hr = 0

            tim = hr * 60 + min
            if tim >= 240:
                tim = tim - 240
            else:
                tim = tim + 1200
            return tim
        return int(value)

    def clear_line(self):
        self.csvname.setText("")

    def connects(self, configobject):

        #        protocol = 'postgres'
        #        user_name = 'postgres'
        #        password = 'Dyou65221'
        #        host_name = 'localhost'
        #        database_name = 'mag_zone'

        protocol = configobject.getConfigElement(DB_CONFIG, DB_PROTOCOL)
        user_name = configobject.getConfigElement(DB_CONFIG, DB_USER)
        password = configobject.getConfigElement(DB_CONFIG, DB_PASS)
        host_name = configobject.getConfigElement(DB_CONFIG, DB_HOST)
        database_name = configobject.getConfigElement(DB_CONFIG, DB_NAME)

        self.database_config_object = DataBaseConfiguration(
            protocol, user_name, password, host_name, database_name)
        self.new_obj = DataBaseConnection(self.database_config_object)
        self.new_obj.new_connection()

    def disconnects(self):
        self.new_obj.close_connection()

#        dialog = QFileDialog()
#        filename = dialog.getSaveFileName(None,"Save KML","","KML file (*.kml)")
#        self.kmlname = str(filename)
#
#        if self.kmlname.find(".kml") > -1:
#            self.new_obj = None
#            self.connects()
#            self.cursor = self.new_obj.cursor
#
#            self.create_kml()

#        coord = "-112.04756,33.50196,0 -112.04752,33.50922,0 -112.04752,33.50922,0 -112.04411,33.5092,0 -112.0335,33.5093,0 -112.0332,33.50924,0 -112.03012,33.50925,0 -112.03012,33.50925,0 -112.03017,33.51056,0 -112.03013,33.51099,0 -112.03011,33.51949,0 -112.02991,33.52121,0 -112.02991,33.5254,0 -112.02983,33.52663,0 -112.02957,33.52759,0 -112.02916,33.52839,0 -112.02836,33.52935,0 -112.02691,33.53053,0 -112.02691,33.53053,0 -112.02682,33.53051,0 -112.02599,33.53097,0 -112.02563,33.53101,0 -112.02514,33.53096,0 -112.02393,33.53051,0 -112.0233,33.53032,0 -112.01915,33.52939,0 -112.01847,33.52934,0 -112.01763,33.52942,0 -112.01673,33.52969,0 -112.01613,33.53,0 -112.01489,33.53106,0 -112.01454,33.53128,0 -112.01382,33.53164,0 -112.01293,33.53187,0 -112.01252,33.5319,0 -111.99518,33.53184,0 -111.97855,33.53109,0 -111.97583,33.53107,0 -111.97568,33.53101,0 -111.94428,33.53105,0 -111.92559,33.53141,0 -111.92559,33.53141,0 -111.92564,33.5387,0 -111.92564,33.5387,0 -111.92138,33.53864,0 -111.91841,33.53855,0 -111.91567,33.53831,0 -111.91487,33.5383,0 -111.91182,33.53854,0 -111.90951,33.53853,0 -111.90932,33.53846,0 -111.90002,33.53838,0 -111.89577,33.53837,0 -111.89557,33.53843,0 -111.89147,33.53842,0 -111.89147,33.53842,0 -111.89146,33.54453,0"
#        xy1 = coord.split(" ")
#        xy2 = []
#        for i in xy1:
#            temp = i.split(",")
#            xyz = []
#            if len(temp) == 3:
#                xyz.append(temp[0])
#                xyz.append(temp[1])
#                xyz.append(temp[2])
#                xy2.append(xyz)
#
#        self.distance_rate(xy2)

#        o = open('C:\Documents and Settings\dhyou\My Documents\SimTRAVEL\KML\dd.kml','r+')
#        numspace = self.makespace(len(str(o.readline())))
#        o.seek(0)
#        o.write(numspace)
#        o.close()
#
#        parser = etree.XMLParser(remove_blank_text=True)
#        self.kml = etree.parse('C:\Documents and Settings\dhyou\My Documents\SimTRAVEL\KML\dd.kml',parser)
#
#        xy1 = []
#        docuelt = self.kml
#        for comp in docuelt.getiterator('kml'):
#            for place in comp.getiterator('Placemark'):
#                for name in place.getiterator('name'):
#                    if name.text == "Route":
#
#                        for coord in place.getiterator("coordinates"):
#                            xy1 = str(coord.text).split(" ")
#
#
#        xy2 = []
#        for i in xy1:
#            temp = i.split(",")
#            xyz = []
#            if len(temp) == 3:
#                xyz.append(float(temp[0]))
#                xyz.append(float(temp[1]))
#                xyz.append(float(temp[2]))
#                xy2.append(xyz)
#
#        self.distance_rate(xy2)
#
#
#        self.kml.write('C:\Documents and Settings\dhyou\My Documents\SimTRAVEL\KML\dd.kml', pretty_print=True)
#        f = open("C:\Documents and Settings\dhyou\My Documents\SimTRAVEL\KML\dd.kml", "r+")
# old = f.read() # read everything in the file
# f.seek(0) # rewind
# f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + old) # write the new line before
#        f.close()


#    def kml_name(self, filename):
#        parse = ""
#        if filename.find("/"):
#            parse = "/"
#        else:
#            parse = "\\"
#        temp = filename.split(parse)
#        return temp[len(temp)-1]
#
#    def create_kml(self):
#        t1 = time.time()
# self.progresslabel.setText("Processing....")
# self.repaint()
#
#        filename = self.kmlname
#        try:
#
#            if filename.find(".kml") > -1:
#
#                self.fieldname = []
# NSMAP = {'gx' : XHTML_NAMESPACE} # the default namespace (no prefix)
#                xhtml = etree.Element("kml", nsmap=NSMAP)
#                docu = etree.SubElement(xhtml, "Document")
#                name = etree.SubElement(docu, "name")
#                name.text = str(self.kml_name(filename))
#
#                index = 1
#                for i in range(index):
#                    self.draw_line_poly(docu,i)
#
#                folder = etree.SubElement(docu,"Folder")
#                name_fold = etree.SubElement(folder,"name")
#                name_fold.text = "Analysis_Zones"
#
#                self.putschema(folder)
#                self.place_boundary(folder)
#
#                newkml = etree.ElementTree(xhtml)
#                newkml.write(filename,pretty_print=True)
#
#                f = open(filename,"r+")
# old = f.read() # read everything in the file
#                f.seek(0)
# f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + old) # write the new line before
#                f.close()
#
#
#            t2 = time.time()
#            print 'time taken is ---> %s'%(t2-t1)
#
#            QMessageBox.information(None, "",
#                            QString("""KML importing is successful"""),
#                            QMessageBox.Yes)
#
#        except Exception, e:
#            print '\tError while creating the KML file'
#            print e
#
#        self.disconnects()
# self.progresslabel.setText("")
# QDialog.accept(self)
#
#    def draw_line_poly(self,docu,i):
#        selcolor = self.choosecolor()
#        style = etree.SubElement(docu, "Style")
#        style.set("id", str(selcolor[0]))
#        line = etree.SubElement(style, "LineStyle")
#        col_line = etree.SubElement(line, "color")
#        col_line.text = str(selcolor[1])
#        width = etree.SubElement(line, "width")
#        width.text = '2'
#
#        poly = etree.SubElement(style,"PolyStyle")
#        fill = etree.SubElement(poly,"fill")
#        fill.text = "0"
#        col_poly = etree.SubElement(poly,"color")
#        col_poly.text = str(selcolor[1])
#
#
#    def putschema(self,folder):
#        schema = etree.SubElement(folder, "Schema")
#        schema.set("name","TAZs_Project_Feature")
#        schema.set("id","TAZs_Project_Feature")
#
#        SQL = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='shape_zone'"
#        self.cursor.execute(SQL)
#        temp = self.cursor.fetchall()
#
#        for i in temp:
#            name = str(i[0])
#            dtype = str(i[1])
#            etype = ""
#            if dtype.find("character") > -1:
#                etype = "string"
#            elif dtype.find("int") > -1:
#                etype = "int"
#            elif dtype.find("numeric") > -1 or dtype.find("double") > -1 or dtype.find("float") > -1:
#                etype = "float"
#
#            if etype <> "":
#                field = etree.SubElement(schema, "SimpleField")
#                field.set("name",name)
#                field.set("type",etype)
#                field.text = ""
#                self.fieldname.append(name)
#
#
#    def place_boundary(self,folder):
#        SQL = "SELECT AsKML(A.the_geom), A.* FROM shape_zone AS A"
#        self.cursor.execute(SQL)
#        tazdata = self.cursor.fetchall()
#
#        for i in tazdata:
#            place = etree.SubElement(folder,"Placemark")
#            name = etree.SubElement(place,"name")
#            name.text = " "
#
#            points = str(i[0])
#            points = points.replace("<MultiGeometry>","")
#            points = points.replace("</MultiGeometry>","")
#            points = points.replace("<Polygon>","")
#            points = points.replace("</Polygon>","")
#            points = points.replace("<outerBoundaryIs>","")
#            points = points.replace("</outerBoundaryIs>","")
#            points = points.replace("<LinearRing>","")
#            points = points.replace("</LinearRing>","")
#            points = points.replace("<coordinates>","")
#            points = points.replace("</coordinates>","")
#
#            style = etree.SubElement(place,"styleUrl")
# style.text = "#boundary"
#
#            extend = etree.SubElement(place,"ExtendedData")
#            schema = etree.SubElement(extend,"SchemaData")
# schema.set("schemaUrl","#TAZs_Project_Feature")
#
#            for j in range(len(self.fieldname)):
#                Simple = etree.SubElement(schema,"SimpleData")
#                Simple.set("name",str(self.fieldname[j]))
#                Simple.text = str(i[j+1])
#
#            poly = etree.SubElement(place,"Polygon")
#            outer = etree.SubElement(poly,"outerBoundaryIs")
#            linering = etree.SubElement(outer,"LinearRing")
#            coord = etree.SubElement(linering,"coordinates")
#
#            coords = "%s" %(points)
#            coord.text = coords
#
#
#    def choosecolor(self):
#        color = ["boundary"]
#        code = ["ff0000ff","d7701919","d7ed9564","d7eeff66","d7ffff00","d76030b0","d7ee687b","d70000ff",
#                "d70000b3","d7bfbfff","d78080ff","d74f4f2f","d7696969","d7bebebe","d70080ff","d7005ab3",
#                "d7006400","d700fc7c","d7000000","d78b3d48","d72f6b55","d732cd32","d76bb7bd","d7a09e5f",
#                "d700ffff","d700d7ff","d70b86b8","d70045ff","d7008cff","d79314ff","d78515c7","d7db7093",
#                "d7c9c9cd","d7b0c0cd","d7b7d5ee","d765778b","d7e0eeee","d7e0eef4","d7838b83","d7cd0000"]
#
#        i = 0
# i = random.randint(0,39)
#
#        choose = []
#        choose.append(color[0])
#        choose.append(code[i])
#        return choose


def main():
    app = QApplication(sys.argv)
    wizard = import_nhts()
    wizard.show()
    app.exec_()

if __name__ == "__main__":
    main()
