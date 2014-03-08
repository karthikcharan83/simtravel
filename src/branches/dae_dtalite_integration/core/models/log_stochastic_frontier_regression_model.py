import numexpr as ne

from openamos.core.data_array import DataArray
from openamos.core.models.stochastic_frontier_regression_model import StocFronRegressionModel

class LogStocFronRegressionModel(StocFronRegressionModel):
    """
    This is the base class for log-stochastic frontier 
    regression model in OpenAMOS
    """

    def __init__(self, specification, error_specification):
        StocFronRegressionModel.__init__(self, specification, error_specification)


    def calc_predvalue(self, data, seed=1):
        """
        This method returns the predicted value for the 
        choice in the specification input.

        Inputs:
        data - DataArray object
        """

        expected_value = self.calc_expected_value(data)
        variance_norm = self.error_specification.variance[0,0]
        variance_halfnorm = self.error_specification.variance[1,1]
        vertex = self.error_specification.vertex
        #threshold = self.error_specification.threshold
        size = (data.rows, 1)

        err = self.calc_errorcomponent(variance_norm, variance_halfnorm, 
                                       vertex, size, seed)
        
        ln_pred_value = expected_value.data + err
        
        pred_value = ne.evaluate("exp(ln_pred_value)")
        
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

        
        
#TODO: Unit Test
