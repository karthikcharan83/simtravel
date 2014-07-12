import copy
import time
import os
import shutil
import traceback
import sys
import csv
import subprocess
from lxml import etree
from numpy import array, ma, ones, zeros, vstack, where, save

from openamos.core.component.config_parser import ConfigParser
from openamos.core.database_management.cursor_query_browser import QueryBrowser
from openamos.core.database_management.cursor_divide_data import DivideData
from openamos.core.errors import ConfigurationError
from openamos.core.data_array import DataArray
from openamos.core.cache.dataset import DB
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.models.interaction_model import InteractionModel
from openamos.core.travel_skims.skimsprocessor import NetworkConditions
#from openamos.core.travel_skims.distprocessor import DistProcessor
#from openamos.core.travel_skims.successive_avg_processor import SuccessiveAverageProcessor

from multiprocessing import Process


from openamos.core.travel_skims.heat_map_skims import PlotHeatMap
from openamos.core.config import ConfigObject
from openamos.gui.results_menu.to_msexcel_nogui import Export_Outputs
from PyQt4.QtGui import QApplication
import sys


class SimulationManager(object):

    """os.copy python
    The class reads the configuration file, creates the component and model objects,
    and runs the models to simulate the various activity-travel choice processes.

    If the configObject is invalid, then a valid fileLoc is desired and if that fails
    as well then an exception is raised. In a commandline implementation, fileLoc will
    be passed.
    """

    def __init__(self, configObject=None, fileLoc=None, component=None, iteration=1, year=2012):
        if configObject is None and fileLoc is None:
            raise ConfigurationError, """The configuration input is not valid; a """\
                """location of the XML configuration file or a valid etree """\
                """object must be passed"""

        if not isinstance(configObject, etree._ElementTree) and configObject is not None:
            print ConfigurationError, """The configuration object input is not a valid """\
                """etree.Element object. Trying to load the object from the configuration"""\
                """ file."""
        try:
            fileLoc = fileLoc.lower()
            self.fileLoc = fileLoc
            configObject = etree.parse(fileLoc)
        except AttributeError, e:
            raise ConfigurationError, """The file location is not a valid."""
        except IOError, e:
            print e
            raise ConfigurationError, """The path for configuration file was """\
                """invalid or the file is not a valid configuration file."""

        self.iteration = iteration
        self.year = year
        self.fileLoc = fileLoc
        self.configObject = configObject
        # creates the model configuration parser
        self.configParser = ConfigParser(configObject)
        self.projectConfigObject = self.configParser.parse_projectAttributes()
        self.projectSkimsObject = self.configParser.parse_network_tables()
        print "Network Skims -- ", self.projectSkimsObject

        self.projectLocationsObject = self.configParser.parse_locations_table()

    def divide_database(self, numParts):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        self.divideDatabaseObj = DivideData(dbConfigObject)
        self.divideDatabaseObj.partition_data(numParts, ['households',
                                                         'persons'], 'houseid')

    def collate_results(self, numParts):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        self.divideDatabaseObj = DivideData(dbConfigObject)
        self.divideDatabaseObj.collate_full_results(numParts)

    def setup_databaseConnection(self, partId=None):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        if partId is not None:
            dbConfigObject.database_name += '_%s' % (partId)

        queryBrowser = QueryBrowser(dbConfigObject)
        queryBrowser.dbcon_obj.new_connection()
        return queryBrowser

    def setup_cacheDatabase(self, partId=None):
        print "-- Creating a hdf5 cache database --"
        fileLoc = self.projectConfigObject.location
        self.db = DB()

    def setup_location_information(self):
        print "-- Processing Location Information --"
        t = time.time()
        queryBrowser = self.setup_databaseConnection()
        colsList = ([self.projectLocationsObject.location_id_var] + 
                          self.projectLocationsObject.locations_varsList)

        tableName = self.projectLocationsObject.tableName
        data = queryBrowser.select_all_from_table(tableName, colsList)
        data.create_index_using_cols([self.projectLocationsObject.location_id_var])
        #print data.data.head()
        #raw_input("location data")
        print '\tTotal time taken to retrieve records from the database %.4f' % (time.time() - t)

        fileLoc = self.projectConfigObject.location

        # the new numpy doesn't work with masked array and hence the conversion
        # ...
        #dataCp = array(data.data)
        file = os.path.join(fileLoc, "%s.csv"%tableName)
        data.data.to_csv(file, index=False)
        #save('%s/%s.npy' % (fileLoc, tableName), dataCp)
        self.close_database_connection(queryBrowser)
        print '\tTime taken to write to numpy cache format %.4f' % (time.time() - t)

    def setup_resultsBackup(self):
        print "-- Creating a hdf5 backup of all results --"
        fileLoc = self.projectConfigObject.location

        backupDirectoryLoc = os.path.join(
            self.projectConfigObject.location, "year_%d" % self.year)

        try:
            os.mkdir(backupDirectoryLoc)
        except OSError, e:
            print 'Error creating directory for year - %s:' % self.year, e

        backupDirectoryLoc = os.path.join(
            backupDirectoryLoc, "iteration_%d" % self.iteration)

        try:
            os.mkdir(backupDirectoryLoc)
        except OSError, e:
            print 'Error creating directory for iteration - %s within year - %s:' % (self.iteration, self.year), e

        queryBrowser = self.setup_databaseConnection()

        # create cache again -
        self.setup_cacheDatabase()
        self.setup_inputCacheTables()
        self.setup_outputCacheTables()
        """
        # Copying results for components that generate runtime outputs e.g. od_r, gap_before_r, gap_after_r etc.
        for component in self.componentList:
            if component.writeToLocFlag == True:
                tableName = component.writeToTable
                self.reflectFromDatabaseToLoc(queryBrowser, tableName, backupDirectoryLoc)
                print 'Backing up results for table - %s' %tableName



        # create populate cache -
        tableList = self.db.list_of_outputtables()

        tableList = ['schedule_skeleton_r', 'schedule_final_r', 'schedule_elapsed_r',
                     'trips_r', 'trips_to_malta_r', 'trips_arrival_from_malta_r',
                     'households_vehicles_count_r', 'persons_r', 'schedule_full_r', 'trips_purpose_r']

        for tableName in tableList:
            #print 'Backing up results for table - ', tableName
            self.reflectFromDatabaseToCache(queryBrowser, tableName)

        # Copying the hdf 5 file
        print 'Copying the hdf 5 file to the iteration folder'
        fileLoc = os.path.join(self.projectConfigObject.location, 'amosdb.h5')
        backupFileLoc = os.path.join(backupDirectoryLoc, 'amosdb.h5')
        shutil.copyfile(fileLoc, backupFileLoc)
        """

        # Copying the skims ...
        print 'Copying the skim files to the iteration folder'
        oldFileFolder = os.path.join(
            self.projectConfigObject.location, "year_%d" % self.year, "iteration_%d" % (int(self.iteration) - 1))

        # dumping the postgres database
        print 'Starting the postgres database dump - '
        dbConfigObject = self.configParser.parse_databaseAttributes()
        host = dbConfigObject.host_name
        username = dbConfigObject.user_name
        dbname = dbConfigObject.database_name
        backupFileLoc = os.path.join(backupDirectoryLoc, 'db.backup')

        cmd = '/usr/bin/pg_dump --host %s --port 5432 --username "%s" --role "postgres" --no-password  --format tar --blobs --encoding SQL_ASCII --verbose --file "%s" "%s"' % (
            host, username, backupFileLoc, dbname)

        try:
            stdout, stderr = subprocess.Popen(cmd,
                                              shell=True
                                              ).communicate()
        except Exception, e:
            print cmd
            print "Error occured when backing up the database", e

        print "\tDumping the postgres database completed"

        """

        # Skims
        fSkimsConv = open(backupDirectoryLoc + os.path.sep + 'skimsConv.txt', 'w')
        for skimsTable in self.projectSkimsObject.table_ttLocationLookup.keys():
            skimsTableLoc = self.projectSkimsObject.table_ttLocationLookup[skimsTable]
            skimsTableName = self.projectSkimsObject.table_lookup[skimsTable]

            shutil.copy(skimsTableLoc, backupDirectoryLoc)
            oldFile = os.path.join(oldFileFolder, "%s.dat" %skimsTableName)
            if self.iteration > 1:
                dev = self.calculate_skims_convergence_criterion(oldFile, skimsTableLoc, skimsTableName, backupDirectoryLoc)
                print 'deviation - ', dev
                fSkimsConv.write('%s,%.4f\n' %(skimsTable,dev))
        fSkimsConv.close()



        if self.iteration > 1:
            # OD
            fODConv = open(backupDirectoryLoc + os.path.sep + 'odConv.txt', 'w')

            oldFile = os.path.join(oldFileFolder, 'od_r_None.csv')
            newFile = os.path.join(backupDirectoryLoc, 'od_r_None.csv')
            dev = self.calculate_od_convergence_criterion(oldFile, newFile, backupDirectoryLoc)
            fODConv.write('%.4f\n' %dev)
            fODConv.close()
        """
        # Creating and copying tabulations
        self.backup_result_tabulations(backupDirectoryLoc)

        self.close_database_connection(queryBrowser)

    def setup_network_conditions(self):
        ti = time.time()
        self.networkConditions = NetworkConditions()
        #TODO: Repeat this for all modes

        loc_dict = self.projectSkimsObject.return_tablelocdict()
        endIntervalForSkims = self.projectSkimsObject.ttIntervalEnd
        
        self.networkConditions.add_mode(175, 48, "auto", 1,  "historic", 1, endIntervalForSkims)
        print "Loading using text as inputs"
        self.networkConditions.read_skims(loc_dict, "auto", "historic")
        print "Time taken to read skims is - %.4f" %(time.time()-ti)
        #print "Skim for minute 29 - ",  self.modalConditions.modes["Historic Skims"].lookup_skim_index(29)
        #print "Skim for minute 30 - ",  self.modalConditions.modes["Historic Skims"].lookup_skim_index(30)        
        #print "Skim for minute 31 - ",  self.modalConditions.modes["Historic Skims"].lookup_skim_index(31)                

    def backup_result_tabulations(self, fileLoc):
        app = QApplication(sys.argv)

        # 4 represents the socio-demographic groups ...

        for i in range(4):
            confObj = ConfigObject(configtree=self.configObject)
            exportObj = Export_Outputs(confObj, index=i)

            # select all tables to download
            # exportObj.check_all.setCheckState(True)
            # exportObj.select_all()

            # sociodemographic group
            # exportObj.pptype.setCurrentIndex(i)
            socioDemText = exportObj.pptypeText[i]

            # set file path
            fileName = fileLoc + os.path.sep + "results_%s.xlsx" % socioDemText

            # create file
            exportObj.accept(fileName)

    def calculate_skims_convergence_criterion(self, oldFileLoc, newFileLoc, skimsTableName, backupDirectory):
        heatMapObj = PlotHeatMap()
        return heatMapObj.createHeatMapForXY('old_%s' % skimsTableName, oldFileLoc,
                                             'new_%s' % skimsTableName, newFileLoc,
                                             skimsTableName, backupDirectory)

    def calculate_od_convergence_criterion(self, oldFileLoc, newFileLoc, backupDirectory):
        heatMapObj = PlotHeatMap()
        return heatMapObj.createHeatMapForIncompleteXY('old_od', oldFileLoc,
                                                       'new_od', newFileLoc, 'od', backupDirectory)

    def restore_from_resultsBackup(self):
        print "-- Creating a hdf5 backup of all results --"
        fileLoc = self.projectConfigObject.location

        backupDirectoryLoc = os.path.join(
            self.projectConfigObject.location, "year_%d" % self.year, "iteration_%d" % self.iteration)

        fileLoc = os.path.join(self.projectConfigObject.location, 'amosdb.h5')
        backupFileLoc = os.path.join(backupDirectoryLoc, 'amosdb.h5')
        shutil.copyfile(backupFileLoc, fileLoc)
        print 'file copied back ... '

        self.read_cacheDatabase()

        queryBrowser = self.setup_databaseConnection()

        # create populate cache -
        tableList = self.db.list_of_outputtables()

        for tableName in tableList:
            print 'Restoring results for table - ', tableName
            queryBrowser.delete_all(tableName)
            self.reflectToDatabase(
                queryBrowser, tableName, createIndex=False, deleteIndex=False, restore=True)

        self.close_cache_connection()
        self.close_database_connection(queryBrowser)

    def setup_outputCacheTables(self, partId=None):
        self.db.create_outputCache(partId)

        # placeholders for creating the hdf5 tables
        # only the network data is read and processed for faster
        # queries
        """
            if partId is not None:
                self.db = DB(fileLoc, partId)
            else:
                self.db = DB(fileLoc)
            #self.db.create()
        """

    def open_cacheDatabase(self, partId):
        fileLoc = self.projectConfigObject.location
        self.db = DB(fileLoc)
        self.db.load_input_output_nodes(partId)

    def setup_tod_skims(self):
        iteration = self.projectConfigObject.iteration

        # self.successive_average_skims(iteration)

        return

    def successive_average_skims(self, iteration=1):
        print 'Processing skims for iteration - %s' % iteration
        uniqueTableList = list(
            set(self.projectSkimsObject.table_ttLocationLookup.values()))

        t_sa = time.time()
        for table in uniqueTableList:
            sa_filePath = '%s/skimOutput/successive_average/SA_%s' % (
                self.projectConfigObject.location, os.path.basename(table))
            sa_oldFilePath = '%s/skimOutput/successive_average/SA_temp_%s' % (
                self.projectConfigObject.location, os.path.basename(table))
            print '\tCalculating successive averages for file - ', sa_filePath
            if iteration == 1:
                try:
                    os.remove(sa_filePath)
                except Exception, e:
                    print 'Error occurred when deleting a successive average file - %s' % e
                shutil.copyfile(table, sa_filePath)

            elif iteration > 1:
                # look for a file with a prefix SA_<filename> and calculate an
                # average based on 1/k * tt_current + k-1/k * tt_current-1

                succAvgObject = SuccessiveAverageProcessor(1995)
                try:
                    os.remove(sa_oldFilePath)
                except Exception, e:
                    print 'Error occurred when deleting a successive average file - %s' % e

                print '\tLag file - ', sa_filePath
                print '\tNew file - ', table
                print '\tCopy of old lag - ', sa_oldFilePath

                succAvgObject.get_avg_tt(
                    sa_filePath, table, sa_oldFilePath, iteration)
            else:
                raise Exception, "the iteration number is invalid"

        # Updating the location of skim tables which are averaged across
        # iterations to be used in OpenAMOS
        skimTables = self.projectSkimsObject.table_ttLocationLookup.keys()
        for skimTable in skimTables:
            oldPath = self.projectSkimsObject.table_ttLocationLookup[skimTable]
            sa_filePath = '%s/skimOutput/successive_average/SA_%s' % (
                self.projectConfigObject.location, os.path.basename(oldPath))
            print '\tOld Path - ', oldPath
            print '\tNew Path - ', sa_filePath
            self.projectSkimsObject.table_ttLocationLookup[
                skimTable] = sa_filePath

        print 'Time taken to calculate successive average - %.4f' % (time.time() - t_sa)

        raw_input()

    def load_file(self, location, delimiter=","):
        f = open(location, 'r')
        arr = []
        for line in f:
            line = line.split(delimiter)
            arr.append(line)
        arr = array(arr, float)
        f.close()
        return arr

    def parse_config(self):
        print "-- Parsing components and model specifications --"
        self.componentList = self.configParser.parse_models(
            self.projectConfigObject.seed)
        # TODO: implement subsample runs

        # Printing models that were parsed
        modelCount = 0
        for comp in self.componentList:
            # print '\n\tFor component - %s ' %(comp.component_name)
            # print "\t -- Model list including model formulation and data filters if any  -- "
            # print '\tPost Run Filters - ', comp.post_run_filter
            for mod in comp.model_list:
                # print "\t\t - name:", mod.dep_varname, ",formulation:",
                # mod.model_type, ",filter:", mod.data_filter
                modelCount += 1

        print "\tTotal of %s components and %s models will be processed" % (len(self.componentList), modelCount)
        print "\t - Note: Some models/components may have been added because of the way OpenAMOS framework is setup."
        # raw_input()

    def clean_database_tables_for_parts(self, numParts):
        for i in range(numParts):
            self.clean_database_tables(partId=i + 1)
            """
            if partId is not None:
                self.db = DB(fileLoc, partId)
            else:
                self.db = DB(fileLoc)
            #self.db.create()
            """

    def clean_database_tables(self, partId=None):
        queryBrowser = self.setup_databaseConnection(partId)
        tableNamesDelete = []
        for comp in self.componentList:
            if comp.skipFlag:
                continue
            # clean the run time tables
            # delete the delete statement; this was done to clean the tables
            # during testing
            tableName = comp.writeToTable
            if tableName not in tableNamesDelete:
                # if comp.readFromTable <> comp.writeToTable:
                tableNamesDelete.append(tableName)
                print "\tDeleting records in the output table - %s before simulating choices again" % (tableName)
                queryBrowser.delete_all(tableName)

            if comp.writeToTable2 is not None:
                tableName = comp.writeToTable2
                if tableName not in tableNamesDelete:
                    tableNamesDelete.append(tableName)
                    print "\tDeleting records in the second output table - %s before simulating choices again" % (tableName)
                    queryBrowser.delete_all(tableName)

        self.close_database_connection(queryBrowser)

    def run_components_for_parts(self, numParts):
        for i in range(numParts):
            self.run_components(partId=i + 1)

    def run_components(self, partId=None):
        #configParser = copy.deepcopy(self.configParser)
        configParser = self.configParser

        queryBrowser = self.setup_databaseConnection(partId)
        t_c = time.time()

        try:
            lastTtTableLoc = None

            # the first argument is an offset and the second one is the count of nodes
            # note that the taz id's should be indexed at the offset and be in increments
            # of 1 for every subsequent taz id

            for comp in self.componentList:
                t = time.time()
                print '\nRunning Component - %s; Analysis Interval - %s' % (comp.component_name,
                                                                            comp.analysisInterval)

                if comp.skipFlag:
                    print '\tSkipping the run for this component'
                    continue

                preProcessFlag = comp.pre_process(queryBrowser,
                                        self.networkConditions,
                                        self.db,  
                                        self.projectConfigObject.location, 
                                        self.projectConfigObject.seed)

                if preProcessFlag is True:
                    # Call the run function to simulate the chocies(models)
                    # as per the specification in the configuration file
                    # data is written to the hdf5 cache because of the faster
                    # I/O
                    fileLoc = self.projectConfigObject.location
                    result = comp.run(queryBrowser, fileLoc, self.networkConditions, partId)

                configParser.update_completedFlag(
                    comp.component_name, comp.analysisInterval)

                comp.data = None
                print '-- Finished simulating component - %s; time taken %.4f --' % (comp.component_name,
                                                                                     time.time() - t)
                # raw_input()
        except Exception, e:
            print 'Exception occurred - %s' % e
            traceback.print_exc(file=sys.stdout)

        self.save_configFile(configParser, partId)
        self.close_database_connection(queryBrowser)
        print '-- TIME TAKEN  TO COMPLETE ALL COMPONENTS - %.4f --' % (time.time() - t_c)

    def save_configFile(self, configParser, partId):
        return
        """"
        if partId is not None:
            fileLoc = '%s_par_%s.xml' % (self.fileLoc[:-4], partId)
        else:
            fileLoc = self.fileLoc
        configFile = open(fileLoc, 'w')
        configParser.configObject.write(configFile, pretty_print=True)
        configFile.close()
        """


    def reflectFromDatabaseToLoc(self, queryBrowser, tableName, fileLoc, partId=None):
        ti = time.time()
        print 'Backing component table separately to location - ', tableName

        tableRef = self.db.returnTableReference(tableName, partId)
        colsToWrite = tableRef.colnames
        data = queryBrowser.select_all_from_table(tableName, cols=colsToWrite)

        if data is None:
            # print '\tNo result returned for the table ... '
            return

        convType = self.db.returnTypeConversion(tableName, partId)
        dtypesInput = tableRef.coldtypes
        data_to_write = data.columnsOfType(colsToWrite, colTypes=dtypesInput)

        queryBrowser.file_write(
            data_to_write.data, fileLoc, partId, fileName=tableName)

        print '\t\tData backed up for table %s in - %.4f' % (tableName, time.time() - ti)

    def close_database_connection(self, queryBrowser):
        queryBrowser.dbcon_obj.close_connection()


if __name__ == '__main__':

    simMan = SimulationManager(
        fileLoc="/workspace/openamos/configs/mag_zone/config_after_malta.xml", iteration=2, year=2019)
    simMan.backup_result_tabulations(
        "/workspace/projects/mag_zone_dynamic/year_2019/")
