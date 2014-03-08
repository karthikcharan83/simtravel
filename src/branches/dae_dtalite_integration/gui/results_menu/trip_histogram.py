'''
Created on Nov 9, 2010

@author: dhyou
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from core_plot import *


class Absreldiff(Matplot):
    def __init__(self, project, parent=None):
        Matplot.__init__(self)
        self.project = project
        self.connects()
        self.valid = False
        if self.isValid():
            self.valid = True
            self.setWindowTitle("Average Absolute Relative Difference Distribution")
            self.setWindowIcon(QIcon("./images/region.png"))
            aardWarning = QLabel("""<font color = blue>Note: The above chart shows the distribution of the """
                                 """Average Absolute Relative Difference (AARD)"""
                                 """ across all geographies for which a synthetic population was generated. """
                                 """ The AARD measure gives the average deviation of the person weighted sums """
                                 """with respect to composite person type constraints. """
                                 """The measure is used to monitor convergence in the Iterative Proportional Updating (IPU)"""
                                 """ algorithm of PopGen. </font>""")

            aardWarning.setWordWrap(True)
            self.vbox.addWidget(self.canvas)
            self.vbox.addWidget(aardWarning)
            self.vbox.addWidget(self.dialogButtonBox)
            self.setLayout(self.vbox)
            self.on_draw()
        else:
            QMessageBox.warning(self, "Results", "A table with name - performance_statistics does not exist.", QMessageBox.Ok)

    def isValid(self):
        return self.checkIfTableExists("schedule_full_r")

    def on_draw(self):
        """ Redraws the figure
        """
        self.err1 = []
        self.err2 = []
        if self.retrieveResults():

            # clear the axes and redraw the plot anew
            self.axes.clear()
            self.axes.grid(True)

            #self.axes.hist(self.err, range=(1,10), normed=True, cumulative=False, histtype='bar', align='mid', orientation='vertical', log=False)
            #self.axes.hist(self.err, normed=False, align='left')
            self.axes.bar(self.err1, self.err2, align='center', width=10, color='b')
            self.axes.set_xlabel("Activity Type")
            self.axes.set_ylabel("Average Activity Duration")
            self.canvas.draw()



    def retrieveResults(self):
#        scenarioDatabase = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)
#        projectDBC = createDBC(self.project.db, scenarioDatabase)
#        projectDBC.dbc.open()
    
        cursor = self.new_obj.cursor
        vars = "activitytype, avg(duration)"
        tablename = "schedule_full_r"
        filter = ""
        group = "activitytype"
        
        try:
            retrieve = self.executeSelectQuery(cursor, vars, tablename, filter, group)
            #cursor.execute("select actcat, count(*) from trips group by actcat")
            for i in retrieve:
                self.err1.append(i[0])
                self.err2.append(i[1])

            return True
        except Exception, e:
            print '\tError while fetching the columns from the table'
            print e
            
        return False
    
    


def main():
    app = QApplication(sys.argv)
    diag = Absreldiff('project')
    diag.show()
    #res.show()
    app.exec_()

if __name__ == "__main__":
    main()