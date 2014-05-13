'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''

import copy
import time
import re
from lxml import etree
from numpy import array

import openamos
from openamos.core.models.linear_regression_model import LinearRegressionModel
from openamos.core.models.log_linear_regression_model import LogLinearRegressionModel
from openamos.core.models.approx_log_linear_regression_model import ApproxLogRegressionModel
from openamos.core.models.stochastic_frontier_regression_model import StocFronRegressionModel
from openamos.core.models.log_stochastic_frontier_regression_model import LogStocFronRegressionModel
from openamos.core.models.count_regression_model import CountRegressionModel
from openamos.core.models.logit_choice_model import LogitChoiceModel
from openamos.core.models.ordered_choice_model import OrderedModel
from openamos.core.models.probability_distribution_model import ProbabilityModel
from openamos.core.models.nested_logit_choice_model import NestedLogitChoiceModel
from openamos.core.models.interaction_model import InteractionModel
from openamos.core.models.model_components import Specification
from openamos.core.models.model_components import ColumnOperationsSpecification
from openamos.core.models.count_regression_model_components import CountSpecification
from openamos.core.models.ordered_choice_model_components import OLSpecification
from openamos.core.models.nested_logit_model_components import NestedChoiceSpecification, NestedSpecification
from openamos.core.models.error_specification import LinearRegErrorSpecification
from openamos.core.models.error_specification import StochasticRegErrorSpecification
from openamos.core.models.schedules_model_components import ReconcileSchedulesSpecification
from openamos.core.models.schedules_model_components import ActivityAttribsSpecification
from openamos.core.models.schedules_model_components import DailyStatusAttribsSpecification
from openamos.core.models.schedules_model_components import DependencyAttribsSpecification
from openamos.core.models.schedules_model_components import HouseholdSpecification
from openamos.core.models.schedules_model_components import TripDependentPersonAttributes
from openamos.core.models.schedules_model_components import PersonsArrivedAttributes
from openamos.core.models.schedules_model_components import TripOccupantSpecification
from openamos.core.models.schedules_model_components import ArrivalInfoSpecification
from openamos.core.models.schedules_model_components import OccupancyInfoSpecification
from openamos.core.models.schedules_model_components import PersonsArrivedSpecification
from openamos.core.models.schedules_model_components import UniqueRecordsSpecification
from openamos.core.models.evolution_model_components import IdSpecification
from openamos.core.models.evolution_model_components import HouseholdAttributesSpecification
from openamos.core.models.evolution_model_components import PersonAttributesSpecification
from openamos.core.models.evolution_model_components import EvolutionAttributesSpecification
from openamos.core.models.evolution_model_components import HouseholdEvolutionSpecification
from openamos.core.models.population_synthesis_model_components import PopGenModelSpecification
from openamos.core.models.reconcile_schedules import ReconcileSchedules
from openamos.core.models.child_dependency_processing import ChildDependencyProcessing
from openamos.core.models.clean_fixed_activity_schedule import CleanFixedActivitySchedule
from openamos.core.models.clean_aggregate_activity_schedule import CleanAggregateActivitySchedule
from openamos.core.models.population_evolution_processing import PopulationEvolutionProcessing
from openamos.core.models.trip_occupant_processing import TripOccupantProcessing
from openamos.core.models.persons_arrived_processing import PersonsArrivedProcessing
from openamos.core.models.unique_records_processing import UniqueRecordsProcessing
from openamos.core.models.adjust_schedules import AdjustSchedules
from openamos.core.models.emigration import Emigration
from openamos.core.models.immigration import Immigration
from openamos.core.models.column_operations_model import ColumnOperationsModel
from openamos.core.models.model import SubModel
from openamos.core.malta_integration.abstract_component_malta import AbstractComponent
from openamos.core.activity_travel.activity_travel_components import HistoryInfo, HouseholdStructureInfo
from openamos.core.spatial_analysis.spatial_query_components import SpatioTemporalConstraint, PrismConstraints
from openamos.core.travel_skims.travel_skims_components import TravelSkimsInfo
from openamos.core.travel_skims.locations_components import LocationsInfo
from openamos.core.database_management.database_configuration import DataBaseConfiguration
from openamos.core.project_configuration import ProjectConfiguration
from openamos.core.data_array import DataArray, DataFilter
from openamos.core.errors import ConfigurationError


