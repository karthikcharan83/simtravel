import copy
import heapq as hp
from numpy import array, zeros

from openamos.core.models.abstract_random_distribution_model import RandomDistribution
from openamos.core.agents.person import Person

class Household(object):
    def __init__(self, hid):
        self.hid = hid
        self.persons = {}
        self.dependencyPersonIds = []
        self.dailyFixedActPersonIds = []
        self.noDailyFixedActPersonIds = []
        self.indepPersonIds = []
        self.numPersons = 0


        # Household attributes for evolution
        self.bldgsz = 0
        self.hht = 0
        self.hinc = 0
        self.noc = 0
        self.personsSize = 0
        self.unittype = 0
        self.vehicl = 0
        self.wif = 0
        self.yrMoved = 0
        self.oldHid = 0
        self.partnerHousehold = None

        self.rndGen = RandomDistribution(int(self.hid))


        self.relateDict = {1:'Householder',
                           2:'Husband/Wife',
                           3:'Natural born son/daughter',
                           4:'Adopted son/daughter',
                           5:'Stepson/stepdaughter',
                           6:'Brother/sister',
                           7:'Father/mother',
                           8:'Grandchild',
                           9:'Parent-in-law',
                           10:'Son-in-law/daughter-in-law',
                           11:'Other relative',
                           12:'Brother-in-law/sister-in-law',
                           13:'Nephew/niece',
                           14:'Grandparent',
                           15:'Uncle/aunt',
                           16:'Cousin',
                           17:'Roomer/boarder',
                           18:'Housemate/roommate',
                           19:'Unmarried partner',
                           20:'Foster child',
                           21:'Other nonrelative',
                           22:'Institutionalized GQ person',
                           23:'Noninstitutionalized GQ person'}

        self.hhtDict = {0:"Not in universe (Vacant or GQ)",
                             1:"Family household: Married-couple",
                             2:"Family household: Male householder, no wife present",
                             3:"Family household: Female householder, no husband present",
                             4:"Nonfamily household: Male householder, living alone",
                             5:"Nonfamily household: Male householder, not living alone",
                             6:"Nonfamily household: Female householder, living alone",
                             7:"Nonfamily household: Female householder, not living alone"}

        self.sexDict = {1:'Male', 2:'Female'}

        self.raceDict = {1:'White alone',
                         2:'Black or African American alone',
                         3:'American Indian alone',
                         4:'Alaska Native alone',
                         5:'American Indian and Alaska Native tribes specified, and American Indian or Alaska Native, not specified, and no other races',
                         6:'Asian alone',
                         7:'Native Hawaiian and Other Pacific Islander alone',
                         8:'Some other race alone',
                         9:'Two or more major race groups'
                        }

        self.hhldrAlive = True


    def add_person(self, person):
        # person is an object of the Person class
        person.hid = self.hid
        self.persons[person.pid] = person
        self.personsSize += 1
        if person.age < 18:
            self.noc += 1
        if person.laborParticipation_f == 1:
            self.wif += 1
            print 'Adding employed person ... '
        self.hinc += person.incomeCont

        if person.child_dependency == 1:
            self.dependencyPersonIds.append(person.pid)
        elif person.workstatus == 1 or person.schoolstatus == 1:
            self.dailyFixedActPersonIds.append(person.pid)
            self.indepPersonIds.append(person.pid)
        else:
            self.noDailyFixedActPersonIds.append(person.pid)
            self.indepPersonIds.append(person.pid)

    def remove_person(self, personId):
        person = self.persons.pop(personId)
        self.personsSize -= 1
        if person.age < 18:
            self.noc -= 1
        if person.laborParticipation_f == 1:
            self.wif -= 1
            print 'Removing employed person ... '
        self.hinc -= person.incomeCont
        print 'Updating income removing income of person leaving'
        return person




    def return_person_list(self):
        personList = []
        for personId in self.persons.keys():
            person = self.persons[personId]
            if person.race1 == 0:
                raw_input('Print the race of the person: hid- %s and pid - %s is 0' %(self.hid, person.pid))
            personList.append([person.hid,
                               person.pid,
                                person.age_f,
                                person.clwkr,
                                person.educ_f,
                                person.enrollment_f,
                                person.esr,
                                person.indnaics,
                                person.occupation_f,
                                person.race1,
                                person.relate,
                                person.sex,
                                person.marstat,
                                person.hours,
                                person.grade_f,
                                person.hispan,
                                self.oldHid])

        return personList





    def set_household_attributes(self, bldgsz, hht, hinc, noc,
                                 persons, unittype, vehicl, wif,
                                 yrMoved):
        self.bldgsz = bldgsz
        self.hht = hht
        #self.hinc = hinc (No need to assign these; they are updated as person objects are added)
        #self.noc = noc (No need to assign these; they are updated as person objects are added)
        #self.persons = persons (No need to assign these; they are updated as person objects are added)
        self.unittype = unittype
        self.vehicl = vehicl
        #self.wif = wif (No need to assign these; they are updated as person objects are added)
        self.yrMoved = yrMoved

    def print_person_relationship_gender(self):
        personIds = copy.deepcopy(self.persons.keys())
        print '\n    Household Id - ', self.hid
        for personId in personIds:
            person = self.persons[personId]
            print """\t    Relationship of person - %s, """\
                        """relationship - %s, gender - %s and race - %s' """%(person.pid,
                                                                              self.relateDict[person.relate],
                                                                              self.sexDict[person.sex],
                                                                              self.raceDict[person.race1])


    def evolve_population(self, highestHid):
        # All data dictionaries are borrowed directly from PUMS 2000
        # Once a full implementation is complete we can extend the code
        # to generalize the data dictionaries


        self.highestHid = highestHid


        # Printing relationship for current residents of the household
        print 'HOUSEHOLD ID - %s' %self.hid
        print '\tHousehold type - ', self.hhtDict[self.hht]
        personIds = copy.deepcopy(self.persons.keys())
        """
        for personId in personIds:
            person = self.persons[personId]
            print '\t    Relationship of all people - %s and gender - %s' %(self.relateDict[person.relate], self.sexDict[person.sex])
        """
        self.print_person_relationship_gender()
        # Processing birth
        birthFlag = False
        personIds = copy.deepcopy(self.persons.keys())
        for personId in personIds:
            person = self.persons[personId]

            if person.birth_f == 1:
                self.process_birth()
                birthFlag = True
        if birthFlag:
            print '1. After birth processing'
            print '\t\tOld Household type - ', self.hhtDict[self.hht]
            self.print_person_relationship_gender()
            print '\t\tNew Household type - ', self.hhtDict[self.hht]
            #raw_input("birth processing; press any key to continue...")

        # Processing mortality
        mortalityFlag = False
        personIds = copy.deepcopy(self.persons.keys())
        self.allAlive = True
        for personId in personIds:
            person = self.persons[personId]
            #print '\tRelationship of all people - %s and gender - %s' %(self.relateDict[person.relate], self.sexDict[person.sex])
            if person.mortality_f == 1:
                self.allAlive = False
                self.process_mortality(personId)
                mortalityFlag = True
                if person.relate == 1:
                    self.hhldrAlive = False




        if mortalityFlag:
            print '2. After Mortality Processing'
            self.print_person_relationship_gender()
            print '\t\tOld Household type - ', self.hhtDict[self.hht]
            self.process_household_type_after_mortality()
            print '\t\tNew Household type - ', self.hhtDict[self.hht]
            #raw_input("mortality processing done ... press any key to continue...")



        #TODO: Processing child leaving


        # Processing divorce
        divorceFlag = False
        personIds = copy.deepcopy(self.persons.keys())
        self.divorce = False
        for personId in personIds:
            person = self.persons[personId]
            if person.divorceDecision_f == 1:
                print '3. Before divorce processing'
                self.print_person_relationship_gender()
                partnerHousehold = self.process_divorce()
                self.partnerHousehold = partnerHousehold
                divorceFlag = True
                self.divorce = True
                break



        if divorceFlag:
            self.process_household_type_after_divorce()
            if partnerHousehold is not None:
                partnerHousehold.process_household_type_after_divorce()

        if divorceFlag:
            print '3. After divorce processing'
            self.print_person_relationship_gender()
            print '\t\tHousehold size - ', self.personsSize
            print '\t\tNumber of children - ', self.noc
            print '\t\tVehicle count - ', self.vehicl
            print '\t\tCount of workers in family - ', self.wif
            print '\t\tHousehold type - ', self.hhtDict[self.hht]
            if partnerHousehold is not None:
                partnerHousehold.print_person_relationship_gender()
                print '\t\tHousehold size - ', partnerHousehold.personsSize
                print '\t\tNumber of children - ', partnerHousehold.noc
                print '\t\tVehicle count - ', partnerHousehold.vehicl
                print '\t\tCount of workers in family - ', partnerHousehold.wif
                print '\t\tHousehold type - ', self.hhtDict[partnerHousehold.hht]

            #raw_input("divorce done ... press any key to continue...")
        else:
            partnerHousehold = None




        #if self.hid == '40001512':
        #    raw_input()


        #TODO:update the household type for this household and partner's household
        #TODO:update the household income for this household and partner's household
        #TODO:update the unit type for this household and partner's household
        #TODO:update the vehicle count for this household and partner's household
        #TODO:update the number of workers for this household and partner's household
        #TODO:update the yrmoved for this household and partner's household


        #TODO:update PERSON ATTRIBUTES


        return partnerHousehold, self.highestHid

    def process_birth(self):
        print '\n--1. Person born--'
        maxPid = max(self.persons.keys())
        personNew = Person(self.hid, maxPid + 1)

        sexRndNum = self.rndGen.return_uniform()
        if sexRndNum<= 0.5:
            sex = 1
        else:
            sex = 2

        personNew.sex = sex
        personNew.relate = 3
        personNew.marstat = 5


        hhldrId = False
        partnerId = False
        for personId in self.persons.keys():
            person = self.persons[personId]
            if person.relate == 1:
                hhldrId = personId
            elif person.relate == 2:
                partnerId = personId

        if hhldrId <> False:
            hhldr = self.persons[hhldrId]
            personNew.hispan = hhldr.hispan

        if hhldrId <> False and partnerId <> False:
            hhldr = self.persons[hhldrId]
            partner = self.persons[partnerId]

            if hhldr.race1 == partner.race1:
                personNew.race1 = hhldr.race1

            if hhldr.race1 <> partner.race1:
                personNew.race1 = 9



            print 'Hhldr race - %s and partner race - %s and new Kids race - %s' %(hhldr.race1, partner.race1, personNew.race1)

        if hhldrId <> False and partnerId == False:
            hhldr = self.persons[hhldrId]
            personNew.race1 = hhldr.race1

            print 'Hhldr race - %s and partner race - %s and new Kids race - %s' %(hhldr.race1, None, personNew.race1)

        if hhldrId == False and partnerId == False:
            print 'Non family household?'
            for personId in self.persons.keys():
                person = self.persons[personId]
                if person.birth_f == 1:
                    print 'Person Id bearing the child - %s' %personId
                    personNew.race1 = person.race1

        self.add_person(personNew)


    def process_mortality(self, personId):
        # Remove person record
        print '\n--2. Person expired need to remove record and update household attributes--'

        print '\tPerson ids list', self.persons.keys()
        #person = self.persons.pop(personId)
        person = self.persons[personId]

        # Update marriage status for the partner
        if person.marstat == 1:
            hhldrId, partnerId = self.identify_hhldr_partner_id()
            if hhldrId == personId and partnerId <> False:
                partner = self.persons[partnerId]
                partner.marstat = 2

            if hhldrId <> False and partnerId == personId:
                hhldr = self.persons[partnerId]
                hhldr.marstat = 2

        self.remove_person(personId)

        print '\tNew Person ids list', self.persons.keys()
        print


    def process_divorce(self):
        print '\n--k. Divorce occurred need to dissolve the household--'

        if self.hht >=4 and self.hht <=7:
            self.print_person_relationship_gender()
            print ('Non family household seeking divorce')
        partnerHousehold = None


        hhldrId, partnerId = self.identify_hhldr_partner_id()


        if hhldrId <> False:
            hhldr = self.persons[hhldrId]
            hhldr.marstat = 3                   # changing the marriage status of the hhldr

        if partnerId <> False:
            partner = self.persons[partnerId]
            partner.marstat = 3                         # changing the marriage status of the partner
            partner.relate = 1                          # changing the relationship status to householder

        if hhldrId == False or partnerId == False:
            print '\tOne or more partners was not identified husbandPid - %s and wifePid - %s' %(hhldrId, partnerId)
            #raw_input("\tNo need to dissolve the household one or both are missing from the household due to passign away")

        if hhldrId and partnerId:
            print '\tBoth partners were identified husbandPid - %s and wifePid - %s' %(hhldrId, partnerId)


            self.highestHid += 1
            partnerHousehold = Household(self.highestHid)

            print '\t    a. Allocate the partner'
            #partner = self.persons.pop(partnerId)
            partner = self.remove_person(partnerId)
            partnerHousehold.add_person(partner)

            print '\tMembers in the household other than the householder and partner- '

            otherIds = []
            ownFamily = []
            partnersFamily = []

            personIds = copy.deepcopy(self.persons.keys())
            for personId in personIds:
                person = self.persons[personId]

                print '\t    Relationship of surviving - %s and gender - %s' %(self.relateDict[person.relate], self.sexDict[person.sex])
                if person.relate == 3 or person.relate == 4: # Own kids / adopted kids
                    otherIds.append(personId)
                elif person.relate == 5:                     # Stepson/stepdaughter
                    partnersFamily.append(personId)
                    person.relate = 3                           # updating the relationship status to Natural born son/daughter
                elif person.relate == 6:                     # Brother/sister
                    ownFamily.append(personId)
                elif person.relate == 7:                     # Father/mother
                    ownFamily.append(personId)
                elif person.relate == 9:                     # Parent-in-law
                    partnersFamily.append(personId)
                    person.relate = 7                           # updating the relationship status to Father/mother
                elif person.relate == 12:                    # Brother-in-law/Sister-in-law
                    partnersFamily.append(personId)
                    person.relate = 6                           # updating the relationship status to Father/mother
                elif person.relate <> 1 and person.relate <> 2:
                    otherIds.append(personId)


            print '\t    c. Partners Family - ', partnersFamily
            print '\t\t Allocating partner kids'
            for paId in partnersFamily:
                #partnersKid = self.persons.pop(partnersKidId)
                partnersKid = self.remove_person(paId)
                partnerHousehold.add_person(partnersKid)

            print '\t    d. Own family - ', ownFamily

            print '\t    f. Other - ', otherIds
            print '\t\t Allocating others'
            for otherId in otherIds:
                otherRndNum = self.rndGen.return_uniform()
                if otherRndNum <= 0.5:
                    other = self.remove_person(otherId)
                    partnerHousehold.add_person(other)

            print '\t    Splitting the vehicle fleet'
            print '\t\tvehicle Count - ', self.vehicl


            vehiclOriHhld = self.rndGen.return_random_integers(0, self.vehicl, 1)[0]

            partnerHousehold.vehicl = self.vehicl - vehiclOriHhld
            self.vehicl = vehiclOriHhld

            print '\t\tVehicle count to new hhld - '            , partnerHousehold.vehicl
            print '\t\tVehicle count to original hhld - '               , self.vehicl


            partnerHousehold.oldHid = self.hid
            partnerHousehold.divorce = True
            #raw_input("\tvehicle allocation as shown above ... ")
            """
            if hhldr.sex == 1 and len(self.persons) == 1:
                self.hht = 4 # Non family household: Male householder living alone
            elif hhldr.sex == 2 and len(self.persons) == 1:
                self.hht = 6 # Non family household: Female householder living alone

            elif self.check_if_family() and hhldr.sex == 1:
                self.hht = 2 # Family household: Male householder
            elif self.check_if_family() and hhldr.sex == 2:
                self.hht = 3 # Family household: Female householder

            elif not self.check_if_family() and hhldr.sex == 1:
                self.hht = 5 # Non Family household: Male householder
            elif not self.check_if_family() and hhldr.sex == 2:
                self.hht = 7 # Non Family household: Female householder


            if partner.sex == 1 and len(partnerHousehold.persons) == 1:
                partnerHousehold.hht = 4 # Non family household: Male householder living alone
            elif partner.sex == 2 and len(partnerHousehold.persons) == 1:
                partnerHousehold.hht = 6 # Non family household: Female householder living alone

            elif partnerHousehold.check_if_family() and partner.sex == 1:
                partnerHousehold.hht = 2 # Family household: Male householder
            elif partnerHousehold.check_if_family() and partner.sex == 2:
                partnerHousehold.hht = 3 # Family household: Female householder

            elif not partnerHousehold.check_if_family() and partner.sex == 1:
                partnerHousehold.hht = 5 # Non Family household: Male householder
            elif not partnerHousehold.check_if_family() and partner.sex == 2:
                partnerHousehold.hht = 7 # Non Family household: Female householder
            """


        return partnerHousehold


    def check_if_family(self):
        for pid in self.persons:
            person = self.persons[pid]

            if (person.relate >= 3 and person.relate <=16):
                return True
        return False

    def identify_hhldr_partner_id(self, hid=None):
        hhldrId = False
        partnerId = False
        if hid is None:
            personsDict = self.persons
        else:
            personsDict = hid.persons

        personIds = copy.deepcopy(personsDict.keys())
        for personId in personIds:
            person = personsDict[personId]
            # Male householder
            if person.relate == 1 and person.sex == 1:
                print '\tIdentified the male householder in the marriage - ', personId
                hhldrId = personId
            # female non-householder
            if person.relate == 2 and person.sex == 2:
                print '\tIdentified the female non-householder in the marriage - ', personId
                partnerId = personId
            # female householder
            if person.relate == 1 and person.sex == 2:
                print '\tIdentified the female householder in the marriage - ', personId
                hhldrId = personId
            # male non-householder
            if person.relate == 2 and person.sex == 1:
                print '\tIdentified the male non-householder in the marriage - ', personId
                partnerId = personId
        return hhldrId, partnerId

    def process_household_type_after_divorce(self):
        print '\n--k+1. Process the household type --'
        print '\tOriginal household type - %s' %self.hhtDict[self.hht]
        print '\tDid a divorce happen - %s' %self.divorce

        hhldrId, partnerId = self.identify_hhldr_partner_id()

        if hhldrId == False or partnerId == False:
            print '\tOne or more partners was not identified husbandPid - %s and wifePid - %s hence house was not split and no further processing' %(hhldrId, partnerId)
            return
        hhldr = self.persons[hhldrId]


        if hhldr.sex == 1 and len(self.persons) == 1:
            self.hht = 4 # Non family household: Male householder living alone
        elif hhldr.sex == 2 and len(self.persons) == 1:
            self.hht = 6 # Non family household: Female householder living alone

        elif self.check_if_family() and hhldr.sex == 1:
            self.hht = 2 # Family household: Male householder
        elif self.check_if_family() and hhldr.sex == 2:
            self.hht = 3 # Family household: Female householder

        elif not self.check_if_family() and hhldr.sex == 1:
            self.hht = 5 # Non Family household: Male householder
        elif not self.check_if_family() and hhldr.sex == 2:
            self.hht = 7 # Non Family household: Female householder



        #raw_input ('\tNEW hht - %s' %self.hhtDict[self.hht])

    def process_household_type_after_mortality(self):
        if self.personsSize == 0:
            self.hht = 0
            return
        hhldrId, partnerId = self.identify_hhldr_partner_id()

        if hhldrId <> False:
            # Householder alive
            print '\t\tNo need to identify new householder ... id is pid - %s' %hhldrId
            hhldr = self.persons[hhldrId]
        elif partnerId <> False:
            # Householder not alive
            print '\t\tPartner is the new householder ... id is pid - %s' %partnerId
            hhldr = self.persons[partnerId]
            hhldr.relate = 1
        else:
            print '\t\tNeed to identify new householder ... id is pid - %s'
            oldestPersonId = self.eldest_person()
            hhldr = self.persons[oldestPersonId]
            print '\t\t THe oldest person is - %s and relationship is - %s' %(hhldr.pid, self.relateDict[hhldr.relate])
            hhldr.relate = 1
            print '\t\t\tThe oldest person is now a householder and all other family members are designated as other relatives for now this needs to be expanded ... '

            for personId in self.persons.keys():
                if personId == hhldr.pid:
                    continue
                else:
                    person = self.persons[personId]
                    if person.relate >= 3 and person.relate <= 16:
                        person.relate = 11
            self.print_person_relationship_gender()

        if hhldrId <> False and partnerId <> False:
            self.hht = 1
            return


        if hhldr.sex == 1 and len(self.persons) == 1:
            self.hht = 4 # Non family household: Male householder living alone
        elif hhldr.sex == 2 and len(self.persons) == 1:
            self.hht = 6 # Non family household: Female householder living alone

        elif self.check_if_family() and hhldr.sex == 1:
            self.hht = 2 # Family household: Male householder
        elif self.check_if_family() and hhldr.sex == 2:
            self.hht = 3 # Family household: Female householder

        elif not self.check_if_family() and hhldr.sex == 1:
            self.hht = 5 # Non Family household: Male householder
        elif not self.check_if_family() and hhldr.sex == 2:
            self.hht = 7 # Non Family household: Female householder

        if hhldrId == False and partnerId == False:
            print 'New household type - ', self.hhtDict[self.hht]
            #raw_input('Need to process differently here ... ')

    def eldest_person(self):
        oldest = 0
        if len(self.persons) == 1:
            return self.persons.keys()[0]
        for personId in self.persons.keys():
            person = self.persons[personId]
            if person.age > oldest:
                oldest = copy.deepcopy(person.age)
                oldestId = personId
        return oldestId


    def identify_family_member_ids(self):
        personIds = copy.deepcopy(self.persons.keys())
        others = []
        family = []
        for personId in personIds:
            person = self.persons[personId]

            if person.relate >= 3 and person.relate <=16:
                family.append(personId)
            elif person.relate > 16:
                family.append(personId)

        return family, others



    def _collate_results(self):
        resList = []
        for pid in self.persons:
            person = self.persons[pid]


            for actStart, act in person.listOfActivityEpisodes:
                resList.append([self.hid, pid, act.scheduleId,
                                act.actType, act.startTime, act.endTime,
                                act.location, act.duration, act.dependentPersonId,
                                act.tripCount])
        return resList

    def _collate_results_without_dependentActs(self):
        resList = []
        for pid in self.dependencyPersonIds:
            person = self.persons[pid]
            for actStart, act in person.listOfActivityEpisodes:
                if act.dependentPersonId == 0 or act.dependentPersonId == 99:
                    resList.append([self.hid, pid, act.scheduleId,
                                   act.actType, act.startTime, act.endTime,
                                   act.location, act.duration, act.dependentPersonId,
                                   act.tripCount])

        for pid in self.indepPersonIds:
            person = self.persons[pid]
            for actStart, act in person.listOfActivityEpisodes:
                resList.append([self.hid, pid, act.scheduleId,
                                act.actType, act.startTime, act.endTime,
                                act.location, act.duration, act.dependentPersonId,
                                act.tripCount])

        return resList



    def _check_for_dependency(self, person):
        if person.child_dependency == 1:
            return True
        else:
            return False

    def _check_for_dailyFixedActStatus(self, person):
        if person.workstatus == 1 or person.schoolstatus == 1:
            return True
        else:
            return False


    def retrieve_fixed_activity_vertices(self, seed):
        verts = []

        for pid in self.persons:
            person = self.persons[pid]

            personVerts = person.retrieve_fixed_activity_ends(seed)
            verts.append(personVerts)

        return verts



    def clean_schedules_for_in_home_episodes(self, seed):
        self.personIds = self.persons.keys()
        self.personIds.sort()

        for pid in self.personIds:
            person = self.persons[pid]
            person.clean_schedules_for_in_home_episodes()

            if not person._check_for_conflicts():
                self.print_activity_list(person)
                raise Exception, 'The person still has conflicts - %s, %s' %(self.hid, pid)

        return self._collate_results()


    def clean_schedules(self, seed):
        #print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        #print '\tPerson Ids with fixed activities - ', self.dailyFixedActPersonIds
        #print '\tPerson Ids with no fixed activities - ', self.noDailyFixedActPersonIds

        self.personIds = self.persons.keys()
        self.personIds.sort()

        # delete fixed work episodes
        for pid in self.personIds:
            person = self.persons[pid]
            if person.workstatus == 0:
                self.remove_work_episodes(person)

        # delete fixed school episodes
        for pid in self.personIds:
            person = self.persons[pid]
            if person.schoolstatus == 0:
                self.remove_school_episodes(person)

        return self._collate_results()

    def remove_work_episodes(self, person):
        person.extract_work_episodes()
        person.remove_episodes(person.workEpisodes)

    def remove_school_episodes(self, person):
        person.extract_school_episodes()
        person.remove_episodes(person.schoolEpisodes)


    def resolve_conflicts_for_dependency_activities(seed):
        return self._collate_results()



    def adjust_schedules_given_arrival_info(self, seed, personarrivedId=None):
        #print 'person arrived id - ', personarrivedId
        #personarrived = self.persons[personarrivedId]

        #print 'number of persons for this household that arrived including dependents - %s and they are pids - %s' %(len(self.persons), self.persons.keys())

        #raw_input('press to proceed to schedule adjustment')

        indepPidsForAdj = []
        for pid in self.persons.keys():
            personarrived = self.persons[pid]

            if (personarrived.child_dependency == 1 or
                (personarrived.expectedArrival == 0 and personarrived.actualArrival == 0)):
                #print '\tAdjusting schedules for houseid - %s and pid - %s' %(personarrived.hid, personarrived.pid)
                #print '\t    the schedule for this person need not be modified; this person is not independent and can only be adjusted due to schedule adjustment of adult'
                continue
            indepPidsForAdj.append(pid)

        for pid in indepPidsForAdj:
            self.affectedActs = {}
            personarrived = self.persons[pid]

            #print '\tAdjusting schedules for houseid - %s and pid - %s' %(personarrived.hid, personarrived.pid)
            #print '\t    --Dest act - ', personarrived.destAct


            #print 'FOR INDEP PERSON BEFORE - ', personarrived.print_activity_list()
            self.adjust_person_schedules_given_arrival_info(personarrived, seed)

            #print 'FOR INDEP PERSON AFTER', personarrived.print_activity_list()

            #print '\t    --Dependentpersonid for trip- ', personarrived.tripDependentPerson
            #print '\t    --Dependentpersonid for next act- ', personarrived.destAct.dependentPersonId


            #self.traverse_through_dependency_chain(personarrived.actualArrival)






            #raw_input('trip dep and subsequent act dep')

            #if personarrived.destAct.dependentPersonId > 0:
                #adjOtherPersonIds = self.parse_personids(personarrived.destAct.dependentPersonId)
                #print '\t     --schedules for more than one person need to be adjusted and these persons are - ', adjOtherPersonIds

                #for depPid in adjOtherPersonIds:
                    #depPerson = self.persons[depPid]
                    #depPerson.add_arrival_status(personarrived.actualArrival,
                    #                    personarrived.expectedArrival)
                    #print 'FOR DEP PERSON BEFORE -', depPerson.print_activity_list()
                    #self.adjust_this_episode_and_subsequent_dependencies(depPerson)
                    #self.adjust_person_schedules_given_arrival_info(depPerson, seed)
                    #print 'FOR DEP PERSON AFTER -', depPerson.print_activity_list()


        #raw_input('Schedules adjusted for household - %s and persons with ids - %s' %(self.hid, self.persons.keys()))


    def traverse_through_dependency_chain(self, arrivaltime):
        return

        while (len(self.affectedActs) > 0):
            personAct, adjustment = self.affectedActs.popitem()
        #for personAct in self.affectedActs.keys():
            if personAct.dependentPersonId > 0:
                print '\tfor personActs:%s and moved by - %s' %(personAct, adjustment)

                adjOtherPersons = self.parse_personids(personAct.dependentPersonId)

                for depPersonId in adjOtherPersons:
                    depPerson = self.persons[depPersonId]
                    print '\t\tfor dependent person - ', depPersonId


                    depPersonConflicts = depPerson._identify_match_activities([personAct])
                    self.add_anchor_activity(depPerson, depPersonConflicts[0], arrivaltime)

                    if len(depPersonConflicts) > 1:
                        for confAct in depPersonConflicts:
                            print '\t\tconflict act - ', confAct
                        raise Exception, 'more than one conflicts really'


                    for confAct in depPersonConflicts:
                        print '\t\t    conflict - %s', confAct

                        # Move start only
                        if adjustment[0] <> -9999:
                            print '\t\t\tStart moved - '
                            print depPerson.move_start(confAct, adjustment[0])
                            print '\t\t\tconflict resolved to- %s', confAct

                        # Move start and end
                        if adjustment[2] <> -9999:
                            print '\t\t\tStart and end are both moved - '
                            print depPerson.move_start_end(confAct, adjustment[2])
                            print '\t\t\tconflict resolved to- %s', confAct

                    if not depPerson._check_for_conflicts():
                        depPerson.print_activity_list()
                        #depPerson.adjust_child_dependencies([confAct])
                        self.resolve_conflict(depPerson, confAct)
                        print 'AFTER CONFLICT IS RESOLVED - '
                        raw_input('conflict occurred for hid - ' %self.hid)
                        raise Exception, 'conflicts introduced for person - %s' %depPerson.pid

    def resolve_conflict(self, person, refAct):
        conflictActs = person._identify_conflict_activities([confAct])

        for act in conflictActs:
            print 'Conflict activity - ', act

            # the conflict act overlaps with the tail end of the reference activity
            if act.startTime <= refAct.endTime and act.endTime > refAct.endTime:

                pass

            if act.dependentPersonId > 0:

                pass





    def adjust_person_schedules_given_arrival_info(self, person, seed=1):
        #print '\tdest act for this person ', person.destAct
        #print '\tactual arrival - %s and expected arrival - %s' %(person.actualArrival, person.expectedArrival)

        #print person.print_activity_list()

        if person.destAct.startTime == person.actualArrival:
            #print '\n-- Arrived as expected; nothing needs to be done --'

            pass

        if person.destAct.startTime > person.actualArrival:
            #print '\n-- Arrived earlier than expected; moving destination activity to earlier --'
            self.push_destination_activity_to_earlier(person)


        if person.destAct.startTime < person.actualArrival:
            #print '\n-- Arrived later than expected; adjustment for activities needs to happen here --'
            self.adjust_push_subsequent_activities(person)

        #print person.print_activity_list()
        #raw_input("after processing")
    def push_destination_activity_to_earlier(self, person):
        #if self.destAct.actType == 100 or self.destAct.actType == 600:

        affectedAct = {}

        #if person.destAct.dependentPersonId > 0:
        if person.destAct.actType == 100 or person.destAct.actType == 600:
            self.add_anchor_activity(person, person.destAct, person.actualArrival)
            #print '\tThe dest act was of type - %s and dependency - %s hence cannot be moved' % (person.destAct.actType,
            #                                                                                    person.destAct.dependentPersonId)
        else:
            #moveByValue = person.actualArrival - person.destAct.startTime
            moveByValue = person.actualArrival - person.destAct.startTime -1
            #self.affectedActs[copy.deepcopy(person.destAct)] = [-9999, -9999, moveByValue]
            person.move_start_end(person.destAct, moveByValue)
            #self.add_anchor_activity(person, person.destAct, person.actualArrival)


    def wait_push_subsequent_activities(self, person):
        #self.affectedActs = {}
        #raw_input('adjusting and pushing subsequent activities')

        #print 'Expected Activities'
        #for act in person.expectedActivities:
        #    print '\t', act

        #print 'Actual Activities'
        #for act in person.actualActivities:
        #    print '\t', act

        #raw_input('actual/expected should all be the same?')

        #print 'before adjustment for occupancy ----', person.print_activity_list()

        person.move_end(person.stAct, person.tripStTime+1)
        actEnd = person.tripStTime + 1

        nextAct = person.expectedActivities[0]
        #print '\tstart act -', person.stAct
        #print '\tnext act - ', nextAct

        if (person.stAct.actType == 600 and person.stAct.dependentPersonId == 99 and
            nextAct.actType == 601 and nextAct.dependentPersonId == 99):
            person.move_start_end(nextAct, 0)
            actEnd = copy.deepcopy(nextAct.endTime)
            index = 1
            #print ('Moving the non-hh member trip anchor in order to keep reasonable trip episodes for these ... ')

        else:
            index = 0

        i = 0
        while i < len(person.expectedActivities[index:]):
            act = person.expectedActivities[index:][i]
            i += 1
            if actEnd-act.startTime > 0:
                moveByValue = copy.deepcopy(actEnd-act.startTime)
                #self.affectedActs[copy.deepcopy(act)] = [-9999, -9999, moveByValue]
                person.move_start_end(act, moveByValue)
                actEnd = copy.deepcopy(act.endTime)

                if act.actType == 600 and act.dependentPersonId == 99:
                    nextAct = person.expectedActivities[index:][i]
                    i += 1
                    person.move_start_end(nextAct, moveByValue)
                    actEnd = copy.deepcopy(nextAct.endTime)

            else:
                break
        """
        for act in person.expectedActivities[index:]:
            if actEnd-act.startTime > 0:
                #print '-->This ', act, ' is being moved by ', actEnd-act.startTime
                moveByValue = copy.deepcopy(actEnd-act.startTime)
                self.affectedActs[copy.deepcopy(act)] = [-9999, -9999, moveByValue]
                person.move_start_end(act, moveByValue)


            actEnd = copy.deepcopy(act.endTime)
        """
        #print 'Moving the end of the starting episode'
        #print 'activity list after ----', person.print_activity_list()
        #raw_input('occupancy processing')

    def adjust_push_subsequent_activities(self, person, refArrivalTime=None):
        #raw_input('adjusting and pushing subsequent activities')

        if refArrivalTime is None:
            actualArrival = person.actualArrival
            #self.add_anchor_activity(person, person.destAct, actualArrival)
        else:
            actualArrival = refArrivalTime

        missedActsStillToPursue = []
        actsToPursue = []
        actsToRemove = []
        movedStartOfAct = False
        pushedActs = False

        # Adjusting if only the first activity is affected
        firstExpActAfterArrival = person.expectedActivities[0]

        if firstExpActAfterArrival.startTime < actualArrival and firstExpActAfterArrival.endTime > actualArrival:
            movedStartOfAct = True
            #person.move_start(firstExpActAfterArrival, actualArrival)
            #self.affectedActs[copy.deepcopy(firstExpActAfterArrival)] = [actualArrival, -9999, -9999]

            if firstExpActAfterArrival.endTime == actualArrival + 1:
                person.move_start(firstExpActAfterArrival, actualArrival)
                #self.affectedActs[copy.deepcopy(firstExpActAfterArrival)] = [actualArrival, -9999, -9999]
                #print ('Only first activity needs to be adjusted; however move start to actual arrival and then move the whole episode to avoid prism extraction errors')
            else:
                person.move_start(firstExpActAfterArrival, actualArrival + 1)
                #print ('Only first activity needs to be adjusted')f
                #self.affectedActs[copy.deepcopy(firstExpActAfterArrival)] = [actualArrival+1, -9999, -9999]
                return

        # Add an anchor only when the first activity is not the only one affected ... because individual's subsequent activity engagement is getting messed up ...
        # because if there is a missed activity without adding an anchor the subsequent activity is starting from nowhere and hence the inconsistency ...
        self.add_anchor_activity(person, person.destAct, actualArrival)
        pushedActs = True

        # Adjusting when more than one activity is affected: Push all activities
        for act in person.expectedActivities:
            #if (act.endTime < actualArrival and act.dependentPersonId > 0 and (act.actType == 600 or act.actType == 601)):
            if (act.endTime < actualArrival and act.dependentPersonId > 0):
                missedActsStillToPursue.append(act)
            elif act.endTime >= actualArrival:
                actsToPursue.append(act)
            else:
                actsToRemove.append(act)


        #print 'Acts to Remove'
        #for act in actsToRemove:
        #    print '\t', act


        if len(actsToRemove) > 0:
            person.remove_episodes(actsToRemove)
            #print 'After removing activities that can be skipped ... '
            #person.print_activity_list()

        #print 'Missed Activities'
        #for act in missedActsStillToPursue:
            #print '\t', act

        #print 'Activities to Pursue'
        #for act in actsToPursue:
            #print '\t', act


        actEnd = actualArrival+1
        actsToBeAdjusted = missedActsStillToPursue + actsToPursue

        if len(actsToBeAdjusted) > 2:
            destAct = actsToBeAdjusted[0]
            nextAct = actsToBeAdjusted[1]

            if (
                destAct.actType == 601 and # act is a dropoff
                ((nextAct.actType >= 450 and nextAct.actType <= 490) or (nextAct.actType == 151)) and # subsequent act is child dependent act
                ((nextAct.startTime < actualArrival) and (nextAct.endTime > actualArrival)) # the dropoff is within duration for subsequent act
                ):
                #print 'before adjusting the dropoff and subs dep act'
                #print 'dest act - ', destAct
                #print 'next act - ', nextAct

                moveByValue = actualArrival - destAct.startTime
                person.move_start_end(destAct, moveByValue)


                if nextAct.endTime > destAct.endTime + 2:
                    person.move_start(nextAct, destAct.endTime + 1)
                else:
                    person.move_end(nextAct, destAct.endTime +2)
                    person.move_start(nextAct, destAct.endTime +1)
                #print 'after adjusting the dropoff and subs dep act'
                #print 'dest act - ', destAct
                #print 'next act - ', nextAct

                actEnd = nextAct.endTime
                index = 2
                #raw_input()
            else:
                index = 0
        else:
            index = 0

        for act in actsToBeAdjusted[index:]:
            #print '-->This ', act, ' is being moved by ', actEnd-act.startTime
            #if actEnd-act.startTime >= 0:
            if actEnd-act.startTime >= 0:
                #print '-->This ', act, ' is being moved by ', actEnd-act.startTime
                moveByValue = copy.deepcopy(actEnd-act.startTime-1)
                #self.affectedActs[copy.deepcopy(act)] = [-9999, -9999, moveByValue]
                person.move_start_end(act, moveByValue)
            else:
                break

            actEnd = copy.deepcopy(act.endTime)

        if pushedActs == False and movedStartOfAct == False:
            self.add_anchor_activity(person, person.destAct, actualArrival)
            #raw_input('actual schedules were not moved ... need to add an anchor ... ')


    def add_anchor_activity(self, person, personAct, arrivaltime):
        anchorAct = copy.deepcopy(personAct)
        anchorAct.actType = 598
        anchorAct.startTime = arrivaltime
        anchorAct.endTime = arrivaltime
        anchorAct.duration = 0
        person.add_episodes([anchorAct])



    def identify_joint_episodes(self):
        if self.dependencyPersonIds == []:
            return self._collate_results()

        print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        print '\tPerson Ids with NO dependencies - ', self.indepPersonIds

        for pid in self.dependencyPersonIds:
            indepPersonActivityList = {}
            person = self.persons[pid]
            print
            self.print_activity_list(person)
            acts = copy.deepcopy(person.listOfActivityEpisodes)
            for i in range(len(acts)):
                stTime, act = hp.heappop(acts)

                if act.dependentPersonId <> 0:
                    indepPersonId = act.dependentPersonId
                    if indepPersonId not in indepPersonActivityList.keys():
                        indepPersonActivityList[indepPersonId] = [act]
                    else:
                        indepPersonActivityList[indepPersonId] += [act]



            for indepPersonId in indepPersonActivityList.keys():
                print '\tIndep Person IDs:', indepPersonId,
                indepPerson = self.persons[indepPersonId]
                print 'length of all acts for person:', indepPerson.actCount
                activityList = indepPersonActivityList[indepPersonId]
                print '\tdependent persons acts - '
                for ac in activityList:
                    print '\t\t Dep->', ac

                indepPersonActs = indepPerson._identify_conflict_activities(activityList)
                print
                check = False
                for act in indepPersonActs:
                    if act.dependentPersonId == 99:
                        act.dependentPersonId = 100 + pid
                    else:
                        act.dependentPersonId = act.dependentPersonId*100. + pid
                        check = True
                        print '\t\t Act Dep', act.dependentPersonId,
                    print '\tIndep->', act



    def lineup_activities_based_on_activities(self, seed):
        print 'Post processing schedules for hid - ', self.hid
        print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        print '\tPerson Ids with NO dependencies - ', self.indepPersonIds

        if len(self.dependencyPersonIds) == 0:
            #print 'DEPENDENCIES DO NOT EXIST; ACTIVITIES NEED NOT BE ALLOCATED TO INDEPENDENT PERSONS'
            return

        depAct = {}
        depIHAct = {}

        for depPid in self.dependencyPersonIds:
            depPerson = self.persons[depPid]
            #depPerson.print_activity_list()
            depPersonTempList = []
            for actC in range(len(depPerson.listOfActivityEpisodes)):
                stTime, act = hp.heappop(depPerson.listOfActivityEpisodes)
                if act.dependentPersonId > 0 and act.dependentPersonId <> 99 and act.actType >= 200:
                    if depPid in depAct:
                        depAct[depPid] += [(act.startTime, act)]
                    else:
                        depAct[depPid] = [(act.startTime, act)]

                if act.dependentPersonId > 0 and act.dependentPersonId <> 99 and act.actType < 200:
                    if depPid in depIHAct:
                        depIHAct[depPid] += [(act.startTime, act)]
                    else:
                        depIHAct[depPid] = [(act.startTime, act)]


                hp.heappush(depPersonTempList, (stTime, act))
            depPerson.listOfActivityEpisodes = depPersonTempList



        depActFromIndep = {}
        depIHActFromIndep = {}

        for pid in self.indepPersonIds:
            person = self.persons[pid]
            #person.print_activity_list()
            indepPersonTempList = []
            for actC in range(len(person.listOfActivityEpisodes)):
                stTime, act = hp.heappop(person.listOfActivityEpisodes)
                if act.dependentPersonId > 0 and act.actType <> 598 and act.actType >= 200:
                    depPersonIds = self.parse_personids(act.dependentPersonId)
                    for depPid in depPersonIds:
                        if depPid in depActFromIndep:
                            depActFromIndep[depPid] += [(act.startTime, act)]
                        else:
                            depActFromIndep[depPid] = [(act.startTime, act)]

                if act.dependentPersonId > 0 and act.actType <> 598 and act.actType < 200:
                    depPersonIds = self.parse_personids(act.dependentPersonId)
                    for depPid in depPersonIds:
                        if depPid in depIHActFromIndep:
                            depIHActFromIndep[depPid] += [(act.startTime, act)]
                        else:
                            depIHActFromIndep[depPid] = [(act.startTime, act)]


                hp.heappush(indepPersonTempList, (stTime, act))
            person.listOfActivityEpisodes = indepPersonTempList


        for pid in depAct.keys():
            depPerson = self.persons[pid]

            if pid not in depAct.keys():
                print depPerson.print_activity_list()
                raise Exception, 'Activities for this person where all allocated to non-hh memebers?'

            depActs = depAct[pid]
            indepActs = depActFromIndep[pid]

            hp.heapify(depActs)
            hp.heapify(indepActs)

            if len(depActs) <> len(indepActs):
                raise Exception, 'Some dependent activities got lost in the dynamic process? i.e. one-to-one matching of dependent activities is not happening'


            print "\nUpdating the dependent person's schedules to reflect the dynamic activity-travel scheduling"
            print 'Before - ', depPerson.print_activity_list()
            for i in range(len(depActs)):
                depenActStTime, depenAct = hp.heappop(depActs)
                indepActStTime, indepAct = hp.heappop(indepActs)

                if depenAct.startTime <> indepAct.startTime and depenAct.endTime <> indepAct.endTime:
                    print '\n\tDep Act             ', depenAct
                    print '\tCorr indep act    ', indepAct
                    print '\t\t Need to adjust the start and/or endtime'

                    if depenAct.actType == 600:
                        depPerson.move_start_end(depenAct, indepAct.startTime-depenAct.startTime-1)

                    if depenAct.actType == 601:
                        depPerson.move_start_end(depenAct, indepAct.startTime-depenAct.startTime-1)

                    if depenAct.actType >= 400 and depenAct.actType <= 450:
                        depPerson.move_start_end_by_diff_values(depenAct, indepAct.startTime, indepAct.endTime)


                    print '\t\t Adjusted Dep Act - ', depenAct



            depIHActs = depIHAct[pid]
            indepIHActs = depIHActFromIndep[pid]

            hp.heapify(depIHActs)
            hp.heapify(indepIHActs)

            if len(depIHActs) <> len(indepIHActs):
                """
                for i in range(len(depIHActs)):
                    depenIHActStTime, depenIHAct = hp.heappop(depIHActs)
                    print 'depn IH - ', depenIHAct

                print
                for i in range(len(indepIHActs)):
                    indepIHActStTime, indepIHAct = hp.heappop(indepIHActs)
                    print 'indepn IH - ', indepIHAct
                """
                raw_input('Number of IH Acts is not the same i.e. count dependent IH episodes <> count dependent IH episodes allocated to independent persons')

            for i in range(len(depIHActs)):
                depenIHActStTime, depenIHAct = hp.heappop(depIHActs)
                try:
                    indepIHActStTime, indepIHAct = hp.heappop(indepIHActs)
                except IndexError, e:
                    print 'Since the indep acts are less; the last act that was popped will be used as reference ... '

                print '\n\tIH Dep Act              ', depenIHAct
                print '\tCorr IH indep act    ', indepIHAct


                if depenIHAct.actType == 101 and indepIHAct.actType == 151:
                    print '\t\t Need to adjust the start and/or endtime of IH Episode'
                    depPerson.move_start_end_by_diff_values(depenIHAct, indepIHAct.startTime, indepIHAct.endTime)

                    print '\t\t Adjusted Dep IH Act - ', depenIHAct
                    raw_input('\t\tadjusting ih allocated as ih dependent')

                if depenIHAct.actType == 101 and indepIHAct.actType == 100:
                    if depenIHAct.startTime < indepIHAct.startTime and indepIHAct.startTime:
                        print '\t\t Need to adjust start/endtime of IH Episode'
                        depPerson.move_start_end(depenIHAct, indepIHAct.startTime-depenIHAct.startTime)

                        print '\t\t Adjusted Dep IH Act - ', depenIHAct
                        raw_input('\t\tadjusting ih allocated to ih sojourn')


            print 'After - ', depPerson.print_activity_list()


            self.fill_gaps_in_dependent_person_schedule(depPerson)
            print depPerson.print_activity_list()

            print 'Conflicts exist: True - No, False - Yes', depPerson._check_for_conflicts()
            raw_input('processing complete for dependent personid - %s' %pid)

    def lineup_activities(self, seed):
        #print 'Post processing schedules for hid - ', self.hid
        #print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        #print '\tPerson Ids with NO dependencies - ', self.indepPersonIds

        if len(self.dependencyPersonIds) == 0:
            return

        depTrips = {}
        depTripsSt = {}
        depTripsEn = {}
        otherOHDepActs = {}
        ihDepActs = {}



        for pid in self.indepPersonIds:
            person = self.persons[pid]
            #person.print_activity_list()
            indepPersonTempList = []


            # Identifying trip vertices from the independent persons schedules
            for i in range(len(person.listOfActivityEpisodes)):
                stTime, act = hp.heappop(person.listOfActivityEpisodes)

                if act.actType == 600:
                    #print 'Trip st for person identified'
                    depPersonIds = self.parse_personids(act.dependentPersonId)
                    for depPid in depPersonIds:
                        if depPid in depTripsSt:
                            depTripsSt[depPid].append(act.endTime)
                        else:
                            depTripsSt[depPid] = [act.endTime]

                if act.actType == 601:
                    #print 'Trip en for person identified'
                    depPersonIds = self.parse_personids(act.dependentPersonId)
                    for depPid in depPersonIds:
                        if depPid in depTripsEn:
                            depTripsEn[depPid].append(act.startTime)
                        else:
                            depTripsEn[depPid] = [act.startTime]

                if act.actType >= 450 and act.actType <= 500:
                    #print 'Other OH joint activity with dependent child identified'
                    depPersonIds = self.parse_personids(act.dependentPersonId)
                    for depPid in depPersonIds:
                        if depPid in otherOHDepActs:
                            otherOHDepActs[depPid].append((act.startTime, act.endTime))
                        else:
                            otherOHDepActs[depPid] = [(act.startTime, act.endTime)]

                if act.actType == 151:
                    depPersonIds = self.parse_personids(act.dependentPersonId)
                    for depPid in depPersonIds:
                        if depPid in ihDepActs:
                            ihDepActs[depPid].append((act.startTime, act.endTime))
                        else:
                            ihDepActs[depPid] = [(act.startTime, act.endTime)]

                hp.heappush(indepPersonTempList, (stTime, act))
            person.listOfActivityEpisodes = indepPersonTempList

        #print ihDepActs



        """
        for depPid in ihDepActs.keys():
            print 'For dependent person the ih acts are - - ', depPid
            depPerson = self.persons[depPid]
            depPerson.print_activity_list()

            depPersonTempList = []

            ihActsVerts = ihDepActs[depPid]
            ihActsVerts.sort()
            ihActCount = 0


            for i in range(len(depPerson.listOfActivityEpisodes)):
                actStTime, act = hp.heappop(depPerson.listOfActivityEpisodes)

                if act.actType == 101 and act.dependentPersonId <> 99:
                    verts = ihActsVerts[ihActCount]
                    depPerson.move_start_end_by_diff_values(act, verts[0], verts[1], removeAdd = False)

                    ihActCount += 1

                hp.heappush(depPersonTempList, (act.startTime, act))


            depPerson.listOfActivityEpisodes = depPersonTempList
            depPerson.print_activity_list()

        raw_input('ih dep act vertices')
        """





        tripVertices = {}
        for depPid in depTripsSt.keys():
            #print 'For dependent person - ', depPid
            depPerson = self.persons[depPid]
            #print depPerson.print_activity_list()

            depPersonTempList = []
            ohActList = []
            actCount = 1
            tripCount = 0
            ohActCount = 0
            #trips = depTrips[depPid]
            #trips.sort()
            tripsSt = depTripsSt[depPid]
            tripsSt.sort()
            tripsEn = depTripsEn[depPid]
            tripsEn.sort()

            try:
                ohActs = otherOHDepActs[depPid]
                ohActs.sort()
            except KeyError, e:
                #print 'No OH Acts to be adjusted for this dependent person - ', depPid
                pass


            firstTripSt = -1
            lastTripEn = -1


            for i in range(len(depPerson.listOfActivityEpisodes)):
                stTime, act = hp.heappop(depPerson.listOfActivityEpisodes)


                if act.actType == 600:
                    if firstTripSt == -1:
                        #print 'start anchor', act.startTime, firstTripSt == -1
                        firstTripSt = copy.deepcopy(act.startTime)


                if act.actType == 601:
                    lastTripEn = copy.deepcopy(act.endTime)

                hp.heappush(depPersonTempList, (act.startTime, act))

            depPerson.listOfActivityEpisodes = copy.deepcopy(depPersonTempList)

            # Identifying first trip start
            #depPerson.print_activity_list()
            #print 'First trip start before adjustment- ', firstTripSt
            #print 'Last trip end before adjustment- ', lastTripEn
            #raw_input()


            #print 'len of acts', len(depPerson.listOfActivityEpisodes)

            # Identifying activities around trips
            actsBeforeFirstTrip = []
            actsBetweenTrips = []
            actsAfterLastTrip = []
            depPersonTempList = []

            for i in range(len(depPerson.listOfActivityEpisodes)):
                stTime, act = hp.heappop(depPerson.listOfActivityEpisodes)

                if act.startTime < firstTripSt and act.actType <600:
                    actsBeforeFirstTrip.append(act)

                elif act.startTime >= lastTripEn and act.actType <600:
                    actsAfterLastTrip.append(act)

                elif  act.actType <600:
                    actsBetweenTrips.append(act)

                hp.heappush(depPersonTempList, (act.startTime, act))

            depPerson.listOfActivityEpisodes = copy.deepcopy(depPersonTempList)

            for act in actsBeforeFirstTrip:
                #print 'before - ', act
                pass

            for act in actsBetweenTrips:
                #print 'between - ', act
                pass

            for act in actsAfterLastTrip:
                #print 'after - ', act
                pass

            #print 'len of acts', len(depPerson.listOfActivityEpisodes)
            #raw_input('finished identifying acts around trip vertices')


            # adjusting the vertices based on arrivals and departure pegs derived from the independent adjults
            depPersonTempList = []
            lastTripEn = 0
            stTime, stAct = hp.heappop(depPerson.listOfActivityEpisodes)
            hp.heappush(depPersonTempList, (stTime, stAct))
            for i in range(len(depPerson.listOfActivityEpisodes)):
                enTime, enAct = hp.heappop(depPerson.listOfActivityEpisodes)


                if ((stAct.actType >= 200 and stAct.actType < 598)
                    or stAct.actType == 599
                    or (stAct.actType == 101 and actCount <> 2)) : # Avoid including the the first ih episode right after waking up ...
                    ohActList.append((stAct.startTime, stAct))

                if stAct.actType == 600 and enAct.actType == 601 and stAct.dependentPersonId <> 99:
                    #st, en = trips[tripCount]
                    st = tripsSt[tripCount]
                    en = tripsEn[tripCount]
                    #print '\tTrip %s: st - %s and end - %s' %(tripCount+1, st, en)
                    #print '\t    St Vertex - ', stAct
                    if st == lastTripEn + 1:
                        st = st + 1 # just change the reference start time ...
                        if en < st: # if the trip is very short then move the reference end of the trip too
                            en = st + 1
                        #raw_input('the waiting and discretizing error case')


                    if st == lastTripEn:
                        st = st + 2
                        if en < st: # if the trip is very short then move the reference end of the trip too
                            en = st + 1
                        #raw_input('the waiting and discretizing error case')

                    if stAct.endTime <> st:
                        depPerson.move_start_end(stAct, st-stAct.endTime-1, removeAdd=False)
                        #print '\t\tMod St Vertex', stAct

                    #print '\t    En Vertex - ', enAct
                    if enAct.startTime <> en + 1:
                        depPerson.move_start_end(enAct, en-enAct.startTime-1, removeAdd=False)
                        #print '\t\tMod En Vertex', enAct
                    tripCount += 1
                    lastTripEn = en


                #if stAct.actType == 600 and enAct.actType == 601 and stAct.dependentPersonId == 99 and enAct.dependentPersonId == 99:
                # All waiting associated for trips with non household members why do you have to move pickup and dropoff simultaneously?
                if stAct.actType == 600 and stAct.dependentPersonId == 99:
                    #print '\tTrip with nonhh member:'

                    st = stAct.endTime
                    en = enAct.startTime
                    #print '\t    St Vertex for non hh- ', stAct
                    #print 'last trip end - ', lastTripEn

                    if st <= lastTripEn:
                        #st = lastTripEn + 1
                        st = lastTripEn

                    """

                    if st == lastTripEn + 1:
                        st = st + 1 # just change the reference start time ...
                        if en < st: # if the trip is very short then move the reference end of the trip too
                            en = st + 1
                        #raw_input('the waiting and discretizing error case for trips with nonhh members')


                    if st == lastTripEn:
                        st = st + 2
                        if en < st: # if the trip is very short then move the reference end of the trip too
                            en = st + 1
                        #raw_input('the waiting and discretizing error case for trips with nonhh members')
                    """
                    #print 'pickup non hh end', stAct.endTime, ' proposed end -', st

                    #if stAct.endTime <> st:
                    depPerson.move_end(stAct, st+1, removeAdd=False)
                    depPerson.move_start(stAct, st, removeAdd=False)
                    #print '\t\tMod St Vertex', stAct


                if enAct.actType == 601 and enAct.dependentPersonId == 99:
                    #print '\t    En Vertex for non hh- ', enAct
                    #if enAct.startTime <> en + 1:
                    #    depPerson.move_start_end(enAct, en-enAct.startTime-1, removeAdd=False)
                    #   print '\t\tMod En Vertex', enAct

                    lastTripEn = en



                if enAct.actType >= 400 and enAct.actType <= 450 and enAct.dependentPersonId <> 99:
                    #print enAct
                    #print 'ohAct', ohActCount
                    ohActSt, ohActEn = ohActs[ohActCount]
                    #print '\tOH Act St - %s and OH Act En - %s' %(ohActSt, ohActEn)
                    #print '\t     OH ACt', enAct

                    if enAct.endTime <> ohActEn or enAct.startTime <> ohActSt:
                        depPerson.move_start_end_by_diff_values(enAct, ohActSt, ohActEn, removeAdd=False)
                    ohActCount += 1
                    #print '\t     Modified OH ACt', enAct
                    #raw_input('OH ACt adjustment as well ... ')

                actCount += 1
                stAct = enAct

                hp.heappush(depPersonTempList, (enAct.startTime, enAct))

            depPerson.listOfActivityEpisodes = copy.deepcopy(depPersonTempList)
            depPerson.reset_activity_heap()
            #print 'After adjusting pickups and dropoffs and OH Acts'
            #print depPerson.print_activity_list()
            #raw_input()




            # Identifying the trip vertices after adjustment
            depPersonTempList = []
            depPersonTripAnchorsList = []

            firstTripSt = -1
            lastTripEn = -1


            for i in range(len(depPerson.listOfActivityEpisodes)):
                stTime, act = hp.heappop(depPerson.listOfActivityEpisodes)


                if act.actType == 600:
                    if firstTripSt == -1:
                        #print 'start anchor', act.startTime, firstTripSt == -1
                        firstTripSt = copy.deepcopy(act.startTime)
                    hp.heappush(depPersonTripAnchorsList, (act.startTime, act))

                if act.actType == 601:
                    lastTripEn = copy.deepcopy(act.endTime)
                    hp.heappush(depPersonTripAnchorsList, (act.startTime, act))
                hp.heappush(depPersonTempList, (act.startTime, act))

            depPerson.listOfActivityEpisodes = copy.deepcopy(depPersonTempList)

            # Identifying first trip start
            #depPerson.print_activity_list()
            #print 'First trip start - ', firstTripSt
            #print 'Last trip end - ', lastTripEn
            #raw_input()


            #actsBeforeFirstTrip = []
            #actsBetweenTrips = []
            #actsAfterLastTrip = []


            # Adjusting the last activity before pickup
            #print actsBeforeFirstTrip
            lastActBeforeFirstPickup = actsBeforeFirstTrip[-1]
            if lastActBeforeFirstPickup.endTime < firstTripSt - 1:
                depPerson.move_end(lastActBeforeFirstPickup, firstTripSt - 1, removeAdd = False)

            #print actsBeforeFirstTrip
            #raw_input('adjusted first activity before pickup')

            # Adjusting activities between trips
            #print 'number of in between acts - ', len(actsBetweenTrips)
            #print 'number of verts - ', len(depPersonTripAnchorsList)

            depPersonActs = copy.deepcopy(depPersonTripAnchorsList)

            hp.heappop(depPersonTripAnchorsList)
            for i in range(len(depPersonTripAnchorsList)/2):
                actVertStTime, actVertSt = hp.heappop(depPersonTripAnchorsList)
                actVertEnTime, actVertEn = hp.heappop(depPersonTripAnchorsList)

                #print 'activity vertex st', actVertSt
                #print 'activity vertex en', actVertEn
                #print '\t act', actsBetweenTrips[i]
                actBet = actsBetweenTrips[i]

                if (actVertEn.startTime - actVertSt.endTime) <= 1:
                    #print '\tThis activity was not pursued ... the person visited the destination and moved on ... '
                    pass

                else:
                    depPerson.move_start_end_by_diff_values(actBet, actVertSt.endTime, actVertEn.startTime, removeAdd=False)
                    #print '\t act after - ', actsBetweenTrips[i]
                    hp.heappush(depPersonActs, (actBet.startTime, actBet))

            for act in actsBetweenTrips:
                #print 'between - ', act
                pass


            #raw_input('adjusted in betweek trips')

            # Adjusting activities after last trip


            for act in actsAfterLastTrip:
                #print 'after last trip - ', act
                if act.startTime < lastTripEn:
                    moveByValue = lastTripEn - act.startTime
                    depPerson.move_start_end(act, moveByValue, removeAdd=False)
                    #print '\tafter last trip modified- ', act
                    lastTripEn = act.endTime

                if act.startTime >= lastTripEn:
                    #print act
                    #print 'moving first act after last trip ... '
                    depPerson.move_start(act, lastTripEn + 1, removeAdd=False)
                    #print act
                    break

            #raw_input ('after adjusting acts after last trip')


            #depPerson.print_activity_list()

            for act in actsBeforeFirstTrip:
                hp.heappush(depPersonActs, (act.startTime, act))

            for act in actsAfterLastTrip:
                hp.heappush(depPersonActs, (act.startTime, act))

            depPerson.listOfActivityEpisodes = depPersonActs

            #depPerson.print_activity_list()
            #raw_input('FINALFINAL')



            if not depPerson._check_for_conflicts():
                depPerson.print_activity_list()
                #raise Exception, 'Conflicts exist still ... and this should not happen'
                #raw_input('conflicts exist still for person')

            depPerson._check_for_acts_between_trip_vertices()

    def extract_tripattributes(self, seed):
        for pid in self.indepPersonIds:
            person = self.persons[pid]
            person.print_activity_list()

            self.extract_tours(person)


    def extract_tours(self, person):
        hbAnchors = []
        wbAnchors = []


        print 'Number of acts before - ', len(person.listOfActivityEpisodes)
        tempList = []

        hbtStopsList = []
        hbtOccuList = []
        tTypeList = []
        start = False
        tType = 0
        maxDurAct = 0

        stStartTime, stAct = hp.heappop(person.listOfActivityEpisodes)
        tempList.append((stAct.startTime, stAct))
        for i in range(len(person.listOfActivityEpisodes)):
            enStartTime, enAct = hp.heappop(person.listOfActivityEpisodes)
            tempList.append((enAct.startTime, enAct))

            if enAct.actType == 598:
                continue

            # Firt home Anchor
            if ((stAct.actType >= 100 and stAct.actType <= 199) and
                 (stAct.startTime == 0) and
                 (enAct.actType == 600) and
                 (stAct.location == enAct.location)):
                print 'St Anchor', stAct
                hbAnchors.append(stAct)
                stops = -1
                occuList = []
                tType = 0
                maxDurAct = 0
                start = True
            # Start Anchor
            elif ((stAct.actType >= 100 and stAct.actType <= 199) and
                (enAct.location == -99 and stAct.location <> -99)):
                print 'St Anchor', stAct
                hbAnchors.append(stAct)
                stops = -1
                occuList = []
                start = True

            if enAct.location == -99:
                stops += 1
                parsedIds = self.parse_personids(enAct.dependentPersonId)
                occuList.append(len(parsedIds) + 1)
                #print 'act - ', enAct, 'stopCount-', stops, 'occuList-', occuList, 'Mean occupancy - ', (array(occuList).sum())/float(array(occuList).size)

            if enAct.location <> -99 and enAct.actType >= 200:
                print '    Acts on tour - ', enAct.actType, enAct.duration
                if enAct.duration > maxDurAct:
                    tType = copy.deepcopy(enAct.actType)
                    maxDurAct = copy.deepcopy(enAct.duration)
                elif enAct.duration == 0:
                    tType = copy.deepcopy(stAct.actType)
                    maxDurAct = copy.deepcopy(stAct.duration)


            if ((enAct.actType >= 100 and enAct.actType <= 199) and enAct.location <> -99 and start):
                print 'En Anchor', enAct
                hbAnchors.append(enAct)
                hbtStopsList.append(stops)
                hbtOccuList.append((array(occuList).sum())/float(array(occuList).size))
                tTypeList.append(tType)
                start = False
                tType = 0
                maxDurAct = 0

            stAct = enAct

        print 'Number of hb tours - %d' %(len(hbAnchors) / 2)
        print '    Number of stops for each of the tours - ', hbtStopsList
        print '    Occupancy for each of the tours - ', hbtOccuList
        print '    Tour type of the tours -', tTypeList

        if len(hbAnchors) % 2 == 1:
            raw_input('Odd number of anchors for HB tours')

        hp.heapify(tempList)
        person.listOfActivityEpisodes = tempList

        tempList = []
        wrkstart = False
        stStartTime, stAct = hp.heappop(person.listOfActivityEpisodes)
        tempList.append((stAct.startTime, stAct))
        for i in range(len(person.listOfActivityEpisodes)):
            enStartTime, enAct = hp.heappop(person.listOfActivityEpisodes)
            tempList.append((enAct.startTime, enAct))

            if enAct.actType == 598:
                continue

            # Firt home Anchor
            if ((stAct.actType >= 200 and stAct.actType <= 299) and
                (enAct.location == -99 and stAct.location <> -99)):
                print 'St Work Anchor', stAct
                wbAnchors.append(stAct)
                stops = -1
                occuList = []
                wrkstart = True

            if enAct.location == -99:
                stops += 1

            if ((enAct.actType >= 200 and enAct.actType <= 299) and enAct.location <> -99 and wrkstart):
                print 'En Work Anchor', enAct
                wbAnchors.append(enAct)
                wrkstart = False

        print '\nNumber of wb tours - %d' %(len(wbAnchors) / 2)
        if len(wbAnchors) >= 1:
            raw_input('Wb tours - ')

        #if len(wbAnchors) % 2 == 1:
        #    raw_input('Odd number of anchors for WB tours')



    def extract_hbtours(self, person):
        hbTours = []

        stops = -1
        occupancy = 0
        startTime = person.firstEpisode.endTime
        stTime, act = hp.heappop(person.listOfActivityEpisodes)
        for i in range(len(person.listOfActivityEpisodes)):
            stTime, act = hp.heappop(person.listOfActivityEpisodes)


            if act.location == -99:
                stops = stops + 1
                print 'TRIP -', act
            else:
                print 'ACTVITY - ', act
            if (act.actType == 100 or act.actType == 101) and (act.location <> -99):
                raw_input ('HB Tour Identified, stops - %s'%stops)
                stops = -1
                occupancy = 0



    def fix_trippurpose(self, seed):
        #print 'Post processing schedules for hid - ', self.hid
        #print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        #print '\tPerson Ids with NO dependencies - ', self.indepPersonIds

        if len(self.dependencyPersonIds)  == 0:
            self.fix_trippurpose_nodependents()
        else:
            self.fix_trippurpose_withdependents()


    def fix_trippurpose_nodependents(self):
        return
        for pid in self.indepPersonIds:
            person = self.persons[pid]
            #print 'Before fixing trip purpose - '
            #person.print_activity_list()

            tempList = []
            stActTime, stAct = hp.heappop(person.listOfActivityEpisodes)
            for i in range(len(person.listOfActivityEpisodes)):
                enActTime, enAct = hp.heappop(person.listOfActivityEpisodes)
                if stAct.actType == -99:
                    stAct.actType = copy.deepcopy(enAct.actType)
                tempList.append((stAct.startTime, stAct))
                stAct = enAct
            tempList.append((enAct.startTime, enAct))
            hp.heapify(tempList)
            person.listOfActivityEpisodes = tempList
            #print 'After fixing trip purpose - '
            #person.print_activity_list()

    def fix_trippurpose_withdependents(self):
        for pid in self.persons.keys():
            person = self.persons[pid]
            #print 'Before fixing trip purpose with dependents - '
            #person.print_activity_list()

            tempAnchorsList = []
            tempList = []
            for i in range(len(person.listOfActivityEpisodes)):
                actTime, act = hp.heappop(person.listOfActivityEpisodes)
                if act.actType == 598:
                    tempAnchorsList.append(act)
                else:
                    if act.actType == 600 and act.location <> -99:
                        person.move_start_end(act, -2, removeAdd=False)
                    tempList.append((act.startTime, act))


            hp.heapify(tempList)
            person.listOfActivityEpisodes = tempList

            # Change unnecessary anchors

            tempList = []
            stActTime, stAct = hp.heappop(person.listOfActivityEpisodes)
            tempList.append((stAct.startTime, stAct))
            for i in range(len(person.listOfActivityEpisodes)):
                enActTime, enAct = hp.heappop(person.listOfActivityEpisodes)
                if stAct.location <> -99 and (enAct.actType == 600 and enAct.location <> -99):
                    enAct.actType = 650
                    #print '\tPickup altered - ', enAct

                if (stAct.actType == 601 and
                    ((enAct.actType >= 450 and enAct.actType <= 500) or
                     (enAct.actType == 151 or enAct.actType == 100) or
                     (stAct.location == enAct.location and enAct.actType == 101) or
                     (person.child_dependency == 1 and enAct.actType >= 400 and enAct.actType <= 450) or
                     (person.child_dependency == 1 and enAct.actType <= 101 )
                    )
                   ):
                    stAct.actType = 651
                    #print '\tDropoff altered - ', enAct

                tempList.append((enAct.startTime, enAct))
                stAct = enAct

            hp.heapify(tempList)
            person.listOfActivityEpisodes = tempList

            #print 'Intermediate with dependents- '
            #person.print_activity_list()


            tempList = []
            stActTime, stAct = hp.heappop(person.listOfActivityEpisodes)
            tempList.append((stAct.startTime, stAct))
            for i in range(len(person.listOfActivityEpisodes)):
                enActTime, enAct = hp.heappop(person.listOfActivityEpisodes)

                if enAct.actType >= 650:
                    #print '\tAltered pickup/dropoff removed - ', enAct
                    continue
                if stAct.location == -99:
                    stAct.actType = copy.deepcopy(enAct.actType)

                tempList.append((enAct.startTime, enAct))
                stAct = enAct

            hp.heapify(tempList)
            person.listOfActivityEpisodes = tempList

            person.add_episodes(tempAnchorsList)

            #print 'After fixing trip purpose with dependents- '
            #person.print_activity_list()
            #raw_input()



    def fill_gaps_in_dependent_person_schedule(self, person):
        return
        stActTime, stAct = hp.heappop(person.listOfActivityEpisodes)
        tempList = []

        for i in range(len(person.listOfActivityEpisodes)):
            enActTime, enAct = hp.heappop(person.listOfActivityEpisodes)

            if stAct.actType == 600 and enAct.actType == 601:
                print 'pickups/dropoffs doing nothing'
                tempList.append((stAct.startTime, stAct))
                stAct = enAct
                continue

            if enAct.startTime > stAct.endTime and enAct.actType <> 600:
                print 'adjusting start for end act except for pickups- ', enAct
                person.move_start(enAct, stAct.endTime, removeAdd=False)
                tempList.append((stAct.startTime, stAct))
                stAct = enAct
                continue

            if stAct.endTime < enAct.startTime and stAct.actType <> 601:
                print 'adjusting end for start act except for dropoffs- ', stAct
                person.move_end(stAct, enAct.startTime, removeAdd=False)
                tempList.append((stAct.startTime, stAct))
                stAct = enAct
                continue


            if enAct.startTime < stAct.endTime and enAct.actType == 100:
                print 'ending sojourn'
                person.move_start_end(enAct, stAct.endTime - enAct.startTime, removeAdd=False)
                tempList.append((stAct.startTime, stAct))
                stAct = enAct
                continue

            if stAct.startTime < enAct.endTime and stAct.actType == 100 and stAct.startTime <> 0:
                print 'ending sojourn'
                person.move_start_end(stAct, enAct.endTime - stAct.startTime, removeAdd=False)
                tempList.append((stAct.startTime, stAct))
                stAct = enAct
                continue


            tempList.append((stAct.startTime, stAct))
            stAct = enAct



        tempList.append((enAct.startTime, enAct))
        hp.heapify(tempList)

        person.listOfActivityEpisodes = tempList


    def lineup_ih_pickups_for_dependents(self):
        # This lines up in home pickup episodes for dependent children

        #print '\tPerson Ids with dependencies - ', self.dependencyPersonIds

        if len(self.dependencyPersonIds) == 0:
            return

        for pid in self.indepPersonIds:
            print '\t\tFor independent person - ', pid, 'and home loc is - ',
            person = self.persons[pid]
            acts = copy.deepcopy(person.listOfActivityEpisodes)

            subsequentPickups = False

            stActStTime, stAct = hp.heappop(acts)
            print stAct.location
            homeLoc = stAct.location

            for i in range(len(acts)):
                nextActStTime, nextAct = hp.heappop(acts)

                if (stAct.actType == nextAct.actType and stAct.actType == 600 and
                        stAct.location == nextAct.location and stAct.location == homeLoc):
                    print '\t\tSubsequent pickup acts at home and we need to line them up and make appropriate adjustments to the dependent persons schedule'
                    print '\t\tfirst Pickup   -', stAct
                    print '\t\tsecond Pickup  -', nextAct

                    stAct = person._identify_match_activity(stAct)[0] #Getting the actual start activity and not the copy for indep person
                    nextAct = person._identify_match_activity(nextAct)[0] # Getting actual next activity and not the copy for indep person



                    nextTwoActs = person._identify_next_activity(nextAct, count=2)
                    print '\t\tfirst dropoff -', nextTwoActs[0]
                    print '\t\tsecond dropoff -', nextTwoActs[1]

                    self.print_activity_list(person)

                    print '\n\t\tThe next two activities and their neighbors are - '
                    for act in nextTwoActs:
                        if stAct.dependentPersonId == act.dependentPersonId:
                            stActCombo = act
                        if nextAct.dependentPersonId == act.dependentPersonId:
                            nextActCombo = act

                    prevToStAct = person._identify_previous_activity(stAct)[0]
                    print '\t\tPrevAct', prevToStAct
                    print '\t\tPickup', stAct
                    stActDepPers = self.parse_personids(stAct.dependentPersonId)
                    print '\t\tDropof', stActCombo



                    print '\n\t\tPickup', nextAct
                    nextActDepPers = self.parse_personids(nextAct.dependentPersonId)
                    print '\t\tDropof', nextActCombo
                    nextToNextAct = person._identify_next_activity(nextActCombo)[0]
                    print '\t\tNextAct', nextToNextAct


                    print '\n\tWe will move the subsequent pickup activities and their go alongs to earlier'
                    print '\t\tCombined pickup time - ', stAct.startTime
                    moveBy = nextAct.startTime - stAct.startTime + 1
                    print '\t\tTherefore move the other person(s) everything by - ',

                    print '\n\tMoving for the indep person - '

                    for depPersId in nextActDepPers:
                        stAct.dependentPersonId = stAct.dependentPersonId*100. + depPersId # The pickup dependentperson id updated to include everyone

                    nextActCopy = copy.deepcopy(nextAct)
                    nextActComboCopy = copy.deepcopy(nextActCombo)
                    person.move_start_end(nextActCombo, -moveBy)
                    if not person._check_for_conflicts():
                        moveConflictCreated = True
                        person.move_start_end(nextActCombo, 1)
                    else:
                        moveConflictCreated = False

                    person.remove_episodes([nextAct])


                    for depPersId in stActDepPers:
                        print '\n\tFor dependent person - ', depPersId
                        depPers = self.persons[depPersId]
                        prevToPickupSt = depPers._identify_previous_activity(stAct)[0]
                        pickUpDropOffActsSt = depPers._identify_match_activities([stAct, stActCombo]) #Getting the actual activities and not the copy for dep person
                        nextToDropOffSt = depPers._identify_next_activity(stActCombo)[0]
                        print '\t\tPrevious to pickup- ', prevToPickupSt
                        print '\t\tPickup            -', pickUpDropOffActsSt[0]
                        print '\t\tDropoff           -', pickUpDropOffActsSt[1]
                        print '\t\tNext to dropoff   -', nextToDropOffSt



                    for depPersId in nextActDepPers:
                        print '\n\tFor dependent person - ', depPersId
                        depPers = self.persons[depPersId]
                        prevToPickup = depPers._identify_previous_activity(nextActCopy)[0]
                        pickUpDropOffActs = depPers._identify_match_activities([nextActCopy, nextActComboCopy]) #Getting the actual activities and not the copy for dep person
                        nextToDropOff = depPers._identify_next_activity(nextActComboCopy)[0]
                        print '\t\tPrevious to pickup- ', prevToPickup
                        print '\t\tPickup            -', pickUpDropOffActs[0]
                        print '\t\tDropoff           -', pickUpDropOffActs[1]
                        print '\t\tNext to dropoff   -', nextToDropOff

                        depPers.move_end(prevToPickup, prevToPickup.endTime-moveBy + 1)
                        prevToPickup.dependentPersonId = prevToPickupSt.dependentPersonId # since we moved we can allocate this persons
                                                                                          # act before pickup to the same adult as the one we used as reference to move i.e. st
                        prevDepAdult = self.persons[prevToPickupSt.dependentPersonId]
                        self.print_activity_list(prevDepAdult)
                        prevDepAdultPrevToPickup = prevDepAdult._identify_match_activities([prevToPickupSt])[0]
                        prevDepAdultPrevToPickup.dependentPersonId = prevDepAdultPrevToPickup.dependentPersonId*100. + depPersId # also update the corresponding act dependency for indep adult


                        depPers.move_start_end(pickUpDropOffActs[0], -moveBy)
                        if moveConflictCreated:
                            depPers.move_start_end(pickUpDropOffActs[1], -moveBy+ 1)
                        else:
                            depPers.move_start_end(pickUpDropOffActs[1], -moveBy)

                        nextToDropOffForIndep = person._identify_match_activities([nextToDropOff])
                        print nextToDropOffForIndep
                        if nextToDropOffForIndep <> []:
                            nextToDropOffForIndep = nextToDropOffForIndep[0]

                        if moveConflictCreated:
                            depPers.move_start(nextToDropOff, nextToDropOff.startTime-moveBy+1 + 1)
                            if nextToDropOffForIndep <> []:
                                depPers.move_start(nextToDropOffForIndep, nextToDropOff.startTime-moveBy+1 + 1)
                        else:
                            depPers.move_start(nextToDropOff, nextToDropOff.startTime-moveBy+1)
                            if nextToDropOffForIndep <> []:
                                depPers.move_start(nextToDropOffForIndep, nextToDropOff.startTime-moveBy+1)

                        print '\t\tAftAdj: Previous to pickup- ', prevToPickup
                        print '\t\tAftAdj: Pickup            -', pickUpDropOffActs[0]
                        print '\t\tAftAdj: Dropoff           -', pickUpDropOffActs[1]
                        print '\t\tAftAdj: Next to dropoff   -', nextToDropOff


                        #MOVE START OR END - goes to a reference value also we need to do a + 1 adjustment for move
                        #MOVEBY START AND END - moves start and end of activity by that amount
                    break

                # for each person in the dependent person list now move/adjust the pickup, dropoff and the nexst activity




                stAct = nextAct

                #indepPersonActs = indepPerson._identify_conflict_activities(activityList)

    def parse_personids(self, tripDep):
        cpTripDep = copy.deepcopy(tripDep)
        modGrt100 = True
        pers = []
        while(modGrt100):
            cpTripDep, pid = divmod(cpTripDep, 100)
            #print cpTripDep, pid
            if pid <> 0 and cpTripDep>0:
                pers.append(int(pid))
            if cpTripDep > 100:
                modGrt100 = True
            else:
                modGrt100 = False
        #print tripDep, pers
        if len(pers) > 1:
            #print '\t\tExciting picking up more than one persoallocate_dependent_activitiesn ... '
            pass
        return pers


    def identify_joint_episodes1(self):
        print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        print '\tPerson Ids with NO dependencies - ', self.indepPersonIds


        self.initialize_dependencyStatusObject()
        self.locked_adults()

        for pid in self.dependencyPersonIds:
            person = self.persons[pid]
            self.print_activity_list(person, dependent=True)
        self.print_joint_acts()

    def initialize_dependencyStatusObject(self):
        self.depenLocks = {}
        maxPid = max(self.persons.keys())
        for pid in self.persons.keys():
            statusObject = zeros((maxPid+1, 1440), dtype=int)
            self.depenLocks[pid] = statusObject

    def locked_adults(self):
        locekdAdults = {}
        for pid in self.dependencyPersonIds:
            person = self.persons[pid]
            self.locked_adults_for_person(person)


    def locked_adults_for_person(self, person):
        acts = copy.deepcopy(person.listOfActivityEpisodes)
        depPers = person.pid
        for i in range(len(acts)):
            stTime, act = hp.heappop(acts)

            if act.dependentPersonId <> 0:
                stTime = act.startTime
                endTime = act.endTime
                indepPers = act.dependentPersonId
                self.depenLocks[depPers][indepPers][stTime:endTime] = 1 #dependent person tree
                self.depenLocks[indepPers][depPers][stTime:endTime] = 1

    def print_joint_acts(self):
        for pid in self.indepPersonIds:
            print '\nFor person - ', pid
            print '\t\tshape', self.depenLocks[pid].sum(0).shape
            print '\t\taccompaniment', self.depenLocks[pid].sum(0)


    def lineup_allocate_start_of_day_episodes_for_dependents(self):
        print '\tPerson Ids with dependencies - ', self.dependencyPersonIds

        minStart = 1440
        maxStart = -1
        startTimeList = []
        for pid in self.dependencyPersonIds:
            depPerson = self.persons[pid]

            print depPerson.firstEpisode
            startTimeList.append(depPerson.firstEpisode.endTime)
            if depPerson.firstEpisode.endTime < minStart:
                minStart = depPerson.firstEpisode.endTime
            if depPerson.firstEpisode.endTime > maxStart:
                maxStart = depPerson.firstEpisode.endTime

            actsOfDepPerson = copy.deepcopy(depPerson.listOfActivityEpisodes)

            print 'for person - ', pid
            stActStartTime, stAct = hp.heappop(actsOfDepPerson)
            endActStartTime, endAct = hp.heappop(actsOfDepPerson)
            print '\tStart - ', stAct
            print '\tEnd - ', endAct

            self.create_dummy_activity(pid, stAct, endAct)

        startTimeList.sort()
        print 'School Min Start - %s and Max Start - %s and sorted start - %s' %(minStart, maxStart, startTimeList)


    def lineup_subsequent_ih_dropoffs(self):





        print 'School Min Start - %s and Max Start - %s and sorted start - %s' %(minStart, maxStart, startTimeList)



    def allocate_terminal_dependent_activities(self, seed):
        self.unallocatedActs = {}
        self.lenUnallocatedActs = 0
        self.seed = seed
        self.rndGen = RandomDistribution(int(self.hid))

        #print 'Household ID - ', self.hid
        #print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        #print '\tPerson Ids with fixed activities - ', self.dailyFixedActPersonIds
        #print '\tPerson Ids with no fixed activities - ', self.noDailyFixedActPersonIds

        if len(self.dependencyPersonIds) == 0:
            #print 'DEPENDENCIES DO NOT EXIST; ACTIVITIES NEED NOT BE ALLOCATED TO INDEPENDENT PERSONS'
            return
        else:
        # For each person identify an adult that has open
        # periods and then allocate to him
            for pid in self.dependencyPersonIds:
                person = self.persons[pid]

                actsOfDepPerson = copy.deepcopy(person.listOfActivityEpisodes)

                #print 'ALLOCATING ACTIVITIES FOR HID - %s, PERSON ID - %s' %(self.hid, pid)
                #self.print_activity_list(person)
                stActStartTime, stAct = hp.heappop(actsOfDepPerson)
                #hp.heappop(person.listOfActivityEpisodes)


                #print '\n\t\t1.1. End of Day/Start of Day: Someone needs to be there'
                #print '\t\t', stAct
                self.adjust_terminal_activity_episodes(pid, stAct, start=True)

                #raw_input()

                #print '\n\t\t1.2. End of Day/Start of Day: Someone needs to be there'
                endAct = person.lastEpisode
                #print '\t\t', endAct
                self.adjust_terminal_activity_episodes(pid, endAct, start=False)


        for pid in self.persons.keys():
            person = self.persons[pid]
            if not person._check_for_conflicts():
                self.print_activity_list(person)
                raise Exception, 'The person still has conflicts - %s, %s' %(self.hid, pid)




    def allocate_dependent_activities(self, seed):
        self.unallocatedActs = {}
        self.lenUnallocatedActs = 0
        self.seed = seed
        self.rndGen = RandomDistribution(int(self.hid))

        #print 'Household ID - ', self.hid
        #print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        #print '\tPerson Ids with fixed activities - ', self.dailyFixedActPersonIds
        #print '\tPerson Ids with no fixed activities - ', self.noDailyFixedActPersonIds

        if len(self.dependencyPersonIds) == 0:
            #print 'DEPENDENCIES DO NOT EXIST; ACTIVITIES NEED NOT BE ALLOCATED TO INDEPENDENT PERSONS'
            return
        else:

        # For each person identify an adult that has open
        # periods and then allocate to him
            for pid in self.dependencyPersonIds:
                person = self.persons[pid]

                actsOfDepPerson = copy.deepcopy(person.listOfActivityEpisodes)
                self.tripCount = 0

                #print 'ALLOCATING ACTIVITIES FOR HID - %s, PERSON ID - %s' %(self.hid, pid)
                #self.print_activity_list(person)
                stActStartTime, stAct = hp.heappop(actsOfDepPerson)
                #hp.heappop(person.listOfActivityEpisodes)


                #print '\n\t\t1.1. End of Day/Start of Day: Someone needs to be there'
                #print '\t\t', stAct
                #self.adjust_terminal_activity_episodes(pid, stAct, start=True)

                #raw_input()

                #print '\n\t\t1.2. End of Day/Start of Day: Someone needs to be there'
                #endAct = person.lastEpisode
                #print '\t\t', endAct
                #self.adjust_terminal_activity_episodes(pid, endAct, start=False)



                actsInTour = []
                inHomeActs = []
                while (len(actsOfDepPerson) > 0):
                    endActStartTime, endAct = hp.heappop(actsOfDepPerson)
                    #hp.heappop(person.listOfActivityEpisodes)
                    #print 'NEW END ACTIVITY _ ', endAct




                    #if (endAct.location <> stAct.location) and (endAct.actType >= 400 and endAct.actType < 500):
                    if (endAct.actType >= 400 and endAct.actType < 500):
                        #print '\n\t\t2.2. OH Act: Activity-travel chain with maintenance activities'
                        #print '\t\t\t START-', stAct
                        #print '\t\t\t END-  ', endAct
                        actsInTour.append(stAct)
                    elif len(actsInTour) > 0:
                        actsInTour.append(stAct)
                        actsInTour.append(endAct)

                        #self.allocate_pickup_dropoff_endact(pid, stAct, endAct)
                        #print "TRIP CHAIN IDENTIFIED"
                        #for act in actsInTour:
                        #    print act
                        #raw_input()
                        self.allocate_trip_activity_chain(pid, actsInTour)
                        #self.print_activity_list(person)
                        if endAct.actType < 200 and endAct.actType > 100:
                            self.allocate_ih_activity(pid, endAct)
                        #raw_input()
                        actsInTour=[]
                        stAct = endAct
                        continue


                    # Building the tour activities
                    if len(actsInTour) > 0:
                        stAct = endAct
                        continue

                    # first check to see when same location and if end is maintenance if so then allocate the end act
                    if (stAct.location == endAct.location) and (endAct.actType >= 400 and endAct.actType <= 500):
                        self.allocate_pickup_dropoff_endact(pid, stAct, endAct)
                        stAct = endAct
                        #raw_input('assigned pickup dropoff for acts with same loc but discretionary/other activity engagement')
                        continue

                    # if above is not true then no need to allocate the end activity ... when both acts are oh episodes
                    if (stAct.location == endAct.location) and (stAct.actType >=200 and endAct.actType >=200):
                        self.allocate_pickup_dropoff(pid, stAct, endAct)
                        stAct = endAct
                        #raw_input('assigned pickup dropoff for acts with same loc but discretionary/other activity engagement')
                        continue

                    # if above is not true then no need to allocate the end activity ... when first act is ih and second act is oh
                    if (stAct.location == endAct.location) and (stAct.actType < 200 and endAct.actType >=200):
                        self.allocate_pickup_dropoff(pid, stAct, endAct)
                        stAct = endAct
                        #raw_input('assigned pickup dropoff for acts with same loc but discretionary/other activity engagement')
                        continue

                    # if above is not true then allocate the end activity ... first act is oh and end act is ih
                    if (stAct.location == endAct.location) and (stAct.actType >= 200 and endAct.actType == 101):
                        self.allocate_pickup_dropoff_endact(pid, stAct, endAct)
                        stAct = endAct
                        #raw_input('assigned pickup dropoff for acts with same loc but discretionary/other activity engagement')
                        continue

                    # if above is not true then allocate the end activity ... first act is oh and end act is sojourn
                    if (stAct.location == endAct.location) and (stAct.actType >= 200 and endAct.actType == 100):
                        self.allocate_pickup_dropoff(pid, stAct, endAct)
                        stAct = endAct
                        #raw_input('assigned pickup dropoff for acts with same loc but discretionary/other activity engagement')
                        continue



                    if (endAct.location <> stAct.location)  and (endAct.actType >= 500 or
                                                                 (endAct.actType < 400 and endAct.actType >= 200) or
                                                                 (endAct.actType <= 100)):
                        #print '\n\t\t2.3. OH Act: Terminal activity is not a Maint. activity and end act need not be allocated'
                        #print '\t\t\t Terminal Activity-', endAct
                        self.allocate_pickup_dropoff(pid, stAct, endAct)
                        stAct = endAct
                        #raw_input('Assigned a pickup dropoff')
                        continue

                    # ALLOCATE PREVIOUS INHOME TO END SOJOURN ADULT - Case1
                    # ALLOCATE PICK-UP DROP-OFF TO END SOJOURN ADULT WHEN PREVIOUS OUTHOME - Case2 (see below started coding)

                    if (endAct.location <> stAct.location)  and (endAct.actType > 100 and endAct.actType < 200):
                        #print '\n\t\t2.4. Return Home Act: Allocate the IH activity as well'
                        #print '\t\t\t Terminal Activity-', endAct
                        self.allocate_pickup_dropoff_endact(pid, stAct, endAct)
                        stAct = endAct
                        continue

                    if (endAct.location == stAct.location) and (endAct.actType > 100 and endAct.actType < 200):
                        #print '\n\t\t2.1. IH Act: Someone needs to be there'
                        #print '\t\t\t', endAct
                        self.allocate_ih_activity(pid, endAct)
                        stAct = endAct
                        continue


                    #print 'is it even getting here'

                    stAct = endAct
                    #raw_input()

                    #if self.hid == 108694:
                    #   self.persons[2].print_activity_list()
                    #   raw_input('check the dep person id ... ')


        """
        for pid in self.unallocatedActs.keys():
            print 'Unallocated activities for person - ', pid

            actList = self.unallocatedActs[pid]

            for act in actList:
                if len(act) == 1:
                    print '\tjust a in-home episode for houseid - %s personid - %s' %(self.hid, pid)
                if len(act) == 2:
                    print '\tjust a pickup and dropoff for houseid - %s personid - %s' %(self.hid, pid)
                if len(act) == 3:
                    print '\tjust a pickup and dropoff and terminal activity for houseid - %s personid - %s' %(self.hid, pid)
                if len(act) > 3:
                    print '\tactivity chain for houseid - %s personid - %s' %(self.hid, pid)

                for a in act:
                    print '\t    act-', a

        if len(self.unallocatedActs.keys()) > 0:
           print 'lenof unallocated acts for hid - %s is - %s' %(self.hid, self.lenUnallocatedActs)
           #raw_input()
        """

        #for pid in self.dependencyPersonIds:
        #    person = self.persons[pid]
        #    self.print_activity_list(person)
        #    #raw_input()

        for pid in self.persons.keys():
            person = self.persons[pid]
            if not person._check_for_conflicts():
                self.print_activity_list(person)
                raise Exception, 'The person still has conflicts - %s, %s' %(self.hid, pid)


    def print_activity_list(self, person, dependent=False):
        print '\t--> ACTIVITY LIST for person - ', person.hid, person.pid
        acts = copy.deepcopy(person.listOfActivityEpisodes)
        for i in range(len(acts)):
            stTime, act = hp.heappop(acts)
            if not dependent:
                print '\t\t', act
            elif act.dependentPersonId <> 0:
                print '\t\t', act


    def check_for_terminal_vertex(self, actOfPerson, actOfdepPerson, start):
        if start:
            return actOfdepPerson.endTime >= actOfPerson.endTime
        else:
            return actOfdepPerson.startTime <= actOfPerson.startTime


    def _adjust_terminal_vertex(self, actOfPerson, actOfdepPerson, start):
        if start:
            actOfPerson.endTime = actOfdepPerson.endTime - 1
            actOfPerson.duration = actOfPerson.endTime - actOfPerson.startTime
        else:
            actOfPerson.startTime = actOfdepPerson.startTime + 1
            actOfPerson.duration = actOfPerson.endTime - actOfPerson.startTime
        return actOfPerson

    def find_terminal_vertex(self, person, start):
        if start:
            actStartTime, act = hp.heappop(person.listOfActivityEpisodes)
            return act
        else:
            for actStartTime, act in person.listOfActivityEpisodes:
                if act.endOfDay:
                    person.remove_episodes([act])
                    return act

    def adjust_terminal_activity_episodes(self, depPersonId, actOfdepPerson, start=True):

        #print '\t\t\t\tAdjusting the terminal start-"%s" activity episodes to ensure that the child is taken care of' %(start)
        depPerson = self.persons[depPersonId]

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            person = self.persons[pid]

            if start:
                check = person.check_start_of_day(actOfdepPerson.endTime, depPersonId)
            else:
                check = person.check_end_of_day(actOfdepPerson.startTime, depPersonId)

            if check:
                #print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.update_depPersonId_for_terminal_episode(start, depPersonId, pid)
                return True

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]


            if start:
                check = person.check_start_of_day(actOfdepPerson.endTime, depPersonId)
            else:
                check = person.check_end_of_day(actOfdepPerson.startTime, depPersonId)

            if check:
                #print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.update_depPersonId_for_terminal_episode(start, depPersonId, pid)
                return True


        #print """\t\t\t --- > Exception: No person identified that can be with the """\
        #    """dependent child for the terminal episodes in a day"""\

        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities and  then adjust their terminal
        # episode durations so that children are not abandoned


        if start:
            terminalAct = depPerson.firstEpisode
        else:
            terminalAct = depPerson.lastEpisode

        if len(self.noDailyFixedActPersonIds) > 0:
            self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)
            pid = self.noDailyFixedActPersonIds[0] # check to see if there any people without fixed acts and
                                                # assign to the first random person among them
        else:
            pid = self.personId_with_terminal_episode_overlap(depPersonId, [terminalAct],
                                                              self.dailyFixedActPersonIds) # else assign to
                                                                                           # person with fixed
                                                                                           # acts with least
                                                                                           # conflict

        pid = None
        if pid is None:
            self.update_depPersonId_for_terminal_episode(start, depPersonId, 99)
            #print "Exception, --There are no independent adults in the household for hid - %s--" %(self.hid)
            return

        #print "\t\t\t\t--Randomly independent adults in the household is selected and id is --", pid

        person = self.persons[pid]


        #print '----before - ', person.lastEpisode.dependentPersonId
        if start:
            depPerson.move_start_of_day(person.firstEpisode.endTime, pid, dependent=True)
            if person.firstEpisode.dependentPersonId == 0:
                person.firstEpisode.dependentPersonId = 100 + depPersonId
            else:
                person.firstEpisode.dependentPersonId = 100.*person.firstEpisode.dependentPersonId + depPersonId
        else:
            depPerson.move_end_of_day(person.lastEpisode.startTime, pid, dependent=True)

            if person.lastEpisode.dependentPersonId == 0:
                person.lastEpisode.dependentPersonId = 100 + depPersonId
            else:
                person.lastEpisode.dependentPersonId = 100.*person.lastEpisode.dependentPersonId + depPersonId
        #print '----after - ', person.lastEpisode.dependentPersonId


        return True


    def adjust_terminal_activity_episodes1(self, depPersonId, actOfdepPerson, start=True):

        #print '\t\t\t\tAdjusting the terminal start-"%s" activity episodes to ensure that the child is taken care of' %(start)
        depPerson = self.persons[depPersonId]

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            person = self.persons[pid]

            if start:
                check = person.check_start_of_day(actOfdepPerson.endTime, depPersonId)
            else:
                check = person.check_end_of_day(actOfdepPerson.startTime, depPersonId)

            if check:
                #print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.update_depPersonId_for_terminal_episode(start, depPersonId, pid)
                return True

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]


            if start:
                check = person.check_start_of_day(actOfdepPerson.endTime, depPersonId)
            else:
                check = person.check_end_of_day(actOfdepPerson.startTime, depPersonId)

            if check:
                #print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.update_depPersonId_for_terminal_episode(start, depPersonId, pid)
                return True


        #print """\t\t\t --- > Exception: No person identified that can be with the """\
        #    """dependent child for the terminal episodes in a day"""\

        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities and  then adjust their terminal
        # episode durations so that children are not abandoned


        if start:
            terminalAct = depPerson.firstEpisode
        else:
            terminalAct = depPerson.lastEpisode


        pid = self.personId_with_terminal_episode_overlap(depPersonId, [terminalAct],
                                                          self.indepPersonIds)

        #pid = self.personId_with_least_conflict([terminalAct],
        #                                        self.indepPersonIds)
        if pid is None:
            self.update_depPersonId_for_terminal_episode(start, depPersonId, 99)
            #print "Exception, --There are no independent adults in the household for hid - %s--" %(self.hid)
            return


        #print "\t\t\t\t--Randomly independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        #actOfPerson = self.find_terminal_vertex(person, start)




        if start:
            person.move_start_of_day(actOfdepPerson.endTime, depPersonId)
        else:
            person.move_end_of_day(actOfdepPerson.startTime, depPersonId)

        """
        # Alternative implementation
        if start:
            actOfPerson = person.firstEpisode
            depPerson.move_start_of_day(actOfPerson.endTime)
        else:
            actOfPerson = person.lastEpisode
            depPerson.move_end_of_day(actOfPerson.startTime)

        """

        if not person._check_for_conflicts_with_activity(actOfdepPerson):
            #print '\t----- NEED TO ADJUST THIS PERSONS ACT SCHEDULE -----'
            #self.print_activity_list(person)
            person.adjust_child_dependencies([actOfdepPerson])
            #self.print_activity_list(person)
            #raw_input()

        self.update_depPersonId_for_terminal_episode(start, depPersonId, pid)
        return True


    def update_depPersonId_for_terminal_episode(self, start, depPersonId, pid):
        #print '\t--> Terminal episode allocated to - ', pid
        depPerson = self.persons[depPersonId]
        if start:
            depPerson.firstEpisode.dependentPersonId = pid
        else:
            depPerson.lastEpisode.dependentPersonId = pid
        if pid <> 99:
            assignPerson = self.persons[pid]
            #self.print_activity_list(assignPerson)


    def allocate_ih_activity(self, depPersonId, act):
        #print 'allocating ih activity ---- >'
        # Changing the activitytype to +50 to assign that as a dependent
        # activity
        act = copy.deepcopy(act)
        act.actType += 50
        #act.dependentPersonId = 99
        act.dependentPersonId = 100 + depPersonId

        #print act
        # If there are people already home then that
        # person is allocated this particular activity

        self.rndGen.shuffle_sequence(self.indepPersonIds)

        for pid in self.indepPersonIds:
            person = self.persons[pid]
            act.scheduleId = person.actCount + 1
            person.add_episodes([act], temp=True)

            if person._check_for_ih_conflicts(act, depPersonId):
                #print '\t\t\t\tPerson - %s is already home so he is allocated this activity' %(pid)
                self.update_depPersonId(act, depPersonId, pid)
                #person.remove_episodes([act])
                return True
            else:
                pass
                #person.remove_episodes([act])



        # Person without fixed activities
        #print '\t\t\tScanning person without fixed activities - '
        # We allocate to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            person = self.persons[pid]
            act.scheduleId = person.actCount + 1
            person.add_episodes([act], temp=True)

            if not person._check_for_conflicts_with_activity(act):
                person.remove_episodes([act])
            else:
                #print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.update_depPersonId(act, depPersonId, pid)
                return True

        # Person with fixed activities
        #print '\t\t\tScanning person with fixed activities - '
        # We allocate to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]
            act.scheduleId = person.actCount + 1
            person.add_episodes([act], temp=True)

            if not person._check_for_conflicts_with_activity(act):
                person.remove_episodes([act])
            else:
                #print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.update_depPersonId(act, depPersonId, pid)
                return True

        #print " \t\t\t--- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities


        pid = self.personId_with_least_conflict(depPersonId, [act],
                                                self.indepPersonIds)


        pid = None
        if pid is None:
            self.update_depPersonId(act, depPersonId, 99)
            #print "Exception, --There are no independent adults in the household for hid - %s--" %(self.hid)
            return

        #print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        act.scheduleId = person.actCount + 1
        person.add_episodes([act], temp=True)
        self.update_depPersonId(act, depPersonId, pid)


        #person._check_for_conflicts()

        if not person._check_for_conflicts_with_activity(act):
            #print '\t----- NEED TO ADJUST THIS PERSONS ACT SCHEDULE -----'
            #self.print_activity_list(person)
            person.adjust_child_dependencies([act])
            #self.print_activity_list(person)


        #person.adjust_activity_schedules(self.seed)
        return True

    def update_depPersonId(self, activity, depPersonId, pid):
        #print '\t--> Activity episode allocated to - ', pid
        if not isinstance(activity, list):
            activityList = [activity]
        else:
            activityList = activity

        depPerson = self.persons[depPersonId]

        for activity in activityList:
            for actStart, act in depPerson.listOfActivityEpisodes:
                if act.startTime == activity.startTime:
                    #print '\t\t\t\t------>BEFORE ASSIGN', act
                    act.dependentPersonId = pid
                    #print '\t\t\t\t-------------->AFTER ASSIGN', act
        #indAct = depPerson.listOfActivityEpisodes.index((activity.startTime, activity))
        #act = depPerson.listOfActivities[indAct]

        #act.dependentPersonId = pid


        #self.print_activity_list(depPerson)

        if pid <> 99:
            assignPerson = self.persons[pid]
            #self.print_activity_list(assignPerson)

    def allocate_pickup_dropoff(self, depPersonId, stAct, endAct):
        # Create pickup-dropoff for the front end of the activity
        dummyActPickUp, dummyActDropOff = self.create_dummy_activity(depPersonId, stAct, endAct)

        dummyActPickUp.dependentPersonId = 100 + depPersonId
        dummyActDropOff.dependentPersonId = 100 + depPersonId

        # Person without fixed activities
        # We allocate pickup/dropoff to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            jointPickUpDropOffFlag = True
            person = self.persons[pid]
            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2

            person.add_episodes([dummyActPickUp, dummyActDropOff], temp=True)

            if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff]):
                if person._check_for_home_to_home_trips():
                    jointPickUpDropOffFlag = False
                    person.remove_episodes([dummyActPickUp, dummyActDropOff])
                else:
                    person.remove_episodes([dummyActPickUp, dummyActDropOff])
                    confActs = person._identify_conflict_activities([dummyActPickUp, dummyActDropOff])

                    if len(confActs) > 0:
                        # If confActs == 0 then it probably means that a home to home trip was being introduced
                        jointPickUpDropOffFlag = self.check_conflicts_with_pickup_dropoff(confActs, dummyActPickUp, dummyActDropOff, depPersonId, pid)

            if jointPickUpDropOffFlag:
                #print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
                return True

        # Person with fixed activities
        # We allocate pickup/dropoff to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            #print '\t\t\tchecking with hid - %s pid - '%self.hid, pid
            jointPickUpDropOffFlag = True
            person = self.persons[pid]
            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2

            person.add_episodes([dummyActPickUp, dummyActDropOff], temp=True)

            if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff]):
                #print '\t\t\t\tfor the above person there is a conflict'
                if person._check_for_home_to_home_trips():
                    #print '\t\t\t\tfor the above person there is a home-to-home conflict'
                    jointPickUpDropOffFlag = False
                    person.remove_episodes([dummyActPickUp, dummyActDropOff])
                else:
                    #print '\t\t\t\tfor the above person there is a overlap conflict'
                    person.remove_episodes([dummyActPickUp, dummyActDropOff])
                    confActs = person._identify_conflict_activities([dummyActPickUp, dummyActDropOff])

                    if len(confActs) > 0:
                        # If confActs == 0 then it probably means that a home to home trip was being introduced
                        jointPickUpDropOffFlag = self.check_conflicts_with_pickup_dropoff(confActs, dummyActPickUp, dummyActDropOff, depPersonId, pid)

            if jointPickUpDropOffFlag:
                #print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
                return True

        #print "\t\t\t --- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities


        pid = self.personId_with_least_conflict(depPersonId,
                                                [dummyActPickUp, dummyActDropOff],
                                                self.indepPersonIds)
        pid = None
        if pid is None:
            self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, 99)
            #print "Exception, --There are no independent adults in the household for hid - %s--" %(self.hid)
            return

        #print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        dummyActPickUp.scheduleId = person.actCount + 1
        dummyActDropOff.scheduleId = person.actCount + 2
        person.add_episodes([dummyActPickUp, dummyActDropOff])
        self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)

        if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff]):
            #print '\t----- NEED TO ADJUST THIS PERSONS ACT SCHEDULE -----'
            person.adjust_child_dependencies([dummyActPickUp, dummyActDropOff])

        return True

    def check_conflicts_with_pickup_dropoff(self, confActs, dummyActPickUp, dummyActDropOff, depPersonId, pid):

        #print '\t\t\tWith person - ', pid
        #print '\t\t\t\tlength of conflicts', confActs
        if len(confActs) > 2:
            raw_input('More than two conflicts with pickup/dropoff? Not possible?')

        if len(confActs) == 2:
            pickUpConf = confActs[0]
            dropOffConf = confActs[1]
            conflictPickup = False
            conflictDropoff = False


        if len(confActs) == 1:
            confAct = confActs[0]

            if confAct.startTime <= dummyActPickUp.startTime and confAct.endTime >= dummyActPickUp.endTime:
                pickUpConf = confAct
                dropOffConf = None
                conflictPickup = False
                conflictDropoff = False
            elif confAct.startTime <= dummyActDropOff.startTime and confAct.endTime >= dummyActDropOff.endTime:
                pickUpConf = None
                dropOffConf = confAct
                conflictPickup = False
                conflictDropoff = False
            else:
                print 'CONF ACT - ', confAct
                raw_input('THIS SHOULD NOT HAPPEN THE CONFLICT ACT SHOULD CONFLCIT WITH EITHER PIKCUP OF DROPOFF')



        #print '\t\t\t\tconf pickup', pickUpConf
        #print '\t\t\t\tconf dropoff', dropOffConf

        if (pickUpConf is not None
            and pickUpConf.actType == 600
            and (dummyActPickUp.location == pickUpConf.location)
            and (dummyActPickUp.startTime == pickUpConf.startTime)
            and (dummyActPickUp.endTime == pickUpConf.endTime)):
            #print '\t\t\t    Conflictwith-', pickUpConf
            conflictPickup = True
            #print '\t\t\t    ConflictwithUpdated-', pickUpConf

        if (dropOffConf is not None
            and dropOffConf.actType == 601
            and (dummyActDropOff.location == dropOffConf.location)
            and (dummyActDropOff.startTime == dropOffConf.startTime)
            and (dummyActDropOff.endTime == dropOffConf.endTime)):
            #print '\t\t\t    Conflictwith-', dropOffConf
            conflictDropoff = True
            #print '\t\t\t    ConflictwithUpdated-', dropOffConf

        if (pickUpConf is not None and dropOffConf is not None):
            if conflictPickup is False or conflictDropoff is False:
                #print '\t\tnot a valid pickup/dropoff because one of the conflicts is not a pickup/dropoff for some other dependent person'
                return False


        if (conflictPickup or conflictDropoff):
            if conflictPickup:
                #print ("\t\t\t\tconflict is with pickup")
                #print '\t\t\t\tpickup act - ', dummyActPickUp
                #print '\t\t\t\tpickup conflict - ', pickUpConf
                pickUpConf.dependentPersonId = pickUpConf.dependentPersonId*100. + depPersonId
                if pickUpConf.tripCount < 100:
                    pickUpConf.tripCount = (100+pickUpConf.tripCount)*100 + dummyActPickUp.tripCount
                else:
                    pickUpConf.tripCount = pickUpConf.tripCount*100 + dummyActPickUp.tripCount
            if conflictDropoff:
                #print ("\t\t\t\tconflict is with dropoff")
                #print '\t\t\t\tdropoff act - ', dummyActDropOff
                #print '\t\t\t\tdropoff conflict - ', dropOffConf
                dropOffConf.dependentPersonId = dropOffConf.dependentPersonId*100. + depPersonId
                if dropOffConf.tripCount < 100:
                    dropOffConf.tripCount = (100+dropOffConf.tripCount)*100 + dummyActDropOff.tripCount
                else:
                    dropOffConf.tripCount = dropOffConf.tripCount*100 + dummyActDropOff.tripCount


            #self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], pid, depPersonId, dependent=False)


            person = self.persons[pid]
            if pickUpConf is None:
                self.add_activity_update_depPersonId([dummyActPickUp], pid, depPersonId, dependent=False)
                # we are using the same function for adding and updating deppersonid for indep adult

            if dropOffConf is None:
                self.add_activity_update_depPersonId([dummyActDropOff], pid, depPersonId, dependent=False)
                # we are using the same function for adding and updating deppersonid for indep adult


            #print ("\t\tconflict with other pick/dropoff so potentially still a candidate")
            #raw_input("conflict with other pick/dropoff so potentially still a candidate")
            return True
        return False


    def create_dummy_activity_for_chain(self, depPersonId, actsInTour):
        intActCount = len(actsInTour) - 2

        # Building the dummy pickup and drop-offs for the chain
        actIncChauffering = []
        chaufferingEpisodes = []
        for i in range(intActCount + 1):
            dummyActPickUp, dummyActDropOff = self.create_dummy_activity(depPersonId,
                                                                         actsInTour[i+0],
                                                                         actsInTour[i+1])

            #dummyActPickUp.dependentPersonId = 99
            #dummyActDropOff.dependentPersonId = 99
            #actsInTour[i+1].dependentPersonId = 99

            dummyActPickUp.dependentPersonId = 100 + depPersonId
            dummyActDropOff.dependentPersonId = 100 + depPersonId
            actsInTour[i+1].dependentPersonId = 100 + depPersonId

            actsInTour[i+1].actType += 50

            chaufferingEpisodes.append(dummyActPickUp)
            chaufferingEpisodes.append(dummyActDropOff)

            actIncChauffering.append(dummyActPickUp)
            actIncChauffering.append(dummyActDropOff)
            actIncChauffering.append(actsInTour[i+1])
        # Removing the last anchor because that is not
        # pursued by the allocated dependent person
        actIncChauffering = actIncChauffering[:-1]

        return actIncChauffering, chaufferingEpisodes



    def intermediate_acts(self, actsInTour):
        intActCount = len(actsInTour) - 2

        intActs = []
        for i in range(intActCount):
            intActs.append(actsInTour[i+1])

        return intActs


    def allocate_trip_activity_chain(self, depPersonId, actsInTour):
        # Create pickup-dropoff for the front end of the activity
        #if pickup:

        actsInTourCopy = copy.deepcopy(actsInTour)
        actIncChauffering, chaufferingEpisodes = self.create_dummy_activity_for_chain(depPersonId,
                                                                                      actsInTourCopy)
        intActs = self.intermediate_acts(actsInTour)

        #print '\t\tActs including chauffering - '
        #for act in actIncChauffering:
        #    print '\t\t    ',act

        # Person without fixed activities
        #print '\t\t\tScanning person without fixed activities - '
        # We allocate pickup/dropoff to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            # Create dummy travel episodes
            person = self.persons[pid]
            #self.print_activity_list(person)
            #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
            for actNum in range(len(actIncChauffering)):
                act = actIncChauffering[actNum]
                act.scheduleId = person.actCount + actNum + 1
            person.add_episodes(actIncChauffering, temp=True)
            #print 'THE ACT COUNT AFTER ADDING', person.actCount, len(person.listOfActivityEpisodes)
            #self.print_activity_list(person)
            #if not person._check_for_conflicts():
            if not person._check_for_conflicts_with_activity(actIncChauffering):
                person.remove_episodes(actIncChauffering)
            else:
                #print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId(chaufferingEpisodes, depPersonId, pid)
                #self.add_activity_update_depPersonId(actIncChauffering, depPersonId, pid)
                self.update_depPersonId(actIncChauffering, depPersonId, pid)
                for intAct in intActs:
                    intAct.dependentPersonId = pid
                return True

        # Person with fixed activities
        #print '\t\t\tScanning person with fixed activities - '
        # We allocate pickup/dropoff to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]
            #self.print_activity_list(person)
            #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
            for actNum in range(len(actIncChauffering)):
                act = actIncChauffering[actNum]
                act.scheduleId = person.actCount + actNum + 1
            person.add_episodes(actIncChauffering, temp=True)
            #print 'THE ACT COUNT AFTER ADDING', person.actCount, len(person.listOfActivityEpisodes)
            #self.print_activity_list(person)
            #if not person._check_f = 0or_conflicts():
            if not person._check_for_conflicts_with_activity(actIncChauffering):
                person.remove_episodes(actIncChauffering)
            else:
                #print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId(chaufferingEpisodes, depPersonId, pid)
                #self.add_activity_update_depPersonId(actIncChauffering, depPersonId, pid)
                self.update_depPersonId(actIncChauffering, depPersonId, pid)
                for intAct in intActs:
                    intAct.dependentPersonId = pid
                return True

        #print "\t\t\t --- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities


        pid = self.personId_with_least_conflict(depPersonId,
                                                actIncChauffering,
                                                self.indepPersonIds)
        pid = None
        if pid is None:
            self.add_activity_update_depPersonId(chaufferingEpisodes, depPersonId, 99)
            self.update_depPersonId(actIncChauffering, depPersonId, 99)
            #print "Exception, --There are no independent adults in the household for hid - %s--" %(self.hid)
            return

        #print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        #self.print_activity_list(person)
        #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
        for actNum in range(len(actIncChauffering)):
            act = actIncChauffering[actNum]
            act.scheduleId = person.actCount + actNum + 1

        person.add_episodes(actIncChauffering)
        self.add_activity_update_depPersonId(chaufferingEpisodes, depPersonId, pid)
        #self.add_activity_update_depPersonId(actIncChauffering, depPersonId, pid)


        """
        if person._check_for_home_to_home_trips():
            person.remove_episodes(actIncChauffering)
            print '\t----- NOT ALLOCATING TO THIS ADULT WITH LEAST CONFLICT BECAUSE IN_HOME_IN_HOME TRIPS ARE BEING INTRODUCED-----'
            return False
        """
        self.update_depPersonId(actIncChauffering, depPersonId, pid)
        for intAct in intActs:
            intAct.dependentPersonId = pid

        #person._check_for_conflicts()

        if not person._check_for_conflicts_with_activity(actIncChauffering):
            #print '\t----- NEED TO ADJUST THIS PERSONS ACT SCHEDULE -----'
            #self.print_activity_list(person)
            person.adjust_child_dependencies(actIncChauffering)
            #self.print_activity_list(person)
        #person.adjust_activity_schedules(self.seed)
        return True


    def allocate_pickup_dropoff_endact(self, depPersonId, stAct, endAct):
        # Create pickup-dropoff for the front end of the activity
        #if pickup:
        endActToNonDependent = copy.deepcopy(endAct)
        dummyActPickUp, dummyActDropOff = self.create_dummy_activity(depPersonId, stAct, endAct)

        #dummyActPickUp.dependentPersonId = 99
        #dummyActDropOff.dependentPersonId = 99
        #endActToNonDependent.dependentPersonId = 99

        dummyActPickUp.dependentPersonId = 100 + depPersonId
        dummyActDropOff.dependentPersonId = 100 + depPersonId
        endActToNonDependent.dependentPersonId = 100 + depPersonId

        endActToNonDependent.actType += 50



        # Person without fixed activities
        #print '\t\t\tScanning person without fixed activities - '
        # We allocate pickup/dropoff to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            # Create dummy travel episodes
            person = self.persons[pid]
            #self.print_activity_list(person)
            #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2
            endActToNonDependent.scheduleId = person.actCount + 3
            #print dummyActPickUp
            #print dummyActDropOff
            person.add_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent], temp=True)
            #print 'THE ACT COUNT AFTER ADDING', person.actCount, len(person.listOfActivityEpisodes)
            #self.print_activity_list(person)
            if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff,
                                                              endActToNonDependent]):
                #if not person._check_for_conflicts():
                person.remove_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent])
            else:
                #print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
                self.update_depPersonId([dummyActPickUp, dummyActDropOff,
                                                              endActToNonDependent], depPersonId, pid)
                endAct.dependentPersonId = pid
                return True

        # Person with fixed activities
        #print '\t\t\tScanning person with fixed activities - '
        # We allocate pickup/dropoff to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]
            #self.print_activity_list(person)
            #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2
            endActToNonDependent.scheduleId = person.actCount + 3
            #print dummyActPickUp
            #print dummyActDropOff
            person.add_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent], temp=True)
            #print 'THE ACT COUNT AFTER ADDING', person.actCount, len(person.listOfActivityEpisodes)
            #self.print_activity_list(person)
            #if not person._check_for_conflicts():
            if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff,
                                                              endActToNonDependent]):

                person.remove_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent])
            else:
                #print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
                self.update_depPersonId([dummyActPickUp, dummyActDropOff,
                                                              endActToNonDependent], depPersonId, pid)

                endAct.dependentPersonId = pid
                return True

        #print "\t\t\t --- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities


        pid = self.personId_with_least_conflict(depPersonId,
                                                [dummyActPickUp, dummyActDropOff, endActToNonDependent],
                                                self.indepPersonIds)
        pid = None
        if pid is None:
            self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, 99)
            self.update_depPersonId([dummyActPickUp, dummyActDropOff,
                                                              endActToNonDependent], depPersonId, 99)

            #print "Exception, --There are no independent adults in the household for hid - %s--" %(self.hid)
            return

        #print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        #self.print_activity_list(person)
        #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
        dummyActPickUp.scheduleId = person.actCount + 1
        dummyActDropOff.scheduleId = person.actCount + 2
        endActToNonDependent.scheduleId = person.actCount + 3
        person.add_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent])

        """
        if person._check_for_home_to_home_trips():
            print '\t----- CHECKING TO SEE IF THE ADULT WITH LEAST CONFLICT HAS IN_HOME_IN_HOME TRIPS BEING INTRODUCED-----??'
            person.remove_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent])
            print '\t----- NOT ALLOCATING TO THIS ADULT WITH LEAST CONFLICT BECAUSE IN_HOME_IN_HOME TRIPS ARE BEING INTRODUCED-----'
            return False

        """

        self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
        self.update_depPersonId([dummyActPickUp, dummyActDropOff,
                                 endActToNonDependent], depPersonId, pid)

        endAct.dependentPersonId = pid

        #person._check_for_conflicts()

        if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff,
                                                          endActToNonDependent]):
            #print '\t----- NEED TO ADJUST THIS PERSONS ACT SCHEDULE -----'
            #self.print_activity_list(person)
            person.adjust_child_dependencies([dummyActPickUp, dummyActDropOff, endActToNonDependent])
            #self.print_activity_list(person)
        return True


    def add_activity_update_depPersonId(self, activityList, depPersonId, pid, dependent=True):
        #print '\t--> Activity list allocated to - ', pid
        depPerson = self.persons[depPersonId]

        activityList = copy.deepcopy(activityList)

        for i in range(len(activityList)):
            act = activityList[i]
            act.scheduleId = depPerson.actCount + i + 1
            if dependent:
                act.dependentPersonId = pid
            else:
                act.dependentPersonId = 100 + pid

        depPerson.add_episodes(activityList)
        depPerson._check_for_conflicts()

        if pid <> 99:
            assignPerson = self.persons[pid]
            #self.print_activity_list(assignPerson)
        #raw_input('activity list added and dep updated')


    def randPersonId(self, personIdList):
        lengthOfList = len(personIdList)
        randNum = self.rndGen.return_random_integers(0, lengthOfList - 1)
        pid = personIdList[randNum]
        return pid



    def personId_with_least_conflict(self, depPersonId, activityList, personIdList):
        personConflict = {}
        personConflictActs = {}
        for pid in personIdList:
            #print '\t\tfor person - ', pid
            person = self.persons[pid]

            person.add_episodes(activityList, temp=True)
            conflict = person._conflict_duration()

            if person._check_for_home_to_home_trips():
                #print '\t----- CHECKING TO SEE IF THE ADULT WITH LEAST CONFLICT HAS IN_HOME_IN_HOME TRIPS BEING INTRODUCED-----??', pid
                checkForHomeToHomeTrips = True
                #print '\t----- NOT ALLOCATING TO THIS ADULT WITH LEAST CONFLICT BECAUSE IN_HOME_IN_HOME TRIPS ARE BEING INTRODUCED-----', pid

            else:
                checkForHomeToHomeTrips = False

            person.remove_episodes(activityList)

            conflictActs = person._identify_conflict_activities(activityList)
            checkForDependencies = self._check_for_dependencies_for_conflictActivities(depPersonId,
                                                                                       conflictActs)

            #print '\t\t\tConflict acts for person id - ', pid
            #for act in conflictActs:
                #print '\t\t\t\t', act

                #print '\t\t\t\tDependencies - ', checkForDependencies, ', checkForHomeToHomeTrips', checkForHomeToHomeTrips

            if not checkForDependencies:
                continue

            if checkForHomeToHomeTrips == True:
                continue

            personConflict[pid] = conflict
            personConflictActs[pid] = conflictActs

        #print personConflict
        #print personConflictActs

            #print '\t\t\t\t\tPerson - %s has conflict of duration - %s  for above activity' %(pid, conflict)

        if len(personConflict) > 0:
            leastConflict = min(personConflict.values())
        else:
            if depPersonId not in self.unallocatedActs.keys():
                self.unallocatedActs[depPersonId] = [activityList]
                self.lenUnallocatedActs += 1
            else:
                self.unallocatedActs[depPersonId].append(activityList)
                self.lenUnallocatedActs += 1
            return


        personIdsWithConflict = copy.deepcopy(personConflict.keys())
        for pid in personIdsWithConflict:
            #print '\t\t\t\t\tperson - ', pid, 'conflict for person - ', personConflict[pid], 'least conflict', leastConflict
            if personConflict[pid] == leastConflict:

                return pid



    def _check_for_dependencies_for_conflictActivities(self, depPersonId, conflictActs, terminal=False):
        #print '\t\t\t\tCHECKING FOR DEPENDENCIES for dep act of person - ', depPersonId

        conflict = []

        for act in conflictActs:
            #print '\t\tdependencies for conflicts - ', act.dependentPersonId, depPersonId
            #print '\t\t\tCONFLICT-', act


            if (act.startTime == 0 or act.endTime == 1439) and terminal:
                if (act.dependentPersonId > 0):
                    conflict.append(True)
                    #return True


            if act.dependentPersonId <> 0: # there is a dependency
                # If the terminal episodes are allocated for that dependent person then the indep person is a candidate
                #if [depPersonId] == self.parse_personids(act.dependentPersonId) and (act.startTime == 0 or act.endTime == 1439):
                #print [depPersonId],self.parse_personids(act.dependentPersonId), 'person ids --- '
                if [depPersonId] == self.parse_personids(act.dependentPersonId):
                    conflict.append(True)
                    #return True

                # If the terminal episodes are allocated for that dependent person and others then the indep person is NOT a candidate
                #if [depPersonId] <> self.parse_personids(act.dependentPersonId) and (act.startTime == 0 or act.endTime == 1439):
                if [depPersonId] <> self.parse_personids(act.dependentPersonId):
                    conflict.append(False)
                    #return False
                """
                if depPersonId > 0:
                    print 'this logic is being applied ---'
                    conflict.append(False)


                if depPersonId not in self.parse_personids(act.dependentPersonId): # check to see if the dependency is the same
                                                                                   # as the one for which activities are being allocated
                                                                                   # for
                    print '\t\t----->deppersonid - ', depPersonId, 'depof acts', self.parse_personids(act.dependentPersonId), 'False--'
                    conflict.append(False)
                    #return False
                """

        for conflictFlag in conflict:
            if conflictFlag == False:
                return False

        return True




    def personId_with_terminal_episode_overlap(self, depPersonId, activityList, personIdList):
        #print activityList
        personConflict = {}

        for pid in personIdList:
            #print '\tConflict acts for person id - ', pid
            person = self.persons[pid]
            #print self.print_activity_list(person)
            person.add_episodes(activityList, temp=True)


            stEpisode = person.firstEpisode
            conflictWithStartEpisode = person._conflict_duration_with_activity(stEpisode)

            enEpisode = person.lastEpisode
            conflictWithEndEpisode = person._conflict_duration_with_activity(enEpisode)

            conflictWithTermEpisodes = conflictWithStartEpisode + conflictWithEndEpisode
            conflict = person._conflict_duration()
            person.remove_episodes(activityList)


            conflictActs = person._identify_conflict_activities(activityList)
            checkForDependencies = self._check_for_dependencies_for_conflictActivities(depPersonId,
                                                                                       conflictActs, terminal=True)
            #print 'check for dependencies', pid, checkForDependencies

            #print 'with start, with end, full conflict'
            #print conflictWithStartEpisode, conflictWithEndEpisode, conflict
            #for act in conflictActs:
            #    print '\t', act

            if not checkForDependencies:
                continue


            personConflict[pid] = conflict - conflictWithTermEpisodes


            #print '\t\t\t\t\tPerson - %s has conflict of duration - %s  for above activity' %(pid,
            #                                                                                  (conflict -
            #                                                                                   conflictWithTerminalEpisode))
            #print '\t\t\t\t\tConflict - %s and conflict with last episode - %s' %(conflict,
            #                                                                      conflictWithTerminalEpisode)

            leastConflict = min(personConflict.values())

        for pid in personConflict.keys():
            #print 'person - ', pid, 'conflict for person - ', personConflict[pid], 'least conflict', leastConflict
            if personConflict[pid] == leastConflict:
                #print '\t\t\t\tPerson with least conflict with terminal episode is', pid
                return pid










    def create_dummy_activity(self, depPersonId, stAct, endAct):
        dummyPickUpAct = copy.deepcopy(stAct)
        dummyDropOffAct = copy.deepcopy(endAct)

        self.tripCount += 1

        # Pickup overlaps with the end of an activity
        dummyPickUpAct.startTime = dummyPickUpAct.endTime
        dummyPickUpAct.endTime = dummyPickUpAct.startTime + 1
        dummyPickUpAct.duration = 1
        dummyPickUpAct.actType = 600
        dummyPickUpAct.startOfDay = False
        dummyPickUpAct.endOfDay = False
        dummyPickUpAct.dependentPersonId = 0
        dummyPickUpAct.tripCount = self.tripCount

        # dropoff overlaps with the start of an activity
        dummyDropOffAct.startTime = dummyDropOffAct.startTime - 1
        dummyDropOffAct.endTime = dummyDropOffAct.startTime + 1
        dummyDropOffAct.duration = 1
        dummyDropOffAct.actType = 601
        dummyDropOffAct.startOfDay = False
        dummyDropOffAct.endOfDay = False
        dummyDropOffAct.dependentPersonId = 0
        dummyDropOffAct.tripCount = self.tripCount


        #print '\n\t\t\tPICKUP ACTIVITY - ', dummyPickUpAct

        #print '\t\t\tDropOff ACTIVITY -', dummyDropOffAct


        return dummyPickUpAct, dummyDropOffAct
