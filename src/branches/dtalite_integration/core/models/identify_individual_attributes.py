from openamos.core.agents.person import Person
from openamos.core.agents.household import Household
from openamos.core.agents.activity import ActivityEpisode
from openamos.core.models.abstract_model import Model

from numpy import array, logical_and, histogram, zeros, unique
from openamos.core.data_array import DataArray


class IdentifyIndividualAttributes(Model):

    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification
        self.activityAttribs = self.specification.activityAttribs
        self.colNames = [self.activityAttribs.hidName,
                         self.activityAttribs.pidName,
                         self.activityAttribs.starttimeName,
                         self.activityAttribs.endtimeName]

    def create_col_numbers(self, colnamesDict):
        # print colnamesDict
        self.hidCol = colnamesDict[self.activityAttribs.hidName]
        self.pidCol = colnamesDict[self.activityAttribs.pidName]

        self.schidCol = colnamesDict[self.activityAttribs.scheduleidName]
        self.actTypeCol = colnamesDict[self.activityAttribs.activitytypeName]
        self.locidCol = colnamesDict[self.activityAttribs.locationidName]
        self.sttimeCol = colnamesDict[self.activityAttribs.starttimeName]
        self.endtimeCol = colnamesDict[self.activityAttribs.endtimeName]
        self.durCol = colnamesDict[self.activityAttribs.durationName]
        self.depPersonCol = colnamesDict[
            self.activityAttribs.dependentPersonName]

    def create_indices(self, data):
        idCols = data.columns([self.activityAttribs.hidName,
                               self.activityAttribs.pidName]).data
        combId = idCols[:, 0] * 100 + idCols[:, 1]
        comIdUnique, comId_reverse_indices = unique(
            combId, return_inverse=True)

        binsIndices = array(range(comId_reverse_indices.max() + 2))
        histIndices = histogram(comId_reverse_indices, bins=binsIndices)

        indicesRowCount = histIndices[0]
        indicesRow = indicesRowCount.cumsum()

        self.personIndicesOfActs = zeros((comIdUnique.shape[0], 4), dtype=int)

        self.personIndicesOfActs[:, 0] = comIdUnique / 100
        self.personIndicesOfActs[
            :, 1] = comIdUnique - self.personIndicesOfActs[:, 0] * 100
        self.personIndicesOfActs[1:, 2] = indicesRow[:-1]
        self.personIndicesOfActs[:, 3] = indicesRow

        hid = self.personIndicesOfActs[:, 0]

        hidUnique, hid_reverse_indices = unique(hid, return_inverse=True)

        binsHidIndices = array(range(hid_reverse_indices.max() + 2))
        histHidIndices = histogram(hid_reverse_indices, bins=binsHidIndices)

        indicesHidRowCount = histHidIndices[0]
        indicesHidRow = indicesHidRowCount.cumsum()

        self.hhldIndicesOfPersons = zeros((hidUnique.shape[0], 3))

        self.hhldIndicesOfPersons[:, 0] = hidUnique
        self.hhldIndicesOfPersons[1:, 1] = indicesHidRow[:-1]
        self.hhldIndicesOfPersons[:, 2] = indicesHidRow

    def resolve_consistency(self, data, seed):

        verts = []
        data.sort([self.activityAttribs.hidName,
                   self.activityAttribs.pidName,
                   self.activityAttribs.scheduleidName])

        # Create Index Matrix
        self.create_indices(data)
        self.create_col_numbers(data._colnames)

        for hhldIndex in self.hhldIndicesOfPersons:
            firstPersonRec = hhldIndex[1]
            lastPersonRec = hhldIndex[2]

            firstPersonFirstAct = self.personIndicesOfActs[firstPersonRec, 2]
            lastPersonLastAct = self.personIndicesOfActs[lastPersonRec - 1, 3]

            schedulesForHhld = DataArray(data.data[firstPersonFirstAct:
                                                   lastPersonLastAct, :], data.varnames)
            persIndicesForActsForHhld = self.personIndicesOfActs[firstPersonRec:
                                                                 lastPersonRec,
                                                                 :]

            householdObject = Household(hhldIndex[0])

            for perIndex in persIndicesForActsForHhld:
                personObject = Person(perIndex[0], perIndex[1])
                schedulesForPerson = DataArray(
                    data.data[perIndex[2]:perIndex[3], :], data.varnames)
                activityList = self.return_activity_list_for_person(
                    schedulesForPerson)
                personObject.add_episodes(activityList)

                householdObject.add_person(personObject)

            hhldVerts = householdObject.retrieve_fixed_activity_vertices(seed)
            # for i in hhldVerts:
            #	print i
            # raw_input()

            verts += hhldVerts

        return DataArray(verts, self.colNames)

    def return_activity_list_for_person(self, schedulesForPerson):
        # Updating activity list
        activityList = []
        for sched in schedulesForPerson.data:
            hid = sched[self.hidCol]
            pid = sched[self.pidCol]

            scheduleid = sched[self.schidCol]
            activitytype = sched[self.actTypeCol]
            locationid = sched[self.locidCol]
            starttime = sched[self.sttimeCol]
            endtime = sched[self.endtimeCol]
            duration = sched[self.durCol]
            depPersonId = sched[self.depPersonCol]

            actepisode = ActivityEpisode(hid, pid, scheduleid, activitytype, locationid,
                                         starttime, endtime, duration, depPersonId)
            activityList.append(actepisode)

        return activityList
