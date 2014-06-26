from numpy import array, zeros
from numpy.random import randint, seed
import time

from openamos.core.malta_integration.simulation_manager_malta import SimulationManager


class DummyMALTA(object):

    def __init__(self):
        self.trips = {}
        self.tripsAct = {}

        self.manager = SimulationManager()

    def request_trips(self):
        #self.tripsActDum = {117:[4], 155:[8], 133:[2], 147:[11], 167:[16]}
        for i in range(1440):
            seed(i)
            time = i + 1

            if (i >= 603 and i <= 610):
                #raw_input('check the schedules for drop off readjustment????')
                pass

            if time in self.tripsAct.keys():
                # if time in self.tripsActDum.keys():
                print 'Following trips have reached the destination in time - %s' % time, self.tripsAct[time]
                # print 'Following trips have reached the destination in time -
                # %s' %time, self.tripsActDum[time]
                tripIdsArrived = self.tripsAct.pop(time)
                tripArrivedDist = [0] * len(tripIdsArrived)
                #tripIdsArrived = self.tripsActDum.pop(time)
                tripInfoArrivals = array(tripIdsArrived + tripArrivedDist)
            else:
                tripInfoArrivals = array([-1])

            trips = self.manager.run_selected_components_for_malta(
                analysisInterval=time, tripInfoArrivals=tripInfoArrivals)

            if trips[0, 0] <> 0:
                print trips.astype(int)
                for trip in trips:
                    # key = endtime and val list = trips
                    if trip[8] not in self.trips.keys():
                        self.trips[trip[8]] = [trip[0]]
                    else:
                        self.trips[trip[8]] += [trip[0]]

                    #actArrival = randint(trip[7]+2, trip[8]+15)
                    #actArrival = randint(trip[7]+15, trip[8]+45)

                    actArrival = trip[8] + 1
                    """
		    if trip[8] - trip[7] == 1:
			actArrival = trip[8] + 1
		    else:
			actArrival = trip[8]		    


		    if trip[8] > trip[7] + 1:
			actArrival = trip[8]			
		    else:
			actArrival = trip[8] + 1

		    """

                    if actArrival not in self.tripsAct.keys():
                        self.tripsAct[actArrival] = [trip[0]]
                    else:
                        self.tripsAct[actArrival] += [trip[0]]

                    # if trip[0] >= 70 and trip[0] <=80:
                    #	print 'tripid - %s, expected arrival - %s and actual arrival - %s' %(trip[0], trip[8], actArrival)
                    #	raw_input()


if __name__ == '__main__':
    d = DummyMALTA()
    ti = time.time()
    d.request_trips()
    print 'Total time taken to simulate - ', time.time() - ti
