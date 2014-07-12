from numpy import all
from openamos.core.models.abstract_regression_model import AbstractRegressionModel
from openamos.core.models.abstract_random_distribution_model import RandomDistribution
from openamos.core.errors import ErrorSpecificationError

from pandas import DataFrame as df

class LinearRegressionModel(AbstractRegressionModel):

    """
    This is the base class for linear regression model in OpenAMOS.

    Inputs:
    specification - Specification object
    error_specification - ErrorSpecification object
    """

    def __init__(self, specification, error_specification):
        AbstractRegressionModel.__init__(
            self, specification, error_specification)

        if not isinstance(error_specification, LinearRegErrorSpecification):
            raise ErrorSpecificationError, """incorrect error specification; it """\
                """should be LinearRegErrroSpecification object"""

    def calc_errorcomponent(self, size, mean=0, sd=1, seed=1):
        """
        The method returns the contribution of the error in the calculation
        of the predicted value for the different choices.

        Inputs:
        size - numeric value (number of rows)
        mean - numeric value (mean)
        sd - numeric value (standard deviation)
        """
        dist = RandomDistribution(seed=seed)
        err_norm = dist.return_normal_variables(
            location=mean, scale=sd, size=size)
        return err_norm

    def calc_halfnormal_error(self, threshold, limit, seed, size):
        """
        A draw from a half normal distribution with 3 s.d. = abs(threshold - limit)
        For smoothing about the boundaries

        """

        dist = RandomDistribution(seed=seed)

        assu_scale = abs(threshold - limit) / 3.0
        err_halfnorm = dist.return_half_normal_variables(
            location=0, scale=assu_scale, size=size)

        chkRowsMore = err_halfnorm > abs(threshold - limit)
        err_halfnorm[chkRowsMore] = abs(threshold - limit)

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
        variance = self.error_specification.variance[0, 0]
        err = self.calc_errorcomponent(size=(data.rows, 1),
                                              mean=0,
                                              sd=variance ** 0.5, seed=seed)
        pred_value = expected_value + err

        # upper threshold - lower threshold is assumed to be 2 sd
        # scattering the points at lower threshold/upper threshold dispersed by
        # a half normal distribution with a sd as calculated above as the size

        if (self.error_specification.lower_threshold == 0 or
             self.error_specification.upper_threshold == 0):
                 return pred_value

        standDev = (self.error_specification.upper_threshold -
                    self.error_specification.lower_threshold) / 2
        #print 'lower threshold - ', self.error_specification.lower_threshold
        #print 'upper threshold - ', self.error_specification.upper_threshold
        #raw_input()
        # print 'sd - ', self.error_specification.upper_threshold
        
        lowerLimit = self.error_specification.lower_threshold - standDev
        upperLimit = self.error_specification.upper_threshold + standDev

        if lowerLimit < 5:
            lowerLimit = 5

        if upperLimit > 1435:
            upperLimit = 1435

        # print 'lower limit ', lowerLimit
        # print 'upper limit', upperLimit
        # raw_input()

        if self.error_specification.lower_threshold > 0:
            threshold = self.error_specification.lower_threshold
            predValue_lessThresholdInd = (pred_value < threshold).values
            pred_value[predValue_lessThresholdInd] = threshold

            if predValue_lessThresholdInd.any():
                numRows = predValue_lessThresholdInd.sum()
                size = (numRows, 1)
                smoothingErr = self.calc_halfnormal_error(
                    threshold, lowerLimit, seed, size)
                pred_value[predValue_lessThresholdInd] -= smoothingErr

        if self.error_specification.upper_threshold > 0:
            threshold = self.error_specification.upper_threshold
            predValue_moreThresholdInd = (pred_value > threshold).values
            pred_value[predValue_moreThresholdInd] = threshold

            if predValue_moreThresholdInd.any():
                numRows = predValue_moreThresholdInd.sum()
                size = (numRows, 1)
                smoothingErr = self.calc_halfnormal_error(
                    threshold, upperLimit, seed, size)
                pred_value[predValue_moreThresholdInd] += smoothingErr
        return pred_value


import unittest
from numpy import array
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification
from openamos.core.models.error_specification import LinearRegErrorSpecification


class TestLinearRegressionModel(unittest.TestCase):

    def setUp(self):
        choice = ['DURATION']
        coefficients = [{'constant': 2, 'Var1': 2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])
        variance = array([[1]])

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.specification = Specification(choice, coefficients)
        self.errorspecification = LinearRegErrorSpecification(variance)

    def testvalues(self):
        model = LinearRegressionModel(
            self.specification, self.errorspecification)
        pred_value = model.calc_predvalue(self.data)

        expected_act = self.data.calculate_equation(
            self.specification.coefficients[0])
        expected_act.shape = (4, 1)

        dist = RandomDistribution(seed=1)
        pred_act = dist.return_normal_variables(
            location=expected_act, scale=1, size=(4, 1))

        pred_diff = all(pred_value.data == pred_act)
        self.assertEqual(True, pred_diff)


if __name__ == '__main__':
    unittest.main()

