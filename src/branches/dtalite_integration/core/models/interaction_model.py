from numpy import all, array, zeros
from openamos.core.data_array import DataArray
from openamos.core.models.abstract_model import Model
from openamos.core.errors import SpecificationError


class InteractionModel(Model):

    def __init__(self, specification):
        Model.__init__(self, specification)

    def calculate_expected_values(self, data):
        """
        The method returns the product using the coefficients
        in the specification input as power.

        Inputs:
        data - DataArray object
        """
        num_choices = self.specification.number_choices
        expected_value_array = DataArray(zeros((data.rows, num_choices)),
                                         self.choices)
        self.inverse = self.specification.inverse[0]
        for i in range(num_choices):
            coefficients = self.coefficients[i]
            expected_value_array.data[:, i] = data.calculate_product(
                coefficients, inverse=self.inverse)
        return expected_value_array

    def calc_predvalue(self, data, seed=1):
        """
        The method returns evaluates the product for the
        different choices using the coefficients in the specification
        input as power.

        Inputs:
        data - DataArray object
        """
        # raw_input()
        expected_value = self.calculate_expected_values(data)
        # print data.columns(['tt1'])
        # print expected_value
        return DataArray(expected_value.data, self.specification.choices)


import unittest
from openamos.core.models.model_components import Specification


class TestInteractionModel(unittest.TestCase):

    def setUp(self):
        choice = ['age_tt_product']
        coefficients = [{'age': 1, 'tt': 1}]

        data = array([[1, 15], [2, 10]])

        self.data = DataArray(data, ['Age', 'TT'])
        self.specification = Specification(choice, coefficients)

    def testvalues(self):
        model = InteractionModel(self.specification)
        pred_value = model.calc_predvalue(self.data)

        pred_act = self.data.calculate_product(
            self.specification.coefficients[0])

        pred_diff = all(pred_value.data[:, 0] == pred_act)

        self.assertEqual(True, pred_diff)

if __name__ == '__main__':
    unittest.main()
