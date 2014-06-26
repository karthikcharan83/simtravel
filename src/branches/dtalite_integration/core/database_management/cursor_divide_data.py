#main class. this class will be used to define the database connection.
#it will create/drop database, schema and tables
 

#include all the import 
import sys
import os
import exceptions
import time
import sqlalchemy
import psycopg2 as dbapi2
import numpy as na
import time
from cursor_database_connection import DataBaseConnection
from psycopg2 import extensions
from sqlalchemy.types import Integer, SmallInteger, \
			                 Numeric, Float, \
            			     VARCHAR, String, CLOB, Text,\
			                 Boolean, DateTime
from numpy import array, ma
from database_configuration import DataBaseConfiguration
from cursor_query_browser import QueryBrowser
from openamos.core.data_array import DataArray

class DivideData(object):
    #initialize the class 

    def __init__(self,dbconfig):
        
        if not isinstance(dbconfig, DataBaseConfiguration):
            raise DatabaseConfigurationError, """The dbconfig input is not a valid """\
                """DataBaseConfiguration object."""

        self.protocol = dbconfig.protocol
        self.user_name = dbconfig.user_name
        self.password = dbconfig.password
        self.host_name = dbconfig.host_name
        self.database_name = dbconfig.database_name
        self.database_config_object = dbconfig
        self.dbcon_obj = DataBaseConnection(dbconfig)
        self.qb_obj = QueryBrowser(dbconfig)
        print self.dbcon_obj
        print self.qb_obj
        
        #input table names
        self.house_tab = 'households'
        self.persons_tab = 'persons'

        #output tables names
        self.child_tab = 'child_dependency_r'
        self.school_tab = 'daily_school_status_r'
        self.work_tab = 'daily_work_status_r'
        self.veh_count_tab = 'households_vehicles_count_r'
        self.ltrec_tab = 'schedule_ltrec_r'
        self.schedule_tab = 'schedule_r'
        self.trips_tab = 'trips_r'
        self.veh_tab = 'vehicles_r'
        self.workers_tab = 'workers_r'
	self.schedule_child_tab = 'schedule_childreninctravelrec_r'
	self.schedule_clean_tab = 'schedule_cleanfixedactivityschedule_r'
	#self.schedule_conflict_tab = 'schedule_conflictrec_r'
	self.schedule_daily_tab = 'schedule_dailyallocrec_r'
	self.schedule_final_tab = 'schedule_final_r'
	self.schedule_intravel_tab = 'schedule_inctravelrec_r'
        
        #output tables resultset
        self.child_op = None
        self.school_op = None
        self.work_op = None
        self.veh_count_op = None
        self.ltrec_op = None
        self.schedule_op = None
        self.trips_op = None
        self.veh_op = None
        self.workers_op = None
	self.schedule_child_op = None
	self.schedule_clean_op = None
	#self.schedule_conflict_op = None
	self.schedule_daily_op = None
	self.schedule_final_op = None
	self.schedule_intravel_op = None


    #create dummy databases
    def dummy_db(self, dbname, number):
        """
        This method is used to create the dummy databases.
        This method is called before any other method in this class
        
        Input:
        Number of dummy databases
        
        Output:
        Dummy databases created
        """
        #database name
        db_name = dbname
        db_str = ''
        t1 = time.time()
       
        for each in range(number):
            db_str = db_name + '_' + str(each+1)
            self.dbcon_obj.database_name = db_str
            result = self.dbcon_obj.create_database(db_str)
            result = result * result
        
        self.dbcon_obj.database_name = dbname

        t2 = time.time()
        print 'Total time taken to create new databases %s'%(t2-t1)

        if result:
            return 'true'
        else:
            return 'false'


    #get the datatypes and primary keys
    def get_tab_structure(self, table_name):
        """
        This method is used to get the data types and the primary keys
        
        Input:
        Database configuration object and table name
        
        Output:
        List of datatypes and primary keys
        """
        #get the columns
        cols = self.dbcon_obj.get_column_list(table_name)
        
        #get the data types of the columns
        data_type = self.dbcon_obj.get_column_types(table_name)
	
	#get column defaults
	col_defaults = self.dbcon_obj.get_column_defaults(table_name)        

        #get the keys of the table
        keys = self.dbcon_obj.get_table_keys(table_name)
        
        #generate the list for the keys
        key_list = []
        for column in cols:
            key_list.append(0)
            
        for key in keys:
            index = cols.index(key)
            key_list[index] = 1
        
        #key list created. return the required
        return cols, data_type, col_defaults, key_list
        

    #get the columns and then create the list of datatypes and keys
    def get_table_info(self):
        """
        This method is used to get the table information
        
        Input:
        
        Output:
        
        """     
        #get info for all tables and store them in variable
        #input tables
        self.house_cols, self.house_dt, self.house_def, self.house_keys = self.get_tab_structure(self.house_tab)
        self.persons_cols, self.persons_dt, self.persons_def, self.persons_keys = self.get_tab_structure(self.persons_tab)
        
        #output tables
        self.child_cols, self.child_dt, self.child_def, self.child_keys = self.get_tab_structure(self.child_tab)
        self.school_cols, self.school_dt, self.school_def, self.school_keys = self.get_tab_structure(self.school_tab)
        self.work_cols, self.work_dt, self.work_def, self.work_keys = self.get_tab_structure(self.work_tab)
        self.veh_count_cols, self.veh_count_dt, self.veh_count_def, self.veh_count_keys = self.get_tab_structure(self.veh_count_tab)
        self.ltrec_cols, self.ltrec_dt, self.ltrec_def, self.ltrec_keys = self.get_tab_structure(self.ltrec_tab)
        self.schedule_cols, self.schedule_dt, self.schedule_def, self.schedule_keys = self.get_tab_structure(self.schedule_tab)
        self.trips_cols, self.trips_dt, self.trips_def, self.trips_keys = self.get_tab_structure(self.trips_tab)
        self.veh_cols, self.veh_dt, self.veh_def, self.veh_keys = self.get_tab_structure(self.veh_tab)
        self.workers_cols, self.workers_dt, self.workers_def, self.workers_keys = self.get_tab_structure(self.workers_tab)
	self.schedule_child_cols, self.schedule_child_dt, self.schedule_child_def, self.schedule_child_keys = self.get_tab_structure(self.schedule_child_tab)
	self.schedule_clean_cols, self.schedule_clean_dt, self.schedule_clean_def, self.schedule_clean_keys = self.get_tab_structure(self.schedule_clean_tab)
	#self.schedule_conflict_cols, self.schedule_conflict_dt, self.schedule_conflict_keys = self.get_tab_structure(self.schedule_conflict_tab)
	self.schedule_daily_cols, self.schedule_daily_dt, self.schedule_daily_def, self.schedule_daily_keys = self.get_tab_structure(self.schedule_daily_tab)
	self.schedule_final_cols, self.schedule_final_dt, self.schedule_final_def, self.schedule_final_keys = self.get_tab_structure(self.schedule_final_tab)
	self.schedule_intravel_cols, self.schedule_intravel_dt, self.schedule_intravel_def, self.schedule_intravel_keys = self.get_tab_structure(self.schedule_intravel_tab)	


    #create db and tables based on the parts
    def create_partitions(self, databasename, parts):
        """
        This method is used to create db's and tables based on the 
        the number of parts.
        
        Input:
        Database configuration object and parts
        
        Output:
        Databases and tables created
        """
        #database name
        db_name = databasename
        
        #databases are created. add tables to each
        #run a loop the create the new table names
        t1 = time.time()
        for each in range(parts):
            db_str = db_name + '_' + str(each+1)
            self.dbcon_obj.database_name = db_str

            #create a new database connection
            self.dbcon_obj.new_connection()
            
            #create the tables
            #print 'child keys is %s'%self.child_keys
            self.dbcon_obj.create_table(self.house_tab, self.house_cols, self.house_dt, self.house_def, self.house_keys)
            self.dbcon_obj.create_table(self.persons_tab, self.persons_cols, self.persons_dt, self.persons_def, self.persons_keys)
            self.dbcon_obj.create_table(self.child_tab, self.child_cols, self.child_dt, self.child_def, self.child_keys)
            self.dbcon_obj.create_table(self.school_tab, self.school_cols, self.school_dt, self.school_def, self.school_keys)
            self.dbcon_obj.create_table(self.work_tab, self.work_cols, self.work_dt, self.work_def, self.work_keys)
            self.dbcon_obj.create_table(self.veh_count_tab, self.veh_count_cols, self.veh_count_dt, self.veh_count_def, self.veh_count_keys)
            self.dbcon_obj.create_table(self.ltrec_tab, self.ltrec_cols, self.ltrec_dt, self.ltrec_def, self.ltrec_keys)
            self.dbcon_obj.create_table(self.schedule_tab, self.schedule_cols, self.schedule_dt, self.schedule_def, self.schedule_keys)
            self.dbcon_obj.create_table(self.trips_tab, self.trips_cols, self.trips_dt, self.trips_def, self.trips_keys)
            self.dbcon_obj.create_table(self.veh_tab, self.veh_cols, self.veh_dt, self.veh_def, self.veh_keys)
            self.dbcon_obj.create_table(self.workers_tab, self.workers_cols, self.workers_dt, self.workers_def, self.workers_keys)
	    self.dbcon_obj.create_table(self.schedule_child_tab, self.schedule_child_cols, self.schedule_child_dt, 
					self.schedule_child_def, self.schedule_child_keys)
	    self.dbcon_obj.create_table(self.schedule_clean_tab, self.schedule_clean_cols, self.schedule_clean_dt, 
					self.schedule_clean_def, self.schedule_clean_keys)
	    #self.dbcon_obj.create_table(self.schedule_conflict_tab, self.schedule_conflict_cols, self.schedule_conflict_dt, self.schedule_conflict_keys)
	    self.dbcon_obj.create_table(self.schedule_daily_tab, self.schedule_daily_cols, self.schedule_daily_dt, 
					self.schedule_daily_def, self.schedule_daily_keys)
	    self.dbcon_obj.create_table(self.schedule_final_tab, self.schedule_final_cols, self.schedule_final_dt, 
					self.schedule_final_def, self.schedule_final_keys)
	    self.dbcon_obj.create_table(self.schedule_intravel_tab, self.schedule_intravel_cols, self.schedule_intravel_dt,
					self.schedule_intravel_def, self.schedule_intravel_keys)
            
            #close the database connection
            self.dbcon_obj.close_connection()
        
        #assign the old database name to the config obj
        self.dbcon_obj.database_name = databasename
        
        t2 = time.time()
        print 'Total time taken to create new tables in the databases %s'%(t2-t1)

    
    #get row count of the table
    def get_count(self, table_name, column_name):
        """
        This method is used to get the max of houseid from the table specified.

        Input:
        Class name corresponding to the table and column name

        Output:
        Returns all the rows in the table
        """
        #check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        
        sql_string = "SELECT max(%s) FROM %s"%(column_name, table_name)

        if tab_flag:
            try:    
                self.dbcon_obj.cursor.execute(sql_string)
                result = self.dbcon_obj.cursor.fetchall()
                res = []
                for each in result:
                    res.append(each[0])
                return res[0]
            except Exception, e:
                print 'Error while retreiving the data from the table'
                print e
        else:
            print 'Table %s does not exist.'%table_name
            

    #divide the rows
    def divide_rows(self, parts):
        """
        This method divides the rows in the households tables
        
        Input:
        Number of parts
        
        Output:
        Intervals
        """
        tab = 'households'
        col = 'houseid'
        total = self.get_count(tab, col)

        interval_list = []
        interval = total/parts
        for each in range(parts-1):
            next_val = interval * (each+1)
            interval_list.append(next_val)
        interval_list.append(total)

        return interval_list
           
  
    #select rows based on a selection criteria
    def get_interval_rows(self, databasename, each_table, column_name, interval_list, index):
        """
        This method is used to get selected rows between the interval 
        from the table in the database.

        Input:
        Database configuration object, class name and selection criteria.

        Output:
        Returns the rows that satisfy the selection criteria
        """   
        #create a new database connection
        self.dbcon_obj.new_connection()
        
        fin_flag = None
        
        #check if table exists
        fin_flag = self.dbcon_obj.check_if_table_exists(each_table)

        #declare the interval
        if index == 0:
            low = 1
            high = interval_list[index]
        else:
            low = interval_list[index-1] + 1
            high = interval_list[index]
        
        t1 = time.time()
        #create a sql query for the table
        sql_string = "SELECT * FROM %s WHERE %s BETWEEN %s AND %s"%(each_table, column_name, low, high)

        #print 'sql query is %s and index --> %s'%(sql_string, index)
        
        if fin_flag:
            try:
                self.dbcon_obj.cursor.execute(sql_string)
                table_data = self.dbcon_obj.cursor.fetchall()

                table_rows = []
                count = 0
                new_rows = []
                for each in table_data:
                    count = count + 1
                    table_rows.append(each)
                    if None in each:
                        each = list(each)
                        loc = each.index(None)
                        each[loc] = 0
                        new_rows.append(each)
                        #print 'None present'

                #close the new database connection
                self.dbcon_obj.close_connection()

                if count == 0:
                    print 'No rows selected.\n'           
                print 'Select query successful.\n'
                if len(new_rows) == 0:
                    return table_rows
                else:
                    return new_rows
                
            except Exception, e:
                print 'Error retrieving the information. Query failed.\n'
                print e
        else:
            print 'Table(s) do not belong to the database.'
            #close the new database connection
            self.dbcon_obj.close_connection()
            
            t2 = time.time()
            print 'Total time taken to select the required rows %s'%(t2-t1)
            return None    
        
    
    #trial insert query
    def insert_data(self, databasename, arr, table_name, index):
        """
        This method is used to insert data into the table
        
        Input:
        Array of the values and the table name
        
        Output:
        Data inserted into the table
        """
        sqlstr, ser_col = self.check_sequences(table_name)
        print 'sequence chk successful. seq col is ', ser_col
        db_name = databasename
        #open a new connection to the required database
        db_str = db_name + '_' + str(index+1)
        self.dbcon_obj.database_name = db_str
        
        t1 = time.time()
        
        #create a new database connection
        self.dbcon_obj.new_connection()
        
        #table = 'temp_households'
	print table_name
        cols = self.dbcon_obj.get_column_list(table_name)
        col_str = ''
        col_count = 0
        for i in cols:
            if i not in ser_col:
                if col_count < (len(cols)-(len(ser_col)+1)):
                    col_str = col_str + i + ', '
                    col_count = col_count + 1
                else:
                    col_str = col_str + i

        if len(arr) < 1:
            return None

        arr_str = [tuple(each) for each in arr]
        arr_str = str(arr_str)[1:-1]
        arr_str = arr_str.replace('L', '')
                    
        sql_string = 'insert into %s (%s) values %s'%(table_name, col_str, arr_str)

        t1 = time.time()
        try:
            self.dbcon_obj.cursor.execute(sql_string)
            self.dbcon_obj.connection.commit()
        except Exception, e:
            print e
        
        t2 = time.time()
        print 'total taken to insert %s'%(t2-t1)
        
        #close the new database connection
        self.dbcon_obj.close_connection()
        
        #assign old database name
        self.dbcon_obj.database_name = databasename
        
        t2 = time.time()
        print 'Total time taken to insert records %s'%(t2-t1)
        
        
    #copy the data from a csv file
    def copy_data(self, databasename, table_name1, table_name2, index, location):
        """
        This method copies the data from a csv file into the 
        persons and households table
        
        Input:
        
        Output:
        """
        db_name = databasename
        #open a new connection to the required database
        db_str = db_name + '_' + str(index+1)
        self.dbcon_obj.database_name = db_str

        #create a new database connection
        self.dbcon_obj.new_connection()
        
        #check if the table exists
        tab_flag1 = self.dbcon_obj.check_if_table_exists(table_name1)
        tab_flag2 = self.dbcon_obj.check_if_table_exists(table_name2)
        if tab_flag1 == tab_flag2:
            try:
                #for the first table
                t1 = time.time()
                insert_stmt = ("""copy %s from '%s/households.csv' """
                               """ delimiters ',' csv header""" %(table_name1, location))
                result = self.dbcon_obj.cursor.execute(insert_stmt)
                self.dbcon_obj.connection.commit()
                t2 = time.time()
                print 'Time taken to copy %s -- %s'%(table_name1, (t2-t1))
                
                #for the second table
                t1 = time.time()
                insert_stmt = ("""copy %s from '%s/persons.csv' """
                               """delimiters ',' csv header"""%(table_name2, location))
                result = self.dbcon_obj.cursor.execute(insert_stmt)
                self.dbcon_obj.connection.commit()
                t2 = time.time()
                print 'Time taken to copy %s -- %s'%(table_name2, (t2-t1))
                
            except Exception, e:
                print e
        else:
           print 'Table(s) do not exist.'

        #close the new database connection
        self.dbcon_obj.close_connection()
        
        #assign old database name
        self.dbcon_obj.database_name = databasename

        
    #delete unwanted records
    def delete_records(self, databasename, table1, table2, column_name, index, interval_list):
        """
        This method is used to delete selected rows between the interval 
        from the table in the database.

        Input:
        Database configuration object, class name and selection criteria.

        Output:
        Returns the rows that satisfy the selection criteria
        """
        fin_flag = None
        db_name = databasename
        
        #open a new connection to the required database
        db_str = db_name + '_' + str(index+1)
        #print db_str
        self.dbcon_obj.database_name = db_str

        #create a new database connection
        self.dbcon_obj.new_connection()
        
        #check if table exists and then if columns exists
        tab_flag1 = self.dbcon_obj.check_if_table_exists(table1)
        tab_flag2 = self.dbcon_obj.check_if_table_exists(table2)
        
        if tab_flag1 == tab_flag2:
            fin_flag = True
        else:
            fin_flag = False

        #declare the interval
        if index == 0:
            low = 1
            high = interval_list[index]
        else:
            low = interval_list[index-1] + 1
            high = interval_list[index]
        #get the rows from households table
        sql_string1 = "DELETE FROM %s WHERE %s NOT BETWEEN %s AND %s"%(table1, column_name, low, high)
        #sql_string2 = "DELETE FROM %s WHERE %s NOT BETWEEN %s AND %s"%(table2, column_name, low, high)
        
        if fin_flag:
            try:
                t1 = time.time()
                self.dbcon_obj.cursor.execute(sql_string1)
                self.dbcon_obj.connection.commit()
    
                self.dbcon_obj.cursor.execute(sql_string2)
                self.dbcon_obj.connection.commit()
                t2 = time.time()
                print 'Total time taken to delete the unwanted rows %s'%(t2-t1)
            except Exception, e:
                print e
        else:
            print 'Table(s) do not exist.'
            
        #close the new database connection
        self.dbcon_obj.close_connection()
        
        #assign old database name
        self.dbcon_obj.database_name = databasename
        

    def collate_full_results(self, parts):
        """
        This method calls the collate data method.
        Prior to that it deletes the indexes on the tables. 
        When all the data is put together the indexes are created again.
        
        Input:
        Number of parts
        
        Output:
        Data from all databases is saved in the parent database
        """

        output_tables = ['child_dependency_r', 'daily_school_status_r', 
                        'daily_work_status_r', 'households_vehicles_count_r', 
                        'schedule_ltrec_r', 'schedule_r', 
                        'trips_r', 'vehicles_r', 
                        'workers_r', 'schedule_childreninctravelrec_r', 
                        'schedule_cleanfixedactivityschedule_r',  
                        'schedule_dailyallocrec_r', 'schedule_final_r', 'schedule_inctravelrec_r']
                        	 
        index_columns = ''
        t1 = time.time()
        #create a new database connection object
        self.new_qb_obj = QueryBrowser(self.database_config_object)
    	
        #open a new object connection
        self.new_qb_obj.dbcon_obj.new_connection()
	
        for table_name in output_tables:
            #print '\n', table_name
	    print 'Getting index columns for table - %s' %(table_name)
            index_columns = self.new_qb_obj.get_index_columns(table_name)
	    print '\tIndex columns for table -', index_columns
            #print '\t', index_columns
            print '\tdelete the index'
            self.new_qb_obj.delete_index(table_name)
            for i in range(parts):
                databasename = '%s_%s'%(self.database_name, i+1)
                #print '\t', databasename
                self.collate_results(databasename, table_name)
            print '\tcreate the index again'
            self.new_qb_obj.create_index(table_name, index_columns)
	        
        #close the connection
        self.new_qb_obj.dbcon_obj.close_connection()
	
        t2 = time.time()
        print 'Total time taken to delete and create all the indexes --> %s'%(t2-t1)


    #new method to check for sequences and the create the sql_string
    def check_sequences(self, table_name):
        """
        This method calls the find sequence method of
        query browser and checks for sequences. it create the sql string 
        based on the output of the method
        
        Input:
        Table name
        
        Output:
        SQL string and column name
        """
	print '-- Starting to check sequences for - ', table_name
        sql_string = ''
        col_name = ''
        #open a new connection
        self.qb_obj.dbcon_obj.new_connection()
        
        #find the sequences present in the table
        seq_list, ser_column = self.qb_obj.find_sequence(table_name)

        if not seq_list:
            #seq_list is empty. no sequence present
            sql_string = "SELECT * FROM %s"%table_name
        else:
            #sequence list is not empty. create sql string
	    print table_name, '---<<<Inside else for the following table_name'
	    print self.qb_obj.dbcon_obj.connection
	    print self.qb_obj.dbcon_obj.cursor
		
            cols = self.qb_obj.dbcon_obj.get_column_list(table_name)
            col_str = ''
            col_count = 0
            for i in cols:
                if i not in ser_column:
                    if col_count < (len(cols)-(len(ser_column)+1)):
                        col_str = col_str + i + ', '
                        col_count = col_count + 1
                    else:
                        col_str = col_str + i
            sql_string = "SELECT " + col_str + " FROM %s"%table_name
        
        #close connection
        self.qb_obj.dbcon_obj.close_connection()

        return sql_string, ser_column
        
        
    #collate the data from all the output table
    def collate_results(self, databasename, table_name):
        """
        This method collate the results from the output tables
        
        Input:
        Database configuration object and number of parts
        
        Output:
        All output tables merge data into main database's output tables
        """
	print '-- Starting to collate results for db - %s and tablename - %s' %(databasename, table_name)
        sql_string, ser_column = self.check_sequences(table_name)
	print sql_string
        #run a loop and open a connection to individual databases
        #execute select query and save the results
        #sql_string = "select * from %s"%table_name

        old_db_name = self.database_config_object.database_name

        
        t1 = time.time()
	#self.database_config_object.database_name = databasename
	self.dbcon_obj.database_name = databasename		
	self.dbcon_obj.new_connection()
	print '-- database connection after starting to collate results', self.dbcon_obj.connection

        try:
            self.dbcon_obj.cursor.execute(sql_string)
            result = self.dbcon_obj.cursor.fetchall()
	    #print 'RESULT', result, self.database_config_object.database_name, self.dbcon_obj.connection
        except Exception, e:
            print 'Select query failed.'
            print e
            
        t2 = time.time()
        print 'Total time taken to retrieve records %s'%(t2-t1)
       	self.dbcon_obj.close_connection()
        
	self.dbcon_obj.database_name = old_db_name

	self.dbcon_obj.new_connection()


        #self.new_db_obj = DataBaseConnection(self.database_config_object)
        #self.new_db_obj.new_connection()
        
        fin_flag = None
        #check if table exists and then if columns exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        
        t1 = time.time()
        if tab_flag:
            cols = self.dbcon_obj.get_column_list(table_name)
            col_str = ''
            col_count = 0
            for i in cols:
                if i not in ser_column:
                    if col_count < (len(cols)-(len(ser_column)+1)):
                        col_str = col_str + i + ', '
                        col_count = col_count + 1
                    else:
                        col_str = col_str + i

            arr_str = [tuple(each) for each in result]
            arr_str = str(arr_str)[1:-1]
            arr_str = arr_str.replace('L', '')
            
	    #print 'EMPTY STRING', arr_str
	    print '-- This is where inserting needs to happen'
            sql_string = 'insert into %s (%s) values %s'%(table_name, col_str, arr_str)
            if len(arr_str) > 0:
                try:
                    self.dbcon_obj.cursor.execute(sql_string)
                    self.dbcon_obj.connection.commit()
                except Exception, e:
                    print e
        
            t2 = time.time()
            print 'Total time taken to insert %s'%(t2-t1)
            
        else:
            print 'Table(s) do not belong to the database.'
            #close the new database connection
        
        #close the new database connection
        self.dbcon_obj.close_connection()

             
    #partition the data in the newly created tables
    def partition_data(self, parts, table_list, 
			column_name, location=None):
        """
        This method runs a loop and divides all the data
        
        Input:
        Number of partitions
        
        Output:
        
        """
        print 'Start'

        #declare the lists
        house_rows = []
        person_rows = []
        table_rows = []
        
        #create the dummy databases
        res = self.dummy_db(self.dbcon_obj.database_name, parts)
        print '---> dummy databases created'
        
        #open a connection to current database and get the table information
        self.dbcon_obj.new_connection()
        print '----> new connection created'
        
        #call the get table info to fetch all data and save it
        self.get_table_info()
        print '---> table info fetched'
        
        #get the interval data
        interval_list = self.divide_rows(parts)
        print '---> divide rows complete'
        
        #close the connection to the database
        self.dbcon_obj.close_connection()
        print '---> connection closed'
        
        #create new tables in the databases
        self.create_partitions(self.database_name, parts)
        print '---> partitions created'
        
        """
        To divide the data into parts and distribute it in the new databases, 
        use the functions in the pairs as mentioned
        
        1) get_interval_rows() and insert_data()
                            OR
        2) copy_data() and delete_records()
        for the copy_data() method the households and persons table have to be 
        exported as a csv file and the location should be assigned where the 
        file is located
        """
        
        #run a loop to copy data and delete the rows
        print 'Loop starts.'
        t1 = time.time()
        for index in range(parts):
            #run a loop for every table in the table list
	    print 'Table list', table_list
	    #raw_input()
            for each_table in table_list:
                #select the required data
                table_rows = self.get_interval_rows(self.database_name, each_table, column_name, interval_list, index)
                print '---> Data selected based on the houseid'
                
                #insert the selected data into the required tables
                insert = self.insert_data(self.database_name, table_rows, each_table, index)
                print '---> Data inserted in the respective table'
            
            #copy all the data into the new data
            #self.copy_data(self.database_name, table1, table2, index, location)
        
            #delete the unwanted rows
            #self.delete_records(self.database_name, table1, table2, 
 	    #	                 column_name, index, interval_list)
           
        print 'Loop ended'
        t2 = time.time()
        print 'Total time taken by main function %s'%(t2-t1)
        
        #return interval_list
        print 'Done'
        
                        
