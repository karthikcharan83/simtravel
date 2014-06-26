from numpy import ndarray
from openamos.core.errors import ErrorSpecificationError


class ErrorSpecification(object):

    """
    This is the base class for specifying the attributes of the error for any
    regression model.

    Inputs:
    variance - array of numeric values (covariance matrix)
    distribution - string (type of distribution)     
    """

    def __init__(self, variance, distribution):
        self.variance = variance

        if not isinstance(self.variance, ndarray):
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the input - variance must be an ndarray object"""

        type_variance = self.variance.dtype
        if type_variance not in [int, float]:
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the input - variance entries are not all numeric"""

        if not isinstance(distribution, str):
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the input - distribution must be a str object"""

        if self.variance.shape[0] <> self.variance.shape[1]:
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the input - variance must be a squre array"""

        self.num_err_components = self.variance.shape[0]
        self.distribution = distribution.lower()


class StochasticRegErrorSpecification(ErrorSpecification):

    """
    This is the class for specifying the stochastic regression error component.

    Inputs:
    variance - numeric array (covariance matrix)
    distribution - string (type of distribution)
    """

    def __init__(self, variance, vertex, lower_threshold=0, upper_threshold=0):
        ErrorSpecification.__init__(
            self, variance, distribution='normal_halfnormal')

        if self.num_err_components <> 2:
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the  input - variance should contain two error components -  """\
                """a normal and a half-normal error component"""

        if not (self.variance[0, 1] == 0 and self.variance[1, 0] == 0):
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the input - variance should contain independent error """\
                """components; the variance matrix supplied implies """\
                """correlation among the error components"""

        if vertex.lower() not in ['start', 'end']:
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the input - vertex should take a value - start or end; this """\
                """determines how the predicted value of the frontier """\
                """is calculated"""
        self.vertex = vertex.lower()

        if type(lower_threshold) not in [int, float]:
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the threshold should take a numeric value. The LOWER threshold """\
                """is used to capoff the start and end values."""

        if type(upper_threshold) not in [int, float]:
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the threshold should take a numeric value. The UPPER threshold """\
                """is used to capoff the start and end values."""

        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold


class LinearRegErrorSpecification(ErrorSpecification):

    """
    This is the class for specifying the normal regression error component.

    Inputs:
    variance - numeric arrray (covariance matrix)
    distribution - string (type of distribution)
    """

    def __init__(self, variance, vertex=None, lower_threshold=0, upper_threshold=0):
        ErrorSpecification.__init__(self, variance, distribution='normal')

        if self.num_err_components > 1:
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the input - variance should contain only one error component"""

        if vertex is not None:
            if vertex.lower() not in ['start', 'end']:
                raise ErrorSpecificationError, """the error specification is invalid, """\
                    """the input - vertex should take a value - start or end; this """\
                    """determines how the predicted value of the frontier """\
                    """is calculated"""
            self.vertex = vertex.lower()
        else:
            self.vertex = None

        if type(lower_threshold) not in [int, float]:
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the threshold should take a numeric value. The LOWER threshold """\
                """is used to capoff the start and end values."""

        if type(upper_threshold) not in [int, float]:
            raise ErrorSpecificationError, """the error specification is invalid, """\
                """the threshold should take a numeric value. The UPPER threshold """\
                """is used to capoff the start and end values."""

        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold


import unittest
from numpy import array


class TestBadErrorSpecification(unittest.TestCase):

    def setUp(self):
        self.variance = array([[1.1]])
        self.variance1 = [[1.1]]
        self.variance2 = array([['1.1']])
        self.variance3 = array([[1., 2., 3.], [1.1, 2.1, 3.1]])
        self.variance4 = array([[]])

        # TODO: for classic linear regression also check for the number of error
        # components specified
        # In the current implementation it also supports specification of
        # multiple error components

        self.distribution = 1

    def testvarianceinputs(self):
        self.assertRaises(ErrorSpecificationError, ErrorSpecification,
                          self.variance1, 'normal')
        self.assertRaises(ErrorSpecificationError, ErrorSpecification,
                          self.variance2, 'normal')
        self.assertRaises(ErrorSpecificationError, ErrorSpecification,
                          self.variance3, 'normal')
        self.assertRaises(ErrorSpecificationError, ErrorSpecification,
                          self.variance4, 'normal')
        self.assertRaises(ErrorSpecificationError, ErrorSpecification,
                          self.variance, self.distribution)


class TestBadLinearRegErrorSpecification(unittest.TestCase):

    def setUp(self):
        self.variance = array([[1., 2., 3.], [1.1, 2.1, 3.1], [1.2, 2.2, 3.2]])

    def testerrorcomponentssize(self):
        self.assertRaises(ErrorSpecificationError, LinearRegErrorSpecification,
                          self.variance)


class TestLinearRegErrorSpecification(unittest.TestCase):

    def setUp(self):
        self.variance = array([[1.]])

    def testerrcomponentsize(self):
        err_spec = LinearRegErrorSpecification(self.variance)
        self.assertEqual(1, err_spec.num_err_components)


class TestBadStochasticRegErrorSpecification(unittest.TestCase):

    def setUp(self):
        self.variance = array([[1., 2.], [1.1, 2.1]])
        self.variance1 = array(
            [[1., 2., 3.], [1.1, 2.1, 3.1], [1.2, 2.2, 3.2]])
        self.variance2 = array([[1.]])
        self.variance3 = array([[1., 0], [1.1, 2.1]])
        self.variance4 = array([[1., 2.], [0, 2.1]])

        self.vertex_st = 'start'
        self.vertex_end = 'end'
        self.vertex1 = 'initial'

    def testerrorcomponentssize(self):
        self.assertRaises(ErrorSpecificationError, StochasticRegErrorSpecification,
                          self.variance1, self.vertex_st)
        self.assertRaises(ErrorSpecificationError, StochasticRegErrorSpecification,
                          self.variance2, self.vertex_end)

    def testindeperrorcomponents(self):
        self.assertRaises(ErrorSpecificationError, StochasticRegErrorSpecification,
                          self.variance3, self.vertex_st)
        self.assertRaises(ErrorSpecificationError, StochasticRegErrorSpecification,
                          self.variance4, self.vertex_end)

    def testvertexspec(self):
        self.assertRaises(ErrorSpecificationError, StochasticRegErrorSpecification,
                          self.variance, self.vertex1)


class TestStochasticRegErrorSpecification(unittest.TestCase):

    def setUp(self):
        self.variance = array([[1., 0], [0, 2.1]])
        self.vertex_st = 'start'

    def testerrorvertexspec(self):
        err_spec = StochasticRegErrorSpecification(
            self.variance, self.vertex_st)
        self.assertEquals('start', err_spec.vertex)


if __name__ == '__main__':
    unittest.main()
