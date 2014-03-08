

class ActivityEpisode(object):
    def __init__(self, hid, pid, scheduleId, actType, 
		 location, startTime, endTime, duration, personId=0, tripCount=0):
        self.scheduleId = scheduleId
	self.hid = hid
	self.pid = pid
        self.actType = actType
        self.startTime = startTime
        self.endTime = endTime
        self.location = location
        self.duration = self.endTime - self.startTime
	self.dependentPersonId = personId
	self.tripCount = tripCount
        self._first_episode_check()
        self._last_episode_check()
	self.activities_subsumed = {}

    def _first_episode_check(self):
        self.startOfDay = self.startTime == 0

    def _last_episode_check(self):
        self.endOfDay = self.endTime == 1439

	
    def add_activities_subsumed(self, depAct):
	#self.activities_subsumed
	pass


    def prev_activity(self, prevAct):
	self.prevAct = prevAct

    def subs_activity(self, subsAct):
	self.subsAct = subsAct

	
    def __repr__(self):
        return """schid - %s, hid - %s, pid - %s, acttype - %s, """\
            """loc - %s, """\
            """start - %s, end - %s, dur - %s, """\
	    """depPId - %s, stFLag-%s, endFlag-%s, tripCnt-%s"""% (self.scheduleId, 
				      self.hid, self.pid, 
				      self.actType, self.location,
		                      self.startTime, self.endTime, self.duration,
			              self.dependentPersonId, 
				      self.startOfDay, self.endOfDay, self.tripCount)

