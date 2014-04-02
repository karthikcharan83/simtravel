import os
import time
import csv
from numpy import array
from numpy.random import randint
import random


from openamos.core.dtalite_integration.simulation_manager_dtalite import SimulationManager
from openamos.core.database_management.database_configuration import DataBaseConfiguration
from openamos.core.database_management.cursor_database_connection import DataBaseConnection



class RunAmosDtalite(object):
    """
    The class reads the configuration file, creates the component and model objects,
    and runs the models to simulate the various activity-travel choice processes.

    If the configObject is invalid, then a valid fileLoc is desired and if that fails
    as well then an exception is raised. In a commandline implementation, fileLoc will
    be passed.
    """


    def __init__(self):
        self.current_min = 1
        self.data_in_real_time = []
        self.proj_path = "C:/DTALite/New_PHXsubarea/"
        
        self.column_index_for_openamos = -1
        self.column_index_for_dtalite = -1
        self.column_index_for_realtimeskim = -1
        
        self.tripsAct = {}
        self.manager = SimulationManager()
        self.manager.subregion = self.read_subregion()
        
        
    def read_Real_Time_Setting_CSV(self):
        
        self.data_in_real_time = []
        real_time_file_name = "%sinput_real_time_simulation_settings.csv" %(self.proj_path)
        ofile = open(real_time_file_name,"rb")
        

        rows = csv.reader(ofile)
        for row in rows:
            self.data_in_real_time.append(row)

        
        ofile.close()
        
        
