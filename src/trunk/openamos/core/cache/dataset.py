import tables as t
import time

from numpy import unique
from numpy.ma import zeros, masked_equal, ones
from openamos.core.cache.dataset_table_layouts import *
from openamos.core.data_array import DataArray

class DB(object):
    def __init__(self, fileLoc, mode='w', fileName=None):

        if fileName == None:
            fileName = "amosdb"

        self.fileh = t.openFile("%s/%s.h5" %(fileLoc, fileName), mode=mode)


        """
        if partId is None:
            self.fileh = t.openFile("%s/amosdb.h5" %(fileLoc), mode=mode)
        else:
            self.fileh = t.openFile("%s/amosdb_part_%s.h5" %(fileLoc, partId), mode=mode)

        """
    def create_inputCache(self):
        input_grp = self.fileh.createGroup(self.fileh.root, "input_grp")

        #Input Tables - Creatign the table
        self.fileh.createTable(input_grp, "travel_skims_peak", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_offpeak", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_0", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_1", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_2", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_3", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_4", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_5", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_6", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_7", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_8", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_9", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_10", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_11", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_12", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_13", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_14", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_15", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_16", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_17", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_18", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_19", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_20", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_21", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_22", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_23", Travel_Skims)

        self.fileh.createTable(input_grp, "locations", Locations)

    def create_outputCache(self, partId=None):
        if partId == None:
            partId = ""
        output_grp = self.fileh.createGroup(self.fileh.root, "output_grp_%s" %(partId))
        # Output Tables - Creating the table
        self.fileh.createTable(output_grp, "households_vehicles_count_r", Households_Vehicles_Count_R)
        self.fileh.createTable(output_grp, "vehicles_r", Vehicles_R)
        self.fileh.createTable(output_grp, "workers_r", Workers_R)
        self.fileh.createTable(output_grp, "schedule_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_ltrec_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_allocterm_r", Schedule_Allocation_R)
        #self.fileh.createTable(output_grp, "schedule_joint_allocterm_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "persons_fixed_activity_vertices_r", Persons_Fixed_Activity_Vertices_R)

        self.fileh.createTable(output_grp, "schedule_cleanfixedactivityschedule_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_childrenlastprismadj_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_childreninctravelrec_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_cleanaggregateactivityschedule_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_dailyallocrec_r", Schedule_Allocation_R)
        #self.fileh.createTable(output_grp, "schedule_joint_dailyallocrec_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_skeleton_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_inctravelrec_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_final_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_elapsed_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_inctrips_r", Schedule_Allocation_R1)
        self.fileh.createTable(output_grp, "schedule_full_r", Schedule_Allocation_R1)
        self.fileh.createTable(output_grp, "schedule_aggregatefinal_r", Schedule_Allocation_R)
        self.fileh.createTable(output_grp, "schedule_allocatedependent_r", Schedule_Allocation_R1)

        self.fileh.createTable(output_grp, "persons_r", Persons_R)
        #self.fileh.createTable(output_grp, "child_dependency_r", Child_Dependency_R)
        #self.fileh.createTable(output_grp, "daily_school_status_r", Daily_School_Status_R)
        #self.fileh.createTable(output_grp, "daily_work_status_r", Daily_Work_Status_R)

        self.fileh.createTable(output_grp, "persons_prism_activities_r", Persons_Prism_Activities_R)
        self.fileh.createTable(output_grp, "trips_r", Trips_R)
        self.fileh.createTable(output_grp, "trips_full_r", Trips_Full_R)
        self.fileh.createTable(output_grp, "trips_purpose_r", Trips_Purpose_R)
        self.fileh.createTable(output_grp, "trips_invalid_r", Trips_Invalid_R)
        self.fileh.createTable(output_grp, "current_occupancy_r", Occupancy_R)
        #self.fileh.createTable(output_grp, "current_occupancy_dup_r", Occupancy_R)
        #self.fileh.createTable(output_grp, "trips_inc_expected_to_malta_r", Trips_R)
        self.fileh.createTable(output_grp, "trips_to_malta_r", Trips_Final_R)
        self.fileh.createTable(output_grp, "persons_location_r", Persons_Location_R)
        self.fileh.createTable(output_grp, "persons_history_r", Persons_History_R)
        self.fileh.createTable(output_grp, "gap_function_r", Gap_Function_R)
        self.fileh.createTable(output_grp, "od_r", OD_R)
        self.fileh.createTable(output_grp, "gap_before_r", Gap_Before_R)
        self.fileh.createTable(output_grp, "gap_after_r", Gap_After_R)


        self.fileh.createTable(output_grp, "person_trips_occupant_origin_invalid_r", Person_Trips_Occupant_Origin_Invalid_R)
        self.fileh.createTable(output_grp, "persons_arrived_from_openamos_r", Persons_Arrived_R)
        self.fileh.createTable(output_grp, "persons_arrived_r", Persons_Arrived_R)
        self.fileh.createTable(output_grp, "persons_arrived_id_r", Persons_Arrived_Id_R)
        self.fileh.createTable(output_grp, "persons_leaving_id_r", Persons_Leaving_Id_R)
        self.fileh.createTable(output_grp, "persons_leaving_valid_trips_id_r", Persons_Leaving_Valid_Trips_Id_R)
        self.fileh.createTable(output_grp, "trips_arrival_from_malta_r", Trips_Arrival_R)
        self.fileh.createTable(output_grp, "trips_arrival_from_openamos_r", Trips_Arrival_R)
        self.fileh.createTable(output_grp, "trips_occupant_origin_invalid_r", Trips_Occupant_Origin_Invalid_R)


        #self.fileh.createTable(output_grp, "odt_r", ODT_R)


        self.fileh.createTable(output_grp, "mortality_r", Mortality_R)
        self.fileh.createTable(output_grp, "birth_r", Birth_R)
        self.fileh.createTable(output_grp, "aging_r", Aging_R)
        self.fileh.createTable(output_grp, "student_residence_choice_r", Student_Residence_Choice_R)
        self.fileh.createTable(output_grp, "education_r", Education_R)
        self.fileh.createTable(output_grp, "education_continuation_r", Education_Forecast_R)
        self.fileh.createTable(output_grp, "labor_participation_r", Labor_Participation_R)
        self.fileh.createTable(output_grp, "marriage_decision_r", Marriage_Decision_R)
        self.fileh.createTable(output_grp, "divorce_decision_r", Divorce_Decision_R)
        self.fileh.createTable(output_grp, "household_forecast_population_r", Household_Forecast_Population_R)
        self.fileh.createTable(output_grp, "person_forecast_population_r", Person_Forecast_Population_R)
        self.fileh.createTable(output_grp, "household_emigration_population_r", Household_Population_R)
        self.fileh.createTable(output_grp, "person_emigration_population_r", Person_Moving_Population_R)
        self.fileh.createTable(output_grp, "household_immigration_population_r", Household_Population_R)
        self.fileh.createTable(output_grp, "person_immigration_population_r", Person_Moving_Population_R)
        self.fileh.createTable(output_grp, "household_population_r", Household_Population_R)
        self.fileh.createTable(output_grp, "person_population_r", Person_Population_R)
        self.fileh.createTable(output_grp, "age_dist_r", Age_Dist_R)
        self.fileh.createTable(output_grp, "sex_dist_r", Sex_Dist_R)
        self.fileh.createTable(output_grp, "race_dist_r", Race_Dist_R)
        self.fileh.createTable(output_grp, "persons_dist_r", Persons_Dist_R)
        self.fileh.createTable(output_grp, "hht_dist_r", Hht_Dist_R)
        self.fileh.createTable(output_grp, "noc_dist_r", Noc_Dist_R)
        self.fileh.createTable(output_grp, "wif_dist_r", Wif_Dist_R)



    def create(self, tableName=None):
        # TODO: create output/input tables everytime?

        # Output Tables - Creating groups
        output_grp = self.fileh.createGroup(self.fileh.root, "output_grp")
        # Input Tables - Creating groups
        input_grp = self.fileh.createGroup(self.fileh.root, "input_grp")

        # Output Tables - Creating the table
        self.fileh.createTable(output_grp, "households_vehicles_count_r", Households_Vehicles_Count_R)
        self.fileh.createTable(output_grp, "vehicles_r", Vehicles_R)
        self.fileh.createTable(output_grp, "workers_r", Workers_R)
        self.fileh.createTable(output_grp, "schedule_r", Schedule_R)
        self.fileh.createTable(output_grp, "schedule_ltrec_r", Schedule_R)
        self.fileh.createTable(output_grp, "schedule_cleanfixedactivityschedule_r", Schedule_R)
        self.fileh.createTable(output_grp, "schedule_childreninctravelrec_r", Schedule_R)
        self.fileh.createTable(output_grp, "schedule_cleanaggregateactivityschedule_r", Schedule_R)
        self.fileh.createTable(output_grp, "schedule_dailyallocrec_r", Schedule_R)
        self.fileh.createTable(output_grp, "schedule_inctravelrec_r", Schedule_R)
        self.fileh.createTable(output_grp, "schedule_final_r", Schedule_R)
        self.fileh.createTable(output_grp, "schedule_aggregatefinal_r", Schedule_R)
        self.fileh.createTable(output_grp, "child_dependency_r", Child_Dependency_R)
        self.fileh.createTable(output_grp, "daily_school_status_r", Daily_School_Status_R)
        self.fileh.createTable(output_grp, "daily_work_status_r", Daily_Work_Status_R)
        self.fileh.createTable(output_grp, "trips_r", Trips_R)
        self.fileh.createTable(output_grp, "trips_to_expected_to_malta_r", Trips_R)
        self.fileh.createTable(output_grp, "trips_to_malta_r", Trips_Final_R)




        #Input Tables - Creatign the table
        self.fileh.createTable(input_grp, "travel_skims_peak", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_offpeak", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_0", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_1", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_2", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_3", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_4", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_5", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_6", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_7", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_8", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_9", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_10", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_11", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_12", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_13", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_14", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_15", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_16", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_17", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_18", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_19", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_20", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_21", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_22", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims_23", Travel_Skims)

        self.fileh.createTable(input_grp, "locations", Locations)


    def close(self):
        self.fileh.close()

    def returnGroup(self, tableName):
        if tableName[-2:] == "_r":
            return 'output'
        else:
            return 'input'


    def returnTableReference(self, tableName, partId=None):
        tableName = tableName.lower()
        grp = self.returnGroup(tableName)
        if partId == None:
            partId = "_"
        else:
            partId = "_%s" %(partId)

        if grp == 'input':
            partId = ""

        loc = '/%s_grp%s' %(grp, partId)
        return self.fileh.getNode(loc, name=tableName)


    def returnTypeConversion(self, tableName, partId=None):
        tableRef = self.returnTableReference(tableName, partId)
        colDtypes = tableRef.coldtypes

        uniqColDtypes = list(set(colDtypes.values()))

        convType = ""
        for i in uniqColDtypes:
            if i.kind in "iu":
                convType = "int"
            if i.kind in "f":
                convType = "float"
                return convType
        return convType

    def list_of_outputtables(self):
        tableList = []

        for group in self.fileh.walkGroups():
            for table in self.fileh.listNodes(group, classname='Table'):
                if self.returnGroup(table.name) == 'output':
                    tableList.append(table.name)


        return tableList


    def createSkimsCache(self, tableName, data):
        t = time.time()
        cols = data.varnames
        colIndices = range(data.cols)

        tableRef = self.returnTableReference(tableName)
        tableRow = tableRef.row


        for i in data.data:
            for j in colIndices:
                #if i[j] is not None:
                #    tableRow[cols[j]] = i[j]
                tableRow[cols[j]] = i[j]
            tableRow.append()
        tableRef.flush()
        print '\tTime taken to write to hdf5 format %.4f' %(time.time()-t)


    def createSkimsTableFromDatabase(self, tableInfo, queryBrowser):
        t = time.time()

        tableName = tableInfo.tableName

        colsList = []
        colsList.append(tableInfo.origin_var)
        colsList.append(tableInfo.destination_var)
        colsList.append(tableInfo.skims_var)

        data = queryBrowser.select_all_from_table(tableName, colsList)
        print '\tTotal time taken to retrieve records from the database %.4f' %(time.time()-t)

        cols = data.varnames
        colIndices = range(data.cols)

        tableRef = self.returnTableReference(tableName)
        tableRow = tableRef.row


        for i in data.data:
            for j in colIndices:
                #if i[j] is not None:
                #    tableRow[cols[j]] = i[j]
                tableRow[cols[j]] = i[j]
            tableRow.append()
        tableRef.flush()
        print '\tTime taken to write to hdf5 format %.4f' %(time.time()-t)



    def createLocationsTableFromDatabase(self, tableInfo, queryBrowser):
        t = time.time()

        colsList = tableInfo.locations_varsList + [tableInfo.location_id_var]

        tableName = tableInfo.tableName
        data = queryBrowser.select_all_from_table(tableName, colsList)
        print '\tTotal time taken to retrieve records from the database %.4f' %(time.time()-t)

        colsList = data.varnames
        colIndices = range(data.cols)

        tableRef = self.returnTableReference(tableInfo.referenceTableName)
        tableRow = tableRef.row


        for i in data.data:
            for j in colIndices:
                #if i[j] is not None:
                #    tableRow[cols[j]] = i[j]
                tableRow[colsList[j]] = i[j]
            tableRow.append()
        tableRef.flush()
        print '\tTime taken to write to hdf5 format %.4f' %(time.time()-t)


    def returnTable(self, tableName, id_var, colNames):
        tableRef = self.returnTableReference(tableName)

        idVarColumn = tableRef.col(id_var)

        uniqueIds = unique(idVarColumn)

        table = zeros((max(uniqueIds) + 1, len(colNames)))

        for i in range(len(colNames)):
            table[uniqueIds, i] = tableRef.col(colNames[i])

        #print table
        return DataArray(table, colNames), uniqueIds



    def returnTableAsMatrix(self, tableName, originColName, destinationColName, skimColName, fillValue=9999):
        tableRef = self.returnTableReference(tableName)

        #print 'OLDER IMPLEMENTATION'
        origin = tableRef.col(originColName)
        destination = tableRef.col(destinationColName)
        skims = tableRef.col(skimColName)

        skimsValues = tableRef[0:]

        # Initialize matrix
        skimsMatrix = ones((max(origin)+1, max(destination)+1)) * fillValue

        # Populate matrix
        skimsMatrix[origin, destination] = skims
        #skimsMatrix = masked_equal(skimsMatrix, 9999)
        print 'Skims Values for O,D pair (1226, 896) and (1538, 1562)- ', skimsMatrix[1226, 896], skimsMatrix[1538, 1562]
        #raw_input()
        return masked_equal(skimsMatrix, 9999), unique(origin)



if __name__ == '__main__':
    db = DB('w')
    db.create()
    table = db.returnTableReference('households_r')
