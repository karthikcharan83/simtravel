

class LocationsInfo(object):
    def __init__(self, tableName, referenceTableName,
                 location_id_var, locations_varsList):
        self.tableName = tableName
        self.referenceTableName = referenceTableName
        self.location_id_var = location_id_var
        self.locations_varsList = locations_varsList


    def __repr__(self):
        return ("""\tLocations table that will be cached is %s """\
                    """and this will be referenced as - %s """\
                    """\n\t\t Location id variable is - %s """\
                    """\n\t\t Variables extracetd and cached are - %s """
                %(self.tableName, self.referenceTableName,
                  self.location_id_var, self.locations_varsList))
