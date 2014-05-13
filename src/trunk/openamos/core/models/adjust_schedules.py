from openamos.core.agents.person import Person
from openamos.core.agents.household import Household
from openamos.core.agents.activity import ActivityEpisode
from openamos.core.models.abstract_model import Model

from numpy import array, logical_and, zeros, histogram

import time


class AdjustSchedules(Model):
    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification
        self.activityAttribs = self.specification.activityAttribs
        self.arrivalInfoAttribs = self.specification.arrivalInfoAttribs
        self.occupancyInfoAttribs = self.specification.occupancyInfoAttribs
        self.dailyStatusAttribs = self.specification.dailyStatusAttribs
        self.dependencyAttribs = self.specification.dependencyAttribs

        self.schedAdjType = self.specification.schedAdjType

        self.colNames = [self.activityAttribs.hidName,
                         self.activityAttribs.pidName,
                         self.activityAttribs.scheduleidName,
                         self.activityAttribs.activitytypeName,
                         self.activityAttribs.starttimeName,
                         self.activityAttribs.endtimeName,
                         self.activityAttribs.locationidName,
                         self.activityAttribs.durationName,
                         self.activityAttribs.dependentPersonName,
                         self.activityAttribs.tripCountName]

    def create_indices(self, data):
        idCols = data.columns([self.activityAttribs.hidName,
                               self.activityAttribs.pidName]).data
        combId = idCols[:,0]*100 + idCols[:,1]
        comIdUnique, comId_reverse_indices = unique(combId, return_inverse=True)

        binsIndices = array(range(comId_reverse_indices.max()+2))
        histIndices = histogram(comId_reverse_indices, bins=binsIndices)

        indicesRowCount = histIndices[0]
        indicesRow = indicesRowCount.cumsum()


        self.personIndicesOfActs = zeros((comIdUnique.shape[0], 4), dtype=int)

        self.personIndicesOfActs[:,0] = comIdUnique/100
        self.personIndicesOfActs[:,1] = comIdUnique - self.personIndicesOfActs[:,0]*100
        self.personIndicesOfActs[1:,2] = indicesRow[:-1]
        self.personIndicesOfActs[:,3] = indicesRow

        #print self.personIndicesOfActs[:20, :]
        #print self.personIndicesOfActs[-20:, :]


        hid = self.personIndicesOfActs[:,0]

        hidUnique, hid_reverse_indices = unique(hid, return_inverse=True)

        binsHidIndices = array(range(hid_reverse_indices.max()+2))
        histHidIndices = histogram(hid_reverse_indices, bins=binsHidIndices)

        indicesHidRowCount = histHidIndices[0]
        indicesHidRow = indicesHidRowCount.cumsum()

        self.hhldIndicesOfPersons = zeros((hidUnique.shape[0], 3))

        self.hhldIndicesOfPersons[:,0] = hidUnique
        self.hhldIndicesOfPersons[1:,1] = indicesHidRow[:-1]
        self.hhldIndicesOfPersons[:,2] = indicesHidRow

        #print idCols[:30,:]
        #print self.hhldIndicesOfPersons[:20,:]
        #print self.personIndicesOfActs[:20,:]



        #raw_input('new implementation of indices')

        self.check_hhldIndices_for_multiple_person_arrivals()

    def check_hhldIndices_for_multiple_person_arrivals(self):
        numPersons = self.hhldIndicesOfPersons[:,-1] - self.hhldIndicesOfPersons[:,-2]
        numPersonGrt1Flag = numPersons > 1

        #if numPersonGrt1Flag.sum() > 0:
        #    print self.hhldIndicesOfPersons[numPersonGrt1Flag,:].astype(int)
        #raw_input('hhldIndices; checking for multiple person arrivals')



    def create_col_numbers(self, colNamesDict):
        self.hidCol = colNamesDict[self.activityAttribs.hidName]
        self.pidCol = colNamesDict[self.activityAttribs.pidName]

        self.schidCol = colNamesDict[self.activityAttribs.scheduleidName]
        self.actTypeCol = colNamesDict[self.activityAttribs.activitytypeName]
        self.locidCol = colNamesDict[self.activityAttribs.locationidName]
        self.sttimeCol = colNamesDict[self.activityAttribs.starttimeName]
        self.endtimeCol = colNamesDict[self.activityAttribs.endtimeName]
        self.durCol = colNamesDict[self.activityAttribs.durationName]
        self.depPersonCol = colNamesDict[self.activityAttribs.dependentPersonName]
        self.tripCountCol = colNamesDict[self.activityAttribs.tripCountName]

        if self.schedAdjType == "Arrival Adjustment":
            self.tripDependentPersonCol = colNamesDict[self.arrivalInfoAttribs.dependentPersonName]
            self.actualArrivalCol = colNamesDict[self.arrivalInfoAttribs.actualArrivalName]
            self.expectedArrivalCol = colNamesDict[self.arrivalInfoAttribs.expectedArrivalName]

        if self.schedAdjType == "Occupancy Adjustment":
            self.tripIndicatorCol = colNamesDict[self.occupancyInfoAttribs.tripIndicatorName]
            self.tripStTimeCol = colNamesDict[self.occupancyInfoAttribs.startTimeName]

        self.schoolStatusCol = colNamesDict[self.dailyStatusAttribs.schoolStatusName]
        self.workStatusCol = colNamesDict[self.dailyStatusAttribs.workStatusName]
        self.childDependencyCol = colNamesDict[self.dependencyAttribs.childDependencyName]


    def return_status_dependency(self, schedulesForPerson):
        workStatus = schedulesForPerson[0,self.workStatusCol]
        schoolStatus = schedulesForPerson[0,self.schoolStatusCol]
        childDependency = schedulesForPerson[0,self.childDependencyCol]

        #print 'wrkcol - %s, schcol - %s, depcol - %s' %(self.workStatusCol,
        #                                                self.schoolStatusCol,
        #                                                self.childDependencyCol)
        #print 'wrkst - %s, schst - %s, dep - %s' %(workStatus, schoolStatus,
        #                                           childDependency)

        # Checking for status and dependency
        # whether the merge happened correctly
        # this can be replaced with a simple extraction as opposed
        # to identifying unique values, checking for single value
        # and then updating the status variables
        """
        workStatusUnique = unique(schedulesForPerson.data[:, self.workStatusCol])
        if workStatusUnique.shape[0] > 1:
            print 'Work Status', workStatusUnique

            raise Exception, "More than one values for status/dependency"
        else:
            workStatus = workStatusUnique[0]

        schoolStatusUnique = unique(schedulesForPerson.data[:, self.schoolStatusCol])
        if schoolStatusUnique.shape[0] > 1:
            print 'School Status', schoolStatusUnique
            raise Exception, "More than one values for status/dependency"
        else:
            schoolStatus = schoolStatusUnique[0]

        childDependencyUnique = unique(schedulesForPerson.data[:, self.childDependencyCol])
        if childDependencyUnique.shape[0] > 1:
            print 'Child Dependency', childDependencyUnique
            raise Exception, "More than one values for status/dependency"
        else:
            childDependency = childDependencyUnique[0]

        #print 'wrkst - %s, schst - %s, dep - %s' %(workStatus, schoolStatus,
        #                                           childDependency)
        """
        return workStatus, schoolStatus, childDependency


    def return_trip_occupancy_info(self, schedulesForPerson):
        tripIndicator = schedulesForPerson[0, self.tripIndicatorCol]
        tripStTime = schedulesForPerson[0, self.tripStTimeCol]
        return tripIndicator, tripStTime

    def return_arrival_info(self, schedulesForPerson):
        actualArrival = schedulesForPerson[0,self.actualArrivalCol]
        expectedArrival = schedulesForPerson[0,self.expectedArrivalCol]
        tripDependentPerson = schedulesForPerson[0,self.tripDependentPersonCol]

        #print 'Actual Arrival - %s and Expected Arrival - %s ' %(actualArrival, expectedArrival)
        return actualArrival, expectedArrival, tripDependentPerson

    def return_activity_list_for_person(self, schedulesForPerson):
        # Updating activity list
        activityList = []
        for sched in schedulesForPerson:
            hid = sched[self.hidCol]
            pid = sched[self.pidCol]

            scheduleid = sched[self.schidCol]
            activitytype = sched[self.actTypeCol]
            locationid = sched[self.locidCol]
            starttime = sched[self.sttimeCol]
            endtime = sched[self.endtimeCol]
            duration = sched[self.durCol]
            depPersonId = sched[self.depPersonCol]
            tripCount = sched[self.tripCountCol]

            actepisode = ActivityEpisode(hid, pid, scheduleid, activitytype, locationid,
                                         starttime, endtime, duration, depPersonId, tripCount)
            activityList.append(actepisode)



        return activityList


    def resolve_consistency(self, data, seed):
        actList = []
        data.sort([self.activityAttribs.hidName,
                   self.activityAttribs.pidName,
                   self.activityAttribs.scheduleidName])
        ti = time.time()
        # Create Index Matrix
        self.create_indices(data)
        self.create_col_numbers(data._colnames)

        #print data._colnames, data.varnames

        print 'Indices created in %.4f' %(time.time()-ti)

        for hhldIndex in self.hhldIndicesOfPersons:
            firstPersonRec = hhldIndex[1]
            lastPersonRec = hhldIndex[2]

            persIndicesForActsForHhld = self.personIndicesOfActs[firstPersonRec:
                                                                     lastPersonRec,
                                                                 :]
            householdObject = Household(hhldIndex[0])

            for perIndex in persIndicesForActsForHhld:

                personObject = Person(perIndex[0], perIndex[1])
                schedulesForPerson = data.data[perIndex[2]:perIndex[3],:]
                activityList = self.return_activity_list_for_person(schedulesForPerson)
                personObject.add_episodes(activityList)

                workStatus, schoolStatus, childDependency = self.return_status_dependency(schedulesForPerson)
                personObject.add_status_dependency(workStatus, schoolStatus,
                                                   childDependency)

                householdObject.add_person(personObject)

                if self.schedAdjType == "Arrival Adjustment":
                    actualArrival, expectedArrival, tripDependentPerson = self.return_arrival_info(schedulesForPerson)
                    personObject.add_arrival_status(actualArrival, expectedArrival, tripDependentPerson)

                elif self.schedAdjType == "Occupancy Adjustment":
                    tripInd, tripStTime = self.return_trip_occupancy_info(schedulesForPerson)
                    #print 'trip indicator, trip start time -- ', tripInd, tripStTime
                    personObject.add_occupancy_status(tripInd, tripStTime)
                    householdObject.wait_push_subsequent_activities(personObject)
                else:
                    raise Exception, 'Invalid adjustment type ... '


            if self.schedAdjType == "Arrival Adjustment":
                householdObject.adjust_schedules_given_arrival_info(seed)
            elif self.schedAdjType == "Occupancy Adjustment":

                #raw_input()
                pass
            #raw_input()
            reconciledSchedules = householdObject._collate_results()

            if not personObject._check_for_conflicts():
                personObject.print_activity_list()
                print "THE SCHEDULES ARE STILL MESSED UP"
                raise Exception, "THE SCHEDULES ARE STILL MESSED UP"

            actList += reconciledSchedules

        print 'Finished running the component including index creation in %.4f' %(time.time()-ti)
        return DataArray(actList, self.colNames)



