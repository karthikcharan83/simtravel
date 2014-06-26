import copy
from openamos.core.errors import SpecificationError
from openamos.core.models.model_components import Specification


class NestedChoiceSpecification(Specification):

    """
    This is the base class for specifying branches in a nested logit model.

    Inputs:
    choices - list of only one choice is expected
    coefficients - list of a single dictionary for the above choice
    logsumparameter - numeric value 
    """

    def __init__(self, choices, coefficients, logsumparameter=None):
        Specification.__init__(self, choices, coefficients)
        if self.number_choices > 1:
            raise SpecificationError, """not a valid inout - more than 1 """\
                """equations specified for the branch in the tree; only one """\
                """ choice expected"""
        if logsumparameter is not None:
            if logsumparameter > 1 or logsumparameter < 0:
                raise SpecificationError, """not a valid input - logsumparameter """\
                    """out of range; valid range [0-1]"""
        self.logsumparameter = logsumparameter


class NestedSpecification(object):

    """
    This is the base class for specifying the attrubutes of a nested logit choice
    model.

    Inputs:
    specification_dict - dictionary of NestedChoiceSpecification objects (defines 
    the structure of the choice tree)
    """

    def __init__(self, specification_dict):
        self.specification = specification_dict
        self.check()
        self.depth_dict = self.depth()
        self.choices, self.coefficients = self.get_choices_coefficients()
        self.current_depth = max(self.depth_dict.values())
        self.number_choices = self.num_choices()
        self.actual_choices = self.get_actual_choices()

    def get_choices_coefficients(self):
        """
        The method returns a list of choices (including branches, trunks etc.) 
        and the corresponding list of coefficients for calculating 
        the respective utilities.
        """
        choices = []
        coefficients = []
        for i in self.depth_dict:
            for j in self.specification[i]:
                choices = choices + j.choices
                coefficients = coefficients + j.coefficients
        return choices, coefficients

    def get_actual_choices(self):
        """
        The method returns a list of choices within the tree. 
        """
        actual_choices = []
        for i in self.choices:
            child_names = self.all_child_names([i])
            if len(child_names) == 0:
                actual_choices.append(i)
        return actual_choices

    def check(self):
        """
        The method checks the inputs and raises appropriate prompts as 
        necessary.
        """
        self.values = []

        if not isinstance(self.specification, dict):
            raise SpecificationError, """not a valid input - dictionary """\
                """of choice tree expected"""

        keys = self.specification.keys()
        for i in keys:
            for j in self.specification[i]:
                if not isinstance(j, NestedChoiceSpecification):
                    raise SpecificationError, """not a valid input - values for keys """\
                        """in the choice tree specification are not a valid """\
                        """NestedChoiceSpecification object"""
                self.values.append(j)

        if not ('root' in keys or 'ROOT' in keys):
            return SpecificationError, """not a valid input - the "root" key is """\
                """missing from the keys"""
        try:
            keys.pop(keys.index('root'))
        except:
            pass
        try:
            keys.pop(keys.index('ROOT'))
            self.specification['root'] = self.specification['ROOT']
            self.specifiation.pop('ROOT')
        except:
            pass

        for i in keys:
            if not isinstance(i, NestedChoiceSpecification):
                raise SpecificationError, """not a valid input - keys in the """\
                    """dictionary of choice are not a valid """\
                    """NestedChoiceSpecification object"""

            if i.logsumparameter is None:
                raise SpecificationError, """not a valid input - the parents in the """\
                    """choice tree do not have a valid logsum parameter"""

            logsum_type = type(i.logsumparameter)
            if logsum_type not in [int, float]:
                raise SpecificationError, """not a valid input - the parents in the """\
                    """choice tree do not have a valid logsum parameter - """\
                    """int or float expected"""

        self.keys = self.specification.keys()

        depth_dict = self.depth()
        for i in depth_dict.keys():
            if i <> 'root':
                self.check_logsum_ofparent(i)
        return 1, ''

    def check_logsum_ofparent(self, child):
        """
        The method checks to make sure that the logsum parameters in the 
        choice tree follow the required hierarchy.
        """
        parent = self.parent(child)
        if not parent == 'root':
            if child.logsumparameter > parent.logsumparameter:
                raise SpecificationError, """not a valid input - the logsum """\
                    """parameters are not feasible; the logsum parameter for one """\
                    """of the children is greater than the parent"""
            else:
                self.check_logsum_ofparent(parent)

    def parent(self, value):
        """
        The method returns the NestedChoiceSpecification parent 
        corresponding to the NestedChoiceSpecification child.

        Inputs:
        value - NestedChoiceSpecification object
        """
        for key in self.specification.keys():
            if value in self.specification[key]:
                return key
        raise SpecificationError, '%s s parent was not found' % value

    def parent_key(self, value):
        """
        The method returns the NestedChoiceSpecification parent
        corresponding to the child's name.

        Inputs:
        value - string corresponding to the child
        """
        for key in self.specification.keys():
            for child in self.specification[key]:
                if child.choices[0] == value:
                    return key

    def child_names(self, key):
        """
        The method returns a list of all the children's names that are present in 
        the corresponding NestedChoiceSpecification parent.

        Inputs:
        key - NestedChoiceSpecification object for the parent 
        """
        names = []
        try:
            for i in self.specification[key]:
                names.append(i.choices[0])
        except KeyError, e:
            # not raised just warning printed
            raise  SpecificationError, """%s key was not found in the """\
                """specification dictionary""" % key

        return names

    def all_child_names(self, values):
        """
        The method returns a list of all children's names that are present in the 
        corresponding parent's (given by the name of parent). 

        Also, it returns a list of all subchildren.

        Input:
        values - list of strings corresponding to the parents for which child
        names are sought 
        """

        # differs from child_names in that this one returns in response to
        # columna name as opposed to a spec object key
        # also this returns all the sub children

        values_iter = copy.deepcopy(values)

        all_names = []

        while len(values_iter) > 0:
            node = values_iter[0]
            for i in self.specification.keys():
                if i <> 'root':
                    check = i.choices[0] == node
                    if check:
                        child_names = self.child_names(i)
                        all_names = all_names + child_names
                        values_iter = values_iter + child_names
                        break
            values_iter.pop(0)
        return all_names

    def all_actual_choice_names(self, values):
        """
        """
        all_choices = set(self.all_child_names(values))
        all_actual_choices = all_choices.intersection(self.actual_choices)
        return all_actual_choices

    def all_parent_names(self, value):
        """
        The method returns the list of all parent names corresponding to the
        child's name given by value.

        Inputs:
        value - string (name of the child)
        """
        all_names = []

        while value:
            key = self.parent_key(value)
            if key is not None:
                if key <> 'root':
                    value = key.choices[0]
                    all_names.append(key.choices[0])
                else:
                    value = None
        return all_names

    def depth(self):
        """
        The method returns the list of the choice tree.

        Inputs:
        None
        """
        depth_dict = {}
        for value in self.values:
            value1 = value
            root = True
            depth = 1
            while root:
                parent = self.parent(value)
                if parent == 'root':
                    root = False
                else:
                    depth = depth + 1
                    root = True
                    value = parent
            parent = self.parent(value1)
            depth_dict[parent] = depth
            # if parent <> 'root':
            #    depth_list[parent] = depth

        return depth_dict

    def __iter__(self):
        return self

    def next(self):
        if self.current_depth == 0:
            self.depth_dict = self.depth()
            raise StopIteration
        keys_atdepth = self.return_keys(self.depth_dict, self.current_depth)
        self.current_key = keys_atdepth[0]
        self.depth_dict.pop(keys_atdepth[0])
        if len(keys_atdepth) == 1:
            self.current_depth = self.current_depth - 1
        return self.current_key

    def return_keys(self, depth_dict, value):
        keys = []
        for i in depth_dict.keys():
            if depth_dict[i] == value:
                keys.append(i)
        return keys

    def num_choices(self):
        return len(self.choices)

