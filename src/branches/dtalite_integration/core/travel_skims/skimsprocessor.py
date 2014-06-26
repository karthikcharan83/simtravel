# include all the import
import traceback
import os
import sys
import time
import exceptions
import skimsquery
from numpy import *

# class to define the database connection along with other functions


class SkimsProcessor(object):

    """
    This is the class for extending the C code to access the graph
    and get the travel times.

    Input: 
    """

    def __init__(self, offset, nodes):
        self.offset = offset
        self.nodes = nodes

        # initialize the graph
        skimsquery.initialize_array(self.nodes)

    def set_tt_fileString(self, file_path):
        self.ttFilePath = file_path
        skimsquery.set_tt_file(file_path, len(self.ttFilePath))

    def set_dist_fileString(self, file_path):
        self.distFilePath = file_path
        skimsquery.set_dist_file(file_path, len(self.distFilePath))

    def create_graph(self):
        skimsquery.set_array(self.offset)

    def set_real_tt_fileString(self, file_path):
        self.ttFilePath = file_path
        skimsquery.set_real_tt_file(file_path, len(self.ttFilePath))

    def set_real_dist_fileString(self, file_path):
        self.distFilePath = file_path
        skimsquery.set_real_dist_file(file_path, len(self.distFilePath))

    def create_real_graph(self):
        skimsquery.set_real_array(self.offset)

    def numpy_to_carray(self, numpy_arr, arr_len, data_type):
        """
        This method converts the numpy array to a carray

        Input:
        Numpy array, array length and data type (to differentiate between float and int)

        Output:
        Carray
        """
        # check the datatype
        if data_type == 1:
            # create a new carray
            new_carr = skimsquery.new_floatArray(arr_len)
            i = 0

            # run a loop to assign the values in the numpy array to the carray
            for each in numpy_arr:
                skimsquery.floatArray_setitem(new_carr, i, float(each))
                i = i + 1
        else:
            # create a new carray
            new_carr = skimsquery.new_intArray(arr_len)
            i = 0

            # run a loop to assign the values in the numpy array to the carray
            for each in numpy_arr:
                skimsquery.intArray_setitem(new_carr, i, int(each))
                i = i + 1

        # return the carray
        return new_carr

    def carray_to_numpy(self, carray, arr_len, data_type):
        """
        This method converts carray to numpy

        Input:
        Carray, array length and data type (to differentiate between float and int)

        Output:
        Numpy Array
        """
        # create a dummy array of length arr_len
        numpy_arr = zeros(arr_len)

        # check for datatype
        if data_type == 1:
            # run a loop to assign the values in the carray to the numpy array
            for i in range(arr_len):
                numpy_arr[i] = skimsquery.floatArray_getitem(carray, i)
        else:
            # run a loop to assign the values in the carray to the numpy array
            for i in range(arr_len):
                numpy_arr[i] = skimsquery.intArray_getitem(carray, i)

        # return the numpy array
        return numpy_arr

    def get_travel_times(self, origin, destination):
        # get the array length and initialize the tt array
        arr_len = origin.size
        tt = zeros(arr_len)

        # convert the arrays to carrays
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        tt_arr = self.numpy_to_carray(tt, arr_len, 1)

        # start retrieving travel times
        skimsquery.get_tt(org_arr, dest_arr, tt_arr, arr_len, self.offset)

        # conversion from carray to numpy
        new_tt = self.carray_to_numpy(tt_arr, arr_len, 1)

        # deleting all the carrays
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        self.delete_carray(tt_arr, 1)

        # return the travel times numpy array
        # print 'tt', new_tt
        return new_tt

    def get_real_travel_times(self, origin, destination):
        # get the array length and initialize the tt array
        arr_len = origin.size
        tt = zeros(arr_len)

        # convert the arrays to carrays
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        tt_arr = self.numpy_to_carray(tt, arr_len, 1)

        # start retrieving travel times
        skimsquery.get_real_tt(org_arr, dest_arr, tt_arr, arr_len, self.offset)

        # conversion from carray to numpy
        new_tt = self.carray_to_numpy(tt_arr, arr_len, 1)

        # deleting all the carrays
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        self.delete_carray(tt_arr, 1)

        # return the travel times numpy array
        # print 'tt', new_tt
        return new_tt

    def get_travel_distances(self, origin, destination):
        # get the array length and initialize the tt array
        arr_len = origin.size
        dist = zeros(arr_len)

        # convert the arrays to carrays
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        dist_arr = self.numpy_to_carray(dist, arr_len, 1)

        # start retrieving travel times
        skimsquery.get_dist(org_arr, dest_arr, dist_arr, arr_len, self.offset)

        # conversion from carray to numpy
        new_dist = self.carray_to_numpy(dist_arr, arr_len, 1)

        # deleting all the carrays
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        self.delete_carray(dist_arr, 1)

        # return the travel times numpy array
        return new_dist

    def get_real_travel_distances(self, origin, destination):
        # get the array length and initialize the tt array
        arr_len = origin.size
        dist = zeros(arr_len)

        # convert the arrays to carrays
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        dist_arr = self.numpy_to_carray(dist, arr_len, 1)

        # start retrieving travel times
        skimsquery.get_real_dist(
            org_arr, dest_arr, dist_arr, arr_len, self.offset)

        # conversion from carray to numpy
        new_dist = self.carray_to_numpy(dist_arr, arr_len, 1)

        # deleting all the carrays
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        self.delete_carray(dist_arr, 1)

        # return the travel times numpy array
        return new_dist

    def get_generalized_time(self, origin, destination, votd=None):
        # get the array length and initialize the tt array
        arr_len = origin.size
        gentt = zeros(arr_len)

        if votd == None:
            votd_arr = self.numpy_to_carray(2 + zeros(arr_len), arr_len, 1)
        else:
            votd_arr = self.numpy_to_carray(votd, arr_len, 1)

        # convert the arrays to carrays
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        gentt_arr = self.numpy_to_carray(gentt, arr_len, 1)

        # start retrieving travel times
        skimsquery.get_generalized_time(
            org_arr, dest_arr, votd_arr, gentt_arr, arr_len, self.offset)

        # conversion from carray to numpy
        new_gentt = self.carray_to_numpy(gentt_arr, arr_len, 1)

        # deleting all the carrays
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        self.delete_carray(gentt_arr, 1)

        # return the travel times numpy array
        return new_gentt

    def get_generalized_real_time(self, origin, destination, votd=None):
        # get the array length and initialize the tt array
        arr_len = origin.size
        gentt = zeros(arr_len)

        if votd == None:
            votd_arr = self.numpy_to_carray(2 + zeros(arr_len), arr_len, 1)
        else:
            votd_arr = self.numpy_to_carray(votd, arr_len, 1)

        # convert the arrays to carrays
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        gentt_arr = self.numpy_to_carray(gentt, arr_len, 1)

        # start retrieving travel times
        skimsquery.get_generalized_real_time(
            org_arr, dest_arr, votd_arr, gentt_arr, arr_len, self.offset)

        # conversion from carray to numpy
        new_gentt = self.carray_to_numpy(gentt_arr, arr_len, 1)

        # deleting all the carrays
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        self.delete_carray(gentt_arr, 1)

        # return the travel times numpy array
        return new_gentt

    def create_carray(self, num):
        """
        This method is used to create the origin and destination carrays.

        Input: Origin and destination numpy arrays

        Output: Origin and destination carrays
        """
        # print 'testing carray creation'
        p = skimsquery.new_intArray(num)
        skimsquery.create_array(p, num)
        skimsquery.print_array(p, num)
        return p

    def get_travel_times(self, origin, destination):
        """
        This method is used to get the travel times

        Input:
        Origin and destination arrays

        Output:
        Returns an array with travel times
        """

        # Printing vertices
        # print 'origin - ', origin
        # print 'destination - ', destination

        # get the array length and initialize the tt array
        arr_len = origin.size
        tt = zeros(arr_len)

        # convert the arrays to carrays
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        tt_arr = self.numpy_to_carray(tt, arr_len, 1)

        # start retrieving travel times
        skimsquery.get_tt(org_arr, dest_arr, tt_arr, arr_len, self.offset)

        # conversion from carray to numpy
        new_tt = self.carray_to_numpy(tt_arr, arr_len, 1)

        # deleting all the carrays
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        self.delete_carray(tt_arr, 1)

        # return the travel times numpy array
        # print 'tt', new_tt
        return new_tt

    def create_location_array(self, arr_len):
        """
        This method initializes the location array and the temporary location 
        array. It also sets the arrays to zero

        Input:
        Array length

        Output:
        Loctions array and temp locations array are initialized and set to zero
        """
        # Starting location array initialization
        skimsquery.initialize_location_array(arr_len)

        # set the locations graph to zero
        skimsquery.set_location_array_to_zero(arr_len)

        # set the temp locations array to zero
        skimsquery.set_temp_location_array()

    def get_location_choices(self, origin, destination, tt, votd, num_of_locations, land_use, seed):
        """
        This method gets the locations choices. it internally calls 
        the generate random locations method.

        Input:
        Origin, Destination, Trave times and number of locations

        Output:
        Location array
        """
        # get the array length and length for location array
        arr_len = origin.size
        loc_len = arr_len * num_of_locations
        land_use_len = land_use.size

        # check if the landuse array is of length 1
        if land_use_len == 1:
            # check if the data is zero
            if land_use[0] == 0:
                # no land use information present, set land use length to nodes
                land_use_len = self.nodes

        # print 'land use length is %s'%land_use_len
        # initialize locations array to zero
        locations = zeros(loc_len)

        # convert the arrays to carrays
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        tt_arr = self.numpy_to_carray(tt, arr_len, 1)
        votd_arr = self.numpy_to_carray(votd, arr_len, 1)
        loc_arr = self.numpy_to_carray(locations, loc_len, 0)
        land_use_arr = self.numpy_to_carray(land_use, land_use_len, 0)

        # Starting location choices computation
        skimsquery.get_location_choices(org_arr, dest_arr, tt_arr, votd_arr, loc_arr,
                                        arr_len, self.offset, num_of_locations, land_use_arr, land_use_len, seed)

        # Conversion from carray to numpy
        new_loc = self.carray_to_numpy(loc_arr, loc_len, 0)

        # change the dimensions of the new_loc numpy array
        new_loc.shape = (arr_len, num_of_locations)

        # deleting all the carrays
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        self.delete_carray(tt_arr, 1)
        self.delete_carray(loc_arr, 0)

        # deleting locations graph
        self.delete_location(arr_len)

        # return the locations numpy array
        return new_loc

    def delete_carray(self, carray, data_type):
        """
        This method is used to delete the carrays

        Input:
        Carray and datatype

        Output:
        Carrays deleted
        """
        # check for the datatype and delete the respective carray
        if data_type == 1:
            skimsquery.delete_floatArray(carray)
        else:
            skimsquery.delete_intArray(carray)

    def delete_graph(self):
        """
        This method is used the delete the dynamic arrays created 
        in the C program

        Input:
        None

        Output:
        Dynamic Arrays deleted
        """
        # delete the network graph created in the C program
        skimsquery.delete_array()

    def delete_location(self, arr_len):
        """
        This method deletes the locations array in the C program

        Input:
        Array length

        Output:
        Dynamic array deleted
        """
        # delete the locations array created in the C program
        skimsquery.delete_location_array(arr_len)

    def __del__(self):
        # check if object is deleted
        print 'object is deleted'


