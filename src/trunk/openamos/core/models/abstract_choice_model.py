from numpy import all, array, zeros
from scipy import exp
from openamos.core.models.abstract_model import Model

class AbstractChoiceModel(Model):
    """
    This is the base class for all discrete choice based mathematical
    formulations in OpenAMOS.

    Inputs:
    specification - Specification object
    """
    def __init__(self, specification):
        Model.__init__(self, specification)

    def calc_observed_utilities(self, data):
        """
        The method returns the observed portion of the utility associated with
        the different choices.

        Inputs:
        data - DataArray object
        """
        return self.calculate_expected_values(data)

    def validchoiceutilities(self):
        """
        The method returns the observed portion of the utility associated with
        the ONLY the valid choices.

        Inputs:
        None
        """
        raise Exception('method not implemented')

    def calc_exp_choice_utilities(self, data):
        """
        The method returns the exponent of the observed portion of the
        utility associated with the different choices.

        Inputs:
        data - DataArray object
        """
        return self.calculate_exp_expected_values(data)

    def calc_probabilities(self):
        """
        The method returns the selection probability associated with the
        the different choices.

        Inputs:
        None
        """
        raise Exception('method not implemented')

    def calc_chosenalternative(self):
        """
        The method returns the selected choice among the available
        alternatives.

        Inputs:
        None
        """
        raise Exception('method not implemented')

import unittest
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification

class TestAbstractChoiceModel(unittest.TestCase):
    def setUp(self):
        choice = ['SOV']
        coefficients = [{'constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.specification = Specification(choice, coefficients)

    def testvalues(self):
        model = AbstractChoiceModel(self.specification)

        model_expected_values = model.calc_observed_utilities(self.data)
        expected_act = zeros((self.data.rows, 1))
        expected_act[:,0] = self.data.data[:,0] * 2 + self.data.data[:,1] * 2.11
        expected_diff = all(expected_act == model_expected_values.data)
        self.assertEqual(True, expected_diff)

        exp_expected_act = exp(expected_act)
        model_exp_expected_values = model.calc_exp_choice_utilities(self.data)
        exp_expected_diff = all(exp_expected_act ==
                                     model_exp_expected_values.data)
        self.assertEqual(True, exp_expected_diff)

if __name__ == '__main__':
    unittest.main()