#unit test to test the code
import unittest

#define a class for testing
class TestDivideData(unittest.TestCase):
    #only initialize objects here
    def setUp(self):
        self.protocol = 'postgres'		
        self.user_name = 'postgres'
        self.password = '1234'
        self.host_name = 'localhost'
        self.database_name = 'mag_zone'

    
    def testdividedata(self):
        """ definitions for config class and create objects """
        dbconf = DataBaseConfiguration(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        newobject = DivideData(dbconf)
        
        print 'Start program'
        
        """ Call main function """
        parts = 3
        location = '/home/namrata/Documents/threads'
        table1 = 'households'
        table2 = 'persons'
        column_name = 'houseid'
        index = 0
        count = 0
        print '\t Parts are %s and Database name is %s'%(parts, self.database_name)
        print '\t Location is %s'%location
        print '\t Table 1 is %s, Table 2 is %s and Column name is %s'%(table1, table2,column_name)
        #main function to divide and distribute the data
        table_list = ['persons', 'households', 'schedule_r']
        #table_list = ['schedule_r']
        newobject.partition_data(parts, table_list, column_name)

        #table_name = 'child_dependency_r'
        #dbname = 'mag_zone'
        
        #open connection
        #newobject.dbcon_obj.new_connection()
        #newobject.collate_results(dbname, table_name)
        #close connection
        #newobject.dbcon_obj.close_connection()
        #newobject.collate_full_results(parts)
        """
        #   MAG_ZONE_2
        newobject.dbcon_obj.database_name = 'mag_zone_2'
        #open connection
        newobject.dbcon_obj.new_connection()
        newobject.collate_results(dbname, table_name)
        #close connection
        newobject.dbcon_obj.close_connection()
        
        #   MAG_ZONE_3
        newobject.dbcon_obj.database_name = 'mag_zone_3'
        #open connection
        newobject.dbcon_obj.new_connection()
        newobject.collate_results(dbname, table_name)
        #close connection
        newobject.dbcon_obj.close_connection()
        
        #   MAG_ZONE_4
        newobject.dbcon_obj.database_name = 'mag_zone_4'
        #open connection
        newobject.dbcon_obj.new_connection()
        newobject.collate_results(dbname, table_name)
        #close connection
        newobject.dbcon_obj.close_connection()
        """
        print 'End of program'
        

if __name__ == '__main__':
    unittest.main()
