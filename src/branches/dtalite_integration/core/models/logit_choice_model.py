from numpy import ma, array, all, any
from scipy import exp
from openamos.core.models.model_components import Specification
from openamos.core.models.abstract_choice_model import AbstractChoiceModel
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.errors import SpecificationError

from pandas import DataFrame as df

class LogitChoiceModel(AbstractChoiceModel):

    """
    This is the base class for implementing logit choice models in OpenAMOS.

    Input:
    specification - Specification object
    """

    def __init__(self, specification):
        if not isinstance(specification, Specification):
            raise SpecificationError, """the specification input is not a valid """\
                """Specification object"""
        AbstractChoiceModel.__init__(self, specification)

    def calc_observed_utilities(self, data):
        """
        The method returns the observed portion of the utility associated with
        the different choices.

        Inputs:
        data - DataArray object
        """
        values = self.calculate_expected_values(data)
        #values.data = ma.array(values.data)
        return values

    def validchoiceutilities(self, data, choiceset):
        """
        The method returns the observed portion of the utility associated with
        the ONLY the valid choices.

        Inputs:
        data - DataArray object
        choiceset - DataArray object
        """
        valid_values = self.calc_observed_utilities(data)
        #print "utilities", valid_values
        return valid_values
        """
        for i in choiceset.varnames:
            mask = choiceset.column(i) == 0
            if any(mask == True):
                valid_values.setcolumn(i, ma.masked, mask)
        return valid_values
    """
    def calc_exp_choice_utilities(self, data, choiceset):
        """
        The method returns the exponent of the observed portion of the
        utility associated with the different choices.

        Inputs:
        data - DataArray object
        choiceset - DataArray object
        """
        #values = self.validchoiceutilities(data, choiceset)
        #values.data = exp(values.data)
        return self.calculate_exp_expected_values(data)

    def calc_probabilities(self, data, choiceset):
        """
        The method returns the selection probability associated with the
        the different choices.

        Inputs:
        data - DataArray object
        choiceset - DataArray object
        """
        exp_expected_utilities = self.calc_exp_choice_utilities(
            data, choiceset)
        #print "exp util",  exp_expected_utilities
        exp_utility_sum = exp_expected_utilities.cumsum(1)
        #print "exp util sum",  exp_utility_sum
        exp_utility_sum_max = exp_utility_sum.max(1)
        probabilities = exp_expected_utilities.div(exp_utility_sum_max, axis=0)
        #print "prob",  probabilities
        return probabilities

    def calc_chosenalternative(self, data, choiceset=None, seed=1):
        """
        The method returns the selected choice among the available
        alternatives.

        Inputs:
        data = DataArray object
        choiceset = DataArray object
        """
        if choiceset is None:
            choiceset = DataArray()
        pred_prob = self.calc_probabilities(data, choiceset)
        #probabilities = DataArray(pred_prob, self.specification.choices, 
        #                                        data.index)
        prob_model = AbstractProbabilityModel(pred_prob, seed)
        return prob_model.selected_choice()

import unittest
from numpy import zeros
from openamos.core.data_array import DataArray


class TestBadInputLogitChoiceModel(unittest.TestCase):

    def setUp(self):
        choices = ['SOV', 'HOV']
        coefficients = [{'Constant': 2, 'Var1': 2.11}, {'Constant': 1.2}]

        self.specification1 = (choices, coefficients)

    def testspecificationvalidtype(self):
        self.assertRaises(
            SpecificationError, LogitChoiceModel, self.specification1)


class TestLogitChoiceModel(unittest.TestCase):

    def setUp(self):
        choices = ['SOV', 'HOV']
        coefficients = [{'Constant': 2, 'Var1': 2.11}, {'Constant': 1.2}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])

        self.choiceset1 = DataArray(ma.array([[0, 1], [0, 1], [1, 1], [1, 1]]),
                                    ['SOV', 'HOV'])

        self.data = DataArray(data, ['Constant', 'Var1'])
        self.specification = Specification(choices, coefficients)

        self.utils_array_act = zeros((self.data.rows,
                                      self.specification.number_choices))
        self.utils_array_act[:, 0] = self.data.data[
            :, 0] * 2 + self.data.data[:, 1] * 2.11
        self.utils_array_act[:, 1] = self.data.data[:, 0] * 1.2
        self.exp_utils_array_act = exp(self.utils_array_act)
        self.prob_array_act = (self.exp_utils_array_act.transpose() /
                               self.exp_utils_array_act.cumsum(-1)[:, -1]).transpose()

        # for the selected data, and seed = 1, chosen alternatives are
        self.selected_act = array([['sov'], ['hov'], ['sov'], ['sov']])
        self.selected_act1 = array([['hov'], ['hov'], ['sov'], ['sov']])

    def testmodelresults(self):
        model = LogitChoiceModel(self.specification)
        choiceset = DataArray(array([]), [])
        probabilities_model = model.calc_probabilities(self.data, choiceset)
        probabilities_diff = all(self.prob_array_act == probabilities_model)
        self.assertEqual(True, probabilities_diff)

        selected_model = model.calc_chosenalternative(self.data)
        selected_diff = all(self.selected_act == selected_model)
        self.assertEqual(True, selected_diff)

    def testmodelresultswithchoicesets(self):
        model = LogitChoiceModel(self.specification)
        probabilities_model = model.calc_probabilities(
            self.data, self.choiceset1)

        # Calculating actual values with mask included and then compare
        # it against outputs from model
        mask = self.choiceset1.data == 0
        self.exp_utils_array_act[mask] = ma.masked
        self.prob_array_act = (self.exp_utils_array_act.transpose() /
                               self.exp_utils_array_act.cumsum(-1)[:, -1]).transpose()
        probabilities_diff = all(self.prob_array_act == probabilities_model)
        self.assertEqual(True, probabilities_diff)

        selected_model = model.calc_chosenalternative(
            self.data, self.choiceset1)
        selected_diff = all(self.selected_act1 == selected_model)
        self.assertEqual(True, selected_diff)


if __name__ == '__main__':
    unittest.main()
