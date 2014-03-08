
from numpy import array, absolute
from openamos.core.data_array import DataArray
from openamos.core.models.linear_regression_model import LinearRegressionModel
from openamos.core.models.error_specification import LinearRegErrorSpecification



class ColumnOperationsModel(LinearRegressionModel):
    def __init__(self, specification):
	error_specification = LinearRegErrorSpecification(array([[0]]))
	LinearRegressionModel.__init__(self, specification, error_specification)

	
    def calc_scalar(self, data, seed=1):
        """
        The method returns the predicted value for the different choices in the 
        specification input.
        
        Inputs:
        data - DataArray object
        """
        if seed == None:
            raise Exception, "linear"


        expected_value = self.calc_expected_value(data)
	if self.specification.scalarCalcType == 'Sum':
	    pred_value = expected_value.data.sum()

	if self.specification.scalarCalcType == 'Absolute Sum':
	    pred_value = absolute(expected_value.data).sum()


	return DataArray(array([[pred_value]]), self.specification.choices)
