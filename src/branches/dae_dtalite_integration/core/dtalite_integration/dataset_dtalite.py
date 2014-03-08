import time

from numpy import unique, int64, int32, float32, float64, load
from numpy.ma import zeros, masked_equal, ones
from openamos.core.data_array import DataArray

class DB(object):
    def __init__(self):
    
        # TODO: where do we get the table definitions and relationships from
        # for now this is static



	self.tableCols = {'travel_skims':['origin', 'destination', 'tt'], 
			  'locations':['locationid', 'retail_employment', 'office_employment', 'public_employment',
				       'industrial_employment', 'other_employment',
				       'retail_employment_density', 'office_employment_density', 'public_employment_density', 
				       'other_employment_density',
				       'total_area', 'low_income', 'lowest_income', 'high_income',
				       'institutional_population', 'groupquarter_households',
				       'residential_households'],
			  'households_vehicles_count_r':['houseid', 'vehcount'],
			  'vehicles_r':['houseid', 'vehid', 'vehtype'],
			  'schedule_r':['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
  			  'schedule_ltrec_r':['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_cleanfixedactivityschedule_r':['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_childreninctravelrec_r':['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_conflictrec_r':['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_inctravelrec_r':['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_dailyallocrec_r':['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_final_r':['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid', 'tripcount'],
			  'schedule_elapsed_r':['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid', 'tripcount'],

			  'trips_r':['houseid', 'personid', 'vehid', 'tripmode', 'fromzone', 'tozone', 'starttime', 'endtime', 'trippurposefrom', 
				     'trippurpose', 'duration', 'occupancy', 'tripind', 'dependentpersonid', 'tripwithhhmember', 
				     'lasttripdependentpersonid', 'lastoccupancy', 'starttripcount', 'endtripcount',
				     'startdependentpersonid', 'enddependentpersonid', 'tripcount', 'lasttripcount'],

			  'trips_with_nonhh_r':['houseid', 'personid', 'vehid', 'tripmode', 'fromzone', 'tozone', 'starttime', 'endtime', 'trippurposefrom', 
				     'trippurpose', 'duration', 'occupancy', 'dependentpersonid'],

			  'trips_to_malta_r':['tripid', 'houseid', 'personid', 'vehid', 'tripmode', 
					      'fromzone', 'tozone', 'starttime', 'endtime', 'trippurpose', 'duration', 
					      'dependentpersonid', 'persononnetworkflag'],
			  'current_occupancy_r':['houseid', 'personid', 'tripid', 'occupancy', 'dependentpersonid', 'tripcount'],
			  'trips_invalid_r':['tripid', 'tripind'],
			  'trips_arrival_from_malta_r':['tripid', 'arrivaltime', 'distance'],
			  'trips_arrival_from_openamos_r':['tripid', 'arrivaltime'],
			  'persons_arrived_r':['houseid', 'personid', 'tripid', 'expectedstarttime', 
					       'expectedarrivaltime', 'actualarrivaltime', 'tripdependentpersonid', 'fromzone', 'tozone', 'tripcount'],
			  'persons_arrived_from_openamos_r':['houseid', 'personid', 'tripid', 'expectedstarttime', 
					       'expectedarrivaltime', 'actualarrivaltime', 'tripdependentpersonid', 'fromzone', 'tozone', 'tripcount'],
			  'persons_arrived_id_r':['houseid', 'personid', 'actualarrivaltime', 'expectedarrivaltime', 
						  'tripdependentpersonid', 'tozone', 'personuniqueid', 'tripcount'],
			  #'persons_leaving_id_r':['tripid', 'houseid', 'personid', 'personuniqueid', 'starttime', 'fromzone', 'tripcount'],
			  'persons_leaving_id_r':['tripid', 'houseid', 'personid', 'starttime', 'fromzone', 'tripcount'],
			  'persons_leaving_valid_trips_id_r':['tripid', 'houseid', 'personid', 'starttime', 'tripcount'],
			  'persons_location_r':['houseid', 'personid', 'personuniqueid', 'location', 'lasttripcount'],
			  'trips_occupant_origin_invalid_r':['tripid', 'tripvalid', 'tripstarttime'],
			  'person_trips_occupant_origin_invalid_r':['tripid', 'houseid', 'personid', 'tripvalid', 'tripstarttime'],
			  'households_arrived_id_r':['houseid', 'actualarrivaltime'],
			  'persons_prism_activities_r':['scheduleid', 'houseid', 'personid'],
			  'workers_r':['houseid', 'personid', 'episodes'], 
			  'child_dependency_r':['houseid', 'personid', 'dependency'],
			  'daily_school_status_r':['houseid', 'personid', 'schdailystatus'],
			  'daily_work_satus_r':['houseid', 'personid', 'wrkdailystatus'],
			  'persons_history_r':['houseid', 'personid', 'personuniqueid', 'ih_history', 'discretionary_history', 'maintenance_history', 'fixed_history']
			   }



	self.colDef = {'houseid':int64, 'personid':int32, 'dependency':int32, 'schdailystatus':int32,
			'wrkdailystatus':int32, 'episodes':int32, 'tripid':int32, 'vehid':int32, 
			'expectedstarttime':int32, 
			'expectedarrivaltime':int32, 'actualarrivaltime':int32,
			'tripmode':int32, 'fromzone':int32, 'tozone':int32, 'starttime':int32,
			'endtime':int32, 'origin':int32, 'destination':int32, 'tt':float32, 'locationid':int32,
			'trippurpose':int32, 'trippurposefrom':int32, 'tripind':int32, 'occupancy':int32,
			'persononnetworkflag':int32, 'personuniqueid':int32, 'time':int32, 'location':int32, 'tripvalid':int32,
			'arrivaltime':int32, 'arrivedpersonid':int32,'tripdependentpersonid':int64, 'tripwithhhmember':int32, 'tripstarttime':int32,
			'lasttripdependentpersonid':int64, 'lastoccupancy':int32,
			'population':int32, 'public_employment':int32, 'retail_employment':int32, 
			'office_employment':int32, 'industrial_employment':int32, 'other_employment':int32, 
			'public_employment_ind':int32, 'retail_employment_ind':int32, 
			'office_employment_ind':int32, 'industrial_employment_ind':int32, 'other_employment_ind':int32, 
			'total_area':float32, 'residential_population':int32, 'single_family_dwelling':int32, 
			'institutional_population':int32, 'multi_family_dwelling':int32, 

			'retail_employment_density':float32, 'public_employment_density':float32, 
			'office_employment_density':float32, 'industrial_employment_density':float32, 'other_employment_density':float32,
		       	'total_area':float32, 'lowest_income':int32, 'low_income':int32, 'high_income':int32,
			'institutional_popultion':int32, 'groupquarter_households':int32,
			'residential_households':int32,

			'vehcount':int32, 
			'vehtype':int32, 'scheduleid':int32, 'activitytype':int32, 'duration':int32, 
			'dependentpersonid':int64, 'ih_history':int32, 'discretionary_history':int32, 
			'maintenance_history':int32, 'fixed_history':int32, 
			'tripcount':int64, 'lasttripcount':int64, 'starttripcount':int64, 'endtripcount':int64,
			'startdependentpersonid':int64, 'enddependentpersonid':int64, 'tripcount':int64, 'lasttripcount':int64, 'distance':float64}

	

    def tableColTypes(self, tableName):
	colTypes = {}
	for col in self.tableCols[tableName]:
	    colTypes[col] = self.colDef[col]
	return colTypes


    def returnTypeConversion(self, tableName):
        colDtypes = self.tableColTypes(tableName)

        uniqColDtypes = list(set(colDtypes.values()))

        for i in uniqColDtypes:
            if i in [int32, int64]:
                convType = "int"
            if i in [float32, float64]:
                convType = "float"
                return convType
        return convType


    def returnCols(self, tableName):
	return self.tableCols[tableName]

    def returnColId(self, tableName, colName):
	#print 'colId', colName
	return self.tableCols[tableName].index(colName)

    def returnTable(self, tableName, id_var, colNames, fileLoc):
	
	data = load('%s/%s.npy' %(fileLoc, tableName))

	colId = self.returnColId(tableName, id_var)
	idVarColumn = data[:,colId]
	
	uniqueIds = unique(idVarColumn.astype(int))

	table = zeros((max(uniqueIds) + 1, len(colNames)))

	#print data.shape, 'SHAPE OF THE LOCS TABLE'
	#print len(uniqueIds)

        for i in range(len(colNames)):
	    colNum = self.returnColId(tableName, colNames[i])
	    #print i, colNum, colNames[i]
	    table[uniqueIds, i] = data[:,colNum]
	
	#print colNames
	return DataArray(table, colNames), uniqueIds



    def returnTableAsMatrix(self, tableName, originColName, destinationColName, 
			    skimColName, fileLoc, fillValue=9999):
        
	data = load('%s/%s.npy' %(fileLoc, tableName))

        origin = data[:,0].astype(int)
        destination = data[:,1].astype(int)
        skims = data[:,2]

	#print origin[:5]

        # Initialize matrix
        skimsMatrix = ones((max(origin)+1, max(destination)+1)) * fillValue

        # Populate matrix
        skimsMatrix[origin, destination] = skims
	#skimsMatrix = masked_equal(skimsMatrix, 9999)
        
        return masked_equal(skimsMatrix, 9999), unique(origin)

    
if __name__ == '__main__':
    db = DB('w')
    db.create()
    table = db.returnTableReference('households_r')
