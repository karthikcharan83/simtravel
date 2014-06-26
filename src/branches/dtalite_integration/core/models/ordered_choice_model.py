from scipy.stats import genlogistic, norm
from numpy import array, zeros, all

import time

from openamos.core.models.abstract_choice_model import AbstractChoiceModel
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.models.ordered_choice_model_components import OLSpecification
from openamos.core.errors import SpecificationError


class OrderedModel(AbstractChoiceModel):

    """
    This is the base class for implementing ordered choice models in OpenAMOS.
    Both ordered probit and logit models are supported.

    Inputs:
    specification -  OLSpecification object
    """

    def __init__(self, ol_specification):
        if not isinstance(ol_specification, OLSpecification):
            raise SpecificationError, """the specification is not a valid """\
                """OLSpecification object"""

        AbstractChoiceModel.__init__(self, ol_specification)

        self.thresholds = ol_specification.thresholds
        self.distribution = ol_specification.distribution

    def calc_observed_utilities(self, data):
        """
        The method returns the observed portion of the utility associated with
        the different choices.

        Inputs:
        data - DataArray object
        """
        return data.calculate_equation(self.coefficients[0])

    def calc_probabilities(self, data):
        """
        The method returns the selection probability associated with the 
        the different choices.

        Inputs:
        data - DataArray object
        """
        [shape_param] = [1, ] * genlogistic.numargs
        observed_utility = self.calc_observed_utilities(data)
        num_choices = self.specification.number_choices
        probabilities = zeros((data.rows, num_choices))
        lower_bin = 0
        for i in range(num_choices - 1):
            value = self.thresholds[i] - observed_utility
            if self.distribution == 'logit':
                upper_bin = genlogistic.cdf(value, shape_param)
            else:
                upper_bin = norm.cdf(value)

            probabilities[:, i] = upper_bin - lower_bin
            lower_bin = upper_bin

        probabilities[:, i + 1] = 1 - upper_bin
        return probabilities

    def calc_chosenalternative(self, data, choiceset=None, seed=1):
        """
        The method returns the selected choice among the available
        alternatives.

        Inputs:
        data = DataArray object
        """
        #ti = time.time()
        probabilities = DataArray(self.calc_probabilities(data),
                                  self.specification.choices)
        # print "\t\t\tprobabilities calculated in %.4f" %(time.time()-ti)
        prob_model = AbstractProbabilityModel(probabilities, seed)
        #ti = time.time()
        choice = prob_model.selected_choice()
        # print "\t\t\tsimulated completed in %.4f" %(time.time()-ti)

        return choice


import unittest
from openamos.core.data_array import DataArray


class TestBadInputOrderedProbitModel(unittest.TestCase):

    def setUp(self):
        choices = ['Veh1', 'Veh2', 'Veh3']
        coefficients = [{'Constant': 2, 'Var1': 2.11}]
        thresholds = [1.2, 2.1]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])
        self.data = DataArray(data, ['CONSTANT', 'VAR1'])

        self.specification = OLSpecification(choices, coefficients, thresholds)
        self.specification1 = [choices, coefficients, thresholds]

    def testolspecification(self):
        self.assertRaises(SpecificationError, OrderedModel,
                          self.specification1)


class TestOrderedProbitModel(unittest.TestCase):

    def setUp(self):
        choices = ['Veh1', 'Veh2', 'Veh3']
        self.coefficients = [{'Constant': 2, 'Var1': 2.11}]
        self.thresholds = [1.2, 2.1]
        self.data = DataArray(array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]]),
                              ['CONSTANT', 'VAR1'])

        specification = OLSpecification(
            choices, self.coefficients, self.thresholds)
        self.model = OrderedModel(specification)

        specification1 = OLSpecification(choices, self.coefficients, self.thresholds,
                                         distribution='probit')
        self.model1 = OrderedModel(specification1)

    def testprobabilitieslogit(self):
        prob = zeros((4, 3))
        obs_utility = self.data.calculate_equation(self.coefficients[0])
        [shape_param] = [1, ] * genlogistic.numargs
        prob[:, 0] = genlogistic.cdf(
            self.thresholds[0] - obs_utility, shape_param)
        prob[:, 1] = (genlogistic.cdf(self.thresholds[1] - obs_utility, shape_param) -
                      genlogistic.cdf(self.thresholds[0] - obs_utility, shape_param))
        prob[:, 2] = 1 - genlogistic.cdf(self.thresholds[1] -
                                         obs_utility, shape_param)

        prob_model = self.model.calc_probabilities(self.data)
        prob_diff = all(prob == prob_model)
        self.assertEqual(True, prob_diff)

    def testselectionlogit(self):
        choice_act = array([['veh3'], ['veh3'], ['veh1'], ['veh1']])
        choice_model = self.model.calc_chosenalternative(self.data)
        choice_diff = all(choice_act == choice_model)
        self.assertEqual(True, choice_diff)

    def testprobabilitiesprobit(self):
        prob = zeros((4, 3))
        obs_utility = self.data.calculate_equation(self.coefficients[0])
        prob[:, 0] = norm.cdf(self.thresholds[0] - obs_utility)
        prob[:, 1] = (norm.cdf(self.thresholds[1] - obs_utility) -
                      norm.cdf(self.thresholds[0] - obs_utility))
        prob[:, 2] = 1 - norm.cdf(self.thresholds[1] - obs_utility)

        prob_model = self.model1.calc_probabilities(self.data)
        prob_diff = all(prob == prob_model)
        self.assertEqual(True, prob_diff)

    def testselectionprobit(self):
        choice_act = array([['veh3'], ['veh2'], ['veh3'], ['veh2']])
        choice_model = self.model1.calc_chosenalternative(self.data)
        choice_diff = all(choice_act == choice_model)
        self.assertEqual(True, choice_diff)

if __name__ == '__main__':
    unittest.main()