# unit test to test the code
import unittest

# define a class for testing


class TestSkimsProcessor(unittest.TestCase):

    def setUp(self):
        self.numarr = 'numarr'
        self.offset = 1
        self.nodes = 175

    def testEx(self):

        ext_obj = SkimsProcessor(self.offset, self.nodes)

        ext_obj.set_tt_fileString(
            "C:\\workspace\\openamos\\core\\travel_skims\\test_data\\skim1.csv")
        ext_obj.set_dist_fileString("C:/DTALite/New_PHXsubarea/distance0.dat")
        print 'paths set'
        ext_obj.create_graph()
        print 'graph created'

        print '1111'
        ext_obj.set_real_tt_fileString(
            "C:/DTALite/New_PHXsubarea/output_td_skim_min30.csv")
        print '2222'
        ext_obj.set_real_dist_fileString(
            "C:/DTALite/New_PHXsubarea/distance0.dat")
        print 'paths set 3333'
        ext_obj.create_real_graph()
        print 'graph created 4444'

#        ext_obj2 = SkimsProcessor(self.offset, self.nodes)
#
#        ext_obj2.set_tt_fileString("C:/DTALite/New_PHXsubarea/output_td_skim_min30.csv")
#        ext_obj2.set_dist_fileString("C:/DTALite/New_PHXsubarea/distance0.dat")
#        print 'paths set'
#        ext_obj2.create_graph()
#        print 'graph created'

        o_arr = array([100, 100, 100, 100])
        d_arr = array([120, 134, 153, 160])
        ava_tt = array([175, 200, 123, 144])

        o_arr = random.randint(1,175,1000)
        d_arr = random.randint(1,175,1000)

        loc_ava = array(arange(1995)) + 1

        #loc_ava = array(arange(1000))+1
        numsampllocs = 5
        votd = array([2., 2., 2., 2.])
        print votd
        votd_def = array([0, 0, 0, 0])

        print 'Check tt -- ', ext_obj.get_travel_times(o_arr, d_arr)[:10]
        print 'Check distances -- ', ext_obj.get_travel_distances(o_arr, d_arr)[:10]
        print 'Check generalized distances -- ', ext_obj.get_generalized_time(o_arr, d_arr, votd)[:10]

        print 'Check real tt -- ', ext_obj.get_real_travel_times(o_arr, d_arr)[:10]
        print 'Check real distances -- ', ext_obj.get_real_travel_distances(o_arr, d_arr)[:10]
        print 'Check generalized real distances -- ', ext_obj.get_generalized_real_time(o_arr, d_arr, votd)[:10]

