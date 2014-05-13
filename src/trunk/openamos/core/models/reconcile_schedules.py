from openamos.core.agents.person import Person
from openamos.core.agents.activity import ActivityEpisode
from openamos.core.models.abstract_model import Model

from numpy import array, logical_and, zeros, histogram

import time


class ReconcileSchedules(Model):
    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification
        self.activityAttribs = self.specification.activityAttribs

    def create_indices(self, data):
        idCols = data.columns([self.activityAttribs.hidName,
                               self.activityAttribs.pidName]).data
        combId = idCols[:,0]*100 + idCols[:,1]

        #print idCols[:20,:]
        #print 'comid', combId[:20]
        #print 'comid', combId[-20:]

        comIdUnique, comId_reverse_indices = unique(combId, return_inverse=True)

        #print 'unique', comIdUnique[:20]
        #print 'unique records', comIdUnique.shape
        #print 'reverse indices', comId_reverse_indices[:20]
        #print 'reverse indices', comId_reverse_indices[-20:]


        binsIndices = array(range(comId_reverse_indices.max()+2))

        histIndices = histogram(comId_reverse_indices, bins=binsIndices)
        #print histIndices[0][:20]
        #print histIndices[0][-20:]

        indicesRowCount = histIndices[0]

        indicesRow = indicesRowCount.cumsum()
        #print 'Row Count', indicesRowCount[:20]
        #print 'Row Index Low', indicesRow[:20]
        #print 'Row Index Hig', indicesRowHigh[:20]


        self.indices = zeros((comIdUnique.shape[0], 4), dtype=int)

        #print self.indices.shape
        #print idCols.shape
        #print indicesRow.shape
        #print binsIndices.shape

        self.indices[:,0] = comIdUnique/100
        self.indices[:,1] = comIdUnique - self.indices[:,0]*100

        self.indices[1:,2] = indicesRow[:-1]
        self.indices[:,3] = indicesRow

        #print self.indices[:20, :]
        #print self.indices[-20:, :]

        #raw_input('New implementation of indics -')



    def resolve_consistency(self, data, seed):
        actList = []
        data.sort([self.activityAttribs.hidName,
                   self.activityAttribs.pidName,
                   self.activityAttribs.scheduleidName])
        ti = time.time()
        # Create Index Matrix
        self.create_indices(data)

        print 'Indices created in %.4f' %(time.time()-ti)
        hidCol = data._colnames[self.activityAttribs.hidName]
        pidCol = data._colnames[self.activityAttribs.pidName]


        schidCol = data._colnames[self.activityAttribs.scheduleidName]
        actTypeCol = data._colnames[self.activityAttribs.activitytypeName]
        locidCol = data._colnames[self.activityAttribs.locationidName]
        sttimeCol = data._colnames[self.activityAttribs.starttimeName]
        endtimeCol = data._colnames[self.activityAttribs.endtimeName]
        durCol = data._colnames[self.activityAttribs.durationName]

        colNames = [self.activityAttribs.hidName,
                    self.activityAttribs.pidName,
                    self.activityAttribs.scheduleidName,
                    self.activityAttribs.activitytypeName,
                    self.activityAttribs.starttimeName,
                    self.activityAttribs.endtimeName,
                    self.activityAttribs.locationidName,
                    self.activityAttribs.durationName,
                    self.activityAttribs.dependentPersonName,
                    self.activityAttribs.tripCountName]



        row = 0

        for perIndex in self.indices:
            schedulesForPerson = data.data[perIndex[2]:perIndex[3],:]

            activityList = []
            for sched in schedulesForPerson:
                hid = sched[hidCol]
                pid = sched[pidCol]

                scheduleid = sched[schidCol]
                activitytype = sched[actTypeCol]
                locationid = sched[locidCol]
                starttime = sched[sttimeCol]
                endtime = sched[endtimeCol]
                duration = sched[durCol]

                actepisode = ActivityEpisode(hid, pid, scheduleid, activitytype, locationid,
                                             starttime, endtime, duration)
                activityList.append(actepisode)

            personObject = Person(perIndex[0], perIndex[1])
            personObject.add_episodes(activityList)
            personObject.reconcile_activity_schedules(seed)
            reconciledSchedules = personObject._collate_results_aslist()

            if not personObject._check_for_conflicts():
                raise Exception, "THE SCHEDULES ARE STILL MESSED UP"

            actList += reconciledSchedules
        return DataArray(actList, colNames)

import unittest
from numpy import genfromtxt, unique
from openamos.core.data_array import DataArray

class TestReconcileModel(unittest.TestCase):
    def setUp(self):
        self.data = genfromtxt("/home/kkonduri/simtravel/test/mag_zone/schedule_txt.csv", delimiter=",", dtype=int)
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
        #pid = unique(self.actSchedules.columns(['houseid', 'personid']).
        #acts = self.actSchedules

        #def


if __name__ == "__main__":
    unittest.main()
