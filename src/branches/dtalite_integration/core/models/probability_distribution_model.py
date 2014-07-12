'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''

from openamos.core.models.model_components import Specification
from openamos.core.models.abstract_choice_model import AbstractChoiceModel
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.errors import SpecificationError
from openamos.core.data_array import DataArray

from pandas import DataFrame as df

class ProbabilityModel(AbstractChoiceModel):

    def __init__(self, specification):
        if not isinstance(specification, Specification):
            raise SpecificationError, """the specification input is not a valid """\
                """Specification object"""
        AbstractChoiceModel.__init__(self, specification)

    def calc_observed_utilities(self, data):
        return self.calculate_expected_values(data)

    def validchoiceutilities(self, data):
        return self.calc_observed_utilities(data)

    def calc_exp_choice_utilities(self, data):
        pass

    def calc_probabilities(self, data):
        expected_utilities = self.validchoiceutilities(data)
        # in Pandas dataframe cumsum across columns is 1
        utility_sum = expected_utilities.cumsum(1) 
        utility_sum_max = utility_sum.max(1)
        probabilities = expected_utilities.div(utility_sum_max, axis=0)
        return probabilities

    def calc_chosenalternative(self, data, choiceset=None, seed=1):
        pred_prob = self.calc_probabilities(data)
        #probabilities = DataArray(pred_prob, 
        #                          self.specification.choices, data.index)
        prob_model = AbstractProbabilityModel(pred_prob, seed)
        return prob_model.selected_choice()
