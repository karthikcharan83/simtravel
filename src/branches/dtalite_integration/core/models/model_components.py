import re
from openamos.core.errors import SpecificationError, ChoicesError, CoefficientsError


class Specification(object):

    """
    This is the base class for specifying models and their coefficients.

    Inputs:
    choices - list of strings
    coefficients - list of dictionaries; dictionary is {'variable':'coefficients'}
    """

    def __init__(self, choices, coefficients, inverse=[{}]):
        self.choices = choices
        self.coefficients = coefficients
        self.check()
        self.convert_to_lowercase()
        self.number_choices = self.num_choices()
        self.inverse = inverse

    def check(self):
        checkVal, checkText = self.check_text_only(self.choices)
        if not checkVal:
            raise ChoicesError, checkText

        checkVal, checkText = self.check_each_dict(self.coefficients)
        if not checkVal:
            raise CoefficientsError, checkText

        checkVal, checkText = self.check_specification_consistency(self.choices,
                                                                   self.coefficients)

        if not checkVal:
            raise SpecificationError, checkText

    def convert_to_lowercase(self):
        self.choices = [i.lower() for i in self.choices]

        coefficients_new = []
        for j in self.coefficients:
            new_dict = {}
            variables = j.keys()
            for k in variables:
                if type(k) is str:
                    new_dict[k.lower()] = j[k]
                elif type(k) is tuple:
                    varList = []
                    for kvar in k:
                        varList.append(kvar.lower())
                    new_dict[tuple(varList)] = j[k]
            coefficients_new.append(new_dict)
        self.coefficients = coefficients_new

    def check_each_dict(self, list_of_dicts):

        if not isinstance(list_of_dicts, list):
            return 0, 'not a valid list of dicts for coefficients'

        for i in list_of_dicts:
            if not isinstance(i, dict):
                return 0, """coefficients dictionary for one of the choices """\
                    """specified incorrectly"""

            checkVal, checkText = self.check_text_only(i.keys())
            if not checkVal:
                return 0, checkText

            checkVal, checkText = self.check_num_only(i.values())
            if not checkVal:
                return 0, checkText

        return 1, ''

    def check_text_only(self, text_list):
        for i in text_list:
            checkVal, checkText = self.check_firstchar(i)
            if checkVal == 0:
                return 0, checkText

            if type(i) is str:
                pass
            elif type(i) is tuple:
                for k in i:
                    if type(k) is not str:
                        return 0, 'not a valid string'
            else:
                return 0, 'not a valid string'

            if len(i) == 0:
                return 0, 'length of the string is zero'

        return 1, ''

    def check_firstchar(self, name):
        name = str(name)
        match = re.match('[0-9]', name)
        if match is not None:
            return 0, 'not a valid string'
        else:
            return 1, ''

    def check_num_only(self, num_list):
        for i in num_list:
            if type(i) is int or type(i) is float or type(i) is long:
                pass
            else:
                return 0, 'not a valid number'
        return 1, ''

    def check_specification_consistency(self, choices, coefficients):
        if len(choices) <> len(coefficients):
            return 0, """the number of choices and equation specification - """\
                """coefficients are inconsistent"""

        return 1, ''

    def num_choices(self):
        return len(self.choices)


class ColumnOperationsSpecification(Specification):

    def __init__(self, choices, coefficients, scalarCalcType):
        Specification.__init__(self, choices, coefficients)
        self.scalarCalcType = scalarCalcType


import unittest
from numpy import array


class TestBadSpecification(unittest.TestCase):

    def setUp(self):
        self.choices = ['SOV', 'HOV']
        self.choices1 = ['SOV', 1]
        self.choices2 = ['werew', '2werwr']

        self.coefficients = [{'Constant': 2, 'Var1': 2.11}, {'Constant': 1.2}]
        self.coefficients1 = [
            {'Constant': '2', 'Var1': 2.11}, {'Constant': 1.2}]
        self.coefficients2 = [
            {'1Constant': 2, 'Var1': 2.11}, {'Constant': 1.2}]
        self.coefficients3 = [{1: 2, 'Var1': 2.11}, {'Constant': 1.2}]
        self.coefficients4 = [{'Constant': 2, 'Var1': 2.11}]

    def testchoices(self):
        self.assertRaises(ChoicesError, Specification, self.choices1,
                          self.coefficients)

    def testchoicesfirstchar(self):
        self.assertRaises(ChoicesError, Specification, self.choices2,
                          self.coefficients)

    def testvariables(self):
        self.assertRaises(CoefficientsError, Specification, self.choices,
                          self.coefficients3)

    def testvariablesfirstchar(self):
        self.assertRaises(CoefficientsError, Specification, self.choices,
                          self.coefficients2)

    def testcoefficients(self):
        self.assertRaises(CoefficientsError, Specification, self.choices,
                          self.coefficients1)

    def testchoicescoefficientslength(self):
        self.assertRaises(SpecificationError, Specification, self.choices,
                          self.coefficients4)

    def testchoiceslength(self):
        spec = Specification(self.choices, self.coefficients)
        num_choices = spec.number_choices
        self.assertEqual(len(self.choices), num_choices)

    def testlowercase(self):
        spec = Specification(self.choices, self.coefficients)
        choices_lower = ['sov', 'hov']
        self.assertEqual(choices_lower, spec.choices)
        coefficients_lower = [{'constant': 2, 'var1': 2.11}, {'constant': 1.2}]
        self.assertEqual(coefficients_lower, spec.coefficients)


if __name__ == '__main__':
    unittest.main()
