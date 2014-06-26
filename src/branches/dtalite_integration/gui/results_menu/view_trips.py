'''
Created on Nov 9, 2010

@author: dhyou
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from core_plot import *
import numpy as np
import matplotlib.font_manager as plot


class MakePlot(Matplot):

    def __init__(self, config, table, parent=None):
        Matplot.__init__(self)
        self.valid = False
        self.connects(config)
        self.cursor = self.new_obj.cursor
        self.table = table

#        self.makeTempTables()
#        self.makecolumns()
#        self.cursor.execute('COMMIT')

        if self.isValid():
            self.valid = True
            if table.lower() == 'trips_full_r':
                self.setWindowTitle("Trip Characteristics")
            else:
                self.setWindowTitle("Activity Characteristics")
            # self.setWindowIcon(QIcon("./images/region.png"))
            aardWarning = QLabel("""<font color = blue>Note: The above chart shows the distribution of the """
                                 """Average Absolute Relative Difference (AARD)"""
                                 """ across all geographies for which a synthetic population was generated. """
                                 """ The AARD measure gives the average deviation of the person weighted sums """
                                 """with respect to composite person type constraints. """
                                 """The measure is used to monitor convergence in the Iterative Proportional Updating (IPU)"""
                                 """ algorithm of PopGen. </font>""")

            aardWarning.setWordWrap(True)
            self.fill_variable1(self.table)
            self.vbox.addWidget(self.addfilter)
            # self.vbox.addWidget(aardWarning)
            self.vbox.addWidget(self.canvas)
            self.vbox.addWidget(self.dialogButtonBox)
            self.vbox.setStretch(1, 1)
            self.setLayout(self.vbox)

            if self.table == "trips_full_r":
                self.xtitle = self.trip_labels(0)
                self.labelsdict = {}
                self.labelsdict['purpose_rec'] = self.trip_labels(1)
                self.labelsdict['tripmode'] = self.trip_labels(2)
                self.labelsdict['starttime'] = self.trip_labels(3)
                self.labelsdict['endtime'] = self.trip_labels(4)
                self.labelsdict['occupancy'] = self.trip_labels(5)
                self.labelsdict['duration'] = self.trip_labels(6)
                self.labelsdict['miles'] = self.trip_labels(7)
            else:
                self.xtitle = self.schedule_labels(0)
                self.labelsdict = {}
                self.labelsdict['activitytype'] = self.schedule_labels(1)
                self.labelsdict['starttime'] = self.schedule_labels(2)
                self.labelsdict['endtime'] = self.schedule_labels(3)
                self.labelsdict['duration'] = self.schedule_labels(4)

            self.connect(self.choicevar1, SIGNAL(
                "currentIndexChanged(int)"), self.manage_combo)  # self.on_draw1)
            # self.on_draw2new)
            self.connect(
                self.choicevar2, SIGNAL("currentIndexChanged(int)"), self.draw_plot)
            self.connect(
                self.selectvar2, SIGNAL("clicked(bool)"), self.dropVar2)

    def isValid(self):
        return self.checkIfTableExists(self.table)

    def manage_combo(self):
        index = self.choicevar1.currentIndex()
        self.choicevar2.clear()
        items = []
        for i in range(self.choicevar1.count()):
            if i <> index:
                item = self.choicevar1.itemText(i)
                items.append(item)
        self.choicevar2.addItems(items)

        if not self.selectvar2.isChecked() and int(self.choicevar1.currentIndex()) > 0:
            self.on_draw1()

    def draw_plot(self):
        if self.selectvar2.isChecked() and int(self.choicevar1.currentIndex()) > 0 and int(self.choicevar2.currentIndex()) > 0:
            self.on_draw2new()

    def on_draw1(self):
        """ Redraws the figure
        """
        # if not self.selectvar2.isChecked() and
        # int(self.choicevar1.currentIndex())>0:
        self.err1 = []
        self.err2 = []
        if self.retrieveResultsnew():
            # clear the axes and redraw the plot anew
            self.axes.clear()
            self.axes.grid(True)
            N = len(self.err1)
            ind = np.arange(N)

            #self.axes.hist(self.err, range=(1,10), normed=True, cumulative=False, histtype='bar', align='mid', orientation='vertical', log=False)
            #self.axes.hist(self.err, normed=False, align='left')
            self.axes.bar(ind, self.err2, color='green', align='center')
            self.axes.set_xlabel(
                self.xtitle[str(self.choicevar1.currentText())])
            self.axes.set_ylabel("Percent (%)")
            self.axes.set_ylim(0, 100)

            labelsdict = self.labelsdict[str(self.choicevar1.currentText())]
            labels = []
            for label in self.err1:
                temp = label
                if label in labelsdict.keys():
                    temp = labelsdict[label]
                labels.append(temp)

            self.axes.set_xticks(ind)
            if len(labels) >= 13:
                self.axes.set_xticklabels(labels, size='xx-small')
            elif (len(labels) >= 7):
                self.axes.set_xticklabels(labels, size='x-small')
            else:
                self.axes.set_xticklabels(labels)

            self.canvas.draw()

#        elif self.selectvar2.isChecked() and int(self.choicevar1.currentIndex())>0 and int(self.choicevar2.currentIndex()) > 0:
#            self.on_draw2new()

    def retrieveResults(self):

        #self.cursor = self.new_obj.cursor
        vars = self.choicevar1.currentText() + ", count(*)"
        tablename = ""
        if self.table == "trips_full_r":
            tablename = "temptrips"
        else:
            tablename = "tempschedule"
        filter = self.choicevar1.currentText() + " >= 0"
        group = self.choicevar1.currentText()
        order = self.choicevar1.currentText()

        try:
            total = 0.0
            retrieve = self.executeSelectQuery(
                self.cursor, vars, tablename, filter, group, order)
            for i in retrieve:
                self.err1.append(i[0])
                self.err2.append(i[1])
                total = total + i[1]

            for i in range(len(self.err1)):
                if total > 0:
                    self.err2[i] = 100 * float(self.err2[i]) / total
                else:
                    self.err2[i] = 0.0

            return True
        except Exception, e:
            print '\tError while fetching the columns from the table'
            print e

        return False

    def on_draw2(self):
        """ Redraws the figure
        """
        self.err1 = []
        self.err2 = []

        if self.x_axe_value():

            bound = self.boundvalue()
            bound.sort()

            self.axes.clear()
            self.axes.grid(True)
            N = len(self.err1)
            ind = np.arange(N)

            bars = []
            cumulate = []
            for j in range(len(self.err1)):
                cumulate.append(0)

            i = 0
            for var in bound:

                vars = "%s, count(*)" % (self.choicevar2.currentText())
                tablename = ""
                if self.table == "trips_full_r":
                    tablename = "temptrips"
                else:
                    tablename = "tempschedule"
                filter = "%s = %s and %s >= 0 and %s >= 0" % (self.choicevar1.currentText(), var,
                                                              self.choicevar1.currentText(), self.choicevar2.currentText())
                print filter
                group = self.choicevar2.currentText()
                order = self.choicevar2.currentText()

                value1 = []
                previous = []
                for j in range(len(self.err1)):
                    value1.append(0)
                    previous.append(cumulate[j])

                try:
                    retrieve = self.executeSelectQuery(
                        self.cursor, vars, tablename, filter, group, order)
                    for k in retrieve:
                        index = self.err1.index(k[0])
                        value1[index] = 100 * float(k[1]) / self.err2[index]
                        cumulate[index] = cumulate[index] + value1[index]

                except Exception, e:
                    print '\tError while fetching the columns from the table'
                    print e

                colors = self.colors(i)
                if i == 0:
                    temp = self.axes.bar(
                        ind, value1, color=colors, align='center')
                    bars.append(temp[0])
                else:
                    temp = self.axes.bar(
                        ind, value1, color=colors, align='center', bottom=previous)
                    bars.append(temp[0])
                i = i + 1

            prop = matplotlib.font_manager.FontProperties(size=8)

            labelsdict = self.labelsdict[str(self.choicevar2.currentText())]
            labels = []
            for label in self.err1:
                temp = label
                if label in labelsdict.keys():
                    temp = labelsdict[label]
                labels.append(temp)

            self.axes.set_xticks(ind)
            if len(labels) >= 13:
                self.axes.set_xticklabels(labels, size='xx-small')
            elif (len(labels) >= 7):
                self.axes.set_xticklabels(labels, size='x-small')
            else:
                self.axes.set_xticklabels(labels)

            legenddict = self.labelsdict[str(self.choicevar1.currentText())]
            legendlabel = []
            for label in bound:
                temp = label
                if label in legenddict.keys():
                    temp = legenddict[label]
                legendlabel.append(temp)

            self.axes.legend(bars, legendlabel, prop=prop, bbox_to_anchor=(
                1.01, 1), loc=2, borderaxespad=0.)
            self.axes.set_xlabel(
                self.xtitle[str(self.choicevar2.currentText())])
            self.axes.set_ylabel("Percent (%)")
            self.axes.set_ylim(0, 100)

            self.canvas.draw()

    def boundvalue(self):

        vars = self.choicevar1.currentText()
        tablename = ""
        if self.table == "trips_full_r":
            tablename = "temptrips"
        else:
            tablename = "tempschedule"
        filter = "%s >= 0" % (self.choicevar1.currentText())
        group = self.choicevar1.currentText()
        order = self.choicevar1.currentText()

        values = []
        try:
            retrieve = self.executeSelectQuery(
                self.cursor, vars, tablename, filter, group, order)
            for i in retrieve:
                values.append(i[0])
            return values

        except Exception, e:
            print '\tError while fetching the columns from the table'
            print e

        return values

    def x_axe_value(self):

        if str(self.choicevar1.currentIndex()) > 0 and str(self.choicevar2.currentIndex()) > 0:
            vars = "%s, count(*)" % (self.choicevar2.currentText())
            tablename = ""
            if self.table == "trips_full_r":
                tablename = "temptrips"
            else:
                tablename = "tempschedule"
            filter = "%s >= 0 and %s >= 0" % (
                self.choicevar1.currentText(), self.choicevar2.currentText())
            group = self.choicevar2.currentText()
            order = self.choicevar2.currentText()

            try:
                retrieve = self.executeSelectQuery(
                    self.cursor, vars, tablename, filter, group, order)
                for i in retrieve:
                    self.err1.append(i[0])
                    self.err2.append(i[1])

                return True

            except Exception, e:
                print '\tError while fetching the columns from the table'
                print e

            return False
        else:
            return False

    def retrieveResultsnew(self):

        tablename = self.table
        column = self.choicevar1.currentText()
        try:
            total = 0.0
            cond = self.time_categroy(column)
            for key in cond.keys():
                lowhigh = cond[key]
                sql = ""
                if len(lowhigh) > 1:
                    sql = "SELECT count(*) FROM %s WHERE %s >= %d AND %s < %d" % (
                        tablename, column, lowhigh[0], column, lowhigh[1])
                else:
                    sql = "SELECT count(*) FROM %s WHERE %s = %d" % (
                        tablename, column, lowhigh[0])

                self.cursor.execute(sql)
                data = self.cursor.fetchall()
                for j in data:
                    self.err1.append(key)
                    self.err2.append(j[0])
                    total = total + j[0]

            for i in range(len(self.err1)):
                self.err2[i] = 100 * float(self.err2[i]) / total

            return True
        except Exception, e:
            print '\tError while fetching the columns from the table'
            print e

        return False

    def time_categroy(self, column):
        time = {1: [0, 120], 2: [120, 300], 3: [300, 480],
                4: [480, 660], 5: [660, 900], 6: [900, 1440]}
        mode = {1: [1], 2: [2], 3: [3], 4: [4], 5: [5],
                6: [6], 7: [7], 8: [8], 9: [9], 10: [10], 11: [11]}
        duration = {1: [0, 11], 2: [11, 31], 3: [
            31, 121], 4: [121, 240], 5: [240, 1440]}
        miles = {1: [0, 6], 2: [6, 16], 3: [
            16, 31], 4: [31, 51], 5: [51, 30000]}
        occupancy = {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5, 30000]}
        activitytype = {100: [100], 101: [101], 200: [200], 300: [300], 411: [411], 412: [412],
                        415: [415], 416: [416], 513: [513], 514: [514], 900: [900], 600: [600], 601: [601]}

        if column == "starttime" or column == "endtime":
            return time
        elif column == "tripmode":
            return mode
        elif column == "duration":
            return duration
        elif column == "miles":
            return miles
        elif column == "occupancy":
            return occupancy
        elif column == "activitytype":
            return activitytype

    def on_draw2new(self):
        """ Redraws the figure
        """
        self.err1 = []
        self.err2 = []

        if self.x_axe_new():

            tablename = self.table
            category2 = self.time_categroy(self.choicevar1.currentText())

            self.axes.clear()
            self.axes.grid(True)
            N = len(self.err1)
            ind = np.arange(N)

            bars = []
            cumulate = []
            for j in range(len(self.err1)):
                cumulate.append(0)

            i = 0
            for key in category2.keys():
                lowhigh1 = category2[key]
                column1 = self.choicevar1.currentText()
                column2 = self.choicevar2.currentText()

                value1 = []
                previous = []
                for j in range(len(self.err1)):
                    value1.append(0)
                    previous.append(cumulate[j])

                try:
                    category1 = self.time_categroy(column2)
                    for k in category1.keys():

                        lowhigh2 = category1[k]
                        sql = ""
                        if len(lowhigh1) > 1 and len(lowhigh2) > 1:
                            sql = "SELECT count(*) FROM %s WHERE (%s >= %d AND %s < %d) AND %s >= %d AND %s < %d" % (
                                tablename, column1, lowhigh1[0], column1, lowhigh1[1], column2, lowhigh2[0], column2, lowhigh2[1])
                        elif len(lowhigh1) > 1 and len(lowhigh2) < 2:
                            sql = "SELECT count(*) FROM %s WHERE (%s >= %d AND %s < %d) AND %s = %d" % (
                                tablename, column1, lowhigh1[0], column1, lowhigh1[1], column2, lowhigh2[0])
                        elif len(lowhigh1) < 2 and len(lowhigh2) > 1:
                            sql = "SELECT count(*) FROM %s WHERE (%s = %d) AND %s >= %d AND %s < %d" % (
                                tablename, column1, lowhigh1[0], column2, lowhigh2[0], column2, lowhigh2[1])
                        else:
                            sql = "SELECT count(*) FROM %s WHERE %s = %d AND %s = %d" % (
                                tablename, column1, lowhigh1[0], column2, lowhigh2[0])

                        self.cursor.execute(sql)
                        data = self.cursor.fetchall()
                        for t in data:
                            index = self.err1.index(k)
                            if self.err2[index] <> 0:
                                value1[index] = 100 * \
                                    float(t[0]) / self.err2[index]
                                cumulate[index] = cumulate[
                                    index] + value1[index]
                            else:
                                value1[index] = 0

                except Exception, e:
                    print '\tError while fetching the columns from the table'
                    print e

                colors = self.colors(i)
                if i == 0:
                    temp = self.axes.bar(
                        ind, value1, color=colors, align='center')
                    bars.append(temp[0])
                else:
                    temp = self.axes.bar(
                        ind, value1, color=colors, align='center', bottom=previous)
                    bars.append(temp[0])
                i = i + 1

            prop = matplotlib.font_manager.FontProperties(size=8)

            labelsdict = self.labelsdict[str(self.choicevar2.currentText())]
            labels = []
            for label in self.err1:
                temp = label
                if label in labelsdict.keys():
                    temp = labelsdict[label]
                labels.append(temp)

            self.axes.set_xticks(ind)
            if len(labels) >= 13:
                self.axes.set_xticklabels(labels, size='xx-small')
            elif (len(labels) >= 7):
                self.axes.set_xticklabels(labels, size='x-small')
            else:
                self.axes.set_xticklabels(labels)

            legenddict = self.labelsdict[str(self.choicevar1.currentText())]
            legendlabel = []
            for label in category2:
                temp = label
                if label in legenddict.keys():
                    temp = legenddict[label]
                legendlabel.append(temp)

            self.axes.legend(bars, legendlabel, prop=prop, bbox_to_anchor=(
                1.01, 1), loc=2, borderaxespad=0.)
            self.axes.set_xlabel(
                self.xtitle[str(self.choicevar2.currentText())])
            self.axes.set_ylabel("Percent (%)")
            self.axes.set_ylim(0, 100)

            self.canvas.draw()

    def x_axe_new(self):

        if str(self.choicevar1.currentIndex()) > 0 and str(self.choicevar2.currentIndex()) > 0:

            tablename = self.table
            column1 = self.choicevar1.currentText()
            column2 = self.choicevar2.currentText()
            try:
                cond = self.time_categroy(column2)
                for key in cond.keys():
                    lowhigh = cond[key]
                    sql = ""
                    if len(lowhigh) > 1:
                        sql = "SELECT count(*) FROM %s WHERE %s >= %d AND %s < %d AND %s >= 0" % (
                            tablename, column2, lowhigh[0], column2, lowhigh[1], column1)
                    else:
                        sql = "SELECT count(*) FROM %s WHERE %s = %d AND %s >= 0" % (
                            tablename, column2, lowhigh[0], column1)

                    self.cursor.execute(sql)
                    data = self.cursor.fetchall()
                    for j in data:
                        self.err1.append(key)
                        self.err2.append(j[0])

                return True

            except Exception, e:
                print '\tError while fetching the columns from the table'
                print e

            return False
        else:
            return False

    def colors(self, index):
        colorpool = ['#0000FF', '#FFFF00', '#7B68EE', '#FF4500', '#1E90FF', '#F0E68C', '#87CEFA', '#FFFACD',
                     '#FFD700', '#4169E1', '#FFA500', '#6495ED', '#BDB76B', '#00BFFF', '#FF6347', '#B0E0E6',
                     '#ADFF2F', '#808080', '#32CD32', '#C0C0C0', '#00FA9A', '#DCDCDC', '#228B22', '#006400',
                     '#696969', '#00FF00', '#A9A9A9', '#98FB98', '#D3D3D3', '#3CB371']
        return colorpool[index]

    def trip_labels(self, index):

        xtitle = {'purpose_rec': 'Trip Purpose', 'starttime': 'Trip Start Time', 'endtime': 'Trip End Time',
                  'tripmode': 'Trip Mode', 'occupancy': 'Occupancy', 'duration': 'Trip Time (mins)', 'miles': 'Trip Length (miles)'}
        purposedict = {0: 'Return Home', 1: 'Work', 2: 'School', 3: 'Pers Buss', 4: 'Shopping', 5: 'Social Visit', 6: 'Sports/Rec', 7: 'Meal',
                       8: 'Serve Passgr', 9: 'Other'}
        modedict = {1: 'Car', 2: 'Van', 3: 'SUV', 4: 'Pickup Truck', 5: 'Bus', 6: 'Train', 7: 'School Bus', 8: 'Bike', 9: 'Walk',
                    10: 'Taxi', 11: 'Other'}
        strttime = {1: '4am-6am', 2: '6am-9am', 3: '9am-12pm',
                    4: '12pm-3pm', 5: '3pm-7pm', 6: 'after 7pm'}
        endtime = {1: '4am-6am', 2: '6am-9am', 3: '9am-12pm',
                   4: '12pm-3pm', 5: '3pm-7pm', 6: 'after 7pm'}
        occupancy = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5 or more'}
        duration = {
            1: '0-10', 2: '11-30', 3: '31-120', 4: '121-240', 5: '> 240'}
        miles = {1: '0-5', 2: '6-15', 3: '16-30', 4: '31-50', 5: '> 50'}

        if index == 0:
            return xtitle
        if index == 1:
            return purposedict
        if index == 2:
            return modedict
        if index == 3:
            return strttime
        if index == 4:
            return endtime
        if index == 5:
            return occupancy
        if index == 6:
            return duration
        if index == 7:
            return miles

    def schedule_labels(self, index):
        xtitle = {'activitytype': 'Activity Type', 'starttime': 'Start Time', 'endtime': 'End Time',
                  'duration': 'Activity Duration (mins)'}
        activitytype = {100: 'Home', 101: 'In-home', 200: 'Work', 300: 'School', 411: 'Pers Buss', 412: 'Shopping',
                        415: 'Meal', 416: 'Serve Passgr', 513: 'Social Visit', 514: 'Sports/Rec', 900: 'Other', 600: 'Pick-up', 601: 'Drop-off'}
        strttime = {1: '4am-6am', 2: '6am-9am', 3: '9am-12pm',
                    4: '12pm-3pm', 5: '3pm-7pm', 6: 'after 7pm'}
        endtime = {1: '4am-6am', 2: '6am-9am', 3: '9am-12pm',
                   4: '12pm-3pm', 5: '3pm-7pm', 6: 'after 7pm'}
        duration = {
            1: '0-10', 2: '11-30', 3: '31-120', 4: '121-240', 5: '> 240'}

        if index == 0:
            return xtitle
        if index == 1:
            return activitytype
        if index == 2:
            return strttime
        if index == 3:
            return endtime
        if index == 4:
            return duration

    def dropVar2(self):
        if not self.selectvar2.isChecked():
            self.choicevar2.setEnabled(False)
        else:
            self.choicevar2.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    diag = MakePlot('project')
    diag.show()
    # res.show()
    app.exec_()

if __name__ == "__main__":
    main()


#    def updatestrt(self, table_name):
#        self.cursor.execute("UPDATE %s SET strttime_rec = 1 WHERE starttime >= 0 AND starttime < 120"%(table_name))
#        self.cursor.execute("UPDATE %s SET strttime_rec = 2 WHERE starttime >= 120 AND starttime < 300"%(table_name))
#        self.cursor.execute("UPDATE %s SET strttime_rec = 3 WHERE starttime >= 300 AND starttime < 480"%(table_name))
#        self.cursor.execute("UPDATE %s SET strttime_rec = 4 WHERE starttime >= 480 AND starttime < 660"%(table_name))
#        self.cursor.execute("UPDATE %s SET strttime_rec = 5 WHERE starttime >= 660 AND starttime < 900"%(table_name))
#        self.cursor.execute("UPDATE %s SET strttime_rec = 6 WHERE starttime >= 900"%(table_name))
#
#    def updateend(self, table_name):
#        self.cursor.execute("UPDATE %s SET endtime_rec = 1 WHERE endtime >= 0 AND endtime < 120"%(table_name))
#        self.cursor.execute("UPDATE %s SET endtime_rec = 2 WHERE endtime >= 120 AND endtime < 300"%(table_name))
#        self.cursor.execute("UPDATE %s SET endtime_rec = 3 WHERE endtime >= 300 AND endtime < 480"%(table_name))
#        self.cursor.execute("UPDATE %s SET endtime_rec = 4 WHERE endtime >= 480 AND endtime < 660"%(table_name))
#        self.cursor.execute("UPDATE %s SET endtime_rec = 5 WHERE endtime >= 660 AND endtime < 900"%(table_name))
#        self.cursor.execute("UPDATE %s SET endtime_rec = 6 WHERE endtime >= 900"%(table_name))
#
#    def updateduration(self, table_name):
#        self.cursor.execute("UPDATE %s SET duration_rec = 1 WHERE duration >= 0 AND duration <= 10"%(table_name))
#        self.cursor.execute("UPDATE %s SET duration_rec = 2 WHERE duration >= 11 AND duration <= 30"%(table_name))
#        self.cursor.execute("UPDATE %s SET duration_rec = 3 WHERE duration >= 31 AND duration <= 120"%(table_name))
#        self.cursor.execute("UPDATE %s SET duration_rec = 4 WHERE duration >= 121 AND duration <= 240"%(table_name))
#        self.cursor.execute("UPDATE %s SET duration_rec = 5 WHERE duration > 240"%(table_name))
#
#    def updatemiles(self, table_name):
#        self.cursor.execute("UPDATE %s SET miles_rec = 1 WHERE miles >= 0 AND miles < 5"%(table_name))
#        self.cursor.execute("UPDATE %s SET miles_rec = 2 WHERE miles >= 5 AND miles < 15"%(table_name))
#        self.cursor.execute("UPDATE %s SET miles_rec = 3 WHERE miles >= 15 AND miles < 30"%(table_name))
#        self.cursor.execute("UPDATE %s SET miles_rec = 4 WHERE miles >= 30 AND miles < 50"%(table_name))
#        self.cursor.execute("UPDATE %s SET miles_rec = 5 WHERE miles >= 50"%(table_name))
#
#    def updateoccupancy(self, table_name):
#        self.cursor.execute("UPDATE %s SET occupancy_rec = 5 WHERE occupancy_rec >= 5"%(table_name))
#
#
#    def makecolumns(self):
#        try:
#            if self.table == "trips_r":
#
#                if not self.checkColumnExists("temptrips","strttime_rec"):
#                    self.cursor.execute("ALTER TABLE temptrips ADD COLUMN strttime_rec bigint")
#                    self.updatestrt("temptrips")
#                if not self.checkColumnExists("temptrips","endtime_rec"):
#                    self.cursor.execute("ALTER TABLE temptrips ADD COLUMN endtime_rec bigint")
#                    self.updateend("temptrips")
#
#            else:
#                if not self.checkColumnExists("tempschedule","activitytype"):
#                    self.cursor.execute("ALTER TABLE tempschedule ADD COLUMN activitytype bigint")
#                if not self.checkColumnExists("tempschedule","strttime_rec"):
#                    self.cursor.execute("ALTER TABLE tempschedule ADD COLUMN strttime_rec bigint")
#                    self.updatestrt("tempschedule")
#                if not self.checkColumnExists("tempschedule","endtime_rec"):
#                    self.cursor.execute("ALTER TABLE tempschedule ADD COLUMN endtime_rec bigint")
#                    self.updateend("tempschedule")
#                if not self.checkColumnExists("tempschedule","duration_rec"):
#                    self.cursor.execute("ALTER TABLE tempschedule ADD COLUMN duration_rec bigint")
#                    self.updateduration("tempschedule")
#
#        except Exception, e:
#            print '\tError while creating the table %s'%self.table_name
#            print e
#
#
#    def makeTempTables(self):
#        try:
#            if self.table == "trips_r":
#                if not self.checkIfTableExists("temptrips"):
#                    self.cursor.execute("CREATE TABLE temptrips AS SELECT *, tripmode as mode_rec FROM %s"%(self.table))
# self.cursor.execute("CREATE TABLE temptrips AS SELECT *, purpose as purpose_rec, mode as mode_rec, occupancy as occupancy_rec FROM %s"%(self.table))
#            else:
#                if not self.checkIfTableExists("tempschedule"):
#                    self.cursor.execute("CREATE TABLE tempschedule AS SELECT * FROM %s"%(self.table))
#
#        except Exception, e:
#            print '\tError while creating the table %s'%self.table_name
#            print e
