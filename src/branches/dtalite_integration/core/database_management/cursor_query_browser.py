# main class. this class will be used to define the database connection.
# it will create/drop database, schema and tables


# include all the import
import sys
import os
import exceptions
import time
import sqlalchemy
import psycopg2 as dbapi2
import numpy as na
import re
from cursor_database_connection import DataBaseConnection
from psycopg2 import extensions
from sqlalchemy.types import Integer, SmallInteger, \
    Numeric, Float, \
    VARCHAR, String, CLOB, Text,\
    Boolean, DateTime
from numpy import array, ma, savetxt
from database_configuration import DataBaseConfiguration
from openamos.core.data_array import DataArray
from openamos.core.errors import DataError
import pandas.io.sql as sql


class QueryBrowser(object):
    # initialize the class
    #TODO: fix exceptions
    #TODO: clean the dbconn_obj, connection etc.

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
        self.dbcon_obj = DataBaseConnection(dbconfig)
        print 'inside query browser ', self.dbcon_obj

    ########## methods for select query  ##########
    # select all rows from the table
    def select_all_from_table(self, table_name, cols=None):
        """
     This method is used to fetch all rows from the table specified.
     Input:
     Name of the table
     
     Output:
     Returns all the rows in the table
     """
        colsStr = ""
        if cols == None:
            cols = self.dbcon_obj.get_column_list(table_name)
        for i in cols:
            colsStr += "%s," % (i)
        colsStr = colsStr[:-1]

        # check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            # print 'Table %s exists.'%table_name
            try:
                sql_string = (
                    "SELECT %s FROM %s" % (colsStr, table_name))
                result = sql.frame_query(sql_string, self.dbcon_obj.connection)
                data = DataArray(result,  cols)
                return data
            except Exception, e:
                raise Exception, '\tError while retreiving the data from the table: %s'%e
                print e
        else:
            print '\tTable %s does not exist.' % table_name

    # select rows based on a selection criteria
    def fetch_selected_rows(self, table_name, column_name, value):
        """
     This method is used to fetch selected rows fom the table in the database.

     Input:
     Database table name and selection criteria specified using column name and value.

     Output:
     Returns the rows that satisfy the selection criteria
     """
        fin_flag = None
        # check if table exists and then if columns exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            # check for columns
            cols = self.dbcon_obj.get_column_list(table_name)
            if column_name in cols:
                fin_flag = True
            else:
                fin_flag = False
        else:
            print 'Table %s does not exist.' % table_name

        if fin_flag:
            try:
                sql_string = (
                    "SELECT * FROM %s where %s = '%s'" % (table_name, column_name, value))
                result = sql.frame_query(sql_string, self.dbcon_obj.connection)
                data = DataArray(result, cols)
                return data
            except Exception, e:
                print 'Error retrieving the information. Query failed.\n'
                print e
        else:
            print 'Column %s does not belong to the table %s' % (column_name, table_name)
            return None

    def select_join(self, db_dict, column_names, table_names, max_dict=None,
                    spatialConst_list=None, analysisInterval=None,
                    analysisIntervalFilter=None, analysisIntervalCondition=None,
                    history_info=None,
                    aggregate_variable_dict={},
                    delete_dict={}, 
                    indexCols=None):
        """
     This method is used to select the join of tables and display them.

     Input:
     Database configuration object, table names, columns and values.

     Output:
     Displays the rows based on the join and the selection criterion.
     """
        #print "\nthis is the index-->",  indexCols
        #raw_input()
        # db_dict = {'households': ['urb', 'numchild', 'inclt35k', 'ownhome', 'one', 'drvrcnt', 'houseid'],
        #           'vehicles_r': ['vehtype', 'vehid'],
        #           'households_r': ['numvehs']}
        #columns_names = ['houseid']
        #table_names = ['households', 'households_r', 'vehicles_r']
        #max_dict = {'vehicles_r':['vehid']}

        # Prism Query or or just a Travel Time Query with Vertices
        # ADD APPROPRIATE JOIN/?INNER JOINS

        # print 'Database Dictionary of Table and Columns - ', db_dict
        # print 'Column Names', db_dict
        # raw_input()

        # print
        # print 'db dict', db_dict
        # print
        # print 'max_dict', max_dict

        # initialize the variables
        final_list = []
        table_list = []
        class_list = []
        cols_list = []
        tabs_list = []
        #col_name = column_name
        final_col_list = db_dict.values()
        table_list = db_dict.keys()

        # print 'table list - ', table_list
        # raw_input()

        table_flag = None
        all_tables = table_list + table_names

        all_tables = list(set(all_tables))

        # print 'table_list', table_list
        # print 'column_names', column_names
        # print 'MAX DICT', max_dict

        # check if the tables exist in the database.
        for each_tab in all_tables:
            # print 'Checking for table name - ', each_tab
            if column_names[each_tab] == ['']:
                # print 'before', db_dict, column_names, table_names
                db_dict.pop(each_tab)
                column_names.pop(each_tab)
                table_list.remove(each_tab)
                table_names.remove(each_tab)
                # print 'after', db_dict, column_names, table_names
                continue
            # print "Checking if table - ", each_tab, " exists"
            table_flag = self.dbcon_obj.check_if_table_exists(each_tab)
            if table_flag:
                pass
            else:
                print 'Table %s does not exist in the database. Exiting the funtion.' % each_tab
                return 0

        # similarly check if the table in the list exists
        num_tab = len(list(set(table_list) & set(table_names)))
        if num_tab <= len(table_list):
            # print 'Tables exist'
            pass
        else:
            # print 'Tables do not exists'
            return None

        # check for the columns passed in the dictionary
        tables = db_dict.keys()
        tables.sort()
        for i in tables:
            clist = self.dbcon_obj.get_column_list(i.lower())
            list1 = db_dict[i]
            chk_list = len(list(set(list1) & set(clist)))

            if chk_list == len(list1):
                cols = db_dict[i]
                cols.sort()
                for j in cols:
                    # print '\tColumn - ', j
                    new_str = i.lower() + '.' + j.lower()
                    final_list.append(new_str)
                cols_list = cols_list + cols
                # print cols_list, 'initial list without spatial const'
            else:
                print (
                    'Column passed in the dictionary does not exist in the table - ')
                print 'Column List in the Table - ', clist
                print (set(list1) & set(clist))
                print 'Actual List of Columns requested from table - ', list1

                return None
        # print 'final_list is %s'%final_list

        # print 'FINAL LIST', final_list
        # print 'TABLE NAMES', table_names
        # print 'db dict', db_dict
        # print 'TABLE LIST', table_list

        # Generating the left join statements
        mainTable = table_names[0]
        # print 'mainTable ----> ', mainTable

        primCols = []
        for i in column_names:
            primCols += column_names[i]
        primCols = list(set(primCols))

        # print primCols, 'PRIMARY COLS'

        joinStrList = []
        table_list.remove(mainTable)
        for table in table_list:
            joinCondition = ''
            for col in column_names[table]:
                joinCondition = (joinCondition
                                 + ' %s.%s=%s.%s ' % (mainTable, col,
                                                      table, col)
                                 + 'and')

            joinCondition = joinCondition[:-3]
            joinStr = ' left join %s on (%s)' % (table, joinCondition)
            joinStrList.append(joinStr)

        # print 'JOIN STRING LIST', joinStrList

        # check the max flag

        if max_dict is not None:
            max_flag = 1
            max_table = max_dict.keys()
            max_column = max_dict.values()[0][0]
            # print max_column, max_table
            # for each in max_dict.values():
            #    max_column = each[0]
        else:
            max_flag = 0

        # Index of the table containing the max dict var
        # as it stands only querying for one count variable is
        # provided
        # print max_dict
        if max_dict is not None:
            for maxTable in max_dict:
                #print '---max', maxTable, mainTable, 'main---'
                #print 'table list here ------->', table_list
                maxColumn = max_dict[maxTable][0]
                try:
                    if maxTable <> mainTable:
                        index = table_list.index(maxTable)
                        table_list.pop(index)
                    else:
                        index = 0
                except Exception, e:
                    print e
                    continue
                # print 'INDEX--->', index

                # remove the count column from the col list
                if maxTable <> mainTable:
                    countVarStr = '%s.%s' % (maxTable, maxColumn)
                    final_list.remove(countVarStr)
                    cols_list.remove(maxColumn)

                final_list.append('temp_%s.max_%s' % (maxTable, maxColumn))
                cols_list.append('max_%s' % maxColumn)

                final_list.append('%s.%s' % (maxTable, maxColumn))
                cols_list.append('%s' % (maxColumn))

                # print 'NEW FINAL LIST -->', final_list

                # left join for the count variable
                joinStr = ''

                # grouping string
                grpStr = ''
                joinCondition = ''

                # print 'column_names of max TABLE ----->', column_names
                for i in column_names[maxTable]:
                    # print 'createing join string for column name - ', i
                    grpStr = grpStr + '%s,' % (i)
                    joinCondition = (joinCondition
                                     + ' temp_%s.%s=%s.%s ' % (maxTable, i,
                                                               mainTable, i)
                                     + 'and')
                grpStr = grpStr[:-1]
                joinCondition = joinCondition[:-3]

                # combine left join along with the count variable/max condition
                if maxTable <> mainTable:
                    mJoinStr = joinStrList.pop(index)
                    mJoinStrIncMaxConditionVar = (mJoinStr[:-1] +
                                                  'and %s.%s=temp_%s.max_%s)'
                                                  % (maxTable, maxColumn, maxTable, maxColumn))
                else:
                    mJoinStrIncMaxConditionVar = ''

                joinStrList.append(""" left join (select %s, max(%s) as max_%s from """
                                   """%s group by %s) as temp_%s on (%s) """ % (grpStr, maxColumn,
                                                                                maxColumn, maxTable, grpStr,
                                                                                maxTable, joinCondition)
                                   + mJoinStrIncMaxConditionVar)
            # print 'LEFT JOIN MAX COL LIST--->', joinStrList
        """
        # separate all the columns from the lists
        new_keys = db_dict.keys()
        for i in new_keys:
            cols = db_dict[i]
            cols.sort()
            cols_list = cols_list + cols
        """

        # Add history information

        if history_info is not None:
            histVarAggConditions = history_info.historyVarAggConditions
            histAggVar = history_info.historyAggVar
            histTable = history_info.tableName
            """

            histTempTableName = "history_temp"

            summationStr = ""
            selectAggStr = ""
            for histVar in histVarAggConditions:
                conditions = histVarAggConditions[histVar]
                conditionsStr = ""

                for j in conditions:
                    conditionsStr += " %s and" %(j)
                conditionsStr = conditionsStr[:-3]

                selectVarStr = "sum(%s) as %s" %(histAggVar, histVar)

                summationStr += " sum(case when (%s) then %s end) as %s, " %(conditionsStr, histAggVar, histVar)

                final_list.append("%s.%s" %(histTempTableName, histVar))
                cols_list.append(histVar)

            summationStr = summationStr[:-2]
            keyCols = column_names[histTable]


            keyCols.reverse()

            grpStr = ""
            for i in keyCols:
                grpStr += "%s," %(i)
            grpStr = grpStr[:-1]



            selectAggStr = ("(select %s, %s from %s where endtime <= %s group by %s) as %s"
                            %(grpStr, summationStr, histTable, analysisInterval, grpStr, histTempTableName))


            joinCondition = ""
            for i in keyCols:
                joinCondition += " %s.%s = %s.%s and" %(mainTable, i,
                                                        histTempTableName, i)
            joinCondition = joinCondition[:-3]

            leftJoinStr = (" left join %s on (%s)"
                           %(selectAggStr, joinCondition))

            joinStrList.append(leftJoinStr)




            """

            for histVar in histVarAggConditions:
                conditions = histVarAggConditions[histVar]
                conditionsStr = ""
                for j in conditions:
                    conditionsStr += " %s and" % (j)
                conditionsStr = conditionsStr[:-3]

                selectVarStr = "sum(%s) as %s" % (histAggVar, histVar)

                histTempTableName = "history_%s" % (histVar)

                final_list.append("%s.%s" % (histTempTableName, histVar))
                cols_list.append(histVar)

                keyCols = column_names[histTable]

                grpStr = ""
                for i in keyCols:
                    grpStr += "%s," % (i)
                grpStr = grpStr[:-1]

                selectAggStr = ("(select %s,%s from %s where (%s) and endtime <= %s group by %s) as %s "
                                % (grpStr, selectVarStr, histTable, conditionsStr, analysisInterval,
                                   grpStr, histTempTableName))

                # print column_names

                joinCondition = ""
                for i in keyCols:
                    joinCondition += " %s.%s = %s.%s and" % (mainTable, i,
                                                             histTempTableName, i)
                joinCondition = joinCondition[:-3]

                leftJoinStr = (" left join %s on (%s)"
                               % (selectAggStr, joinCondition))

                joinStrList.append(leftJoinStr)

        # Spatial TSP identification
        if len(spatialConst_list) > 0:
            for i in spatialConst_list:
                #print "spatial const",  i
                # if i.countChoices is not None:
                if i.buildTSPrism is True: #countChoices == i.endConstraint.table:
                    # substring for the inner join
                    stTable = i.startConstraint.table
                    #stLocationField = 'st_' + i.startConstraint.locationField
                    stLocationCol = 'stl.%s' % i.startConstraint.locationField
                    #stTimeField = 'st_'+ i.startConstraint.timeField
                    stVEndTimeCol = 'st.%s' % i.startConstraint.timeField
                    stVStTimeCol = 'st.%s' % (i.endConstraint.timeField)
                    # TODO: Make these dynamic entries or properties of the
                    # prism constraints
                    #stActType = 'st.%s' %('activitytype')
                    #stScheduleid = 'st.%s' %('scheduleid')

                    enTable = i.endConstraint.table
                    #enLocationField = 'en_' + i.endConstraint.locationField
                    enLocationCol = 'enl.%s' % i.endConstraint.locationField
                    #enTimeField = 'en_' + i.endConstraint.timeField
                    enVStTimeCol = 'en.%s' % i.endConstraint.timeField
                    enVEndTimeCol = 'en.%s' % i.startConstraint.timeField

                    #enActType = 'en.%s' %('activitytype')
                    #enScheduleid = 'en.%s' %('scheduleid')

                    timeCols = [stVStTimeCol, enVEndTimeCol]

                    table_list.append(stTable)

                    # left join for end location

                    # time cols are part of sptime
                    timeColsNewNames = []
                    for j in timeCols:
                        timeColsNewNames.append(j.replace('.', '_'))

                    timeColsStr = ''
                    for j in range(len(timeCols)):
                        # minimum of the time cols gives the first prism
                        timeColsStr += 'min(%s) %s,' % (
                            timeCols[j], timeColsNewNames[j])

                    timeColsStr = timeColsStr[:-1]

                    spGrpNewNameStr = ''
                    spGrpStr = ''
                    for j in column_names[stTable]:
                        spGrpNewNameStr += 'st.%s %s,' % (j, j)
                        spGrpStr += 'st.%s,' % (j)
                    spGrpNewNameStr = spGrpNewNameStr[:-1]
                    spGrpStr = spGrpStr[:-1]

                    spInnerJoinCondition = ''
                    for j in column_names[stTable]:
                        spInnerJoinCondition += ' %s.%s = %s.%s and' % (
                            'st', j, 'en', j)
                    spInnerJoinCondition = spInnerJoinCondition[:-3]

                    spJoinCondition = ''
                    for j in column_names[stTable]:
                        spJoinCondition += ' %s.%s = %s.%s and' % (
                            'sptime', j, mainTable, j)
                    spJoinCondition = spJoinCondition[:-3]

                    # Left join condition for prism start location
                    stLocJoinCondition = ''
                    stLocCondCols = column_names[stTable]
                    for j in stLocCondCols:
                        stLocJoinCondition += ' %s.%s = %s.%s and ' % (
                            'stl', j, mainTable, j)

                    stLocJoinCondition += 'sptime.st_%s = %s.%s' % (i.endConstraint.timeField, 'stl',
                                                                    i.endConstraint.timeField)
                    # stLocJoinCondition += '%s.%s = %s' %('stl', i.startConstraint.timeField,
                    #                                     analysisInterval)
                    # stLocJoinCondition += ' sptime.st_%s = %s.%s' %(i.startConstraint.timeField,
                    #                                           'stl', i.startConstraint.timeField)

                    final_list.append('stl.%s as st_%s' % (i.startConstraint.locationField,
                                                           i.startConstraint.locationField))
                    cols_list.append('st_%s' % i.startConstraint.locationField)

                    final_list.append('stl.%s as st_%s' % (i.startConstraint.timeField,
                                                           i.startConstraint.timeField))
                    cols_list.append('st_%s' % i.startConstraint.timeField)

                    final_list.append('stl.%s as st_%s' % (i.endConstraint.timeField,
                                                           i.endConstraint.timeField))
                    cols_list.append('st_%s' % i.endConstraint.timeField)

                    # TODO: Make these dynamic entries or properties of the
                    # prism constraints
                    final_list.append('stl.%s as st_%s' %
                                      ('activitytype', 'activitytype'))
                    cols_list.append('st_%s' % 'activitytype')

                    final_list.append('stl.%s as st_%s' %
                                      ('scheduleid', 'scheduleid'))
                    cols_list.append('st_%s' % 'scheduleid')

                    final_list.append(
                        'stl.%s as st_%s' % ('dependentpersonid', 'dependentpersonid'))
                    cols_list.append('st_%s' % 'dependentpersonid')

                    final_list.append('stl.%s as st_%s' %
                                      ('tripcount', 'tripcount'))
                    cols_list.append('st_%s' % 'tripcount')

                    final_list.append(
                        'stl.%s as st_%s' % ('duration', 'duration'))
                    cols_list.append('st_%s' % 'duration')

                    #stLocJoinCondition = stLocJoinCondition[:-3]

                    # Left join condition for prism end location
                    enLocJoinCondition = ''
                    enLocCondCols = column_names[stTable]
                    for j in enLocCondCols:
                        enLocJoinCondition += ' %s.%s = %s.%s and' % (
                            'enl', j, mainTable, j)
                    enLocJoinCondition += ' sptime.en_%s = %s.%s' % (i.startConstraint.timeField,
                                                                     'enl', i.startConstraint.timeField)
                    final_list.append('enl.%s as en_%s' % (i.endConstraint.locationField,
                                                           i.endConstraint.locationField))
                    cols_list.append('en_%s' % i.endConstraint.locationField)

                    final_list.append('enl.%s as en_%s' % (i.endConstraint.timeField,
                                                           i.endConstraint.timeField))
                    cols_list.append('en_%s' % i.endConstraint.timeField)

                    final_list.append('enl.%s as en_%s' % (i.startConstraint.timeField,
                                                           i.startConstraint.timeField))
                    cols_list.append('en_%s' % i.startConstraint.timeField)
                    #enLocJoinCondition = enLocJoinCondition[:-3]

                    # TODO: Make these dynamic entries or properties of the
                    # prism constraints
                    final_list.append('enl.%s as en_%s' %
                                      ('activitytype', 'activitytype'))
                    cols_list.append('en_%s' % 'activitytype')

                    final_list.append('enl.%s as en_%s' %
                                      ('scheduleid', 'scheduleid'))
                    cols_list.append('en_%s' % 'scheduleid')

                    final_list.append(
                        'enl.%s as en_%s' % ('dependentpersonid', 'dependentpersonid'))
                    cols_list.append('en_%s' % 'dependentpersonid')

                    final_list.append('enl.%s as en_%s' %
                                      ('tripcount', 'tripcount'))
                    cols_list.append('en_%s' % 'tripcount')

                    final_list.append(
                        'enl.%s as en_%s' % ('duration', 'duration'))
                    cols_list.append('en_%s' % 'duration')

                    # TSP consistency check
                    # nextepisode_starttime > lastepisode_endtime
                    #consistencyStr = '%s < %s' %(stTimeCol, endTimeCol)

                    # Old Implementation of the condition for mergining
                    # analysisPeriodStr = ('%s=%s and %s>%s'
                    #                     %(stVEndTimeCol, analysisInterval,
                    #                       enVStTimeCol, analysisInterval))

                    analysisPeriodStr = ('%s=%s and %s>%s'
                                         % (stVEndTimeCol, analysisInterval,
                                            enVEndTimeCol, stVEndTimeCol))

                    spatialJoinStr = (""" join (select %s, %s """
                                      """from %s as %s """
                                      """inner join %s as %s """
                                      """on ( %s and %s) group by"""
                                      """ %s) """
                                      """as sptime on (%s)"""
                                      % (spGrpNewNameStr, timeColsStr,
                                         stTable, 'st',
                                         enTable, 'en',
                                         spInnerJoinCondition, analysisPeriodStr,
                                         spGrpStr,
                                         spJoinCondition))
                    # print 'SPATIAL JOIN'
                    # print spatialJoinStr
                    # left join for start location

                    stLocJoinStr = (""" left join %s %s on """
                                    """(%s) """
                                    % (stTable, 'stl', stLocJoinCondition))

                    enLocJoinStr = (""" left join %s %s on """
                                    """(%s) """
                                    % (enTable, 'enl', enLocJoinCondition))

                    joinStrList.insert(0, spatialJoinStr)
                    joinStrList.insert(1, stLocJoinStr)
                    joinStrList.insert(2, enLocJoinStr)

                    joinStrList.append(' where enl.%s > stl.%s ' % (i.endConstraint.timeField,
                                                                    i.endConstraint.timeField))

                    #cols_list += timeColsNewNames

                    # for i in timeColsNewNames:
                    #    final_list.append('sptime.%s' %(i))
                    # Only one time-space prism can be retrieved within a component
                    # there cannot be two TSP's in the same component
                    break

        if analysisIntervalFilter is not None:
            final_list.append('%s.%s as %s_%s' % (analysisIntervalFilter[0], analysisIntervalFilter[1],
                                                  analysisIntervalFilter[0], analysisIntervalFilter[1]))
            cols_list.append(
                '%s_%s' % (analysisIntervalFilter[0], analysisIntervalFilter[1]))

            if len(spatialConst_list) < 1:
                joinStrList.append(' where %s.%s %s %s' % (analysisIntervalFilter[0],
                                                           analysisIntervalFilter[
                                                               1],
                                                           analysisIntervalCondition,
                                                           analysisInterval))

        # Creating the select command with aggregates for OUTPUT tables
        if len(aggregate_variable_dict) > 0:

            aggStr = " group by "
            for tab in aggregate_variable_dict:
                cols = aggregate_variable_dict[tab]
                for col in cols:
                    aggStr += "%s.%s," % (tab, col)

                    #final_list.append("%s.%s as %s_%s" %(tab, col, tab, col))
                    #cols_list.append("%s_%s" %(tab, col))

            final_list.append('count(*) as frequency')
            cols_list.append('frequency')
            aggStr = aggStr[:-1]
        else:
            aggStr = ""

        # Generating the col list
        colStr = ''
        for i in final_list:
            colStr = colStr + '%s,' % (i)
        colStr = colStr[:-1]

        # Build the SQL string
        allJoinStr = ''
        for i in joinStrList:
            allJoinStr = allJoinStr + '%s' % i

        sql_string = 'select %s from %s %s %s' % (
            colStr, mainTable, allJoinStr, aggStr)

        #sql_string += ' and (persons.houseid = 35802 or persons.houseid = 90971  or persons.houseid = 119866)'
        #print 'SQL string for query - ', sql_string
        # print cols_list
        # raw_input()

        try:
            ti = time.time()
            result = sql.frame_query(sql_string, self.dbcon_obj.connection) 
            result.fillna(0,  inplace=True)
            data = DataArray(result, cols_list, indexCols=indexCols)

            print '\tRetrieved from the database using Pandas in %.4f' % (time.time() - ti)
            # print cols_list
            # Sort with respect to primary columns

            print "\tNumber of rows - %d and cols - %d" %(data.rows, data.cols)
            #print "\tFirst five rows of data retrieved"
            #print data.data.head()
            # print primCols
            #raw_input("Check data")

        #except AttributeError, e:
        #    raise DataError,  'AttributeError occurred with text - %s' %e
        except Exception, e:
            raise DataError,  'Other error occurred with text - %s' %e


        if len(delete_dict) > 0:
            #TODO: Fold this delete in to the two other delete functions implemented in cursor_query_browser
            table = delete_dict.keys()[0]
            var = delete_dict[table]

            delete_sql_string = ('delete from %s where %s in (select %s from (%s) as foo)'
                                 % (table, var, var, sql_string))
            #print 'Delete string - ', delete_sql_string

            # print 'delete records after select'

            try:
                ti = time.time()
                self.dbcon_obj.cursor.execute(delete_sql_string)
                self.dbcon_obj.connection.commit()
                print '\tTime taken to delete data - %.4f' % (time.time() - ti)
            except Exception, e:
                print 'Error deleting records. Query failed - ', e

        return data

    ########## methods for select query end ##########

    ########## methods for delete query  ##########
    # delete rows based on a deletion criteria
    def delete_selected_rows(self, table_name, column_name, value):
        """
        This method is used to delete selected rows fom the table in the database.

        Input:
        Database configuration object, table name and selection criteria

        Output:
        Deletes the rows that satisfy the selection criteria
        """
        fin_flag = None
        # check if table exists and then if columns exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            # check for columns
            get_cols = self.dbcon_obj.get_column_list(table_name)
            if column_name in get_cols:
                fin_flag = True
            else:
                fin_flag = False
        else:
            print 'Table %s does not exist.' % table_name

        if fin_flag:
            try:
                self.dbcon_obj.cursor.execute(
                    "delete FROM %s where %s = '%s'" % (table_name, column_name, value))
                self.dbcon_obj.connection.commit()
                print 'Delete successful'
            except Exception, e:
                print e
                print 'Error deleting the information. Query failed.'
        else:
            'Column %s does not belong to the table %s. Could not delete rows.' % (
                column_name, table_name)

    # delete all rows i.e. empty table

    def delete_all(self, table_name):
        """
        This method is used to delete all rows from the table.

        Input:
        Database configuration object, table name

        Output:
        Deletes all rows in the table
        """
        # check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            # print 'Table %s exists.'%table_name
            try:
                self.dbcon_obj.cursor.execute("delete FROM %s " % table_name)
                self.dbcon_obj.connection.commit()
                print '\t - Delete all records successful.'
            except Exception, e:
                print e
                print '\t - Error retrieving the information. Query failed.'
        else:
            print '\t - Table %s does not exist.' % table_name
        # after deleting all the data reset the sequences
        seqlist, ser_column = self.find_sequence(table_name)
        self.reset_sequence(seqlist)

    ########## methods for delete query end ##########

    ########## methods for insert query     ##########
    # insert values in the table
    def insert_into_table(self, arr, cols_list, table_name, keyCols, chunkSize=100000):
        """
        self, arr, cols_list, table_name, keyCols, chunkSize=None):
        This method is used to insert rows into the table.

        Input:
        Database configuration object, table name, data array

        Output:
        Inserts all the rows from data array in the table
        """

        table_name = table_name.lower()

        # Delete index before inserting
        index_cols = self.delete_index(table_name)

        # check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        tab_flag = True

        if tab_flag:
            # print 'Table %s exists.'%table_name
            try:

                ti = time.time()
                #arr_str = [tuple(each) for each in arr]
                #arr_str = str(arr_str)[1:-1]
                # Generate the column list
                cols_listStr = ""
                for i in cols_list:
                    cols_listStr += "%s," % i
                cols_listStr = cols_listStr[0:-1]
                cols_listStr = "(%s)" % cols_listStr

                # Divide the data into chunks
                last = 0
                lastRow = len(arr)
                nChunks = int(lastRow / chunkSize)
                for i in range(nChunks):
                    last = (i + 1) * chunkSize
                    arrSub = arr[i * chunkSize:last]
                    self.insert_nrows(table_name, cols_listStr, arrSub)

                # Insert last ODD chunk
                arrSub = arr[nChunks * chunkSize:]
                self.insert_nrows(table_name, cols_listStr, arrSub)

                #result = self.dbcon_obj.cursor.execute(insert_stmt)
                self.dbcon_obj.connection.commit()
                # print '\t\tTime after insert query %.4f' %(time.time()-ti)
            except Exception, e:
                print e
        else:
            print 'Table %s does not exist.'  # %table_name
        self.create_index(table_name, keyCols)

    def copy_into_table(self, data, cols_list, table_name, keyCols, 
                                         loc, partId=None, createIndex=True, 
                                         deleteIndex=True, delimiter=','):
        """
     Output:
     Inserts all the rows from data array in the table
     """
        t_d = time.time()
        if deleteIndex:
            # Delete index before inserting

            index_cols = self.delete_index(table_name)
        print '\t\tDeleting index took - %.2f' % (time.time() - t_d)

        self.file_write(data, loc, partId)

        cols_listStr = ""
        for i in cols_list:
            cols_listStr += "%s," % i
        cols_listStr = "(%s)" % cols_listStr[:-1]

        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            # print 'Table %s exists.'%table_name
            try:
                ti = time.time()
                insert_stmt = ("""copy %s %s from '%s/tempData_%s.csv' """
                               """ delimiters '%s'""" % (table_name, cols_listStr, loc,
                                                         partId, delimiter))

                #print '\t\t', insert_stmt
                result = self.dbcon_obj.cursor.execute(insert_stmt)
                self.dbcon_obj.connection.commit()
            except Exception, e:
                print e
        else:
            print 'Table %s does not exist.'  # %table_name
        t_c = time.time()
        if createIndex:
            self.create_index(table_name, keyCols)
        print '\t\tCreating index took - %.2f' % (time.time() - t_c)

    def copy_into_table_old(self, arr, cols_list, table_name, keyCols, loc, partId=None, createIndex=True, deleteIndex=True, delimiter=','):
        """
        self, arr, cols_list, table_name, keyCols, chunkSize=None):
        This method is used to insert rows into the table.

        Input:
        Database configuration object, table name, data array

        Output:
        Inserts all the rows from data array in the table
        """

        # print 'Table Name - %s, creating index - %s and deleting index - %s'
        # %(table_name , createIndex, deleteIndex)

        if partId == None:
            partId = ""

        table_name = table_name.lower()

        t_d = time.time()
        if deleteIndex:
            # Delete index before inserting

            index_cols = self.delete_index(table_name)
        print '\t\tDeleting index took - %.2f' % (time.time() - t_d)

        self.file_write(arr, loc, partId)

        # check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        tab_flag = True

        cols_listStr = ""
        for i in cols_list:
            cols_listStr += "%s," % i
        cols_listStr = "(%s)" % cols_listStr[:-1]

        if tab_flag:
            # print 'Table %s exists.'%table_name
            try:
                ti = time.time()
                insert_stmt = ("""copy %s %s from '%s/tempData_%s.csv' """
                               """ delimiters '%s'""" % (table_name, cols_listStr, loc,
                                                         partId, delimiter))

                print '\t\t', insert_stmt
                result = self.dbcon_obj.cursor.execute(insert_stmt)
                self.dbcon_obj.connection.commit()
                # print '\t\tTime after insert query - %.4f' %(time.time() - ti)
                # print '\t\tTime to insert - %.4f' %(time.time()-ti)
            except Exception, e:
                print e
        else:
            print 'Table %s does not exist.'  # %table_name
        t_c = time.time()
        if createIndex:

            self.create_index(table_name, keyCols)
        print '\t\tCreating index took - %.2f' % (time.time() - t_c)

    def insert_nrows(self, table_name, cols_listStr, arr):
        arr_str = [tuple(each) for each in arr]
        arr_str = str(arr_str)[1:-1]
        try:
            insert_stmt = "insert into %s %s values %s" % (
                table_name, cols_listStr, arr_str)
            result = self.dbcon_obj.cursor.execute(insert_stmt)
            self.dbcon_obj.connection.commit()
        except Exception, e:
            print '\t    Error while inserting data in the table'
            print e

    ########## methods for delete query end ##########

    ########## methods for creating and deleting index##########
    # create an index
    def create_index(self, table_name, col_list, index_name=None):
        """
        This method creates an index on the table

        Input:
        Database configuration object, table name and column list

        Output:
        Index created on the table with the specified columns
        """
        fin_flag = None
        # check if table exists and then if columns exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            # check for columns
            get_cols = self.dbcon_obj.get_column_list(table_name)
            num_tab = len(list(set(get_cols) & set(col_list)))
            if num_tab <= len(get_cols):
                fin_flag = True
            else:
                fin_flag = False
        else:
            print 'Table %s does not exist.' % table_name

        if fin_flag:
            index_stmt = ''
            columns = ''
            count = 0
            if not index_name:
                index_name = table_name + '_index'

            for i in col_list:
                if count < (len(col_list) - 1):
                    columns = columns + i + ', '
                    count = count + 1
                else:
                    columns = columns + i
            index_stmt = 'create index %s on %s (%s)' % (
                index_name, table_name, columns)
            # print 'Index Statement - %s' %(index_stmt)
            try:
                self.dbcon_obj.cursor.execute(index_stmt)
                self.dbcon_obj.connection.commit()
                # print '\t\tIndex %s created'%index_name
            except Exception, e:
                print 'Error while creating an index'
                print e
                self.dbcon_obj.connection.rollback()

    # delete an index
    def delete_index(self, table_name, index_name=None):
        """
        This method deletes an index on the table

        Input:
        Database configuration object and table name

        Output:
        Index on the table is deleted
        """
        # check if table exists and then if columns exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            # check if index exits
            ind_cols = self.get_index_columns(table_name)
            if ind_cols:
                if not index_name:
                    index_name = table_name + '_index'
                try:
                    self.dbcon_obj.cursor.execute("drop index %s" % index_name)
                    self.dbcon_obj.connection.commit()
                    # print '\t\tIndex %s deleted'%index_name
                except Exception, e:
                    print 'Error while deleting an index'
                    print e
                    self.dbcon_obj.connection.rollback()
            else:
                print '\t\tIndex does not exists so cannot be deleted.'

    # get the index columns
    def get_index_columns(self, table_name):
        """
        This method is used to fetch the columns that form the index for the table

        Input:
        Database configuration object and table_name

        Output:
        List of columns that form the index
        """
        self.table_name = table_name
        # before returning the column types check if the table exists
        table_flag = self.dbcon_obj.check_if_table_exists(table_name)
        sql_string = "SELECT indexdef FROM pg_indexes WHERE tablename = '%s'" % table_name
        pkey = "CREATE UNIQUE INDEX "
        index = ''
        if table_flag:
            try:
                self.dbcon_obj.cursor.execute(sql_string)
                columns = self.dbcon_obj.cursor.fetchall()
                cols = [cl[0] for cl in columns]

                for each in cols:
                    if pkey not in each:
                        index = each
                if index != '':
                    split_str = index.split("(")
                    sub_str = split_str[1].split(")")[0]
                    ind_str = sub_str.split(", ")
                    return ind_str
                else:
                    return None
            except Exception, e:
                print 'Error while fetching the columns from the table'
                print e
        else:
            print 'Table %s does not exist. Cannot get the column list' % table_name

    ########## methods for creating and deleting index##########

    ########### file function #################
    def file_write(self, data, loc, partId, fileName=None):
        """
     This method is used to write the result to a file
     in a csv format.
     """
        ti = time.time()
        if fileName is not None:
            loc = os.path.join(loc, "%s.csv"%fileName)
        else:
            loc = os.path.join(loc, "tempData_%s.csv" %(partId))
        data.to_csv(loc, header=False, index=False)
        print '\t\tTime to write to file Pandas implementation - %.4f' % (time.time() - ti)

    def file_write_old(self, data_arr, loc, partId, fileName=None):
        """
        This method write the resultset to a file.

        Input:
        Data array or resultset and the column list

        Output:
        File created with all data written in it.
        """
        """
        #open the file
        ti = time.time()
        myfile = open('%s/tempData_%s.csv' %(loc, partId), 'w')

        #loop through the array and write to file
        for each in data_arr:
            each = list(each)
            myfile.write(str(each)[1:-1])
            myfile.write('\n')
        myfile.close()
        print '\t\tTime to write to file - %.4f' %(time.time()-ti)
        """
        fmt = ''
        for col in range(len(data_arr[0])):
            colType = data_arr[0][col].dtype
            if str(colType)[0] == 'f':
                # print 'atleast one float store as float'
                fmt += '%.4f,'
            else:
                fmt += '%u,'
        fmt = fmt[:-1]
        print '\t\tThis is the final format-', fmt
        ti = time.time()
        if fileName is None:
            savetxt('%s/tempData_%s.csv' %
                    (loc, partId), data_arr, delimiter=',', fmt=fmt)
        else:
            savetxt('%s/%s_%s.csv' %
                    (loc, fileName, partId), data_arr, delimiter=',', fmt=fmt)
        print '\t\tTime to write to file new implementation - %.4f' % (time.time() - ti)
    ########### file function ends ############

    ###########################################
    # new code for copy file
    # file to get datatype
    def column_data_type(self, res, temp_arr):
        """
        Input:
        resultset and data array object
        """
        temp_cols = temp_arr.varnames
        print temp_cols
        write_file_str = ""
        write_file_str = self.get_column_data_type(temp_cols)
        print write_file_str

        print 'write file start ----------->', time.time()
        try:
            file_fp = open(
                '/home/namrata/Documents/DBclasses/dbapi/temp1.csv', 'w')
            print 'file opened'
            data_arr_len = len(temp_arr.data)
            myfile.write(str(temp_cols)[1:-1])
            myfile.write('\n')

            for each in temp_arr.data:
                each = list(each)
                each = str(each)[1:-1]
                parts = each.split(', ')
                count = len(parts)
                ctr = 0
                #write_str = "'%s,%s,%s,%s'%(int(float(parts[0])), long(float(parts[1])), float(parts[2]), int(float(parts[3])))"
                # print write_str
                #file_fp.write('%s,%s,%s,%s\n'%(int(float(parts[0])), long(float(parts[1])), float(parts[2]), int(float(parts[3]))))
                file_fp.write(eval(write_file_str))
                file_fp.write('\n')
        except Exception, e:
            print e
        file_fp.close()
        print 'write file end ----------->', time.time()

        print '\ninsert data'

        try:
            insert_stmt = "copy abc from '/home/namrata/Documents/DBclasses/dbapi/temp1.csv' with delimiter as ',' csv header"
            # print insert_stmt
            print 'time before insert query ------>', time.time()
            result = self.dbcon_obj.cursor.execute(insert_stmt)
            self.dbcon_obj.connection.commit()
            print 'time after insert query ------>', time.time()
        except Exception, e:
            print e
        print '\n'

    def get_column_data_type(self, temp_arr):
        """
        Input:
        resultset and data array object
        """
        data_type_arr = []
        data_type_stmt = "select column_name, data_type  from information_schema.columns where table_schema = 'public'"
        try:
            self.dbcon_obj.cursor.execute(data_type_stmt)
            result = self.dbcon_obj.cursor.fetchall()

            columns = [cl[0] for cl in result]
            data_type = [dt[1] for dt in result]
            print columns
            for each in temp_arr:
                for col, dat in zip(columns, data_type):
                    if each == col:
                        data_type_arr.append(dat)
                        break
        except Exception, e:
            print e
        print 'data_type_arr is ------>', data_type_arr
        final_data_types = self.define_mapping(data_type_arr)
        print 'final data types are ------->', final_data_types

        # create string for file
        file_str = ""
        type_iden_str = " '"
        # create string for the type identifier
        for each in range(len(temp_arr)):
            type_iden_str = type_iden_str + "%s\t"
        type_iden_str = type_iden_str[1:-1]
        type_iden_str = type_iden_str + "'%"

        # create string for
        data_type_str = "("
        count = 0
        for each in final_data_types:
            if count == (len(final_data_types) - 1):
                data_type_str = data_type_str + each + \
                    "(float(parts[" + str(count) + "])))"
            else:
                data_type_str = data_type_str + each + \
                    "(float(parts[" + str(count) + "])), "
                count = count + 1

        final_str = type_iden_str + data_type_str
        return final_str

    def define_mapping(self, data_type_list):
        new_data_types = []

        for each in data_type_list:
            if each == 'integer':
                new_data_types.append('int')
            elif each == 'real':
                new_data_types.append('float')
            elif each == 'bigint':
                new_data_types.append('long')
            elif each == 'character varying':
                new_data_types.append('str')
            elif each == 'double precision':
                new_data_types.append('float')

        return new_data_types
    ###########################################################

    def find_sequence(self, table_name=None):
        """
        This method is used to find the sequences in the database

        Input:
        Database configuration object and table name.
        If no table name is provided then find sequences for all tables

        Output:
        Reset sequence to 1
        """
        if table_name == None:
            seq_flag = 1
        else:
            seq_flag = 0

        if seq_flag:
            # find sequences for all tables and save in a list
            sql_query = (
                "SELECT column_name, column_default FROM INFORMATION_SCHEMA.COLUMNS WHERE column_default LIKE 'nextval%'")
            try:
                self.dbcon_obj.cursor.execute(sql_query)
                col_default = self.dbcon_obj.cursor.fetchall()
            except Exception, e:
                print 'Query execution failed. Failed to find sequences'
                print e
        else:
            # find sequences for the specified table and save in a list
            sql_query = ("SELECT column_name, column_default FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '%s'" % table_name
                         + " and column_default LIKE 'nextval%'")
            # AND column_default LIKE 'nextval%'"
            try:
                self.dbcon_obj.cursor.execute(sql_query)
                col_default = self.dbcon_obj.cursor.fetchall()
            except Exception, e:
                print 'Query execution failed. Failed to find sequences'
                print e

        seq_list = []
        sequence = []
        serial_column = []
        # create a list that has only the tuples with the sequence name in it
        for each in col_default:
            off_set = str(each[1]).find("'")
            if off_set is not -1:
                seq_list.append(each[1])
                serial_column.append(each[0])

        # find the indexes for the sequence, extract the substring from the tuple
        # and save in a new list
        for each in seq_list:
            each = str(each)
            sub_str = [match.start()
                       for match in re.finditer(re.escape("'"), each)]
            start = sub_str[0] + 1
            end = sub_str[1]
            seq = each[start:end]
            sequence.append(seq)
        # return the list with all the sequences
        return sequence, serial_column

    def reset_sequence(self, sequence_list):
        """
        This method is used to reset the sequence

        Input:
        Database configuration object and sequence list

        Output:
        Sequence is reset to 1
        """
        # run a loop to reset the sequences
        if not sequence_list:
            # print 'No sequences present'
            return False

        for each in sequence_list:
            sql_string = "alter sequence %s restart with 1" % each
            # print sql_string
            try:
                self.dbcon_obj.cursor.execute(sql_string)
                self.dbcon_obj.connection.commit()
                return True
            except Exception, e:
                print 'Query execution failed. Failed to reset sequences'
                print e
                return False

    def cluster_index(self, table_name, index_name):
        """
        This method is used to create a clustered index

        Input:
        Table name and index name

        Output:
        The index created is clustered
        """
        print 'table name --> %s and index name --> %s' % (table_name, index_name)
        cluster_index = "ALTER TABLE %s CLUSTER ON %s" % (
            table_name, index_name)
        print cluster_index
        try:
            self.dbcon_obj.cursor.execute(cluster_index)
            self.dbcon_obj.connection.commit()
            return True
        except Exception, e:
            print 'Error while creating an index'
            print e
            self.dbcon_obj.connection.rollback()
        return False


