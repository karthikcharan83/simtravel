# sample program for metaclass

import sys
import os
import exceptions
import sqlite3
import psycopg2 as dbapi2
#import tables as t
import time
from psycopg2 import extensions
from new import classobj
from inspect import getmembers
#from database_configuration import DataBaseConfiguration
#from cursor_database_connection import DataBaseConnection
from openamos.core.database_management.database_configuration import DataBaseConfiguration
from openamos.core.database_management.cursor_database_connection import DataBaseConnection


""" below class method will create a class on the fly """

# this class will be used to create a class at runtime


class create_class(object):

    def mkClass(self, name, k):
        class bah(object):
            pass
        bah.__name__ = name
        # print 'bah is %s and k is %s'%(bah, k)
        for n in k:
            setattr(bah, n, k[n])
        return bah


""" temp class for getting table names and column names """
# temporary class for database connection and database related work


class temp_class(object):

    def __init__(self):
        db_con = DataBaseConfiguration(
            'postgres', 'postgres', '1234', 'localhost', 'postgres')
        self.db_con = db_con
        dbcon_obj = DataBaseConnection(db_con)
        self.dbcon_obj = dbcon_obj

    def return_tab(self):
        tab_list = self.dbcon_obj.get_table_list()
        return tab_list


# current code will create a class for the table 'Persons'
# create object of class temp_class
aa = temp_class()

# open new connection to database to get the table names and columns
aa.dbcon_obj.new_connection()
tab_list = aa.return_tab()
for each in tab_list:
    if (each == 'persons'):
        table_name = each

# get the columns for the table, append a zero '0' to each column and save
# in a list
cols_list = aa.dbcon_obj.get_column_list(table_name)
new_col_list = []
for each in cols_list:
    new_col_list.append(each + ':' + '0')

# close database connection
aa.dbcon_obj.close_connection()


""" data processing
Convert the column list into dictionary.
pass the dictionary and table name to create class method to create new class by table name
"""

# convert the column list into a dictionary
new_dictionary = dict([x.split(':') for x in new_col_list])

# create object of create class and return the object
temp_obj = create_class()

# call the method of create class to create new class and pass the column
# list as argument
fin_obj = temp_obj.mkClass(table_name, new_dictionary)


""" store the class members which are the columns in a separate list
convert the columns from tuples to string
TODO: convert the columns from tuple to Int32 or Float
"""

# get the class members of the class
some_list = getmembers(fin_obj)
class_members = []

for each_mem in some_list:
    tmp = each_mem[1]
    if(tmp == '0'):
        class_members.append(str(each_mem).strip('[]'))

print '\nprinting the columns'
for every_mem in class_members:
    print every_mem
