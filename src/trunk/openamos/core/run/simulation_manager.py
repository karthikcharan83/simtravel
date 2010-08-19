import copy
from lxml import etree
from numpy import array, ma

from openamos.core.component.config_parser import ConfigParser
from openamos.core.database_management.query_browser import QueryBrowser
from openamos.core.errors import ConfigurationError
from openamos.core.data_array import DataArray
from openamos.core.run.dataset import DB

class ComponentManager(object):
    """
    The class reads the configuration file, creates the component and model objects,
    and runs the models to simulate the various activity-travel choice processes.

    If the configObject is invalid, then a valid fileLoc is desired and if that fails
    as well then an exception is raised. In a commandline implementation, fileLoc will
    be passed.
    """

    def __init__(self, configObject=None, fileLoc=None, component=None):
        if configObject is None and fileLoc is None:
                raise ConfigurationError, """The configuration input is not valid; a """\
                """location of the XML configuration file or a valid etree """\
                """object must be passed"""

        if not isinstance(configObject, etree._ElementTree) and configObject is not None:
            print ConfigurationError, """The configuration object input is not a valid """\
                """etree.Element object. Trying to load the object from the configuration"""\
                """ file."""

        try:
            configObject = etree.parse(fileLoc)
        except Exception, e:
            print e
            raise ConfigurationError, """The path for configuration file was """\
                """invalid or the file is not a valid configuration file."""

        self.configObject = configObject
        self.configParser = ConfigParser(configObject) #creates the model configuration parser


    def establish_databaseConnection(self):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        self.queryBrowser = QueryBrowser(dbConfigObject)
        self.queryBrowser.dbcon_obj.new_connection()
        self.queryBrowser.create_mapper_for_all_classes()
        print 'Database Connection Established'

        
        """
        Example Query:
        hhld_class_name = 'households'
        query_gen, cols = queryBrowser.select_all_from_table(hhld_class_name)
        
        c = 0
        for i in query_gen:
            c = c + 1
            if c > 10:
                break
            print i.houseid
        print dir(i)
        """

    def establish_cacheDatabase(self):
        db = DB('w')
        db.create()
        return db
        
        
    def run_components(self, db):
        componentList = self.configParser.parse_models()
        
        for i in componentList:
            print '\nRunning Component - %s' %(i.component_name)
            for j in i.model_list:
                print '\tModel - ', j.dep_varname
                
            variableList = i.variable_list
            #print '\tVariable List - ', len(variableList)
            vars_inc_dep = self.prepare_vars(variableList, i)
            data = self.prepare_data(vars_inc_dep)        
            print '\t',(['houseid', 'vehid', 'numvehs', 'vehtype'])                                                
            print data.columns(['houseid', 'vehid', 'numvehs', 'vehtype'])
            i.run(data, db)

        print '\t',(['houseid', 'vehid', 'numvehs', 'vehtype'])                                                        
        print data.columns(['houseid', 'vehid', 'numvehs', 'vehtype'])

            

    def prepare_vars(self, variableList, component):
        #print variableList
        indep_columnDict = self.prepare_vars_independent(variableList)
        print '\tIndependent Column Dictionary - '#, indep_columnDict

        dep_columnDict = {}
        prim_keys = {}
        index_keys = {}

        for model in component.model_list:
            depVarName = model.dep_varname
            depVarTable = model.table
            if depVarTable in dep_columnDict:
                dep_columnDict[depVarTable].append(depVarName)
            else:
                dep_columnDict[depVarTable] = [depVarName]
        
            if model.key is not None:
                prim = model.key[0]

                if prim is not None:
                    if depVarTable not in prim_keys:
                        prim_keys[depVarTable] = prim
                    else:
                        prim_keys[depVarTable] = prim_keys[depVarTable] + prim
                        
                index = model.key[1]
                if index is not None:
                    if depVarTable not in index_keys:
                        index_keys[depVarTable] = index
                    else:
                        index_keys[depVarTable] = index_keys[depVarTable] + index
                        
        print '\tDependent Column Dictionary - '#, dep_columnDict
        print '\tPrimary Keys - '#, prim_keys
        print '\tIndex Keys - '#, index_keys
       
        columnDict = self.update_dictionary(indep_columnDict, dep_columnDict)
        prim_keysNoDuplicates = self.return_keys_toinclude(prim_keys)
        #print '\tPrimary Keys - ', prim_keysNoDuplicates
        columnDict = self.update_dictionary(columnDict, prim_keysNoDuplicates)
        index_keysNoDuplicates = self.return_keys_toinclude(index_keys)
        #print '\tIndex Keys - ', index_keysNoDuplicates
        columnDict = self.update_dictionary(columnDict, index_keysNoDuplicates)

        
        #print '\tCombined Column Dictionary - ', columnDict
        return columnDict
        

    def prepare_vars_independent(self, variableList):
        # Here we append attributes for all columns that appear on the RHS in the 
        # equations for the different models

        indepColDict = {}
        for i in variableList:
            tableName = i[0]
            colName = i[1]
            if tableName in indepColDict:
                indepColDict[tableName].append(colName)
            else:
                indepColDict[tableName] = [colName]

        return indepColDict


    def update_dictionary(self, dict_master, dict_to_merge):
        dict_m = copy.deepcopy(dict_master)

        for key in dict_to_merge:
            if key in dict_m:
                dict_m[key] = list(set(dict_m[key] + dict_to_merge[key]))
            else:
                dict_m[key] = dict_to_merge[key]

        return dict_m

    def return_keys_toinclude(self, keys, prim_keys_ind=None):
        keysList = []
        keysNoDuplicates = {}
        for i in keys:
            if prim_keys_ind and i.find('_r') > -1:                
                print 'primary keys and _r (result) table found'
                continue
            if len(set(keys[i]) & set(keysList)) == 0:
                keysNoDuplicates[i] = keys[i]
                keysList = keysList + keys[i]
                #print '%s not in - ' %(i), keysList, i not in keysList
        return keysNoDuplicates
            
            
    def prepare_data(self, columnDict):
        print columnDict
        maxDict = {'vehicles_r':['vehid']}
        query_gen, cols = self.queryBrowser.select_join(columnDict, 
                                                        ['houseid'], 
                                                        ['households', 'households_r', 'vehicles_r'],
                                                        maxDict)

        data = []
        c = 1
        for i in query_gen:
            #print i
            c = c + 1
            if c > 10:
                #break
                pass
            data.append(i)
        #data = array(data)
        #print data
        #data.dtype=int
        #print data
        #print 'THE MASK'
        mask = ma.masked_values(data, None).mask
        data = array(data)
        data[mask] = 0
        data = DataArray(data, cols)
        
        print '\tNumber of records fetched - ', data.data.shape
        return data
    

    def process_data_for_locs(self):
        """
        This method is called whenever there are location type queries involved as part
        of the model run. Eg. In a Destination Choice Model, if there are N number of 
        random location choices, and there is a generic MNL specifcation then in addition
        to generating the choices, one has to also retrieve the travel skims corresponding
        to the N random location choices.
        """
        pass


# Storing data ??                                                                                                             
# Linearizing data for calculating activity-travel choice attributes??                                                        
# how to update data like schedules, open periods etc.??

# create component list object
# iterate through component list
# - read the variable list
# - retrieve data
# - process the data further for retrieving accessibilities <>
# - update model objects/equation specifications for generic choice models
# - simulate
# - 


if __name__ == '__main__':
    fileloc = '/home/kkonduri/simtravel/test/VehOwn.xml'
    componentManager = ComponentManager(fileLoc = fileloc)
    componentManager.establish_databaseConnection()
    db = componentManager.establish_cacheDatabase()
    componentManager.run_components(db)

