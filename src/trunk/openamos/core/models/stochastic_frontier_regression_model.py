from scipy.stats import norm
from numpy import random
from openamos.core.models.abstract_regression_model import AbstractRegressionModel
from openamos.core.errors import ErrorSpecificationError
from openamos.core.models.abstract_random_distribution_model import RandomDistribution

class StocFronRegressionModel(AbstractRegressionModel):
    """
    This is teh base class for stochastic frontier regression models in OpenAMOS.

    Inputs:
    specification - Specification object
    error_specification - StochasticRegErrorSpecification object
    """
    def __init__(self, specification, error_specification):
        AbstractRegressionModel.__init__(self, specification, error_specification)

        if not isinstance(error_specification, StochasticRegErrorSpecification):
            raise ErrorSpecificationError, """incorrect error specification; it """\
                """should be StochasticRegErrroSpecification object"""

    def calc_errorcomponent(self, variance_norm, variance_halfnorm,
                            vertex, size, seed):
        """
        The method returns the contribution of the error component in the
        calculation of the predicted value for the different choices.

        Inputs:
        variance_norm - numeric value (variance of the normal portion of error)
        variance_halfnorm - numeric value (variance of the half normal portion of
                                        error)
        vertex - string (the vertext to predict -- start/end)
        size - numeric value (number of rows)

        """

        dist = RandomDistribution(seed=seed)
        err_halfnorm = dist.return_half_normal_variables(location=0, scale=variance_halfnorm**0.5, size=size)

        dist = RandomDistribution(seed=seed)
        err_norm = dist.return_normal_variables(location=0, scale=variance_norm**0.5, size=size)

        if vertex == 'start':
            return err_norm + err_halfnorm

        if vertex == 'end':
            return err_norm - err_halfnorm

    def calc_halfnormal_error(self, threshold, limit, seed, size):
        """
        A draw from a half normal distribution with 3 s.d. = abs(threshold - limit)
        For smoothing about the boundaries

        """

        dist = RandomDistribution(seed=seed)

        assu_scale = abs(threshold-limit)/3.0
        err_halfnorm = dist.return_half_normal_variables(location=0, scale=assu_scale, size=size)

        chkRowsMore = err_halfnorm > abs(threshold-limit)
        err_halfnorm[chkRowsMore] = abs(threshold-limit)

        return err_halfnorm



    def calc_predvalue(self, data, seed=1):
        """
        The method returns the predicted value for the different choices in the
        specification input.

        Inputs:
        data - DataArray object
        """
        if seed == None:
            raise Exception, "linear"

        expected_value = self.calc_expected_value(data)
        variance_norm = self.error_specification.variance[0,0]
        variance_halfnorm = self.error_specification.variance[1,1]
        vertex = self.error_specification.vertex
        #threshold = self.error_specification.threshold
        size = (data.rows, 1)

        err = self.calc_errorcomponent(variance_norm, variance_halfnorm,
                                       vertex, size, seed)

        pred_value = expected_value.data + err


        # upper threshold - lower threshold is assumed to be 2 sd
        # scattering the points at lower threshold/upper threshold dispersed by
        # a half normal distribution with a sd as calculated above as the size


        standDev = (self.error_specification.upper_threshold -
                    self.error_specification.lower_threshold)/2
        #print 'lower threshold - ', self.error_specification.lower_threshold
        #print 'upper threshold - ', self.error_specification.upper_threshold
        #print 'sd - ', self.error_specification.upper_threshold


        lowerLimit = self.error_specification.lower_threshold - standDev
        upperLimit = self.error_specification.lower_threshold + standDev

        if lowerLimit < 5:
            lowerLimit = 5

        if upperLimit > 1435:
            upperLimit = 1435

        #print 'lower limit ', lowerLimit
        #print 'upper limit', upperLimit
        #raw_input()

        if self.error_specification.lower_threshold >0:
            threshold = self.error_specification.lower_threshold
            predValue_lessThresholdInd = pred_value < threshold
            numRows = predValue_lessThresholdInd.sum()

            pred_value[predValue_lessThresholdInd] = threshold

            if numRows > 0:
                size = (numRows, 1)
                smoothingErr = self.calc_halfnormal_error(threshold, lowerLimit, seed, size)
                pred_value[predValue_lessThresholdInd] -= smoothingErr[:,0]


        if self.error_specification.upper_threshold >0:
            threshold = self.error_specification.upper_threshold
            predValue_moreThresholdInd = pred_value > threshold
            numRows = predValue_moreThresholdInd.sum()

            pred_value[predValue_moreThresholdInd] = threshold

            if numRows > 0:
                size = (numRows, 1)
                smoothingErr = self.calc_halfnormal_error(threshold, upperLimit, seed, size)
                pred_value[predValue_moreThresholdInd] += smoothingErr[:,0]

        return DataArray(pred_value, self.specification.choices)


import unittest
from numpy import array
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification
from openamos.core.models.error_specification import StochasticRegErrorSpecification

class TestStocFronRegressionModel(unittest.TestCase):
    def setUp(self):
        choice = ['Frontier']
        coefficients = [{'constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])
        variance = array([[1., 0], [0, 1.1]])

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.specification = Specification(choice, coefficients)
        self.errorspecification = StochasticRegErrorSpecification(variance, 'start')


    def testvalues(self):
        model = StocFronRegressionModel(self.specification,
                                        self.errorspecification)
        pred_value = model.calc_predvalue(self.data)

        expected_act = self.data.calculate_equation(
                                                    self.specification.coefficients[0])
        expected_act.shape = (4,1)
        variance = self.errorspecification.variance

        dist = RandomDistribution(seed=1)
        err_norm = dist.return_normal_variables(location=0, scale=variance[0,0]**0.5, size=(4,1))

        pred_act = (expected_act + err_norm)

        pred_diff = all(pred_value.data == pred_act)
        self.assertEquals(True, pred_diff)

if __name__ == '__main__':
    unittest.main()
