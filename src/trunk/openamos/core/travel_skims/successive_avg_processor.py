#include all the import
import traceback
import os, sys
import time
import exceptions
import successive_average


#class to define the database connection along with other functions
class SuccessiveAverageProcessor(object):
    """
    This is the class for extending the C code to access the graph
    and get the travel times.

    Input:
    """

    def __init__(self, nodes):
        self.nodes = nodes
        print self.nodes
        print 'Testing extension'


    def initialize_array(self):
        """
        This method is used to create and initialize the avg array

        Input:
        None

        Output:
        Entire network Graph is created
        """
        #initialize the graph
        successive_average.initialize_ts_array(self.nodes)


    def get_avg_tt(self, file_path_1, file_path_2, file_path_3, iteration):
        """
        This method gets the avg of travel times from the previous iteration

        Input:
        File1, File2, File3 and iteration

        Output:
        Avg travel times stored in an array
        """
        #initialize the array
        self.initialize_array()

        #get the avg tt
        successive_average.set_ts_array(file_path_1, file_path_2, file_path_3, iteration)
        self.write_results()

    def write_results(self):
        """
        """
        #write results
        successive_average.write_avg_ts_to_file()



    def delete_graph(self):
        """
        This method is used the delete the dynamic arrays created
        in the C program

        Input:
        None

        Output:
        Dynamic Arrays deleted
        """
        #delete the network graph created in the C program
        successive_average.delete_ts_array()


    def __del__(self):
        #check if object is deleted
        print 'object is deleted'



#unit test to test the code
import unittest

#define a class for testing
class TestSuccessiveAverageProcessor(unittest.TestCase):
    def setUp(self):
        self.nodes = 2006

    def testEx(self):
        avg_obj = SuccessiveAverageProcessor(self.nodes)
        #print avg_obj

        file_path_1 = "/home/namrata/Documents/swig/avg_travel_skims/skim1.dat"
        file_path_2 = "/home/namrata/Documents/swig/avg_travel_skims/skim2.dat"
        file_path_3 = "/home/namrata/Documents/swig/avg_travel_skims/skim3.dat"
        iteration = 3

        t1 = time.time()
        print 'get avg tt'
        avg_obj.get_avg_tt(file_path_1, file_path_2, file_path_3, iteration)
        t2 = time.time()
        print '\tTime taken to get avg tt %s'%(t2-t1)

        t1 = time.time()
        avg_obj.write_results()
        t2 = time.time()
        print '\tTime taken to write results %s'%(t2-t1)

        avg_obj.delete_graph()


if __name__ == '__main__':
    unittest.main()
