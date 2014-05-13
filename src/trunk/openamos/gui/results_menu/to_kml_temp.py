'''
Created on Mar 3, 2011

@author: dhyou
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from openamos.gui.env import *
from openamos.core.database_management.cursor_database_connection import *
from openamos.core.database_management.database_configuration import *

import zipfile,os
import sys,math,random,time
from lxml import etree
from copy import deepcopy
from datetime import date

#import codecs,unicodedata
#import re

XHTML_NAMESPACE = "http://www.google.com/kml/ext/2.2"

class Read_KML(): #QDialog):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
#        super(Read_KML, self).__init__(parent)
        '''
        Constructor
        '''
#        kmz_file = "C:\Documents and Settings\dhyou\Desktop\kkkk.kmz"
#        kml_file = "C:\Documents and Settings\dhyou\Desktop\ddd.kml"
#        fileObj = zipfile.ZipFile(kmz_file,'w')
#        fileObj.write(kml_file, os.path.basename( kml_file ) ,zipfile.ZIP_DEFLATED)
#        fileObj.close()

        dialog = QFileDialog()
        filename = dialog.getSaveFileName(None,"Save KML","","KML file (*.kml)")
        self.kmlname = str(filename)

        if self.kmlname.find(".kml") > -1:
            self.new_obj = None
            self.connects()
            self.cursor = self.new_obj.cursor

            self.create_kml()

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
#        old = f.read() # read everything in the file
#        f.seek(0) # rewind
#        f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + old) # write the new line before
#        f.close()


    def connects(self):
        protocol = 'postgres'
        user_name = 'postgres'
        password = 'Dyou65221'
        host_name = 'localhost'
        database_name = 'mag_zone'
#        protocol = self.configobject.getConfigElement(DB_CONFIG,DB_PROTOCOL)
#        user_name = self.configobject.getConfigElement(DB_CONFIG,DB_USER)
#        password = self.configobject.getConfigElement(DB_CONFIG,DB_PASS)
#        host_name = self.configobject.getConfigElement(DB_CONFIG,DB_HOST)
#        database_name = self.configobject.getConfigElement(DB_CONFIG,DB_NAME)

        self.database_config_object = DataBaseConfiguration(protocol, user_name, password, host_name, database_name)
        self.new_obj = DataBaseConnection(self.database_config_object)
        self.new_obj.new_connection()


    def disconnects(self):
        self.new_obj.close_connection()


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
#        self.progresslabel.setText("Processing....")
#        self.repaint()

        filename = self.kmlname
        try:

            if filename.find(".kml") > -1:

                self.fieldname = []
                NSMAP = {'gx' : XHTML_NAMESPACE} # the default namespace (no prefix)
                xhtml = etree.Element("kml", nsmap=NSMAP)
                docu = etree.SubElement(xhtml, "Document")
                name = etree.SubElement(docu, "name")
                name.text = str(self.kml_name(filename))

                index = 1
                for i in range(index):
                    self.draw_line_poly(docu,i)

                folder = etree.SubElement(docu,"Folder")
                name_fold = etree.SubElement(folder,"name")
                name_fold.text = "Analysis_Zones"

                self.putschema(folder)
                self.place_boundary(folder)

                newkml = etree.ElementTree(xhtml)
                newkml.write(filename,pretty_print=True)

                f = open(filename,"r+")
                old = f.read() # read everything in the file
                f.seek(0)
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + old) # write the new line before
                f.close()


            t2 = time.time()
            print 'time taken is ---> %s'%(t2-t1)

            QMessageBox.information(None, "",
                            QString("""KML importing is successful"""),
                            QMessageBox.Yes)

        except Exception, e:
            print '\tError while creating the KML file'
            print e

        self.disconnects()
#        self.progresslabel.setText("")
#        QDialog.accept(self)

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
        fill = etree.SubElement(poly,"fill")
        fill.text = "0"
        col_poly = etree.SubElement(poly,"color")
        col_poly.text = str(selcolor[1])


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
        SQL = "SELECT AsKML(A.the_geom), A.* FROM shape_zone AS A"
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
        color = ["boundary"]
        code = ["ff0000ff","d7701919","d7ed9564","d7eeff66","d7ffff00","d76030b0","d7ee687b","d70000ff",
                "d70000b3","d7bfbfff","d78080ff","d74f4f2f","d7696969","d7bebebe","d70080ff","d7005ab3",
                "d7006400","d700fc7c","d7000000","d78b3d48","d72f6b55","d732cd32","d76bb7bd","d7a09e5f",
                "d700ffff","d700d7ff","d70b86b8","d70045ff","d7008cff","d79314ff","d78515c7","d7db7093",
                "d7c9c9cd","d7b0c0cd","d7b7d5ee","d765778b","d7e0eeee","d7e0eef4","d7838b83","d7cd0000"]

        i = 0
        #i = random.randint(0,39)

        choose = []
        choose.append(color[0])
        choose.append(code[i])
        return choose


def main():
    app = QApplication(sys.argv)
    wizard = Read_KML()
#    wizard.show()
    app.exec_()

if __name__=="__main__":
    main()


#    def makespace(self, length):
#        temp = ""
#        for i in range(length-1):
#            temp = temp + " "
#        temp = temp + "\n"
#        return temp
#
#
#    def distance_rate(self, xy):
#        dists = []
#        begin = 100
#        end = 200
#        for i in range(len(xy)-1):
#            x1 = float(xy[i][0])
#            y1 = float(xy[i][1])
#            x2 = float(xy[i+1][0])
#            y2 = float(xy[i+1][1])
#            dist = self.distance(x1,y1,x2,y2)
#            dists.append(dist)
#
#        total = 0.0
#        for dist in dists:
#            total = total+dist
#
#        duration = end - begin
#        start = begin
#        for i in range(len(xy)-1):
#            finish = start + duration*dists[i]/total
#            x1 = float(xy[i][0])
#            y1 = float(xy[i][1])
#            x2 = float(xy[i+1][0])
#            y2 = float(xy[i+1][1])
#            self.inter_points2(x1,y1,x2,y2,start,finish)
#            start = finish
#
#
#    def distance(self,x1,y1,x2,y2):
#        dist = math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))
#        return dist
#
#    def inter_points2(self,x1,y1,x2,y2,begin,end):
#        num_points = int((end-begin)/2)
#        print num_points
#        if num_points<1:
#            num_points = 1
#
#        slope,b,distx,disty = 0.0,0.0,0.0,0.0
#        if x1 <> x2:
#            slope = (y2-y1)/(x2-x1)
#            b = y1 - slope * x1
#            distx = (x1 - x2)/num_points
#        else:
#            disty = (y1 - y2)/num_points
#
#        x = x1
#        y = y1
#        time = begin
#        #z = time*10
#
#        for i in range(num_points):
#            if slope <> 0.0:
#                y = slope * x + b
#
#            print '%f,%f,%d,%d' %(x,y,time,time+2)
#
##            print '            <Placemark>'
##            print '               <TimeSpan>'
##            print '                  <begin>%d</begin>' %(time)
##            print '                  <end>%d</end>' %(time+2) #distt)
##            print '               </TimeSpan>'
##            print '               <styleUrl>#osa_person</styleUrl>'
##            print '               <Point>'
##            print '                  <altitudeMode>relativeToGround</altitudeMode>'
##            print '                  <gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>'
##            print '                  <coordinates>%f,%f,10</coordinates>' %(x,y)
##            print '               </Point>'
##            print '            </Placemark>'
#
#            begin = begin+2
#            x = x - distx
#            y = y - disty
#            time = time + 2
#            #z = z + distt*10
