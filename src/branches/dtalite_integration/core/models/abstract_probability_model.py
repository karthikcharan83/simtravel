from numpy import ndarray, array, random, ma, zeros, ones
from openamos.core.errors import ProbabilityError, DataError
from openamos.core.data_array import DataArray
from openamos.core.models.abstract_random_distribution_model import RandomDistribution

from pandas import DataFrame as df
from pandas import Series


class AbstractProbabilityModel(object):

    """
    This is the base class for probability models in OpenAMOS.

    Inputs:
    probabilities - datarray object (columns give the probability for the choice)
    seed - numeric value
    """

    def __init__(self, probabilities, seed=1):
        if seed == None:
            raise Exception, "probability"

        self.seed = seed
        self.probabilities = probabilities
        self.check()
        self.choices = list(probabilities.columns.values)

    def check(self):
        """
        This method checks the probabilities input and raises appropriate
        error prompts as necessary.

        Inputs:
        None
        """
        self.check_probabilities()
        #self.check_valid_probabilities()
        self.check_sum()


    def check_probabilities(self):
        """
        The method checks to make sure that the probabilities is a
        valid array object.

        Inputs:
        None
        """
        if not isinstance(self.probabilities, df):
            raise ProbabilityError, ("""Probability input is not a valid 
                                Pandas DataFrame object. Instead provided
                                %s"""%(type(self.probabilities)))

    def check_sum(self):
        """
        The method checks to make sure that the probabilities add up to
        1 across choices.

        Inputs:
        None
        """
        self.num_agents = self.probabilities.shape[0]
        self.num_choices = self.probabilities.shape[-1]
        # print 'OLD CUM SUM'
        #cumsum_across_rows = self.probabilities.cumsum(-1)[:,-1]
        # print cumsum_across_rows
        # print 'NEW CUM SUM'
        cumsum_across_rows = self.probabilities.sum(1)
        #print self.probabilities.head()
        #print cumsum_across_rows.head()
        cumsum_zeros_ind = cumsum_across_rows.isnull()
        
        diff_from_unity = Series.abs(cumsum_across_rows - 1)
        if cumsum_zeros_ind.any():
            check_sum_across = diff_from_unity[~cumsum_zeros_ind] < 1e-6
            #self.error = True
            #raw_input("Cumulative sum is zero")
        else:
            check_sum_across = diff_from_unity < 1e-6
            #self.error = False
        if not check_sum_across.all():
            raise ProbabilityError, """probability values do not add up """ \
                """to one across rows"""


    def check_valid_probabilities(self):
        """
        The method checks to make sure that the probabilities are not
        Nan.

        Inputs:
        None
        """
        nullProb = self.probabilities.isnull()
        if not nullProb.any().any():
            return
        else:
            #self.probabilities[nullProb] = 0
            print nullProb
            print self.probabilities
            #raise ProbabilityError,  "Some probabilities are not valid"
            raw_input("Some probabilities are not valid")

    def generate_random_numbers(self):
        """
        The method generates a random array for making the choice of
        the alternative.

        Inputs:
        None
        """
        # random.seed(seed=self.seed)
        #err = random.random((3,1))
        #f = open('test_res', 'a')
        #f.write('probability - %s' %self.seed)
        # f.write(str(list(err[:3,:])))
        # f.write('\n')
        # f.close()

        dist = RandomDistribution(self.seed)
        rand_numbers = dist.return_random_variables(self.num_agents)
        return rand_numbers

    def cumprob(self):
        """
        The method returns the cumulative probability array.

        Inputs:
        None
        """
        return self.probabilities.cumsum(1)

    def selected_choice(self):
        """
        The method returns the selected alternative for each agent.

        Inputs:
        None
        """
        choice = Series(zeros(self.num_agents), name="selected choice",  
                                index=self.probabilities.index)

        #choice = DataArray(zeros((self.num_agents, 1)), ["selected choice"], 
        #                             self.probabilities.index)
        random_numbers = self.generate_random_numbers()

        #self.prob_cumsum = self.cumprob().filled(-1)
        self.prob_cumsum = self.cumprob()
        
        self.prob_cumsum.fillna(-1,  inplace=True)

        for i in range(self.num_choices):
            # Indicator for the zero cells in the choice array
            #indicator_zero_cells = ones(self.num_agents)
            ##indicator = array([True] * self.num_agents)

            #zero_indices = choice == 0
            #indicator_zero_cells[~zero_indices] = ma.masked
            ##indicator[~zero_indices] = False

            # Indicator for the cells where the random number
            # is less than the probability
            #indicator_less_cells = ones(self.num_agents)
            #indicator_less_cells = array([True]*self.num_agents)
            if i == 0:
                indices = random_numbers < self.prob_cumsum.ix[:, i]
            else:
                indices = ((random_numbers < self.prob_cumsum.ix[:, i]) &
                                (random_numbers >= self.prob_cumsum.ix[:, i-1]))

            #indicator_less_cells[~less_indices] = ma.masked
            # indicator_less_cells
            #indicator[~less_indices] = False

            #indicator_less_zero_cells = indicator_zero_cells + indicator_less_cells

            #indicator_less_zero_cells = indicator_less_zero_cells == 2
            #choice.setcolumn("selected choice", i + 1, indices)
            choice.loc[indices] = i+1

        #choice.shape = (self.num_agents, 1)

        #alt_text = []
        # for i in choice:
        #    alt_text.append(self.choices[int(i[0])-1])
        #alt_text = array(alt_text)
        #alt_text.shape = (self.num_agents, 1)

        # return alt_text
        #return DataArray(choice, ['selected choice'], self.probabilities.index)
        #if self.error:
        #    print "choice is "
        #    print choice
        #    raw_input("check choice for invalid sum of prob")
        return choice

