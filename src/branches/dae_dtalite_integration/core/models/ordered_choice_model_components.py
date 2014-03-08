from openamos.core.models.model_components import Specification
from openamos.core.errors import SpecificationError, ChoicesError, CoefficientsError, ThresholdsError

class OLSpecification(Specification):
    """
    This is the base class for specifying the attributes of a ordered choice
    model.
    
    Inputs:
    choices - list of strings
    coefficients - list of dictionaries
    thresholds - list of threshold values
    distribution - string (logit/probit)
    """
    def __init__(self, choices, coefficients, thresholds, distribution=None):
        self.thresholds = thresholds
        Specification.__init__(self, choices, coefficients)

        if distribution is None:
            self.distribution = 'logit'
        else:
            self.distribution = distribution
            checkVal, checkText = self.check_text_only([self.distribution])
            if not checkVal:
                raise SpecificationError, """the distribution specification is not """\
                    """a valid string"""
            if self.distribution not in ['logit', 'probit']:
                raise SpecificationError, """the ordered model formulations """\
                    """supported are probit and logit specification"""

    def check(self):
        checkVal, checkText = self.check_text_only(self.choices)
        if not checkVal:
            raise ChoicesError, checkText

        checkVal, checkText = self.check_each_dict(self.coefficients)
        if not checkVal:
            raise CoefficientsError, checkText

        checkVal, checkText = self.check_specification_consistency(self.choices, 
                                                                   self.coefficients, 
                                                                   self.thresholds)

        if not checkVal:
            raise SpecificationError, checkText

        
        checkVal, checkText = self.check_num_only(self.thresholds)
        if not checkVal:
            raise ThresholdsError, checkText


    def check_specification_consistency(self, choices, coefficients, thresholds):
        if len(choices) - 1 <> len(thresholds):
            return 0, """the number of choices and the number of thresholds """\
                """are inconsistent"""
        
        if len(coefficients) > 1:
            return 0, """the number of equations specified is more than 1; """\
                """only one equation expected"""

        return 1, ''
        

import unittest

class TestBadOLSpecification(unittest.TestCase):
    def setUp(self):
        self.choices = ['Veh1', 'Veh2', 'Veh3']
        self.coefficients = [{'Constant':2, 'Var1':2.11}]
        self.coefficients1 = [{'Constant':2, 'Var1':2.11}, {'Constant':1.2}]
        
        self.thresholds = [1.2, 2.1]
        self.thresholds1 = ['1.2', '2.1']
        self.thresholds2 = [1.2, 2.1, 3.2]

        self.distribution1 = 'notspecified'
        self.distribution2 = 123

    def testcoeffecients(self):
        self.assertRaises(SpecificationError, OLSpecification, self.choices, 
                          self.coefficients1, self.thresholds)

    def testthredholds(self):
        self.assertRaises(ThresholdsError, OLSpecification, self.choices, 
                          self.coefficients, self.thresholds1)
        self.assertRaises(SpecificationError, OLSpecification, self.choices, self.coefficients, 
                          self.thresholds2)
    def testdistributions(self):
        self.assertRaises(SpecificationError, OLSpecification, self.choices, 
                          self.coefficients, 
                          self.thresholds, distribution=self.distribution1)
        self.assertRaises(SpecificationError, OLSpecification, self.choices, 
                          self.coefficients, 
                          self.thresholds, distribution=self.distribution2)

if __name__ == '__main__':
    unittest.main()
