import copy
import heapq as hp
from numpy import array, zeros

from openamos.core.models.abstract_random_distribution_model import RandomDistribution


class Person(object):

    def __init__(self, hid, pid):
        self.hid = hid
        self.pid = pid
        self.listOfActivityEpisodes = []
        self.workEpisodes = []
        self.schoolEpisodes = []
        self.actCount = 0
        self.scheduleIds = []
        self.firstEpisode = None
        self.lastEpisode = None
        self.scheduleConflictIndicator = zeros((2880, 1))

        # Activity attributes
        self.child_dependency = 0
        self.workstatus = 0
        self.schoolstatus = 0

        # Person-level attributes for evolution
        self.age = 0
        self.clwkr = 0
        self.educ = 0
        self.enroll = 0
        self.esr = 0
        self.indnaics = 0
        self.occcen5 = 0
        self.race1 = 0
        self.relate = 0
        self.sex = 0
        self.marstat = 0
        self.hours = 0
        self.grade = 0
        self.hispan = 0

        # Evolution process fields for evolution
        self.mortality_f = 0
        self.birth_f = 0
        self.age_f = 0
        self.enrollment_f = 0
        self.grade_f = -3
        self.educ_f = -3
        self.educInYears_f = 0
        self.residenceType_f = 0
        self.laborParticipation_f = 0
        self.occupation_f = 0
        self.income_f = 0
        self.incomeCont = 0
        self.marriageDecision_f = 0
        self.divorceDecision_f = 0

        self.rndGen = RandomDistribution(int(self.hid * self.pid))

    def set_person_attributes(self, age, clwkr, educ, enroll,
                              esr, indnaics, occcen5, race1,
                              relate, sex, marstat, hours, grade,
                              hispan):
        # Person attributes for evolution
        self.age = age
        self.clwkr = clwkr
        self.educ = educ
        self.enroll = enroll
        self.esr = esr
        self.indnaics = indnaics
        self.occcen5 = occcen5
        self.race1 = race1
        self.relate = relate
        self.sex = sex
        self.marstat = marstat
        self.hours = hours
        self.grade = grade
        self.hispan = hispan

    def set_evolution_attributes(self, mortality_f, birth_f,
                                 age_f, enrollment_f,
                                 grade_f, educ_f,
                                 educInYears_f, residenceType_f,
                                 laborParticipation_f, occupation_f,
                                 income_f, marriageDecision_f,
                                 divorceDecision_f):
        # Evolution process fields
        self.mortality_f = mortality_f
        self.birth_f = birth_f
        self.age_f = age_f
        self.enrollment_f = enrollment_f
        self.grade_f = grade_f
        self.educ_f = educ_f
        self.educInYears_f = educInYears_f
        self.residenceType_f = residenceType_f
        self.laborParticipation_f = laborParticipation_f
        self.occupation_f = occupation_f
        self.income_f = income_f
        self.incomeCont = self.discretize_personal_income(income_f)
        self.marriageDecision_f = marriageDecision_f
        self.divorceDecision_f = divorceDecision_f

    def discretize_personal_income(self, incomeCat):
        if incomeCat == 0:
            contIncome = 0
        elif incomeCat == 1:
            contIncome = self.rndGen.return_uniform(0, 10000)
        elif incomeCat == 2:
            contIncome = self.rndGen.return_uniform(10000, 20000)
        elif incomeCat == 3:
            contIncome = self.rndGen.return_uniform(20000, 30000)
        elif incomeCat == 4:
            contIncome = self.rndGen.return_uniform(30000, 40000)
        elif incomeCat == 5:
            contIncome = self.rndGen.return_uniform(40000, 50000)
        elif incomeCat == 6:
            contIncome = self.rndGen.return_uniform(50000, 60000)
        elif incomeCat == 7:
            contIncome = self.rndGen.return_uniform(60000, 80000)
        elif incomeCat == 8:
            contIncome = self.rndGen.return_uniform(80000, 100000)
        elif incomeCat == 9:
            contIncome = self.rndGen.return_uniform(100000, 150000)
        elif incomeCat == 10:
            contIncome = self.rndGen.return_half_normal_variables(
                150000, 25000)
        return contIncome

    def reconcile_activity_schedules(self, seed=1):
        self.reconciledActivityEpisodes = []
        self.seed = seed
        # print self.hid * self.pid + self.seed
        self.rndGen = RandomDistribution(int(self.hid * self.pid))
        # self.add_episodes(activityEpisodes)
        self._reconcile_schedule()
        self.scheduleConflictIndicator = zeros((2880, 1))
        self.listOfActivityEpisodes = copy.deepcopy(
            self.reconciledActivityEpisodes)
        for actStart, act in self.listOfActivityEpisodes:
            self._update_schedule_conflict_indicator(act, add=True)

    def print_activity_list(self):
        print '\t--> ACTIVITY LIST for person - ', self.hid, self.pid
        acts = copy.deepcopy(self.listOfActivityEpisodes)
        for i in range(len(acts)):
            stTime, act = hp.heappop(acts)
            print '\t\t', stTime, act

    def add_episodes(self, activityEpisodes, temp=False):
        # print 'Before adding: Number of acts - ',
        # len(self.listOfActivityEpisodes)
        for activity in activityEpisodes:
            #activity.personid = self.pid
            if activity.startOfDay and not temp:
                self.firstEpisode = activity
            if activity.endOfDay and not temp:
                self.lastEpisode = activity
            hp.heappush(
                self.listOfActivityEpisodes, (activity.startTime, activity))
            self.actCount += 1
            self._update_schedule_conflict_indicator(activity, add=True)
        # print 'After adding episodes - '
        # self.print_activity_list()
        # raw_input()
        # print 'After adding: Number of acts - ',
        # len(self.listOfActivityEpisodes)

    def remove_episodes(self, activityEpisodes):
        # print 'CURRENT ACTIVIITES FOR PERSON - ', self.hid, self.pid
        # for currActivities in self.listOfActivityEpisodes:
        #    print '\t', currActivities

        for activity in activityEpisodes:
            #print (activity.startTime, activity)
            try:
                self.listOfActivityEpisodes.remove(
                    (activity.startTime, activity))
                hp.heapify(self.listOfActivityEpisodes)
            except ValueError, e:
                print 'Warning: Trying to remove a copy of the activityObject: %s and removing - %s' % (e, activity)
                raise ValueError, 'Warning: Trying to remove a copy of the activityObject: %s and removing - %s' % (
                    e, activity)

            self._update_schedule_conflict_indicator(activity, add=False)

    def retrieve_fixed_activity_ends(self, seed):
        minStart = 1440
        maxEnd = -1
        for stTime, act in self.listOfActivityEpisodes:
            if act.actType == 200 or act.actType == 300:
                if act.startTime < minStart:
                    minStart = copy.deepcopy(act.startTime)
                if act.endTime > maxEnd:
                    maxEnd = copy.deepcopy(act.endTime)

        if minStart == 1440:
            minStart = 0

        if maxEnd == 1440:
            maxEnd = 0

        return [self.hid, self.pid, minStart, maxEnd]

    def reset_activity_heap(self):
        tempList = []
        for stTime, act in self.listOfActivityEpisodes:
            tempList.append((act.startTime, act))

        self.listOfActivityEpisodes = tempList
        hp.heapify(self.listOfActivityEpisodes)

    def _update_schedule_conflict_indicator(self, activity, add=True):
        if add:
            self.scheduleConflictIndicator[
                activity.startTime:activity.endTime, :] += 1
        else:
            self.scheduleConflictIndicator[
                activity.startTime:activity.endTime, :] -= 1

    def reset_schedule_conflict_indicator(self):
        self.scheduleConflictIndicator = zeros((2880, 1))
        for stTime, activity in self.listOfActivityEpisodes:
            self.scheduleConflictIndicator[
                activity.startTime:activity.endTime, :] += 1

    def adjust_child_dependencies(self, activityList):
        # print '--->inside adjustment for conflicts',
        # self.print_activity_list()
        conflictActs = self._identify_conflict_activities(activityList)
        ownActs, depActs = self.return_own_dep_acts(conflictActs)
        #minStartTime, maxEndTime = self.return_min_max_time_of_activities(depActs)

        minStartTime = activityList[0].startTime
        maxEndTime = activityList[-1].endTime
        # print 'Min Start Time - %s and Max End Time - %s' %(minStartTime, maxEndTime)
        # print 'DEPENDENT ACTS'
        # for act in depActs:
        #    print '\t', act

        # print 'OWN ACTIVITIES'
        # for act in ownActs:
        #    print '\t', act

        # print 'Min Start Time - %s and Max End Time - %s' %(minStartTime,
        # maxEndTime)

        if len(ownActs) == 1:
            # print '\tException, Only one activity of the adult that needs to
            # be modified'
            self.adjust_and_delete_own_activities(
                ownActs, minStartTime, maxEndTime)
        elif len(ownActs) > 1:
            # print '\tException, More than one activity of the adult person
            # need to be modified/deleted'
            self.adjust_and_delete_own_activities(
                ownActs, minStartTime, maxEndTime)
        else:
            print 'No conflicts with own acts'
            #raise Exception, 'NO CONFLICTS??'
        # print 'Adjusted acts - '
        # for i in ownActs:
        #    print '\t', i
        # print '--->after adjustment for conflicts',
        # self.print_activity_list()
        """
        if len(depActs) == 0:
            self.adjust_merged_own_acts(ownActs, minStartTime, maxEndTime)
        else:
            if len(ownActs) == 1:
                print '\tException, Only one activity of the adult that needs to be modified'
                self.adjust_and_delete_own_activities(ownActs, minStartTime, maxEndTime)
            elif len(ownActs) > 1:
                print '\tException, More than one activity of the adult person need to be modified/deleted'
                self.adjust_and_delete_own_activities(ownActs, minStartTime, maxEndTime)
            else:
                print '\tException, NO CONFLICTS??'
        """

    def adjust_merged_own_acts(self, ownActs, minStartTime, maxEndTime):
        # Remove completely engulfed own activities that are colliding
        # with dependent activities of children
        newOwnActs = []
        for act in ownActs:
            if (act.startTime > minStartTime and act.endTime < maxEndTime):
                # print '\tRemoving activity', act
                # raw_input()
                self.remove_episodes([act])
            else:
                newOwnActs.append(act)

        newOwnActs = self.sort_acts(newOwnActs)

        firstAct = newOwnActs[0]

        for nextActIndex in range(len(newOwnActs) - 1):
            nextAct = newOwnActs[nextActIndex + 1]
            # print firstAct, nextAct, 'BEFORE'

            #self.remove_episodes([firstAct, nextAct])
            overlap = self._conflict_duration_with_activity(nextAct)
            overlapAdj = int(overlap / 2)

            firstActRef = firstAct.endTime - overlapAdj
            self.move_end(firstAct, firstActRef)

            nextActRef = nextAct.startTime + (overlap - overlapAdj) + 1
            self.move_start(nextAct, nextActRef)
            # print overlap, overlapAdj, firstActRef, nextActRef

            firstAct = nextAct

            # print firstAct, nextAct, 'AFTER'
            # raw_input()

    def sort_acts(self, actList):
        actVerticesDict = {}

        for act in actList:
            actVerticesDict[(act.startTime, act.endTime)] = act

        actVerticesList = actVerticesDict.keys()
        actVerticesList.sort()
        actList = [actVerticesDict[(st, end)] for (st, end) in actVerticesList]

        return actList

    def adjust_one_activity(self, ownAct, minStartTime, maxEndTime):
        # return
        # TODO: NEED TO INCLUDE THE NECESSARY TRAVEL TIME LATER
        # Adjusting start term episode
        # print 'ownAct start - %s and ownAct end - %s' %(ownAct.startTime,
        # ownAct.endTime)
        if (ownAct.startTime == 0 and ownAct.endTime >= minStartTime):
            # print 'Logic 1---------------------------------------'
            # print 'move_end'
            self.move_end(ownAct, minStartTime - 1)
            # print ownAct
            return

        # Adjusting end term episode
        if (ownAct.endTime == 1439 and ownAct.startTime <= maxEndTime):
            # print 'Logic 2---------------------------------------'
            self.move_start(ownAct, maxEndTime + 1)
            return

        # Own activity is engulfing the travel episode
        if ownAct.startTime < minStartTime and ownAct.endTime > maxEndTime:
            if ((minStartTime - ownAct.startTime) > (ownAct.endTime - maxEndTime)):
                # print 'Logic 3---------------------------------------'
                self.move_end(ownAct, minStartTime - 1)
            else:
                # print 'Logic 4---------------------------------------'
                self.move_start(ownAct, maxEndTime + 1)
            return

        if (ownAct.endTime >= minStartTime and ownAct.endTime <= maxEndTime):
            # print 'Logic 5---------------------------------------'
            self.move_end(ownAct, minStartTime - 1)
            return

        if (ownAct.startTime >= minStartTime and ownAct.startTime <= maxEndTime):
            # print 'Logic 6---------------------------------------'
            self.move_start(ownAct, maxEndTime + 1)
            return

        # print ownAct
        raise Exception, 'DONE NOTHING'

    def adjust_and_delete_own_activities(self, ownActs, minStartTime, maxEndTime):
        # return
        for act in ownActs:
            # print 'THIS IS WHAT IS BEING ADJUSTED'
            if (act.startTime == minStartTime and act.endTime == maxEndTime and
                    act.actType == 100):
                continue
            if (act.startTime == minStartTime and act.endTime == maxEndTime and
                    act.actType <> 100):
                # print '\tRemoving activity', act
                self.remove_episodes([act])
                continue
            if (act.startTime >= minStartTime - 1 and act.endTime <= maxEndTime + 1):
                # print '\tRemoving activity', act
                # raw_input()
                self.remove_episodes([act])
            else:
                # print '--->BEFORE one activity adjustment for conflicts',
                # self.print_activity_list()
                self.adjust_one_activity(act, minStartTime, maxEndTime)
                # print '--->AFTER one activity adjustment for conflicts',
                # self.print_activity_list()

    def return_min_max_time_of_activities(self, activityList):
        minStartTime = 1440
        maxEndTime = 0
        for act in activityList:
            if act.startTime < minStartTime:
                minStartTime = act.startTime
            if act.endTime > maxEndTime:
                maxEndTime = act.endTime

        return minStartTime, maxEndTime

    def return_own_dep_acts(self, activityList):
        ownActsList = []
        depActsList = []
        for act in activityList:
            # print '\tchecking for own/dep', act
            # if act.dependentPersonId <> 99:
            if act.dependentPersonId == 0:
                ownActsList.append(act)
            # elif act.dependentPersonId == 99 and (act.startTime == 0 or
            # act.endTime == 1439):
            elif act.dependentPersonId > 0 and (act.startTime == 0 or act.endTime == 1439):
                ownActsList.append(act)
            else:
                depActsList.append(act)
        return ownActsList, depActsList

    def clean_schedules_for_in_home_episodes(self, actType=101, inHomeActThreshold=1440):

        consequentInHomeActs = []
        lengthOfConseqActs = 0

        # print 'Original Acts List'
        # for i in self.listOfActivityEpisodes:
        #    print i

        newActsList = []

        for i in range(len(self.listOfActivityEpisodes)):
            startTime, act = hp.heappop(self.listOfActivityEpisodes)
            if act.actType == actType and lengthOfConseqActs < inHomeActThreshold:
                consequentInHomeActs.append(act)
                lengthOfConseqActs += act.duration
            else:
                if len(consequentInHomeActs) > 0:
                    newIHAct = self.createNewInHomeAct(consequentInHomeActs)
                    hp.heappush(newActsList, (newIHAct.startTime, newIHAct))

                if act.actType == actType:
                    consequentInHomeActs = [act]
                    lengthOfConseqActs = act.duration
                else:
                    hp.heappush(newActsList, (act.startTime, act))
                    consequentInHomeActs = []
                    lengthOfConseqActs = 0

        # print 'New Acts List'
        # for i in newActsList:
        #    print i

        self.listOfActivityEpisodes = newActsList

        #raw_input ('Inside aggregating acts')

    def createNewInHomeAct(self, consequentInHomeActs):
        #print ('\tAggregating all in-home acts between subsequent OH acts')
        minStartTime, maxEndTime = self.return_min_max_time_of_activities(
            consequentInHomeActs)

        act = copy.deepcopy(consequentInHomeActs[0])
        act.startTime = minStartTime
        act.endTime = maxEndTime

        return act

    def _check_for_conflicts(self):
        conflict = (self.scheduleConflictIndicator[:, :] > 1).sum()
        if conflict > 0:
            # print '\t\t\t\tTHERE ARE CONFLICTS IN THE SCHEDULE FOR PERSON - %s and CONFLICT - %s' %(self.pid,
            # conflict)
            return False
        return True

    def _check_for_acts_between_trip_vertices(self):

        tempList = []
        actListBetween = []

        actListCp = copy.deepcopy(self.listOfActivityEpisodes)

        actCount = len(self.listOfActivityEpisodes)
        i = 0
        stActSt, stAct = hp.heappop(actListCp)
        hp.heappush(tempList, (stActSt, stAct))

        for i in range(actCount - 1):
            enActSt, enAct = hp.heappop(actListCp)
            hp.heappush(tempList, (enActSt, enAct))

            if stAct.actType == 600 and enAct.actType <> 601:
                self.print_activity_list()
                raise Exception, "there are activities between trip vertices and this shouldn't happen"

    def _check_for_conflicts_with_activity(self, activity):
        if self._check_for_home_to_home_trips():
            # self.print_activity_list()
            # print '\tLooks like a home to home trip for hid - %s, pid - %s ? --------------------<<<<<<<<<<<<<<' %(self.hid, self.pid)
            # self.print_activity_list()
            return False

        if type(activity) == list:
            actList = activity
        else:
            actList = [activity]
        conflict = 0

        for activity in actList:
            stTime = activity.startTime
            endTime = activity.endTime

            conflictAct = (
                self.scheduleConflictIndicator[stTime:endTime, :] > 1).sum()
            # if conflictAct > 0:
            # print '\t\t\t', self.hid, self.pid, stTime, endTime
            # print '\t\t\t', activity
            conflict += conflictAct

        if conflict > 0:
            return False
        return True

    def _check_for_home_to_home_trips(self):
        # print 'checking for home to home trips'
        # self.print_activity_list()
        actCount = len(self.listOfActivityEpisodes)

        homeLoc = self.firstEpisode.location

        tempList = []

        i = 0
        stTime, stAct = hp.heappop(self.listOfActivityEpisodes)
        hp.heappush(tempList, (stTime, stAct))
        actCount -= 1

        homeToHomeTripFlag = False
        while (i < actCount):
            enStTime, enAct = hp.heappop(self.listOfActivityEpisodes)
            hp.heappush(tempList, (enStTime, enAct))

            # print '\t', stAct
            # print '\t', enAct
            # print '\t\t', (stAct.location == enAct.location and
            # stAct.location == homeLoc and stAct.actType == 600 and
            # enAct.actType == 600)

            if (stAct.location == enAct.location and stAct.location == homeLoc and stAct.actType == 600 and enAct.actType == 600):
                # print '\t\t\t\t\tHome to home trip added therefore conflict identified for person - ', self.pid
                # print '\t\t\t\t\t', stAct
                # print '\t\t\t\t\t', enAct

                homeToHomeTripFlag = True
            i += 1
            stTime = enStTime
            stAct = enAct
        self.listOfActivityEpisodes = tempList

        return homeToHomeTripFlag

    def parse_personids(self, tripDep):
        cpTripDep = copy.deepcopy(tripDep)
        modGrt100 = True
        pers = []
        while(modGrt100):
            cpTripDep, pid = divmod(cpTripDep, 100)
            # print cpTripDep, pid
            if pid <> 0 and cpTripDep > 0:
                pers.append(int(pid))
            if cpTripDep > 100:
                modGrt100 = True
            else:
                modGrt100 = False
        # print tripDep, pers
        if len(pers) > 1:
            # print '\t\tExciting picking up more than one
            # persoallocate_dependent_activitiesn ... '
            pass
        return pers

    def _check_for_ih_conflicts(self, activity, depPersonId):
        conflict = self._conflict_duration_with_activity(activity)

        self.remove_episodes([activity])

        conflictActs = self._identify_conflict_activities([activity])
        checkConflictActsLocation = self._check_location_match(activity,
                                                               conflictActs)

        if (conflict == activity.duration) and checkConflictActsLocation:
            # print """\t\t\t\tThere is some person at the current location """\
            #    """and the activities temporal vertices fit in with this person - %s""" %(self.pid)
            for act in conflictActs:
                # print 'conflictact - ', act
                if act.dependentPersonId == 0:
                    act.dependentPersonId = 100 + depPersonId
                else:
                    otherDepPids = self.parse_personids(act.dependentPersonId)
                    if depPersonId not in otherDepPids:
                        act.dependentPersonId = act.dependentPersonId * \
                            100. + depPersonId
                #act.dependentPersonId = 99
                # print 'conflictact after - ', act
                # print 'checking for in home conflicts', act

            return True
        else:
            return False

    def _check_location_match(self, activity, conflictActs):
        for act in conflictActs:
            if act.location <> activity.location:
                return False
            if act.actType >= 200:
                return False

        return True

    def _check_for_travel_threshold(self):
        pass

    def _check_for_roundtrip_threshold(self):
        pass

    def _conflict_duration(self):
        conflict = (self.scheduleConflictIndicator[:, :] > 1).sum()
        return conflict

    def _conflict_duration_with_activity(self, activity):
        stTime = activity.startTime
        endTime = activity.endTime
        # print 'stTime - ', stTime, 'endTime', endTime
        conflict = (
            self.scheduleConflictIndicator[stTime:endTime, :] > 1).sum()
        return conflict

    def _identify_next_activity(self, activity, count=1):
        # conflict wrt one activity

        actCount = len(self.listOfActivityEpisodes)

        actList = []
        tempList = []

        # print 'Length before - ', len(self.listOfActivityEpisodes)

        i = 0
        while (i < actCount):
            # print 'i value', i
            actSt, act = hp.heappop(self.listOfActivityEpisodes)
            hp.heappush(tempList, (actSt, act))

            if (act.startTime >= activity.startTime and act.endTime <= activity.endTime):

                # print '\nNext TWO----------'
                for k in range(count):
                    try:
                        nextActSt, nextAct = hp.heappop(
                            self.listOfActivityEpisodes)
                        # print nextAct
                        if nextAct.startTime >= activity.endTime:
                            actList.append(nextAct)
                        hp.heappush(tempList, (nextActSt, nextAct))
                    except IndexError, e:
                        # print 'Cannot identify %s number of activities
                        # returned as many as possible...' %count
                        self.listOfActivityEpisodes = tempList
                        return actList
                # print '--------ABOVE TWO'
                i = i + count
                # print 'i value updated -', i
            i += 1
        self.listOfActivityEpisodes = tempList
        # print 'Length after - ', len(self.listOfActivityEpisodes)
        return actList

    def _identify_previous_activity(self, activity, count=1):
        # conflict wrt one activity

        actList = []
        tempList = []
        tempPrevList = []

        # print 'Length before - ', len(self.listOfActivityEpisodes)
        actCount = len(self.listOfActivityEpisodes)
        i = 0
        for i in range(actCount):
            actSt, act = hp.heappop(self.listOfActivityEpisodes)
            hp.heappush(tempList, (actSt, act))

            if (act.startTime >= activity.startTime and act.endTime <= activity.endTime):
                pass
            elif act.startTime < activity.startTime:
                tempPrevList.append(act)

        self.listOfActivityEpisodes = tempList
        # print 'Length after - ', len(self.listOfActivityEpisodes)
        return tempPrevList[-count:]

    def _identify_match_activities(self, activityList):
        # matches with respect to a list of activities including chains

        actMatches = []
        for act in activityList:
            # print 'Checking Matches for act - ', act
            actMatch = self._identify_match_activity(act)

            if actMatch is not None:
                for newMatchAct in actMatch:
                    if newMatchAct not in actMatches:
                        actMatches.append(newMatchAct)

        #actMatches = self.sort_acts(actMatches)
        return actMatches

    def _identify_match_activity(self, activity):
        # match wrt one activity
        for stAct, act in self.listOfActivityEpisodes:

            # perfectly in line or within
            if (act.startTime == activity.startTime and act.endTime == activity.endTime):
                return [act]

    def _identify_activities_between_time_boundaries(self, start, end):
        # print 'boundaries ... ', start, end
        # print self.print_activity_list()
        actList = []
        for stAct, act in self.listOfActivityEpisodes:
            # print 'for act - ', act, 'condition is - ', act.startTime >=
            # start and act.endTime <= end
            if act.startTime >= start and act.endTime <= end:
                actList.append(act)
        return actList

    def _identify_conflict_activities(self, activityList):
        # conflict with respect to a list of activities including chains

        actConflicts = []
        for act in activityList:
            # print 'Checking conflicts for act - ', act
            actConflict = self._identify_conflict_activity(act)

            if actConflict is not None:
                for newConfAct in actConflict:
                    if newConfAct not in actConflicts:
                        actConflicts.append(newConfAct)

        #actConflicts = self.sort_acts(actConflicts)
        return actConflicts

    def _identify_conflict_activity(self, activity):
        # conflict wrt one activity
        actList = []
        for stAct, act in self.listOfActivityEpisodes:
            # print len(self.listOfActivityEpisodes)
            # print '\t\tACTIVITY COORDINATES', activity.startTime, activity.endTime
            # print '\t\tCONFLICT COORDINATES', act.startTime, act.endTime

            if ((act.startTime >= activity.startTime and act.endTime <= activity.endTime)  # perfectly in line or within
                    or
                    # if it just grazes it is not a conflict?
                    (activity.startTime >
                     act.startTime and activity.startTime < act.endTime)
                    or
                    # if it just grazes it is not a conflict?
                    (activity.endTime >
                     act.startTime and activity.endTime < act.endTime)
                    or
                    (act.startTime < activity.startTime and act.endTime > activity.endTime)):
                actList.append(act)
                # print '\tchecking against', act,
                # print 'this is it --<'
        return actList

    def pop_earliest_activity(self):
        self.actCount -= 1
        activityStart, activity = hp.heappop(self.listOfActivityEpisodes)
        self.scheduleIds.remove(activity.scheduleId)
        return activityStart, activity

    def check_start_of_day(self, refEndTime, depPersonId):
        # print 'First episode end - %s for pid - %s and ref - %s'
        # %(self.firstEpisode.endTime, self.pid, refEndTime),
        # self.firstEpisode.endTime >= refEndTime
        if self.firstEpisode.endTime >= refEndTime:
            # if self.firstEpisode.dependentPersonId == 0:
            #    self.firstEpisode.dependentPersonId = depPersonId
            if self.firstEpisode.dependentPersonId == 0:
                self.firstEpisode.dependentPersonId = 100 + depPersonId
            else:
                self.firstEpisode.dependentPersonId = 100. * \
                    self.firstEpisode.dependentPersonId + depPersonId
            #self.firstEpisode.dependentPersonId = 99
            return True
        else:
            return False

    def check_end_of_day(self, refStartTime, depPersonId):
        # print 'Checking end of day for person - ', self.pid
        # print 'Pid - ', self.pid, 'Last Episode starttime - ', self.lastEpisode, self.lastEpisode.startTime
        # print 'Ref starttime - ', refStartTime
        if self.lastEpisode.startTime <= refStartTime:
            # if self.lastEpisode.dependentPersonId == 0:
            #    self.lastEpisode.dependentPersonId = depPersonId
            # print 'dep person id before - ',
            # self.lastEpisode.dependentPersonId
            if self.lastEpisode.dependentPersonId == 0:
                self.lastEpisode.dependentPersonId = 100 + depPersonId
            else:
                self.lastEpisode.dependentPersonId = 100. * \
                    self.lastEpisode.dependentPersonId + depPersonId
            # print '-- dep person id after - ', self.lastEpisode.dependentPersonId
            #self.lastEpisode.dependentPersonId = 99
            return True
        else:
            return False

    def move_start_end(self, act, moveByValue, removeAdd=True):
        # print '\tRemoving episode - ', act
        if removeAdd:
            self.remove_episodes([act])
        act.startTime += moveByValue + 1
        act.endTime += moveByValue + 1
        # print '\tAdding episode - ', act
        if removeAdd:
            self.add_episodes([act])

    def move_start_end_by_diff_values(self, act, stValue, endValue, removeAdd=True):
        if removeAdd:
            self.remove_episodes([act])
        act.startTime = stValue
        act.endTime = endValue
        act.duration = act.endTime - act.startTime
        if act.duration < 0:
            raise Exception, 'Incorrect adjustment - %s' % act
        if removeAdd:
            self.add_episodes([act])

    def move_start(self, act, value, removeAdd=True):
        # self.print_activity_list()
        if removeAdd:
            self.remove_episodes([act])
        act.startTime = value
        act.duration = act.endTime - act.startTime
        if act.duration < 0:
            raise Exception, 'Incorrect adjustment - %s' % act
        if removeAdd:
            self.add_episodes([act])

        # self.print_activity_list()

    def move_end(self, act, value, removeAdd=True):
        # print 'before logic 3 - ', self.print_activity_list()
        if removeAdd:
            self.remove_episodes([act])
        # print 'after removing episode logic 3 - ', self.print_activity_list()
        act.endTime = value
        act.duration = act.endTime - act.startTime
        if act.duration < 0:
            raise Exception, 'Incorrect adjustment - %s' % act
        if removeAdd:
            self.add_episodes([act])

        # print 'after logic 3 - ', self.print_activity_list()

    def move_start_of_day(self, refEndTime, depPersonId, dependent=False):
        self.remove_episodes([self.firstEpisode])
        self.firstEpisode.endTime = refEndTime
        self.firstEpisode.duration = (self.firstEpisode.endTime -
                                      self.firstEpisode.startTime)

        if not dependent:
            self.firstEpisode.dependentPersonId = 100 + depPersonId
        else:
            self.firstEpisode.dependentPersonId = depPersonId
        self.add_episodes([self.firstEpisode])

    def move_end_of_day(self, refStartTime, depPersonId, dependent=False):
        self.remove_episodes([self.lastEpisode])
        self.lastEpisode.startTime = refStartTime
        self.lastEpisode.duration = (self.lastEpisode.endTime -
                                     self.lastEpisode.startTime)

        if not dependent:
            self.lastEpisode.dependentPersonId = 100 + depPersonId
        else:
            self.lastEpisode.dependentPersonId = depPersonId

        self.add_episodes([self.lastEpisode])

    def add_status_dependency(self, workstatus, schoolstatus, child_dependency):
        self.workstatus = workstatus
        self.schoolstatus = schoolstatus
        self.child_dependency = child_dependency

    def add_arrival_status(self, actualArrival, expectedArrival, tripDependentPerson=None):
        self.actualArrival = actualArrival
        self.expectedArrival = expectedArrival
        self.tripDependentPerson = tripDependentPerson
        if self.actualArrival > 0 and self.expectedArrival > 0:
            # print 'before extracting destination episode -'
            # self.print_activity_list()
            self.extract_destination_episode()
            # print 'after extracting destination episode but before identifying actual and expected -'
            # self.print_activity_list()
            # self.reset_activity_heap()
            self.identify_actual_expected_activities(arrival=True)
            # print 'after extracting destination episode and identifying actual and expected -'
            # self.print_activity_list()

    def add_occupancy_status(self, tripIndicator, tripStTime):
        self.tripIndicator = tripIndicator
        self.tripStTime = tripStTime

        if self.tripIndicator == -1:
            self.extract_start_episode()
            self.identify_actual_expected_activities(waiting=True)

    def extract_start_episode(self):
        stAct = None
        stActList = self._identify_conflict_with_endtime(self.tripStTime)

        # print 'Start time of trip - ', self.tripStTime

        if len(stActList) == 0:
            # self.print_activity_list()
            # print '\tNo start activity found for this trip'
            pass

        elif len(stActList) > 1:
            self.print_activity_list()
            raise Exception, '\tThis should not happen how can there be two activities with same end time'

        else:
            stAct = stActList[0]

        self.stAct = stAct

    def extract_destination_episode(self):
        """
        for startTime, destAct in self.listOfActivityEpisodes:
            if destAct.startTime == self.expectedArrival:
                break
        """
        destAct = None
        destActList = self._identify_conflict_with_arrival(
            self.expectedArrival)

        # print '\texpected arrival - ', self.expectedArrival
        if len(destActList) == 0:
            # self.print_activity_list()
            # print '\t     No dest act found for this arrival'
            pass
        elif len(destActList) > 1:
            self.print_activity_list()
            print '\t     More than one conflicts found for this arrival'
            for i in destActList:
                print '\t\tdest Act with conflict arrival - ', i
        else:
            destAct = destActList[0]

        self.destAct = destAct

    def _identify_conflict_with_arrival(self, arrivalTime):
        actList = []
        for stAct, act in self.listOfActivityEpisodes:
            # encases the arrivalTime
            if (act.startTime == arrivalTime and arrivalTime <= act.endTime):
                actList.append(act)
        return actList

    def _identify_conflict_with_endtime(self, endTime):
        actList = []
        for stAct, act in self.listOfActivityEpisodes:
            if (act.endTime == endTime):  # encases the arrivalTime
                actList.append(act)
        return actList

    def identify_actual_expected_activities(self, arrival=None, waiting=None):
        # print 'Activities after expected arrival of %s - ' %(self.expectedArrival)
        #tempActList = copy.deepcopy(self.listOfActivityEpisodes)

        self.expectedActivities = []
        self.actualActivities = []

        if arrival == True:
            refExpTime = self.expectedArrival
            refActTime = self.actualArrival

        if waiting == True:
            refExpTime = self.tripStTime
            refActTime = self.tripStTime

        tempActList = []
        for actIndex in range(len(self.listOfActivityEpisodes)):
            startTime, act = hp.heappop(self.listOfActivityEpisodes)
            if act.startTime >= refExpTime:
                self.expectedActivities.append(act)

            if act.startTime >= refActTime:
                self.actualActivities.append(act)

            hp.heappush(tempActList, (startTime, act))

        self.listOfActivityEpisodes = tempActList

        """

        tempActList = []
        for actIndex in range(len(self.listOfActivityEpisodes)):
            startTime, act = hp.heappop(self.listOfActivityEpisodes)
            if act.startTime >= refExpTime:
                self.expectedActivities.append(act)
                #print '\t', act
            hp.heappush(tempActList, (startTime, act))

        self.listOfActivityEpisodes = tempActList
        tempActList = []
        #print 'Activities after actual arrival of %s - ' %(self.actualArrival)
        #tempActList = copy.deepcopy(self.listOfActivityEpisodes)
        for actIndex in range(len(self.listOfActivityEpisodes)):
            startTime, act = hp.heappop(self.listOfActivityEpisodes)
            if act.startTime >= refActTime:
                self.actualActivities.append(act)
                #print '\t', act
            hp.heappush(tempActList, (startTime, act))
        self.listOfActivityEpisodes = tempActList
        #self.destAct = copy.deepcopy(destAct)
        """

    def extract_work_episodes(self):
        for startTime, act in self.listOfActivityEpisodes:
            if act.actType > 199 and act.actType < 300:
                self.workEpisodes.append(act)

    def extract_school_episodes(self):
        for startTime, act in self.listOfActivityEpisodes:
            if act.actType > 299 and act.actType < 400:
                self.schoolEpisodes.append(act)

    def _reconcile_schedule(self):
        # print len(self.listOfActivityEpisodes), len(self.reconciledActivityEpisodes)
        #stAct = hp.heappop(self.listOfActivityEpisodes)[1]
        stAct = self._return_start_activity()

        while (len(self.listOfActivityEpisodes) > 0):

            endAct = hp.heappop(self.listOfActivityEpisodes)[1]
            # If the second activity is identified as end of the day vertex,
            # then we move its location in the heap to end so that the adjustment
            # for this activity happens at the end after all other activities have been
            # reconciled
            # print len(self.listOfActivityEpisodes), len(self.reconciledActivityEpisodes)
            # print '\tFIRST ACT OF PRISM - ', stAct
            # print '\tLAST ACT OF PRISM -  ', endAct

            if endAct.endTime == 1439 and len(self.listOfActivityEpisodes) > 0:
                hp.heappush(self.listOfActivityEpisodes, (1439, endAct))
                continue

            # If there are subsequent activities with a start time of 0 then we need to
            # move it and not process it as a start of day reconciliation
            if endAct.startTime == 0 and len(self.listOfActivityEpisodes) > 0:
                endAct.startOfDay = False

            # First act
            if stAct.startOfDay == True:
                stAct = self._adjust_first_episode(stAct, endAct)
                continue

            # Last act
            if endAct.endOfDay == True:
                stAct = self._adjust_last_episode(stAct, endAct)
                continue

            # intermediate acts
            intAct = self._move_episode(stAct, endAct)
            if intAct.endTime > 1439:
                #print("cannot be adjusted within the day for person with hid = %s and pid = %s" %(self.hid, self.pid))
                pass
            else:
                stAct = intAct

            # print '\tMOVED EPISODE -', stAct

            # print 'RECONCILED SCHEDULES', self.reconciledActivityEpisodes

        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))

    def _return_start_activity(self):
        stActFound = False

        while (not stActFound):
            act = hp.heappop(self.listOfActivityEpisodes)[1]

            if act.startTime == 0:
                stActFound = True
            else:
                if act.startTime == 0:
                    hp.heappush(self.listOfActivityEpisodes, (1, act))
                else:
                    hp.heappush(
                        self.listOfActivityEpisodes, (act.startTime, act))

        return act

    def _collate_results(self):
        # print self.listOfActivityEpisodes
        # print self.reconciledActivityEpisodes
        resList = []
        for recAct in self.listOfActivityEpisodes:
            actObject = recAct[1]
            resList.append([actObject.scheduleId,
                            actObject.actType, actObject.startTime, actObject.endTime,
                            actObject.location, actObject.duration])
        return array(resList)

    def _collate_results_aslist(self):
        # print self.listOfActivityEpisodes
        # print self.reconciledActivityEpisodes
        # print 'Length before collaing results - ',
        # len(self.listOfActivityEpisodes)
        resList = []
        for recAct in self.listOfActivityEpisodes:
            actObject = recAct[1]
            resList.append([self.hid, self.pid, actObject.scheduleId,
                            actObject.actType, actObject.startTime, actObject.endTime,
                            actObject.location, actObject.duration, actObject.dependentPersonId,
                            actObject.tripCount])
        return resList

    def _adjust_first_episode(self, stAct, endAct):
        tt = self._extract_travel_time(stAct.location, endAct.location)
        prismDur = endAct.startTime - stAct.endTime

        #adjDenominator = stAct.duration + 0.5*endAct.duration
        adjDenominator = stAct.duration

        if prismDur > tt:
            pass
        else:
            # print '\t\t-- ADJUSTING FOR FIRST PRISM OF DAY --'

            adjDur = tt - prismDur

            # Modify end of the Starting Activity for the prism
            stAct_EndAdj = adjDur * stAct.duration / adjDenominator
            stAct.endTime = stAct.endTime - stAct_EndAdj
            # Update duration
            stAct.duration = stAct.endTime - stAct.startTime

            # Modify start of the Ending Activity for the prism
            """
            endAct_StAdj = adjDur * 0.5*endAct.duration/adjDenominator
            endAct.startTime = endAct.startTime + endAct_StAdj
            # Modify end of the Ending Activity for the prism
            rndNum = self.rndGen.return_random_variables()
            endAct_EndAdj = rndNum * 0.5 * endAct_StAdj
            endAct.endTime = endAct.endTime + endAct_EndAdj

            if endAct.endTime > 1439:
                endAct.endTime = 1439
            #Update duration
            endAct.duration = endAct.endTime - endAct.startTime
            """

        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))
        return endAct

    def _adjust_episode(self, stAct, endAct):
        tt = self._extract_travel_time(stAct.location, endAct.location)
        prismDur = endAct.startTime - stAct.endTime

        adjDenominator = 0.5 * stAct.duration + 0.5 * endAct.duration + tt

        if prismDur > tt:
            pass
        else:
            # print '\t\t-- ADJUSTING FOR ACTIVITIES WITHIN A DAY --'

            adjDur = tt - prismDur

            # Modify end of the Starting Activity for the prism
            stAct_EndAdj = adjDur * 0.5 * stAct.duration / adjDenominator
            stAct.endTime = stAct.endTime - stAct_EndAdj
            # Update duration
            stAct.duration = stAct.endTime - stAct.startTime

            # Modify start of the Ending Activity for the prism
            endAct_StAdj = adjDur * 0.5 * endAct.duration / adjDenominator
            endAct.startTime = endAct.startTime + endAct_StAdj
            # Modify end of the Ending Activity for the prism
            rndNum = self.rndGen.return_random_variables()
            endAct_EndAdj = rndNum * 0.5 * endAct_StAdj
            endAct.endTime = endAct.endTime + endAct_EndAdj

            if endAct.endTime > 1439:
                endAct.endTime = 1439
            # Update duration
            endAct.duration = endAct.endTime - endAct.startTime

        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))
        return endAct

    def _move_episode(self, stAct, endAct):
        tt = self._extract_travel_time(stAct.location, endAct.location)
        prismDur = endAct.startTime - stAct.endTime

        if prismDur > tt:
            hp.heappush(
                self.reconciledActivityEpisodes, (stAct.startTime, stAct))
            pass
        else:
            # print "\t\t-- MOVING WITHIN DAY FIXED ACTIVITY --"

            adjDur = tt - prismDur

            # Modify start of the Ending Activity for the prism
            endAct.startTime = endAct.startTime + adjDur
            # Modify end of the Ending Activity for the prism
            rndNum = self.rndGen.return_random_variables()
            endAct_EndAdj = rndNum * 0.5 * adjDur
            endAct.endTime = endAct.endTime + endAct_EndAdj

            # If the adjusted endtime is less than the adjusted starttime
            if endAct.endTime < endAct.startTime:
                rndNum = self.rndGen.return_random_variables()
                endAct.endTime = endAct.startTime + rndNum * endAct.duration

            if endAct.endTime > 1439:
                if endAct.startTime < 1438:
                    endAct.endTime = 1438

                if endAct.startTime > 1438:
                    endAct.startTime = 1438
                    endAct.endTime = 1438
            endAct.duration = endAct.endTime - endAct.startTime
            hp.heappush(
                self.reconciledActivityEpisodes, (stAct.startTime, stAct))

            """

            if (endAct.endTime > 1439 and endAct.startTime < 1438) or (endAct.endTime < 1439):
                # i.e even by limiting the endtime we are doing OK because the starttime is still < 1438
                # in the other case where starttime >= 1438 we try to leave out the activity since it
                # cannot be accommodated within the schedule

                endAct.endTime = 1438
                #print("endtime less than starttime random * duration being added")
                hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))

            """
            # Update duration

        return endAct

    def _adjust_last_episode(self, stAct, endAct):
        tt = self._extract_travel_time(stAct.location, endAct.location)
        prismDur = endAct.startTime - stAct.endTime

        #adjDenominator = 0.5*stAct.duration + endAct.duration
        adjDenominator = endAct.duration

        if prismDur > tt:
            pass
        else:
            # print "\t\t-- ADJUSTING FOR LAST PRISM OF DAY --"
            adjDur = tt - prismDur

            """
            # Modify end of the Starting Activity for the prism
            stAct_EndAdj = adjDur * 0.5*stAct.duration/adjDenominator
            stAct.endTime = stAct.endTime - stAct_EndAdj
            #Update duration
            stAct.duration = stAct.endTime - stAct.startTime
            """

            # Modify start of the Ending Activity for the prism
            endAct_StAdj = adjDur * endAct.duration / adjDenominator
            endAct.startTime = endAct.startTime + endAct_StAdj
            # Update duration
            endAct.duration = endAct.endTime - endAct.startTime

        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))
        return endAct

    def adjust_activity_schedules(self, seed=1):
        self.reconciledActivityEpisodes = []
        self.seed = seed
        self.rndGen = RandomDistribution(int(self.hid * self.pid))
        self._adjust_schedule()
        self.listOfActivityEpisodes = copy.deepcopy(
            self.reconciledActivityEpisodes)

    def _adjust_schedule(self):
        stAct = self._return_start_activity()

        while (len(self.listOfActivityEpisodes) > 0):

            endAct = hp.heappop(self.listOfActivityEpisodes)[1]
            # If the second activity is identified as end of the day vertex,
            # then we move its location in the heap to end so that the adjustment
            # for this activity happens at the end after all other activities have been
            # reconciled
            # print '\tFIRST ACT OF PRISM - ', stAct
            # print '\tLAST ACT OF PRISM -  ', endAct

            if endAct.endTime == 1439 and len(self.listOfActivityEpisodes) > 0:
                hp.heappush(self.listOfActivityEpisodes, (1439, endAct))
                continue

            # If there are subsequent activities with a start time of 0 then we need to
            # move it and not process it as a start of day reconciliation
            if endAct.startTime == 0 and len(self.listOfActivityEpisodes) > 0:
                endAct.startOfDay = False

            # First act
            if stAct.startOfDay == True:
                stAct = self._adjust_first_episode(stAct, endAct)
                continue

            # Last act
            if endAct.endOfDay == True:
                stAct = self._adjust_last_episode(stAct, endAct)
                continue

            # intermediate acts
            stAct = self._adjust_episode(stAct, endAct)
            # print '\tADJUSTEDD EPISODE -', stAct

        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))

    def _extract_travel_time(self, st_loc, end_loc):
        # Currently assume that the travel time between any two
        # activity episodes that are not same is 30 mins
        # TODO: Needs to be replaced with querying the travel skims
        if st_loc == end_loc:
            tt = 1
        tt = 1
        return tt
