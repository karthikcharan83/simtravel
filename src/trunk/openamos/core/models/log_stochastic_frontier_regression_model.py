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
        
	if self.error_specification.lower_threshold >0:
	    threshold = self.error_specification.lower_threshold
	    predValue_lessThresholdInd = pred_value < threshold
            print '\t\tPred value is less than START threshold for - %d cases ' \
                % predValue_lessThresholdInd.sum()
            pred_value[predValue_lessThresholdInd] = threshold


	if self.error_specification.upper_threshold >0:
	    threshold = self.error_specification.upper_threshold
	    predValue_moreThresholdInd = pred_value > threshold
            print '\t\tPred value is greater than END threshold for - %d cases ' \
                % predValue_moreThresholdInd.sum()
            pred_value[predValue_moreThresholdInd] = threshold


	if self.error_specification.lower_threshold >0:
	    threshold = self.error_specification.lower_threshold
	    predValue_lessThresholdInd = pred_value < threshold
	    numRows = predValue_lessThresholdInd.sum()
            print '\t\tPred value is less than START threshold for - %d cases ' \
                % numRows
	    
            pred_value[predValue_lessThresholdInd] = threshold
	    print 'Lower; Before', pred_value[predValue_lessThresholdInd]
	    size = (numRows, )
	    smoothingErr = self.calc_halfnormal_error(threshold, 1, seed, size)
	    print smoothingErr.shape, pred_value[predValue_lessThresholdInd].shape
	    pred_value[predValue_lessThresholdInd] -= smoothingErr
	    print 'Lower; After', pred_value[predValue_lessThresholdInd]


	if self.error_specification.upper_threshold >0:
	    threshold = self.error_specification.upper_threshold
	    predValue_moreThresholdInd = pred_value > threshold
	    numRows = predValue_moreThresholdInd.sum()
            print '\t\tPred value is greater than END threshold for - %d cases ' \
                % numRows
		
            pred_value[predValue_moreThresholdInd] = threshold
	    print 'Upper; Before - ', pred_value[predValue_moreThresholdInd]
	    size = (numRows, )
	    smoothingErr = self.calc_halfnormal_error(threshold, 1438, seed, size)
	    print smoothingErr.shape, pred_value[predValue_moreThresholdInd].shape
	    pred_value[predValue_moreThresholdInd] += smoothingErr
	    print 'Upper; After - ', pred_value[predValue_moreThresholdInd]

        return DataArray(pred_value, self.specification.choices)

        
        
#TODO: Unit Test
