import copy

from numpy import array, logical_and, histogram, zeros, amax, unique


from openamos.core.models.abstract_model import Model
from openamos.core.data_array import DataArray



class TripOccupantProcessing(Model):
    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification

        self.idSpec = specification.idSpec
        self.tripDepAttribSpec = specification.tripDepAttribSpec



    def create_col_numbers(self, colnamesDict):
        #print colnamesDict
        self.hidCol = colnamesDict[self.idSpec.hidName]
        self.pidCol = colnamesDict[self.idSpec.pidName]

        self.tripPurposeFromNameCol = colnamesDict[self.tripDepAttribSpec.tripPpurposeFromName]
        self.tripDepNameCol = colnamesDict[self.tripDepAttribSpec.tripDepName]
        self.lastTripDepNameCol = colnamesDict[self.tripDepAttribSpec.lastTripDepName]
        self.stActDepNameCol = colnamesDict[self.tripDepAttribSpec.stActDepName]
        self.enActDepNameCol = colnamesDict[self.tripDepAttribSpec.enActDepName]
        self.personOnNetworkNameCol = colnamesDict[self.tripDepAttribSpec.personOnNetworkName]
        self.tripCountCol = colnamesDict[self.tripDepAttribSpec.tripCountName]

        self.stActTripCountCol = colnamesDict[self.tripDepAttribSpec.stActTripCountName]
        self.enActTripCountCol = colnamesDict[self.tripDepAttribSpec.enActTripCountName]
        self.lastTripCountCol = colnamesDict[self.tripDepAttribSpec.lastTripCountName]

    def resolve_consistency(self, data, seed):
        self.create_col_numbers(data._colnames)

        #print '--------------------------------------------'
        for rowId in range(data.rows):
            row = data.data[rowId,:]
            hid = row[self.hidCol]
            pid = row[self.pidCol]
            tripPurposeFrom = row[self.tripPurposeFromNameCol]
            lastTripDep = row[self.lastTripDepNameCol]
            stActDep = row[self.stActDepNameCol]
            enActDep = row[self.enActDepNameCol]

            tripCount = row[self.tripCountCol]
            lastTripCount = row[self.lastTripCountCol]
            stActTripCount = row[self.stActTripCountCol]
            enActTripCount = row[self.enActTripCountCol]

            #print 'For hid - %s and pid - %s' %(hid, pid)
            #print '     The trip purpose from is - ', tripPurposeFrom
            #print '     StTripCount Col - ', stActTripCount
            #print '     EnTripCount Col - ', enActTripCount
            #print '     LastTripCount Col - ', lastTripCount

            if self.personOnNetworkNameCol <> None:
                self.personOnNetwork = row[self.personOnNetworkNameCol]
                # THIS IS LIKE AN OVERRIDE FOR PROCESSING OCCUPANCY WHEN THE PERSON IS STILL ON THE NETWORK FOR THE DYNAMIC CASE
                if self.personOnNetwork == 1:
                    #print '\ta.3. Person is still on the network therefore the trip dependent person is set to the old occupancy - ', lastTripDep
                    tripDepPers = lastTripDep
                    data.data[rowId, self.tripDepNameCol] = tripDepPers
                    tripCountDepPers = lastTripCount
                    data.data[rowId, self.tripCountCol] = tripCountDepPers
                    continue

            if tripPurposeFrom == 600 or tripPurposeFrom == 601:
                if stActDep > 100:
                    #print '\ta.2. The occupancy of the trip changed and processing occupancy now ... stActDep - %s' %stActDep
                    tripDepPers, tripCountDepPers = self.parse_trip_dependentpersonid_count(hid, pid,
                                                                                            lastTripDep, stActDep,
                                                                                            lastTripCount, stActTripCount,
                                                                                            tripPurposeFrom)
                    #print '\t-->New dependentperson - %s<--' %tripDepPers, type(tripDepPers)
                    #print '\t-->New tripcount dep pers - %s' %tripCountDepPers

                else:
                    #print '\ta.2. No need to process occupancy this is a dependent person ... stActDep - %s' %stActDep
                    tripDepPers = stActDep
                    tripCountDepPers = stActTripCount
            else:
                #print '\ta.1. The occupancy of the trip did not change and occupancy is - ', lastTripDep
                tripDepPers = lastTripDep
                tripCountDepPers = lastTripCount

            data.data[rowId, self.tripDepNameCol] = tripDepPers
            data.data[rowId, self.tripCountCol] = tripCountDepPers
        #raw_input('trip occupant processing')
        #print ('trip occupant processing')
        return data

    def parse_trip_dependentpersonid_count(self, hid, pid,
                                           lastTripDep, stActDep,
                                           lastTripCount, stActTripCount,
                                           tripPurposeFrom):
        #print 'Parsing trip dependentpersonid and tripcount --'
        #print '\t\tTrip Purpose From - ', tripPurposeFrom

        #print '\t\tStart Activity Dep - %s' %(stActDep)
        #print '\t\tLast trip Dependency is - ', lastTripDep

        #print
        #print '\t\tStart Activity Trip Count - %s' %(stActTripCount)
        #print '\t\tLast trip Count is - ', lastTripCount

        lastTripCount = self.parse_personids(lastTripCount)

        lastTripPersons = self.parse_personids(lastTripDep)
        #print '\t\tThe number of people on the previous trip is - %s and they are - %s and depid is - %s' %(len(lastTripPersons), lastTripPersons, lastTripDep)


        if tripPurposeFrom == 600:
            pickupPersons = self.parse_personids(stActDep)

            if stActTripCount >0 and stActTripCount < 100:
                stActTripCount = 100 + stActTripCount
            pickupTripCount = self.parse_personids(stActTripCount)

            #print '\t\tThis is a pickup so we should take all people from dummy pickup loc; count of people - %s and they are - %s ... ' %(len(pickupPersons), pickupPersons)

            lastTripPersons += pickupPersons
            lastTripCount += pickupTripCount

        if tripPurposeFrom == 601:
            dropoffPersons = self.parse_personids(stActDep)
            #print '\t\tThis is a dropoff so we should take all people from dummy pickup loc; count of people - %s and they are - %s ... ' %(len(dropoffPersons), dropoffPersons)

            for person in dropoffPersons:
                try:
                    index = lastTripPersons.index(person)
                    lastTripPersons.pop(index)
                    lastTripCount.pop(index)
                except ValueError, e:
                    #print 'hid - %s and pid - %s' %(hid, pid)
                    raise Exception, 'The hid - %s person - %s should be on the trip check again error occurred and last trip persons - %s' %(hid, person, lastTripPersons)

        lastTripPersonsNum = 1
        lastTripCountNum = 1
        for i in range(len(lastTripPersons)):
            person = lastTripPersons[i]
            tripCount = lastTripCount[i]
            lastTripPersonsNum = lastTripPersonsNum*100 + person
            lastTripCountNum = lastTripCountNum*100 + tripCount

        return lastTripPersonsNum, lastTripCountNum

    def parse_personids(self, tripDep):
        cpTripDep = copy.deepcopy(tripDep)
        modGrt100 = True
        pers = []
        while(modGrt100):
            cpTripDep, pid = divmod(cpTripDep, 100)
            #print cpTripDep, pid
            if (pid > 0 and pid < 99) and cpTripDep>0:
                pers.append(pid)
            if cpTripDep > 100:
                modGrt100 = True
            else:
                modGrt100 = False
        #print tripDep, pers
        #if len(pers) > 1:
        #    print 'Exciting picking up more than one person ... '
        return pers

    def add_dependentpersonid(self,):
        pass


    def remove_dependentpersonid(self,):
        pass
