import networkx
import heapq as hp
import matplotlib.pyplot as plt
from numpy import array, ceil, ma, zeros
#from math import ceil


class Graph(object):

    def __init__(self, skims_t_res=15, analy_t_res=6,
                 analysis_period=24, dist=None, data=None):
        """
        skims_t_res = in mins
        analy_t_res = in seconds
        analysis_period = in hrs
        all the temporal skims should be reported in seconds

        Layout - linkid, direction, anode, bnode, tt in period, length
        Be sure to provide the required number of columns

        TODO: Pass data as an input as opposed to reading from a file
              So data can be read from the tables in the database and provided
              to an instance of this class

        Test Data Layout:
        1 --> 2 --> 3

        """
        # for test data with 12 links
        #skims_t_res = 1
        #analy_t_res = 60
        #analysis_period = 0.5

        self.dist_g_ind = dist
        if self.dist_g_ind is not None:
            self.graph_dist = networkx.DiGraph()
        self.graph_time = networkx.DiGraph()

        self.skims_t_res = skims_t_res
        self.num_skim_intervals = analysis_period * 60 / skims_t_res
        self.analy_t_res = analy_t_res
        self.num_analy_intervals = analysis_period * 60 * 60 / self.analy_t_res

        print 'Number of skim intervals', self.num_skim_intervals
        print 'Number of analysis intervals', self.num_analy_intervals

        # print self.data.shape

        #self.tts = self.process_data()
        #self.arc_index = self.create_arc_index()

        # print self.arc_index.keys(), 'KEYSSSSSSSSSSSSSSSSSS'

        #self.arrival_time(1, 2, 5)

        #g = self.build_graph()
        #self.build_tree_from_source_at_time(g, 1, 5, 7)
        #self.build_tree_to_dest_at_time(g, 9, 25, 22)

        #self.build_prism_between_nodes(g, 1, 9, 2, 8)

    def read_data(self, location):
        # Layout -- Link, Dir, ANode, BNode, Avg_Time_for all intervals, Length
        # currently reads data from a flat file
        # add functionality to read from a database table if necessary

        self.data = []
        if not len(self.data) > 0:
            for line in open(location, 'r'):
                fields = line.strip().split(',')
                fields = [float(i) for i in fields]
                self.data.append(fields)

        #self.data = array(self.data)
        self.data = ma.masked_equal(self.data, -99)

    def process_data(self):
        # Travel Time Matrix
        tts = self.data[:, 4:-1]
        # Average Values
        tts_avg = tts.mean(axis=-1)
        mask = ma.getmaskarray(tts)
        # Assigning missing with average value across other intervals
        for i in range(self.num_skim_intervals):
            tts[mask[:, i], i] = tts_avg[mask[:, i]]
        # Converting into discrete time intervals
        tts = ceil(tts / self.analy_t_res)
        # return tts
        self.tts = tts

        """
        f = open('links_processed.csv', 'w')
        for i in self.tts:
            for j in i:
                f.write('%s,'%j)
            f.write('\n')
        """

    def create_arc_index(self):
        arc_index = {}
        count = 0
        for i in self.data[:, 2:4]:
            arc_index[(int(i[0]), int(i[1]))] = count
            count = count + 1

        self.arc_index = arc_index

    def arrival_time(self, i, j, t):
        """
        t is reported in analysis units default - 6 seconds
        """

        if t > self.num_analy_intervals:
            return 99999999
        # print '\n\t\tcalculating arrival time for nodes %s, %s, in discrete
        # interval %s ' %(i, j, t)
        if i == j:
            return t
        row = self.arc_index[(i, j)]
        #skim_int = ceil((t+1)*self.analy_t_res/(self.skims_t_res*60))
        skim_int = ceil(t * self.analy_t_res / (self.skims_t_res * 60.))

        # print '\t\tSKIMMING INTERVAL', skim_int
        #ttaken = self.tts[row, skim_int-1]
        #a_ij = t+1 + self.tts[row, skim_int-1]
        a_ij = t + self.tts[row, skim_int - 1]

        # print "\t\ttravel time is - %s discrete units"  %self.tts[row, skim_int-1]
        # print "\t\tarrival time is - %s discrete units" %a_ij
        return a_ij
        # print ('leaves in interval %d, leaves %d and time taken is %d and arrives %d at %d'
        #       %(t+1, i, ttaken, j, a_ij))

    def departure_time(self, i, j, t):
        """
        t is repored in analysis units default - 6 seconds
        """
        if i == j:
            return t

        # print '\n\t\tcalculating earliest departure time for nodes - ', i, j

        earliest_dep_time = False
        st_time = t

        while not earliest_dep_time:
            st_time = st_time - 1
            if st_time < 1:
                return -1
            row = self.arc_index[(i, j)]
            skim_int = ceil(
                (st_time) * self.analy_t_res / (self.skims_t_res * 60.))
            tts = self.tts[row, skim_int - 1]

            if tts + st_time <= t:
                earliest_dep_time = True
                # print '\t\tSKIMMING INTERVAL', skim_int
                # print '\t\tstart time', st_time
                # print '\t\ttravel time', tts
                # print '\t\treturning earliest departure time', st_time
                return st_time
            else:
                earliest_dep_time = False

    def build_graph(self):
        g = networkx.DiGraph()

        for n in range(self.data.shape[0]):
            i = self.data[n, 2]
            j = self.data[n, 3]

            g.add_edge(int(i), int(j))

        print 'Graph was successfully created'
        print '\tThe number of nodes - %s' % (g.number_of_nodes())
        print '\tThe number of edges - %s' % (g.number_of_edges())
        # print g.edges()
        return g

    def build_static_graph(self):
        g = networkx.DiGraph()
        for n in range(self.data.shape[0]):
            i = self.data[n, 2]
            j = self.data[n, 3]

            if self.data[n, 4] == -99:
                wt = max(self.data[n, 4:-1])
            else:
                wt = self.data[n, 4]

            g.add_edge(int(i), int(j), weight=wt)
        return g

    def build_time_expanded_graph(self):
        g = networkx.DiGraph()

        for n in range(self.data.shape[0]):
            i = self.data[n, 2]
            j = self.data[n, 3]
            for t in range(self.num_analy_intervals):
                a_ij = self.arrival_time(i, j, t + 1)
                tt = a_ij - (t + 1)

                g.add_edge((int(i), t + 1), (int(j), a_ij), weight=tt)

        print 'Graph was successfully created'
        print '\tThe number of nodes - %s' % (g.number_of_nodes())
        print '\tThe number of edges - %s' % (g.number_of_edges())

    def build_tree_from_source_at_time(self, g, source, t, cutoff=None):
        """
        cutoff - Latest Arrival at destination in seconds

        """

        # if cutoff is not None:
        #    cutoff = ceil((cutoff)*self.analy_t_res/(self.skims_t_res*60))

        ea_sj = []
        nodes_ind = {}
        dist = {}  # to store final distances
        # paths = {source:[source]} # to store paths

        # print g.nodes()

        for j in g.nodes():
            if j <> source:
                hp.heappush(ea_sj, (99999999, j))
                #nodes_ind[j] = False

        hp.heappush(ea_sj, (t, source))
        nodes_ind[source] = False

        while nodes_ind:
            (t_i, i) = hp.heappop(ea_sj)
            if not i in dist:
                if t_i < 99999999:
                    dist[i] = t_i

            # print '\nAT NODE - ', i, 'MIN VALUE OF EA_SI - ', t_i
            # print '\t number of nodes to be skimmed', len(nodes_ind)
            # print '\t', nodes_ind

            # Finalizing and removing fthe node from the dist indicator
            if i in nodes_ind:
                nodes_ind.pop(i)
            else:
                'the node does not exist in the node indicator dictionary'
                continue
            # print '\t number of nodes still to be skimmed after removing the current one', len(nodes_ind)
            # print '\t', nodes_ind

            # Printing final distances for debugging
            # print '\tEA_SJ HEAP BEFORE UPDATING', ea_sj

            edata = g[i].iteritems()

            # print '\tNumber of edges retrieved - ', len(g[i])

            for j, edgedata in edata:
                # print '\tconnection to source - ', j

                if j in dist:
                    t_j = dist[j]
                else:
                    t_j = 99999999

                # print '\tfor node - %s, ea_s%s(%s) from dist dict was - %s'
                # %(j, j, t, t_j)

                t_j_new = min(t_j, self.arrival_time(i, j, t_i))

                # print '\tfor node - %s, ea_s%s(%s) updated valus is - %s'
                # %(j, j, t, t_j_new)

                # if value already updated do not update again
                if j in dist:
                    if t_j_new >= dist[j]:
                        #nodes_ind[j] = False
                        # print "\tGREATER FOUND NOT UPDATED"
                        # raw_input()
                        continue

                # limiting locations to earliest cutoff criterion
                if cutoff is not None:
                    if t_j_new <= cutoff:
                        # print '\tNEW VALUE UPDATED LESS THAN
                        # CUTOFF---------------------------------------'
                        dist[j] = t_j_new
                        hp.heappush(ea_sj, (t_j_new, j))
                        nodes_ind[j] = False
                    else:
                        # print '\tCUTOFF EXCEEDED-----------------------------'
                        # print '\tnode at which exceeded', j
                        # print '\texceed value is ', t_j_new
                        # print '\tcutoff is', cutoff
                        if j in nodes_ind:
                            nodes_ind.pop(j)

                elif t_j_new < 99999999:
                    # print '\tNEW VALUE UPDATED HERE FOR LESS THAN
                    # 99999999-----------------------------'
                    dist[j] = t_j_new
                    hp.heappush(ea_sj, (t_j_new, j))
                    nodes_ind[j] = False

            # print nodes_ind
            # print '\tEA_SJ HEAP AFTER UPDATING', ea_sj
            # print '\tafter updating distance dictionary', dist
            # raw_input()
        # print dist
        return dist

    def build_tree_to_dest_at_time(self, g, dest, t, cutoff=None):
        """
        cutoff - Latest Arrival at destination in seconds

        """
        # if cutoff is not None:
        #    cutoff = ceil((cutoff)*self.analy_t_res/(self.skims_t_res*60))

        ld_jd = []
        nodes_ind = {}
        dist = {}  # to store final distances
        # paths = {source:[source]} # to store paths

        # print g.nodes()

        for j in g.nodes():
            if j <> dest:
                hp.heappush(ld_jd, (99999999, j))
                #nodes_ind[j] = False

        hp.heappush(ld_jd, (-t, dest))
        nodes_ind[dest] = False

        # print 'EA_SJ HEAP BEFORE UPDATING', ld_jd

        while nodes_ind:
            (t_i, i) = hp.heappop(ld_jd)
            if not i in dist:
                dist[i] = -t_i

            # print '\nAT NODE - ', i, 'Latest Departure LD_ID - ', -t_i
            # print '\t number of nodes to be skimmed', len(nodes_ind)
            # print '\t', nodes_ind

            # Finalizing and removing fthe node from the dist indicator
            nodes_ind.pop(i)
            # print '\t number of nodes still to be skimmed after removing the current one', len(nodes_ind)
            # print '\t', nodes_ind

            # Printing final distances for debugging
            # print '\tEA_SJ HEAP BEFORE UPDATING', ld_jd

            edata = g[i].iteritems()

            pred_data = g.predecessors_iter(i)

            for j in pred_data:
                # print '\n\tconnection to destination - ', j

                if j in dist:
                    t_j = -dist[j]
                else:
                    t_j = 99999999

                # print '\tfor node - %s, ld_%sd(%s) from dist dict was - %s'
                # %(j, j, t, -t_j)

                dep_time = self.departure_time(j, i, -t_i)
                if dep_time == -1:
                    # print 'valid departure not possible for j - %s, i - %s,
                    # time - %s' %(j, i, -t_i)
                    continue

                t_j_new = min(t_j, dep_time)

                # print '\tfor node - %s, ea_s%s(%s) updated valus is - %s'
                # %(j, j, t, t_j_new)

                if j in dist:
                    if t_j_new <= dist[j]:
                        #nodes_ind[j] = False
                        # print "GREATER FOUND NOT UPDATED"
                        # raw_input()
                        continue

                # limiting locations to earliest cutoff criterion
                if cutoff is not None:
                    if t_j_new >= cutoff:
                        # print '\tNEW VALUE UPDATED MORE THAN
                        # CUTOFF---------------------------------------'
                        dist[j] = t_j_new
                        hp.heappush(ld_jd, (-t_j_new, j))
                        nodes_ind[j] = False
                    else:
                        # print '\tLESS THAN CUTOFF -----------------------------'
                        # print '\tnode at which less', j
                        if j in nodes_ind:
                            nodes_ind.pop(j)

                elif t_j_new < 99999999:
                    # print '\tNEW VALUE UPDATED HERE FOR LESS THAN
                    # 99999999-----------------------------'
                    dist[j] = t_j_new
                    hp.heappush(ld_jd, (-t_j_new, j))
                    nodes_ind[j] = False

            # print '\tNodes to be skimmed in the next round', nodes_ind
            # print '\tEA_SJ HEAP AFTER UPDATING', ld_jd
            # print '\tafter updating distance dictionary', dist
            # raw_input()

        return dist

    def build_prism_between_nodes_static(self, g, source, dest, t_s, t_d):
        ti = time.time()
        reached_d, reached_path = networkx.single_source_dijkstra(
            g, source, cutoff=t_d - t_s)
        # print '\tReached retrieved in', time.time()-ti

        ti = time.time()
        left_d, left_path = networkx.single_source_dijkstra(
            g, dest, cutoff=t_d - t_s)
        # print '\tLeft retrieved in', time.time()-ti

        # print ('\tDestination(s) reached from source starting at %s within %s analysis intervals is %s' %
        #       (t_s, t_d, len(reached_d)))
        # print ('\tDestination(s) accessed to destination by %s start after %s analysis intervals is %s' %
        #       (t_d, t_s, len(left_d)))

        # print 'cutoff = ', t_d-t_s
        # print 'max_dist = ', max(reached_d.values()), max(left_d.values())
        dests_accessible = {}
        for i in reached_d:
            if i in left_d and ((reached_d[i] + left_d[i]) < t_d - t_s):
                dests_accessible[i] = reached_d[i]

        return dests_accessible

    def build_prism_between_nodes(self, g, source, dest, t_s, t_d):
        #cutoff = ceil(t_s + (t_d-t_s)/self.analy_t_res)
        t_s = ceil(t_s / self.analy_t_res)
        t_d = ceil(t_d / self.analy_t_res)

        ti = time.time()
        reached = self.build_tree_from_source_at_time(g, source, t_s, t_d)
        # print '\tReached retrieved in ', time.time()-ti
        ti = time.time()
        left = self.build_tree_to_dest_at_time(g, dest, t_d, t_s)
        # print '\tleft retrieved in ', time.time()-ti

        # print '\tEA Cutoff Analysis Intervals', cutoff
        # print '\tLD Cutoff Analysis Intervals', cutoff

        # print ('\tDestination(s) reached from source starting at %s within %s analysis intervals is %s' %
        #       (t_s, t_d, len(reached)))
        # print reached
        # print ('\tDestination(s) accessed to destination by %s start after %s analysis intervals is %s' %
        #       (t_d, t_s, len(left)))
        # print left

        dests_accessible = {}
        for i in reached:
            if i in left and (reached[i] < left[i]):
                dests_accessible[i] = [(reached[i] - t_s) * self.analy_t_res,
                                       (t_d - left[i]) * self.analy_t_res,
                                       (left[i] - reached[i]) * self.analy_t_res]

        """
        print 'FOLLOWING DESTINATIONS ARE ACCESSIBLE GIVEN THE TEMPORAL AND SPATIAL CONSTRAINTS'
        print dests_accessible

        print 'TIME BETWEEN SOURCE AND DESTINATION - %s' %(t_d - t_s)
        
        """
        # for i in dests_accessible:
        #    print ("""Destination - %s, time from source - %s"""\
        #               """, time to destination - %s, potential """\
        #               """duration at destination %s"""
        #           %(i, reached[i]-t_s, t_d-left[i], left[i]-reached[i]))
        return dests_accessible

    def build_graph1(self):
        self.add_links()
        if self.nedges > 0:
            print 'Graph was successfully created'
            print '\tThe number of nodes - %s' % (self.graph_time.number_of_nodes())
            print '\tThe number of edges - %s' % (self.graph_time.number_of_edges())

    def add_links(self):
        self.nodes = self.graph_time.number_of_nodes()

        if self.nodes > 0:
            self.graph_time.clear()
            self.graph_dist.clear()

        for i in self.data:
            self.graph_time.add_edge(i[2], i[3], weight=i[-2])
            if self.dist_g_ind is not None:
                self.graph_dist.add_edge(i[2], i[3], weight=i[-1])

        self.nedges = self.graph_time.number_of_edges()
        self.nnodes = self.graph_time.number_of_nodes()

    def draw_graph(self):
        if self.nedges < 200:
            networkx.draw(self.graph_time)
            plt.show()
        else:
            print 'Too many nodes to display'

    def shortest_path_tree(self, node, search_type='time', cutoff=None):
        if node in self.graph_time.nodes():
            if search_type == 'distance':
                dist, path = networkx.single_source_dijkstra(
                    self.graph_dist, node, cutoff=cutoff)
            elif search_type == 'time':
                dist, path = networkx.single_source_dijkstra(
                    self.graph_time, node, cutoff=cutoff)
            else:
                print 'invalid search type; valid values for variable - distance or time'
                return None
        else:
            print 'Source node not found in the graph'
            return None
        return dist, path

