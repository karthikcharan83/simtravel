
class HistoryInfo(object):
    def __init__(self, tableName, historyAggVar, historyVarAggConditions):
        self.tableName = tableName
        self.historyAggVar = historyAggVar
        self.historyVarAggConditions = historyVarAggConditions




class HouseholdStructureInfo(object):
    def __init__(self, tableName, houseid,
                 personid, structuresDict):
        self.tableName = tableName
        self.houseid = houseid
        self.personid = personid
        self.structuresDict = structuresDict


    def __repr__(self):
        return ("""Tablename - %s, keys - %s, %s"""\
                    """\n\tStructures - %s """
                %(self.tableName, self.houseid, self.personid, self.structuresDict))

    
