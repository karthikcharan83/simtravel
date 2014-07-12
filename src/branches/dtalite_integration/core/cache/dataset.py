import time
import os

from pandas import DataFrame as df
from numpy import unique, int64, int, float32, float, load
from numpy.ma import zeros, masked_equal, ones
from openamos.core.data_array import DataArray


class DB(object):

    def __init__(self):

        # TODO: where do we get the table definitions and relationships from
        # for now this is static

        self.tableCols = {'travel_skims': ['origin', 'destination', 'tt'],
                          'locations': ['locationid', 'retail_employment', 'office_employment', 'public_employment',
                                        'industrial_employment', 'other_employment',
                                        'retail_employment_density', 'office_employment_density', 'public_employment_density',
                                        'other_employment_density',
                                        'total_area', 'low_income', 'lowest_income', 'high_income',
                                        'institutional_population', 'groupquarter_households',
                                        'residential_households'],
                          'households_r': ['houseid', 'vehcount', 'vehdefi', 'avratio', 'informationtype', 'ecoflag'],
                          'vehicles_r': ['houseid', 'vehid', 'vehtype'],
                          'schedule_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                         'endtime', 'duration', 'dependentpersonid'],
                          'schedule_ltrec_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                               'endtime', 'duration', 'dependentpersonid'],
                          'schedule_allocterm_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                               'endtime', 'duration', 'dependentpersonid'],

                          'schedule_cleanfixedactivityschedule_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                                                    'endtime', 'duration', 'dependentpersonid'],
                          'schedule_childreninctravelrec_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                                              'endtime', 'duration', 'dependentpersonid'],
                          'schedule_childrenlastprismadj_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                                              'endtime', 'duration', 'dependentpersonid'],
                          'schedule_cleanaggregateactivityschedule_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                                              'endtime', 'duration', 'dependentpersonid'],
                          'schedule_skeleton_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                                              'endtime', 'duration', 'dependentpersonid'],

                          'schedule_conflictrec_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                                     'endtime', 'duration', 'dependentpersonid'],
                          'schedule_inctravelrec_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                                      'endtime', 'duration', 'dependentpersonid'],
                          'schedule_dailyallocrec_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                                       'endtime', 'duration', 'dependentpersonid'],
                          'schedule_final_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                               'endtime', 'duration', 'dependentpersonid', 'tripcount'],
                          'schedule_elapsed_r': ['houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                                                 'endtime', 'duration', 'dependentpersonid', 'tripcount'],

                          'trips_r': ['houseid', 'personid', 'vehid', 'tripmode', 'fromzone', 'tozone', 'starttime', 'endtime', 'trippurposefrom',
                                      'trippurpose', 'duration', 'occupancy', 'tripind', 'dependentpersonid', 'tripwithhhmember',
                                      'lasttripdependentpersonid', 'lastoccupancy', 'starttripcount', 'endtripcount',
                                      'startdependentpersonid', 'enddependentpersonid', 'tripcount', 'lasttripcount'],

                          'trips_with_nonhh_r': ['houseid', 'personid', 'vehid', 'tripmode', 'fromzone', 'tozone', 'starttime', 'endtime', 'trippurposefrom',
                                                 'trippurpose', 'duration', 'occupancy', 'dependentpersonid'],

                          'trips_to_dta_r': ['tripid', 'houseid', 'personid', 'vehid', 'tripmode',
                                             'fromzone', 'tozone', 'starttime', 'endtime', 'trippurpose', 'duration',
                                             'dependentpersonid', 'persononnetworkflag', 'valueoftime', 'informationtype',
                                             'pricingtype', 'vehicletype', 'vehicleage'],
                          'current_occupancy_r': ['houseid', 'personid', 'tripid', 'occupancy', 'dependentpersonid', 'tripcount'],
                          'trips_invalid_r': ['tripid', 'tripind'],
                          'persons_r': ['houseid','personid','vehcount','vehdefi','avratio','informationtype','ecoflag','schdailystatus','wrkdailystatus',
                          'dependency','valueoftimeperdist','episodes','hhwagerate','valueoftime','hhsize',
                          'unittype','tenure','bldgsz','yrbuilt','yrmoved','vehicl','value','hht','noc','grent',
                          'wif','hinc','msacmsa1','msacmsa5','msapmsa1','msapmsa5','areatyp1','areatyp5','homeown','inclt35k','incge35k','incge50k',
                          'incge75k','incge100k','inc35t50','inc50t75','inc75t100','withchild','numadlt','sparent','numwrkr','nwrkcnt','zonetidi4',
                          'htaz','drvrcnt','urb','rur','own','twnhouse','serialno','personuniqueid','state',
                          'pumano','hhid','relate','sex','hispan','race1','marstat','enroll','grade','educ','esr','trvmns',
                          'indnaics','occcen5','clwkr','wrklyr','hours','earns','trvtime','lvtime','coled','male','female','age','ag5t10',
                          'ag11t14','ag15t17','ag18t24','ag25t34','ag35t44','ag45t54','ag55t64','agge65','fulltim','parttim','white','hispanic',
                          'timetowk','isemploy','schtazi8','wtazi8','schtaz','wtaz','wrkr','presch','nadlt','ag12t17','ag5t14','schstat','agge15'],
                          'persons_fixed_activity_vertices_r': ['houseid', 'personid', 'starttime', 'endtime'],
                          'trips_arrival_from_dta_r': ['tripid', 'arrivaltime', 'distance'],
                          'trips_arrival_from_openamos_r': ['tripid', 'arrivaltime'],
                          'persons_arrived_r': ['houseid', 'personid', 'tripid', 'expectedstarttime',
                                                'expectedarrivaltime', 'actualarrivaltime', 'tripdependentpersonid', 'fromzone', 'tozone', 'tripcount'],
                          'persons_arrived_from_openamos_r': ['houseid', 'personid', 'tripid', 'expectedstarttime',
                                                              'expectedarrivaltime', 'actualarrivaltime', 'tripdependentpersonid', 'fromzone', 'tozone', 'tripcount'],
                          'persons_arrived_id_r': ['houseid', 'personid', 'actualarrivaltime', 'expectedarrivaltime',
                                                   'tripdependentpersonid', 'tozone', 'personuniqueid', 'tripcount'],
                          #'persons_leaving_id_r':['tripid', 'houseid', 'personid', 'personuniqueid', 'starttime', 'fromzone', 'tripcount'],
                          'persons_leaving_id_r': ['tripid', 'houseid', 'personid', 'starttime', 'fromzone', 'tripcount'],
                          'persons_leaving_valid_trips_id_r': ['tripid', 'houseid', 'personid', 'starttime', 'tripcount'],
                          'persons_location_r': ['houseid', 'personid', 'personuniqueid', 'location', 'lasttripcount'],
                          'trips_occupant_origin_invalid_r': ['tripid', 'tripvalid', 'tripstarttime'],
                          'person_trips_occupant_origin_invalid_r': ['tripid', 'houseid', 'personid', 'tripvalid', 'tripstarttime'],
                          'households_arrived_id_r': ['houseid', 'actualarrivaltime'],
                          'persons_prism_activities_r': ['scheduleid', 'houseid', 'personid'],
                          'workers_r': ['houseid', 'personid', 'episodes'],
                          'child_dependency_r': ['houseid', 'personid', 'dependency'],
                          'daily_school_status_r': ['houseid', 'personid', 'schdailystatus'],
                          'daily_work_satus_r': ['houseid', 'personid', 'wrkdailystatus'],
                          'persons_history_r': ['houseid', 'personid', 'personuniqueid', 'ih_history', 'discretionary_history', 'maintenance_history', 'fixed_history']
                          }
        #'valueoftime', 'informationtype'

        self.colDef = {'houseid': int64, 'personid': int, 'dependency': int, 'schdailystatus': int,
                       'wrkdailystatus': int, 'episodes': int, 'tripid': int, 'vehid': int,
                       'expectedstarttime': int,
                        
                        'hhwagerate':float, 'valueoftime':float, 'valueoftimeperdist':float,'informationtype':int, 'ecoflag':int, 
                       'expectedarrivaltime': int, 'actualarrivaltime': int,
                       'tripmode': int, 'fromzone': int, 'tozone': int, 'starttime': int,
                       'endtime': int, 'origin': int, 'destination': int, 'tt': float, 'locationid': int,
                       'trippurpose': int, 'trippurposefrom': int, 'tripind': int, 'occupancy': int,
                       'persononnetworkflag': int, 'personuniqueid': int, 'time': int, 'location': int, 'tripvalid': int,
                       'arrivaltime': int, 'arrivedpersonid': int, 'tripdependentpersonid': int64, 'tripwithhhmember': int, 'tripstarttime': int,
                       'lasttripdependentpersonid': int64, 'lastoccupancy': int,
                       'population': int, 'public_employment': int, 'retail_employment': int,
                       'office_employment': int, 'industrial_employment': int, 'other_employment': int,
                       'public_employment_ind': int, 'retail_employment_ind': int,
                       'office_employment_ind': int, 'industrial_employment_ind': int, 'other_employment_ind': int,
                       'total_area': float, 'residential_population': int, 'single_family_dwelling': int,
                       'institutional_population': int, 'multi_family_dwelling': int,

                       'retail_employment_density': float, 'public_employment_density': float,
                       'office_employment_density': float, 'industrial_employment_density': float, 'other_employment_density': float,
                       'total_area': float, 'lowest_income': int, 'low_income': int, 'high_income': int,
                       'institutional_popultion': int, 'groupquarter_households': int,
                       'residential_households': int,

                       'vehcount': int, 'vehdefi': int, 'avratio': float, 'informationtype': int, 
                       'vehtype': int, 'scheduleid': int, 'activitytype': int, 'duration': int,
                       'dependentpersonid': int64, 'ih_history': int, 'discretionary_history': int,
                       'maintenance_history': int, 'fixed_history': int,
                       'tripcount': int64, 'lasttripcount': int64, 'starttripcount': int64, 'endtripcount': int64,
                       'startdependentpersonid': int64, 'enddependentpersonid': int64, 'tripcount': int64, 'lasttripcount': int64, 'distance': float,
                       'valueoftime': float, 'informationtype': int, 'pricingtype': int, 'vehicletype': int, 'vehicleage': int, 
                       
                       'vehcount':int,'vehdefi':int,'avratio':float,'informationtype':int,
                       'ecoflag':int,'hhsize':int,'unittype':int,'tenure':int,'bldgsz':int,
                       'yrbuilt':int,'yrmoved':int,'vehicl':int,'value':int,'hht':int,
                       'noc':int,'grent':int,'wif':int,'hinc':int,'msacmsa1':int,
                       'msacmsa5':int,'msapmsa1':int,'msapmsa5':int,'areatyp1':int,'areatyp5':int,'homeown':int,'inclt35k':int,
                       'incge35k':int,'incge50k':int,'incge75k':int,'incge100k':int,'inc35t50':int,'inc50t75':int,'inc75t100':int,
                       'withchild':int,'numadlt':int,'sparent':int,'numwrkr':int,'nwrkcnt':int,'zonetidi4':int,'htaz':int,'drvrcnt':int,
                       'urb':int,'rur':int,'own':int,'twnhouse':int,'serialno':int64,'personuniqueid':int64,'state':int,'pumano':int,
                       'hhid':int,'relate':int,'sex':int,'hispan':int,'race1':int,'marstat':int,'enroll':int,'grade':int,'educ':int,'esr':int,
                       'trvmns':int,'indnaics':int,'occcen5':int,'clwkr':int,'wrklyr':int,'hours':int,'earns':int,'trvtime':int,'lvtime':int,
                       'coled':int,'male':int,'female':int,'age':int,'ag5t10':int,'ag11t14':int,'ag15t17':int,'ag18t24':int,'ag25t34':int,
                       'ag35t44':int,'ag45t54':int,'ag55t64':int,'agge65':int,'fulltim':int,'parttim':int,'white':int,'hispanic':int,
                       'timetowk':int,'isemploy':int,'schtazi8':int,'wtazi8':int,'schtaz':int,'wtaz':int,'wrkr':int,'presch':int,
                       'nadlt':int,'ag12t17':int,'ag5t14':int,'schstat':int,'agge15':int}

    def tableColTypes(self, tableName):
        colTypes = {}
        for col in self.tableCols[tableName]:
            colTypes[col] = self.colDef[col]
        return colTypes

    def returnTypeConversion(self, tableName):
        colDtypes = self.tableColTypes(tableName)

        uniqColDtypes = list(set(colDtypes.values()))

        #for i in uniqColDtypes:
        #    if i in [int, int64]:
        #        convType = "int"
        #    if i in [float32, float]:
        #        convType = "float"
        #        return convType
        return convType

    def returnCols(self, tableName):
        return self.tableCols[tableName]

    def returnColId(self, tableName, colName):
        # print 'colId', colName
        return self.tableCols[tableName].index(colName)

    def returnTable(self, tableName, id_var, colNames, fileLoc):
        file = os.path.join(fileLoc, "%s.csv"%tableName)
        data = df.from_csv(file)
        return DataArray(data[colNames], colNames)

        """
        colId = self.returnColId(tableName, id_var)
        idVarColumn = data[:, colId]

        uniqueIds = unique(idVarColumn.astype(int))

        table = zeros((max(uniqueIds), len(colNames)))

        # print data.shape, 'SHAPE OF THE LOCS TABLE'
        # print len(uniqueIds)

        print colNames
        print data
        print data.shape

        for i in range(len(colNames)):
            colNum = self.returnColId(tableName, colNames[i])
            # print i, colNum, colNames[i]
            table[:, i] = data[:, colNum]

        # print colNames
    
        return DataArray(table, colNames), uniqueIds
    """
    def returnTableAsMatrix(self, tableName, originColName, destinationColName,
                            skimColName, fileLoc, fillValue=9999):

        data = load('%s/%s.npy' % (fileLoc, tableName))

        origin = data[:, 0].astype(int)
        destination = data[:, 1].astype(int)
        skims = data[:, 2]

        # print origin[:5]

        # Initialize matrix
        skimsMatrix = ones((max(origin) + 1, max(destination) + 1)) * fillValue

        # Populate matrix
        skimsMatrix[origin, destination] = skims
        #skimsMatrix = masked_equal(skimsMatrix, 9999)

        return masked_equal(skimsMatrix, 9999), unique(origin)


if __name__ == '__main__':
    db = DB('w')
    db.create()
    table = db.returnTableReference('households_r')