class ConfigParser(object):
    """
    The class defines the parser for translating the model configuration
    file into python objects for execution.
    """

    def __init__(self, configObject, component=None):
        """
        The configObject should be an etree.ElementBase object, component is the
        keyword for the component until which componentList is desired. The component
        entry will be updated further to pick and choose components to run.
        """
        #TODO: filter_conditons, run_until conditions


        if not isinstance(configObject, etree._ElementTree):
            raise ConfigurationError, """The configuration input is not a valid """\
                """etree.ElementBase object"""

        self.configObject = configObject
        self.componentName = component

    def update_completedFlag(self, component_name, analysisInterval=None):
        return
        self.iterator = self.configObject.getiterator('Component')

        for compElement in self.iterator:
            if compElement.get('name') == component_name:
                if analysisInterval is None:
                    #print 'OLD FLAG _ ', compElement.get('completed')
                    #compElement.set('completed', "True")
                    #compElement.set('skip', "True")
                    #print 'NEW FLAG _ ', compElement.get('completed')
                    pass

                if analysisInterval is not None:
                    analysisIntervalElement = compElement.find('AnalysisInterval')
                    if analysisIntervalElement is None:
                        continue
                    #print 'OLD ANALYSIS INTERVAL START _ ', analysisIntervalElement.get('start')
                    analysisIntervalElement.set('start', str(analysisInterval + 1))
                    #print 'updated ANALYSIS INTERVAL START _ ', analysisIntervalElement.get('start')
                    #print dir(analysisIntervalElement)

                    endIntervalValue = int(analysisIntervalElement.get('end'))

                    if endIntervalValue == analysisInterval + 1:
                        #print 'OLD FLAG _ ', compElement.get('completed')
                        #compElement.set('completed', "True")
                        #compElement.set('skip', "True")
                        #print 'NEW FLAG _ ', compElement.get('completed')
                        pass

    def parse_models(self, projectSeed=0):
        ti = time.time()
        componentList = []
        for element in self.configObject.iter(tag=etree.Element):
            if element.tag == 'Component':
                #print 'Found component - ', element.get('name')
                componentList += self.parse_analysis_interval_and_create_component(element, projectSeed)
            elif element.tag == 'ComponentList':
                print 'Component list found - '

                interval_element = element.find("AnalysisInterval")
                if interval_element is not None:
                    startInterval = interval_element.get("start")
                    startInterval = int(startInterval)

                    endInterval = interval_element.get("end")
                    endInterval = int(endInterval)

                else:
                    startInterval = 0
                    endInterval = 1

                for i in range(endInterval - startInterval):
                    for subElement in element.getiterator('SubComponent'):
                        #print 'Found component in component list - ', subElement.get('name')
                        subComponentList = self.parse_analysis_interval_and_create_component(subElement, projectSeed,
                                                                                             analysisInterval=i+1)

                        for subComp in subComponentList:
                            for model in subComp.model_list:
                                model.seed +=  i

                            if interval_element is not None:
                                subComp.analysisInterval = startInterval + i
                        componentList += subComponentList

        print '\tTime taken to parse all the components - %.4f' %(time.time()-ti)
        #raw_input('waiting in config parse ... ')
        return componentList

    def parse_projectAttributes(self):
        print "-- Parse project attributes --"
        projectElement = self.configObject.find('Project')
        projectName = projectElement.get('name')
        projectLocation = projectElement.get('location')
        projectSubsample = projectElement.get('subsample')
        projectSeed = projectElement.get('seed')
        projectIteration = projectElement.get('iteration')
        if projectSeed is None:
            projectSeed = 0
        else:
            projectSeed = int(projectSeed)
        if projectSubsample is not None:
            projectSubsample = int(projectSubsample)

        if projectIteration is not None:
            projectIteration = int(projectIteration)
        else:
            projectIteration = 1

        projectConfigObject = ProjectConfiguration(projectName,
                                                   projectLocation,
                                                   projectSubsample,
                                                   projectSeed,
                                                   projectIteration)

        return projectConfigObject

    def parse_databaseAttributes(self):
        print "-- Parse database attributes --"
        dbConfig_element = self.configObject.find('DBConfig')
        protocol = dbConfig_element.get('dbprotocol')
        host = dbConfig_element.get('dbhost')
        dbname = dbConfig_element.get('dbname')
        username = dbConfig_element.get('dbusername')
        password = dbConfig_element.get('dbpassword')

        dbConfigObject = DataBaseConfiguration(protocol,
                                               username,
                                               password,
                                               host,
                                               dbname)
        return dbConfigObject

    def parse_tableHierarchy(self, component_element):
        #print "-- Parse table hierarchy --"
        dbTables_element = component_element.find('DBTables')
        tableIterator = dbTables_element.getiterator("Table")
        tableOrderDict = {}
        tableNamesKeyDict = {}
        for table_element in tableIterator:
            tableName = table_element.get("table")
            tableKeys = table_element.get("key")
            tableKeys = re.split('[,]', tableKeys)
            countKeys = table_element.get("count_key")
            if countKeys is not None:
                countKeys = re.split('[,]', countKeys)
            else:
                countKeys = []

            tableOrder = table_element.get("order")
            if tableOrder is not None:
                tableOrder = int(tableOrder)
                tableOrderDict[tableOrder] = [tableName, tableKeys]
            tableNamesKeyDict[tableName] = [tableKeys, countKeys]
        return tableOrderDict, tableNamesKeyDict


    def parse_network_tables(self):
        print "-- Parse skims tables' Time of Day information --"
        skims_element = self.configObject.find("NetworkSkims")

        periodIterator = skims_element.getiterator("Period")

        travelSkimsLookup = TravelSkimsInfo()

        for period_element in periodIterator:
            # Skim properties
            tablename = period_element.get("tablename")
            origin_var = period_element.get("origin_var")
            destination_var = period_element.get("destination_var")
            interval_start = int(period_element.get("intervalStart"))
            interval_end = int(period_element.get("intervalEnd"))

            # Network condition properties
            tt_period_element = period_element.find("Time")
            dist_period_element = period_element.find("Distance")

            tt_skim_var = tt_period_element.get("skim_var")
            tt_fileLocation = tt_period_element.get('fileLocation')
            tt_delimiter = tt_period_element.get('delimiter')

            if dist_period_element == None:
                dist_skim_var = None
                dist_fileLocation = None
                dist_delimiter = None
            else:
                dist_skim_var = dist_period_element.get("skim_var")
                dist_fileLocation = dist_period_element.get('fileLocation')
                dist_delimiter = dist_period_element.get('delimiter')


            travelSkimsLookup.add_tableInfoToList(tablename, origin_var,
                                                  destination_var,
                                                  interval_start,
                                                  interval_end,

                                                  tt_skim_var,
                                                  tt_fileLocation,
                                                  tt_delimiter,

                                                  dist_skim_var,
                                                  dist_fileLocation,
                                                  dist_delimiter)

        return travelSkimsLookup

    def parse_locations_table(self):
        print "-- Parse locations table --"
        locations_element = self.configObject.find("Locations")
        referenceTablename = locations_element.get("reference_tablename")
        tablename = locations_element.get("tablename")
        location_var = locations_element.get("location_var")
        indb_flag = locations_element.get("indb")

        variablesIterator = locations_element.getiterator("LocationVariable")

        variablesList = []
        for var_element in variablesIterator:
            varName = var_element.get("var")
            variablesList.append(varName)


        locationsInfo = LocationsInfo(tablename, referenceTablename,
                                      location_var, variablesList)

        return locationsInfo


    def parse_household_structure_info(self):
        print "-- Parse household structures --"
        structures_element = self.configObject.find("HouseholdStructure")
        tablename = structures_element.get('tablename')
        houseid = structures_element.get('houseid')
        personid = structures_element.get('personid')

        #prim_keys = re.split('[,]', keys_element)

        structuresIterator = structures_element.getiterator('Structure')

        structuresDict = {}
        for structure in structuresIterator:
            name = structure.get("name")
            var = structure.get("var")
            value = structure.get("value")

            structuresDict[name] = [var,int(value)]

        householdStructureInfoObject = HouseholdStructureInfo(tablename,
                                                              houseid,
                                                              personid,
                                                              structuresDict)
        return householdStructureInfoObject





    def parse_analysis_interval_and_create_component(self, component_element, projectSeed, analysisInterval=None):
        ti = time.time()
        comp_name, comp_read_table, comp_write_table, comp_write_to_table2 = self.return_component_attribs(component_element)
        print "Parsing Component - %s" %(comp_name)
        interval_element = component_element.find("AnalysisInterval")
        componentList = []
        if interval_element is not None:
            startInterval = interval_element.get("start")
            startInterval = int(startInterval)

            endInterval = interval_element.get("end")
            endInterval = int(endInterval)



            #repeatComponent = self.create_component(component_element)

            for i in range(endInterval - startInterval):
                #tempComponent = copy.deepcopy(repeatComponent)
                tempComponent = self.create_component(component_element, projectSeed, analysisInterval)
                for model in tempComponent.model_list:
                    model.seed +=  i
                tempComponent.analysisInterval = startInterval + i
                componentList.append(tempComponent)
            """
            repeatComponentList = [repeatComponent] * (endInterval - startInterval)
            for i in range(endInterval - startInterval):
                repeatComponentList[i].analysisInterval = startInterval + i
            componentList += repeatComponentList
            """

        else:
            component = self.create_component(component_element, projectSeed, analysisInterval)
            componentList.append(component)
        #print '\t\tTime taken to parse across all analysis intervals %.4f' %(time.time()-ti)

        return componentList


    def return_delete_records_criterion(self, component_element):
        delete_records_element = component_element.find("DeleteRecords")
        if delete_records_element is not None:
            delete_criterion = delete_records_element.get("value")
            if delete_criterion == "True":
                delete_criterion = True
            elif delete_criterion == "False":
                delete_criterion = False
        else:
            delete_criterion = None

        return delete_criterion


    def create_component(self, component_element, projectSeed=0, analysisInterval=None):
        self.model_list = []
        self.component_variable_list = []

        analysisIntervalFilter_element = component_element.find('AnalysisIntervalFilter')
        if analysisIntervalFilter_element is not None:
            analysisIntervalFilter = self.return_table_var(analysisIntervalFilter_element)
            analysisIntervalCondition = analysisIntervalFilter_element.get("condition")
            if analysisIntervalCondition == None or analysisIntervalCondition == "equals":
                analysisIntervalCondition = "="
            if analysisIntervalCondition == "less than":
                analysisIntervalCondition = "<"
        else:
            analysisIntervalFilter = None
            analysisIntervalCondition = None


        comp_name, comp_read_table, comp_write_table, comp_write_to_table2 = self.return_component_attribs(component_element)

        deleteCriterion = self.return_delete_records_criterion(component_element)




        tableOrder, tableKeys = self.parse_tableHierarchy(component_element)
        if comp_write_table is not None:
            comp_keys = tableKeys[comp_write_table]
        else:
            comp_keys = tableKeys[comp_read_table]

        if comp_write_to_table2 is not None:
            key2 = tableKeys[comp_write_to_table2]
        else:
            key2 = None

        spatialConstIterator = component_element.getiterator("SpatialConstraints")
        spatialConst_list = []
        for i in spatialConstIterator:
            spatialConst = self.return_spatial_query(i)
            spatialConst_list.append(spatialConst)


        dynamicSpatialConstIterator = component_element.getiterator("DynamicSpatialConstraints")
        dynamicSpatialConst_list = []
        for i in dynamicSpatialConstIterator:
            dynamicSpatialConst = self.return_spatial_query(i)
            dynamicSpatialConst_list.append(dynamicSpatialConst)


        preProcessData_element = component_element.find('PreProcessData')
        if preProcessData_element is not None:
            pre_run_filter = self.return_filter_condition_list(preProcessData_element)
            #print pre_run_filter
            #raw_input()
        else:
            pre_run_filter = None



        consistencyChecks_element = component_element.find("ConsistencyChecks")
        if consistencyChecks_element is not None:
            post_run_filter = self.return_filter_condition_list(consistencyChecks_element)
        else:
            post_run_filter = None

        historyInfo_element = component_element.find("HistoryInformation")
        if historyInfo_element is not None:
            historyInfoObject = self.return_history_info(historyInfo_element)
        else:
            historyInfoObject = None


        modelsIterator = component_element.getiterator("Model")
        for i in modelsIterator:
            self.create_model_object(i, projectSeed, analysisInterval)
            self.create_linear_object_for_locations(i, spatialConst_list)
            #component_variable_list = (component_variable_list
            #                           + variable_list)
            #model_list.append(model)
        #print self.component_variable_list


        #if spatialConst_list == []:
        #    spatialConst_list = None


        dependencyAllocationFlag = component_element.get("dependency")
        if dependencyAllocationFlag == "True":
            dependencyAllocationFlag = True
        else:
            dependencyAllocationFlag = False

        skipFlag = component_element.get("skip")
        if skipFlag == "True":
            skipFlag = True
        else:
            skipFlag = False

        agg_vars_dict = self.parse_aggregate_output(component_element)

        delete_dict = self.parse_delete_dict(component_element)

        self.component_variable_list = list(set(self.component_variable_list))

        model_list_noInteractionReplicates = []
        modelNames_interaction = []
        for model in self.model_list:
            #print model.dep_varname, 'Interaction model - ', isinstance(model.model, openamos.core.models.interaction_model.InteractionModel)
            if isinstance(model.model, openamos.core.models.interaction_model.InteractionModel):
                if model.data_filter is not None:
                    raise Exception, "the interaction model has a filter ... is this possible?"
                if model.dep_varname in modelNames_interaction:
                    continue
                else:
                    modelNames_interaction.append(model.dep_varname)
            model_list_noInteractionReplicates.append(model)

        #print 'len of original model list - ', len(self.model_list)
        self.model_list = model_list_noInteractionReplicates
        #print 'len of original model list - ', len(self.model_list)
        #print 'len of new modet list no replicates of interaction models', len(model_list_noInteractionReplicates)
        #raw_input()


        component = AbstractComponent(comp_name, self.model_list,
                                      self.component_variable_list,
                                      comp_read_table,
                                      comp_write_table,
                                      comp_keys,
                                      tableOrder,
                                      tableKeys,
                                      spatialConst_list,
                                      dynamicSpatialConst_list,
                                      analysisIntervalFilter = analysisIntervalFilter,
                                      analysisIntervalCondition = analysisIntervalCondition,
                                      history_info = historyInfoObject,
                                      post_run_filter=post_run_filter,
                                      delete_criterion=deleteCriterion,
                                      dependencyAllocationFlag = dependencyAllocationFlag,
                                      skipFlag = skipFlag,
                                      aggregate_variable_dict = agg_vars_dict,
                                      delete_dict = delete_dict,
                                      writeToTable2=comp_write_to_table2,
                                      key2 = key2,
                                      pre_run_filter = pre_run_filter)
        return component


    def parse_delete_dict(self, component_element):
        delete_dict = {}

        delete_element = component_element.find("DeleteBasedOn")
        if delete_element is None:
            return delete_dict

        table = delete_element.get('table')
        var = delete_element.get('var')

        delete_dict[table] = var

        return delete_dict


    def parse_aggregate_output(self, component_element):
        vars_dict = {}

        agg_output_element = component_element.find("Aggregate")
        if agg_output_element is None:
            return vars_dict

        variableIterator = agg_output_element.getiterator('Variable')


        for var_element in variableIterator:
            table, var = self.return_table_var(var_element)
            if table in vars_dict:
                vars_dict[table] += [var]
            else:
                vars_dict[table] = [var]

        return vars_dict




    def return_history_info(self, history_element):
        historyVarsIterator = history_element.getiterator("HistoryVar")
        histTableName = history_element.get('table')

        histAggVar = history_element.get('history_var')

        histVarAggConditions = {}
        for histVar_element in historyVarsIterator:
            conditions = self.return_var_values_list(histVar_element)
            histVar = histVar_element.get('var')
            histVarAggConditions[histVar] = conditions

        historyInfoObject = HistoryInfo(histTableName, histAggVar, histVarAggConditions)
        return historyInfoObject


    def return_var_values_list(self, histVar_element):
        histVarValuesIterator = histVar_element.getiterator('Aggregate')

        conditions = []
        for i in histVarValuesIterator:
            value = i.get('value')
            conditionVariable = i.get('condition_var')
            if value is not None:
                conditions.append('%s=%s' %(conditionVariable, value))

        return conditions




    def create_model_object(self, model_element, projectSeed=0, analysisInterval=None):
        model_formulation = model_element.attrib['formulation']
        #print "\tParsing model - %s, formulation - %s " %(model_element.get('name'), model_element.get('formulation'))
        #print model_formulation

        if model_formulation == 'Regression':
            self.create_regression_object(model_element, projectSeed)

        if model_formulation == 'Count':
            self.create_count_object(model_element, projectSeed)

        if model_formulation == 'Multinomial Logit':
            if model_element.find('AlternativeSet') is None:
                self.create_multinomial_logit_object(model_element, projectSeed)
            else:
                self.create_multinomial_logit_object_generic_locs(model_element, projectSeed)

        if model_formulation == 'Nested Logit':
            self.create_nested_logit_object(model_element, projectSeed)

        if model_formulation == 'Ordered':
            self.create_ordered_choice_object(model_element, projectSeed)

        if model_formulation == 'Probability Distribution':
            self.create_probability_object(model_element, projectSeed)

        if model_formulation == 'Reconcile Schedules':
            self.create_reconcile_schedules_object(model_element, projectSeed)

        if model_formulation == 'Clean Fixed Activity Schedule':
            self.create_clean_fixed_activity_schedule(model_element, projectSeed)

        if model_formulation == 'Clean Aggregate Activity Schedule':
            self.create_clean_aggregate_activity_schedule(model_element, projectSeed)

        if model_formulation == 'Child Dependency Allocation Terminal':
            self.create_child_dependency_allocation_object(model_element, terminal=True, projectSeed=projectSeed)


        if model_formulation == 'Child Dependency':
            self.create_child_dependency_allocation_object(model_element, terminal=False, projectSeed=projectSeed)

        if model_formulation == 'Column Operations':
            self.create_column_operations_object(model_element, projectSeed)

        if model_formulation == 'Evolution Post Process':
            self.create_evolution_post_process_object(model_element, projectSeed)

        if model_formulation == 'Emigration':
            self.create_migration_object(model_element, projectSeed, migrationType='Emigration')

        if model_formulation == 'Immigration':
            self.create_migration_object(model_element, projectSeed, migrationType='Immigration', analysisInterval=analysisInterval)

        if model_formulation == 'Trip Occupant Processing':
            self.create_trip_occupant_processing_object(model_element, projectSeed)

        if model_formulation == 'Persons On Trip Arrival Processing':
            self.create_persons_arrived_processing_object(model_element, projectSeed)

        if model_formulation == 'Schedule Adjustment':
            self.create_schedule_adjustment_object(model_element)

        if model_formulation == 'Identify Unique':
            self.create_unique_records_object(model_element, projectSeed)


    def process_seed(self, model_element):
        seed = model_element.get('seed')
        if seed is not None:
            return int(seed)
        else:
            return 1

    def create_regression_object(self, model_element, projectSeed=0):
        #model type
        model_type = model_element.get('type')
        seed = self.process_seed(model_element) + projectSeed

        #variable list required for running the model
        variable_list = []

        #dependent variable
        depvariable_element = model_element.find('DependentVariable')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        #print dep_varname, '----variable Name -----'
        choice = [dep_varname]

        # Creating the coefficients input for the regression model
        coeff_dict, vars_list = self.return_coeff_vars(model_element)
        coefficients = coeff_dict

        variable_list = variable_list + vars_list

        #print choice, coefficients
        # specification object
        specification = Specification(choice, coefficients)

        # Reading the vertex
        vertex = model_element.get('vertex')

        # Reading the threshold for the stochastic frontier
        lower_threshold = model_element.get('lower_threshold')
        upper_threshold = model_element.get('upper_threshold')

        if lower_threshold == None:
            lower_threshold = 0
        else:
            lower_threshold = float(lower_threshold)


        if upper_threshold == None:
            upper_threshold = 0
        else:
            upper_threshold = float(upper_threshold)

        # Creating the variance matrix
        model_type = model_element.get('type')

        varianceIterator = model_element.getiterator('Variance')

        if model_type in ['Linear', 'Log Linear', 'Approx Log'] :
            for i in varianceIterator:
                variance = array([[float(i.get('value'))]])
            errorSpec = LinearRegErrorSpecification(variance, vertex,
                                                    lower_threshold,
                                                    upper_threshold)
            if model_type == 'Linear':
                model = LinearRegressionModel(specification, errorSpec)
            elif model_type == 'Log Linear':
                model = LogLinearRegressionModel(specification, errorSpec)
            elif model_type == 'Approx Log':
                model = ApproxLogRegressionModel(specification, errorSpec)
        """
        if model_type == 'Log Linear':
            for i in varianceIterator:
                variance = array([[float(i.get('value'))]])
            errorSpec = LinearRegErrorSpecification(variance)
            model = LogLinearRegressionModel(specification, errorSpec)
        """

        if model_type in ['Stochastic Frontier', 'Log Stochastic Frontier']:
            for i in varianceIterator:
                variance_type = i.get('type', default=None)
                if variance_type == None:
                    norm_variance = float(i.get('value'))
                elif variance_type == 'Half Normal':
                    half_norm_variance = float(i.get('value'))

            variance = array([[norm_variance, 0],[0, half_norm_variance]])
            errorSpec = StochasticRegErrorSpecification(variance, vertex,
                                                        lower_threshold,
                                                        upper_threshold)

            if model_type == 'Stochastic Frontier':
                model = StocFronRegressionModel(specification, errorSpec)
            else:
                model = LogStocFronRegressionModel(specification, errorSpec)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model_type = 'regression'
        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)

        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list


    def create_count_object(self, model_element, projectSeed=0):
        #model type
        model_type = model_element.get('type')
        seed = self.process_seed(model_element) + projectSeed
        #variable list required for running the model
        variable_list = []

        #dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        #Creating the coefficients input for the regression model
        coeff_dict, vars_list = self.return_coeff_vars(model_element)
        coefficients = coeff_dict

        variable_list = variable_list + vars_list

        # dependent variable
        variable = model_element.get('name')

        # alternatives and values-categorues lookup
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        values = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)
            value = i.get('value')
            if value is not None:
                values.append(float(value))
            #print alternative, value

        if len(values) == 0:
            values = None

        # specification object
        specification = CountSpecification(choice, coefficients)

        # filters
        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)


        model_type = 'choice'
        model = CountRegressionModel(specification)
        model_object = SubModel(model, model_type, dep_varname, dataFilter, runUntilFilter,
                                values=values, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)

        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list


    def create_multinomial_logit_object(self, model_element, projectSeed=0):
        """
        Accomodates both generic and alternative specific where the
        alternatives are spelled out
        """
        #print 'INSIDE LOGIT MODEL NOTTTT FOR LOCATIONS'

        #model type
        model_type = model_element.get('type')
        seed = self.process_seed(model_element) + projectSeed

        #variable_list_required for running the model
        variable_list = []

        # dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #print dep_varname, "inside, regiular"

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        # alternatives
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        coefficients_list = []
        values = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)
            value = i.get('value')
            if value is not None:
                values.append(float(value))
            if model_type == 'Alternative Specific':
                coeff_dict, vars_list = self.return_coeff_vars(i)
                coefficients_list = coefficients_list + coeff_dict
                variable_list = variable_list + vars_list
        if model_type <> 'Alternative Specific':
            coeff_dict, vars_list = self.return_coeff_vars(model_element)
            coefficients_list = coefficients_list + coeff_dict
            coefficients_list = coefficients_list*len(choice)
            variable_list = variable_list + vars_list

        if len(values) == 0:
            values = None

        #print dep_varname

        # logit specification object
        specification = Specification(choice, coefficients_list)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = LogitChoiceModel(specification)
        model_type = 'choice'                   #Type of Model
        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, values=values, seed=seed,
                                filter_type=filter_type,
                                run_filter_type=run_filter_type)#Model Object

        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list


    def create_multinomial_logit_object_generic_locs(self, model_element, projectSeed=0):
        """
        Accomodates alternative specific where the
        alternatives are not spelled out. Like for location choices
        """

        #print 'INSIDE LOGIT MODEL FOR LOCATIONS'

        #model type
        model_type = model_element.get('type')
        seed = self.process_seed(model_element) + projectSeed

        #variable_list_required for running the model
        variable_list = []

        # dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        #print dep_varname, 'other one'
        # alternatives
        altSetElement = model_element.find('AlternativeSet')
        alternativeSet = int(altSetElement.get('count'))
        #print 'alternativeSet --->', alternativeSet
        choice = []
        coefficients_list = []
        values = []

        for i in range(alternativeSet):
            alternative = dep_varname + str(i+1)
            choice.append(alternative)
            value = i + 1
            values.append(float(value))
            #variable_list.append(('temp', alternative))

        coeff_list, vars_list = self.return_coeff_vars(model_element, alternativeSet)
        #print vars_list, 'VARIABLES LISTTTTTTTT'
        #print coeff_list, 'COEFFICIENTS LISTTTTTTT'

        #print dep_varname

        # logit specification object
        specification = Specification(choice, coeff_list)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = LogitChoiceModel(specification)
        model_type = 'choice'                   #Type of Model
        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, values=values, seed=seed,
                                filter_type=filter_type,
                                run_filter_type=run_filter_type)#Model Object

        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list


    def create_linear_object_for_locations(self, model_element, spatialConst_list, projectSeed=0):
        """
        creates linear combination objects for locations and travel times
        """

        seed = self.process_seed(model_element) + projectSeed
        altSetElement = model_element.find('AlternativeSet')
        if altSetElement is None or spatialConst_list is None:
            return

        for const in spatialConst_list:
            if const.countChoices is not None:
                depvariable_element = model_element.find('DependentVariable')
                dep_varname = depvariable_element.get('var')

                countChoices = const.countChoices
                destinationField = const.destinationField

                #Filter set
                filter_set_element = model_element.find('FilterSet')
                if filter_set_element is not None:
                    filter_type = filter_set_element.get('type')
                else:
                    filter_type = None

                #Filter set
                run_filter_set_element = model_element.find('RunUntilConditionSet')
                if run_filter_set_element is not None:
                    run_filter_type = run_filter_set_element.get('type')
                else:
                    run_filter_type = None

                dataFilter = self.return_filter_condition_list(model_element)
                runUntilFilter = self.return_run_until_condition(model_element)

                choice = [dep_varname]
                variance = array([[0.0]])
                errorSpec = LinearRegErrorSpecification(variance)
                model_type = 'regression'

                variableIterator = model_element.getiterator('Variable')
                rep_var_list = []
                for variable_element in variableIterator:
                    rep_var = variable_element.get('repeat')

                    if rep_var is not None:
                        rep_var_list += re.split('[,]', rep_var)



                for i in range(countChoices):

                    # additional data filter
                    dataFilterLoc = DataFilter(dep_varname, 'equals', i+1)

                    """
                    #Models to populate the travel time to destination variable
                    var = const.asField
                    coefficients = [{'%s%s'%(var, i+1):1}]
                    specification = Specification([var], coefficients)
                    model = LinearRegressionModel(specification, errorSpec)
                    model_type = 'regression'
                    model_object = SubModel(model, model_type, var, dataFilter + [dataFilterLoc],
                                            runUntilFilter, seed=seed, filter_type=filter_type,
                                            run_filter_type=run_filter_type)
                    self.model_list.append(model_object)

                    #Models to populate the travel time from destination variable
                    var = 'tt_from'
                    coefficients = [{'%s%s'%(var, i+1):1}]
                    specification = Specification([var], coefficients)
                    model = LinearRegressionModel(specification, errorSpec)
                    model_type = 'regression'
                    model_object = SubModel(model, model_type, var, dataFilter + [dataFilterLoc],
                                            runUntilFilter, seed=seed, filter_type=filter_type,
                                            run_filter_type=run_filter_type)
                    self.model_list.append(model_object)
                    """
                    #Models to populate the location id variable
                    coefficients = [{'%s%s'%(destinationField, i+1):1}]
                    specification = Specification(choice, coefficients)
                    model = LinearRegressionModel(specification, errorSpec)
                    model_object = SubModel(model, model_type, dep_varname, dataFilter + [dataFilterLoc],
                                            runUntilFilter, seed=seed, filter_type=filter_type,
                                            run_filter_type=run_filter_type)
                    self.model_list.append(model_object)


    def create_nested_logit_object(self, model_element, projectSeed=0):
        #variable list required for running the model
        variable_list = []
        seed = self.process_seed(model_element) + projectSeed
        #dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        #Specification dict
        spec_build_ind = {}


        #building the nest structure
        nest_struct = {}
        spec_dict = {}
        alts = []
        values = []
        alternativeIterator = model_element.getiterator('Alternative')
        for i in alternativeIterator:
            name = i.get('id')
            value = i.get('value')
            if value is not None:
                values.append(float(value))
            coeff_dict, vars_list = self.return_coeff_vars(i)
            variable_list = variable_list + vars_list
            spec = NestedChoiceSpecification([name], coeff_dict)
            spec_build_ind[name] = spec

            branch = i.get('branch')

            parents = branch.strip().split('/')

            if parents == ['root']:
                try:
                    val = nest_struct['root']
                    val.append(name)
                    nest_struct['root'] = val
                except:
                    nest_struct['root'] = [name]


            for j in range(len(parents)-1):
                nest = parents[j]
                # Updating parent entries
                try:
                    val = nest_struct[nest]
                    if parents[j+1] not in val:
                        val.append(parents[j+1])
                        nest_struct[nest] = val
                except:
                    nest_struct[nest] = [parents[j+1]]


                # Updating alternative entries
                try:
                    val = nest_struct[parents[-1]]
                    val.append(name)
                    nest_struct[parents[-1]] = val
                except:
                    nest_struct[parents[-1]] = [name]

        if len(values) == 0:
            values = None

        for i in nest_struct:
            if i not in alts:
                alts.append(i)
            for j in nest_struct[i]:
                if j not in alts:
                    alts.append(j)

        for i in alts:
            if i not in spec_build_ind.keys() and i <> 'root':
                spec = self.create_spec(i)
                spec_build_ind[i] = spec

        spec_dict = copy.deepcopy(nest_struct)

        for i in nest_struct:
            vals = spec_dict.pop(i)
            vals_spec = []
            for j in vals:
                vals_spec.append(spec_build_ind[j])
            if i <> 'root':
                i = spec_build_ind[i]
            spec_dict[i] = vals_spec



        branchIterator = model_element.getiterator('Branch')
        for i in branchIterator:
            name = i.get('name')
            logsum = float(i.get('coeff'))

            for j in spec_dict.keys():
                if j <> 'root':
                    if j.choices == [name.lower()]:
                        j.logsumparameter = logsum



        for i in spec_dict:
            if i <> 'root':
                #print i.choices
                #print i.logsumparameter
                pass
            else:
                #print i
                pass
            for j in spec_dict[i]:
                #print j.choices
                pass


        #print nest_struct
        #print alts
        #print spec_build_ind

        #print '-----', spec_dict

        specification = NestedSpecification(spec_dict)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = NestedLogitChoiceModel(specification)
        model_type = 'choice'
        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, values=values, seed=seed,
                                filter_type=filter_type,
                                run_filter_type=run_filter_type)


        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list


    def create_spec(self, name):
        choices = name
        coefficients = {'ONE':0}

        spec = NestedChoiceSpecification([choices], [coefficients])
        return spec



    def create_ordered_choice_object(self, model_element, projectSeed=0):
        #model type
        model_type = model_element.get('type')
        seed = self.process_seed(model_element) + projectSeed
        #variable_list_required for running the model
        variable_list = []

        # dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        # alternatives
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        values = []
        coefficients_list = []
        threshold_list = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)
            value = i.get('value')
            if value is not None:
                values.append(float(value))
            threshold = i.get('threshold')
            if threshold is not None:
                threshold_list.append(float(threshold))
        coeff_dict, vars_list = self.return_coeff_vars(model_element)
        coefficients_list = coefficients_list + coeff_dict
        variable_list = vars_list

        if len(values) == 0:
            values = None

        #print dep_varname, model_type

        # logit specification object
        if model_type == 'Logit':
            #print coefficients_list
            specification = OLSpecification(choice, coefficients_list, threshold_list,
                                            distribution=model_type.lower())
        else:
            specification = OLSpecification(choice, coefficients_list, threshold_list,
                                            distribution=model_type.lower())

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = OrderedModel(specification)
        model_type = 'choice'                   #Type of Model
        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, values=values, seed=seed,
                                filter_type=filter_type,
                                run_filter_type=run_filter_type) #Model Object

        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list
        #print self.component_variable_list
        #print 'HERE IS OREDERED LOGIT'
        #raw_input()


    def create_probability_object(self, model_element, projectSeed=0):
        #variable_list_required for running the model
        variable_list = []
        seed = self.process_seed(model_element) + projectSeed
        # dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        # alternatives
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        values = []
        coefficients_list = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)
            value = i.get('value')
            if value is not None:
                values.append(float(value))
            coeff_dict, vars_list = self.return_coeff_vars(i)
            coefficients_list = coefficients_list + coeff_dict
            variable_list = variable_list + vars_list
        if len(values) == 0:
            values = None
        #print coefficients_list
        #print dep_varname

        # logit specification object
        specification = Specification(choice, coefficients_list)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = ProbabilityModel(specification)
        model_type = 'choice'                   #Type of Model
        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, values=values, seed=seed,
                                filter_type=filter_type,
                                run_filter_type=run_filter_type) #Model Object

        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list

    def create_reconcile_schedules_object(self, model_element, projectSeed=0):
        #variable_list_required for running the model

        variable_list = []

        seed = self.process_seed(model_element) + projectSeed

        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Run Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None


        activity_attribs_element = model_element.find('ActivityAttributes')

        activityAttribsSpec = self.return_activity_attribs(activity_attribs_element)


        specification = ReconcileSchedulesSpecification(activityAttribsSpec)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = ReconcileSchedules(specification)

        model_type = 'consistency'

        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)

        self.model_list.append(model_object)

        self.component_variable_list = self.component_variable_list + variable_list

    def create_clean_fixed_activity_schedule(self, model_element, projectSeed=0):
        #variable_list_required for running the model

        variable_list = []

        seed = self.process_seed(model_element) + projectSeed

        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Run Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None


        activity_attribs_element = model_element.find('ActivityAttributes')
        activityAttribsSpec = self.return_activity_attribs(activity_attribs_element)

        dailystatus_attribs_element = model_element.find('DailyStatus')
        dailyStatusAttribsSpec = self.return_daily_status_attribs(dailystatus_attribs_element)

        dependency_attribs_element = model_element.find('Dependency')
        dependencyAttribsSpec = self.return_dependency_attribs(dependency_attribs_element)



        specification = HouseholdSpecification(activityAttribsSpec,
                                               dailyStatusAttribsSpec,
                                               dependencyAttribsSpec)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = CleanFixedActivitySchedule(specification)

        model_type = 'consistency'

        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)

        self.model_list.append(model_object)

        self.component_variable_list = self.component_variable_list + variable_list


    def create_clean_aggregate_activity_schedule(self, model_element, projectSeed=0):
        #variable_list_required for running the model

        variable_list = []

        seed = self.process_seed(model_element) + projectSeed

        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Run Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None


        activity_attribs_element = model_element.find('ActivityAttributes')
        activityAttribsSpec = self.return_activity_attribs(activity_attribs_element)

        dailystatus_attribs_element = model_element.find('DailyStatus')
        dailyStatusAttribsSpec = self.return_daily_status_attribs(dailystatus_attribs_element)

        dependency_attribs_element = model_element.find('Dependency')
        dependencyAttribsSpec = self.return_dependency_attribs(dependency_attribs_element)



        specification = HouseholdSpecification(activityAttribsSpec,
                                               dailyStatusAttribsSpec,
                                               dependencyAttribsSpec)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = CleanAggregateActivitySchedule(specification)

        model_type = 'consistency'

        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)

        self.model_list.append(model_object)

        self.component_variable_list = self.component_variable_list + variable_list


    def create_child_dependency_allocation_object(self, model_element, terminal=False, projectSeed=0):
        #variable_list_required for running the model

        variable_list = []

        model_type = model_element.get('type')

        if model_type == None:
            model_type == "Allocation"
        else:
            model_type == 'Processing'

        seed = self.process_seed(model_element) + projectSeed

        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Run Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None


        activity_attribs_element = model_element.find('ActivityAttributes')
        activityAttribsSpec = self.return_activity_attribs(activity_attribs_element)

        dailystatus_attribs_element = model_element.find('DailyStatus')
        dailyStatusAttribsSpec = self.return_daily_status_attribs(dailystatus_attribs_element)

        dependency_attribs_element = model_element.find('Dependency')
        dependencyAttribsSpec = self.return_dependency_attribs(dependency_attribs_element)



        specification = HouseholdSpecification(activityAttribsSpec,
                                               dailyStatusAttribsSpec,
                                               dependencyAttribsSpec,
                                               terminalEpisodesAllocation=terminal,
                                               childDepProcessingType=model_type)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = ChildDependencyProcessing(specification)

        model_type = 'consistency'

        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)

        self.model_list.append(model_object)

        self.component_variable_list = self.component_variable_list + variable_list


    def create_evolution_post_process_object(self, model_element, projectSeed):
        variable_list = []

        seed = self.process_seed(model_element) + projectSeed

        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Run Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        agentType = model_element.get('type')


        id_element = model_element.find('Id')
        idSpec = self.return_id_spec(id_element)

        hhld_attribs_element = model_element.find('HouseholdAttributes')
        hhldAttribsSpec = self.return_hhld_attribs(hhld_attribs_element)

        person_attribs_element = model_element.find('PersonAttributes')
        personAttribsSpec = self.return_person_attribs(person_attribs_element)

        evolution_attribs_element = model_element.find('EvolutionAttributes')
        evolutionAttribsSpec = self.return_evolution_attribs(evolution_attribs_element)

        specification = HouseholdEvolutionSpecification(idSpec, agentType,
                                                        hhldAttribsSpec,
                                                        personAttribsSpec,
                                                        evolutionAttribsSpec)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = PopulationEvolutionProcessing(specification)

        model_type = 'consistency'

        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)

        self.model_list.append(model_object)

        self.component_variable_list = self.component_variable_list + variable_list

    def create_migration_object(self, model_element, projectSeed, migrationType, analysisInterval=None):
        variable_list = []

        seed = self.process_seed(model_element) + projectSeed

        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Run Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        agentType = model_element.get('type')

        id_element = model_element.find('Id')
        idSpec = self.return_id_spec(id_element)

        hhld_attribs_element = model_element.find('HouseholdAttributes')
        hhldAttribsSpec = self.return_hhld_attribs(hhld_attribs_element)

        person_attribs_element = model_element.find('PersonAttributes')
        personAttribsSpec = self.return_person_attribs(person_attribs_element)

        householdIdSeries_element = model_element.find('HHldIDSeries')
        if householdIdSeries_element is not None:
            householdIdSeries_val = householdIdSeries_element.get('value')

            householdIdSeries = float(householdIdSeries_val)*analysisInterval

        else:
            householdIdSeries = None
        popgenConfig = model_element.find('ProjectConfig')

        specification = PopGenModelSpecification(idSpec,
                                                 hhldAttribsSpec,
                                                 personAttribsSpec,
                                                 popgenConfig,
                                                 householdIdSeries)

        print '\t - ', householdIdSeries
        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        if migrationType == 'Emigration':
            model = Emigration(specification)
        elif migrationType == 'Immigration':
            model = Immigration(specification)

        model_type = 'consistency'

        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)



        self.model_list.append(model_object)

        self.component_variable_list = self.component_variable_list + variable_list


    def create_unique_records_object(self, model_element, projectSeed):
        variable_list = []

        seed = self.process_seed(model_element) + projectSeed

        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Run Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None


        unique_records_element = model_element.find('Variable')
        uniqueRecordsVarNameParsed = self.return_table_var(unique_records_element)

        variable_list.append(uniqueRecordsVarNameParsed)

        specification = UniqueRecordsSpecification(uniqueRecordsVarNameParsed[1])

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = UniqueRecordsProcessing(specification)

        model_type = 'consistency'

        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)



        self.model_list.append(model_object)

        self.component_variable_list = self.component_variable_list + variable_list


    def create_persons_arrived_processing_object(self, model_element, projectSeed):
        variable_list = []

        seed = self.process_seed(model_element) + projectSeed

        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Run Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        id_element = model_element.find('Id')
        idSpec = self.return_id_spec(id_element)


        pers_arrived_attribs_element = model_element.find('PersonsArrivedAttributes')
        persArrivedAttribSpec = self.return_arrived_pers_attribs(pers_arrived_attribs_element)

        specification = PersonsArrivedSpecification(idSpec,
                                                  persArrivedAttribSpec)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = PersonsArrivedProcessing(specification)

        model_type = 'consistency'

        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)



        self.model_list.append(model_object)

        self.component_variable_list = self.component_variable_list + variable_list





    def create_trip_occupant_processing_object(self, model_element, projectSeed):
        variable_list = []

        seed = self.process_seed(model_element) + projectSeed

        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Run Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        id_element = model_element.find('Id')
        idSpec = self.return_id_spec(id_element)

        trip_dep_pers_attribs_element = model_element.find('TripDependentPersonAttributes')
        tripDepAttribSpec = self.return_dep_pers_attribs(trip_dep_pers_attribs_element)

        specification = TripOccupantSpecification(idSpec,
                                                  tripDepAttribSpec)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = TripOccupantProcessing(specification)

        model_type = 'consistency'

        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)



        self.model_list.append(model_object)

        self.component_variable_list = self.component_variable_list + variable_list


    def create_schedule_adjustment_object(self, model_element):
        #variable_list_required for running the model

        variable_list = []

        seed = self.process_seed(model_element)

        model_type = model_element.get('type')

        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Run Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        activity_attribs_element = model_element.find('ActivityAttributes')
        activityAttribsSpec = self.return_activity_attribs(activity_attribs_element)

        dailystatus_attribs_element = model_element.find('DailyStatus')
        dailyStatusAttribsSpec = self.return_daily_status_attribs(dailystatus_attribs_element)

        dependency_attribs_element = model_element.find('Dependency')
        dependencyAttribsSpec = self.return_dependency_attribs(dependency_attribs_element)


        arrival_info_element = model_element.find('ArrivalTime')
        if arrival_info_element is not None:
            arrivalInfoAttribsSpec = self.return_arrival_info_attribs(arrival_info_element)
        else:
            arrivalInfoAttribsSpec = None

        occupancy_info_element = model_element.find('OccupancyInvalid')
        if occupancy_info_element is not None:
            occupancyInfoAttribsSpec = self.return_occupancy_info_attribs(occupancy_info_element)
        else:
            occupancyInfoAttribsSpec = None

        specification = HouseholdSpecification(activityAttribsSpec,
                                               dailyStatusAttribs=dailyStatusAttribsSpec,
                                               dependencyAttribs=dependencyAttribsSpec,
                                               arrivalInfoAttribs=arrivalInfoAttribsSpec,
                                               occupancyInfoAttribs=occupancyInfoAttribsSpec)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = AdjustSchedules(specification)

        model_type = 'consistency'

        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)

        self.model_list.append(model_object)

        self.component_variable_list = self.component_variable_list + variable_list




    def create_column_operations_object(self, model_element, projectSeed=0):
        variable_list = []

        seed = self.process_seed(model_element) + projectSeed

        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Run Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        #print dep_varname, '----variable Name -----'
        choice = [dep_varname]

        # Creating the coefficients input for the regression model
        coeff_dict, vars_list = self.return_coeff_vars(model_element)
        coefficients = coeff_dict

        variable_list = variable_list + vars_list

        #print choice, coefficients
        # specification object
        scalarCalcType = model_element.get('type')
        specification = ColumnOperationsSpecification(choice, coefficients,
                                                       scalarCalcType)

        model = ColumnOperationsModel(specification)



        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model_type = 'create_scalar'
        model_object = SubModel(model, model_type, dep_varname, dataFilter,
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)

        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list


    def return_arrived_pers_attribs(self, trip_arrived_pers_attribs_element):
        variable_list = []

        trpDepPersIdName_element = trip_arrived_pers_attribs_element.find('TripDependentPersonIdName')
        trpDepPersIdNameParsed = self.return_table_var(trpDepPersIdName_element)
        variable_list.append(trpDepPersIdNameParsed)


        tripCountName_element = trip_arrived_pers_attribs_element.find('TripCountName')
        tripCountNameParsed = self.return_table_var(tripCountName_element)
        variable_list.append(tripCountNameParsed)

        endTripCountName_element = trip_arrived_pers_attribs_element.find('EndTripCountName')
        if endTripCountName_element is not None:
            endTripCountNameParsed = self.return_table_var(endTripCountName_element)
            variable_list.append(endTripCountNameParsed)
        else:
            endTripCountNameParsed = (None, None)


        actDepPersIdName_element = trip_arrived_pers_attribs_element.find('ActDependentPersonIdName')
        actDepPersIdNameParsed = self.return_table_var(actDepPersIdName_element)
        variable_list.append(actDepPersIdNameParsed)


        personsArrivedSpec = PersonsArrivedAttributes(trpDepPersIdNameParsed[1],
                                                      tripCountNameParsed[1],
                                                      endTripCountNameParsed[1],
                                                      actDepPersIdNameParsed[1])

        self.component_variable_list = self.component_variable_list + variable_list

        return personsArrivedSpec


    def return_dep_pers_attribs(self, trip_dep_pers_attribs_element):
        variable_list = []

        tripPurpFrom_element = trip_dep_pers_attribs_element.find('TripPurposeFrom')
        tripPurpFromParsed = self.return_table_var(tripPurpFrom_element)
        variable_list.append(tripPurpFromParsed)

        trpDepPersIdName_element = trip_dep_pers_attribs_element.find('TripDependentPersonIdName')
        trpDepPersIdNameParsed = self.return_table_var(trpDepPersIdName_element)
        variable_list.append(trpDepPersIdNameParsed)


        lastTrpActDepPersIdName_element = trip_dep_pers_attribs_element.find('LastTripDependentPersonIdName')
        lastTrpActDepPersIdNameParsed = self.return_table_var(lastTrpActDepPersIdName_element)
        variable_list.append(lastTrpActDepPersIdNameParsed)


        stActDepPersIdName_element = trip_dep_pers_attribs_element.find('StActDependentPersonIdName')
        stActDepPersIdNameParsed = self.return_table_var(stActDepPersIdName_element)
        variable_list.append(stActDepPersIdNameParsed)


        enActDepPersIdName_element = trip_dep_pers_attribs_element.find('EnActDependentPersonIdName')
        enActDepPersIdNameParsed = self.return_table_var(enActDepPersIdName_element)
        variable_list.append(enActDepPersIdNameParsed)

        stActTripCountName_element = trip_dep_pers_attribs_element.find('StActTripCountName')
        stActTripCountNameParsed = self.return_table_var(stActTripCountName_element)
        variable_list.append(stActTripCountNameParsed)


        enActTripCountName_element = trip_dep_pers_attribs_element.find('EnActTripCountName')
        enActTripCountNameParsed = self.return_table_var(enActTripCountName_element)
        variable_list.append(enActTripCountNameParsed)

        tripCountName_element = trip_dep_pers_attribs_element.find('TripCountName')
        tripCountNameParsed = self.return_table_var(tripCountName_element)
        variable_list.append(tripCountNameParsed)

        lastTripCountName_element = trip_dep_pers_attribs_element.find('LastTripCountName')
        lastTripCountNameParsed = self.return_table_var(lastTripCountName_element)
        variable_list.append(lastTripCountNameParsed)


        persOnNetworkName_element = trip_dep_pers_attribs_element.find('PersonOnNetwork')
        if persOnNetworkName_element is not None:
            persOnNetworkNameParsed = self.return_table_var(persOnNetworkName_element)
            variable_list.append(persOnNetworkNameParsed)
        else:
            persOnNetworkNameParsed = (None,None)

        tripDepAttribSpec = TripDependentPersonAttributes(tripPurpFromParsed[1],
                                                          trpDepPersIdNameParsed[1],
                                                          lastTrpActDepPersIdNameParsed[1],
                                                          stActDepPersIdNameParsed[1],
                                                          enActDepPersIdNameParsed[1],
                                                          persOnNetworkNameParsed[1],
                                                          tripCountNameParsed[1],
                                                          lastTripCountNameParsed[1],
                                                          stActTripCountNameParsed[1],
                                                          enActTripCountNameParsed[1])


        self.component_variable_list = self.component_variable_list + variable_list

        return tripDepAttribSpec


    def return_daily_status_attribs(self, dailystatus_attribs_element):
        variable_list = []

        dailySchStatus_element = dailystatus_attribs_element.find('DailySchoolStatus')
        dailySchStatusParsed = self.return_table_var(dailySchStatus_element)
        variable_list.append(dailySchStatusParsed)

        dailyWrkStatus_element = dailystatus_attribs_element.find('DailyWorkStatus')
        dailyWrkStatusParsed = self.return_table_var(dailyWrkStatus_element)
        variable_list.append(dailyWrkStatusParsed)


        dailyStatusSpec = DailyStatusAttribsSpecification(dailyWrkStatusParsed[1],
                                                          dailySchStatusParsed[1])

        self.component_variable_list = self.component_variable_list + variable_list

        return dailyStatusSpec

    def return_arrival_info_attribs(self, arrival_info_element):
        variable_list = []


        dependentperson_element = arrival_info_element.find('DependentPersonId')
        dependentpersonParsed = self.return_table_var(dependentperson_element)
        variable_list.append(dependentpersonParsed)


        actualArrival_element = arrival_info_element.find('Actual')
        actualArrivalParsed = self.return_table_var(actualArrival_element)
        variable_list.append(actualArrivalParsed)

        expectedArrival_element = arrival_info_element.find('Expected')
        expectedArrivalParsed = self.return_table_var(expectedArrival_element)
        variable_list.append(expectedArrivalParsed)

        arrivalInfoSpec = ArrivalInfoSpecification(dependentpersonParsed[1],
                                                   actualArrivalParsed[1],
                                                   expectedArrivalParsed[1])

        self.component_variable_list = self.component_variable_list + variable_list

        return arrivalInfoSpec

    def return_occupancy_info_attribs(self, occupancy_info_element):
        variable_list = []


        tripIndicator_element = occupancy_info_element.find('TripInd')
        tripIndicatorParsed = self.return_table_var(tripIndicator_element)
        variable_list.append(tripIndicatorParsed)

        startTime_element = occupancy_info_element.find('StartTime')
        startTimeParsed = self.return_table_var(startTime_element)
        variable_list.append(startTimeParsed)


        occupancyInfoSpec = OccupancyInfoSpecification(tripIndicatorParsed[1],
                                                       startTimeParsed[1])

        self.component_variable_list = self.component_variable_list + variable_list
        return occupancyInfoSpec


    def return_dependency_attribs(self, dependency_attribs_element):
        variable_list = []

        childDependency_element = dependency_attribs_element.find('ChildDependency')
        childDependencyParsed = self.return_table_var(childDependency_element)
        variable_list.append(childDependencyParsed)


        """
        IN THE FUTURE IF WE WANT TO INCLUDE ELDERLY DEPENDENCY AS WELL
        elderlyDependency_element = dependency_attribs_element.find('ElderlyDependency')
        elderlyDepedencyParsed = self.return_table_var(elderlyDependency_element)
        variable_list.append(elderlyDependencyParsed)
        """

        dependencySpec = DependencyAttribsSpecification(childDependencyParsed[1], elderlyDependencyName=None)

        self.component_variable_list = self.component_variable_list + variable_list

        return dependencySpec



    def return_id_spec(self, id_element):
        variable_list = []

        houseIdName_element = id_element.find('HouseId')
        houseIdParsed = self.return_table_var(houseIdName_element)
        variable_list.append(houseIdParsed)

        personIdName_element = id_element.find('PersonId')
        personIdParsed = self.return_table_var(personIdName_element)
        variable_list.append(personIdParsed)

        idSpec = IdSpecification(houseIdParsed[1], personIdParsed[1])

        self.component_variable_list = self.component_variable_list + variable_list

        return idSpec


    def return_hhld_attribs(self, hhld_attribs_element):
        variable_list = []

        bldgszName_element = hhld_attribs_element.find('BuildingSize')
        bldgszParsed = self.return_table_var(bldgszName_element)
        variable_list.append(bldgszParsed)

        typeName_element = hhld_attribs_element.find('Type')
        typeParsed = self.return_table_var(typeName_element)
        variable_list.append(typeParsed)

        hincName_element = hhld_attribs_element.find('HhldIncome')
        hincParsed = self.return_table_var(hincName_element)
        variable_list.append(hincParsed)

        numChildren_element = hhld_attribs_element.find('NumChildren')
        numChildrenParsed = self.return_table_var(numChildren_element)
        variable_list.append(numChildrenParsed)

        personsName_element = hhld_attribs_element.find('Persons')
        personsParsed = self.return_table_var(personsName_element)
        variable_list.append(personsParsed)

        unittype_element = hhld_attribs_element.find('UnitType')
        unittypeParsed = self.return_table_var(unittype_element)
        variable_list.append(unittypeParsed)

        vehicleCount_element = hhld_attribs_element.find('VehicleCount')
        vehicleCountParsed = self.return_table_var(vehicleCount_element)
        variable_list.append(vehicleCountParsed)

        workersInFamily_element = hhld_attribs_element.find('WorkersInFamily')
        workersInFamilyParsed = self.return_table_var(workersInFamily_element)
        variable_list.append(workersInFamilyParsed)

        yearMoved_element = hhld_attribs_element.find('YearMoved')
        yearMovedParsed = self.return_table_var(yearMoved_element)
        variable_list.append(yearMovedParsed)


        hhldAttribsSpec = HouseholdAttributesSpecification(bldgszParsed[1],
                                                           typeParsed[1],
                                                           hincParsed[1],
                                                           numChildrenParsed[1],
                                                           personsParsed[1],
                                                           unittypeParsed[1],
                                                           vehicleCountParsed[1],
                                                           workersInFamilyParsed[1],
                                                           yearMovedParsed[1])


        self.component_variable_list = self.component_variable_list + variable_list

        return hhldAttribsSpec

    def return_person_attribs(self, person_attribs_element):
        variable_list = []

        ageName_element = person_attribs_element.find('Age')
        ageParsed = self.return_table_var(ageName_element)
        variable_list.append(ageParsed)

        clwkrName_element = person_attribs_element.find('ClassWorker')
        clwkrParsed = self.return_table_var(clwkrName_element)
        variable_list.append(clwkrParsed)

        educationName_element = person_attribs_element.find('Education')
        educationParsed = self.return_table_var(educationName_element)
        variable_list.append(educationParsed)

        enrollmentName_element = person_attribs_element.find('Enrollment')
        enrollmentParsed = self.return_table_var(enrollmentName_element)
        variable_list.append(enrollmentParsed)

        employmentName_element = person_attribs_element.find('Employment')
        employmentParsed = self.return_table_var(employmentName_element)
        variable_list.append(employmentParsed)

        industryName_element = person_attribs_element.find('IndustryCode')
        industryParsed = self.return_table_var(industryName_element)
        variable_list.append(industryParsed)

        occupationName_element = person_attribs_element.find('Occupation')
        occupationParsed = self.return_table_var(occupationName_element)
        variable_list.append(occupationParsed)

        raceName_element = person_attribs_element.find('Race')
        raceParsed = self.return_table_var(raceName_element)
        variable_list.append(raceParsed)

        relateName_element = person_attribs_element.find('Relate')
        relateParsed = self.return_table_var(relateName_element)
        variable_list.append(relateParsed)

        sexName_element = person_attribs_element.find('Sex')
        sexParsed = self.return_table_var(sexName_element)
        variable_list.append(sexParsed)

        maritalStatusName_element = person_attribs_element.find('MaritalStatus')
        maritalStatusParsed = self.return_table_var(maritalStatusName_element)
        variable_list.append(maritalStatusParsed)

        hoursWorkedName_element = person_attribs_element.find('HoursWorked')
        hoursWorkedParsed = self.return_table_var(hoursWorkedName_element)
        variable_list.append(hoursWorkedParsed)

        gradeName_element = person_attribs_element.find('Grade')
        gradeParsed = self.return_table_var(gradeName_element)
        variable_list.append(gradeParsed)

        hispanicIndicatorName_element = person_attribs_element.find('HispanicIndicator')
        hispanicIndicatorParsed = self.return_table_var(hispanicIndicatorName_element)
        variable_list.append(hispanicIndicatorParsed)

        personAttribsSpec = PersonAttributesSpecification(ageParsed[1],
                                                          clwkrParsed[1],
                                                          educationParsed[1],
                                                          enrollmentParsed[1],
                                                          employmentParsed[1],
                                                          industryParsed[1],
                                                          occupationParsed[1],
                                                          raceParsed[1],
                                                          relateParsed[1],
                                                          sexParsed[1],
                                                          maritalStatusParsed[1],
                                                          hoursWorkedParsed[1],
                                                          gradeParsed[1],
                                                          hispanicIndicatorParsed[1])


        self.component_variable_list = self.component_variable_list + variable_list

        return personAttribsSpec

    def return_evolution_attribs(self, evolution_attribs_element):
        variable_list = []

        mortalityName_element = evolution_attribs_element.find('MortalityStatus')
        mortalityParsed = self.return_table_var(mortalityName_element)
        variable_list.append(mortalityParsed)

        birthName_element = evolution_attribs_element.find('BirthStatus')
        birthParsed = self.return_table_var(birthName_element)
        variable_list.append(birthParsed)

        agingName_element = evolution_attribs_element.find('AgeStatus')
        agingParsed = self.return_table_var(agingName_element)
        variable_list.append(agingParsed)

        enrollmentName_element = evolution_attribs_element.find('Enrollment')
        enrollmentParsed = self.return_table_var(enrollmentName_element)
        variable_list.append(enrollmentParsed)

        gradeName_element = evolution_attribs_element.find('Grade')
        gradeParsed = self.return_table_var(gradeName_element)
        variable_list.append(gradeParsed)

        educationName_element = evolution_attribs_element.find('Education')
        educationParsed = self.return_table_var(educationName_element)
        variable_list.append(educationParsed)

        educationInYearsName_element = evolution_attribs_element.find('EducationInYears')
        educationInYearsParsed = self.return_table_var(educationInYearsName_element)
        variable_list.append(educationInYearsParsed)

        residenceDecisionName_element = evolution_attribs_element.find('ResidenceDecision')
        residenceDecisionParsed = self.return_table_var(residenceDecisionName_element)
        variable_list.append(residenceDecisionParsed)

        laborParticipationName_element = evolution_attribs_element.find('LaborParticipation')
        laborParticipationParsed = self.return_table_var(laborParticipationName_element)
        variable_list.append(laborParticipationParsed)

        occupationName_element = evolution_attribs_element.find('Occupation')
        occupationParsed = self.return_table_var(occupationName_element)
        variable_list.append(occupationParsed)

        incomeName_element = evolution_attribs_element.find('Income')
        incomeParsed = self.return_table_var(incomeName_element)
        variable_list.append(incomeParsed)

        marriageDecisionName_element = evolution_attribs_element.find('MarriageDecision')
        marriageDecisionParsed = self.return_table_var(marriageDecisionName_element)
        variable_list.append(marriageDecisionParsed)

        divorceDecisionName_element = evolution_attribs_element.find('DivorceDecision')
        divorceDecisionParsed = self.return_table_var(divorceDecisionName_element)
        variable_list.append(divorceDecisionParsed)

        evolutionAttribsSpec = EvolutionAttributesSpecification(mortalityParsed[1],
                                                                birthParsed[1],
                                                                agingParsed[1],
                                                                enrollmentParsed[1],
                                                                gradeParsed[1],
                                                                educationParsed[1],
                                                                educationInYearsParsed[1],
                                                                residenceDecisionParsed[1],
                                                                laborParticipationParsed[1],
                                                                occupationParsed[1],
                                                                incomeParsed[1],
                                                                marriageDecisionParsed[1],
                                                                divorceDecisionParsed[1])


        self.component_variable_list = self.component_variable_list + variable_list

        return evolutionAttribsSpec



    def return_activity_attribs(self, activity_attribs_element):
        variable_list = []

        householdIdName_element = activity_attribs_element.find('HouseholdIdName')
        householdIdParsed = self.return_table_var(householdIdName_element)
        variable_list.append(householdIdParsed)

        personIdName_element = activity_attribs_element.find('PersonIdName')
        personIdParsed = self.return_table_var(personIdName_element)
        variable_list.append(personIdParsed)

        scheduleIdName_element = activity_attribs_element.find('ScheduleIdName')
        scheduleIdParsed = self.return_table_var(scheduleIdName_element)
        variable_list.append(scheduleIdParsed)

        activityTypeName_element = activity_attribs_element.find('ActivityTypeName')
        activityTypeParsed = self.return_table_var(activityTypeName_element)
        variable_list.append(activityTypeParsed)

        startTimeName_element = activity_attribs_element.find('StartTimeName')
        startTimeParsed = self.return_table_var(startTimeName_element)
        variable_list.append(startTimeParsed)

        endTimeName_element = activity_attribs_element.find('EndTimeName')
        endTimeParsed = self.return_table_var(endTimeName_element)
        variable_list.append(endTimeParsed)

        locationIdName_element = activity_attribs_element.find('LocationIdName')
        locationIdParsed = self.return_table_var(locationIdName_element)
        variable_list.append(locationIdParsed)

        durationName_element = activity_attribs_element.find('DurationName')
        durationParsed = self.return_table_var(durationName_element)
        variable_list.append(durationParsed)


        dependentPersonName_element = activity_attribs_element.find('DependentPersonName')
        dependentPersonParsed = self.return_table_var(dependentPersonName_element)
        variable_list.append(dependentPersonParsed)


        tripCountName_element = activity_attribs_element.find('TripCountName')
        tripCountParsed = self.return_table_var(tripCountName_element)
        variable_list.append(tripCountParsed)

        actAttribsSpec = ActivityAttribsSpecification(householdIdParsed[1],
                                                      personIdParsed[1],
                                                      scheduleIdParsed[1],
                                                      activityTypeParsed[1],
                                                      startTimeParsed[1],
                                                      endTimeParsed[1],
                                                      locationIdParsed[1],
                                                      durationParsed[1],
                                                      dependentPersonParsed[1],
                                                      tripCountParsed[1])

        self.component_variable_list = self.component_variable_list + variable_list

        return actAttribsSpec





    def return_table_var(self, var_element):
        return var_element.get('table'), var_element.get('var')

    def return_coeff_vars(self, element, alternativeSet=None):
        variableIterator = element.getiterator('Variable')
        vars_list = []
        coeff_ret = []
        inverse_list = []

        for i in variableIterator:
            dep_var, inverse_dict = self.check_for_interaction_terms(i, alternativeSet)
            if dep_var is not None:
                #print '\t\tINTERACTION TERM', dep_var
                for j in dep_var:
                    coeff_dict = {}
                    coeff = i.get('coeff')
                    #print coeff
                    #coeff_dict[j] = float(coeff)
                    if len(coeff_ret) < len(dep_var):
                        coeff_dict[j] = float(coeff)
                        coeff_ret.append(coeff_dict)
                    else:
                        coeff_ret[dep_var.index(j)][j] = float(coeff)

                #print coeff_ret, 'new repeated INTERACTION TERMSSSSSSSSSSSSSSSSSSSSSSSSS'
                #print 'inverse dict', inverse_dict
            else:
                #print 'NOT AN INTERACTION TERM'
                coeff_dict = {}
                vars_list.append(self.return_table_var(i))
                varname = i.get('var')
                coeff = i.get('coeff')
                if len(coeff_ret) < 1:
                    coeff_dict[varname] = float(coeff)
                    coeff_ret.append(coeff_dict)
                else:
                    coeff_ret[0][varname] = float(coeff)
                #print coeff_ret
        #print vars_list, 'sent back', coeff_ret
        #print 'coeff_re', coeff_ret
        return coeff_ret, vars_list

    def check_for_interaction_terms(self, var_element, alternativeSet):
        variable_list = []
        coeff_dict = {}
        inverse_dict = {}
        dep_varname = ''

        #print 'alternativeSet', alternativeSet
        #print var_element.get('var'), var_element.get('table')

        interaction_element = var_element.get('interaction')
        rep_var = var_element.get('repeat')

        if var_element.get('interaction') is None and rep_var is None:
            return None, None
        else:
            rep_var = var_element.get('repeat')
            if rep_var is not None:
                rep_var_list = re.split('[,]', rep_var)
            else:
                rep_var_list = []

            #print '\tREPEAT VARIABLE LIST -->', rep_var_list

            #var_element.get('interaction')
            varnames = re.split('[,]', var_element.get('var'))
            #print 'varnames', varnames
            tablenames = re.split('[,]', var_element.get('table'))
            #print 'tablenames', tablenames

            inverseElement = var_element.get('inverse')
            if inverseElement is not None:
                inverseFlag = re.split('[,]', var_element.get('inverse'))
            else:
                inverseFlag = []

            rep_var_table_list = []
            for i in rep_var_list:
                #find and remove the repeate variable from varnames
                var_ind = varnames.index(i)
                varnames.pop(var_ind)

                #find the tablenames for the ones that are to be repeated
                rep_var_table_list.append(tablenames.pop(var_ind))
            #print '\tREPEAT TABLE LIST', rep_var_table_list

            for i in range(len(varnames)):
                variable_list.append((tablenames[i], varnames[i]))

            varNamesNew = []
            if len(inverseFlag) > 0:
                for var in varnames:
                    ind = varnames.index(var)
                    if inverseFlag[ind] == 'True':
                        varNamesNew.append('inv_%s' %var)
                    else:
                        varNamesNew.append(var)

                varnames = varNamesNew
                #raw_input('inverse ... should it happen here ... ')



            if alternativeSet is None:
                dep_var = [tuple(varnames)]
                inverse_dict[tuple(varnames)] = inverseFlag

                self.component_variable_list = self.component_variable_list + variable_list
            else:
                dep_var = []
                for j in range(alternativeSet):
                    for k in range(len(rep_var_list)):
                        variable_list.append(('temp', rep_var_list[k]+str(j+1)))
                        varnamesCp = copy.deepcopy(varnames)
                        varnamesCp.append(rep_var_list[k]+str(j+1))

                        if len(varnamesCp) == 1:
                            dep_var.append(varnamesCp[0])
                        else:
                            dep_var.append(tuple(varnamesCp))

                    self.component_variable_list = self.component_variable_list + variable_list

            return dep_var, inverse_dict





    def return_spatial_query(self, spatial_query_element):

        # Parsing attributes of the spatial query
        table = spatial_query_element.get('table')
        skimField = spatial_query_element.get('skim_var')
        asField = spatial_query_element.get('as_var')
        distField = spatial_query_element.get('dist_var')
        originField = spatial_query_element.get('origin_var')
        destinationField = spatial_query_element.get('destination_var')
        sampleField = spatial_query_element.get('sample_var')

        countChoices = spatial_query_element.get('count')
        if countChoices is not None:
            countChoices = int(countChoices)
        thresholdTimeConstraint = spatial_query_element.get('threshold')
        seed = spatial_query_element.get('seed')
        if seed is not None:
            seed = int(seed)
        else:
            seed = 1

        if thresholdTimeConstraint is not None:
            thresholdTimeConstraint = int(thresholdTimeConstraint)


        activity_element = spatial_query_element.get('ActivityFilter')
        if activity_element is not None:
            activityTypeFilter = self.return_activity_type_condition(activity_element)
        else:
            activityTypeFilter = None

        startConstraint_element = spatial_query_element.find('Start')
        startConstraint = self.return_spatio_temporal_constraint(startConstraint_element)
        startTableVar = self.return_table_var(startConstraint_element)

        endConstraint_element = spatial_query_element.find('End')
        endConstraint = self.return_spatio_temporal_constraint(endConstraint_element)
        endTableVar = self.return_table_var(endConstraint_element)


        votdConstraint_element = spatial_query_element.find('ValueofTimePerDistance')
        votdTableVar = self.return_table_var(votdConstraint_element)
        votdField = votdTableVar[1]

        self.component_variable_list = self.component_variable_list + [votdTableVar]

        locationVariables = []
        locationInfoTable = None
        locationIdVar = None
        locationInformationElement = spatial_query_element.find('ExtractLocationInformation')
        if locationInformationElement is not None:
            locationInfoTable = locationInformationElement.get('table')
            locationIdVar = locationInformationElement.get('location_var')
            locationVarsIterator = locationInformationElement.getiterator('LocationVariable')

            for var in locationVarsIterator:
                varname = var.get('var')
                locationVariables.append(varname)


        beforeModel = spatial_query_element.get('before_model')
        afterModel = spatial_query_element.get('after_model')


        locationFilterList = []
        locationFilterType = "or"


        if locationInformationElement is not None:
            locationFilterList = self.return_filter_condition_list(locationInformationElement)
            locationFilterTypeElement = locationInformationElement.find('FilterSet')
            if locationFilterTypeElement is not None:
                locationFilterType = locationFilterTypeElement.get('type')

        prismConstraint = PrismConstraints(table, skimField,
                                           originField, destinationField,
                                           startConstraint, endConstraint,
                                           asField,
                                           distField,
                                           votdField,
                                           sampleField, countChoices, activityTypeFilter,
                                           thresholdTimeConstraint, seed,
                                           afterModel, beforeModel,
                                           locationInfoTable,
                                           locationIdVar,
                                           locationVariables,
                                           locationFilterList,
                                           locationFilterType)


        #print prismConstraint
        return prismConstraint

    def return_spatio_temporal_constraint(self, constraint_element):
        table = constraint_element.get('table')
        location_field = constraint_element.get('var')
        time_field = constraint_element.get('time_var')

        constraint = SpatioTemporalConstraint(table, location_field, time_field)
        return constraint


    def return_activity_type_condition(self, model_element):
        # Varies from the filter condition in that no variables
        # are added to the variable list for the component

        filter_element = model_element.find('Filter')

        if filter_element is None:
            return None

        tablename = filter_element.get('table')
        varname = filter_element.get('var')
        variable_list = [(tablename, varname)]

        filterCondition = filter_element.get('condition')
        filterValue = float(filter_element.get('value'))

        dataFilter = DataFilter(varname, filterCondition, filterValue)

        return dataFilter




    def return_filter_condition_list(self, model_element):
        filterIterator = model_element.getiterator("Filter")
        filterList = []
        for i in filterIterator:
            filterCondition = self.return_filter_condition(i)
            filterList.append(filterCondition)
        return filterList

    def return_filter_condition(self, filter_element):

        if filter_element is None:
            return None

        tablename = filter_element.get('table')
        varname = filter_element.get('var')
        variable_list = [(tablename, varname)]

        filterCondition = filter_element.get('condition')
        filterValue = filter_element.get('value')
        if filterValue is not None:
            filterValue = float(filter_element.get('value'))
        else:
            filterTablename = filter_element.get('valuetable')
            filterValue = filter_element.get('valuevar')
            variable_list_val = [(filterTablename, filterValue)]
            self.component_variable_list = (self.component_variable_list +
                                            variable_list_val)
        dataFilter = DataFilter(varname, filterCondition, filterValue)

        self.component_variable_list = (self.component_variable_list +
                                        variable_list)

        #print 'FILTERCONDITION - ', filterCondition

        return dataFilter

    def return_run_until_condition(self, model_element):
        runIterator = model_element.getiterator('RunUntilCondition')
        runList = []

        for i in runIterator:
            runCondition = self.return_filter_condition(i)
            runList.append(runCondition)
        return runList

    def dummy(self):

        if run_until_element is None:
            return None

        tablename_ind = run_until_element.get('table')
        varname_ind = run_until_element.get('var')
        variable_list_ind = [(tablename_ind, varname_ind)]

        runUntilCondition = run_until_element.get('condition')
        filterValue = run_until_element.get('value')
        if filterValue is not None:
            filterValue = float(run_until_element.get('value'))
        else:
            filterTablename = run_until_element.get('valuetable')
            filterValue = run_until_element.get('valuevar')
            variable_list_val = [(filterTablename, filterValue)]
            self.component_variable_list = (self.component_variable_list +
                                            variable_list_val)
        runUntilFilter = DataFilter(varname_ind, runUntilCondition, filterValue)


        """


        tablename_val = run_until_element.get('valuetable')
        varname_val = run_until_element.get('valuevar')
        variable_list_val = [(tablename_val, varname_val)]

        self.component_variable_list = self.component_variable_list +\
            variable_list_ind + variable_list_val

        #print 'RUNUNTILCONDITION - ', runUntilCondition

        runUntilFilter = DataFilter(varname_ind, runUntilCondition, varname_val)
        """
        return runUntilFilter

    def return_component_attribs(self, component_element):
        """
        Returns the variable name, table name, keys for the component.
        """
        name = component_element.get('name')
        readFromTable = component_element.get('read_from_table')
        writeToTable = component_element.get('write_to_table')
        if writeToTable is None:
            writeToTable = readFromTable

        writeToTable2 = component_element.get('write_to_table_2')

        """
        prim_keys = component_element.get('key')
        if prim_keys is not None:
            prim_keys = re.split('[,]', prim_keys)
        index_keys = component_element.get('count_key')
        if index_keys is not None:
            index_keys = re.split('[,]', index_keys)
        """

        #print varname, tablename, [prim_keys, index_keys]
        #return name, readFromTable, writeToTable, [prim_keys, index_keys]
        return name, readFromTable, writeToTable, writeToTable2




