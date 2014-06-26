import tables as t
import time


class Travel_Skims(t.IsDescription):
    origin = t.Int32Col()
    destination = t.Int32Col()
    tt = t.Float32Col()


class Locations(t.IsDescription):
    locationid = t.Int32Col()
    year = t.Int32Col()
    chtaz = t.Int32Col()
    raz = t.Int32Col()
    pop1 = t.Int32Col()
    pop2 = t.Int32Col()
    pop3 = t.Int32Col()
    pop4 = t.Int32Col()
    residential_households = t.Int32Col()
    groupquarter_households = t.Int32Col()
    hh3 = t.Int32Col()
    hh4 = t.Int32Col()
    other_employment = t.Int32Col()
    public_employment = t.Int32Col()
    retail_employment = t.Int32Col()
    office_employment = t.Int32Col()
    industrial_employment = t.Int32Col()
    lowest_income = t.Int32Col()
    low_income = t.Int32Col()
    inc3 = t.Int32Col()
    high_income = t.Int32Col()
    inc5 = t.Int32Col()
    total_area = t.Float32Col()
    offarea = t.Float32Col()
    enroll = t.Int32Col()
    rflag = t.Int32Col()
    apass = t.Int32Col()
    du9 = t.Int32Col()
    du19 = t.Int32Col()
    du20 = t.Int32Col()
    du30 = t.Int32Col()
    sfhh = t.Int32Col()
    mfhh = t.Int32Col()
    popcorr = t.Int32Col()
    institutional_population = t.Int32Col()
    popminst = t.Int32Col()
    wahemp = t.Int32Col()
    constemp = t.Int32Col()
    puboff = t.Int32Col()
    pubpub = t.Int32Col()
    pubarea = t.Float32Col()
    asuenroll = t.Int32Col()
    tothh = t.Int32Col()
    reszone = t.Int32Col()
    rzone = t.Int32Col()
    other_employment_density = t.Float32Col()
    public_employment_density = t.Float32Col()
    retail_employment_density = t.Float32Col()
    office_employment_density = t.Float32Col()
    industrial_employment_density = t.Float32Col()


class Households_Vehicles_Count_R(t.IsDescription):
    houseid = t.Int64Col()
    vehcount = t.Int32Col()
    vehdefi = t.Int32Col()
    avratio = t.Float32Col()
    informationtype = t.Int32Col()


class Vehicles_R(t.IsDescription):
    houseid = t.Int64Col()
    vehid = t.Int32Col()
    vehtype = t.Int32Col()


class Tsp_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    daystart = t.Int32Col()
    dayend = t.Int32Col()


class Schedule_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    activitytype = t.Int32Col()
    locationid = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()
    duration = t.Int32Col()
    dependentpersonid = t.Int64Col()


class Schedule_Allocation_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    activitytype = t.Int32Col()
    locationid = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()
    duration = t.Int32Col()
    dependentpersonid = t.Int64Col()
    tripcount = t.Int64Col()


class Schedule_Allocation_R1(t.IsDescription):
    scheduleid = t.Int64Col()
    houseid = t.Int64Col()
    personid = t.Int32Col()
    activitytype = t.Int32Col()
    locationid = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()
    duration = t.Int32Col()
    dependentpersonid = t.Int64Col()
    tripcount = t.Int64Col()


class Persons_Fixed_Activity_Vertices_R(t.IsDescription):
    houseid = t.Int32Col()
    personid = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()


class Persons_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    schdailystatus = t.Int32Col()
    wrkdailystatus = t.Int32Col()
    dependency = t.Int32Col()
    valueoftimeperdist = t.Float32Col()
    episodes = t.Int32Col()
    hhwagerate = t.Float32Col()
    valueoftime = t.Float32Col()
    informationtype = t.Int32Col()


class Child_Dependency_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    dependency = t.Int32Col()


class Daily_School_Status_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    schdailystatus = t.Int32Col()


class Daily_Work_Status_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    wrkdailystatus = t.Int32Col()


class Workers_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    episodes = t.Int32Col()


