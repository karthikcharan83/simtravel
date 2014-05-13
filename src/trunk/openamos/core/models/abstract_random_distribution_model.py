from numpy import zeros, array, iinfo, int32
from numpy.random.mtrand import RandomState

class RandomDistribution(RandomState):
    def __init__(self, seed):
        RandomState.__init__(self, seed)
        self.seed = seed

    def return_normal_variables(self, location, scale, size):
        if scale == 0:
            return zeros(size) + location

        rand_norm_vars = self.normal(loc=location, scale=scale, size=size)
        return rand_norm_vars

    def return_random_variables(self, size=None):
        if size == None:
            return self.random_sample()

        rand_vars = self.random_sample(size)
        return rand_vars

    def return_random_integers(self, low, high=None, size=None):
        rand_int_vars = self.random_integers(low, high, size)
        return rand_int_vars

    def return_half_normal_variables(self, location, scale, size=1):
        norm_vars = self.return_normal_variables(location, scale, size)
        half_norm_vars = abs(norm_vars)

        return half_norm_vars

    def shuffle_sequence(self, sequence):
        return self.shuffle(sequence)

import unittest


class TestRandomDistribution(unittest.TestCase):
    def setUp(self):
        pass
    def testValues(self):
        for i in range(100):
            self.dist1 = RandomDistribution(seed=1)
            self.dist2 = RandomDistribution(seed=1)


            dist1Vals = self.dist1.return_normal_variables(location=0, scale=1, size=(10000,1))
            dist2Vals = self.dist2.return_normal_variables(location=0, scale=1, size=(10000,1))

            pred_diff = all(dist1Vals == dist2Vals)
            if not pred_diff:
                print 'Run:%s' %(i+1)

                print dist1Vals, dist2Vals
            self.assertEquals(True, pred_diff)



if __name__ == '__main__':
    unittest.main()