#     def write_Real_Time_Setting_CSV(self):
#         
#         real_time_file_name = "%sinput_real_time_simulation_settings.csv" %(self.proj_path)
#         wfile = open(real_time_file_name,"wb")
#         
#         c = csv.writer(wfile) 
#         for row in self.data_in_real_time:
#             c.writerow(row)
#         
#         wfile.close()
        

        
        
        
    def run_openamos_simulation(self):
        
        
        numRuns = len(self.data_in_real_time)
        #numRuns = 60
        read_realtime_skim = False
        realtime_time_path = ""
        realtime_dist_path = ""
        for i in range(numRuns):

            
            if i == 0:
                print "============================ Start Running Simulation ==============================="
                inds = self.findindexbyname(self.data_in_real_time[i])
                
            else:
                
                openamos_output_name = self.data_in_real_time[i][self.column_index_for_openamos]
                if openamos_output_name <> '' and i > 0:
                    print "%s - %s " %(i, openamos_output_name)
                    dtal_output_name = self.data_in_real_time[i][self.column_index_for_dtalite]
                    realtime_skim_name = self.data_in_real_time[i][self.column_index_for_realtimeskim]
                    
                    
                    #self.temp_create_dtalite(i-1)       # Just For Testing
                    
                    
                    tripInfoArrivals = self.arrival_from_dtalite(i-1, dtal_output_name)
                    print "File name from OpenAmos: %s" %(openamos_output_name)
                    print "File name from DTALITE: %s" %(dtal_output_name)
                    self.manager.run_selected_components_for_dtalite(i, tripInfoArrivals, openamos_output_name)             
                     
                    
                    #self.temp_trips_from_openamos(i)  # Just For Testing



                    if realtime_skim_name != "":
                        realtime_time_path = "%s%s"%(self.proj_path, realtime_skim_name)
                        realtime_dist_path = "%sdistance0.dat"%(self.proj_path)
                        read_realtime_skim = True
                        
                    if read_realtime_skim:
                        if os.path.exists(realtime_time_path):
                            self.manager.load_currentskims_matrix(realtime_time_path, realtime_dist_path)
                            read_realtime_skim = False
                        else:
                            print "%s does not exist" %(realtime_time_path)
                
                elif openamos_output_name == '' and i > 1:
                    print """Please check the control file called as input_real_time_simulation_settings.csv""" 
                    print """because there is empty on row %s and column %s.""" %(i, self.column_index_for_openamos)
                    break
                  


    def arrival_from_dtalite(self, time, name_dtalite=""):
        
        
        if time == 0 or name_dtalite == "":
            print "No Trip Arrivals------------------------"
            tripInfoArrivals = array([-1])
            return tripInfoArrivals

        else:
            
            isFind = False    
            out_dtalite_name = "%s%s" %(self.proj_path,name_dtalite)
            print "============= Trip Arrival Times from %s" %out_dtalite_name
            while not isFind:
                         
                if os.path.exists(out_dtalite_name) == True:
                    print "It is done to find %s" %(out_dtalite_name)
                    
                    try:
                        
                    
                        tripInfoArrivals = self.read_arrivals_from_dtalite(out_dtalite_name)                  
                        print "Time : %s" %(time)
                        print tripInfoArrivals
                        
                        isFind = True
                        
                    except:
                        print "DTALite may be writing arrival times at this minutes: %s" %time
                        
                    
                    
            return tripInfoArrivals


    def read_arrivals_from_dtalite(self, filename):
        
        ifile = open(filename, "rb")
            
        isSkip = 0
        trip_ids = []
        trip_distances = []
        dta_trips = csv.reader(ifile)
        for tripId in dta_trips:
                
            if isSkip == 0:
                isSkip += 1
                continue
                
            
            trip_ids.append(tripId[1])
            trip_distances.append(tripId[15])
                
        
        if len(trip_ids) > 0:        
            tripInfoArrivals = array(trip_ids+trip_distances)
        else:
            tripInfoArrivals = array([-1])
                
        ifile.close()
        
        print "==============================="
        print tripInfoArrivals
        return tripInfoArrivals
                            
    # It should be deleted 
    def temp_trips_from_openamos(self, time):
        
        input_file = "%sopen_amos_trip_min%s.csv" %(self.proj_path,time-1)
        ofile = open(input_file, "rb")
        trips_from_openamos = csv.reader(ofile)
        
        isSkip = 0
        for trip in trips_from_openamos:
            
            if isSkip == 0:
                isSkip += 1
                continue
            
            trip_id = float(trip[0])
                
            if int(trip_id) > 0.0:
                starttime = float(trip[7])
                arrivaltime = int(starttime) + randint(1, 200)

                    
                if arrivaltime not in self.tripsAct.keys():
                    self.tripsAct[arrivaltime] = [trip_id]
                else:
                    self.tripsAct[arrivaltime] += [trip_id]
            

        ofile.close()
        


    def temp_arrivals_from_dtalite(self, time):
        
        dta_output_name = "output_trip_min%s.csv" %time
        read_from_dtalite = "%s%s" %(self.proj_path,dta_output_name)
        ifile = open(read_from_dtalite, "rb")
            
        isSkip = 0
        trip_ids = []
        trip_distances = []
        dta_trips = csv.reader(ifile)
        for tripId in dta_trips:
                
            if isSkip == 0:
                isSkip += 1
                continue
                
            trip_ids.append(tripId[0])
            trip_distances.append(tripId[2])
                
        
        if len(trip_ids) > 0:        
            tripInfoArrivals = array(trip_ids+trip_distances)
        else:
            tripInfoArrivals = array([-1])
                
        ifile.close()
        
        
        return tripInfoArrivals
    
    
    def temp_create_dtalite(self, time):
        
        dta_output_name = "output_trip_min%s.csv" %(time)
        output_file1 = "%s%s" %(self.proj_path,dta_output_name)
        ifile = open(output_file1, "wb")
            
        out_trips = csv.writer(ifile)
        out_trips.writerow(["agent_id", "trip_id", "from_zone_id", "to_zone_id", "from_origin__node_id", "to_destination_node_id", "start_time_in_min","end_time_in_min", "travel_time_in_min", "demand_type", "pricing_type", "information_type", "value_of_time", "vehicle_type", "vehicle_age", "distance"])
        
        next_arrive_time = time
        if next_arrive_time in self.tripsAct.keys():
                
            tripIds = self.tripsAct.pop(next_arrive_time)
            for tripId in tripIds:
                arrive_time = next_arrive_time
                distance = random.random() * 20.0
                trip = [0,tripId,0,0,0,0,0,arrive_time,0,0,0,0,0,0,0,distance]
                out_trips.writerow(trip)
                    
        ifile.close()
        
        
    def findindexbyname(self, row):
        
        inds = []
        for i in range(len(row)):
            
            if row[i].lower() == 'output_trip_file':
                inds.append(i)
                self.column_index_for_dtalite = i
                
            if row[i].lower() == 'update_trip_file':
                inds.append(i)
                self.column_index_for_openamos = i
                
            if row[i].lower() == 'output_td_skim_file':
                inds.append(i)
                self.column_index_for_realtimeskim = i
                
        return inds
    
    
    def read_subregion(self):
        
        ifile = open("%ssubregion.csv" %(self.proj_path), "rb")
            
        isSkip = 0
        ids_to_dtalite = {}
        self.ids_from_dtalite ={}
        zones = csv.reader(ifile)
        for zone in zones:
                
            if isSkip == 0:
                isSkip += 1
                continue
                
            self.ids_from_dtalite[int(zone[1])] = int(zone[2])
            ids_to_dtalite[int(zone[2])] = int(zone[1])
                
        ifile.close()
             
        return ids_to_dtalite
        
        
        
        
