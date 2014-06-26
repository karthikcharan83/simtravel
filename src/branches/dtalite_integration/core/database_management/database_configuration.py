# class to define the the database object configuration
# import all the libraries
import os


class DataBaseConfiguration(object):

    """Database configuration object is the structure of the database.
    The object describes the attributes to connect to the database.
    for now using the __init__ method to define the object"""

    def __init__(self,
                 protocol=None,
                 user_name=None,
                 password=None,
                 host_name=None,
                 database_name=None):

        self.protocol = protocol
        self.user_name = user_name
        self.password = password
        self.host_name = host_name
        self.database_name = database_name

        # DBConnection.__init__(self,
        #               protocol = protocol,
        #               user_name = user_name,
        #               password = password,
        #               host_name = host_name,
        #               database_name = database_name
        #               )
        #self.database_name = database_name

    def __repr__(self):
        return 'Inside database configuration class %s://%s:%s@%s:5432/%s' % (self.protocol, self.user_name,
                                                                              self.password, self.host_name,
                                                                              self.database_name)


# unit test to test the code
import unittest

# define a class for testing


class TestDBConfiguration(unittest.TestCase):
    # only initialize objects here

    def setUp(self):
        self.protocol = 'postgres'
        self.user_name = 'postgres'
        self.password = '1234'
        self.host_name = 'localhost'
        self.database_name = 'test'

    def testDB(self):
        # test to connect to database
        DBobj = DataBaseConfiguration(
            self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        print DBobj


if __name__ == '__main__':
    unittest.main()
