from numpy import ma, array, any, zeros
from scipy import log
from openamos.core.models.nested_logit_model_components import NestedSpecification
from openamos.core.models.abstract_choice_model import AbstractChoiceModel
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.errors import SpecificationError


class NestedLogitChoiceModel(AbstractChoiceModel):

    """
    This is the base class for implementing nested logit choice models
    in OpenAMOS. The formulation can accommodate any number of nests, and
    also accommodates variable choice sets across respondents.

    Input:
    specification - NestedSpecification object
    """

    def __init__(self, specification):
        AbstractChoiceModel.__init__(self, specification)
        if not isinstance(specification, NestedSpecification):
            raise SpecificationError, """the specification input is not a valid """\
                """NestedSpecification object"""

        self.parent_list = []
        for parent in self.specification:
            self.parent_list.append(parent)

    def calc_observed_utilities(self, data):
        """
        The method returns the observed portion of the utility associated with
        the different choices.

        Inputs:
        data - DataArray object
        """
        # Just calculating the individual branch's utility without
        # scaling by the logsum parameters and the logsum carry overs to
        # considering parent nodes
        values = self.calculate_expected_values(data)
        values.data = ma.array(values.data)
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
        for i in choiceset.varnames:
            mask = choiceset.column(i) == 0
            if any(mask == True):
                child_choices = self.specification.all_child_names([i])
                for i in child_choices + [i]:
                    valid_values.setcolumn(i, ma.masked, mask)
        return valid_values

    def calc_exp_choice_utilities(self, data, choiceset):
        """
        The method returns the exponent of the observed portion of the
        utility associated with the different choices.

        Inputs:
        data - DataArray object
        choiceset - DataArray object
        """
        obs_values = self.validchoiceutilities(data, choiceset)
        spec_dict = self.specification.specification

        missing_choices = choiceset.varnames

        # Iterating through parent nodes and calculating exp of utilities
        # logsum_parameter_parent --> the node which is being considered
        # logsum_parameter_child --> the logsum parameter of the child node if
        #                          it has sub branches
        #self.parent_list = []
        # for parent in self.specification:
        #    self.parent_list.append(parent)

        for parent in self.parent_list:
            if parent == 'root':
                logsum_parameter_parent = 1
                all_actual_choices = self.specification.all_actual_choice_names(
                    ['root'])
                parent_name = 'root'
            else:
                logsum_parameter_parent = parent.logsumparameter
                all_actual_choices = self.specification.all_actual_choice_names(
                    [parent.choices[0]])
                parent_name = parent.choices[0]

            # If all the ACTUAL CHOICES for a particular parent are missing
            # as specified in the CHOICESET variable then the
            # scaled utilities are coded as missing and the branch is not considered
            # in the calculation of probabilities
            actual_choices_missing = list(all_actual_choices.intersection(
                missing_choices))
            if len(all_actual_choices) > 0 and (list(all_actual_choices) ==
                                                actual_choices_missing):
                missing_child_values = obs_values.column(
                    actual_choices_missing[0])
                rows = missing_child_values == ma.masked
                parent_values = obs_values.column(parent_name)
                parent_values[rows] = ma.masked
                obs_values.setcolumn(parent_name, parent_values)

            # Iterating through the children in each parent
            for child in spec_dict[parent]:
                child_name = child.choices[0]
                if child in spec_dict.keys():
                    sub_branch_check = True
                    logsum_parameter_child = child.logsumparameter
                else:
                    sub_branch_check = False
                    logsum_parameter_child = 1
                    # if sub-branch exists

                # checking to see if the node has any children and accordingly
                # calculate the logsum values and then accordingly calculate the
                # utility and exponent of utility
                # if the node does not have any children then scale the utilities
                # by the logsum parameter and calculate the exponent of that
                if sub_branch_check:
                    # branch exists
                    sub_child_names = self.specification.child_names(child)
                    logsum = zeros((obs_values.rows, ))
                    for i in sub_child_names:
                        logsum = logsum + obs_values.column(i)
                    logsum = log(logsum)
                    obs_values.addtocolumn(child_name,
                                           logsum_parameter_child * logsum)
                    obs_values.scaledowncolumn(child_name,
                                               logsum_parameter_parent)
                    obs_values.expofcolumn(child_name)

                else:
                    # if sub-branch does not exist
                    obs_values.scaledowncolumn(child_name,
                                               logsum_parameter_parent)
                    obs_values.expofcolumn(child_name)
        return obs_values

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

        # missing_choices = choiceset.varnames

        #spec_dict = self.specification.specification
        for parent in self.parent_list:
            child_names = self.specification.child_names(parent)

            # calculating the sum of utilities across children in a branch
            util_sum = 0
            for child in child_names:
                # For utils with missing values they are converted to zero
                # before summing the utils across choices in a parent
                # to avoid the case where missing + valid = missing
                child_column = exp_expected_utilities.column(child)
                child_column = child_column.filled(0)
                util_sum = util_sum + child_column

            # calculating the probability of children in a branch
            for child in child_names:
                exp_expected_utilities.setcolumn(child,
                                                 exp_expected_utilities.column(child) / util_sum)

            # Dummy check to ensure that within any branch the probs add to one
            prob_sum = 0
            for child in child_names:
                prob_sum = prob_sum + exp_expected_utilities.column(child)

        for choice in self.specification.actual_choices:
            parent_names = self.specification.all_parent_names(choice)
            for parent in parent_names:
                parent_column = exp_expected_utilities.column(parent)
                choice_column = exp_expected_utilities.column(choice)
                exp_expected_utilities.setcolumn(choice, choice_column *
                                                 parent_column)

        self.specification.actual_choices.sort()
        probabilities = DataArray(ma.zeros((exp_expected_utilities.rows,
                                            len(self.specification.actual_choices))),
                                  self.specification.actual_choices)

        for choice in self.specification.actual_choices:
            probabilities.setcolumn(
                choice, exp_expected_utilities.column(choice))

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
            choiceset = DataArray(array([]), [])
        probabilities = self.calc_probabilities(data, choiceset)
        prob_model = AbstractProbabilityModel(probabilities, seed)
        return prob_model.selected_choice()