if __name__ == "__main__":

    import time
    """
    g = Graph()
    ti = time.time()
    g.read_data('Links_tt_24hrs.csv')
    net_graph = g.build_static_graph()
    ti = time.time()
    print '\n\tNumber of nodes accessible subject to spatio-temporal constraints- '

    for i in range(10):
        #netowrkx single_source_dijkstra code was modified to mot save paths
        locs = g.build_prism_between_nodes_static(net_graph, 4378, 4727, 601., 3000.)
    #print '\t', len(locs)
    print '\tTime Taken for 10 STATIC Prism query', (time.time()-ti)
    
    """
    g = Graph()
    ti = time.time()
    g.read_data('Links_tt_24hrs.csv')
    g.process_data()
    g.create_arc_index()
    net_graph = g.build_graph()

    print '\n\tNumber of nodes accessible subject to spatio-temporal constraints- '

    for i in range(10):
        # netowrkx single_source_dijkstra code was modified to mot save paths
        locs = g.build_prism_between_nodes(net_graph, 4378, 4727, 601., 3000.)
    # print '\t', len(locs)
    print '\tTime Taken for 10 TIME DEPENDENT Prism query', (time.time() - ti)

    """
    print '\n1. Time to build the graph - %s' %(time.time()-ti)

    ti = time.time()
    #self.build_prism_between_nodes(net_graph, 1, 9, 2, 8)
    print '\n2. Testing Arrival Time'
    print g.arrival_time(3002, 11965, 1)
    print g.arrival_time(3002, 11965, 151)
    print g.arrival_time(3002, 11965, 301)
    print g.arrival_time(3002, 11965, 451)

    print '\n3. Testing Departure Time'
    g.departure_time(3002, 11965, 1)
    g.departure_time(3002, 11965, 151)
    g.departure_time(3002, 11965, 301)
    g.departure_time(3002, 11965, 451)
    print 'Time to query possible destinations - %s' %(time.time()-ti)

    

    print '\n4. Testing building a SPT from a source: Earliest Arrival'
    ti = time.time()
    print '\tNumber of locations accessible with no cutoff starting at 301 analysis interval'
    print '\t', len(g.build_tree_from_source_at_time(net_graph, 3002, 301))
    print '\tTime Taken:From a single source to entire network node - ', (time.time()-ti)
    ti = time.time()
    print '\n\tNumber of locations accessible starting at 301 subject to a 900 analysis interval cutoff'
    print '\t', len(g.build_tree_from_source_at_time(net_graph, 3002, 301, 900))
    print '\tTime Taken:From a single source to entire network node with a cutoff of i hour or 600 analysis intervals - ', (time.time()-ti)

    print '\n4. Testing building a SPT from a source: Latest Departure'
    ti = time.time()
    print '\n\tNumber of nodes accessible to reach 11984 by 900 analysis interval'
    print '\t', len(g.build_tree_to_dest_at_time(net_graph, 11984, 900))
    print '\tTime Taken:From a single source to entire network node - ', (time.time()-ti)
    ti = time.time()
    print '\n\tNumber of nodes accessible to reach 11984 by 900 and should not start before 601 analysis interval'
    print '\t', len(g.build_tree_to_dest_at_time(net_graph, 11984, 900, 601))
    print '\tTime Taken:From a single source to entire network node with a cutoff of i hour or 600 analysis intervals - ', (time.time()-ti)
    
    ti = time.time()
    print '\n5. Locations within Prism with Start Anchor -8232, 600s and End Anchor - 12236, 900s'
    print '\n\tNumber of nodes accessible subject to spatio-temporal constraints is - '
    #locs = g.build_prism_between_nodes(net_graph, 8232, 12236, 601., 6000.)
    locs = g.build_prism_between_nodes(net_graph, 4378, 4727, 601., 3000.)
    print '\t', len(locs)
    print '\tTime Taken:Prism query', (time.time()-ti)

    f = open('prism_locs.csv', 'w')
    for i in locs:
        f.write('%s,' %i)
        for j in locs[i]:
            f.write('%s,' %j)
        f.write('\n')


    

    ti = time.time()
    g = Graph()
    g.read_data('Links_tt_24hrs.csv')
    g.process_data()
    g.create_arc_index()
    g.build_time_expanded_graph()
    #for i in g.graph_time.nodes()[:5]:
    #    print 'Node - ', i
    #    dist, path = g.shortest_path_tree(i, cutoff=600)
    #    print 'number of paths within 10 minutes - ', len(path)

    print 'time taken - %.4f' %(time.time()-ti)
   """
