class HouseholdEvolutionSpecification(object):
    def __init__(self, idSpec, agentType, hhldAttribs=None,
                 personAttribs=None, evolutionAttribs=None):
	self.idSpec = idSpec
	self.agentType = agentType
	self.hhldAttribs = hhldAttribs
	self.personAttribs = personAttribs
	self.evolutionAttribs = evolutionAttribs

	self.choices = None
	self.coefficients = None


class IdSpecification(object):
    def __init__(self, hidName, pidName):
	self.hidName = hidName
	self.pidName = pidName

class HouseholdAttributesSpecification(object):
    def __init__(self, bldgszName, hhtName, hincName, 
		 nocName, personsName, unittypeName,	
		 vehiclName, wifName, yrMovedName):
	self.bldgszName = bldgszName
	self.hhtName = hhtName
	self.hincName = hincName
	self.nocName = nocName
	self.personsName = personsName
	self.unittypeName = unittypeName
	self.vehiclName = vehiclName
	self.wifName = wifName
	self.yrMovedName = yrMovedName

class PersonAttributesSpecification(object):
    def __init__(self, ageName, clwkrName, educName,
		 enrollName, esrName, indnaicsName,	
		 occcen5Name, race1Name, relateName,
		 sexName, marstatName, hoursName,
		 gradeName, hispanName):
	self.ageName = ageName
	self.clwkrName = clwkrName
	self.educName = educName
	self.enrollName = enrollName
	self.esrName = esrName
	self.indnaicsName = indnaicsName
	self.occcen5Name = occcen5Name
	self.race1Name = race1Name
	self.relateName	= relateName	
	self.sexName = sexName
	self.marstatName = marstatName
	self.hoursName = hoursName
	self.gradeName = gradeName
	self.hispanName = hispanName

	
class EvolutionAttributesSpecification(object):
    def __init__(self, mortality_fName, birth_fName, 
		 age_fName,
		 enrollment_fName, 
		 grade_fName, educ_fName, educInYears_fName, 
		 residenceType_fName, laborParticipation_fName,
		 occupation_fName, income_fName, 
		 marriageDecision_fName, divorceDecision_fName):
	self.morality_fName = mortality_fName
	self.birth_fName = birth_fName
	self.age_fName = age_fName
	self.enrollment_fName = enrollment_fName
	self.grade_fName = grade_fName
	self.educ_fName = educ_fName
	self.educInYears_fName = educInYears_fName
	self.residenceType_fName = residenceType_fName
	self.laborParticipation_fName = laborParticipation_fName
	self.occupation_fName = occupation_fName
	self.income_fName = income_fName
	self.marriageDecision_fName = marriageDecision_fName
	self.divorceDecision_fName = divorceDecision_fName

	