# TODO - ELIMINATE PARENTS IF THE ACTUAL CHOICE IS
# ABSENT WHEN CALCULATING PROBABILITIES


import unittest
from numpy import all
from openamos.core.data_array import DataArray
from openamos.core.models.nested_logit_model_components import NestedChoiceSpecification


class TestNestedLogitChoiceModel(unittest.TestCase):

    def setUp(self):
        choices1 = ['sov']
        coefficients1 = [{'Constant': 2, 'Var1': 2.11}]
        spec1 = NestedChoiceSpecification(choices1, coefficients1, 0.88)

        choices2 = ['hov']
        coefficients2 = [{'Constant': 1.2}]
        spec2 = NestedChoiceSpecification(choices2, coefficients2)

        choices3 = ['transit']
        coefficients3 = [{'Constant': .4352, 'Var1': -1.11}]
        spec3 = NestedChoiceSpecification(choices3, coefficients3, 0.9)

        choices31 = ['light rail']
        coefficients31 = [{'Constant': .32, 'Var1': .581}]
        spec31 = NestedChoiceSpecification(choices31, coefficients31, 0.8)

        choices32 = ['bus']
        coefficients32 = [{'Constant': 1.2, 'Var1': 4.11}]
        spec32 = NestedChoiceSpecification(choices32, coefficients32, 0.7)

        choices11 = ['sov1']
        coefficients11 = [{'Constant': 2, 'Var1': 2.11}]
        spec11 = NestedChoiceSpecification(choices11, coefficients11, 0.6)

        choices111 = ['sov11']
        coefficients111 = [{'Constant': 2, 'Var1': 2.11}]
        spec111 = NestedChoiceSpecification(choices111, coefficients111)

        choices311 = ['light rail1']
        coefficients311 = [{'Constant': 1.2, 'Var1': 4.11}]
        spec311 = NestedChoiceSpecification(choices311, coefficients311)

        choices312 = ['light rail2']
        coefficients312 = [{'Constant': 1.2, 'Var1': 4.11}]
        spec312 = NestedChoiceSpecification(choices312, coefficients312)

        choices321 = ['bus1']
        coefficients321 = [{'Constant': 1.2, 'Var1': 4.11}]
        spec321 = NestedChoiceSpecification(choices321, coefficients321)

        choices322 = ['bus2']
        coefficients322 = [{'Constant': 1.2, 'Var1': 4.11}]
        spec322 = NestedChoiceSpecification(choices322, coefficients322)

        specification_dict = {'root': [spec1, spec2, spec3],
                              spec1: [spec11],
                              spec3: [spec31, spec32],
                              spec11: [spec111],
                              spec31: [spec311, spec312],
                              spec32: [spec321, spec322]}

        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])
        self.data = DataArray(data, ['Constant', 'Var1'])

        self.choiceset = DataArray(ma.array([[0, 1], [0, 1], [1, 1], [1, 1]]),
                                   ['sov11', 'HOV'])

        nested_spec = NestedSpecification(specification_dict)
        self.model = NestedLogitChoiceModel(nested_spec)

        nested_spec = NestedSpecification(specification_dict)
        self.model1 = NestedLogitChoiceModel(nested_spec)

    # TODO: Results from the probability distribution model for nested logit
    # specification need to be parsed

    def testmodelresults(self):
        result_model = self.model.calc_chosenalternative(self.data)
        result_act = array([['sov11'], ['sov11'], ['bus1'], ['sov11']])

        result_diff = all(result_act == result_model)
        self.assertEqual(True, result_diff)

    def testmodelresultswithchoicesets(self):
        result_model = self.model1.calc_chosenalternative(self.data,
                                                          self.choiceset)
        result_act = array([['bus1'], ['light rail1'], ['bus1'], ['sov11']])

        result_diff = all(result_act == result_model)
        self.assertEqual(True, result_diff)

if __name__ == '__main__':
    unittest.main()
