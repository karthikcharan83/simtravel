from openamos.core.agents.person import Person
from openamos.core.agents.activity import ActivityEpisode
from openamos.core.models.abstract_model import Model
from openamos.core.data_array import DataArray

from openamos.core.models.schedules_model_components import split_df
from openamos.core.models.schedules_model_components import resolve_by_multiprocessing
from openamos.core.models.schedules_model_components import return_act

import time

def reconcile_schedules(args):
    data = args[0]
    seed = args[1]
    activityAttribs = args[2]
    
    t = time.time()
    data["actobjects"] = data.apply(lambda x: return_act(x,  activityAttribs),  axis=1)
    
    pschedulesGrouped = data.groupby(level=[0,1], sort=False)    
    print "Size is %d and time taken to run the df apply - %.4f" %(data.shape[0], time.time()-t)
    
    t = time.time()
    actList = []
    for (hid,pid), pidSchedules in pschedulesGrouped:
        personObject = Person(hid, pid)
        
        activityList = list(pidSchedules["actobjects"].values)
        personObject.add_episodes(activityList)

        reconciledSchedules = personObject.reconcile_activity_schedules(seed)

        if not personObject._check_for_conflicts():
            raise Exception, "THE SCHEDULES ARE STILL MESSED UP"

        actList += reconciledSchedules

    print "Time taken to loop through all schedules - %.4f" %(time.time()-t)
    return actList


class ReconcileSchedules(Model):

    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification
        self.activityAttribs = self.specification.activityAttribs

        self.hidName = self.activityAttribs.hidName
        self.pidName = self.activityAttribs.pidName
        self.scheduleidName = self.activityAttribs.scheduleidName
        self.activitytypeName = self.activityAttribs.activitytypeName
        self.locationidName = self.activityAttribs.locationidName
        self.starttimeName = self.activityAttribs.starttimeName
        self.endtimeName = self.activityAttribs.endtimeName
        self.durationName = self.activityAttribs.durationName
        self.dependentPersonName = self.activityAttribs.dependentPersonName
        self.tripCountName = self.activityAttribs.tripCountName        

        self.colNames = [self.hidName,
                                  self.pidName,
                                  self.scheduleidName,
                                  self.activitytypeName,
                                  self.starttimeName,
                                  self.endtimeName,
                                  self.locationidName,
                                  self.durationName,
                                  self.dependentPersonName,
                                  self.tripCountName]


    def resolve_consistency(self, data, seed, numberProcesses):
        #TODO: add the number of workers/processes as an input in the config file

        splits = split_df(data.data, houseidCol=self.hidName, 
                                   workers=numberProcesses)
        args = [(split,seed,  self.activityAttribs) for split in splits]        
        
        resultList = []
        resultList += resolve_by_multiprocessing(func=reconcile_schedules, 
                                                                        args=args,  
                                                                        workers=numberProcesses)

        return DataArray(resultList,  self.colNames)
        
    """
    def resolve_consistency(self, data, seed):
        print "seed",  seed
        actList = []
        grpByCols = [self.hidName, self.pidName]
        for (hid, pid), pidSchedules in data.data.groupby(grpByCols,  sort=False):
            #for pid,  pidSchedules in hidSchedules.groupby(level=1, axis=0):
            personObject = Person(hid, pid)                
            activityList = self.return_activity_list_for_person(pidSchedules)
            personObject.add_episodes(activityList)
        
            reconciledSchedules = personObject.reconcile_activity_schedules(seed)

            if not personObject._check_for_conflicts():
                raise Exception, "THE SCHEDULES ARE STILL MESSED UP"

            actList += reconciledSchedules
            #personObject.print_activity_list()
        #raw_input("Completed reconciling schedules in %.4f" %(time.time()-ti))
        return DataArray(actList, self.colNames)
   """
    def return_activity_list_for_person(self, pidSchedules):
        # Updating activity list
        activityList = []
        for index, schedule in pidSchedules.iterrows():
            hid = schedule[self.hidName]
            pid = schedule[self.pidName]

            scheduleid = schedule[self.scheduleidName]
            activitytype = schedule[self.activitytypeName]
            locationid = schedule[self.locationidName]
            starttime = schedule[self.starttimeName]
            endtime = schedule[self.endtimeName]
            duration = schedule[self.durationName]

            actepisode = ActivityEpisode(hid, pid, scheduleid, activitytype, locationid,
                                         starttime, endtime, duration)
            activityList.append(actepisode)
        return activityList


import unittest
from numpy import genfromtxt, unique
from openamos.core.data_array import DataArray


class TestReconcileModel(unittest.TestCase):

    def setUp(self):
        self.data = genfromtxt(
            "/home/kkonduri/simtravel/test/mag_zone/schedule_txt.csv", delimiter=",", dtype=int)
        colNames = ['houseid', 'personid', 'scheduleid', 'activitytype', 'locationid', 'starttime',
                    'endtime', 'duration']
        self.actSchedules = DataArray(self.data, colNames)

    def test_retrieve_loop_ids(self):
        houseIdsCol = self.actSchedules.columns(['houseid']).data
        houseIdsUnique = unique(houseIdsCol)
        print houseIdsUnique

        for hid in houseIdsUnique:
            schedulesRowsIndForHh = houseIdsCol == hid
            schedulesForHh = self.actSchedules.rowsof(schedulesRowsIndForHh)

            pIdsCol = schedulesForHh.columns(['personid']).data
            pIdsUnique = unique(pIdsCol)

            for pid in pIdsUnique:
                schedulesRowIndForPer = pIdsCol == pid
                schedulesForPerson = schedulesForHh.rowsof(
                    schedulesRowIndForPer)

                # print 'Raw schedules for hid:%s and pid:%s' %(hid, pid)
                # print schedulesForPerson

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
                # print '\tReconciled Activity schedules - ', personObject.reconciledActivityEpisodes
                # raw_input()
        # pid = unique(self.actSchedules.columns(['houseid', 'personid']).
        #acts = self.actSchedules

        # def


if __name__ == "__main__":
    unittest.main()
