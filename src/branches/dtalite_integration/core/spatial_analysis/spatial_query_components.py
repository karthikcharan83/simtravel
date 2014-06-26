from openamos.core.data_array import DataFilter

from openamos.core.errors import PrismConstraintError, SpatioTemporalConstraintError


class SpatioTemporalConstraint(object):

    def __init__(self, table, loc, time=None):

        if not isinstance(table, str):
            raise SpatioTemporalConstraintError, """The table name is """\
                """not valid; should a str object"""
        self.table = table

        if not isinstance(loc, str):
            raise SpatioTemporalConstraintError, """The locations field name is """\
                """not valid; should a str object"""
        self.locationField = loc

        if time is not None and not isinstance(time, str):
            raise SpatioTemporalConstraintError, """The time field name is """\
                """not valid; should be a str object"""
        self.timeField = time

    def __repr__(self):
        return ("""Table - %s; """
                """Location Field - %s; Time Field - %s\n"""
                % (self.table, self.locationField, self.timeField))


class PrismConstraints(object):

    def __init__(self, table, skimField,
                 originField, destinationField,
                 startConstraint, endConstraint,
                 asField,
                 distField,
                 votdField=None,
                 sampleField=None,
                 countChoices=None, activityTypeFilter=None, threshold=None,
                 seed=1, afterModel=None, beforeModel=None, locationInfoTable=None,
                 locationIdVar=None, locationVariables=[], locationFilterList=[], locationFilterType="or"):

        if not isinstance(table, str):
            raise PrismConstraintError, """The destination locations table name is """\
                """not valid; should be a str object"""
        self.table = table

        if not isinstance(skimField, str):
            raise PrismConstraintError, """The skim field is """\
                """not valid; should be a str object"""
        self.skimField = skimField

        if not isinstance(originField, str):
            raise PrismConstraintError, """The origin field is """\
                """not valid; should be a str object"""
        self.originField = originField

        if not isinstance(destinationField, str):
            raise PrismConstraintError, """The destination field is """\
                """not valid; should be a str object"""
        self.destinationField = destinationField

        if not isinstance(startConstraint, SpatioTemporalConstraint):
            raise PrismConstraintError, """The start constraint for the prism """\
                """is not a valid SpatioTemporalConstraint object"""
        self.startConstraint = startConstraint

        if not isinstance(endConstraint, SpatioTemporalConstraint):
            raise PrismConstraintError, """The start constraint for the prism """\
                """is not a valid SpatioTemporalConstraint object"""
        self.endConstraint = endConstraint

        if asField is not None and not isinstance(asField, str):
            raise PrismConstraintError, """The as field is """\
                """not valid; should be a str object"""
        self.asField = asField

        if distField is not None and not isinstance(distField, str):
            raise PrismConstraintError, """The dist field is """\
                """not valid; should be a str object"""
        self.distField = distField

        if votdField is not None and not isinstance(votdField, str):
            raise PrismConstraintError, """The votd field is """\
                """not valid; should be a str object"""
        self.votdField = votdField

        if sampleField is not None and not isinstance(sampleField, str):
            raise PrismConstraintError, """The sample field is """\
                """not valid; should be a str object"""
        self.sampleField = sampleField

        if countChoices is not None and not isinstance(countChoices, int):
            raise PrismConstraintError, """The number of destination choices """\
                """to be returned; should be a valid integer type """
        self.countChoices = countChoices

        if not isinstance(seed, int):
            raise PrismConstraintError, """The seed  """\
                """should be a valid integer type """
        self.seed = seed

        if activityTypeFilter is not None and not isinstance(analysisTypeFilter, DataFilter):
            raise PrismConstraintError, """The activity type filter for the prism is """\
                """not a valid DataFilter object"""
        self.activityTypeFilter = activityTypeFilter

        if threshold is not None and not type(threshold) in [int, float]:
            raise PrismConstraintError, """The threshold level for the prism constraint """\
                """not a valid numeric type object"""
        self.threshold = threshold

        self.afterModel = afterModel
        self.beforeModel = beforeModel

        self.locationInfoTable = locationInfoTable
        self.locationIdVar = locationIdVar
        self.locationVariables = locationVariables
        self.locationFilterList = locationFilterList
        self.locationFilterType = locationFilterType

    def __repr__(self):
        return ("""\nTable - %s; Field - %s\n"""
                """\t\tOrigin Field - %s; Destination Field - %s; Sample Field - %s"""
                """\n\t\tStart Constraint - %s"""
                """\t\tEnd Constraint - %s"""
                """\t\tNumber of choices - %s"""
                """\n\t\tThreshold for window - %s"""
                """\n\t\tAfter Model - %s"""
                """\n\t\tBefore Model - %s"""
                """\n\t\tLocation Variables = %s"""
                """\n\t\tLocation Filter List = %s"""
                """\n\t\tLocation Filter Type = %s"""
                % (self.table, self.skimField, self.originField, self.destinationField,
                   self.sampleField, self.startConstraint,
                   self.endConstraint, self.countChoices,
                   self.threshold,
                   self.afterModel,
                   self.beforeModel,
                   self.locationVariables,
                   self.locationFilterList,
                   self.locationFilterType))


# class PrismLocationChoicesConstraints(PrismConstraints):
#    def __init__(self, table, field, startConstraint, endConstraint,
#        PrismConstraints.__init__(table, field, startConstraint, endConstraint)
