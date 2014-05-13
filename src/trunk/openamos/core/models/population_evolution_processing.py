from openamos.core.agents.person import Person
from openamos.core.agents.household import Household
from openamos.core.agents.activity import ActivityEpisode
from openamos.core.models.abstract_model import Model
from openamos.core.data_array import DataArray

from numpy import array, logical_and, histogram, zeros, amax, unique

class PopulationEvolutionProcessing(Model):
    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification

        self.agentType =self.specification.agentType
        self.idSpec = self.specification.idSpec
        self.hhldAttribs = self.specification.hhldAttribs
        self.personAttribs = self.specification.personAttribs
        self.evolutionAttribs = self.specification.evolutionAttribs


        self.hhldColNames = [self.idSpec.hidName,

                             self.hhldAttribs.bldgszName,
                             self.hhldAttribs.hhtName,
                             self.hhldAttribs.hincName,
                             self.hhldAttribs.nocName,
                             self.hhldAttribs.personsName,
                             self.hhldAttribs.unittypeName,
                             self.hhldAttribs.vehiclName,
                             self.hhldAttribs.wifName,
                             self.hhldAttribs.yrMovedName,
                             'old_houseid']
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
                             self.personAttribs.hispanName,

                             #self.evolutionAttribs.morality_fName,
                             #self.evolutionAttribs.birth_fName,
                             #self.evolutionAttribs.age_fName,
                             #self.evolutionAttribs.enrollment_fName,
                             #self.evolutionAttribs.grade_fName,
                             #self.evolutionAttribs.educ_fName,
                             #self.evolutionAttribs.educInYears_fName,
                             #self.evolutionAttribs.residenceType_fName,
                             #self.evolutionAttribs.laborParticipation_fName,
                             #self.evolutionAttribs.occupation_fName,
                             #self.evolutionAttribs.income_fName,
                             #self.evolutionAttribs.marriageDecision_fName,
                             #self.evolutionAttribs.divorceDecision_fName,
                             'old_houseid']



    def create_col_numbers(self, colnamesDict):
        #print colnamesDict
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

        self.morality_fCol = colnamesDict[self.evolutionAttribs.morality_fName]
        self.birth_fCol = colnamesDict[self.evolutionAttribs.birth_fName]
        self.age_fCol = colnamesDict[self.evolutionAttribs.age_fName]
        self.enrollment_fCol = colnamesDict[self.evolutionAttribs.enrollment_fName]
        self.grade_fCol = colnamesDict[self.evolutionAttribs.grade_fName]
        self.educ_fCol = colnamesDict[self.evolutionAttribs.educ_fName]
        self.educInYears_fCol = colnamesDict[self.evolutionAttribs.educInYears_fName]
        self.residenceType_fCol = colnamesDict[self.evolutionAttribs.residenceType_fName]
        self.laborParticipation_fCol = colnamesDict[self.evolutionAttribs.laborParticipation_fName]
        self.occupation_fCol = colnamesDict[self.evolutionAttribs.occupation_fName]
        self.income_fCol = colnamesDict[self.evolutionAttribs.income_fName]
        self.marriageDecision_fCol = colnamesDict[self.evolutionAttribs.marriageDecision_fName]
        self.divorceDecision_fCol = colnamesDict[self.evolutionAttribs.divorceDecision_fName]



    def create_indices(self, data):
        idCols = data.columns([self.idSpec.hidName,
                               self.idSpec.pidName]).data
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

        print 'IDCols\n', idCols[:30,:].astype(int)
        print 'hhldIndices\n', self.hhldIndicesOfPersons[:20,:].astype(int)
        print 'personIndices\n', self.personIndicesOfActs[:20,:]



        #raw_input('new implementation of indices')



    def resolve_consistency(self, data, seed):

        hhldAgentList = []
        personAgentList = []
        data.sort([self.idSpec.hidName,
                   self.idSpec.pidName])

        # Create Index Matrix
        self.create_indices(data)
        self.create_col_numbers(data._colnames)

        highestHid = amax(self.hhldIndicesOfPersons[:,0])

        for hhldIndex in self.hhldIndicesOfPersons:
            firstPersonRec = hhldIndex[1]
            lastPersonRec = hhldIndex[2]

            print 'HID - ', hhldIndex[0]

            personRecs = DataArray(data.data[firstPersonRec:lastPersonRec, :], data.varnames)
            print '\tPerson records - \n', personRecs.data.astype(int)



            householdObject = Household(hhldIndex[0])

            householdObject.set_household_attributes(

                                                     personRecs.data[0][self.bldgszCol],
                                                     personRecs.data[0][self.hhtCol],
                                                     personRecs.data[0][self.hincCol],
                                                     personRecs.data[0][self.nocCol],
                                                     personRecs.data[0][self.personsCol],
                                                     personRecs.data[0][self.unittypeCol],
                                                     personRecs.data[0][self.vehiclCol],
                                                     personRecs.data[0][self.wifCol],
                                                     personRecs.data[0][self.yrMovedCol])

            for personRec in personRecs.data:
                personObject = Person(personRec[self.hidCol], personRec[self.pidCol])

                personObject.set_person_attributes(personRec[self.ageCol],
                                                   personRec[self.clwkrCol],
                                                   personRec[self.educCol],
                                                   personRec[self.enrollCol],
                                                   personRec[self.esrCol],
                                                   personRec[self.indnaicsCol],
                                                   personRec[self.occcen5Col],
                                                   personRec[self.race1Col],
                                                   personRec[self.relateCol],
                                                   personRec[self.sexCol],
                                                   personRec[self.marstatCol],
                                                   personRec[self.hoursCol],
                                                   personRec[self.gradeCol],
                                                   personRec[self.hispanCol])

                personObject.set_evolution_attributes(personRec[self.morality_fCol],
                                                      personRec[self.birth_fCol],
                                                      personRec[self.age_fCol],
                                                      personRec[self.enrollment_fCol],
                                                      personRec[self.grade_fCol],
                                                      personRec[self.educ_fCol],
                                                      personRec[self.educInYears_fCol],
                                                      personRec[self.residenceType_fCol],
                                                      personRec[self.laborParticipation_fCol],
                                                      personRec[self.occupation_fCol],
                                                      personRec[self.income_fCol],
                                                      personRec[self.marriageDecision_fCol],
                                                      personRec[self.divorceDecision_fCol])


                householdObject.add_person(personObject)
            additionalHouseholdObject, highestHid = householdObject.evolve_population(highestHid)



            if householdObject.personsSize == 0:
                #raw_input('the household has a size of 0? and hid - %s' %hhldIndex[0])
                continue
            hhldAgentList.append([householdObject.hid,
                                  householdObject.bldgsz,
                                  householdObject.hht,
                                  householdObject.hinc,
                                  householdObject.noc,
                                  householdObject.personsSize,
                                  householdObject.unittype,
                                  householdObject.vehicl,
                                  householdObject.wif,
                                  householdObject.yrMoved,
                                  householdObject.oldHid])

            if additionalHouseholdObject is not None:
                hhldAgentList.append([additionalHouseholdObject.hid,
                                          additionalHouseholdObject.bldgsz,
                                          additionalHouseholdObject.hht,
                                          additionalHouseholdObject.hinc,
                                          additionalHouseholdObject.noc,
                                          additionalHouseholdObject.personsSize,
                                          additionalHouseholdObject.unittype,
                                          additionalHouseholdObject.vehicl,
                                          additionalHouseholdObject.wif,
                                          additionalHouseholdObject.yrMoved,
                                          additionalHouseholdObject.oldHid])



            personAgentList += householdObject.return_person_list()
            if additionalHouseholdObject is not None:
                personAgentList += additionalHouseholdObject.return_person_list()
                    #print additionalHouseholdObject.return_person_list()
                    #raw_input()

        print self.personColNames
        print array(personAgentList).shape
        print self.hhldColNames
        print array(hhldAgentList).shape

        return DataArray(personAgentList, self.personColNames), DataArray(hhldAgentList, self.hhldColNames)
