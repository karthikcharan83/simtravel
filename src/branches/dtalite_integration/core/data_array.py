import re
import time
import pandas as pd
from pandas import DataFrame as df
from pandas import Series

import numpy as np

from openamos.core.errors import DataError

class DataArray(object):

    def __init__(self, data=None, varnames=None, index=None, indexCols=None):
        # TODO:index
        if varnames is not None:
            for varname in varnames:
                self.check_varname(varname)
        else:
            varnames = []
        try:
            self.data = df(data, columns=varnames, index=index)
        except Exception, e:
            raise DataError, ("""Error creating the data frame object
                              with the dataset:%s""" % e)
        if index is not None and indexCols is not None:
            raise DataError,  ("""Conflicting indexes specified. Both
            index and indexCol inputs cannot be specified.""")
        self.update_meta_data()
        if indexCols is not None:
            self.create_index_using_cols(indexCols)

    def create_index_using_cols(self, columnameList):
        if len(columnameList) == 0:
            raise DataError("""No valid column names specified.""")

        for columname in columnameList:
            self.check_varname_exists(columname)

        self.data.set_index(columnameList, inplace=True,  drop=False)
        #print self.data.head()
        self.data.sort(columnameList, inplace=True)
        #print self.data.head()
        self.update_meta_data()
        #raw_input("--check sort--")

    def update_meta_data(self):
        self.varnames = list(self.data.columns.values)
        self.rows = self.data.shape[0]
        self.cols = self.data.shape[1]
        self.index = self.data.index

    def check_varname(self, varname):
        if type(varname) is not str:
            raise DataError, ("Variable name is not a valid string")
        firstchar = varname[0]
        match = re.match('[0-9]', firstchar)
        if match is not None:
            raise DataError, ("""Variable name is not a valid string -
                              first character is invalid""")

    def sort(self, columnames):
        if not isinstance(columnames, list):
            raise DataError, ("""The column names argument must be a
                              python list object""")
        self.data.sort(columnames, inplace=True)
        self.update_meta_data()

    def check_varname_exists(self, varname):
        if not isinstance(varname,  str):
            print varname,  "--<"
            raise DataError, ("Variable name is not a valid string - %s")
        firstchar = varname[0]
        match = re.match('[0-9]', firstchar)
        if match is not None:
            raise DataError, ("""Variable name is not a valid string -
                              first character is invalid""")
        if varname not in self.varnames:
            raise DataError, ("""Reference to a column - %s that does
                              not exist in the dataset""" % varname)

    def calculate_equation1(self, coefficients, rows=None):
        t = time.time()
        res = self.calculate_equation_eval(coefficients, rows)
        print res.head()
        print "Result calculated with eval in %.6f" % (time.time() - t)

        t = time.time()
        res = self.calculate_equation_noeval(coefficients, rows)
        print res.head()
        print "Result calculated without eval in %.6f" % (time.time() - t)

    def calculate_equation_eval(self, coefficients, rows=None):
        evalStr = ""
        for var in coefficients.keys():
            coeff = coefficients[var]
            print var,  type(var)
            if isinstance(var,  tuple):
                print "product found"
                prod="1"
                for k in var:
                    if k[:4] == 'inv_':
                        k = k[4:]
                        prod +="/%s"%k
                    else:
                        prod += "*%s"%k
                var = prod
            evalStr += "%s * %s+" %(var,  coeff)
        evalStr = evalStr[:-1]
        print evalStr
        return self.data.eval(evalStr)



    def calculate_equation(self, coefficients, rows=None):
        #print coefficients
        t = time.time()

        res = Series(np.zeros(self.rows), index=self.index)
        if not isinstance(coefficients, dict):
            raise DataError, ("""Coefficient argument should be a
                              python dictionary type""")
        #print "These are the coefficients", coefficients
        for coeff in coefficients.keys():
            # Checking coefficient name
            if type(coeff) is str:
                #self.check_varname_exists(coeff)
                varCol = self.data[coeff]

            # Checking and storing derived variables with inverse calculation
            prodCoeffDict = {}
            inverseDict = {}
            if type(coeff) is tuple:
                for k in coeff:
                    if k[:4] == 'inv_':
                        k = k[4:]
                        #self.check_varname_exists(k)
                        inverseDict[k] = True
                    prodCoeffDict[k] = 1.
                varCol = self.calculate_product(
                    prodCoeffDict, inverse=inverseDict)

            # Checking value of coefficient
            try:
                coeffval = coefficients[coeff]
                float(coeffval)
            except ValueError, e:
                raise DataError, ("""Enter valid value for coefficient -
                                  %s - %s""" (coeff, coeffval))
            #print "before coeff", coeff, "coeffval-", coeffval, res.head()
            #print "variable Col", varCol.head()
            res = res + varCol * coeffval
            #print "variable Col", varCol
        if rows is not None:
            res = res[rows]
        #print "Sum calculated in %.4f" % (time.time() - t)
        #print "Result", res
        return res

    def calculate_product_(self, coefficients, rows=None, inverse={}):
        t = time.time()
        res = self.calculate_product_eval(coefficients, rows)
        print "Product calculated with eval in %.6f" % (time.time() - t)
        
        t = time.time()
        res = self.calculate_product_noeval(coefficients, rows)
        print "Product calculated without eval in %.6f" % (time.time() - t)


    def calculate_product_eval_(self, coefficients, rows=None, inverse={}):
        print coefficients
        evalStr = ""
        for var in coefficients.keys():
            if isinstance(var,  tuple):
                pass
            evalStr += "%s * %s+" %(var,  coefficients[var])
        evalStr = evalStr[:-1]
        print evalStr


    def calculate_product(self, coefficients, rows=None, inverse={}):
        t = time.time()
        res = Series(np.ones(self.rows), index=self.index)
        if not isinstance(coefficients, dict):
            raise DataError, ("""Coefficient argument should be a
                              python dictionary type""")

        for coeff in coefficients.keys():
            # Checking coefficient name
            #self.check_varname_exists(coeff)
            varCol = self.data[coeff]

            # Checking value of coefficient
            try:
                coeffval = coefficients[coeff]
                float(coeffval)
            except ValueError, e:
                raise DataError, ("""Enter valid value for coefficient -
                                  %s - %s""" (coeff, coeffval))
            if coeff in inverse:
                # Checking for rows where value is zero and converting the
                # inverse to 1 and the corresponding derived product value
                # to zero because we cannot calculate 1 over zero
                nanRows = varCol == 0
                varCol = 1 / varCol
                if nanRows.any():
                    varCol[nanRows] = 0

            res = res * varCol * coeffval


        if rows is not None:
            res = res[rows]
        #print "Product calculated in %.4f" % (time.time() - t)
        return res

    def exp_calculate_equation(self, coefficients):
        res = self.calculate_equation(coefficients)
        res = res.apply(np.exp)

        return res

    def column(self, columname):
        self.check_varname_exists(columname)
        return self.data[columname]

    def setcolumn1(self, columname, values, rows=None, start=None, end=None):
        #print "\n--->Before setting values for ",  columname
        #print self.data[columname].head()
        t = time.time()

        self.check_varname_exists(columname)
        if isinstance(values, df) and rows is not None:
            self.data.loc[rows, columname] = values.values
        elif isinstance(values, np.ndarray) and rows is not None:
            self.data.loc[rows, columname] = values
        elif isinstance(values, df) and rows is None:
            self.data.loc[:, columname] = values.values
        elif isinstance(values, np.ndarray) and rows is None:
            self.data.loc[:, columname] = values
        elif rows is not None:
            self.data.loc[rows, columname] = values
        else:
            self.data.loc[:, columname] = values            

        #print "\n--->After setting values for ",  columname
        #print self.data[columname].head()
        print "Column set in %.4f" %(time.time()-t)


    def insertcolumn(self, columnameList, values):
        if self.rows <> values.shape[0]:
            raise DataError, ("""The number of rows in the dataset and
                              the values column are not the same""")

        if type(columnameList) == str:
            columnameList = [columnameList]

        for i in range(len(columnameList)):
            columname = columnameList[i]
            self.data[columname] = values[:, i]
        self.update_meta_data()

    def scaledowncolumn(self, columname, scale):
        self.check_varname_exists(columname)
        if type(scale) not in [int, float]:
            raise DataError, "The scale value is not a valid number"
        self.data[columname] = self.data[columname] / scale

    def addtocolumn(self, columname, values):
        self.check_varname_exists(columname)
        try:
            self.data[columname] = self.data[columname] + values
        except Exception, e:
            raise DataError, ("""Error adding values - %s""" % e)

    def expofcolumn(self, columname):
        self.check_varname_exists(columname)
        self.data[columname].apply(np.exp)

    def deleterows(self, rows=None):
        if rows.shape == (0,):
            return
        self.data = self.data[rows]
        self.update_meta_data()

    def columns(self, columnameList, rows=None):
        ti = time.time()
        if not isinstance(columnameList, list):
            raise DataError, ("""The column names attribute should be a python
                        list of variable names - %s
                        """%columnameList)
        for columname in columnameList:
            self.check_varname_exists(columname)

        if rows is not None:
            colData = DataArray(self.data[rows][columnameList], columnameList, self.index[rows])
        else:
            colData = DataArray(self.data[columnameList], columnameList, self.index)
        print "Time taken to extract and create DataArray obj is %.6f" %(time.time()-ti)
        return colData

    def columnsOfType(self, columnames, rows=None, colTypes=None):
        if colTypes == None:
            return self.columns(columnames, rows)

        dataSubset = self.columns(columnames, rows)
        for i in range(len(columnames)):
            colName = columnames[i]
            colType = colTypes[colName]
            dataSubset.data[colName] = dataSubset.data[colName].astype(colType, copy=True)
        return dataSubset


    def rowsof(self, rows):
        return DataArray(self.data.ix[rows, :], self.data.columns.values, self.index[rows])

    def __repr__(self):
        return repr(self.data)

    def __lt__(self, value):
        if value is None:
            raise DataError, "Cannot compare when value is None"
        return self.data < value

    def __gt__(self, value):
        if value is None:
            raise DataError, "Cannot compare when value is None"
        return self.data > value

    def __le__(self, value):
        if value is None:
            raise DataError, "Cannot compare when value is None"
        return self.data <= value

    def __ge__(self, value):
        if value is None:
            raise DataError, "Cannot compare when value is None"
        return self.data >= value

    def __eq__(self, value):
        if value is None:
            raise DataError, "Cannot compare when value is None"
        return self.data == value

    def __ne__(self, value):
        if value is None:
            raise DataError, "Cannot compare when value is None"
        return self.data <> value


