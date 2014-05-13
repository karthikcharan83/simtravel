import copy
import time
from lxml import etree
from numpy import array, ma, ones, zeros, vstack, where

from openamos.core.component.config_parser import ConfigParser
from openamos.core.database_management.query_browser import QueryBrowser
from openamos.core.errors import ConfigurationError
from openamos.core.data_array import DataArray
from openamos.core.cache.dataset import DB
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.models.interaction_model import InteractionModel

from multiprocessing import Process

class ComponentManager(object):
    """
    The class reads the configuration file, creates the component and model objects,
    and runs the models to simulate the various activity-travel choice processes.

    If the configObject is invalid, then a valid fileLoc is desired and if that fails
    as well then an exception is raised. In a commandline implementation, fileLoc will
    be passed.
    """

    def __init__(self, configObject=None, fileLoc=None, component=None):
        if configObject is None and fileLoc is None:
            raise ConfigurationError, """The configuration input is not valid; a """\
            """location of the XML configuration file or a valid etree """\
            """object must be passed"""

        if not isinstance(configObject, etree._ElementTree) and configObject is not None:
            print ConfigurationError, """The configuration object input is not a valid """\
                """etree.Element object. Trying to load the object from the configuration"""\
                """ file."""

        try:
            configObject = etree.parse(fileLoc)
        except Exception, e:
            print e
            raise ConfigurationError, """The path for configuration file was """\
                """invalid or the file is not a valid configuration file."""

        self.configObject = configObject
        self.configParser = ConfigParser(configObject) #creates the model configuration parser
        self.projectConfigObject = self.configParser.parse_projectAttributes()


    def establish_databaseConnection(self):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        self.queryBrowser = QueryBrowser(dbConfigObject)
        self.queryBrowser.dbcon_obj.new_connection()
        self.queryBrowser.create_mapper_for_all_classes()
        print 'Database Connection Established'


    def close_databaseConnection(self):
        pass

    def establish_cacheDatabase(self, fileLoc, mode='w'):
        self.db = DB(fileLoc, mode)
        if mode == 'w':
            self.db.create()
        # placeholders for creating the hdf5 tables
        # only the network data is read and processed for faster
        # queries
        self.db.createTableFromDatabase('travel_skims', self.queryBrowser)


    def run_components(self):
        t_c = time.time()
        componentList = self.configParser.parse_models()

        subsample = self.projectConfigObject.subsample

        for i in componentList:
            for j in i.model_list:
                print j.dep_varname
            #self.queryBrowser.dbcon_obj.new_sessionInstance()
            tableName = i.table
            print '\nFor component - %s deleting corresponding table - %s' %(i.component_name, tableName)
            # clean the run time tables
            #delete the delete statement; this was done to clean the tables during testing
            self.queryBrowser.delete_all(tableName)
        #self.queryBrowser.dbcon_obj.close_sessionInstance()

        for i in componentList:
            # Create New Instance of the Session
            #self.queryBrowser.dbcon_obj.new_sessionInstance()

            t = time.time()
            print '\nRunning Component - %s; Analysis Interval - %s' %(i.component_name,
                                                                       i.analysisInterval)

            # Prepare variable list/objects for retrieving the corresponding records for processing
            variableList = i.variable_list

            #print '\tVariable List - ', len(variableList)
            vars_dict, depvars_dict, prim_keys, count_keys = self.prepare_vars(variableList, i)

            #Spatial Constraints list
            spatialConst_list = i.spatialConst_list

            #print '\nVARS BEFORE REMOVING TEMP', vars_dict
            # Exclude the temp variables
            if 'temp' in vars_dict:
                temp_tableEntries = vars_dict.pop('temp')
                temp_dict = {'temp':temp_tableEntries}

                depvars_dict = self.update_dictionary(depvars_dict, temp_dict)

                #print 'VARS AFTER REMOVING TEMP', vars_dict
                #print type(temp_tableEntries)


            tableName = i.table

            analysisInterval = i.analysisInterval


            # Prepare Data
            data = self.prepare_data(vars_dict, depvars_dict, count_keys,
                                     spatialConst_list, analysisInterval, subsample)
            # Append the Spatial Query Results
            # data = self.process_spatial_query(data, i.spatialConst_list)

            #if i.component_name == 'MorningVertex' or i.component_name == 'EveningVertex':
            #    print 'Data', data.columns(['houseid', 'personid', 'scheduleid']).data

            # Run the component
            nRowsProcessed = i.run(data, self.db)

            if i.component_name == 'AfterSchoolActivities':
                f = open('test_res', 'a')
                f.write('%s,rows - %s\n' %(i.component_name, nRowsProcessed))
                f.close()

                #if nRowsProcessed <> 6:
                #    raw_input()



            # Write the data to the database from the hdf5 results cache
            if i.key[1] is not None:
                keyCols = i.key[0] + i.key[1]
            else:
                keyCols = i.key[0]
            self.reflectToDatabase(tableName, keyCols, nRowsProcessed)

            print '-- Finished simulating model --'
            print '-- Time taken to complete - %.4f' %(time.time()-t)
            #print raw_input('-- Press any key to continue... --')
            # Create New Instance of the Session
            #self.queryBrowser.dbcon_obj.close_sessionInstance()
            #raw_input()
        print '-- TIME TAKEN  TO COMPLETE ALL COMPONENTS - %.4f' %(time.time()-t_c)

    def reflectToDatabase(self, tableName, keyCols=[], nRowsProcessed=0):
        """
        This will reflect changes for the particular component to the database
        So that future queries can fetch appropriate run-time columns as well
        because the output is currently cached on the hard drive and the queries
        are using tables in the database which only contain the input tables
        and hence the need to reflect the run-time caches to the database
        """

        #self.queryBrowser.inser_into_table(data.data
        table = self.db.returnTableReference(tableName)


        #resIterator = table.iterrows()
        #t = time.time()
        #resArr = [row[:] for row in resIterator]
        #print """\tCreating the array object (iterating through the hdf5 results) """\
        #    """to insert into tbale - %.4f""" %(time.time()-t)
        #print type(resArr)

        t = time.time()

        print '\tNumber of rows processed in this iteration - ', nRowsProcessed
        if nRowsProcessed == 0:
            return
        resArr = list(table[-nRowsProcessed:])
        print """\tCreating the array object (WITHOUT iterating through the hdf5 results) """\
            """to insert into tbale - %.4f""" %(time.time()-t)
        colsToWrite = table.colnames

        #print resArr
        # TODO: delete rows from the local cache
        # In the current implementation, the rows are deleted before every update so that replication is not  done
        # in actual implementation, the local cache should be wiped clean so as to avoid the latency of
        # inserting old rows and creating indices for them

        #self.queryBrowser.delete_all(tableName)
        self.queryBrowser.insert_into_table(resArr, colsToWrite, tableName, keyCols, chunkSize=100000)


    def prepare_vars(self, variableList, component):
        #print variableList
        indep_columnDict = self.prepare_vars_independent(variableList)
        #print '\tIndependent Column Dictionary - ', indep_columnDict

        tempdep_columnDict = {'temp':[]}
        spatialquery_columnDict = {}
        dep_columnDict = {}
        prim_keys = {}
        count_keys = {}


        depVarTable = component.table

        if component.key[0] is not None:
            prim_keys[depVarTable] = component.key[0]
        if component.key[1] is not None:
            count_keys[depVarTable] = component.key[1]


        for submodel in component.model_list:

            depVarName = submodel.dep_varname

            if isinstance(submodel.model, InteractionModel):
                tempdep_columnDict['temp'].append(depVarName)
            else:
                #depVarTable = model.table
                if depVarTable in indep_columnDict:
                    if depVarName in indep_columnDict[depVarTable]:
                        continue

                if depVarTable in dep_columnDict:
                    dep_columnDict[depVarTable].append(depVarName)
                else:
                    dep_columnDict[depVarTable] = [depVarName]


        #print '\tDependent Column Dictionary - ', dep_columnDict
        #print '\tDependent Column Dictionary - ', tempdep_columnDict
        #print '\tPrimary Keys - ', prim_keys
        #print '\tIndex Keys - ', count_keys

        #columnDict = self.update_dictionary(indep_columnDict, dep_columnDict)
        indep_columnDict = self.update_dictionary(indep_columnDict, prim_keys)
        indep_columnDict = self.update_dictionary(indep_columnDict, count_keys)

        if len(tempdep_columnDict['temp']) > 0:
            dep_columnDict = self.update_dictionary(dep_columnDict, tempdep_columnDict)

        #print '\tIndependent Column Dictionary - ', indep_columnDict
        #print '\tDependent Column Dictionary - ', dep_columnDict
        return indep_columnDict, dep_columnDict, prim_keys, count_keys


    def prepare_vars_independent(self, variableList):
        # Here we append attributes for all columns that appear on the RHS in the
        # equations for the different models
        #print variableList

        indepColDict = {}
        for i in variableList:
            tableName = i[0]
            colName = i[1]
            if tableName in indepColDict:
                indepColDict[tableName].append(colName)
            else:
                indepColDict[tableName] = [colName]

        return indepColDict


    def update_dictionary(self, dict_master, dict_to_merge):
        dict_m = copy.deepcopy(dict_master)

        for key in dict_to_merge:
            if key in dict_m:
                dict_m[key] = list(set(dict_m[key] + dict_to_merge[key]))
            else:
                dict_m[key] = dict_to_merge[key]

        return dict_m

    def return_keys_toinclude(self, keys, prim_keys_ind=None):
        keysList = []
        keysNoDuplicates = {}
        for i in keys:
            if prim_keys_ind and i.find('_r') > -1:
                #print 'primary keys and _r (result) table found'
                continue
            if len(set(keys[i]) & set(keysList)) == 0:
                keysNoDuplicates[i] = keys[i]
                keysList = keysList + keys[i]
                #print '%s not in - ' %(i), keysList, i not in keysList
        return keysNoDuplicates

    def process_anchors(self, columnDict, anchor):
        anchor_cols = []
        anchor_cols.append(anchor.locationField)

        if anchor.timeField is not None:
            anchor_cols.append(anchor.timeField)


        if anchor.table in columnDict:
            cols = columnDict[anchor.table]
            columnDict[anchor.table] = list((set(cols) |
                                             set(anchor_cols)))
        else:
            columnDict[anchor.table] = anchor_cols

        #print columnDict
        #raw_input()
        return columnDict

    def prepare_data(self, indepVarDict, depVarDict,
                     count_keys=None, spatialConst_list=None,
                     analysisInterval=None, subsample=None):
        # get hierarchy of the tables

        #print indepVarDict

        # PROCESSING TO INCLUDE THE APPROPRIATE SPATIAL QUERY ANCHORS
        if spatialConst_list is not None:
            # Removing those table/column entries which will be processed
            # separately
            spatialQryTables = []
            for i in spatialConst_list:
                if i.table not in spatialQryTables:
                    spatialQryTables.append(i.table)

            #print 'SPATIAL QRY TABLES', spatialQryTables
            spatialQryDict = {}
            for i in spatialQryTables:
                if i in indepVarDict:
                    spatialQryDict[i] = indepVarDict.pop(i)
            # Include those variables that will be used to process the spatial
            # queries for example the htaz, wtaz etc.


            #Processing Anchors for variables to be included
            for i in spatialConst_list:
                if i.countChoices is None:
                    # Adding the columns that can then be used to retrieve the
                    # respective skims
                    stAnchor = i.startConstraint
                    endAnchor = i.endConstraint
                    indepVarDict = self.process_anchors(indepVarDict, stAnchor)
                    indepVarDict = self.process_anchors(indepVarDict, endAnchor)

                # the above cols are added for travel time type queries as they fit in the current
                # select join query build framework

                # the cols for time space prism vertices will be added to the query in real time
                # as they don't quite fit into the current setup



        tableOrderDict, tableNamesKeyDict = self.configParser.parse_tableHierarchy()
        #print 'TABLE ORDER DICT', tableOrderDict
        #print 'TABLE NAMES KEY DICT', tableNamesKeyDict

        orderKeys = tableOrderDict.keys()
        orderKeys.sort()

        tableNamesOrderDict = {}
        #tableNamesKeyDict = {}
        for i in orderKeys:
            tableNamesOrderDict[tableOrderDict[i][0]] = i
            #tableNamesKeyDict[tableOrderDict[i][0]] = tableOrderDict[i][1]

        #print 'TABLE NAMES ORDER', tableNamesOrderDict
        # table order
        tableNamesForComponent = indepVarDict.keys()
        #print 'TABLE NAMES FOR COMPONENT', tableNamesForComponent

        found = []
        for i in list(set(tableNamesForComponent) & set(tableNamesOrderDict.keys())):
            order = tableNamesOrderDict[i]
            minOrder = min(tableNamesOrderDict.values())
            found.insert(order-minOrder, i)
            tableNamesForComponent.remove(i)

        #print 'COMPONENT TABLES AFTER', tableNamesForComponent
        #print 'HIERARCHY TABLES FOUND - ', found
        #inserting back the ones that have a hierarchy defined
        tableNamesForComponent = found + tableNamesForComponent

        #print '\ttableNamesforComponent - ', tableNamesForComponent

        # replacing with the right keys for the main agents so that zeros are not
        # returned by the query statement especially for the variables defining the
        # agent id's
        #print 'BEFORE FIXING INDEX KEYS', indepVarDict

        found.reverse() # so that the tables higher in the hierarchy are fixed last; lowest to highest now

        for i in found:
            key = tableNamesKeyDict[i][0]
            for table in indepVarDict:
                intersectKeyCols = set(key) & set(indepVarDict[table])
                if len(intersectKeyCols) > 0:
                    indepVarDict[table] = list(set(indepVarDict[table]) - intersectKeyCols)

                    if i in indepVarDict:
                        indepVarDict[i] = indepVarDict[i] + list(intersectKeyCols)
                    else:
                        indepVarDict[i] = intersectKeyCols
        #print 'AFTER FIXING INDEX KEYS', indepVarDict

        found.reverse() # reversing back the heirarchy to go from highest to lowest

        # matching keys
        matchingKey = {}
        mainTable = found[0]
        #print 'mainTable', mainTable
        mainTableKeys = tableNamesKeyDict[mainTable][0]

        for i in indepVarDict.keys():
            if i == mainTable:
                continue
            else:
                matchTableKeys = tableNamesKeyDict[i][0]
            matchingKey[i] = list((set(mainTableKeys) and set(matchTableKeys)))
        #print 'MATCHING KEY DICTIONARY', matchingKey
        #raw_input()

        #for i in found:
        #    if i in indepVarDict:
        #        matchingKey = tableNamesKeyDict[i][0]
        #        break

        #print '\tMATCHING KEY - ', matchingKey
        # count dictionary or max dictionary
        if len(count_keys) == 0:
            max_dict = None
        else:
            max_dict = count_keys

        #print 'COLUMN DICTIONARY', indepVarDict
        #print 'TABLE HIERARCHY', tableNamesForComponent
        #print 'MATCHING COLUMN', matchingKey
        #maxDict = {'vehicles_r':['vehid']}

        # Cleaning up the independent variables dictionary
        iterIndepDictKeys = indepVarDict.keys()
        for i in iterIndepDictKeys:
            if len(indepVarDict[i]) == 0:
                indepVarDict.pop(i)

        data = self.queryBrowser.select_join(indepVarDict,
                                             matchingKey,
                                             tableNamesForComponent,
                                             max_dict,
                                             spatialConst_list,
                                             analysisInterval,
                                             subsample)

        self.append_cols_for_dependent_variables(data, depVarDict)
        self.process_data_for_locs(data, spatialConst_list)
        return data


    def append_cols_for_dependent_variables(self, data, depVarDict):
        #print 'INSERTING FOLLOWING DEPENDENT COLS', depVarDict

        numRows = data.rows
        tempValsArr = zeros((numRows,1))
        for i in depVarDict:
            colsInTable = depVarDict[i]
            colsInTable.sort()
            for j in colsInTable:
                data.insertcolumn([j], tempValsArr)

    def process_data_for_locs(self, data, spatialConst_list):
        """
        This method is called whenever there are location type queries involved as part
        of the model run. Eg. In a Destination Choice Model, if there are N number of
        random location choices, and there is a generic MNL specifcation then in addition
        to generating the choices, one has to also retrieve the travel skims corresponding
        to the N random location choices.
        """
        # LOAD THE NETWORK SKIMS ON THE MEMORY AS NUMPY ARRAY
        t = time.time()

        if spatialConst_list is not None:
            for i in spatialConst_list:
                tableName = i.table
                originColName = i.originField
                destinationColName = i.destinationField
                skimColName = i.skimField

                skimsMatrix, uniqueIDs = self.db.returnTableAsMatrix(tableName,
                                                                     originColName,
                                                                     destinationColName,
                                                                     skimColName)
                if i.countChoices is not None:
                    print '\n\tNeed to sample location choices for the following model'
                    self.sample_location_choices(data, skimsMatrix, uniqueIDs, i)
                else:
                    print '\n\tNeed to extract skims'
                    self.extract_skims(data, skimsMatrix, i)

        #raw_input()
        return data


    def sample_location_choices(self, data, skimsMatrix, uniqueIDs, spatialconst):
        # extract destinations subject to the spatio-temporal
        # constraints

        originLocColName = 'st_%s' %(spatialconst.startConstraint.locationField)
        destinationLocColName = 'en_%s' %(spatialconst.endConstraint.locationField)

        originTimeColName = 'st_%s' %(spatialconst.startConstraint.timeField)
        destinationTimeColName = 'en_%s' %(spatialconst.endConstraint.timeField)

        # insert column for data availability
        originLocColVals = array(data.columns([originLocColName]).data, dtype=int)
        destinationLocColVals = array(data.columns([destinationLocColName]).data, dtype=int)


        originTimeColVals = array(data.columns([originTimeColName]).data, dtype=int)
        destinationTimeColVals = array(data.columns([destinationTimeColName]).data, dtype=int)


        timeAvailable = destinationTimeColVals - originTimeColVals

        destLocSetInd = zeros((data.rows, max(uniqueIDs) + 1), dtype=float)

        for zone in uniqueIDs:
            destZone = zone * ones((data.rows, 1), dtype=int)
            timeToDest = skimsMatrix[originLocColVals, destZone]
            timeFromDest = skimsMatrix[destZone, destinationLocColVals]

            #print 'TIME TO DEST', zone, min(timeToDest), max(timeToDest)
            #print 'TIME FROM DEST', zone, min(timeFromDest), max(timeFromDest)

            rowsLessThan = (timeToDest + timeFromDest < timeAvailable)[:,0]
            destLocSetInd[rowsLessThan, zone] = 1

        destLocSetInd = ma.masked_equal(destLocSetInd, 0)

        #print 'ORIGIN LOCS', originLocColVals[:5, 0]
        #print 'DESTINATION LOCS', destinationLocColVals[:5, 0]
        #print 'TIME AVAILABLE', timeAvailable[:5, 0]
        #print destLocSetInd.sum(-1)

        #destLocSetIndSum = destLocSetInd.sum(-1)

        #probLocSet = (destLocSetInd.transpose()/destLocSetIndSum).transpose()


        zoneLabels = ['geo-%s'%(i+1) for i in range(max(uniqueIDs)+1)]
        #probDataArray = DataArray(probLocSet, zoneLabels)

        sampleVarDict = {'temp':[]}
        sampleVarName = spatialconst.sampleField

        for i in range(spatialconst.countChoices):
            sampleVarDict['temp'].append('%s%s' %(sampleVarName, i+1))

        self.append_cols_for_dependent_variables(data, sampleVarDict)
        #print data.varnames
        #print destLocSetInd.sum(-1)

        seed = spatialconst.seed
        count = spatialconst.countChoices
        sampledChoicesCheck = True
        while (sampledChoicesCheck):
            print '\tSampling Locations'
            self.sample_choices(data, destLocSetInd, zoneLabels, count, sampleVarName, seed)
            sampledVarNames = sampleVarDict['temp']
            sampledChoicesCheck = self.check_sampled_choices(data, sampledVarNames)
            seed = seed + 1




        #originLocColName = spatialconst.startConstraint.locationField
        #originLocColVals = array(data.columns([originLocColName]).data, dtype=int)

        for i in range(count):
            sampleLocColName = '%s%s' %(sampleVarName, i+1)
            sampleLocColVals = array(data.columns([sampleLocColName]).data, dtype=int)

            vals = skimsMatrix[originLocColVals, sampleLocColVals]
            skimLocColName = '%s%s' %(spatialconst.skimField, i+1)
            #print skimLocColName
            data.setcolumn(skimLocColName, vals)
        colsInTable = sampleVarDict['temp']
        colsInTable.sort()
        #print data.columns(colsInTable + [originLocColName])
        #tt = data.columns(['tt1', 'tt2', 'tt3', 'tt4', 'tt5'])
        #print tt
        print '\tTravel skims extracted for the sampled locations'
        #raw_input()




    def extract_skims(self, data, skimsMatrix, spatialconst):

        # hstack a column for the skims that need to be extracted for the
        # location pair
        originLocColName = spatialconst.startConstraint.locationField
        destinationLocColName = spatialconst.endConstraint.locationField

        originLocColVals = array(data.columns([originLocColName]).data, dtype=int)
        destinationLocColVals = array(data.columns([destinationLocColName]).data, dtype=int)

        vals = skimsMatrix[originLocColVals, destinationLocColVals]
        #vals.shape = (data.rows,1)
        data.insertcolumn(['tt'], vals)




    def sample_choices(self, data, destLocSetInd, zoneLabels, count, sampleVarName, seed):
        for i in range(count):
            destLocSetIndSum = destLocSetInd.sum(-1)
            #print 'NUMBER OF DESTINATIONS', destLocSetInd
            probLocSet = (destLocSetInd.transpose()/destLocSetIndSum).transpose()
            #print probLocSet.shape, 'PROBABILITY SHAPE'
            #raw_input()
            probDataArray = DataArray(probLocSet, zoneLabels)

            # seed is the count of the sampled destination starting with 1
            probModel = AbstractProbabilityModel(probDataArray, seed+i)
            res = probModel.selected_choice()

            # Assigning the destination
            # We subtract -1 from the results that were returned because the
            # abstract probability model returns results indexed at 1
            # actual location id = choice returned - 1

            colName = '%s%s' %(sampleVarName, i+1)
            nonZeroRows = where(res.data <> 0)
            actualLocIds = res.data
            actualLocIds[nonZeroRows] -= 1
            data.setcolumn(colName, actualLocIds)

            # Retrieving the row indices
            dataCol = data.columns([colName]).data
            rowIndices = array(xrange(dataCol.shape[0]), int)
            colIndices = actualLocIds.astype(int)
            #print res.data.shape
            destLocSetInd[rowIndices, colIndices] = 0
        #print data.varnames

    def check_sampled_choices(self, data, sampledVarNames):
        for i in range(len(sampledVarNames)):
            varName = sampledVarNames[i]
            checkAgainstVarNames = sampledVarNames[i+1:]
            for j in checkAgainstVarNames:
                columnI = data.columns([varName]).data
                columnJ = data.columns([j]).data
                check = data.data[where(columnI[where(columnI == columnJ)] <> 0)]
                if check.shape[0] > 0:
                    #print check
                    #print columnI[:,0]
                    #print columnJ[:,0]
                    #raw_input()
                    print '\t -- Warning:Choices are repeated; Repeating location sampling step --'
                    return True

        print '\t -- Choices are not repeated --'
        return False

                #xraw_input()







        """
        tableName = 'travel_skims'
        table = self.db.returnTableReference(tableName)

        origin = table.col('origin')
        destination = table.col('destination')
        tt = table.col('tt')

        ttMatrix = zeros((max(origin)+1, max(destination)+1))

        ttMatrix[origin, destination] = tt

        originQ = 110
        destinationQ = 1745
        timeWindow = 45

        randint = random.randint

        destMatrix = zeros((10000, max(destination) + 1))


        #print ttToDest.shape, ttFromDest.shape
        for i in range(4000):
            originQ = randint(101, 2095)
            destinationQ = randint(101, 2095)
            timeWindow = randint(15, 60)
            ttToDest = ttMatrix[originQ,:]
            ttFromDest = ttMatrix[:,destinationQ]
            dest = ttToDest + ttFromDest < 45
            #destMatrix[i, dest] = 1

        print 'time taken - %.4f' %(time.time()-t)

        print 'travel skims read'
        raw_input()

        print cols
        queryData = array([i[:] for i in query_gen])

        mask = array == None
        mask = ma.masked_values(queryData, None).mask
        queryData = array(queryData)
        queryData[mask] = 0
        data = DataArray(queryData, cols)
        from numpy import where
        t = time.time()
        print 'start'

        print sum(data.columns(['origin']).data == 101), sum(data.columns(['destination']).data == 1994)
        print 'end', time.time()-t
        raw_input()
        """

# Storing data ??
# Linearizing data for calculating activity-travel choice attributes??
# how to update data like schedules, open periods etc.??

# create component list object
# iterate through component list
# - read the variable list
# - retrieve data
# - process the data further for retrieving accessibilities <>
# - update model objects/equation specifications for generic choice models
# - simulate
# -


if __name__ == '__main__':
    fileloc = '/home/kkonduri/simtravel/test/vehown'
    componentManager = ComponentManager(fileLoc = "%s/config.xml" %fileloc)
    for i in range(1):
        f = open('test_res', 'a')
        f.write('Run - %s' %(i+1))
        f.close()
        componentManager.establish_databaseConnection()
        componentManager.establish_cacheDatabase(fileloc, 'w')
        componentManager.run_components()
        componentManager.db.close()
