class ProjectConfiguration(object):
    """Project configuration object stores key inputs and project """
    """attributes for the OpenAMOS project."""

    
    def __init__(self, 
                 name,
                 location, 
                 seed=0, 
                 subsample=None):
        
        self.name = name
        self.location = location
        self.seed = seed
        self.subsample = subsample

    def __repr__(self):
        return ("""Project Configuration:\n\tName - %s"""\
            """\n\tLocation - %s"""\
            """\n\tSeed - %s"""\
            """\n\tSubSample - %s""" %(self.name, self.location, 
                                       self.seed, self.subsample))

#unit test to test the code
import unittest

#define a class for testing
class TestProjectConfiguration(unittest.TestCase):
    #only initialize objects here
    def setUp(self):
        self.name = ''


    def testDB(self):
        #test to connect to database 
        DBobj = ProjectConfiguration(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        print DBobj


if __name__ == '__main__':
    unittest.main()