import unittest
from numpy import array


class TestBadNestedBranchSpecification(unittest.TestCase):

    def setUp(self):
        self.choices = ['sov']
        self.choices1_bad = ['sov1', 'sov2']

        self.coefficients = [{'Constant': 2, 'Var1': 2.11}]
        self.coefficients1_bad = [
            {'Constant': 2, 'Var1': 2.11}, {'Constant': 12}]

    def testtwochoices(self):
        self.assertRaises(SpecificationError, NestedChoiceSpecification,
                          self.choices1_bad, self.coefficients1_bad)

    def testgrtonelogsum(self):
        self.assertRaises(SpecificationError, NestedChoiceSpecification,
                          self.choices, self.coefficients, 1.5)

    def testlesszerologsum(self):
        self.assertRaises(SpecificationError, NestedChoiceSpecification,
                          self.choices, self.coefficients, -.1)


class TestBadNestedSpecification(unittest.TestCase):

    def setUp(self):
        choices1 = ['sov']
        coefficients1 = [{'Constant': 2, 'Var1': 2.11}]
        spec1 = NestedChoiceSpecification(choices1, coefficients1)

        choices2 = ['hov']
        coefficients2 = [{'Constant': 1.2}]
        spec2 = NestedChoiceSpecification(choices2, coefficients2)

        choices3 = ['transit']
        coefficients3 = [{'Constant': .4352, 'Var1': -1.11}]
        spec3 = NestedChoiceSpecification(choices3, coefficients3)

        choices31 = ['light rail']
        coefficients31 = [{'Constant': .32, 'Var1': .581}]
        spec31 = NestedChoiceSpecification(choices31, coefficients31)

        choices32 = ['bus']
        coefficients32 = [{'Constant': 1.2, 'Var1': 4.11}]
        spec32 = NestedChoiceSpecification(choices32, coefficients32)

        self.specification_dict = {'root': [spec1, spec2, spec3],
                                   spec3: [spec31, spec32]}

        self.specification_dict_bad2 = {'root': [choices1, spec2, spec3],
                                        spec3: [spec31, spec32]}

        self.specification_dict_bad3 = {'root1': [spec1, spec2, spec3],
                                        spec3: [spec31, spec32]}

        self.specification_dict_bad4 = {'root': [spec1, spec2, spec3],
                                        'dummy': [spec31, spec32]}

        self.specification_dict_bad5 = {'root': [spec1, spec2, spec3],
                                        spec3: [spec31, spec32]}

    def testnospecobjectvaluetinspecdict(self):
        self.assertRaises(SpecificationError, NestedSpecification,
                          self.specification_dict_bad2)

    def testnorootkeyinspecdict(self):
        self.assertRaises(SpecificationError, NestedSpecification,
                          self.specification_dict_bad3)

    def testnospecobjectkeyinspecdict(self):
        self.assertRaises(SpecificationError, NestedSpecification,
                          self.specification_dict_bad4)

    def testnologsum(self):
        self.assertRaises(SpecificationError, NestedSpecification,
                          self.specification_dict_bad5)


