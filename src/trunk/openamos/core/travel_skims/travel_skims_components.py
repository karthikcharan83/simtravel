
class TravelSkimsPeriodDBInfo(object):
    def __init__(self, tableName, origin_var, destination_var,
                 intervalStart, intervalEnd,
                 tt_skim_var, tt_fileLocation, tt_delimiter,
                 dist_skim_var, dist_fileLocation, dist_delimiter):
        self.tableName = tableName
        self.origin_var = origin_var
        self.destination_var = destination_var
        self.intervalStart = intervalStart
        self.intervalEnd = intervalEnd

        self.ttSkimVar = tt_skim_var
        self.ttFileLocation = tt_fileLocation
        self.ttDelimiter = tt_delimiter

        self.distSkimVar = dist_skim_var
        self.distFileLocation = dist_fileLocation
        self.distDelimiter = dist_delimiter


    def __repr__(self):
        return ("""\tTravel skims table that will be cached - %s """\
                    """\n\t\tOrigin variable - %s, Destination variable - %s, """\
                    """Interval start - %s, Interval end - %s, """\
                    """tt File location - %s, dist File location - %s""" %(self.tableName,
                                              self.origin_var, self.destination_var,
                                              self.intervalStart, self.intervalEnd,
                                              self.ttFileLocation, self.distFileLocation))

class TravelSkimsInfo(object):
    def __init__(self):
        self.table_lookup = {}
        self.table_ttLocationLookup = {}
        self.table_distLocationLookup = {}
        self.tableDBInfoList = []
        self.tableNamesList = []

    def add_tableInfoToList(self, tableName, origin_var, destination_var,
                            intervalStart, intervalEnd,
                            tt_skim_var, tt_fileLocation, tt_delimiter,
                            dist_skim_var, dist_fileLocation, dist_delimiter):

        if tableName not in self.tableNamesList:
            dbInfoObject = TravelSkimsPeriodDBInfo(tableName, origin_var,
                                                   destination_var,
                                                   intervalStart,
                                                   intervalEnd,

                                                   tt_skim_var,
                                                   tt_fileLocation,
                                                   tt_delimiter,

                                                   dist_skim_var,
                                                   dist_fileLocation,
                                                   dist_delimiter)
            print 'Skim added - ', dbInfoObject

            self.tableDBInfoList.append(dbInfoObject)
            self.tableNamesList.append(tableName)
        self.add_tableLookup(intervalStart, intervalEnd, tableName)
        self.add_ttTableLocationLookup(intervalStart, intervalEnd, tt_fileLocation)
        self.add_distTableLocationLookup(intervalStart, intervalEnd, dist_fileLocation)

    def add_tableLookup(self, intervalStart, intervalEnd, tableName):
        self.table_lookup[(intervalStart, intervalEnd)] = tableName
        #print '\tSkims table name - %s applies for interval starting at %s and ending at %s' %(tableName, intervalStart,
        #                                                      intervalEnd)

    def add_ttTableLocationLookup(self, intervalStart, intervalEnd, file_location):
        self.table_ttLocationLookup[(intervalStart, intervalEnd)] = file_location
        #print '\tSkims file location - %s applies for interval starting at %s and ending at %s' %(file_location, intervalStart,
        #                                                                                         intervalEnd)

    def add_distTableLocationLookup(self, intervalStart, intervalEnd, file_location):
        self.table_distLocationLookup[(intervalStart, intervalEnd)] = file_location


    def lookup_table(self, period):
        period_boundaries = self.table_lookup.keys()
        period_boundaries.sort()


        for boundary in period_boundaries:
            if period >= boundary[0] and period <= boundary[1]:
                return self.table_lookup[boundary]

        return None


    def lookup_ttTableLocation(self, period):
        period_boundaries = self.table_ttLocationLookup.keys()
        period_boundaries.sort()


        for boundary in period_boundaries:
            if period >= boundary[0] and period <= boundary[1]:
                return self.table_ttLocationLookup[boundary]

        return None


    def lookup_distTableLocation(self, period):
        period_boundaries = self.table_distLocationLookup.keys()
        period_boundaries.sort()

        print period_boundaries
        print period


        for boundary in period_boundaries:
            if period >= boundary[0] and period <= boundary[1]:
                return self.table_distLocationLookup[boundary]

        return None
