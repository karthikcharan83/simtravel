"""
Template to generate the database schema: v1
TODO: have to include the relationship between database.
"""

#import the necessary modules
from elixir import *

#define metadata and connect to the database
metadata.bind = "postgres://postgres:1234@localhost/open_amos"
metadata.bind.echo = True

#start define the classes
#schedule class
class Schedule(Entity):
    using_options(tablename='schedule')
    Schedule_ID = Field(Integer, primary_key = True)
    Type_of_Activity = Field(UnicodeText)
    Start_Time = Field(Integer)
    End_Time = Field(Integer)
    Destination = Field(Integer)
    Duration = Field(Integer)


#link od class
class Link_OD(Entity):
    using_options(tablename='link_od')
    Link_OD_ID = Field(Integer, primary_key = True)
    TOD = Field(Integer)
    Mode = Field(UnicodeText)
    Travel_Time = Field(Integer)
    Cost = Field(Integer)
    Average_Speed = Field(Integer)
    Distance = Field(Integer)


#household class
class Household(Entity):
    using_options(tablename='household')
    Household_ID = Field(Integer, primary_key = True)
    adults = Field(Integer)
    age_of_head = Field(Integer)
    autos = Field(Integer)
    building_id = Field(Integer)
    homestaz = Field(Integer)
    household_size = Field(Integer)
    income = Field(Integer)
    nfulltime = Field(Integer)
    nparttime = Field(Integer)
    persons = Field(Integer)
    race_id = Field(Integer)
    test = Field(Integer)
    tract_id = Field(Integer)
    zone_id = Field(Integer)

    
#TSP class
class TSP(Entity):
    using_options(tablename='tsp')
    TSP_ID = Field(Integer, primary_key = True)
    Start_Location = Field(Integer)
    End_Location = Field(Integer)
    Start_Time = Field(Integer)
    End_Time = Field(Integer)
    DO_ID_fk = ManyToOne('Destination_Opportunities', field=Destination_Opportunities_ID)


#link class
class Link(Entity):
    using_options(tablename='link')
    Link_ID = Field(Integer, primary_key = True)
    Oppurtinities_by_Activity_Type = Field(UnicodeText)
    X_Coordinates = Field(Integer)
    Y_Coordinates = Field(Integer)
    DO_ID_fk = ManyToOne('Destination_Opportunities', field=DO_ID)
    

#destination opportunities class
class Destination_Opportunities(Entity):
    using_options(tablename='destination_opportunities')
    DO_ID = Field(Integer, primary_key = True)
    Link_ID_fk = OneToMany('Link', field=Link_ID)
    TSP_ID_fk = OneToMany('TSP', field=TSP_ID)

    
#person class
class Person(Entity):
    using_options(tablename='person')
    Person_ID = Field(Integer, primary_key = True)
    Age = Field(Integer)
    Gender = Field(UnicodeText)
    School_Status = Field(UnicodeText)
    Worker_Status = Field(UnicodeText)
    Driver_Status = Field(UnicodeText)
    Number_of_jobs = Field(Integer)
    Work_Location = Field(Integer)
    School_Location = Field(Integer)
    Pre_School_Location = Field(Integer)
    Earliest_Start_Time_of_Morning_Prism = Field(Integer)
    Latest_End_Time_of_Evening_Prism = Field(Integer)
    PS_ID_fk = OneToMany('Person_Schedule', field=PS_ID)
    Household_ID_fk = ManyToOne('Vehicle', field=Vehicle_ID)
    Vehicle_ID_fk = OneToMany('Vehicle', field=Vehicle_ID)
    PT_ID_fk = ManyToOne('Person_Trip', field=PT_ID)
    
    
#person schedule class
class Person_Schedule(Entity):
    using_options(tablename='person_schedule')
    PS_ID = Field(Integer, primary_key = True)
    Person_ID_fk = ManyToOne('Person', field=Person_ID)
    Schedule_ID_fk = ManyToOne('Schedule', field=Schedule_ID)
    
    
#Vehicle class
class Vehicle(Entity):
    using_options(tablename='vehicle')
    Vehicle_ID = Field(Integer, primary_key = True)
    Person_ID_fk = ManyToOne('Person', field=Person_ID)
    Body_Type = Field(UnicodeText)
    Fuel_Type = Field(UnicodeText)
    Vintage = Field(UnicodeText)
    Mileage = Field(UnicodeText)
    Capacity = Field(UnicodeText)
    Trip_ID_fk = OneToMany('Trip', field=Trip_ID)

    
#trip class
class Trip(Entity): 
    using_options(tablename='trip')
    Trip_ID = Field(Integer, primary_key = True)
    Start_Time = Field(Integer)
    End_Time = Field(Integer)
    Vehicle_ID_fk = ManyToOne('Vehicle', field=Vehicle_ID)
    PT_ID_fk = ManyToOne('Person_Trip', field=PT_ID)
    Start_Location = Field(Integer)
    Mode = Field(UnicodeText)
    Fare = Field(Integer)
    Travel_Times = Field(Integer)
    

#person trip class
class Person_Trip(Entity):
    using_options(tablename='person_trip')
    PT_ID = Field(Integer, primary_key = True)
    Trip_ID_fk = OneToMany('Trip', field=Trip_ID)
    Person_ID_fk = OneToMany('Person', field=Person_ID)


#create all the tables and commit the changes to the database
setup_all()
create_all()

session.commit()

#end of schema generator template