#     def generate_input_dtalite(self):
#         
# 
#         dbConfigObject = DataBaseConfiguration("postgres",
#                                                "postgres",
#                                                "Dyou65221",
#                                                "localhost",
#                                                "mag_zone_dynamic_2009_2")
#         
#         
#         dbcon_obj = DataBaseConnection(dbConfigObject)
#         
#         dbcon_obj.new_connection()
#         
#         
#         for i in range(1440):
# #             insert_stmt = ("""COPY (select tripid as trip_id, houseid as house_id, personid as person_id, vehid as vehicle_id, """
# #                            """tripmode as trip_mode, fromzone as from_zone_id, tozone as to_zone_id, starttime as start_time_in_min, """
# #                            """endtime as end_time_in_min, trippurpose as trip_purpose, duration as duration_in_min, """
# #                            """dependentpersonid as dependent_person_id, tripwithhhmember as trip_with_hh_member from trips_r where starttime = %s) """
# #                            """TO 'C:/openamos_project/Input_Dtalite/open_amos_trip_min%s.csv' DELIMITER ',' CSV HEADER;""" %(i+1, i+1))
# 
#             insert_stmt = ("""COPY (select a.tripid as trip_id, a.houseid as house_id, a.personid as person_id, a.vehid as vehicle_id, """ 
#                            """a.tripmode as trip_mode, (a.fromzone+100) as from_zone_id, (a.tozone+100) as to_zone_id, a.starttime as start_time_in_min, """ 
#                            """a.endtime as end_time_in_min, a.trippurpose as trip_purpose, a.duration as duration_in_min, a.dependentpersonid as dependent_person_id, """ 
#                            """a.tripwithhhmember as person_on_network_flag from (select * from trips_r as t, subregion as s where t.fromzone = s.taz100) as a, """ 
#                            """subregion as b where a.tozone = b.taz100 and a.starttime = %s) """
#                            """TO 'C:/openamos_project/Input_to_DTALITE_0117/open_amos_trip_min%s.csv' DELIMITER ',' CSV HEADER;""" %(i+1, i+1))
#                                                                        
#             print '\t\t', insert_stmt
#             dbcon_obj.cursor.execute(insert_stmt)
#             dbcon_obj.connection.commit()
#         
#         
#         dbcon_obj.close_connection()
        
        
#     def generate_dummy_skim(self):
#         
#         for i in range(23):
#             tt = i+1
#             ifile = open("C:/openamos_project/dynamic_sub/skim%s.dat" %(tt), "rb")
#             ofile = open("C:/openamos_project/dynamic_sub/skim0%s.dat" %(tt), "wb")
#             out_skims = csv.writer(ofile)
#                 
#             skims = csv.reader(ifile)
#             for skim in skims:
#                 
#                 if int(skim[0]) <= 175 and int(skim[1]) <= 175:
#                     out_skims.writerow(skim)
#                     
#         
#             ifile.close()
#             ofile.close()


        
        
if __name__ == '__main__':
    runSimulation = RunAmosDtalite()
    runSimulation.read_Real_Time_Setting_CSV()
    runSimulation.run_openamos_simulation()
    
    
    
    #runSimulation.generate_input_dtalite()
    
    #runSimulation.generate_dummy_skim()
    
    
    
