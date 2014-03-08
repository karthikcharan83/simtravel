#main class. this class will be used to define the database connection.
#it will create/drop database, schema and tables
 

#include all the import 
import sys
import os
import time
import exceptions
import sqlalchemy
import sqlite3
import psycopg2 as dbapi2
import sqlalchemy.schema
from numpy import ma, array
from psycopg2 import extensions
from sqlalchemy.sql import select
from sqlalchemy.schema import MetaData, Column, Table
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import class_mapper
from sqlalchemy import schema, types
from sqlalchemy.types import Integer, SmallInteger, \
			     Numeric, Float, \
			     VARCHAR, String, CLOB, Text,\
			     Boolean, DateTime

from database_configuration import DataBaseConfiguration
from database_connection import DataBaseConnection
from database_configuration import DataBaseConfiguration

from openamos.core.errors import DatabaseConfigurationError
from openamos.core.data_array import DataArray

class VECHICLE(object): pass

class LINKS(object): pass

class LINK_OD(object): pass

class SCHEDULE(object): pass

class TSP(object): pass

class DESTINATION_OPPORTUNITIES(object): pass

class HOUSEHOLDS(object): pass

class PERSONS(object): pass

class PERSON_SCHEDULE(object): pass

class TRIP(object): pass

class PERSON_TRIP(object): pass

class OFFICE(object): pass
 
class TEMP(object): pass

class SCHOOL(object): pass

# Run time tables empty class objects
class PERSONS_R(object): pass

class HOUSEHOLDS_R(object):pass

class VEHICLES_R(object):pass

class TSP_R(object):pass

class SCHEDULE_R(object):pass

class TRAVEL_SKIMS(object):pass