# unit test to test the code
import unittest

# define a class for testing


class TestMainClass(unittest.TestCase):
    # only initialize objects here

    def setUp(self):
        self.protocol = 'postgres'
        self.user_name = 'postgres'
        self.password = '1234'
        self.host_name = 'localhost'
        self.database_name = 'mag_zone_upto_afterschoolacts_5percent'

    def testMainClass(self):
        abc = DataBaseConfiguration(
            self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        newobject = QueryBrowser(abc)

        """ create a connection to the database """
        newobject.dbcon_obj.new_connection()
        """
        table_name = 'temp_table1'
        column_name = 'role_id'
        value = '1'
        abc = None
        defg = None
        #abc = newobject.fetch_selected_rows(table_name, column_name, value)
        #print abc
        #newobject.fetch_selected_rows(table_name, column_name, value)

        #newobject.delete_selected_rows(table_name, column_name, value)

        #newobject.delete_all(table_name)

        col_list = ['grad', 'role_id']
        #newobject.create_index(table_name, col_list)

        #newobject.delete_index(table_name)

        #data_arr = [('aa','aa','1'),('bb','bb','1')]
        #newobject.insert_into_table(data_arr, table_name)

        DB_DICT = {'households': ['htaz', 'numchild', 'inclt35k', 'hhsize'],
                 'persons': ['male', 'schstatus', 'one', 'houseid', 'personid'],
                 'schedule_r': ['scheduleid', 'activitytype']}
        COLUMN_NAMES = {'households': ['houseid'],
                      'schedule_r': ['personid', 'houseid']}
        TABLE_NAMES = ['persons', 'households', 'schedule_r', 'abcd']
        MAX_DICT = {'schedule_r': ['scheduleid']}

        #print DB_DICT, COLUMN_NAMES, TABLE_NAMES, MAX_DICT

        #newobject.select_join(DB_DICT, COLUMN_NAMES, TABLE_NAMES, MAX_DICT)
        print '\n-----------------> select all from table'
        res, temp, columns = newobject.select_all_from_table(table_name)
        print '\n-----------------> write data to file'
        newobject.file_write(temp, columns)
        print '\n-----------------> insert into table'
        #newobject.insert_into_table()
        """
        table_name = 'temp'
        #cols = newobject.dbcon_obj.get_column_list(table_name)
        cols = ['aa', 'bb']
        cols_list = ['bb']
        # print cols
        total = 2
        index_name = 'index_1'
        for i in range(total):
            print '--> %s' % i
            t1 = time.time()
            # print 'delete index'
            # newobject.delete_index(table_name)
            #newobject.copy_table(cols, table_name, delimiter=',')
            # print 'create index'
            #newobject.create_index(table_name, cols_list)
            t2 = time.time()
            print 'Time ---> %s' % (t2 - t1)

        #newobject.create_index(table_name, cols_list, index_name)
        res = newobject.cluster_index(table_name, index_name)
        print 'cluster index result --> %s' % res
        #newobject.delete_index(table_name, index_name)
        # newobject.delete_all(table_name)
        #seqlist = newobject.find_sequence()
        # print seqlist
        #seql = []
        # newobject.reset_sequence(seql)
        # for each in seqlist:
        # print each
        #    print str(each)[str(each).find("'")+1:str(each).find("'")]
        #    print type(each)
        #index_columns = newobject.get_index_columns(table_name)
        # for each in index_columns:
        #    print each
        """ close the connection to the database """
        newobject.dbcon_obj.close_connection()


if __name__ == '__main__':
    unittest.main()
