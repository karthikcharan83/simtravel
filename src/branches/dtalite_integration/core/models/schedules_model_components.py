

class ReconcileSchedulesSpecification(object):

    def __init__(self, activityAttribs):
        self.activityAttribs = activityAttribs

        self.choices = None
        self.coefficients = None


class HouseholdSpecification(object):

    def __init__(self, activityAttribs, dailyStatusAttribs=None,
                 dependencyAttribs=None, arrivalInfoAttribs=None,
                 terminalEpisodesAllocation=False,
                 childDepProcessingType="Allocation",
                 occupancyInfoAttribs=False):
        self.childDepProcessingType = childDepProcessingType
        self.activityAttribs = activityAttribs
        self.dailyStatusAttribs = dailyStatusAttribs
        self.dependencyAttribs = dependencyAttribs
        self.arrivalInfoAttribs = arrivalInfoAttribs
        self.occupancyInfoAttribs = occupancyInfoAttribs

        self.terminalEpisodesAllocation = terminalEpisodesAllocation

        if self.arrivalInfoAttribs == None:
            self.schedAdjType = "Occupancy Adjustment"

        if self.occupancyInfoAttribs == None:
            self.schedAdjType = "Arrival Adjustment"

        self.choices = None
        self.coefficients = None


class ActivityAttribsSpecification(object):

    def __init__(self, hidName, pidName, scheduleidName,
                 activitytypeName, starttimeName,
                 endtimeName, locationidName,
                 durationName, dependentPersonName, tripCountName):
        self.hidName = hidName
        self.pidName = pidName
        self.scheduleidName = scheduleidName
        self.activitytypeName = activitytypeName
        self.locationidName = locationidName
        self.starttimeName = starttimeName
        self.endtimeName = endtimeName
        self.durationName = durationName
        self.dependentPersonName = dependentPersonName
        self.tripCountName = tripCountName


class ArrivalInfoSpecification(object):

    def __init__(self, dependentPersonName,
                 actualArrivalName, expectedArrivalName):
        self.dependentPersonName = dependentPersonName
        self.actualArrivalName = actualArrivalName
        self.expectedArrivalName = expectedArrivalName


class OccupancyInfoSpecification(object):

    def __init__(self, tripIndicatorName, startTimeName):
        self.tripIndicatorName = tripIndicatorName
        self.startTimeName = startTimeName


class DailyStatusAttribsSpecification(object):

    def __init__(self, workStatusName, schoolStatusName):
        self.workStatusName = workStatusName
        self.schoolStatusName = schoolStatusName


class DependencyAttribsSpecification(object):

    def __init__(self, childDependencyName, elderlyDependencyName=None):
        self.childDependencyName = childDependencyName
        self.elderlyDependencyName = elderlyDependencyName


class TripOccupantSpecification(object):

    def __init__(self,
                 idSpec,
                 tripDepAttribSpec):
        self.idSpec = idSpec
        self.tripDepAttribSpec = tripDepAttribSpec

        self.choices = None
        self.coefficients = None


class PersonsArrivedSpecification(object):

    def __init__(self,
                 idSpec,
                 persArrivedAttribSpec):
        self.idSpec = idSpec
        self.persArrivedAttribSpec = persArrivedAttribSpec

        self.choices = None
        self.coefficients = None


class PersonsArrivedAttributes(object):

    def __init__(self, tripDepName, tripCountName=None, endTripCountName=None, actDepName=None):
        self.tripDepName = tripDepName
        self.tripCountName = tripCountName
        self.endTripCountName = endTripCountName
        self.actDepName = actDepName


class TripDependentPersonAttributes(object):

    def __init__(self,
                 tripPurposeFromName,
                 tripDepName,
                 lastTripDepName,
                 stActDepName,
                 enActDepName,
                 personOnNetworkName,
                 tripCountName,
                 lastTripCountName,
                 stActTripCountName,
                 enActTripCountName):
        self.tripPpurposeFromName = tripPurposeFromName
        self.tripDepName = tripDepName
        self.lastTripDepName = lastTripDepName
        self.stActDepName = stActDepName
        self.enActDepName = enActDepName
        self.personOnNetworkName = personOnNetworkName
        self.tripCountName = tripCountName
        self.stActTripCountName = stActTripCountName
        self.enActTripCountName = enActTripCountName
        self.lastTripCountName = lastTripCountName


class UniqueRecordsSpecification(object):

    def __init__(self, uniqueRecordsColName):
        self.uniqueRecordsColName = uniqueRecordsColName

        self.choices = None
        self.coefficients = None
