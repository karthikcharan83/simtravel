from numpy import all, array, zeros
from scipy import exp
from openamos.core.models.abstract_model import Model
from openamos.core.errors import SpecificationError, ErrorSpecificationError

class AbstractRegressionModel(Model):
    def __init__(self, specification, error_specification):
        """
        This is the base class for all regression based mathematical formulations
        in OpenAMOS

        Inputs:
        specification - Specification object
        error_specifciation - ErrorSpecification object
        """

        Model.__init__(self, specification)

        if not isinstance(self.specification, Specification):
            raise SpecificationError, """specification input is not a """\
                """valid Specification object"""

        self.error_specification = error_specification

        if specification.number_choices > 1:
            raise SpecificationError, """invalid specification for regression """\
                """ model only one equation needs to be specified"""

        if not isinstance(self.error_specification, ErrorSpecification):
            raise ErrorSpecificationError, """invalid error specification"""\
                """ it should be of type ErrorSpecification"""

    def calc_expected_value(self, data):
        """
        The method returns the expected values for the different choices using
        the coefficients specified in the specification input.

        Inputs:
        data - DataArray object
        """

        return self.calculate_expected_values(data)

    def calc_exp_expected_value(self, data):
        """
        The method returns the exponent of the expected values for the
        different choices using the coefficients specified in the specification input.

        Inputs:
        data - DataArray object
        """
        return self.calculate_exp_expected_values(data)

    def calc_errorcomponent(self):
        """
        The method returns the contribution of the error in the calculation
        of the predicted value for the different choices.

        Inputs:
        None
        """
        raise Exception('method not implemented')

    def calc_predvalue(self):
        """
        The method returns the predicted value for the different choices in the
        specification input.

        Inputs:
        None
        """

        raise Exception('method not implemented')


import unittest
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification
from openamos.core.models.error_specification import ErrorSpecification


class TestBadSpecificationRegressionModel(unittest.TestCase):
    def setUp(self):
        choices = ['SOV', 'HOV']
        coefficients = [{'Constant':2, 'Var1':2.11}, {'Constant':1.2}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])

        variance = array([[1.1]])
        variance1 = array([[1.1, 1.2], [2.1, 2.2]])

        self.data = DataArray(data, ['Constant', 'VAR1'])

        self.specification = Specification(choices, coefficients)

        self.errorspecification = ErrorSpecification(variance, 'normal')
        self.errorspecification1 = ErrorSpecification(variance1, 'normal')

    def testtwodependentvars(self):
        self.assertRaises(SpecificationError, AbstractRegressionModel,
                          self.specification, self.errorspecification)

    def testtwoerrorcomponents(self):
        self.assertRaises(SpecificationError, AbstractRegressionModel,
                          self.specification, self.errorspecification1)


class TestAbstractRegressionModel(unittest.TestCase):
    def setUp(self):
        choice = ['SOV']
        coefficients = [{'constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])
        variance = array([[1.1]])

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.specification = Specification(choice, coefficients)
        self.errorspecification = ErrorSpecification(variance, 'normal')


    def testvalues(self):
        model = AbstractRegressionModel(self.specification, self.errorspecification)

        model_expected_values = model.calc_expected_value(self.data)
        expected_act = zeros((self.data.rows, 1))
        expected_act[:,0] = self.data.data[:,0] * 2 + self.data.data[:,1] * 2.11
        expected_diff = all(expected_act == model_expected_values.data)
        self.assertEqual(True, expected_diff)

        exp_expected_act = exp(expected_act)
        model_exp_expected_values = model.calc_exp_expected_value(self.data)
        exp_expected_diff = all(exp_expected_act ==
                                model_exp_expected_values.data)
        self.assertEqual(True, exp_expected_diff)


    def testerrorspecification(self):
        #TODO:Write the tests for errorspecification if any in here
        #or should they just be written in the specifica implementations
        #e.g. stochastic-frontier, linear regression etc.
        pass

if __name__ == '__main__':
    unittest.main()
