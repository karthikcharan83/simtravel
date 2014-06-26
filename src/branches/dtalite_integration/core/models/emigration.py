import os
import time
import csv
import copy
import re

from numpy import array, logical_and, histogram, zeros, amax, unique

from openamos.core.agents.person import Person
from openamos.core.agents.household import Household
from openamos.core.agents.activity import ActivityEpisode
from openamos.core.models.abstract_model import Model
from openamos.core.data_array import DataArray

from configuration.config_parser import ConfigParser as ConfigParserPopGen
from popgen_manager import PopgenManager


class Emigration(Model):

    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification

        self.idSpec = self.specification.idSpec
        self.hhldAttribs = self.specification.hhldAttribs
        self.personAttribs = self.specification.personAttribs
        self.popgenConfig = self.specification.popgenConfig

        self.hhldColNames = [self.idSpec.hidName,

                             self.hhldAttribs.bldgszName,
                             self.hhldAttribs.hhtName,
                             self.hhldAttribs.hincName,
                             self.hhldAttribs.nocName,
                             self.hhldAttribs.personsName,
                             self.hhldAttribs.unittypeName,
                             self.hhldAttribs.vehiclName,
                             self.hhldAttribs.wifName,
                             self.hhldAttribs.yrMovedName]
        self.personColNames = [self.idSpec.hidName,
                               self.idSpec.pidName,

                               self.personAttribs.ageName,
                               self.personAttribs.clwkrName,
                               self.personAttribs.educName,
                               self.personAttribs.enrollName,
                               self.personAttribs.esrName,
                               self.personAttribs.indnaicsName,
                               self.personAttribs.occcen5Name,
                               self.personAttribs.race1Name,
                               self.personAttribs.relateName,
                               self.personAttribs.sexName,
                               self.personAttribs.marstatName,
                               self.personAttribs.hoursName,
                               self.personAttribs.gradeName,
                               self.personAttribs.hispanName]

    def create_col_numbers(self, colnamesDict):
        # print colnamesDict
        self.hidCol = colnamesDict[self.idSpec.hidName]
        self.pidCol = colnamesDict[self.idSpec.pidName]

        self.bldgszCol = colnamesDict[self.hhldAttribs.bldgszName]
        self.hhtCol = colnamesDict[self.hhldAttribs.hhtName]
        self.hincCol = colnamesDict[self.hhldAttribs.hincName]
        self.nocCol = colnamesDict[self.hhldAttribs.nocName]
        self.personsCol = colnamesDict[self.hhldAttribs.personsName]
        self.unittypeCol = colnamesDict[self.hhldAttribs.unittypeName]
        self.vehiclCol = colnamesDict[self.hhldAttribs.vehiclName]
        self.wifCol = colnamesDict[self.hhldAttribs.wifName]
        self.yrMovedCol = colnamesDict[self.hhldAttribs.yrMovedName]

        self.ageCol = colnamesDict[self.personAttribs.ageName]
        self.clwkrCol = colnamesDict[self.personAttribs.clwkrName]
        self.educCol = colnamesDict[self.personAttribs.educName]
        self.enrollCol = colnamesDict[self.personAttribs.enrollName]
        self.esrCol = colnamesDict[self.personAttribs.esrName]
        self.indnaicsCol = colnamesDict[self.personAttribs.indnaicsName]
        self.occcen5Col = colnamesDict[self.personAttribs.occcen5Name]
        self.race1Col = colnamesDict[self.personAttribs.race1Name]
        self.relateCol = colnamesDict[self.personAttribs.relateName]
        self.sexCol = colnamesDict[self.personAttribs.sexName]
        self.marstatCol = colnamesDict[self.personAttribs.marstatName]
        self.hoursCol = colnamesDict[self.personAttribs.hoursName]
        self.gradeCol = colnamesDict[self.personAttribs.gradeName]
        self.hispanCol = colnamesDict[self.personAttribs.hispanName]

    def create_indices(self, data):
        idCols = data.columns([self.idSpec.hidName,
                               self.idSpec.pidName]).data
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

        print 'IDCols\n', idCols[:30, :].astype(int)
        print 'hhldIndices\n', self.hhldIndicesOfPersons[:20, :].astype(int)
        print 'personIndices\n', self.personIndicesOfActs[:20, :]

        #raw_input('new implementation of indices')

    def resolve_consistency(self, data, seed):
        print 'Data processing for use in PopGen'

        popgenConfigObject = ConfigParserPopGen(self.popgenConfig)
        popgenManagerObj = PopgenManager(configObject=self.popgenConfig)

        popgenConfigObject.parse_project()
        popgenConfigObject.parse_scenarios()
        scenario = popgenConfigObject.scenarioList[0]

        print 'Household vars - ', self.hhldColNames, len(self.hhldColNames)
        print 'Extra household vars - ', scenario.hhldVars, len(scenario.hhldVars)
        hhldVars = copy.deepcopy(self.hhldColNames)
        for var in scenario.hhldVars:
            if var not in hhldVars:
                hhldVars.append(var)

        print '\nHousehold vars - ', self.personColNames, len(self.personColNames)
        print 'Extra household vars - ', scenario.personVars, len(scenario.personVars)
        personVars = copy.deepcopy(self.personColNames)
        for var in scenario.personVars:
            if var not in personVars:
                personVars.append(var)

        print '\nHousehold sample file location - ', scenario.sampleUserProv.hhLocation
        print 'Person sample file location - ', scenario.sampleUserProv.personLocation

        # Create Index Matrix
        data.sort([self.idSpec.hidName, self.idSpec.pidName])
        self.create_indices(data)
        self.create_col_numbers(data._colnames)

        highestHid = amax(self.hhldIndicesOfPersons[:, 0])

        #fHhld = csv.writer(open(scenario.sampleUserProv.hhLocation, 'w'), delimiter=",")
        fHhld = open(scenario.sampleUserProv.hhLocation, 'w')

        hhldVars_forPopGen = copy.deepcopy(hhldVars)
        hidIndex = hhldVars_forPopGen.index('houseid')
        hhldVars_forPopGen[hidIndex] = 'hhid'

        hhldVars_forPopGen.insert(hidIndex + 1, 'serialno')
        hhldVars_forPopGen.insert(0, 'pumano')
        hhldVars_forPopGen.insert(0, 'state')
        print 'new hhldvars', hhldVars_forPopGen
        # fHhld.writerow(hhldVars_forPopGen)
        hhldVars_str = ''
        for var in hhldVars_forPopGen:
            hhldVars_str += '%s,' % var
        hhldVars_str = hhldVars_str[:-1]
        # fHhld.writerow(hhldVars_forPopGen)
        fHhld.write(hhldVars_str)
        fHhld.write('\n')

        personVars_forPopGen = copy.deepcopy(personVars)
        #fPerson = csv.writer(open(scenario.sampleUserProv.personLocation, 'w'), delimiter=",")
        fPerson = open(scenario.sampleUserProv.personLocation, 'w')

        hidIndex = personVars_forPopGen.index('houseid')
        personVars_forPopGen[hidIndex] = 'hhid'

        pidIndex = personVars_forPopGen.index('personid')
        personVars_forPopGen[pidIndex] = 'pnum'

        personVars_forPopGen.insert(hidIndex + 1, 'serialno')
        personVars_forPopGen.insert(0, 'pumano')
        personVars_forPopGen.insert(0, 'state')
        print 'new personvars', personVars_forPopGen
        personVars_str = ''
        for var in personVars_forPopGen:
            personVars_str += '%s,' % var
        personVars_str = personVars_str[:-1]
        # fPerson.writerow(personVars_forPopGen)
        fPerson.write(personVars_str)
        fPerson.write('\n')

        hhldCols = data.columns(hhldVars)
        personCols = data.columns(personVars)

        ti = time.time()
        hhldRow_forPopGen = [0] * len(hhldVars_forPopGen)
        hhldRow_forPopGen[0] = 24
        hhldRow_forPopGen[1] = 99

        personRow_forPopGen = [0] * len(personVars_forPopGen)
        personRow_forPopGen[0] = 24
        personRow_forPopGen[1] = 99

        for hhldIndex in self.hhldIndicesOfPersons:
            firstPersonRec = hhldIndex[1]
            lastPersonRec = hhldIndex[2]

            #personRecs = DataArray(data.data[firstPersonRec:lastPersonRec, :], data.varnames)

            hhldRow = hhldCols.data[firstPersonRec].astype(int)
            personRows = personCols.data[
                firstPersonRec:lastPersonRec].astype(int)

            # print 'Hhlds\n', hhldRow
            # print 'Persons\n', personRows

            # Writing out rows for the household sample file
            hhldRow_forPopGen[3:] = list(hhldRow)
            hhldRow_forPopGen[2] = hhldRow_forPopGen[3]
            # fHhld.writerow(list(hhldRow_forPopGen))
            fHhld.write(','.join(map(str, list(hhldRow_forPopGen))))
            fHhld.write('\n')

            # Writing out rows for the person sample file
            for personRow in personRows:
                personRow_forPopGen[3:] = personRow
                personRow_forPopGen[2] = personRow_forPopGen[3]
                # fPerson.writerow(list(personRow_forPopGen))
                fPerson.write(','.join(map(str, list(personRow_forPopGen))))
                fPerson.write('\n')
        fHhld.close()
        fPerson.close()
        print '\t Sample input files created in - %.4f' % (time.time() - ti)

        print 'Startint to synthesize population - '
        ti = time.time()
        popgenManagerObj = PopgenManager(configObject=self.popgenConfig)
        popgenManagerObj.run_scenarios()
        print '\t Synthesis complete in - %.4f' % (time.time() - ti)

        hhldSynLoc = scenario.synHousingTableNameLoc.location
        hhldSynFileName = scenario.synHousingTableNameLoc.name
        fHhldSyn = csv.reader(open(
            '%s%s%s.dat' % (hhldSynLoc, os.path.sep, hhldSynFileName), 'r'), delimiter='\t')
        hhldSynArr = self.load_file(fHhldSyn)
        print hhldSynArr[:5, :]
        hhldSynVars = self.parse_meta_file(
            '%s%s%s_meta.txt' % (hhldSynLoc, os.path.sep, hhldSynFileName))
        print 'Old var names - ', hhldSynVars

        hidIndex_popgen = hhldSynVars.index('hhid')
        hhldSynVars[hidIndex_popgen] = 'houseid'
        print 'New var names - ', hhldSynVars

        persSynLoc = scenario.synPersTableNameLoc.location
        persSynFileName = scenario.synPersTableNameLoc.name
        fPersSyn = csv.reader(open(
            '%s%s%s.dat' % (persSynLoc, os.path.sep, persSynFileName), 'r'), delimiter='\t')
        persSynArr = self.load_file(fPersSyn)
        print persSynArr[:5, :]
        personSynVars = self.parse_meta_file(
            '%s%s%s_meta.txt' % (persSynLoc, os.path.sep, persSynFileName))
        print 'Old var names - ', personSynVars

        hidIndex_popgen = personSynVars.index('hhid')
        personSynVars[hidIndex_popgen] = 'houseid'

        pidIndex_popgen = personSynVars.index('pnum')
        personSynVars[pidIndex_popgen] = 'personid'
        print 'New var names - ', personSynVars

        print '\nHousehold sample file location - ', scenario.synHousingTableNameLoc
        print 'Person sample file location - ', scenario.synPersTableNameLoc

        return DataArray(persSynArr, personSynVars), DataArray(hhldSynArr, hhldSynVars)

    def parse_meta_file(self, loc):
        varNames = []
        f = open(loc, 'r')
        for line in f:
            line = line.split(" ")
            varNames.append(line[-1][:-1])
        return varNames

    def load_file(self, f):
        arr = []
        for line in f:
            arr.append(line)
        arr = array(arr, int)
        return arr