class DataFilter(object):

    def __init__(self, varname, filterString, value, filterType=None):
        if not isinstance(varname, str):
            raise DataError, ("""Variable name input has to be
                              a string object""")
        self.varname = varname

        if not isinstance(filterString, str):
            raise DateError, ("""Filter string has to be a valid
                              string object""")
        self.filterString = filterString

        value_type = type(value)
        if value_type in [int, float, str]:
            self.value = value
        else:
            raise DataError, ("""the value has to be a valid numeric object or ;
                              a valid column name string object
                              only 'float', 'int', 'str' objects are accepted checking to see
                              if a column was specified instead for the value to check against. """)

    def compare(self, data):
        if type(self.value) == str:
            valueToCompareAgainst = data.column(self.value)
        else:
            valueToCompareAgainst = self.value

        if self.filterString == "less than":
            valid_rows = data.column(self.varname) < valueToCompareAgainst

        if self.filterString == "greater than":
            valid_rows = data.column(self.varname) > valueToCompareAgainst

        if self.filterString == "less than equals":
            valid_rows = data.column(self.varname) <= valueToCompareAgainst

        if self.filterString == "greater than equals":
            valid_rows = data.column(self.varname) >= valueToCompareAgainst

        if self.filterString == "equals":
            valid_rows = data.column(self.varname) == valueToCompareAgainst

        if self.filterString == "not equals":
            valid_rows = data.column(self.varname) <> valueToCompareAgainst

        return valid_rows

    def __repr__(self):
        return ('Data Filter Object %s %s %s'
                % (self.varname, self.filterString, self.value))