class Trips_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    vehid = t.Int32Col()
    tripmode = t.Int32Col()
    fromzone = t.Int32Col()
    tozone = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()
    trippurpose = t.Int32Col()
    duration = t.Int32Col()
    trippurposefrom = t.Int32Col()
    occupancy = t.Int32Col()
    tripind = t.Int32Col()
    dependentpersonid = t.Int64Col()
    tripwithhhmember = t.Int32Col()
    lasttripdependentpersonid = t.Int64Col()
    lastoccupancy = t.Int32Col()
    starttripcount = t.Int64Col()
    endtripcount = t.Int64Col()
    startdependentpersonid = t.Int64Col()
    enddependentpersonid = t.Int64Col()
    tripcount = t.Int64Col()
    lasttripcount = t.Int64Col()


class Trips_Purpose_R(t.IsDescription):
    tripid = t.Int32Col()
    houseid = t.Int32Col()
    personid = t.Int32Col()
    trippurpose = t.Int32Col()
    endtime = t.Int32Col()
    duration = t.Int32Col()


class Trips_Full_R(t.IsDescription):
    tripid = t.Int32Col()
    houseid = t.Int32Col()
    personid = t.Int32Col()
    fromzone = t.Int32Col()
    tozone = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()
    duration = t.Int32Col()
    trippurpose = t.Int32Col()
    dependentpersonid = t.Int64Col()
    tripcount = t.Int64Col()
    occupancy = t.Int32Col()
    distance = t.Float64Col()


class Trips_Invalid_R(t.IsDescription):
    tripid = t.Int64Col()
    tripind = t.Int32Col()


class Occupancy_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    tripid = t.Int32Col()
    occupancy = t.Int32Col()
    dependentpersonid = t.Int64Col()
    tripcount = t.Int64Col()


class Trips_Final_R(t.IsDescription):
    tripid = t.Int64Col()
    houseid = t.Int64Col()
    personid = t.Int32Col()
    vehid = t.Int32Col()
    tripmode = t.Int32Col()
    fromzone = t.Int32Col()
    tozone = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()
    trippurpose = t.Int32Col()


class Persons_Prism_Activities_R(t.IsDescription):
    scheduleid = t.Int64Col()
    houseid = t.Int64Col()
    personid = t.Int32Col()


class Persons_Location_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    personuniqueid = t.Int32Col()
    time = t.Int32Col()
    location = t.Int32Col()
    lasttripcount = t.Int64Col()


class Persons_History_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    personuniqueid = t.Int32Col()
    ih_history = t.Int32Col()
    maintenance_history = t.Int32Col()
    discretionary_history = t.Int32Col()
    fixed_history = t.Int32Col()


class Person_Trips_Occupant_Origin_Invalid_R(t.IsDescription):
    tripid = t.Int32Col()
    houseid = t.Int64Col()
    personid = t.Int32Col()
    tripvalid = t.Int32Col()
    tripstarttime = t.Int32Col()


class Persons_Arrived_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    tripid = t.Int32Col()
    expectedstarttime = t.Int32Col()
    expectedarrivaltime = t.Int32Col()
    actualarrivaltime = t.Int32Col()
    tripdependentpersonid = t.Int64Col()
    fromzone = t.Int32Col()
    tozone = t.Int32Col()
    tripcount = t.Int64Col()


class Persons_Arrived_Id_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    actualarrivaltime = t.Int32Col()
    expectedarrivaltime = t.Int32Col()
    tripdependentpersonid = t.Int64Col()
    tozone = t.Int32Col()
    personuniqueid = t.Int64Col()
    tripcount = t.Int64Col()


class Persons_Leaving_Id_R(t.IsDescription):
    tripid = t.Int32Col()
    houseid = t.Int64Col()
    personid = t.Int32Col()
    starttime = t.Int32Col()
    fromzone = t.Int32Col()
    tripcount = t.Int64Col()


class Persons_Leaving_Valid_Trips_Id_R(t.IsDescription):
    tripid = t.Int32Col()
    houseid = t.Int64Col()
    personid = t.Int32Col()
    starttime = t.Int32Col()
    tripcount = t.Int64Col()


class Trips_Arrival_R(t.IsDescription):
    tripid = t.Int32Col()
    arrivaltime = t.Int32Col()
    distance = t.Float64Col()


class Trips_Occupant_Origin_Invalid_R(t.IsDescription):
    tripid = t.Int32Col()
    tripvalid = t.Int32Col()
    tripstarttime = t.Int32Col()


class Gap_Function_R(t.IsDescription):
    tripid = t.Int64Col()
    houseid = t.Int32Col()
    personid = t.Int32Col()
    gap_before = t.Int32Col()
    gap_after = t.Int32Col()


class Gap_Before_R(t.IsDescription):
    gap_before = t.Int32Col()
    count = t.Int32Col()