#	ext_obj.create_location_array(4)
#	choices = ext_obj.get_location_choices(o_arr, d_arr, ava_tt, votd, 1995, loc_ava)
#	print choices
#	nonzerochoices = choices <> 0
#	print nonzerochoices.sum(-1)
#
#	for i in range(5):
#	    print "LOCATION CHOICES - ", i + 1
#	    dests = choices[:,i]
#	    tt_to = ext_obj.get_travel_times(o_arr, dests)
#	    tt_from = ext_obj.get_travel_times(dests, d_arr)
#
#	    gen_tt_to = ext_obj.get_generalized_time(o_arr, dests, votd)
#	    gen_tt_from = ext_obj.get_generalized_time(dests, d_arr, votd)
#
#
#	    print "\tAva TT", ava_tt
#	    print "\t-----"
#	    print "\tTT to", tt_to
#	    print "\tTT from", tt_from
#	    print "\tCheck", tt_to + tt_from > ava_tt
#	    print "\t-----"
#	    print "\tGen TT to", gen_tt_to
#	    print "\tGen TT from", gen_tt_from
#	    print "\tCheck", gen_tt_to + gen_tt_from > ava_tt
#
#	ext_obj.create_location_array(4)
#	choices = ext_obj.get_location_choices(o_arr, d_arr, ava_tt, votd_def, 1995, loc_ava)
#	nonzerochoices = choices <> 0
#	print nonzerochoices.sum(-1)
#
#	for i in range(5):
#	    print "LOCATION CHOICES no VOTD - ", i + 1
#	    dests = choices[:,i]
#	    tt_to = ext_obj.get_travel_times(o_arr, dests)
#	    tt_from = ext_obj.get_travel_times(dests, d_arr)
#
#	    gen_tt_to = ext_obj.get_generalized_time(o_arr, dests, votd_def)
#	    gen_tt_from = ext_obj.get_generalized_time(dests, d_arr, votd_def)
#
#
#	    print "\tAva TT", ava_tt
#	    print "\t-----"
#	    print "\tTT to", tt_to
#	    print "\tTT from", tt_from
#	    print "\tCheck", tt_to + tt_from > ava_tt
#	    print "\t-----"
#	    print "\tGen TT to", gen_tt_to
#	    print "\tGen TT from", gen_tt_from
#	    print "\tCheck", gen_tt_to + gen_tt_from > ava_tt


if __name__ == '__main__':
    unittest.main()
