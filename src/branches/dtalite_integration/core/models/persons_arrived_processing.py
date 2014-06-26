import copy

from numpy import array, logical_and, histogram, zeros, amax, unique


from openamos.core.models.abstract_model import Model
from openamos.core.data_array import DataArray


class PersonsArrivedProcessing(Model):

    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification

        self.idSpec = specification.idSpec
        self.persArrivedAttribSpec = specification.persArrivedAttribSpec

    def create_col_numbers(self, colnamesDict):
        # print colnamesDict
        self.hidCol = colnamesDict[self.idSpec.hidName]
        self.pidCol = colnamesDict[self.idSpec.pidName]

        self.persArrivedCol = colnamesDict[
            self.persArrivedAttribSpec.tripDepName]
        self.persTripCountCol = colnamesDict[
            self.persArrivedAttribSpec.tripCountName]
        if self.persArrivedAttribSpec.endTripCountName is not None:
            self.endTripCountCol = colnamesDict[
                self.persArrivedAttribSpec.endTripCountName]
        else:
            self.endTripCountCol = None
        self.actDepCol = colnamesDict[self.persArrivedAttribSpec.actDepName]

    def resolve_consistency(self, data, seed):
        self.create_col_numbers(data._colnames)

        #raw_input('processing arrived persons and num rows - %s' %data.rows)

        # print '--------------------------------------------'
        newData = []
        for rowId in range(data.rows):
            row = data.data[rowId, :]
            hid = row[self.hidCol]
            pid = row[self.pidCol]

            # print 'For hid - %s and pid - %s' %(hid, pid)

            persArrived = row[self.persArrivedCol]
            # print '     There are other dependent persons on the trip - ',
            # persArrived
            tripCount = row[self.persTripCountCol]
            # print '     Trip count on the trip - ', tripCount
            actDep = row[self.actDepCol]
            # print '     Act dep for the trip - ', actDep

            if self.endTripCountCol is not None:
                endTripCount = row[self.endTripCountCol]
                if endTripCount < 100:
                    endTripCount = 100 + endTripCount
                parsedDropOffTripCount = self.parse_personids(endTripCount)
                parsedDropOffs = self.parse_personids(actDep)
                # print '     Trip count on the trip - ', endTripCount
            else:
                parsedDropOffs = []
                parsedDropOffTripCount = []

        # TODO: What ishappening here?

            if persArrived <= 100:
                newData.append(list(row))
                continue

            newData.append(list(row))

            parsedPersonIds = self.parse_personids(persArrived)
            # print '     Parsed dependent persons on the trip - ',
            # parsedPersonIds

            parsedTripCount = self.parse_personids(tripCount)
            # print '     Parsed trip count on the trip - ', parsedTripCount

            # print '     Parsed end act dependents - ', parsedDropOffs
            # print '     Parsed end dropoff trip count - ',
            # parsedDropOffTripCount

        # TODO: What happens when this condition is not satisfied ...?
            if tripCount > 100:

                i = 0
                for pid in parsedPersonIds:
                    rowCp = copy.deepcopy(row)
                    rowCp[self.pidCol] = pid
                    if pid in parsedDropOffs:
                        index = parsedDropOffs.index(pid)
                        rowCp[self.persTripCountCol] = parsedDropOffTripCount[
                            index]
                    elif self.endTripCountCol is not None:
                        # print 'this persons count is being reduced ... '
                        rowCp[self.persTripCountCol] = parsedTripCount[i] - 1
                        # print rowCp
                    else:
                        rowCp[self.persTripCountCol] = parsedTripCount[i]
                    newData.append(list(rowCp))
                    i += 1

                parsedPersonIds = list(
                    set(parsedPersonIds) - set(parsedPersonIds))
                # print 'left over persons - ', parsedPersonIds

                # raw_input()

            """
	    for pid in parsedPersonIds:
		rowCp = copy.deepcopy(row)
		rowCp[self.pidCol] = pid
		# if the pid on the trip is not getting off at the end do not change his trip count
		if pid not in parsedDropOffs:
		    rowCp[self.persTripCountCol] = -999
		newData.append(list(rowCp))
	    """
        data = DataArray(newData, data.varnames)

        # print data.varnames
        # print data.data.astype(int)

        #raw_input('arrived persons processing complete ---  and rows - %s' %data.rows)
        #print ('arrived persons processing complete ---  and rows - %s' %data.rows)

        return data

    def parse_personids(self, tripDep):
        cpTripDep = copy.deepcopy(tripDep)
        modGrt100 = True
        pers = []
        while(modGrt100):
            cpTripDep, pid = divmod(cpTripDep, 100)
            # print cpTripDep, pid
            if (pid > 0 and pid < 99) and cpTripDep > 0:
                pers.append(pid)
            if cpTripDep > 100:
                modGrt100 = True
            else:
                modGrt100 = False
        # print tripDep, pers
        # if len(pers) > 1:
        #    print 'Exciting picking up more than one person ... '
        return pers
