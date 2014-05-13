'''
Created on Mar 6, 2011

@author: dhyou
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from openamos.gui.env import *
from openamos.core.database_management.cursor_database_connection import *
from openamos.core.database_management.database_configuration import *
from openamos.gui.misc.basic_widgets import *

import sys,math,random,time
from lxml import etree
from copy import deepcopy
from datetime import date #datetime,

XHTML_NAMESPACE = "http://www.google.com/kml/ext/2.2"

class kml_trips(QDialog):
    '''
    classdocs
    '''

    def __init__(self, config, parent = None):
        QDialog.__init__(self, parent)
        '''
        Constructor
        '''
        self.configobject = config
        self.setMinimumSize(QSize(400,350))
        self.setWindowTitle("Save Travel or Activity Characteristics in KML")
        self.setWindowIcon(QIcon("./images/run.png"))

        pagelayout = QVBoxLayout()
        self.setLayout(pagelayout)

        segment = QGroupBox(self)
        addsegment = QHBoxLayout()
        segment.setLayout(addsegment)
        self.tripradio = QRadioButton("Travel Characteristics")
        self.tripradio.setChecked(True)
        self.actiradio = QRadioButton("Activity Characteristics")
        addsegment.addWidget(self.tripradio)
        addsegment.addWidget(self.actiradio)

        self.fromtobox = QGroupBox(self)
        addfromto = QHBoxLayout()
        self.fromtobox.setLayout(addfromto)
        self.fromradio = QRadioButton("Origin Zone")
        self.fromradio.setChecked(True)
        self.toradio = QRadioButton("Destination Zone")
        addfromto.addWidget(self.fromradio)
        addfromto.addWidget(self.toradio)

        dbinputbox = QGroupBox("")
        vbox = QVBoxLayout()
        dbinputbox.setLayout(vbox)

        filelabel = QLabel("Select Folder and Type KML name")
        kmlwidget = QWidget(self)
        kmllayout = QHBoxLayout()
        kmllayout.setContentsMargins(0,0,0,0)
        kmlwidget.setLayout(kmllayout)

        self.kmlname = LineEdit()
        self.kmlname.setDisabled(True)
        kmllayout.addWidget(self.kmlname)
        self.kmlbutton = QPushButton('...')
        self.kmlbutton.setMaximumWidth(30)
        kmllayout.addWidget(self.kmlbutton)

        activitylabel = QLabel("Select Activity Type")
        self.activitieswidget = QListWidget()
        self.activitieswidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.activitieswidget.setMaximumWidth(300)
        self.activitieswidget.setMaximumHeight(350)
        actives = self.activity()
        activities = []
        for i in actives.keys():
            active = "%s - %s" %(i,actives[i])
            activities.append(active)
        activities.sort()
        self.activitieswidget.addItems(activities)

        self.isAll = QCheckBox("Check to select all activities.")

        vbox.addWidget(self.fromtobox)
        vbox.addWidget(filelabel)
        vbox.addWidget(kmlwidget)
        vbox.addWidget(activitylabel)
        vbox.addWidget(self.activitieswidget)
        vbox.addWidget(self.isAll)

        progresswidget = QWidget(self)
        progresslayout = QHBoxLayout()
        progresswidget.setLayout(progresslayout)
        self.progresslabel = QLabel("")
        self.progresslabel.setMinimumWidth(150)
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        progresslayout.addWidget(self.progresslabel)
        progresslayout.addWidget(self.dialogButtonBox)
        progresslayout.setContentsMargins(0,0,0,0)

        pagelayout.addWidget(segment)
        pagelayout.addWidget(dbinputbox)
        pagelayout.addWidget(progresswidget)

        self.connect(self.kmlbutton, SIGNAL("clicked(bool)"), self.save_folder)
        self.connect(self.isAll, SIGNAL("stateChanged(int)"), self.selectAll)
        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self.create_kml)
        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), SLOT("reject()"))
        self.connect(self.tripradio, SIGNAL("clicked(bool)"), self.hide_radio)
        self.connect(self.actiradio, SIGNAL("clicked(bool)"), self.hide_radio)


    def connects(self):
#        protocol = 'postgres'
#        user_name = 'postgres'
#        password = 'Dyou65221'
#        host_name = 'localhost'
#        database_name = 'mag_zone'
        protocol = self.configobject.getConfigElement(DB_CONFIG,DB_PROTOCOL)
        user_name = self.configobject.getConfigElement(DB_CONFIG,DB_USER)
        password = self.configobject.getConfigElement(DB_CONFIG,DB_PASS)
        host_name = self.configobject.getConfigElement(DB_CONFIG,DB_HOST)
        database_name = self.configobject.getConfigElement(DB_CONFIG,DB_NAME)

        self.database_config_object = DataBaseConfiguration(protocol, user_name, password, host_name, database_name)
        self.new_obj = DataBaseConnection(self.database_config_object)
        self.new_obj.new_connection()

    def disconnects(self):
        self.new_obj.close_connection()


    def save_folder(self):
        dialog = QFileDialog()
        filename = dialog.getSaveFileName(self,"Save KML","","KML file (*.kml)")
        self.kmlname.setText(filename)


    def selectAll(self):
        if self.isAll.isChecked():
            for i in range(self.activitieswidget.count()):
                temp = self.activitieswidget.item(i)
                temp.setSelected(True)
        else:
            for i in range(self.activitieswidget.count()):
                temp = self.activitieswidget.item(i)
                temp.setSelected(False)


    def kml_name(self, filename):
        parse = ""
        if filename.find("/"):
            parse = "/"
        else:
            parse = "\\"
        temp = filename.split(parse)
        return temp[len(temp)-1]


    def create_kml(self):
        t1 = time.time()
        self.progresslabel.setText("Processing....")
        self.repaint()

        filename = str(self.kmlname.text())
        try:

            if filename.find(".kml") > -1:
                self.new_obj = None
                self.connects()
                self.cursor = self.new_obj.cursor

                self.fieldname = []
                NSMAP = {'gx' : XHTML_NAMESPACE} # the default namespace (no prefix)
                xhtml = etree.Element("kml", nsmap=NSMAP)
                docu = etree.SubElement(xhtml, "Document")
                name = etree.SubElement(docu, "name")
                name.text = str(self.kml_name(filename))
                self.overlay(docu)

                index = 1
                for i in range(index):
                    self.draw_line_poly(docu,i)

                folder1 = etree.SubElement(docu,"Folder")
                name_fold1 = etree.SubElement(folder1,"name")
                if self.tripradio.isChecked():
                    name_fold1.text = "Trip_Zones"
                else:
                    name_fold1.text = "Activity_Zones"
                self.putschema(folder1)
                self.place_boundary(folder1)

                folder2 = etree.SubElement(docu,"Folder")
                name_fold2 = etree.SubElement(folder2,"name")
                if self.tripradio.isChecked():
                    name_fold2.text = "Trip_Frequencies_Zones"
                else:
                    name_fold2.text = "Activity_Frequencies_Zones"

                self.table = ""
                self.zoneid = ""
                if self.tripradio.isChecked():
                    self.table = "trips_full_r"
                    if self.fromradio.isChecked():
                        self.zoneid = "fromzone"
                    else:
                        self.zoneid = "tozone"
                else:
                    self.table = "schedule_full_r"
                    self.zoneid = "locationid"

                for i in range(48):
                    start = i*30
                    end = i*30 + 30
                    self.place_icon(folder2,start,end)

                newkml = etree.ElementTree(xhtml)
                newkml.write(filename,pretty_print=True)

                f = open(filename,"r+")
                old = f.read() # read everything in the file
                f.seek(0)
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + old) # write the new line before
                f.close()


            t2 = time.time()
            print 'time taken is ---> %s'%(t2-t1)

            QMessageBox.information(self, "",
                            QString("""KML importing is successful"""),
                            QMessageBox.Yes)

        except Exception, e:
            print '\tError while creating the KML file'
            print e

        self.progresslabel.setText("")
        self.repaint()
        self.disconnects()
        QDialog.accept(self)


    def overlay(self,docu):
        figures = self.time_png()
        for i in range(24):
            begin = i*60
            end = begin+60
            soverlay = etree.SubElement(docu,"ScreenOverlay")
            name = etree.SubElement(soverlay,"name")
            name.text = ""
            timespan = etree.SubElement(soverlay,"TimeSpan")
            time_begin = etree.SubElement(timespan,"begin")
            time_begin.text = "%d"%(begin)
            time_end = etree.SubElement(timespan,"end")
            time_end.text = "%d"%(end)
            icon = etree.SubElement(soverlay,"Icon")
            href = etree.SubElement(icon,"href")
            href.text = str(figures[i])
            overxy = etree.SubElement(soverlay,"overlayXY")
            overxy.set("x","1")
            overxy.set("y","0.13")
            overxy.set("xunits","fraction")
            overxy.set("yunits","fraction")
            screenxy = etree.SubElement(soverlay,"screenXY")
            screenxy.set("x","1")
            screenxy.set("y","0.13")
            screenxy.set("xunits","fraction")
            screenxy.set("yunits","fraction")
            rotationxy = etree.SubElement(soverlay,"rotationXY")
            rotationxy.set("x","0")
            rotationxy.set("y","0")
            rotationxy.set("xunits","fraction")
            rotationxy.set("yunits","fraction")
            size = etree.SubElement(soverlay,"size")
            size.set("x","0")
            size.set("y","0")
            size.set("xunits","fraction")
            size.set("yunits","fraction")

    def time_png(self):
        path = str(os.getcwd())
        isFind = path.find("/")
        parse = ""
        if isFind > -1:
            parse = "/"
        else:
            parse = "\\"
        fig_path = ["%s%simages%s4am.jpg"%(path,parse,parse),
                    "%s%simages%s5am.jpg"%(path,parse,parse),
                    "%s%simages%s6am.jpg"%(path,parse,parse),
                    "%s%simages%s7am.jpg"%(path,parse,parse),
                    "%s%simages%s8am.jpg"%(path,parse,parse),
                    "%s%simages%s9am.jpg"%(path,parse,parse),
                    "%s%simages%s10am.jpg"%(path,parse,parse),
                    "%s%simages%s11am.jpg"%(path,parse,parse),
                    "%s%simages%s12pm.jpg"%(path,parse,parse),
                    "%s%simages%s1pm.jpg"%(path,parse,parse),
                    "%s%simages%s2pm.jpg"%(path,parse,parse),
                    "%s%simages%s3pm.jpg"%(path,parse,parse),
                    "%s%simages%s4pm.jpg"%(path,parse,parse),
                    "%s%simages%s5pm.jpg"%(path,parse,parse),
                    "%s%simages%s6pm.jpg"%(path,parse,parse),
                    "%s%simages%s7pm.jpg"%(path,parse,parse),
                    "%s%simages%s8pm.jpg"%(path,parse,parse),
                    "%s%simages%s9pm.jpg"%(path,parse,parse),
                    "%s%simages%s10pm.jpg"%(path,parse,parse),
                    "%s%simages%s11pm.jpg"%(path,parse,parse),
                    "%s%simages%s12am.jpg"%(path,parse,parse),
                    "%s%simages%s1am.jpg"%(path,parse,parse),
                    "%s%simages%s2am.jpg"%(path,parse,parse),
                    "%s%simages%s3am.jpg"%(path,parse,parse)]
        return fig_path

    def draw_line_poly(self,docu,i):
        selcolor = self.choosecolor()
        style = etree.SubElement(docu, "Style")
        style.set("id", str(selcolor[0]))
        line = etree.SubElement(style, "LineStyle")
        col_line = etree.SubElement(line, "color")
        col_line.text = str(selcolor[1])
        width = etree.SubElement(line, "width")
        width.text = '2'

        poly = etree.SubElement(style,"PolyStyle")
        col_poly = etree.SubElement(poly,"color")
        col_poly.text = str(selcolor[1])

        style = etree.SubElement(docu, "Style")
        style.set("id","boundary")
        line = etree.SubElement(style, "LineStyle")
        col_line = etree.SubElement(line, "color")
        col_line.text = str("ff0000ff")
        width = etree.SubElement(line, "width")
        width.text = '1'

        poly = etree.SubElement(style,"PolyStyle")
        fill = etree.SubElement(poly,"fill")
        fill.text = "0"
        col_poly = etree.SubElement(poly,"color")
        col_poly.text = str("ff0000ff")


    def place_icon(self,folder,start,end):
        condition = " AND ("
        activities = self.activitieswidget.selectedItems()
        for active in activities:
            activity = active.text()
            activity = activity[0:3]
            if self.tripradio.isChecked():
                condition = condition + "trippurpose = %s OR " %(activity)
            else:
                condition = condition + "activitytype = %s OR " %(activity)
        condition = condition[0:len(condition)-4] + ") "
        end1 = start + 1
        #SQL = "SELECT A.*, AsKML(ST_Centroid(B.the_geom)), B.* FROM (SELECT count(*), %s FROM %s WHERE ((starttime >= %d AND starttime < %d) OR (endtime >= %d AND endtime < %d) OR (starttime <= %d AND endtime >= %d))%sGROUP BY %s) AS A, shape_zone AS B WHERE A.%s = B.locationid" %(self.zoneid,self.table,start,end1,start,end1,start,end1,condition,self.zoneid,self.zoneid)
        SQL = "SELECT A.*, st_AsKML(text(ST_Centroid(text(B.the_geom)))), B.* FROM (SELECT count(*), %s FROM %s WHERE (starttime <= %d AND endtime >= %d)%sGROUP BY %s) AS A, shape_zone AS B WHERE A.%s = B.locationid" %(self.zoneid,self.table,start,end1,condition,self.zoneid,self.zoneid)
        #print SQL
        self.cursor.execute(SQL)
        tazdata = self.cursor.fetchall()
        if len(tazdata) <= 0:
            self.place_empty(folder,start,end)

        for i in tazdata:
            self.place_polygon(folder,i,start,end)


    def place_polygon(self,folder,i,start,endtime):
        place = etree.SubElement(folder,"Placemark")
        name = etree.SubElement(place,"name")
        name.text = " "

        timespan = etree.SubElement(place,"TimeSpan")
        begin = etree.SubElement(timespan,"begin")
        begin.text = str(start)
        end = etree.SubElement(timespan,"end")
        end.text = str(endtime)

        trips = int(i[0])
        points = str(i[2])
        points = points.replace("<Point>","")
        points = points.replace("</Point>","")
        points = points.replace("<coordinates>","")
        points = points.replace("</coordinates>","")


#        color = 1
#        isColor = True
#        max = self.max_trips
#        inter = max / 8
#        upper = max
#        lower = max - inter
#        while isColor:
#            color = color + 1
#            if upper >= trips and lower <= trips:
#                isColor = False
#            upper = upper - inter
#            lower = lower - inter

        style = etree.SubElement(place,"styleUrl")
        style.text = "#colors"


#        extend = etree.SubElement(place,"ExtendedData")
#        schema = etree.SubElement(extend,"SchemaData")
#        schema.set("schemaUrl","#TAZs_Project_Feature")
#
#        for j in range(len(self.fieldname)):
#            Simple = etree.SubElement(schema,"SimpleData")
#            Simple.set("name",str(self.fieldname[j]))
#            Simple.text = str(i[j+3])


        poly = etree.SubElement(place,"Polygon")
        extrude = etree.SubElement(poly,"extrude")
        extrude.text = "1"
        altitude = etree.SubElement(poly,"altitudeMode")
        altitude.text = "relativeToGround"
        outer = etree.SubElement(poly,"outerBoundaryIs")
        linering = etree.SubElement(outer,"LinearRing")

        coord = etree.SubElement(linering,"coordinates")
        xy = points.split(",")
        x = float(xy[0])
        y = float(xy[1])
        z = trips * 20

        coords = "%f,%f,%d " %(x-0.003,y-0.003,z)
        coords = coords + "%f,%f,%d " %(x+0.003,y-0.003,z)
        coords = coords + "%f,%f,%d " %(x+0.003,y+0.003,z)
        coords = coords + "%f,%f,%d " %(x-0.003,y+0.003,z)
        coords = coords + "%f,%f,%d" %(x-0.003,y-0.003,z)

        coord.text = coords

    def place_empty(self,folder,start,endtime):
        place = etree.SubElement(folder,"Placemark")
        name = etree.SubElement(place,"name")
        name.text = " "

        timespan = etree.SubElement(place,"TimeSpan")
        begin = etree.SubElement(timespan,"begin")
        begin.text = str(start)
        end = etree.SubElement(timespan,"end")
        end.text = str(endtime)

        style = etree.SubElement(place,"styleUrl")
        style.text = "#colors"

#        poly = etree.SubElement(place,"Polygon")
#        extrude = etree.SubElement(poly,"extrude")
#        extrude.text = "1"
#        altitude = etree.SubElement(poly,"altitudeMode")
#        altitude.text = "relativeToGround"
#        outer = etree.SubElement(poly,"outerBoundaryIs")
#        linering = etree.SubElement(outer,"LinearRing")
#        coord = etree.SubElement(linering,"coordinates")




    def origin_time(self,itime):
        hour = ""
        if itime<1200:
            temp = int(itime/60 + 4)
            if temp < 10:
                hour = "0%d" %(temp)
            else:
                hour = "%d" %(temp)
        else:
            temp = (itime - 1200)/60
            hour = "%d" %(temp)

        otime = "%sT%s:00:00Z" %(date.today(),hour)
        return otime


    def putschema(self,folder):
        schema = etree.SubElement(folder, "Schema")
        schema.set("name","TAZs_Project_Feature")
        schema.set("id","TAZs_Project_Feature")

        SQL = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='shape_zone'"
        self.cursor.execute(SQL)
        temp = self.cursor.fetchall()

        for i in temp:
            name = str(i[0])
            dtype = str(i[1])
            etype = ""
            if dtype.find("character") > -1:
                etype = "string"
            elif dtype.find("int") > -1:
                etype = "int"
            elif dtype.find("numeric") > -1 or dtype.find("double") > -1 or dtype.find("float") > -1:
                etype = "float"

            if etype <> "":
                field = etree.SubElement(schema, "SimpleField")
                field.set("name",name)
                field.set("type",etype)
                field.text = ""
                self.fieldname.append(name)


    def place_boundary(self,folder):
        SQL = "SELECT st_AsKML(text(A.the_geom)), A.* FROM shape_zone AS A"
        self.cursor.execute(SQL)
        tazdata = self.cursor.fetchall()

        for i in tazdata:
            place = etree.SubElement(folder,"Placemark")
            name = etree.SubElement(place,"name")
            name.text = " "

            points = str(i[0])
            points = points.replace("<MultiGeometry>","")
            points = points.replace("</MultiGeometry>","")
            points = points.replace("<Polygon>","")
            points = points.replace("</Polygon>","")
            points = points.replace("<outerBoundaryIs>","")
            points = points.replace("</outerBoundaryIs>","")
            points = points.replace("<LinearRing>","")
            points = points.replace("</LinearRing>","")
            points = points.replace("<coordinates>","")
            points = points.replace("</coordinates>","")

            style = etree.SubElement(place,"styleUrl")
            style.text = "#boundary"

            extend = etree.SubElement(place,"ExtendedData")
            schema = etree.SubElement(extend,"SchemaData")
            schema.set("schemaUrl","#TAZs_Project_Feature")

            for j in range(len(self.fieldname)):
                Simple = etree.SubElement(schema,"SimpleData")
                Simple.set("name",str(self.fieldname[j]))
                Simple.text = str(i[j+1])

            poly = etree.SubElement(place,"Polygon")
            outer = etree.SubElement(poly,"outerBoundaryIs")
            linering = etree.SubElement(outer,"LinearRing")
            coord = etree.SubElement(linering,"coordinates")

            coords = "%s" %(points)
            coord.text = coords


    def choosecolor(self):
        color = ["colors"]
        code = ["d7701919","d7ed9564","d7eeff66","d7ffff00","d76030b0","d7ee687b","d70000ff","d70000b3",
                "d7bfbfff","d78080ff","d74f4f2f","d7696969","d7bebebe","d70080ff","d7005ab3",
                "d7006400","d700fc7c","d7000000","d78b3d48","d72f6b55","d732cd32","d76bb7bd","d7a09e5f",
                "d700ffff","d700d7ff","d70b86b8","d70045ff","d7008cff","d79314ff","d78515c7","d7db7093",
                "d7c9c9cd","d7b0c0cd","d7b7d5ee","d765778b","d7e0eeee","d7e0eef4","d7838b83","d7cd0000"]

        i = 0
        if len(self.activitieswidget.selectedItems()) > 1:
            i = random.randint(0,38)
        else:
            i = self.activitieswidget.selectedIndexes()[0].row()

        choose = []
        choose.append(color[0])
        choose.append(code[i])
        return choose



    def activity(self):
        activitytype = {100:'IH-Sojourn',101:'IH',150:'IH-Dependent Sojourn', 151:'IH-Dependent',
            200:'OH-Work',201:'Work',
            300:'OH-School',301:'School',
            411:'OH-Pers Buss',412:'OH-Shopping',415:'OH-Meal',416:'OH-Serve Passgr',
            461:'OH-Dependent Pers Buss',462:'OH-Dependent Shopping',465:'OH-Dependent Meal',466:'OH-Dependent Serve Passgr',
            513:'OH-Social Visit',514:'OH-Sports/Rec',
            600:'Pick Up',601:'Drop Off',
            900:'OH-Other'}

        return activitytype



    def hide_radio(self):
        if self.tripradio.isChecked():
            self.fromtobox.setVisible(True)
        else:
            self.fromtobox.setVisible(False)



################################################################################################
#######  It is to fix kml file using lxml library. #############################################
################################################################################################
#        o = open('C:\Documents and Settings\dhyou\My Documents\SimTRAVEL\KML\dd.kml','r+')
#        numspace = self.makespace(len(str(o.readline())))
#        o.seek(0)
#        o.write(numspace)
#        o.close()
#
#
#        parser = etree.XMLParser(remove_blank_text=True)
#        self.kml = etree.parse('C:\Documents and Settings\dhyou\My Documents\SimTRAVEL\KML\dd.kml',parser)
#
#
#        docuelt = self.kml
#        for comp in docuelt.getiterator('kml'):
#            print comp.nsmap
#
#
#        for comp in docuelt.getiterator('Style'):
#            print comp.get("id")
#            if str(comp.get("id")) == "sn_noicon":
#                comp.set("id", str("noicon"))
#
#        self.kml.write('C:\Documents and Settings\dhyou\My Documents\SimTRAVEL\KML\dd.kml', pretty_print=True)
#
#
#        f = open("C:\Documents and Settings\dhyou\My Documents\SimTRAVEL\KML\dd.kml", "r+")
#        old = f.read() # read everything in the file
#        f.seek(0) # rewind
#        f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + old) # write the new line before
#        f.close()
#
#
#    def makespace(self, length):
#        temp = ""
#        for i in range(length-1):
#            temp = temp + " "
#        temp = temp + "\n"
#        return temp
################################################################################################
################################################################################################
################################################################################################





def main():
    app = QApplication(sys.argv)
    wizard = kml_trips()
    wizard.show()
    app.exec_()

if __name__=="__main__":
    main()



#    def chooseicon(self,i):
#        iconnames = ["site-home","site-work","site-school","site-business","site-shop",
#                     "site-meal","site-social","site-sport","site-other","site-pickup",
#                     "site-dropoff"]
#        iconaddr = ["C:/Documents and Settings/dhyou/My Documents/SimTRAVEL/KML/09_02_osa_icons_png/osa_home.png",
#                    "C:/Documents and Settings/dhyou/My Documents/SimTRAVEL/KML/09_02_osa_icons_png/osa_site-head-office.png",
#                    "C:/Documents and Settings/dhyou/My Documents/SimTRAVEL/KML/09_02_osa_icons_png/osa_site-branch.png",
#                    "C:/Documents and Settings/dhyou/My Documents/SimTRAVEL/KML/09_02_osa_icons_png/osa_mobile_pda.png",
#                    "http://maps.google.com/mapfiles/kml/shapes/grocery.png",
#                    "http://maps.google.com/mapfiles/kml/shapes/dining.png",
#                    "C:/Documents and Settings/dhyou/My Documents/SimTRAVEL/KML/09_02_osa_icons_png/osa_user_large_group.png",
#                    "http://maps.google.com/mapfiles/kml/shapes/play.png",
#                    "http://maps.google.com/mapfiles/kml/shapes/donut.png",
#                    "C:/Documents and Settings/dhyou/My Documents/SimTRAVEL/KML/09_02_osa_icons_png/osa_arrow_green_left.png",
#                    "C:/Documents and Settings/dhyou/My Documents/SimTRAVEL/KML/09_02_osa_icons_png/osa_arrow_yellow_right.png"]
#
#
#        choose = []
#        choose.append(iconnames[i])
#        choose.append(iconaddr[i])
#
#        return choose


#    def place_line(self,folder,tazdata):
#        place = etree.SubElement(folder,"Placemark")
#        name = etree.SubElement(place,"name")
#        name.text = "Absolute Extruded"
#        descript = etree.SubElement(place,"description")
#        descript.text = "HouseID:14787 PersonID:1"
#        style = etree.SubElement(place,"styleUrl")
#        style.text = "#yellowLine"
#
#        line = etree.SubElement(place,"LineString")
#        tessel = etree.SubElement(line,"tessellate")
#        tessel.text = "1"
#        altitude = etree.SubElement(line,"altitudeMode")
#        altitude.text = "relativeToGround"
#
#        coord = etree.SubElement(line,"coordinates")
#
#        coordinates = ""
#        for i in range(len(tazdata)-1):
#            stay = tazdata[i][4] + "," + tazdata[i][5] + ",0 "
#            move = tazdata[i+1][4] + "," + tazdata[i+1][5] + ",0 "
#            coordinates = coordinates + stay + move
#
#        coord.text = coordinates
