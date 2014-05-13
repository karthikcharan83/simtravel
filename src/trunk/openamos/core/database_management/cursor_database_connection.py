#main class. this class will be used to define the database connection.
#it will create/drop database, schema and tables


#include all the import
import traceback
import sys
import os
import exceptions
import sqlite3
import psycopg2 as dbapi2
import sqlalchemy
from psycopg2 import extensions
from sqlalchemy.schema import MetaData, Column, Table
from sqlalchemy.types import Integer, SmallInteger, \
                             Numeric, Float, \
                             VARCHAR, String, CLOB, Text,\
                             Boolean, DateTime

from database_configuration import DataBaseConfiguration


#class to define the database connection along with other functions
class DataBaseConnection(object):
    """
    This is the class for database connectivity and functionality.
    The class will also perform various other functions on the database for
    data definition and data manipulation.

    Input: Database configuration object
    """

    def __init__(self, dbconfig):
        if not isinstance(dbconfig, DataBaseConfiguration):
            raise DatabaseConfigurationError, """the dbconfig input is not a valid """\
                """DatabaseConfiguration object."""

        #create the database object here
        self.protocol = dbconfig.protocol
        self.user_name = dbconfig.user_name
        self.password = dbconfig.password
        self.host_name = dbconfig.host_name
        self.database_name = dbconfig.database_name


    #checks if the database engine is installed
    def check_if_database_engine_exits(self):
        """
        This method checks if the database engine has been installed.
        The types of databases checked are as below. The installed
        engines are stored in an array.

        Input:
        Protocol/database type of the database configuration object

        Output:
        Return the database engine if it exists else raises exception.
        """

        database_engine = None
        try:
            import psycopg2
            database_engine = 'postgres'
        except:
            pass

        """
        After storing the installed engies, check if the protocol in
        the database configuration object is present in the array
        """
        db_engine = self.protocol

        if db_engine == database_engine:
            return db_engine
        else:
            raise Exception('Required database is not installed')
            sys.exit()


    #checks if the database exists
    def check_if_database_exists(self):
        """
        This method opens a raw connection to the postgres database
        and checks if the database name passed by the database
        configuration object already exists or not. If the database
        does not exists the database is created by another method.

        Input:
        Database name of the database configuration object.

        Output:
        Returns a boolean value indicating the database exists or not.
        """

        """
        Before checking for database check if the database engine
        is installed or not. If database is not installed then exit.
        """
        installed_db = self.check_if_database_engine_exits()
        if installed_db:
            print 'Database %s is installed.'%installed_db
        else:
            print 'Database is not installed. Cannot proceed furthur.'
            print 'Exiting the program'
            sys.exit()

        """
        Create a connection to the database.
        """

        if self.protocol == 'postgres':
            try:
                #create a connection

                self.connection = dbapi2.connect("host=%s user=%s password=%s port=5432"
                                                 %(self.host_name, self.user_name, self.password))

                #create a cursor
                self.cursor = self.connection.cursor()
                self.cursor.execute("select datname from pg_database")

                dbs = [db[0] for db in self.cursor.fetchall()]
                database_flag = self.database_name in dbs


                #set a flag that indicates the existence of the database.
                if database_flag:
                    print 'Database %s exists'%self.database_name
                    #dispose the engine and close the raw connection
                    self.cursor.close()
                    self.connection.close()
                    return 1
                else:
                    #dispose the engine and close the raw connection
                    self.cursor.close()
                    self.connection.close()
                    print 'Database %s does not exist.'%self.database_name
                    return 0
            except Exception, e:
                print e


    #this function creates a new database
    def create_database(self, new_database):
        """
        This method creates a new database by the database name passed
        in the database configuration object.

        Input:
        Database name

        Output:
        Database created if it does not exists
        """

        db_flag = self.check_if_database_exists()
        print 'new database is %s'%new_database
        #db_flag = 0
        if not db_flag:
        #since the database does not exist we create a new database.
        #before creating the new database check the protocol.
            try:
                self.connection = dbapi2.connect("host=%s user=%s password=%s port=5432"%(self.host_name, self.user_name, self.password))
                self.connection.set_isolation_level(0)
                self.cursor = self.connection.cursor()
                self.cursor.execute("create database %s encoding = 'utf8'"%new_database)
                print 'Database %s created'%new_database
                self.cursor.close()
                self.connection.close()
                return 1
            except Exception, e:
                print e
                return 0
                #raise Exception('Error while creating a new database')
        else:
            print 'Database exists. No need to create a new database'
            return 1


    #drops a database
    def drop_database(self):
        """
        This method is used to drop the database.

        Input:
        Database name

        Output:
        Database dropped and boolean returned
        """

        #Before dropping the database check if the database exists or not
        db_flag = self.check_if_database_exists()
        if db_flag:
            try:
                self.connection = dbapi2.connect("host=%s user=%s password=%s port=5432"%(self.host_name, self.user_name, self.password))
                self.connection.set_isolation_level(0)
                self.cursor = self.connection.cursor()
                self.cursor.execute("drop database %s"%self.database_name)
                print 'Database dropped'
            except:
                raise Exception('Error while deleting a database')
        else:
            print 'Database does not exists. Cannot drop database.'


    #get the list of databases
    def get_list_databases(self):
        """
        This method is used to get the list of all the databases for the
        database engine

        Input:
        Database configuration object

        Output:
        List of databases present.
        """
        installed_db = self.check_if_database_engine_exits()
        if installed_db:
            print 'Database %s is installed.'%installed_db
        else:
            print 'Database is not installed. Cannot proceed furthur.'
            print 'Exiting the program'
            sys.exit()


        if self.protocol is 'postgres':
            try:
                #create a connection
                self.connection = dbapi2.connect("host=%s user=%s password=%s port=5432"%(self.host_name, self.user_name, self.password))

                #create a cursor
                self.cursor = self.connection.cursor()
                self.cursor.execute("select datname from pg_database")

                dbs = [db[0] for db in self.cursor.fetchall()]
                self.cursor.close()
                self.connection.close()
                return dbs
            except Exception, e:
                self.cursor.close()
                self.connection.close()
                print e


    #create a new connection with the database name
    def new_connection(self):
        """
        This method creates a new connection to the database with the databse name.
        This method is used to create a new connection that will be furthur used
        for data manipulation.

        Input:
        Database configuration object

        Output:
        New connection created
        """

        #before connecting to the database check if the database exists
        db_flag = self.check_if_database_exists()
        if db_flag:
            #create a connection and try to establish a session with the database
            try:
                self.connection = dbapi2.connect("host=%s dbname=%s user=%s password=%s port=5432"
                                                 %(self.host_name, self.database_name,
                                                   self.user_name, self.password))
                self.cursor = self.connection.cursor()
                print 'New connection created.\n'
            except Exception, e:
                print "Exiting the program since database connectivity failed"
                print e
        else:
            print 'Database %s does not exists. Cannot create connection to the database'%self.database_name


    #close the connection
    def close_connection(self):
        """
        This method is used to close the database connection.

        Input:
        Database configuration object

        Output:
        Close the connection
        """
        if self.connection is None:
            print 'Connection is None. Cannot close the connection.'
        else:
            try:
                print "Closing the database connection."
                self.cursor.close()
                self.connection.close()
                if self.connection.closed:
                    print 'Connection to database closed.\n'
                else:
                    print 'Connection to database not closed.\n'
            except:
                print "Error while closing the database connection. Exiting the program."
                self.cursor = None
                self.connection = None
                sys.exit()


    #check if table exists
    def check_if_table_exists(self, table_name):
        """
        This method checks if the table exists in the database.

        Input:
        Table name

        Output:
        Return boolean indicating the table exists or not
        """
        self.table_name = table_name
        try:
            self.cursor.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES where table_schema = 'public'")
            tables = self.cursor.fetchall()
            tbs = [tb[0] for tb in tables]
            #print tbs
            table_exists = self.table_name in tbs
            return table_exists
        except Exception, e:
            print 'Error when checking for existing tables'
            print e
            traceback.print_exc(file=sys.stdout)
            raise Exception


    #get the list of tables from the database
    def get_table_list(self):
        """
        This method is used to fetch the list of all tables in the database.

        Input:
        Database configuration object

        Output:
        List of the tables in the database.
        """
        try:
            self.cursor.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES where table_schema = 'public'")
            tables = self.cursor.fetchall()
            tbs = [tb[0] for tb in tables]
            return tbs
        except Exception, e:
            print 'Error while fetching the tables from the database'
            print e


    #get the list of tables from the database
    def get_column_list(self, table_name):
        """
        This method is used to fetch the list of all tables in the database.

        Input:
        Database configuration object

        Output:
        List of the tables in the database.
        """
        self.table_name = table_name
        #before returning the columns check if the table exists
        #self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        if table_flag:
            try:
                self.cursor.execute("select column_name from information_schema.columns where table_name = '%s'"%table_name)
                columns = self.cursor.fetchall()
                cols = [cl[0] for cl in columns]
                return cols
            except Exception, e:
                print 'Error while fetching the columns from the table'
                print e
        else:
            print 'Table %s does not exist. Cannot get the column list'%table_name


    #creates a new table
    def create_table(self, table_name, columns, ctypes, cdefaults, keys):
        """
        This method is used to create new table in the database.

        Input:
        Database configuration object and table name

        Output:
        New table created
        table_name, columns, ctypes, keys
        """
        #before creating a new table check if that table exists
        self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        const_str = 'constraint ' + table_name + '_pkey primary key'
        if table_flag:
            print 'Table already exists in the database. No need to create a new table'
        else:
            #create a new table since it does not exist
            print 'Table does not exist. Create a new table'
            column = ''
            for col, ctype, cdefault in zip(columns, ctypes, cdefaults):
                if cdefault is None:
                    column = column + col + ' ' + ctype + ', '
                elif cdefault[:7] == 'nextval':
                    column = column + col + ' ' + 'serial NOT NULL' + ', '
                else:
                    column = column + col + ' ' + ctype + ' DEFAULT ' + cdefault + ', '
            pkey = ''
            for col, key in zip(columns, keys):
                if key == '1' or key == 1:
                    pkey = pkey + col + ','

            if pkey == "":
                column = column[0:-2]
                sql_string = 'create table %s ( %s )'%(self.table_name, column)
            else:
                pkey = const_str + '(' + pkey[0:-1] + ')'
                sql_string = 'create table %s ( %s %s )'%(self.table_name, column, pkey)
            #print sql_string
            try:
                self.cursor.execute(sql_string)
                self.connection.commit()
                print "Table '%s' created"%self.table_name
            except Exception, e:
                print 'Error while creating the table %s'%self.table_name
                print e


    #drop the table
    def drop_table(self, table_name):
        """
        This method is used to drop the table from the database

        Input:
        Database configuration object and table name

        Output:
        Table is dropped from the database
        """

        #before dropping the table check if the table exists
        self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        if table_flag:
            #table exists and hence can be dropped
            print 'Table exists in the database.'
            self.cursor.execute("drop table %s"%self.table_name)
            self.connection.commit()
        else:
            print 'Table does not exist in the database. Cannot the drop the table'


    ##################### adding 2 new functions #########################
    #get the list of tables from the database
    def get_column_types(self, table_name):
        """
        This method is used to data types of the columns in table.

        Input:
        Database configuration object and table name

        Output:
        List of the column data types in the database.
        """
        self.table_name = table_name
        #before returning the column types check if the table exists
        self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        if table_flag:
            try:
                self.cursor.execute("select data_type from INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'"%table_name)
                columns = self.cursor.fetchall()
                cols = [cl[0] for cl in columns]
                return cols
            except Exception, e:
                print 'Error while fetching the data types of columns from the table'
                print e
        else:
            print 'Table %s does not exist. Cannot get the column information'%table_name


    #get the list of tables from the database
    def get_column_defaults(self, table_name):
        """
        This method is used to data types of the columns in table.

        Input:
        Database configuration object and table name

        Output:
        List of the column data types in the database.
        """
        self.table_name = table_name
        #before returning the column types check if the table exists
        self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        if table_flag:
            try:
                self.cursor.execute("select column_default from INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'"%table_name)
                columns = self.cursor.fetchall()
                colsDef = [cl[0] for cl in columns]
                return colsDef
            except Exception, e:
                print 'Error while fetching the data types of columns from the table'
                print e
        else:
            print 'Table %s does not exist. Cannot get the column information'%table_name


    #get the keys from the tables
    def get_table_keys(self, table_name):
        """
        This method is used to get the keys of a table.

        Input:
        Database configuration object and table name

        Output:
        List of keys in a table.
        """
        self.table_name = table_name
        #before returning the column types check if the table exists
        self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        sql_str = "SELECT KU.COLUMN_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS \
                    AS TC INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KU \
                    ON TC.CONSTRAINT_TYPE = \'PRIMARY KEY\' AND \
                    TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME \
                    WHERE TC.TABLE_NAME = \'%s\' ORDER BY KU.TABLE_NAME, KU.ORDINAL_POSITION"%table_name

        if table_flag:
            try:
                self.cursor.execute(sql_str)
                keys = self.cursor.fetchall()
                cols = [cl[0] for cl in keys]
                return cols
            except Exception, e:
                print 'Error while getting the keys of the table'
                print e
        else:
            print 'Table %s does not exist. Cannot get the table keys'%table_name

    ##################### adding 2 new functions #########################

    #temp function prints the values of the database configuration object
    def temp_function(self):
        """
        This is a test function.
        It displays the values of the database configuration object

        Input:
        Database configuration object

        Output:
        Display the object details
        """

        print 'protocol is %s'%self.protocol
        print 'host name is %s'%self.host_name
        print 'user name is %s'%self.user_name
        print 'password is %s'%self.password
        print 'database name is %s'%self.database_name
        print 'cursor is %s'%self.cursor
        print 'connection is %s\n'%self.connection