class TestNestedSpecification(unittest.TestCase):

    def setUp(self):
        choices1 = ['sov']
        coefficients1 = [{'Constant': 2, 'Var1': 2.11}]
        spec1 = NestedChoiceSpecification(choices1, coefficients1, 0.7)

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
        spec11 = NestedChoiceSpecification(choices11, coefficients11, 0.7)

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
                              spec3: [spec31, spec32]}

        specification_dict1 = {'root': [spec1, spec2, spec3],
                               spec1: [spec11],
                               spec3: [spec31, spec32],
                               spec11: [spec111],
                               spec31: [spec311, spec312],
                               spec32: [spec321, spec322]}

        self.nested_spec = NestedSpecification(specification_dict)
        self.nested_spec1 = NestedSpecification(specification_dict1)
        self.keys = ['root', spec3]
        self.parentkeys1 = ['root', spec3]
        self.childkeys1 = [spec1, spec31]
        self.keys.sort()
        self.values = [spec1, spec2, spec3, spec31, spec32]
        self.values.sort()
        self.keys_de_3_act = [spec11, spec31, spec32]

    def testkeys(self):
        keys_specclass = self.nested_spec.keys
        keys_specclass.sort()
        self.assertEquals(self.keys, keys_specclass)

    def testvalues(self):
        values_specclass = self.nested_spec.values
        values_specclass.sort()
        self.assertEquals(self.values, values_specclass)

    def testdepth(self):
        depth_act = 3
        depth_specclass = max(self.nested_spec1.depth().values())
        self.assertEquals(depth_act, depth_specclass)

        # Iterating over parents
        print '\nPARENT', 'Number of Children'
        for i in self.nested_spec1:
            if i == 'root':
                print i, len(self.nested_spec1.specification[i])
            else:
                print i.choices, len(self.nested_spec1.specification[i])

    def testchoicescoeffs(self):
        choices_act = ['sov', 'sov1', 'sov11', 'hov', 'transit',
                       'light rail', 'light rail1', 'light rail2',
                       'bus', 'bus1', 'bus2']
        choices_act.sort()
        choices_model = self.nested_spec1.choices
        choices_model.sort()
        self.assertEquals(choices_act, choices_model)

    def testactchoices(self):
        actual_choices_act = ['sov11', 'hov', 'light rail1', 'light rail2',
                              'bus1', 'bus2']
        actual_choices_act.sort()
        actual_choices_model = self.nested_spec1.actual_choices
        actual_choices_model.sort()
        self.assertEquals(actual_choices_act, actual_choices_model)

    def testparent(self):
        parent1_act = self.parentkeys1[0]
        parent2_act = self.parentkeys1[1]

        child1_act = self.childkeys1[0]
        child2_act = self.childkeys1[1]

        parent1_model = self.nested_spec1.parent(child1_act)
        parent2_model = self.nested_spec1.parent(child2_act)

        self.assertEqual(parent1_act, parent1_model)
        self.assertEqual(parent2_act, parent2_model)

    def testparent_key(self):
        parent1_act = self.parentkeys1[0]
        parent2_act = self.parentkeys1[1]

        child1_act = 'sov'
        child2_act = 'bus'

        parent1_model = self.nested_spec1.parent_key(child1_act)
        parent2_model = self.nested_spec1.parent_key(child2_act)

        self.assertEqual(parent1_act, parent1_model)
        self.assertEqual(parent2_act, parent2_model)

    def testchildnames(self):
        parent1_act = self.parentkeys1[0]
        child_names1_act = ['sov', 'hov', 'transit']
        child_names1_act.sort()

        parent2_act = self.parentkeys1[1]
        child_names2_act = ['light rail', 'bus']
        child_names2_act.sort()

        child_names1_model = self.nested_spec1.child_names(parent1_act)
        child_names1_model.sort()
        child_names2_model = self.nested_spec1.child_names(parent2_act)
        child_names2_model.sort()

        self.assertEquals(child_names1_act, child_names1_model)
        self.assertEquals(child_names2_act, child_names2_model)

    def testallchildnames(self):
        parent2_act = 'transit'
        child_names2_act = ['light rail', 'light rail1', 'light rail2',
                            'bus', 'bus1', 'bus2']
        child_names2_act.sort()

        child_names2_model = self.nested_spec1.all_child_names([parent2_act])
        child_names2_model.sort()

        self.assertEquals(child_names2_act, child_names2_model)

    def testallparentnames(self):
        child1_act = 'light rail2'
        all_parents1_act = ['light rail', 'transit']

        child2_act = 'sov11'
        all_parents2_act = ['sov', 'sov1']

        all_parents1_model = self.nested_spec1.all_parent_names(child1_act)
        all_parents1_model.sort()

        all_parents2_model = self.nested_spec1.all_parent_names(child2_act)
        all_parents2_model.sort()

        self.assertEquals(all_parents1_act, all_parents1_model)
        self.assertEquals(all_parents2_act, all_parents2_model)

    def testnumchoices(self):
        choices_act = ['sov', 'sov1', 'sov11', 'hov', 'transit',
                       'light rail', 'light rail1', 'light rail2',
                       'bus', 'bus1', 'bus2']
        numchoices_act = len(choices_act)

        numchoices_model = self.nested_spec1.num_choices()

        self.assertEquals(numchoices_act, numchoices_model)

    def testreturnkeys(self):
        depth_dict = self.nested_spec1.depth()
        self.keys_de_3_act.sort()

        keys_de_3_model = self.nested_spec1.return_keys(depth_dict, 3)
        keys_de_3_model.sort()

        self.assertEquals(self.keys_de_3_act, keys_de_3_model)


# TODO - rename get_choices_coefficients --> get_parentnodes_coefficients
# TODO - all values to lower case where string is being passed
# TODO - also check for absence of keys/values should exception be
# raised or a no value return ??

if __name__ == '__main__':
    unittest.main()
