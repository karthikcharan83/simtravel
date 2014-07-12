import numpy as np
import time as t
import bisect
import skimsquery as sk

from collections import defaultdict
from openamos.core.errors import NetworkError

class NetworkConditions(object):
    def __init__(self):
        self.modes = defaultdict(dict)

    def add_mode(self, nodes, count_skims, mode, mode_value,  
                   information_type,  information_type_value, enIntTrigger):
        modeObj = Mode(nodes, count_skims, mode, enIntTrigger)
        self.modes[mode][information_type] = modeObj
        self.modes[mode_value][information_type_value] = modeObj
    
    def read_skims(self, loc_dict, mode=None, information_type=None, mode_value=None, information_type_value=None):
        errorMsg = ("""Invalid inputs for reading skims
                   mode - %s, information_type - %s, mode_value - %s, 
                   information_type - %s. Enter valid values for 
                   either mode and information_type or mode_value and 
                    information_type_value""" %(mode, information_type, 
                                                       mode_value, 
                                                       information_type_value))
        if mode == None and information_type == None:
            if mode_value == None | information_type == None:
                raise NetworkError, errorMsg
            self.modes[mode_value][information_type_value].read_skims(loc_dict)
        elif mode == None or information_type == None:
            raise NetworkError, errorMsg
        else:
            self.modes[mode][information_type].read_skims(loc_dict)
    
    def __del__(self):
        for mode, modedict in self.modes.iteritems():
            for information_type, modeObj in modedict.iteritems():
                del(modeObj)

class Mode(object):
    def __init__(self, nodes, count_skims, desc, enIntTrigger):
        self.nodes = nodes
        self.count_skims = count_skims
        self.desc = desc
        self._create_mode_object()
        self.enIntTrigger = enIntTrigger

    def _create_mode_object(self):
        mode = sk.Mode()
        mode.nodes = self.nodes
        mode.count_skims = self.count_skims
        mode.desc = self.desc
        self._c_mode = sk.alloc_mode(mode)

    def lookup_skim_index(self, interval):
        if interval == None:
            interval = 240
        skim_index = bisect.bisect_left(self.enIntTrigger, interval)
        return skim_index

    def read_skims(self, loc_dict):
        for key, value in loc_dict.iteritems():
            if not isinstance(key, int):
                raise SkimsError, ("""Key for location dictionary input
                                   is not a valid integer - %s""" %(key))
            if not isinstance(value, str):
                raise SkimsError, ("""Key for location dictionary input
                                   is not a valid integer - %s""" %(str))
            sk.populate_skim(self._c_mode, key, value)

    def get_tt(self, interval,  origin,  dest,  votd=None):
        skim_index = self.lookup_skim_index(interval)
        size = origin.shape[0]
        tt = np.zeros(size, dtype=np.double)
        if votd == None:
            votd = np.zeros(size, dtype=np.double)
        sk.get_tt_w(self._c_mode,  skim_index,  origin,  dest,  tt, votd,  size)        
        return tt

    def get_dist(self, interval,  origin,  dest):
        skim_index = self.lookup_skim_index(interval)
        size = origin.shape[0]
        dist = np.zeros(size, dtype=np.double)
        sk.get_dist_w(self._c_mode,  skim_index,  origin,  dest,  dist, size)
        return dist

    def get_locations(self, interval, origin, dest, available_tt,
                        nodes_available, count, seed, votd=None):
        #TODO: Seed is a int value, need to fix it to array at some point
        skim_index = self.lookup_skim_index(interval)
        size = origin.shape[0]
        seed = np.zeros(size, dtype=int) + seed
        locations = np.zeros((size, count), dtype=int)
        if votd == None:
            votd = np.zeros(size, dtype=np.double)
        sk.get_locations_w(self._c_mode, skim_index, origin, dest,
                              available_tt, votd, size, nodes_available,
                              locations, count, seed)
        return locations

    def check_locations(self, interval, origin, dest, locations,
                           count, available_tt, votd=None):
        skim_index = self.lookup_skim_index(interval)
        size = origin.shape[0]
        if votd == None:
            votd = np.zeros(size, dtype=np.double)
        for i in range(count):
            tt_from = self.get_tt(skim_index,  origin,  locations[:, i],  votd)
            tt_to =  self.get_tt(skim_index,  locations[:, i], dest, votd)

            #Checking to see if the locations sampled are correct
            index_incorrect = tt_from + tt_to > available_tt
            if index_incorrect.any():
                print "This is wrong"
                print "\tOrigin with issue - ", origin[index_incorrect]
                print "\tDestination with issue - ", dest[index_incorrect]
                print "\ttt_from with issue - ", tt_from[index_incorrect]
                print "\ttt_to with issue - ", tt_to[index_incorrect]
                raise Exception,  "This is wrong"

        #Checking for count of locations sampled
        count_locations = (locations == 0).sum(axis=1)
        index = count_locations > 0
        if index.any():
            print "Was not able to get %d locations for all od" %(count)

            print "\tCount of locations ", count_locations[index]
            print "\tThese are the corresponding origins - ", origin[index]
            print "\tThese are the corresponding destinations - ", dest[index]

if __name__ == "__main__":
    t_s = t.time()
    mode = Mode(175, 2, "auto", [720, 1440])
    size = 12
    count = 5

    #origin = np.random.randint(1,175,size)
    #dest = np.random.randint(1,175,size)
    #available_tt = np.zeros(size, dtype = np.double) + 50
    #nodes_available = np.array(range(175)) + 1
    #seed = np.array(range(size)) + 1

    origin = np.array([129,131,158,39,127,20,59,73,35,70,84,173])

    dest = np.array([129,131,158,39,127,20,59,73,35,70,84,173])
    available_tt =  np.array([586,1,508,664,613,763,746,684,700,791,780,493])
    nodes_available = np.array(range(175)) + 1
    seed = np.array(range(12)) + 162


    print origin.shape, dest.shape

    loc_dict = {0:"C:\\DTALite\\New_PHXsubarea\\skims\\skim10.csv",
                  1:"C:\\workspace\\openamos\\core\\travel_skims\\test_data\\skim2_175.csv"}
    mode.read_skims(loc_dict)

    # Testing basic skims no votd
    tt = mode.get_tt(0, origin, dest)
    dist = mode.get_dist(0, origin, dest)
    locations = mode.get_locations(0, origin, dest, available_tt, nodes_available,
                                count, seed)
    print "\n",locations
    """
    print "Travel time - ",  tt
    print "Travel distance - ",dist
    print "Locations given 50 min availability - ", locations
    mode.check_locations(0, origin, dest, locations, count, available_tt)
    print "Time taken - %.4f" %(t.time()-t_s)

    # Testing votd
    votd = np.zeros(size, dtype = np.double) + 2
    tt = mode.get_tt(0, origin, dest, votd)
    locations = mode.get_locations(0, origin, dest, available_tt, nodes_available,
                                count, seed, votd)
    print "Travel time st VOT - ",  tt
    print "Locations given 50 min availability st VOT- ", locations
    mode.check_locations(0, origin, dest, locations, count, available_tt)
    print "Time taken - %.4f" %(t.time()-t_s)
    """