class Gap_After_R(t.IsDescription):
    gap_after = t.Int32Col()
    count = t.Int32Col()


class OD_R(t.IsDescription):
    origin = t.Int32Col()
    destination = t.Int32Col()
    count = t.Int32Col()


class ODT_R(t.IsDescription):
    origin = t.Int32Col()
    destination = t.Int32Col()
    time = t.Int32Col()
    count = t.Int32Col()


class Mortality_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    mortality_f = t.Int32Col()


class Birth_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    childbirth_f = t.Int32Col()


class Aging_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    age_f = t.Int32Col()
    age_sq_f = t.Int32Col()


class Student_Residence_Choice_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    residence_type_f = t.Int32Col()


class Education_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    enroll = t.Int32Col()
    grade_disagg = t.Int32Col()
    educ_disagg = t.Int32Col()
    educ_in_yrs = t.Int32Col()


class Education_Forecast_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    enroll_f = t.Int32Col()
    grade_disagg_f = t.Int32Col()
    educ_disagg_f = t.Int32Col()
    educ_in_yrs_f = t.Int32Col()


class Labor_Participation_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    labor_participation_f = t.Int32Col()
    occupation_f = t.Int32Col()
    income_f = t.Int32Col()


class Marriage_Decision_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    marriage_decision_f = t.Int32Col()


class Divorce_Decision_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    divorce_decision_f = t.Int32Col()


class Household_Forecast_Population_R(t.IsDescription):
    houseid = t.Int64Col()
    bldgsz = t.Int32Col()
    hht = t.Int32Col()
    hinc = t.Int32Col()
    noc = t.Int32Col()
    persons = t.Int32Col()
    unittype = t.Int32Col()
    vehicl = t.Int32Col()
    wif = t.Int32Col()
    yrmoved = t.Int32Col()
    old_houseid = t.Int64Col()


class Household_Population_R(t.IsDescription):
    houseid = t.Int64Col()
    bldgsz = t.Int32Col()
    hht = t.Int32Col()
    hinc = t.Int32Col()
    noc = t.Int32Col()
    persons = t.Int32Col()
    unittype = t.Int32Col()
    vehicl = t.Int32Col()
    wif = t.Int32Col()
    yrmoved = t.Int32Col()


class Person_Forecast_Population_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    age = t.Int32Col()
    clwkr = t.Int32Col()
    educ_disagg = t.Int32Col()
    enroll = t.Int32Col()
    esr = t.Int32Col()
    indnaics = t.Int32Col()
    occcen5 = t.Int32Col()
    race1 = t.Int32Col()
    relate = t.Int32Col()
    sex = t.Int32Col()
    marstat = t.Int32Col()
    hours = t.Int32Col()
    grade_disagg = t.Int32Col()
    hispan = t.Int32Col()
    old_houseid = t.Int64Col()


class Person_Moving_Population_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    age = t.Int32Col()
    clwkr = t.Int32Col()
    educ = t.Int32Col()
    enroll = t.Int32Col()
    esr = t.Int32Col()
    indnaics = t.Int32Col()
    occcen5 = t.Int32Col()
    race1 = t.Int32Col()
    relate = t.Int32Col()
    sex = t.Int32Col()
    marstat = t.Int32Col()
    hours = t.Int32Col()
    grade = t.Int32Col()
    hispan = t.Int32Col()


class Person_Population_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    age = t.Int32Col()
    clwkr = t.Int32Col()
    educ_disagg = t.Int32Col()
    enroll = t.Int32Col()
    esr = t.Int32Col()
    indnaics = t.Int32Col()
    occcen5 = t.Int32Col()
    race1 = t.Int32Col()
    relate = t.Int32Col()
    sex = t.Int32Col()
    marstat = t.Int32Col()
    hours = t.Int32Col()
    grade_disagg = t.Int32Col()
    hispan = t.Int32Col()


class Age_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    age = t.Int32Col()
    count = t.Int32Col()


class Sex_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    sex = t.Int32Col()
    count = t.Int32Col()


class Race_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    race1 = t.Int32Col()
    count = t.Int32Col()


class Persons_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    persons = t.Int32Col()
    count = t.Int32Col()


class Hht_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    hht = t.Int32Col()
    count = t.Int32Col()


class Wif_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    wif = t.Int32Col()
    count = t.Int32Col()


class Noc_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    noc = t.Int32Col()
    count = t.Int32Col()