if __name__ == '__main__':
    import time
    """
    from numpy import zeros, random
    fileloc = '/home/kkonduri/simtravel/test/config.xml'
    configObject = etree.parse(fileloc)
    conf_parser = ConfigParser(configObject)
    component_list = conf_parser.parse_models()

    colnames = ['one', 'age', 'parttime', 'telcomm', 'empserv', 'commtime', 'popres',
                'numchild', 'numdrv', 'respb', 'autoworkmode', 'gender', 'numadlts',
                'numadltsgender', 'schstat',
                'daystart', 'dayend', 'numjobs', 'workstart1', 'workend1',
                'workstat', 'workloc', 'numadlts', 'timeend',
                'numvehs', 'schdailystatus', 'actdestination', 'actduration']

    cols = len(colnames)
    cols_dep = 15

    ti = time.time()

    proc_time = []
    for i in range(4):
        rows = 10**(i)
        print 'RUN WITH - %d records' %(rows)

        ti = time.time()
        rand_input = random.random_integers(1, 4, (rows,cols - cols_dep))

        data = zeros((rows, cols))

        data[:,:cols-cols_dep] = rand_input
        data = DataArray(data, colnames)

        #print data.data[0,:]


        for i in component_list:
            print '\tCOMPONENT NAME - ', i.component_name
            #print '\t\tVARIABLE LIST FOR COMPONENT - ',i.variable_list
            i.run(data)
        #print i.data.data[:10]
        diff = time.time()-ti
        proc_time.append(diff)
        print '\tTIME ELAPSED USING ARRAY FORMAT - %.2f' %(diff)


    """

    from openamos.core.database_management.database_configuration import DataBaseConfiguration
    from openamos.core.database_management.database_connection import DataBaseConnection
    from openamos.core.database_management.query_browser import QueryBrowser

    ti = time.time()
    # Changes in the configuration file - add protocol,
    # convert string parameters to lower case when parsing, variable names

    protocol = 'postgres'
    user_name = 'postgres'
    password = '1234'
    host_name = '10.206.111.198'
    database_name = 'postgres'

    dbconfig = DataBaseConfiguration(protocol, user_name, password,
                                     host_name, database_name)
    newobject = QueryBrowser(dbconfig)

    # setup a connection
    newobject.dbcon_obj.new_connection()

    newobject.create_mapper_for_all_classes()

    #print type(VEHICLE)

    hhld_class_name = 'households'
    pers_class_name = 'persons'

    query_gen, cols = newobject.select_all_from_table(hhld_class_name)
    query_gen, cols = newobject.fetch_selected_rows(pers_class_name, 'employ', '1')
    #temp_dict = {'households':'household_id, adults, homestaz', 'persons':'employ, workstaz'}
    temp_dict = {'households':['household_id', 'adults', 'homestaz'],
                 'persons':['employ', 'workstaz']}

    query_gen, cols = newobject.select_join(temp_dict, 'household_id', pers_class_name, 'employ', '1')

    ti = time.time()

    print type(query_gen)

    """
    c = 0
    for i in query_gen:
        c = c + 1
        if c> 10:
            break
        print i.household_id

    print 'records read', c





    # create a mapper object
    newobject.create_mapper_for_all_classes()

    # to select all rows from table
    class_name = 'School'
    newobject.select_all_from_table(class_name)

    # to select rows based on a filter
    class_name = 'Office'
    column_name = 'role'
    value = 'se'
    newobject.fetch_selected_rows(class_name, column_name, value)

    # join across tables
    key_column_name = 'role_id'
    temp_dict = {'Person':'first_name, last_name', 'Office':'role, years'}
    match_column_name = 'role_id'
    value='1'
    newobject.select_join(temp_dict, column_name, new_col, value)

    # deleting records
    class_name = 'School'
    newobject.delete_all(class_name)





    # close a connection
    newobject.dbcon_obj.close_connection()

    """