class QueryBrowser(object):
    
    ########## initialization ##########
    #initialize the class 
    def __init__(self, dbconfig):

        if not isinstance(dbconfig, DataBaseConfiguration):
            raise DatabaseConfigurationError, """The dbconfig input is not a valid """\
                """DataBaseConfiguration object."""

        self.protocol = dbconfig.protocol
        self.user_name = dbconfig.user_name
        self.password = dbconfig.password
        self.host_name = dbconfig.host_name
        self.database_name = dbconfig.database_name
        self.database_config_object = dbconfig
        """
        self.engine = None
        self.connection = None
        self.result = None
        self.query = None
        self.metadata = None
        self.table_name = None
        self.session = None
        self.class_name = None
        self.database_config_object = None
        """
        self.dbcon_obj = DataBaseConnection(dbconfig)
        print self.dbcon_obj
    
    ########## initialization ends ##########

    ########## methods for mapping ##########
    
    #separate function for mapper
    def table_mapper(self, class_name, table_name):
        """
        This method is used to create a mapper to the table in the database
        
        Input:
        Class name and Table name
        
        Output:
        Creates a table mapper object
        """
        
        #before creating the mapper check if the table exists
        self.table_name = table_name
        self.class_name = class_name
        table_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if table_flag:
            #table exists
            try:
                #print 'table name is %s and class name is %s'%(table_name, class_name)
                #load the table
                new_table = Table(self.table_name, self.dbcon_obj.metadata, autoload=True)
                
                #create mapper
                class_name = class_name.upper()                
                mapper(eval(class_name), new_table)

                #create an object for the mapper
                self.temp_object = eval(class_name)()
                
                #print the session and mapper object
                #print 'the session object is %s and the mapper object is %s\n'%(self.dbcon_obj.session, self.temp_object)
                return self.temp_object
            except Exception, e:
                print 'Failed to create mapper'
                print e
                #raise Exception                                
        else:
            print 'Table - %s does not exist in the database. Cannot create a mapper' %(table_name)
            return None


    #create mapper for all the classes
    def create_mapper_for_all_classes(self):
        """
        This method is used to create mapper objects for all the classes/tables
        This method calls the table_mapper method to map a table to a class
        
        Input:
        None
        
        Output:
        Mapper objects for all classes        
        """
        
        #print 'map all the classes'
        """
        #for class Vechile
        class_name = 'VECHICLE'
        table_name = 'vehicle'
        self.vehicle = self.table_mapper(class_name, table_name)
                
        #for class Links
        class_name = 'LINKS'
        table_name = 'links'
        self.links = self.table_mapper(class_name, table_name)

        #for class Link_OD
        class_name = 'LINK_OD'
        table_name = 'link_od'
        self.link_od = self.table_mapper(class_name, table_name)
        
        
        #for class Destination_Opportunities
        class_name = 'DESTINATION_OPPORTUNITIES'
        table_name = 'destination_opportunities'
        self.destination_opportunities = self.table_mapper(class_name, table_name)
        
        #for class Person_Schedule
        class_name = 'PERSON_SCHEDULE'
        table_name = 'person_schedule'
        self.person_schedule = self.table_mapper(class_name, table_name)

        #for class Trip
        class_name = 'TRIP'
        table_name = 'trip'
        self.trip = self.table_mapper(class_name, table_name)
        
        #for class Person_Trip
        class_name = 'PERSON_TRIP'
        table_name = 'person_trip'
        self.person_trip = self.table_mapper(class_name, table_name)
        
        #for class Office
        class_name = 'OFFICE'
        table_name = 'office'
        self.office = self.table_mapper(class_name, table_name)

        #for class School
        class_name = 'SCHOOL'
        table_name = 'school'
        self.school = self.table_mapper(class_name, table_name)


        """

        #for travel skims
        class_name = 'TRAVEL_SKIMS'
        table_name = 'travel_skims'
        self.table_mapper(class_name, table_name)

        #for class Household
        class_name = 'HOUSEHOLDS'
        table_name = 'households'
        self.table_mapper(class_name, table_name)

        #for class Person
        class_name = 'PERSONS'
        table_name = 'persons'
        self.table_mapper(class_name, table_name)
        
        # RUNTIME TABLES FOLLOW HERE
        class_name = 'PERSONS_R'
        table_name = 'persons_r'
        self.table_mapper(class_name, table_name)

        class_name = 'HOUSEHOLDS_R'
        table_name = 'households_r'
        self.table_mapper(class_name, table_name)

        class_name = 'VEHICLES_R'
        table_name = 'vehicles_r'
        self.table_mapper(class_name, table_name)        

        #for class TSP
        class_name = 'TSP_R'
        table_name = 'tsp_r'
        self.table_mapper(class_name, table_name)
        
        #for class Schedule
        class_name = 'SCHEDULE_R'
        table_name = 'schedule_r'
        self.table_mapper(class_name, table_name)


    ########## methods for mapping end ##########


    ########## methods for select query ##########
    
    #select all rows from the table
    def select_all_from_table(self, class_name):
        """
        This method is used to fetch all rows from the table specified.

        Input:
        Class name corresponding to the table

        Output:
        Returns all the rows in the table
        """
        self.dbcon_obj.new_sessionInstance()                
        #get the column list for the table
        new_class_name = class_name.upper()
        new_table_name = new_class_name.lower()
        
        col = []
        temp_table = Table(new_table_name, self.dbcon_obj.metadata, autoload=True)
        for cl in temp_table.c:
            col.append(cl)

        #query the table to fetch all the records by passing the columns
        query = self.dbcon_obj.session.query(eval(new_class_name)).values(*col)
        cols_list = [str(cl.name) for cl in col]
        """
        all_rows = []
        for instance in query:
            print instance
            all_rows.append(instance)

        print ' '
        """
        #print 'sample_str is %s'%sample_str                
        
        resultArray = self.createResultArray(query)
            
        # Returns the query as a DataArray object
        data = DataArray(resultArray, cols_list)

        self.dbcon_obj.close_sessionInstance()        

        return data


    #select rows based on a selection criteria
    def fetch_selected_rows(self, class_name, column_name, value):
        """
        This method is used to fetch selected rows fom the table in the database.

        Input:
        Database configuration object, class name and selection criteria.

        Output:
        Returns the rows that satisfy the selection criteria
        """
        
        #get the column list for the table
        new_class_name = class_name.upper()
        new_table_name = new_class_name.lower()
        
        col = []
        temp_table = Table(new_table_name, self.dbcon_obj.metadata, autoload=True)
        #print 'table object is %s'%temp_table
        for cl in temp_table.c:
            col.append(cl)

        try:
            query = self.dbcon_obj.session.query(eval(new_class_name))\
                .filter(getattr((eval(new_class_name)), column_name) == value).values(*col)
            """
            row_list = []
            counter = 0
            for each in query:
                counter = counter + 1
                row_list.append(each)
                
            if counter == 0:
                print 'No rows selected.\n'
            else:
                for each_ins in row_list:
                    print each_ins            
            print 'Select query successful.\n'
            """
            return query, col            
        except:
            print 'Error retrieving the information. Query failed.\n'


    #select and print the join
    def select_join(self, db_dict, column_names, table_names, max_dict=None, 
                    spatialConst_list=None, analysisInterval=None, subsample=None):
        """
        self, table1_list, table2_list, column_name
        This method is used to select the join of tables and display them.
        
        Input:
        Database configuration object, table names, columns and values.
        
        DB_DICT {'households': ['htaz', 'numchild', 'inclt35k', 'hhsize'], 
                 'persons': ['male', 'schstatus', 'one', 'houseid', 'personid'], 
                 'schedule_r': ['scheduleid', 'activitytype']}
        COLUMN_NAMES {'households': ['houseid'], 
                      'schedule_r': ['personid', 'houseid']}
        TABLE_NAMES ['persons', 'households', 'schedule_r']
        MAX_DICT {'schedule_r': ['scheduleid']}
        SPATIALCONST_LIST [Table - travel_skims; 
                           Field - tt
                           Orifin Field - origin; 
                           Destination Field - destination; 
                           Sample Field - destination
                           Start Constraint - Table - schedule_r; Location Field - locationid; Time Field - endtime
                           End Constraint - Table - schedule_r; Location Field - locationid; Time Field - starttime
                           Number of choices - 5
                           Threshold for window - 120]
         ANALYSISINTERVAL 195
         SUBSAMPLE None

         Test SQL String for above inputs:
         select households.htaz,households.numchild,households.inclt35k,households.hhsize,persons.male,persons.schstatus,persons.one,
         persons.houseid,persons.personid,schedule_r.activitytype,temp.scheduleid,stl.locationid as st_locationid,enl.locationid 
         as en_locationid,sptime.st_endtime,sptime.en_starttime from persons  left join households on 
         ( persons.houseid=households.houseid ) left join (select personid,houseid, max(scheduleid) 
         as scheduleid from schedule_r group by personid,houseid) as temp on 
         ( temp.personid=persons.personid and temp.houseid=persons.houseid )  
         left join schedule_r on 
         ( persons.personid=schedule_r.personid and persons.houseid=schedule_r.houseid and schedule_r.scheduleid=temp.scheduleid) 
         join (select st.personid personid,st.houseid houseid, min(st.endtime) st_endtime,min(en.starttime) 
               en_starttime from schedule_r as st inner join schedule_r as en on 
               (  st.personid = en.personid and st.houseid = en.houseid  and st.endtime=195 and en.starttime>195) 
               group by st.personid,st.houseid) as sptime on ( sptime.personid = persons.personid and sptime.houseid = persons.houseid ) 
               left join schedule_r stl on 
               ( stl.personid = persons.personid and stl.houseid = persons.houseid and sptime.st_endtime = stl.endtime)  
               left join schedule_r enl on 
               ( enl.personid = persons.personid and enl.houseid = persons.houseid and sptime.en_starttime = enl.starttime) 



        Output:
        Displays the rows based on the join and the selection criterion.
        """
        self.dbcon_obj.new_sessionInstance()        

        print 'DB_DICT', db_dict
        print 'COLUMN_NAMES', column_names
        print 'TABLE_NAMES', table_names
        print 'MAX_DICT', max_dict
        print 'SPATIALCONST_LIST', spatialConst_list
        print 'ANALYSISINTERVAL', analysisInterval
        print 'SUBSAMPLE', subsample

        #db_dict = {'households': ['urb', 'numchild', 'inclt35k', 'ownhome', 'one', 'drvrcnt', 'houseid'], 
        #           'vehicles_r': ['vehtype', 'vehid'], 
        #           'households_r': ['numvehs']}
        #columns_names = ['houseid']
        #table_names = ['households', 'households_r', 'vehicles_r']
        #max_dict = {'vehicles_r':['vehid']}
        
        # Prism Query or or just a Travel Time Query with Vertices
        # ADD APPROPRIATE JOIN/?INNER JOINS


        print 'Database Dictionary of Table and Columns - ', db_dict
        print 'Column Names', column_names
        #raw_input()

        #initialize the variables
        final_list = []
        table_list = []
        class_list = []
        cols_list = []
        tabs_list = []
        #col_name = column_name
        final_col_list = db_dict.values()
        table_list = db_dict.keys()      
        
        """
        #check if the table exists. If not return none
        if chk_table.lower() in [each.lower() for each in table_list]:
            print 'table %s is present in the table list'%chk_table
        else:
            print 'table %s is not present in the table list'%chk_table
            return None
        """
        
        #similarly check if the table in the list exists
        num_tab = len(list(set(table_list) & set(table_names)))
        if num_tab <= len(table_list):
            #print 'Tables exist'
            pass
        else:
            #print 'Tables do not exists'
            return None
        
        #check for the columns passed in the dictionary
        for i in db_dict.keys():
            clist = self.dbcon_obj.get_column_list(i.lower())
            list1 = db_dict[i]
            #print 'table--', i
            #print 'clist', clist
            #print 'list1', list1
            chk_list = len(list(set(list1) & set(clist)))
            if chk_list == len(list1):
                for j in db_dict[i]:
                    #print '\tColumn - ', j
                    new_str = i.lower() + '.' + j.lower()
                    final_list.append(new_str)                    
            else:
                print ('Column passed in the dictionary does not exist in the table - ')
                print 'Column List in the Table - ', clist
                print 'Actual List of Columns requested from table - ', list1
                
                return None
        #print 'final_list is %s'%final_list
        

                
        #print 'FINAL LIST', final_list
        #print 'TABLE LIST', table_list

        # Generating the left join statements
        mainTable = table_names[0]
        #print 'mainTable ----> ', mainTable

        primCols = []
        for i in column_names:
            primCols += column_names[i]
        primCols = list(set(primCols))

        joinStrList = []
        for table in table_list:
            if table == mainTable:
                continue
            joinCondition = ''
            for col in column_names[table]:
                joinCondition = (joinCondition 
                                 + ' %s.%s=%s.%s ' %(mainTable, col, 
                                                     table, col) 
                                 + 'and')
                
            joinCondition = joinCondition[:-3]
            joinStr = ' left join %s on (%s)' %(table, joinCondition)
            joinStrList.append(joinStr)

        #print 'JOIN STRING LIST', joinStrList

        #check the max flag
        
        if max_dict is not None:
            max_flag = 1
            max_table = max_dict.keys()
            max_column = max_dict.values()[0][0]
            #print max_column, max_table
            #for each in max_dict.values():
            #    max_column = each[0]
        else:
            max_flag = 0

        # Index of the table containing the max dict var
        # as it stands only querying for one count variable is 
        # provided
        #print max_dict
        if max_dict is not None:
            maxTable = max_dict.keys()[0]
            maxColumn = max_dict.values()[0][0]
            index = table_list.index(maxTable)
            #print 'INDEX--->', index
        
            #remove the count column from the col list
            countVarStr = '%s.%s' %(maxTable, maxColumn)
            final_list.remove(countVarStr)
            final_list.append('temp.%s'%maxColumn)

            #print 'NEW FINAL LIST -->', final_list

            # left join for the count variable
            joinStr = ''


            #grouping string
            grpStr = ''
            joinCondition=''

            #print 'column_names of max TABLE ----->', column_names
            for i in column_names[maxTable]:
                #print 'createing join string for column name - ', i
                grpStr = grpStr + '%s,' %(i)
                joinCondition = (joinCondition 
                                 + ' temp.%s=%s.%s ' %(i, 
                                                       mainTable, i) 
                                 + 'and')
            grpStr = grpStr[:-1]
            joinCondition = joinCondition[:-3]
            
        #combine left join along with the count variable/max condition
            mJoinStr = joinStrList.pop(index-1)
            mJoinStrIncMaxConditionVar = (mJoinStr[:-1] + 
                                          'and %s.%s=temp.%s)' 
                                          %(maxTable, maxColumn, maxColumn))
            
            joinStrList.append(""" left join (select %s, max(%s) as %s from """
                               """%s group by %s) as temp on (%s) """ %(grpStr, maxColumn, 
                                                                        maxColumn,maxTable, grpStr,
                                                                        joinCondition)
                               + mJoinStrIncMaxConditionVar)
            #print 'LEFT JOIN MAX COL LIST--->', joinStrList

        # Spatial TSP identification
        if spatialConst_list is not None:
            for i in spatialConst_list:
                if i.countChoices is not None:
                    # substring for the inner join
                    stTable = i.startConstraint.table
                    #stLocationField = 'st_' + i.startConstraint.locationField
                    stLocationCol = 'stl.%s' %i.startConstraint.locationField
                    #stTimeField = 'st_'+ i.startConstraint.timeField
                    stTimeCol = 'st.%s' %i.startConstraint.timeField

                    enTable = i.endConstraint.table
                    #enLocationField = 'en_' + i.endConstraint.locationField
                    enLocationCol = 'enl.%s' %i.endConstraint.locationField
                    #enTimeField = 'en_' + i.endConstraint.timeField                    
                    enTimeCol = 'en.%s' %i.endConstraint.timeField

                    timeCols = [stTimeCol, enTimeCol]

                    table_list.append(stTable)
                    

                    # left join for end location
                    
                    # time cols are part of sptime
                    timeColsNewNames = []
                    for j in timeCols:
                        timeColsNewNames.append(j.replace('.', '_'))
                        
                    timeColsStr = ''
                    for j in range(len(timeCols)):
                        # minimum of the time cols gives the first prism
                        timeColsStr += 'min(%s) %s,' %(timeCols[j], timeColsNewNames[j])

                    timeColsStr = timeColsStr[:-1]

                    spGrpNewNameStr = ''
                    spGrpStr = ''
                    for j in column_names[stTable]:
                        spGrpNewNameStr += 'st.%s %s,' %(j, j)
                        spGrpStr += 'st.%s,' %(j)
                    spGrpNewNameStr = spGrpNewNameStr[:-1]
                    spGrpStr = spGrpStr[:-1]

                    spInnerJoinCondition = ''
                    for j in column_names[stTable]:
                        spInnerJoinCondition += ' %s.%s = %s.%s and' %('st', j, 'en', j)
                    spInnerJoinCondition = spInnerJoinCondition[:-3]
                        
                    spJoinCondition = ''
                    for j in column_names[stTable]:
                        spJoinCondition += ' %s.%s = %s.%s and' %('sptime', j, mainTable, j)
                    spJoinCondition = spJoinCondition[:-3]

                    # Left join condition for prism start location
                    stLocJoinCondition = ''
                    stLocCondCols = column_names[stTable] 
                    for j in stLocCondCols:
                        stLocJoinCondition += ' %s.%s = %s.%s and' %('stl', j, mainTable, j)
                    stLocJoinCondition += ' sptime.st_%s = %s.%s' %(i.startConstraint.timeField,
                                                               'stl', i.startConstraint.timeField)

                    final_list.append('stl.%s as st_%s' %(i.startConstraint.locationField,
                                                          i.startConstraint.locationField))
                    cols_list.append('st_%s' %i.startConstraint.locationField)
                    #stLocJoinCondition = stLocJoinCondition[:-3]

                    # Left join condition for prism end location
                    enLocJoinCondition = ''
                    enLocCondCols = column_names[stTable] 
                    for j in enLocCondCols:
                        enLocJoinCondition += ' %s.%s = %s.%s and' %('enl', j, mainTable, j)
                    enLocJoinCondition += ' sptime.en_%s = %s.%s' %(i.endConstraint.timeField,
                                                               'enl', i.endConstraint.timeField)
                    final_list.append('enl.%s as en_%s' %(i.endConstraint.locationField, 
                                                       i.endConstraint.locationField))
                    cols_list.append('en_%s' %i.endConstraint.locationField)
                    #enLocJoinCondition = enLocJoinCondition[:-3]

                    
                    # TSP consistency check
                    # nextepisode_starttime > lastepisode_endtime
                    #consistencyStr = '%s < %s' %(stTimeCol, endTimeCol)
                    

                    analysisPeriodStr = ('%s=%s and %s>%s' 
                                         %(stTimeCol, analysisInterval,
                                           enTimeCol, analysisInterval))

                    spatialJoinStr = (""" join (select %s, %s """\
                                          """from %s as %s """\
                                          """inner join %s as %s """\
                                          """on ( %s and %s) group by"""\
                                          """ %s) """\
                                          """as sptime on (%s)"""
                                      % (spGrpNewNameStr, timeColsStr, 
                                         stTable, 'st', 
                                         enTable, 'en',
                                         spInnerJoinCondition, analysisPeriodStr,
                                         spGrpStr,
                                         spJoinCondition))
                    #print 'SPATIAL JOIN'
                    #print spatialJoinStr
                    # left join for start location

                    stLocJoinStr = (""" left join %s %s on """\
                                        """(%s) """ 
                                    %(stTable, 'stl', stLocJoinCondition))


                    enLocJoinStr = (""" left join %s %s on """\
                                        """(%s) """ 
                                    %(enTable, 'enl', enLocJoinCondition))


                    joinStrList.append(spatialJoinStr)
                    joinStrList.append(stLocJoinStr)
                    joinStrList.append(enLocJoinStr)
                    
                    cols_list += timeColsNewNames
                    

                    for i in timeColsNewNames:
                        final_list.append('sptime.%s' %(i))
                    # Only one time-space prism can be retrieved within a component
                    # there cannot be two TSP's in the same component
                    break
                                         
                                         
                                         
                    
                    
                    
        # Generating the col list
        colStr = ''
        for i in final_list:
            colStr = colStr + '%s,' %(i)
        colStr = colStr[:-1]
        
        # Build the SQL string
        allJoinStr = ''
        for i in joinStrList:
            allJoinStr = allJoinStr + '%s' %i
            

        sql_string = 'select %s from %s %s' %(colStr, mainTable, allJoinStr)
        print 'SQL string for query - ', sql_string
            


        #convert all the table names to upper case
        for each in table_list:
            tabs_list.append(each.upper())
        #print 'tabs_list is %s'%tabs_list
        
        #separate all the columns from the lists
        new_keys = db_dict.keys()
        for i in new_keys:
            cols_list = cols_list + db_dict[i]
        #print 'cols_list is %s'%cols_list
        
        try:
            sample_str = ''
            ctr = 0
            for i in tabs_list:
                if ctr==0:
                    sample_str = i
                    ctr = ctr + 1
                else:
                    sample_str = sample_str + ', ' + i
                query = self.dbcon_obj.session.query((sample_str))

            #print 'sample_str is %s'%sample_str                
                
            result = query.from_statement(sql_string).values(*cols_list)
                        
            resultArray = self.createResultArray(result)

            # Returns the query as a DataArray object
            data = DataArray(resultArray, cols_list)

            data.sort(primCols)
            self.dbcon_obj.close_sessionInstance()        
        
            return data
        except Exception, e:
            print e
            print 'Error retrieving the information. Query failed.'
                 

    ########## methods for select query end ##########

    ########## methods for delete query ##########
    
    def createResultArray(self, result, fillValue=0):
        t = time.time()

        # Create list of records
        data = [i[:] for i in result]
        print '\tLooping through results took - %.4f' %(time.time()-t), len(data)

        # Converting the none values returned into a zero value
        # using the ma library in numpy
        # - retrieve mask for None
        # - then assign the fillValue to those columns
        data = array(data)
        mask = ma.masked_equal(data, None).mask

        if mask.any():
            data[mask] = fillValue

        #Sorting the array by primary cols identifying the agent as 
        # postgres seems to return queries without any order
            
        
        # Convert it back to a regular array to enable all the other processing
        print '\tSize of the data set that was retrieved - ', data.shape
        print '\tRecords were processed after query in %.4f' %(time.time()-t)

        return data



    #delete rows based on a deletion criteria
    def delete_selected_rows(self, class_name, col_name, value):
        """
        This method is used to delete selected rows fom the table in the database.

        Input:
        Database configuration object, table name and selection criteria

        Output:
        Deletes the rows that satisfy the selection criteria
        """

        print 'testing delete'
        new_class_name = class_name.upper()
        
        new_table_name = new_class_name.lower()
        
        col = []
        temp_table = Table(new_table_name, self.dbcon_obj.metadata, autoload=True)
        #print 'table object is %s'%temp_table
        for cl in temp_table.c:
            col.append(cl)

        try:
            self.dbcon_obj.session.query(eval(new_class_name))\
                .filter(getattr((eval(new_class_name)), col_name) == value).delete()
            """
            #based on the count determine if any rows were selected
            if delete_query.count() == 0:
                print 'No rows were fetched. Cannot complete delete operation.'
            else:                
                for each_ins in delete_query:
                    #print 'each is %s'%each_ins
                    self.dbcon_obj.session.delete(each_ins)
            """
            #print 'Selected rows delete successful.'                    
        except Exception, e:
            print e
            print 'Selected rows delete failed'
        

    #delete all rows i.e. empty table
    def delete_all(self, class_name):
        """
        This method is used to delete all rows from the table.

        Input:
        Database configuration object, table name

        Output:
        Deletes all rows in the table
        """
        self.dbcon_obj.new_sessionInstance()        
        new_class_name = class_name.upper()

        new_table_name = new_class_name.lower()
        #print 'table name is %s and class name is %s'%(new_class_name, new_table_name)
        
        #fetch al rows of the table and then delete
        col = []
        temp_table = Table(new_table_name, self.dbcon_obj.metadata, autoload=True)
        for cl in temp_table.c:
            #print 'column is %s'%cl
            col.append(cl)

        try:
            self.dbcon_obj.session.query(eval(new_class_name)).delete()
            """
            print 'query is %s'%query
            if query.count() == 0:
                print 'No rows fectched. Cannot complete delete operation'
            else:
                for instance in query:
                    #print instance
                    self.dbcon_obj.session.delete(instance)
            """
            #print '\t    Delete all records successful.'
            self.dbcon_obj.close_sessionInstance()        
        except Exception, e:
            print e
            print '\t    Delete all records failed.'

    ########## methods for delete query end ##########


    ########## methods for insert query ##########
    #insert values in the table
    def insert_into_table(self, arr, col_list, class_name, keyCols, chunkSize=100000):
        """
        This method is used to insert new values into the table.

        Input:
        Database configuration object, table name and values
        chunkSize = number of rows to be written at once; to avoid memory issues
        arr = is a list of tuples extracted from the hdf5 format

        Output:
        Values inserted in to the table
        """

    
        #method 4
        #before inserting data delete the index
        index_cols = self.delete_index(class_name.lower())
        
        #make a string of the columns
        col_str = ''
        col_count = 0
        for i in col_list:
            if col_count < (len(col_list)-1):
                col_str = col_str + i + ', '
                col_count = col_count + 1
            else:
                col_str = col_str + i


        # Breaking it into chunks for insert
        last = 0
        lastRow = len(arr)
        nChunks = int(lastRow/chunkSize)

        t = time.time()

        for i in range(nChunks):
            #print 'rows - ', i*chunkSize, (i+1)*chunkSize
            last = (i+1)*chunkSize
            arrSub = arr[i*chunkSize:last]
            self.insert_nrows(class_name, arrSub, col_str)

        #print 'rows - ', last, lastRow
        arrSub = arr[last:lastRow]
        self.insert_nrows(class_name, arrSub, col_str)

        #after insert create new index
        self.create_index(class_name.lower(), keyCols)
        print """\t    Time  after inserting all using chunks of size """\
            """%s - %.4f\n"""%(chunkSize, time.time()-t)


    def insert_nrows(self, class_name, arr, col_str):
        self.dbcon_obj.new_sessionInstance()        
        arr_str = str(arr)[1:-1]
        #print arr_str

        try:
            insert_stmt = "insert into %s (%s) values %s"%(class_name.lower(), col_str, arr_str)
            #print insert_stmt
            result = self.dbcon_obj.connection.execute(insert_stmt)
            self.dbcon_obj.close_sessionInstance()        
        except Exception, e:
            print '\t    Error while inserting data in the table'
            print e.message
        self.dbcon_obj.close_sessionInstance()        
        

    ########## methods for insert query end ##########
    
    ########## methods for creating and deleting index##########
    #create an index
    def create_index(self, class_name, col_list):
        self.dbcon_obj.new_sessionInstance()        
        index_stmt = ''
        columns = ''
        count = 0
        index_name = class_name.lower() + '_index'
        for i in col_list:
            if count < (len(col_list)-1):
                columns = columns + i + ', '
                count = count + 1
            else:
                columns = columns + i
        index_stmt = 'create index %s on %s (%s)'%(index_name, class_name.lower(), columns)
        try:
            self.result = self.dbcon_obj.connection.execute(index_stmt)
            #print '\t    Index %s created'%index_name
            self.dbcon_obj.close_sessionInstance()        
        except Exception, e:
            print '\t    Error while creating an index'
            print e

            
    #delete an index
    def delete_index(self, class_name):
        self.dbcon_obj.new_sessionInstance()        
        index_stmt = ''
        columns = []
        count = 0
        index_name = class_name.lower() + '_index'
        index_stmt = 'drop index %s'%(index_name)
        try:
            new_table = Table(self.class_name.lower(), self.dbcon_obj.metadata, autoload=True)
            pk = new_table.indexes
            parts = str(pk).split("'")
            count = 1
            for i in parts:
                if count%2 == 0:
                    columns.append(i)
                count = count + 1
            self.result = self.dbcon_obj.connection.execute(index_stmt)
            print '\t    Index %s deleted'%index_name
            self.dbcon_obj.close_sessionInstance()        
            return columns
        except Exception, e:
            print '\t    Error while creating an index'
            print e
        
    ########## methods for creating and deleting index##########
    