#unit test to test the code
import unittest

#define a class for testing
class TestDataBaseConnection(unittest.TestCase):
        #only initialize objects here
    def setUp(self):
        self.protocol = 'postgres'
        self.user_name = 'postgres'
        self.password = '1234'
        self.host_name = 'localhost'
        self.database_name = 'postgres'

    def testDB(self):
        print 'test'
        #db_obj = DataBaseConnection(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        dbconf = DataBaseConfiguration(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        db_obj = DataBaseConnection(dbconf)
        print db_obj
        #temp = db_obj.get_list_databases()
        #print temp
        db_obj.new_connection()
        #tab = 'asu'
        #cls = db_obj.get_column_types(tab)
        #print cls
        #keys = db_obj.get_table_keys(tab)
        #print keys
        #db = 'mag_zone_0'
        #res = db_obj.create_database(db)
        #db_obj.check_if_database_exists()
        #print db_obj.connection
        #print res
        table_name = 'abc2'
        columns = ['aa', 'bb', 'cc', 'dd']
        ctypes = ['integer', 'integer', 'integer', 'integer']
        keys = ['0', '0', '0', '0']
        #print table_name, columns, ctypes, keys
        #db_obj.create_table(table_name, columns, ctypes, keys)
        db_obj.close_connection()


if __name__ == '__main__':
    unittest.main()