if __name__ == "__main__":
    from numpy import random

    random.seed(1)

    darr = DataArray(
        random.random_integers(0, 10, (10000, 3)), ["first", "second", "third"])
    print "Original"
    print darr.data.head()

    ti = time.time()
    coefficients = {'first': 1.0, 'second': 1.0, 'first': 1.0, 'second': 1.0, 
                            'first': 1.0, 'second': 1.0, 'first': 1.0, 'second': 1.0, 
                            'first': 1.0, 'second': 1.0}
    res = darr.calculate_equation(coefficients)
    print "Addition in %.8f\n" %(time.time()-ti)

    ti = time.time()
    coefficients = {'first': 1.0, ('second', 'inv_third'): 1.0, 'first': 1.0, ('second', 'inv_third'): 1.0, 
                            'first': 1.0, ('second', 'inv_third'): 1.0, 'first': 1.0, ('second', 'inv_third'): 1.0}
    res = darr.calculate_equation(coefficients)
    print "Addition with inverse (uses product) in %.8f\n" %(time.time()-ti)
    
    ti = time.time()
    for i in range(5):
        darr.data.loc[:,"res%s"%i] = res
    print "Assigning in %.8f\n" %(time.time()-ti)

    ti = time.time()
    for i in range(5):
        darr.data.ix[:,"res2%s"%i] = res
    print "Assigning in %.8f\n" %(time.time()-ti)

    darr.update_meta_data()
    ti = time.time()
    for i in range(5):
        res = darr.columns(['res0', 'res1', 'res2', 'res3'], darr.data["first"]>4)
        print res.rows,  (darr.data["first"]>4).sum()
    print "Columns in in %.8f\n" %(time.time()-ti)


    """
    ti = time.time()
    res = darr.data.eval("first*1 + second*1")
    print "Addition eval in %.8f\n" %(time.time()-ti)

    ti = time.time()
    res = darr.data.eval("first*1+second/third*1")
    print "Addition with inverse (uses product) eval in %.8f\n" %(time.time()-ti)
    """

    """
    print "Sorted by first and third"
    darr.sort(["first", "third"])
    print darr
    raw_input("Check")

    print "Addition"
    coefficients = {'first': 1.0, 'second': 1.0}
    res = darr.calculate_equation(coefficients)
    print res
    raw_input("Check")

    print "Addition with one column"
    coefficients = {'first': 1.0}
    res = darr.calculate_equation(coefficients)
    print res
    raw_input("Check")
    
    print "exponent"
    res = darr.exp_calculate_equation(coefficients)
    print res
    raw_input("Check")
    
    print "Product"
    coefficients = {'first': 1.0, 'second': 1.0}
    res = darr.calculate_product(coefficients, inverse={'second': True})
    print res
    raw_input("Check")
    
    print "Retrieve Column"
    print darr.column("third")
    raw_input("Check")

    print "Add Column"
    print darr.insertcolumn("fifth", random.random_integers(0, 10, (10, 1)))
    print darr
    raw_input("Check")
    
    print "Add Columns"
    print darr.insertcolumn(["sixth", "seventh"], random.random_integers(0, 10, (10, 2)))
    print darr
    raw_input("Check")
    """
