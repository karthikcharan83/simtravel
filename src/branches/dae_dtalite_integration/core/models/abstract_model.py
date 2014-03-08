from numpy import zeros
from scipy import exp
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification

class Model(object):
    """
    This is the base class for all the mathematical formulations
    implemented in OpenAMOS including both regression and choice models.
    
    Inputs:
    specification - Specification object
    """
    def __init__(self, specification):
        self.specification = specification
        self.choices = self.specification.choices
        self.coefficients = self.specification.coefficients

    def calculate_expected_values(self, data):
        """
        The method returns the expected values for the different choices
        using the coefficients in the specification input.
        
        Inputs:
        data - DataArray object
        """
        num_choices = self.specification.number_choices
        expected_value_array = DataArray(zeros((data.rows, num_choices)), 
                                         self.choices)

        for i in range(num_choices):
            coefficients = self.coefficients[i]
            expected_value_array.data[:,i] = data.calculate_equation(coefficients)
        return expected_value_array
    

    def calculate_exp_expected_values(self, data):
        """
        The method returns the exponent of the expected values for the
        the different choices using the coefficients in the specification input.
        
        Inputs:
        data - DataArray object
        """
        num_choices = self.specification.number_choices
        exp_expected_value_array = DataArray(zeros((data.rows, num_choices)),
                                        self.choices)
        for i in range(num_choices):
            coefficients = self.coefficients[i]
            exp_expected_value_array.data[:,i] = data.exp_calculate_equation(coefficients)

        #exp_expected_values = self.calculate_expected_values(data)
        #exp_expected_values.data = exp(exp_expected_values.data)
        return exp_expected_value_array
        

import unittest
from numpy import array, all

class TestAbstractModel(unittest.TestCase):
    def setUp(self):
        choices = ['SOV', 'HOV']
        variables = [['Constant', 'Var1'], ['Constant']]
        coefficients = [{'Constant':2, 'Var1':2.11}, {'Constant':1.2}]

        self.data = DataArray(array([[1, 1.1], [1, -0.25]]), ['Constant', 'Var1'])
        self.specification = Specification(choices, coefficients)
        self.model = Model(self.specification)
        

    def testexpectedvalue(self):
        value_array_act = zeros((self.data.rows,self.specification.number_choices))
        value_array_act[:,0] = self.data.data[:,0]*2 + self.data.data[:,1]*2.11
        value_array_act[:,1] = self.data.data[:,0]*1.2

        expected_value_array = self.model.calculate_expected_values(self.data)
        self.assertEqual(True, isinstance(expected_value_array, DataArray))
        self.assertEqual(self.specification.choices, expected_value_array.varnames)
        diff_values = all(value_array_act == expected_value_array.data)
        self.assertEqual(True, diff_values)

        exp_expected_value_array = self.model.calculate_exp_expected_values(
                                                                                self.data)
        self.assertEqual(True, isinstance(exp_expected_value_array, DataArray))
        self.assertEqual(self.specification.choices, 
                            exp_expected_value_array.varnames)
        diff_values = all(exp(value_array_act) == exp_expected_value_array.data)
        self.assertEqual(True, diff_values)

if __name__ == '__main__':
    unittest.main()
