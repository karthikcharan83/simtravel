class PopGenModelSpecification(object):
    def __init__(self, idSpec, hhldAttribs, personAttribs,
                 popgenConfig, hhldIdSeries):

        self.idSpec = idSpec
        self.hhldAttribs = hhldAttribs
        self.personAttribs = personAttribs

        self.popgenConfig = popgenConfig

        self.hhldIdSeries = hhldIdSeries

        self.choices = None
        self.coefficients = None


class ImmigrationSpecification(object):
    def __init__(self, idSpec, agentType, hhldAttribs=None,
                 personAttribs=None, evolutionAttribs=None):

        self.hhldSampleLoc = hhldSampleLoc
        self.personSampleLoc = personSampleLoc
        self.gqSampleLoc = gqSampleLoc

        self.hhldMarginalsLoc = hhldMarginalsLoc
        self.personMarginalsLoc = personMarginalsLoc
        self.gqMarginalsLoc = gqMarginalsLoc

        self.geocorrLoc = geocorrLoc

        self.hhSynthesizedLoc = hhSynthesizedLoc
        self.hhSynthesizedMetaLoc = hhSynthesizedMetaLoc
        self.personSynthesizedLoc = personSynthesizedLoc
        self.personSynthesizedMetaLoc = personSynthesizedMetaLoc

        self.popgenConfigObject = popgenConfigObject


        self.choices = None
        self.coefficients = None
