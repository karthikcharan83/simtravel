class ArgumentsError(Exception):
    pass

class SpecificationError(Exception):
    pass

class ChoicesError(SpecificationError):
    pass

class VariablesError(SpecificationError):
    pass

class CoefficientsError(SpecificationError):
    pass

class SeedError(SpecificationError):
    pass

class ThresholdsError(SpecificationError):
    pass

class DataError(Exception):
    pass

class ProbabilityError(Exception):
    pass

class ErrorSpecificationError(Exception):
    pass

class ModelError(Exception):
    pass

class ConfigurationError(Exception):
    pass

class DatabaseConfigurationError(Exception):
    pass

class SpatioTemporalConstraintError(Exception):
    pass

class PrismConstraintError(Exception):
    pass

# Checking to see how SVN works
