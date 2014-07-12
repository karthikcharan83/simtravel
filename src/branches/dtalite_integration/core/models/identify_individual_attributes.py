from openamos.core.agents.person import Person
from openamos.core.agents.household import Household
from openamos.core.agents.activity import ActivityEpisode
from openamos.core.models.abstract_model import Model
from openamos.core.data_array import DataArray

from pandas import DataFrame as df

class IdentifyIndividualAttributes(Model):

    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification
        self.activityAttribs = self.specification.activityAttribs
        self.colNames = [self.activityAttribs.hidName,
                         self.activityAttribs.pidName,
                         self.activityAttribs.starttimeName,
                         self.activityAttribs.endtimeName]
        self.hidName = self.activityAttribs.hidName
        self.pidName = self.activityAttribs.pidName
        self.scheduleidName = self.activityAttribs.scheduleidName
        self.activitytypeName = self.activityAttribs.activitytypeName
        self.locationidName = self.activityAttribs.locationidName
        self.starttimeName = self.activityAttribs.starttimeName
        self.endtimeName = self.activityAttribs.endtimeName
        self.durationName = self.activityAttribs.durationName
        self.depPersonIdName = self.activityAttribs.dependentPersonName

    def resolve_consistency(self, data, seed, numberProcesses):
        pschedulesGrouped = data.data.groupby(level=[0,1], sort=False)   
        
        verts = df(columns=self.colNames)
        verts[self.hidName] = pschedulesGrouped[self.hidName].min()
        verts[self.pidName] = pschedulesGrouped[self.pidName].min()
        verts[self.starttimeName] = pschedulesGrouped[self.starttimeName].min()
        verts[self.endtimeName] = pschedulesGrouped[self.endtimeName].max()  
        
        return DataArray(verts.values, self.colNames, 
                                  indexCols=[self.hidName, self.pidName])
        """
        for (hid, pid),  pidSchedules in data.data.groupby(level=[0, 1], axis=0):
            #householdObject = Household(hid)
            #for pid,  pidSchedules in hidSchedules.groupby(level=1, axis=0):
                min_starttime,  max_endtime = self.return_vertices(pidSchedules)
                pVerts = [hid,  pid,  min_starttime,  max_endtime]
                verts.append(pVerts)
        #raw_input("Completed the vertex identification in %.4f" %(time.time()-ti))
        return DataArray(verts, self.colNames)
    """

    def return_vertices(self, pidSchedules):
        min_starttime = pidSchedules[self.starttimeName].min()
        max_endtime = pidSchedules[self.endtimeName].max()
        return min_starttime,  max_endtime

