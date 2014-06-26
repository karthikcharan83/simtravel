from openamos.core.models.model_components import Specification
from openamos.core.errors import SpecificationError, ChoicesError
from openamos.core.errors import CoefficientsError

class CountSpecification(Specification):
    """
    This is the base class for specifying the attributes for a count data
    regression model.
    
    Inputs:
    choices - a list object of strings
    coefficients - a list of dictionaries; dictionary is a {'variable':'coefficient'}
    distribution - type of distribution (poisson/negativebinomial)
    """
    def __init__(self, choices, coefficients, distribution=None):
        Specification.__init__(self, choices, coefficients)

        if distribution is None:
            self.distribution = 'poisson'
        else:
            self.distribution = distribution
            checkVal, checkText = self.check_text_only([self.distribution])
            if not checkVal:
                raise SpecificationError, """the distribution specification is not """\
                    """a valid string"""
            if self.distribution not in ['poisson', 'negativebinomial']:
                raise SpecificationError, """the ordered model formulations """\
                    """ supported are poisson and negativebinomial specification"""

    def check(self):
        checkVal, checkText = self.check_text_only(self.choices)
        if not checkVal:
            raise ChoicesError, checkText

        checkVal, checkText = self.check_each_dict(self.coefficients)
        if not checkVal:
            raise CoefficientsError, checkText

        checkVal, checkText = self.check_specification_consistency(self.choices, 
                                                                   self.coefficients)

        if not checkVal:
            raise SpecificationError, checkText

    def check_specification_consistency(self, choices, coefficients):
        if len(coefficients) > 1:
            return 0, """the number of equations specified is more than 1; """\
                """only one equation expected"""

        return 1, ''
        

import unittest

class TestBadCountSpecification(unittest.TestCase):
    def setUp(self):
        self.choices = ['Veh1', 'Veh2', 'Veh3']
        self.coefficients = [{'Constant':2, 'Var1':2.11}]
        self.coefficients1 = [{'Constant':2, 'Var1':2.11}, {'Constant':1.2}]
        
        self.distribution1 = 'notspecified'
        self.distribution2 = 123

    def testcoeffecients(self):
        self.assertRaises(SpecificationError, CountSpecification, 
                          self.choices, self.coefficients1)

    def testdistributions(self):
        self.assertRaises(SpecificationError, CountSpecification, self.choices, 
                          self.coefficients, distribution=self.distribution1)
        self.assertRaises(SpecificationError, CountSpecification, self.choices, 
                          self.coefficients, distribution=self.distribution2)

        
        
if __name__ == '__main__':
    unittest.main()