import unittest
from numpy import genfromtxt, unique
from openamos.core.data_array import DataArray

class TestReconcileModel(unittest.TestCase):
    def setUp(self):
        self.data = genfromtxt("/home/karthik/simtravel/test/mag_zone_dynamic/schedule_txt_small.csv", delimiter=",", dtype=int)
        colNames = ['scheduleid', 'houseid', 'personid', 'activitytype', 'locationid', 'starttime',
                    'endtime', 'duration', 'dependentpersonid']
        self.actSchedules = DataArray(self.data, colNames)


    def create_indices(self, data):
        idCols = data.columns(['houseid',
                               'personid']).data
        combId = idCols[:,0]*100 + idCols[:,1]
        comIdUnique, comId_reverse_indices = unique(combId, return_inverse=True)

        binsIndices = array(range(comId_reverse_indices.max()+2))
        histIndices = histogram(comId_reverse_indices, bins=binsIndices)

        indicesRowCount = histIndices[0]
        indicesRow = indicesRowCount.cumsum()


        self.personIndicesOfActs = zeros((comIdUnique.shape[0], 4), dtype=int)

        self.personIndicesOfActs[:,0] = comIdUnique/100
        self.personIndicesOfActs[:,1] = comIdUnique - self.personIndicesOfActs[:,0]*100
        self.personIndicesOfActs[1:,2] = indicesRow[:-1]
        self.personIndicesOfActs[:,3] = indicesRow

        #print self.personIndicesOfActs[:20, :]
        #print self.personIndicesOfActs[-20:, :]


        hid = self.personIndicesOfActs[:,0]

        hidUnique, hid_reverse_indices = unique(hid, return_inverse=True)

        binsHidIndices = array(range(hid_reverse_indices.max()+2))
        histHidIndices = histogram(hid_reverse_indices, bins=binsHidIndices)

        indicesHidRowCount = histHidIndices[0]
        indicesHidRow = indicesHidRowCount.cumsum()

        self.hhldIndicesOfPersons = zeros((hidUnique.shape[0], 3))

        self.hhldIndicesOfPersons[:,0] = hidUnique
        self.hhldIndicesOfPersons[1:,1] = indicesHidRow[:-1]
        self.hhldIndicesOfPersons[:,2] = indicesHidRow

        #print idCols[:30,:]
        #print self.hhldIndicesOfPersons[:20,:]
        #print self.personIndicesOfActs[:20,:]



        #raw_input('new implementation of indices')



    def test_retrieve_loop_ids(self):
        #houseIdsCol = self.actSchedules.columns(['houseid']).data
        #houseIdsUnique = unique(houseIdsCol)
        #print houseIdsUnique
        self.create_indices(self.actSchedules)

        for hid in self.hhldIndicesOfPersons:
            print hid


            """

            schedulesRowsIndForHh = houseIdsCol == hid
            schedulesForHh = self.actSchedules.rowsof(schedulesRowsIndForHh)

            pIdsCol = schedulesForHh.columns(['personid']).data
            pIdsUnique = unique(pIdsCol)

            for pid in pIdsUnique:
                schedulesRowIndForPer = pIdsCol == pid
                schedulesForPerson = schedulesForHh.rowsof(schedulesRowIndForPer)

                #print 'Raw schedules for hid:%s and pid:%s' %(hid, pid)
                #print schedulesForPerson

                activityList = []
                for sch in schedulesForPerson.data:
                    scheduleid = sch[2]
                    activitytype = sch[3]
                    locationid = sch[4]
                    starttime = sch[5]
                    endtime = sch[6]
                    duration = sch[7]

                    actepisode = ActivityEpisode(scheduleid, activitytype, locationid,
                                                 starttime, endtime, duration)
                    activityList.append(actepisode)
                personObject = Person(hid, pid)
                personObject.add_and_reconcile_episodes(activityList)
                #print '\tReconciled Activity schedules - ', personObject.reconciledActivityEpisodes
                #raw_input()
                """
        #pid = unique(self.actSchedules.columns(['houseid', 'personid']).
        #acts = self.actSchedules

        #def


if __name__ == "__main__":
    unittest.main()
