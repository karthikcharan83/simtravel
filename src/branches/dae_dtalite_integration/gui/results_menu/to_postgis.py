'''
Created on Jan 19, 2011

@author: dhyou
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from openamos.gui.env import *
from openamos.core.database_management.cursor_database_connection import *
from openamos.core.database_management.database_configuration import *

from openamos.gui.misc.basic_widgets import *
import sys,codecs,unicodedata,string 
from shapefile import *
#from pyproj import Proj, transform
from osgeo import osr
from copy import deepcopy


class Read_Shape(QDialog):
    '''
    classdocs
    '''
    def __init__(self, configobject = None, parent = None):
        QDialog.__init__(self, parent)
        
        self.new_obj = None
        self.connects(configobject)
        self.cursor = self.new_obj.cursor
        
        self.tablename = "shape_zone"
        self.setMinimumSize(QSize(400,160))
        self.setWindowTitle("Import Shapefile")
        
        pagelayout = QVBoxLayout()
        self.setLayout(pagelayout)
        
        dbinputbox = QGroupBox("")
        vbox = QVBoxLayout()
        dbinputbox.setLayout(vbox)
        
        shapenamelabel = QLabel("Select a shapefile")
        shapewidget = QWidget(self)
        shapelayout = QHBoxLayout()
        shapelayout.setContentsMargins(0,0,0,0)
        shapewidget.setLayout(shapelayout)
        
        self.shapename = LineEdit()
        shapelayout.addWidget(self.shapename)
        self.shapebutton = QPushButton('...')
        self.shapebutton.setMaximumWidth(30)
        shapelayout.addWidget(self.shapebutton)
        
        SIDlabel = QLabel("Enter EPSG code")
        self.epsg = LineEdit()
        self.epsg.setMaximumWidth(150)
        
        IDlabel = QLabel("Select ID")
        self.polyID = QComboBox()
        self.polyID.setMaximumWidth(250)
        
        vbox.addWidget(shapenamelabel)
        vbox.addWidget(shapewidget)
        vbox.addWidget(SIDlabel)
        vbox.addWidget(self.epsg)
        vbox.addWidget(IDlabel)
        vbox.addWidget(self.polyID)
        
        pagelayout.addWidget(dbinputbox)
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        pagelayout.addWidget(self.dialogButtonBox)

        self.connect(self.shapebutton, SIGNAL("clicked(bool)"), self.open_folder)
        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self.create_sql)
        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), self.disconnects)

    def get_EPSG(self,shppath):
        path = deepcopy(shppath)
        path = path[0:len(path)-3]
        path = path + "prj"
        prj_file = open(path,'r')
        prj_lines = prj_file.readlines()
        prj_file.close()
        
        for i in range(len(prj_lines)):
            prj_lines[i] = string.rstrip(prj_lines[i])
            
        prj = osr.SpatialReference()
        prj.ImportFromESRI(prj_lines)
        prj.from_esri = True        
        prj.AutoIdentifyEPSG()
        
        srid = ''
        if prj.IsGeographic():
            srid = str(prj.GetAuthorityCode('GEOGCS'))
        else:
            if prj.GetAuthorityCode('PROJCS') == None:
                srid = str(prj.GetAuthorityCode('GEOGCS'))
            else:
                srid = str(prj.GetAuthorityCode('PROJCS'))
        self.epsg.setText(srid)
        

    def open_folder(self):
        dialog = QFileDialog()
        temp = dialog.getOpenFileName(self,"Browse to select a project configuration file","","Shape File (*.shp)")
        self.shapename.setText(temp)
        self.get_EPSG(temp)
        sf = Reader(str(temp))
        for i in sf.fields:
            self.polyID.addItem(i[0])


    def create_sql(self):
        
        shpname = self.shapename.text()
        sid = self.epsg.text()
        pid = self.polyID.currentText()
        #self.tablename = self.table_name()
        
        if self.checkIfTableExists(self.tablename):
            self.cursor.execute("DROP TABLE %s" %(self.tablename))
            self.new_obj.connection.commit()
            
        if shpname != '' and sid != '' and pid != '':
            self.sqlname = shpname[0:len(shpname)-4] + '.sql'
            f = codecs.open(self.sqlname,'w',"utf-8")
            f.write(u'SET CLIENT_ENCODING TO UTF8;\n')
            f.write(u'SET STANDARD_CONFORMING_STRINGS TO ON;\n')
            f.write(u'BEGIN;\n')

            #sf = Reader("C:/mag_taz/Control_Points_Project.shp")
            sf = Reader(str(shpname))

            self.create_state(f,sf)
            self.select_state(f,sf)
            self.insert_state(f,sf)

            f.write(u'CREATE INDEX "%s_the_geom_gist" ON "%s" using gist ("the_geom");\n' %(self.tablename,self.tablename))
            f.write(u'COMMIT;\n')
            f.close()
            
            self.read_sql()
            QMessageBox.information(self, "",
                            QString("""Shapefile importing is successful!"""), 
                            QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "Import spatial information...",
                                        QString("""You should select shapefile and enter EPSG code."""), 
                                        QMessageBox.Yes)
        
        self.disconnects()
        QDialog.accept(self)

    def table_name(self):
        wholename = self.shapename.text()
        names = wholename.split('/')
        name = names[len(names)-1]
        name = str(name[0:len(name)-4]).lower()
        return name

    def create_state(self,f,sf):
        f.write(u'CREATE TABLE "%s" (gid serial PRIMARY KEY,\n' %(self.tablename))
        
        fields = sf.fields
        numfields = len(fields)
        
        for i in range(numfields):
            field = fields[i]
            Fname = field[0]
            if i == self.polyID.currentIndex():
                Fname = "locationid"
            Ftype = field[1]
            Flength = int(field[2])
            Dlength = int(field[3])
            
            type = ''
            if Ftype == 'C':
                type = 'varchar(%d)' %(Flength)
            elif Ftype == 'N':
                if Dlength > 0:
                    type = 'float8' 
                else:
                    if Flength <= 4:
                        type = 'smallint'
                    elif Flength <= 8:
                        type = 'integer'
                    else:
                        type = 'bigint'
            elif Ftype == 'F':
                type = 'numeric'
                
            if i > 0:
                if i <> numfields-1:
                    line = '"%s" %s,\n' %(Fname,type)
                    f.write(u'%s' %(line))
                else:
                    line = '"%s" %s);\n' %(Fname,type)
                    f.write(u'%s' %(line))


    def select_state(self,f,sf):
        sid = self.epsg.text()
        stype = sf.shapeType
        shapetype = ''
        
        if stype == 1:
            shapetype = 'POINT'
        elif stype == 3:
            shapetype = 'LINESTRING'
        elif stype == 5:
            shapetype = 'MULTIPOLYGON'
        elif stype == 23:
            shapetype = 'MULTILINESTRING'
        elif stype == 25:
            shapetype = 'MULTIPOLYGON'
        
        f.write(u"SELECT addgeometrycolumn('','%s','the_geom',%s,'%s',2,true);\n" %(self.tablename,sid,shapetype))


    def insert_state(self,f,sf):
        sid = self.epsg.text()
        fields = sf.fields
        numfields = len(fields)
        shapes = sf.shapes()
        records = sf.records()
        numshapes = len(shapes)
        
        columns = self.insert_first(sf)
        geom = ''
        for i in range(numshapes):
            value = " VALUES ("
            for j in range(numfields-1):
                temp = records[i][j]
                if temp <> '':
                    value = value + "'%s'," %(temp)
                else:
                    value = value + "NULL,"
            
            stype = sf.shapeType
            if stype == 1:
                geom = self.point_state(shapes,i,sid)
            elif stype == 3:
                geom = self.line_state(shapes,i,sid)
            elif stype == 5:
                geom = self.multipolygon_state(shapes,i,sid)
            elif stype == 25:
                geom = self.multipolygon_state(shapes,i,sid)

            geom = columns + value + geom
            f.write(u"%s" %(geom))


    def insert_first(self,sf):
        fields = sf.fields
        numfields = len(fields)
        columns = 'INSERT INTO "%s" (' %(self.tablename)
        for i in range(numfields-1):
            fname = str(fields[i+1][0])
            if i == self.polyID.currentIndex()-1:
                fname = "locationid"
            columns = columns + '"%s",' %(fname)
        columns = columns + 'the_geom)'        
        return columns


    def point_state(self,shapes,i,sid):
        x = shapes[i].points[0][0]
        y = shapes[i].points[0][1]
        geom = "st_geometryfromtext('POINT(%s %s)',%s));\n" %(x,y,sid)
        return geom

    def line_state(self,shapes,i,sid):
        numpoints = len(shapes[i].points)
        points = ''
        
        for j in range(numpoints):
            x = shapes[i].points[j][0]
            y = shapes[i].points[j][1]
            points = points + '%s %s,' %(x,y)
    
        points = points[0:len(points)-1]
        geom = "st_geometryfromtext('LINESTRING(%s)',%s));\n" %(points,sid)
        return geom

    def polygon_state(self,shapes,i,sid):
        numpoints = len(shapes[i].points)
        polys = ''
        
        for j in range(numpoints):
            x = shapes[i].points[j][0]
            y = shapes[i].points[j][1]
            polys = polys + '%s %s,' %(x,y)
    
        polys = polys[0:len(polys)-1]
        geom = "st_geometryfromtext('POLYGON((%s))',%s));\n" %(polys,sid)
        return geom


    def multipolygon_state(self,shapes,i,sid):
        numpoints = len(shapes[i].points)
        numparts = len(shapes[i].parts)
        
        polys = ''
        for j in range(numparts):
            poly = '('
            for k in range(numpoints):
                index = k + shapes[i].parts[j]

                x = shapes[i].points[index][0]
                y = shapes[i].points[index][1]
                poly = poly + '%s %s,' %(x,y)
            polys = polys + poly[0:len(poly)-1] + ')'

        geom = "st_geometryfromtext('MULTIPOLYGON((%s))',%s));\n" %(polys,sid)
        return geom
        
        
#    def creat_table(self):
#        
#        ssql = 'CREATE TABLE "test" (gid serial PRIMARY KEY,"objectid" int4,"taz" int4,"raz" int4,"mpa" varchar(2),"county" varchar(3),"tazacres" numeric,"istaz" numeric,"shape_area" numeric,"shape_len" numeric,"area" numeric,"perimeter" numeric,"p504_d00_" float8,"p504_d00_i" float8,"puma5" varchar(5),"name" varchar(90),"lsad" varchar(2),"lsad_trans" varchar(50))'
#        self.cursor.execute(ssql)
#        #self.new_obj.connection.commit()
#        ssql = "SELECT AddGeometryColumn('','test','the_geom','24047','MULTIPOLYGON',2)"
#        self.cursor.execute(ssql)
#        ssql = 'INSERT INTO "test" ("objectid","taz","raz","mpa","county","tazacres","istaz","shape_area","shape_len","area","perimeter","p504_d00_","p504_d00_i","puma5","name","lsad","lsad_trans",the_geom) VALUES' + "('1529','1531','312','GI','MC','182.04000000','1531.00000000','7929554.20458','11282.4135439','0.0167306207425','0.687472230512','27','26','00122','00122','P5',NULL,'0106000020EF5D0000010000000103000020EF5D00000100000010000000E04FF91E3A362741407413C0D57E2A41607BB47F2A362741C017B11F6A6A2A41A0898E8016332741C01645DF656A2A4140676CA0852F274140F65AA0656A2A41E0098680082C27410094BB9F5B6A2A41C00F91DF67232741402F475F496A2A41404CE5C0B7212741004ECBDF456A2A41607C859FC420274100FE787F446A2A41C0E8A41F991E2741404D5F9F416A2A41A01EC220751E274100DC7BDF007A2A4100D31940841E2741C0FA7FE0B27E2A41C068A2BF5C2627410002FC5ECB7E2A41A0F477DF3D272741C0B2153FCE7E2A4180AE2D9F713227410071D23FC97E2A41003EE69F2533274140F18980CB7E2A41E04FF91E3A362741407413C0D57E2A41');"
#        self.cursor.execute(ssql)
#        self.new_obj.connection.commit()


    def read_sql(self):
        #self.connects()
        
        text_file = open(self.sqlname, "r")
        create = '' 
        step = 0
        
        for line in text_file:
            temp = line[0:len(line)-1]
            if step == 0:
                if temp.find('CREATE',0,6) > -1:
                    create = temp
                    step = 1
                else:
                    self.cursor.execute(temp[0:len(temp)-1])
            elif step == 1:
                if temp[len(temp)-1] == ';':
                    create = create + temp[0:len(line)-2]
                    self.cursor.execute(create)
                    step = 2
                else:
                    create = create + temp
            elif step == 2:
                if temp.find('COMMIT') < 0:
                    self.cursor.execute(temp[0:len(temp)-1])
                else:
                    self.cursor.execute('COMMIT')
                    #self.new_obj.connection.commit()
       
        text_file.close()


    def checkIfTableExists(self, tablename):
        tables = self.tableList()
        try:
            tables.index(tablename)
        except:
            return False
        return True

    def tableList(self):
        tables = self.new_obj.get_table_list()
        return tables

    def connects(self,configobject):
        
#        protocol = 'postgres'        
#        user_name = 'postgres'
#        password = 'Dyou65221'
#        host_name = 'localhost'
#        database_name = 'mag_zone'
#        
#        self.database_config_object = DataBaseConfiguration(protocol, user_name, password, host_name, database_name)
#        self.new_obj = DataBaseConnection(self.database_config_object)
#        self.new_obj.new_connection()
        
        protocol = configobject.getConfigElement(DB_CONFIG,DB_PROTOCOL)        
        user_name = configobject.getConfigElement(DB_CONFIG,DB_USER)
        password = configobject.getConfigElement(DB_CONFIG,DB_PASS)
        host_name = configobject.getConfigElement(DB_CONFIG,DB_HOST)
        database_name = configobject.getConfigElement(DB_CONFIG,DB_NAME)
        
        self.database_config_object = DataBaseConfiguration(protocol, user_name, password, host_name, database_name)
        self.new_obj = DataBaseConnection(self.database_config_object)
        self.new_obj.new_connection()
        

    def disconnects(self):
        self.new_obj.close_connection()
        self.close()


def main():
    app = QApplication(sys.argv)
    wizard = Read_Shape()
    wizard.show()
    app.exec_()

if __name__=="__main__":
    main()
    


#def importSHP():
#    apppath = ''
#    savepath = 'C:/mag_taz'
#    host = 'localhost'
#    port = '5432'
#    username = 'postgres'
#    tablename = 'template_postgis'
#    path = ''

#
#    cmd = str('C:/Temp/psql.exe -U postgres -d template_postgis -h localhost -p 5432 -f C:/mag_taz/postgis.sql')
#    temp = os.popen(cmd, "w")
#    temp.write("hostname")
#
#    #os.system(cmd)
#
#        self.setWindowTitle("Database Configuration")
#        x,y = 968156.398100, 3706621.569993
#        p1 = Proj(proj="utm",zone=11,datum='NAD83')
#        p2 = Proj(init='epsg:4326')
#        x2, y2 = transform(p1,p2,x,y)
#        print '%f %f' %(x2, y2)
#
##C:\Program Files\PostgreSQL\8.3\bin\shp2pgsql.exe" -s 4326 -I countries.shp countries 
##| "C:\Program Files\PostgreSQL\8.3\bin\psql.exe" -d mapfish_workshop -U postgres
#
## -------------------------------------------------------
## Example calls
#if __name__ == '__main__':
#
#    importSHP()
    