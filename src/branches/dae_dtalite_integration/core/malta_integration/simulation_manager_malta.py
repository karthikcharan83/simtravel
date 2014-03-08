print '-- INSIDE OPENAMOS --'
import copy
import time
import os
import csv
import traceback
import sys
from lxml import etree
from numpy import array, ma, ones, zeros, vstack, where, save, load

from openamos.core.malta_integration.config_parser_malta import ConfigParser
from openamos.core.database_management.cursor_query_browser import QueryBrowser
from openamos.core.errors import ConfigurationError
from openamos.core.data_array import DataArray
from openamos.core.malta_integration.dataset_malta import DB
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.models.interaction_model import InteractionModel
from openamos.core.travel_skims.skimsprocessor import SkimsProcessor
from openamos.core.travel_skims.successive_average_link_skims import SuccessiveAverageLinkAttributes

#from multiprocessing import Process

class SimulationManager(object):
    """
    The class reads the configuration file, creates the component and model objects,
    and runs the models to simulate the various activity-travel choice processes.

    If the configObject is invalid, then a valid fileLoc is desired and if that fails
    as well then an exception is raised. In a commandline implementation, fileLoc will
    be passed.
    """

    def __init__(self):
	#, configObject=None, fileLoc=None, component=None):
	#TODO: REMOVE PLACEHOLDER 
	fileLoc = '/workspace/openamos/configs/mag_zone/config_mag_malta.xml'
	configObject = None


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
            configObject = etree.parse(fileLoc)
        except AttributeError, e:
            raise ConfigurationError, """The file location is not a valid."""
        except IOError, e:
            print e
            raise ConfigurationError, """The path for configuration file was """\
                """invalid or the file is not a valid configuration file."""

        self.configObject = configObject
        self.configParser = ConfigParser(configObject) #creates the model configuration parser
        self.projectConfigObject = self.configParser.parse_projectAttributes()
        self.projectSkimsObject = self.configParser.parse_network_tables()
        self.projectLocationsObject = self.configParser.parse_locations_table()

	self.setup_databaseConnection()
	self.setup_cacheDatabase()
	self.setup_location_information()
	self.parse_config()
	self.clean_database_tables()
        self.idCount = 0
        self.idList = []
	self.lastTtTableLoc = None
	self.skimsMatrix = SkimsProcessor(1, 1995)
        self.uniqueIds = None
	self.trips = 0


    def setup_databaseConnection(self):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        self.queryBrowser = QueryBrowser(dbConfigObject)
        self.queryBrowser.dbcon_obj.new_connection()
        #self.queryBrowser.create_mapper_for_all_classes()
        #print 'Database Connection Established'


    def setup_cacheDatabase(self):
	self.db = DB()


    def createLocationsTableFromDatabase(self, tableInfo):
        t = time.time()
        
        colsList = [tableInfo.location_id_var] + tableInfo.locations_varsList

        tableName = tableInfo.tableName
        data = self.queryBrowser.select_all_from_table(tableName, colsList)
        print '\tTotal time taken to retrieve records from the database %.4f' %(time.time()-t)

	fileLoc = self.projectConfigObject.location
	
	dataCp = array(data.data) # the new numpy doesn't work with masked array and hence the conversion ... 
	save('%s/%s.npy' %(fileLoc, tableName), dataCp)

        print '\tTime taken to write to numpy cache format %.4f' %(time.time()-t)

	    

    def setup_location_information(self):
        print "-- Processing Location Information --"
        self.createLocationsTableFromDatabase(self.projectLocationsObject)


 
    def parse_config(self):
        print "-- Parsing components and model specifications --"
        self.componentList = self.configParser.parse_models()

	# Store original seed to replicate the same as stand-alone OpenAMOS run
	self.modSeedDict = {}
	for comp in self.componentList:
	    for mod in comp.model_list:
	    	self.modSeedDict[(comp.component_name, mod.dep_varname)] = copy.deepcopy(mod.seed)


        #TODO: implement subsample runs 
        self.subsample = self.projectConfigObject.subsample

        # Printing models that were parsed
        modelCount = 0
        for comp in self.componentList:
            #print '\n\tFor component - %s ' %(comp.component_name)
            #print "\t -- Model list including model formulation and data filters if any  -- "
            #print '\tPost Run Filters - ', comp.post_run_filter
            for mod in comp.model_list:
                #print "\t\t - name:", mod.dep_varname, ",formulation:", mod.model_type, ",filter:", mod.data_filter
                modelCount += 1

        print "\tTotal of %s components and %s models will be processed" %(len(self.componentList), modelCount)
        print "\t - Note: Some models/components may have been added because of the way OpenAMOS framework is setup."
        #raw_input()

    def clean_database_tables(self):
        tableNamesDelete = []
        for comp in self.componentList:
            # clean the run time tables
            tableName = comp.writeToTable
            if tableName not in tableNamesDelete:
		if (comp.writeToTable == 'schedule_final_r' 
		    or comp.writeToTable == 'persons_location_r'
		    or comp.writeToTable == 'persons_history_r'):
		    continue
                tableNamesDelete.append(tableName)
                print "\tDeleting records in the output table - %s before simulating choices again" %(tableName)
                self.queryBrowser.delete_all(tableName)                            


    def run_selected_components_for_malta(self, analysisInterval, tripInfoArrivals=array([])):
	try:
            tripInfo = self.run_components(analysisInterval, tripInfoArrivals)
	except Exception, e:
	    print 'Error occurred: ', e
	    traceback.print_exc(file=sys.stdout)		
	    raw_input()
	    raise Exception, 'Error occurred when executing component - %s: %s'%(comp.component_name, e)
	return tripInfo
	
    def run_components(self, analysisInterval, tripInfoArrivals):

        print '-- INSIDE OpenAMOS generating activity-trvel records -- '
	print 'These are trips that arrived - '
	#return zeros((1,11))
	ti = time.time()

	print tripInfoArrivals

        # To test python simulation_manager_cursor.py use dummy arrival info

	if tripInfoArrivals.shape[0] > 1 or (tripInfoArrivals.shape[0] == 1 and tripInfoArrivals[0] <> -1):
	    arrSize = tripInfoArrivals.shape[0]
            dataVals = zeros((arrSize/2, 3))
            dataVals[:,0] = tripInfoArrivals[:arrSize/2]
            dataVals[:,1] = analysisInterval - 1
	    dataVals[:,2] = tripInfoArrivals[arrSize/2:]

            data = DataArray(dataVals, ['tripid', 'arrivaltime', 'distance'])
        else:
            data = None

	t_c = time.time()

        # The analysis interval returned is the end of the analysis interval
        # In openamos everything is referenced to the start of the analysis Interval
        # openamos analysisInterval = above_analysisInterval - 1

        fileLoc = self.projectConfigObject.location
	print ('Starting to process...')
	if analysisInterval > 180 and analysisInterval <= 359:
	    #self.lastTableName = None
	    pass

	for comp in self.componentList:
            t = time.time()
            comp.analysisInterval = analysisInterval - 1
            print '\nRunning Component - %s; Analysis Interval - %s' %(comp.component_name,
                                                                       comp.analysisInterval)

            if comp.component_name == 'ArrivalTimeInformation':
                comp.db = self.db
            
            else:
                if comp.skipFlag:
                    print '\tSkipping the run for this component'
                    continue

		# Reset seed 
		for mod in comp.model_list:
		    mod.seed = self.modSeedDict[(comp.component_name, mod.dep_varname)] + analysisInterval - 1

                #Load skims matrix outside so that when there is temporal aggregation
                # of tod skims then loading happens only so many times
		
		t_sk = time.time()
                ttTableLoc, distTableLoc = self.identify_skims_matrix(comp)


                if ttTableLoc <> self.lastTtTableLoc and (len(comp.spatialConst_list) > 0 or 
							len(comp.dynamicspatialConst_list) > 0):
		    #raw_input("check size before ...") 

                    #self.skimsMatrix, self.uniqueIds = self.load_skims_matrix(comp, tableName)
		    self.load_skims_matrix(comp, ttTableLoc, distTableLoc)
                    self.lastTtTableLoc = ttTableLoc
		    #raw_input("check size after ...") 
                elif ttTableLoc == self.lastTtTableLoc:
		    pass

		print '\tTime taken to process skims %.4f' %(time.time()-t_sk)
                data = comp.pre_process(self.queryBrowser, 
                                        self.skimsMatrix, self.db, fileLoc)


            if data is not None:
                #print 'inside here for component - ', comp.component_name
		if comp.component_name == "ExtractAllTravelEpisodes":
		    tripInfo = comp.run(data, self.queryBrowser, 
			    self.skimsMatrix, self.uniqueIds, fileLoc)
		    print 'Origin Zone Ids Before - ', tripInfo[:5,5]
		    print 'Destination Zone Ids Before - ', tripInfo[:5,6]
		    tripInfo[:,5] += 11
		    tripInfo[:,6] += 11
		    print 'Origin Zone Ids After Mod - ', tripInfo[:5,5]
		    print 'Destination Zone Ids After Mod - ', tripInfo[:5,6]
		    #raw_input()
		else:
		    comp.run(data, self.queryBrowser, 
			    self.skimsMatrix, self.uniqueIds, fileLoc)

		
		    

            elif data is None and comp.component_name == "ExtractAllTravelEpisodes":
                tripInfo = zeros((1,11))
		"""
                tripInfo = zeros((3,11))

		self.trips += 1
		tripInfo[0,0] = self.trips
		tripInfo[0,5] = 1850 + 11
		tripInfo[0,6] = 1075 + 11 

		self.trips += 1
		tripInfo[1,0] = self.trips
		tripInfo[1,5] = 1488 + 11
		tripInfo[1,6] = 1074 + 11 

		self.trips += 1
		tripInfo[2,0] = self.trips
		tripInfo[2,5] = 28 + 11
		tripInfo[2,6] = 1995 + 11 
		"""
            print '\t-- Finished simulating component; time taken %.4f --' %(time.time()-t)


	tripInfo = tripInfo.astype(int)



	print '-- Number of trip records that are being passed from OpenAMOS is - %s --' %(tripInfo.shape[0])
	print '\t Time taken to retrieve trips for the simulation interval - %.4f' %(time.time()-ti)

	#raw_input()

	return tripInfo

    def identify_skims_matrix(self, comp):
        ti = time.time()
        if len(comp.spatialConst_list) == 0 and len(comp.dynamicspatialConst_list) == 0:
            # When there are no spatial constraints to be processed
            # return an empty skims object
            ttTableLocation = None
	    distTableLocation = None
            pass
        else:
            analysisInterval = comp.analysisInterval
        
            if comp.analysisInterval is not None:
                ttTableLocation = self.projectSkimsObject.lookup_ttTableLocation(analysisInterval)
		distTableLocation = self.projectSkimsObject.lookup_distTableLocation(analysisInterval)
            else:
                # Corresponding to the morning peak
                # currently fixed can be varied as need be
                ttTableLocation = self.projectSkimsObject.lookup_ttTableLocation(240)
		distTableLocation = self.projectSkimsObject.lookup_distTableLocation(240)

        print '\tSkims Matrix Identified in - %.4f' %(time.time()-ti)
        return ttTableLocation, distTableLocation


    def load_skims_matrix(self, comp, ttTableLocation, distTableLocation):

	print 'tt Table Location - ', ttTableLocation
	print 'dist Table Location - ', distTableLocation

	#raw_input("check memory before creating travel skims -- ")
	self.skimsMatrix.set_tt_fileString(ttTableLocation)
	self.skimsMatrix.set_dist_fileString(distTableLocation)
	self.skimsMatrix.create_graph()
	
	print 'TRAVEL Skims object created --'
	#raw_input("check memory after distance skims -- ")
	print 'Check travel times -- ', self.skimsMatrix.get_travel_times(array([1,2,3,4]), array([1,2,3,4]))
	print 'Check distances -- ', self.skimsMatrix.get_travel_distances(array([1,2,3,4]), array([1,2,3,4]))
	print 'Check generalized cost tt + dist*2 -- ', self.skimsMatrix.get_generalized_time(array([1,2,3,4]), array([1,2,3,4]))


    def close_connections(self):
        self.queryBrowser.dbcon_obj.close_connection()
        self.db.close()

if __name__ == '__main__':
    simulationObject = SimulationManager()

    for i in range(1400):
    	simulationObject.run_selected_components_for_malta(0 + i)
    #raw_input()
    #simulationObject.run_selected_components_for_malta(191)
    #raw_input()
    #simulationObject.run_selected_components_for_malta(192)
    #raw_input()