#unit test to test the code
import unittest

#define a class for testing
class TestMainClass(unittest.TestCase):
    #only initialize objects here
    def setUp(self):
        self.protocol = 'postgres'		
        self.user_name = 'postgres'
        self.password = '1234'
        self.host_name = 'localhost'
        self.database_name = 'postgres'

    
    def testMainClass(self):
        newobject = MainClass(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        #newobject = MainClass(self.protocol, self.user_name, self.password, self.host_name, self.database_name, self.database_config_object, self.dbcon_obj)
        """ create a connection to the database """
        newobject.dbcon_obj.new_connection()
        
        """ create mapper objects for all classes """
        newobject.create_mapper_for_all_classes()
        
        """ to select all rows from the table """
        class_name = 'School'
        #newobject.select_all_fom_table(class_name)

        """ to select few rows """
        class_name = 'Office'
        column_name = 'role'
        value = 'se'
        #newobject.fetch_selected_rows(class_name, column_name, value)

        """ to print the join """
        column_names = ['role_id']
        table_names = ['Office', 'Person']
        new_col = 'role_id'
        value = '1'
        chk_table = 'Person'
        db_dict = {'Person':['first_name', 'last_name'], 'Office':['role', 'years'], 'Asu':['grad', 'undergrad']}
        max_dict = {'Person':['salary', '1']}
        #db_dict = {'Person':['first_name', 'last_name', 'salary'], 'Office':['role', 'years']}
        #db_dict = {'Person':['first_name', 'last_name']}

        newobject.select_join(db_dict, column_names, table_names, max_dict)
        #newobject.select_join(temp_dict, column_name, chk_table)
        
        """ delete all records """
        class_name = 'School'
        #newobject.delete_all(class_name)

        """ delete selected rows """
        class_name = 'School'
        col_name = 'teacher'
        value = 'ab'
        #newobject.delete_selected_rows(class_name, col_name, value)
        
        """ to select all rows from the table """
        class_name = 'School'
        #newobject.select_all_fom_table(class_name)
        
        """ to insert rows """
        class_name = 'Person2'
        arr = na.arange(1000000).reshape(500000,2)
        col_list = ['age', 'id']
        #print arr
        newobject.insert_into_table(arr, col_list, class_name)        
        
        """ create an index """
        class_name = 'Person2'
        col_list = ['id', 'age']
        #newobject.create_index(class_name, col_list)
        
        """ delete an index """
        class_name = 'Person2'
        #newobject.delete_index(class_name)
        
        """ close the connection to the database """
        newobject.dbcon_obj.close_connection()


if __name__ == '__main__':
    unittest.main()