import unittest


class TestBadInputAbstractProbabilityModel(unittest.TestCase):

    def setUp(self):
        self.probabilities1 = [(0.5, 0.19, 0.31), (0.1, 0.2, 0.72)]
        self.probabilities2 = DataArray(array([[0.5, 0.29, 0.31], [0.1, 0.2, 0.7]]),
                                        ['ch1', 'ch2', 'ch3'])
        self.probabilities3 = DataArray(array(self.probabilities1),
                                        ['ch1', 'ch2', 'ch3'])

    def testprobabilitylist(self):
        self.assertRaises(
            DataError, AbstractProbabilityModel, self.probabilities1)

    def testvaluessum(self):
        self.assertRaises(ProbabilityError, AbstractProbabilityModel,
                          self.probabilities3)


class TestAbstractProbabilityModel(unittest.TestCase):

    def setUp(self):

        probabilities = array([[0.5, 0.19, 0.31], [0.1, 0.2, 0.7]])
        choices = ['ch1', 'ch2', 'ch3']
        self.model = AbstractProbabilityModel(
            DataArray(probabilities, choices))

    def testrandomvalues(self):
        random_array = array([0.417022, 0.72032449])
        random_numbers_frommodel = self.model.generate_random_numbers()
        diff_numbers = random_array - random_numbers_frommodel
        sum_diff_numbers = diff_numbers.sum()
        if sum_diff_numbers < 1e-6:
            sum_diff_numbers = 0
        self.assertEqual(0, sum_diff_numbers)

    def testcalculatecumprob(self):
        cumprob_array = array([[0.5, 0.69, 1.00], [0.1, 0.3, 1.0]])
        cumprob_array_frommodel = self.model.cumprob()
        diff_cumprob = cumprob_array - cumprob_array_frommodel
        diff_cumprob_sum = diff_cumprob.sum()
        if diff_cumprob_sum < 1e-6:
            diff_cumprob_sum = 0
        self.assertEqual(0, diff_cumprob_sum)

    def testchoicecolumns(self):
        #choice_array = array([['ch1'], ['ch3']])
        choice_array = array([[1], [3]])
        choice_array_frommodel = self.model.selected_choice()
        diff_choice = all(choice_array == choice_array_frommodel.data)
        self.assertEqual(True, diff_choice)


if __name__ == '__main__':
    unittest.main()
