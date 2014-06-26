from PyQt4.QtCore import *
from PyQt4.QtGui import *
from models import *
from spec_abstract_dialog import *
from mixed_abstract_dialog import *
from project_config_dialog import *
from openamos.gui.file_menu.databaseconfig import *
from openamos.gui.env import *


CAMPAIGN_TYPE, FOLDER_TYPE, CALC_TYPE = range(1001, 1004)


class Model_Manager_Treewidget(QTreeWidget):

    def __init__(self, parent=None):
        super(Model_Manager_Treewidget, self).__init__(parent)
        self.models = Models(parent)
        self.father = parent
        self.setColumnCount(3)
        self.setHeaderLabels(["Model", "Completed", "Skip"])
        self.setColumnWidth(0, 260)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 30)
        self.setMinimumSize(360, 50)

        self.configobject = None
        self.isMove = True
        self.subcomponent = ""

# Define long term models
#
#        long_term_models = QTreeWidgetItem(self)
# long_term_models.setText(0, COMP_LONGTERM)                          #"Long Term Choices")
#
#
#        generate_synthetic_population = QTreeWidgetItem(long_term_models)
# generate_synthetic_population.setText(0, COMPMODEL_SYNTHPOP)        #"Generate Synthetic Population")
#
#        labor_force_participation_model = QTreeWidgetItem(long_term_models)
# labor_force_participation_model.setText(0, COMPMODEL_WORKSTAT)      #"Labor Force Participation Model")
#
#        number_of_jobs = QTreeWidgetItem(long_term_models)
# number_of_jobs.setText(0, COMPMODEL_NUMJOBS)                        #"Identify the number of jobs")
#
#        primary_worker = QTreeWidgetItem(long_term_models)
# primary_worker.setText(0, COMPMODEL_PRIMWORK)                       #"Primary worker in the household")
#
#        school_status = QTreeWidgetItem(long_term_models)
# school_status.setText(0, COMPMODEL_SCHSTAT)                         #"School status of everyone")
#
#        residential_location_choice = QTreeWidgetItem(long_term_models)
# residential_location_choice.setText(0, COMPMODEL_RESLOC)            #"Residential Location Choice")
#
# Define fixed activity location choice generator
#
#        fixed_activity_models = QTreeWidgetItem(long_term_models)
# fixed_activity_models.setText(0, COMP_FIXEDACTLOCATION)     #"Fixed Activity Location Choice Generator")
#
#        workers = QTreeWidgetItem(fixed_activity_models)
#        workers.setText(0, "Workers")
#
#        work_location = QTreeWidgetItem(workers)
# work_location.setText(0, COMPMODEL_WORKLOC)                 #"Identify a primary work location")
#
#        children_adult = QTreeWidgetItem(fixed_activity_models)
#        children_adult.setText(0, "Students")
#
#        school_location_choice1 = QTreeWidgetItem(children_adult)
# school_location_choice1.setText(0, COMPMODEL_SCHLOC1)        #"School location choice")
#        school_location_choice2 = QTreeWidgetItem(children_adult)
#        school_location_choice2.setText(0, COMPMODEL_SCHLOC2)
#
#        children_1 = QTreeWidgetItem(fixed_activity_models)
#        children_1.setText(0, "Preschoolers")
#
#        preschool_location_choice = QTreeWidgetItem(children_1)
# preschool_location_choice.setText(0, COMPMODEL_PRESCHLOC)   #"Preschool location choice"
#
#
#        medium_term_models = QTreeWidgetItem(self)
#        medium_term_models.setText(0, COMP_MEDIUMTERM)
#
# Define Vehicle Ownership Model
#
#        vehicle_ownership_models = QTreeWidgetItem(medium_term_models)
# vehicle_ownership_models.setText(0, COMP_VEHOWN)            #"Vehicle Ownership Model")
#
#        count_vehicles = QTreeWidgetItem(vehicle_ownership_models)
# count_vehicles.setText(0, COMPMODEL_NUMVEHS)                #"Count of Vehicles")
#
#
#        Vehicle_body_fuel_type  = QTreeWidgetItem(vehicle_ownership_models)
# Vehicle_body_fuel_type.setText(0, COMPMODEL_NUMTYPES )      #"Vehicle body/fuel type")
#
# Define Fixed Activity Prism Models
#
#        fixed_activity_prism_models = QTreeWidgetItem(medium_term_models)
#        fixed_activity_prism_models.setText(0, COMP_FIXEDACTPRISM)
#
#        daystart = QTreeWidgetItem(fixed_activity_prism_models)
#        daystart.setText(0, COMPMODEL_DAYSTART)
#
#        daystart_aw = QTreeWidgetItem(daystart)
#        daystart_aw.setText(0, "Adult Workers")
#        daystart_an = QTreeWidgetItem(daystart)
#        daystart_an.setText(0, "Adult Non-workers")
#        daystart_na = QTreeWidgetItem(daystart)
#        daystart_na.setText(0, "Children (5-17 years) and\nAdult Students")
#        daystart_ps = QTreeWidgetItem(daystart)
#        daystart_ps.setText(0, "Pre-school Children\n(0-4 years)")
#
#        dayend = QTreeWidgetItem(fixed_activity_prism_models)
#        dayend.setText(0, COMPMODEL_DAYEND)
#
#        dayend_aw = QTreeWidgetItem(dayend)
#        dayend_aw.setText(0, "Adult Workers")
#        dayend_an = QTreeWidgetItem(dayend)
#        dayend_an.setText(0, "Adult Non-workers")
#        dayend_na = QTreeWidgetItem(dayend)
#        dayend_na.setText(0, "Children (5-17 years) and\nAdult Students")
#        dayend_ps = QTreeWidgetItem(dayend)
#        dayend_ps.setText(0, "Pre-school Children\n(0-4 years)")
#
#        work_episodes = QTreeWidgetItem(fixed_activity_prism_models)
#        work_episodes.setText(0, COMPMODEL_WRKEPISODES)
#
#        one_episode_workers = QTreeWidgetItem(fixed_activity_prism_models)
#        one_episode_workers.setText(0, COMPMODEL_1WEPISODE)
#        latest_oneepiso = QTreeWidgetItem(one_episode_workers)
#        latest_oneepiso.setText(0, COMPMODEL_WORKSTART)
#        early_oneepiso = QTreeWidgetItem(one_episode_workers)
#        early_oneepiso.setText(0, COMPMODEL_WORKEND)
#
#
#        two_episode_workers1 = QTreeWidgetItem(fixed_activity_prism_models)
#        two_episode_workers1.setText(0, COMPMODEL_2WEPISODE1)
#        latest_twoepiso1 = QTreeWidgetItem(two_episode_workers1)
#        latest_twoepiso1.setText(0, COMPMODEL_WORKSTART1)
#        early_twoepiso1 = QTreeWidgetItem(two_episode_workers1)
#        early_twoepiso1.setText(0, COMPMODEL_WORKEND1)
#
#        two_episode_workers2 = QTreeWidgetItem(fixed_activity_prism_models)
#        two_episode_workers2.setText(0, COMPMODEL_2WEPISODE2)
#        latest_twoepiso2 = QTreeWidgetItem(two_episode_workers2)
#        latest_twoepiso2.setText(0, COMPMODEL_WORKSTART2)
#        early_twoepiso2 = QTreeWidgetItem(two_episode_workers2)
#        early_twoepiso2.setText(0, COMPMODEL_WORKEND2)
#
#        schoolprisms = QTreeWidgetItem(fixed_activity_prism_models)
#        schoolprisms.setText(0, COMPMODEL_SCHEPISODES)
#        latest_school = QTreeWidgetItem(schoolprisms)
#        latest_school.setText(0, COMPMODEL_SCHSTART)
#        early_school = QTreeWidgetItem(schoolprisms)
#        early_school.setText(0, COMPMODEL_SCHEND)
#
#        preschoolprisms = QTreeWidgetItem(fixed_activity_prism_models)
#        preschoolprisms.setText(0, COMPMODEL_PRESCHEPISODES)
#        latest_preschool = QTreeWidgetItem(preschoolprisms)
#        latest_preschool.setText(0, COMPMODEL_PRESCHSTART)
#        early_preschool = QTreeWidgetItem(preschoolprisms)
#        early_preschool.setText(0, COMPMODEL_PRESCHEND)
#
# Define Activity Skeleton Reconciliation System
#
#        skeleton_reconciliation_system = QTreeWidgetItem(medium_term_models)
#        skeleton_reconciliation_system.setText(0, COMP_ACTSKELRECONCILIATION)
#
#        skeleton_reconciliation = QTreeWidgetItem(skeleton_reconciliation_system)
# skeleton_reconciliation.setText(0, COMPMODEL_ASRECONCIL)    #"Activity Skeleton Reconciliation")
#
#        person_constraints_1 = QTreeWidgetItem(skeleton_reconciliation_system)
# person_constraints_1.setText(0, COMPMODEL_ASCONST)          #"Within person constraints")
#
#        adjustment_1 = QTreeWidgetItem(skeleton_reconciliation_system)
# adjustment_1.setText(0, COMPMODEL_ASADJUST )                #"Adjustments to the activity skeleton based on expected Travel Time from previous day")
#
#        short_term_models = QTreeWidgetItem(self)
#        short_term_models.setText(0, COMP_SHORTTERM)
#
# Define Child Daily Status and Allocation Model
#
#        child_model = QTreeWidgetItem(medium_term_models)
#        child_model.setText(0, COMP_CHILDSTATUS)
#
#        sch_status = QTreeWidgetItem(child_model)
#        sch_status.setText(0, COMPMODEL_SCHSTATUS)
#        children_preschool = QTreeWidgetItem(sch_status)
#        children_preschool.setText(0, COMPMODEL_PRESCHDAILYSTATUS)
#        children_school1 = QTreeWidgetItem(sch_status)
# children_school1.setText(0, COMPMODEL_SCHDAILYSTATUS)         #"Children (Status \55 School)")
#
#        child_dependent = QTreeWidgetItem(child_model)
#        child_dependent.setText(0, COMPMODEL_CHIDDEPEND)
#        children_hmindep = QTreeWidgetItem(child_dependent)
#        children_hmindep.setText(0, COMPMODEL_HMINDEP)
#        children_schindep = QTreeWidgetItem(child_dependent)
#        children_schindep.setText(0, COMPMODEL_SCHDAILYINDEP)
#        children_aftschindep = QTreeWidgetItem(child_dependent)
#        children_aftschindep.setText(0, COMPMODEL_AFTSCHDAILYINDEP)
#
#        aft_sch_activity = QTreeWidgetItem(child_model)
#        aft_sch_activity.setText(0, COMPMODEL_AFTSCHACTIVITY)
#        children_aftschacttype = QTreeWidgetItem(aft_sch_activity)
#        children_aftschacttype.setText(0, COMPMODEL_AFTSCHACTTYPE)
#        children_aftschactdest = QTreeWidgetItem(aft_sch_activity)
#        children_aftschactdest.setText(0, COMPMODEL_AFTSCHACTDEST)
#        children_aftschactdur = QTreeWidgetItem(aft_sch_activity)
#        children_aftschactdur.setText(0, COMPMODEL_AFTSCHACTDUR)
#        children_aftschactjointact = QTreeWidgetItem(aft_sch_activity)
#        children_aftschactjointact.setText(0, COMPMODEL_AFTSCHJOINTACT)
#
#
##        children_1 = QTreeWidgetItem(child_model)
# children_1.setText(0, COMPMODEL_CSCHILD0t4)                 #"Children (0-4 years old)")
##        children_2 = QTreeWidgetItem(child_model)
##        children_2.setText(0, COMPMODEL_CSCHILD5t17)
#
#
#
#
# Define Adult Daily Status Model
#
#        adult_model = QTreeWidgetItem(medium_term_models)
#        adult_model.setText(0, COMP_ADULTSTATUS)
#
#        assign_stayhmchild_wrk = QTreeWidgetItem(adult_model)
# assign_stayhmchild_wrk.setText(0, COMPMODEL_ASDEPSTAYHM_WRK) #"Assign all dependent children to one non-working adult")
#        assign_stayhmchild_nonwrk = QTreeWidgetItem(adult_model)
# assign_stayhmchild_nonwrk.setText(0, COMPMODEL_ASDEPSTAYHM_NONWORK)   #"Assign each dependent child to a household adult subject to the fixed activity schedule of the adult")
#        assign_chauffchild = QTreeWidgetItem(adult_model)
#        assign_chauffchild.setText(0, COMPMODEL_ASDEPCHAUFF)
#        work_today = QTreeWidgetItem(adult_model)
#        work_today.setText(0, COMPMODEL_WRKDAILYSTATUS)
#
#
# Define Activity Travel Pattern Simulator
#        activity_travel_pattern_simulator = QTreeWidgetItem(short_term_models)
#        activity_travel_pattern_simulator.setText(0, COMP_ACTTRAVSIMULATOR)
#
#        time_slice = QTreeWidgetItem(activity_travel_pattern_simulator)
# time_slice.setText(0, COMPMODEL_SMSLICE)                    #"Within a time slice")
#
#        children_with_activity = QTreeWidgetItem(activity_travel_pattern_simulator)
#        children_with_activity.setText(0, "Children with after school dependent activities")
#
#        activity_pursued_1 = QTreeWidgetItem(children_with_activity)
# activity_pursued_1.setText(0, COMPMODEL_SMACTIVEPURSUE)     #"Can activity be pursued jointly with a Household member?")
#
#        assign_to_non_hhold = QTreeWidgetItem(children_with_activity)
# assign_to_non_hhold.setText(0, COMPMODEL_SMACTIVEASSIGNED)  #"Activity assigned to a Non-household member comprising Joint Activity with Non-household member")
#
#        assign_to_hhold = QTreeWidgetItem(children_with_activity)
# assign_to_hhold.setText(0, COMPMODEL_SMASSIGNACTIVE)        #"Assign the activity to Household member comprising Joint Activity with household member")
#
#        mode_choice_model = QTreeWidgetItem(children_with_activity)
# mode_choice_model.setText(0, COMPMODEL_AFTSCHACTIVITYMODE)       #"Mode choice model for intra-household joint trips with children")
#
#        all_other_individuals = QTreeWidgetItem(activity_travel_pattern_simulator)
#        all_other_individuals.setText(0, "All other individuals")
#
#        adult_individuals = QTreeWidgetItem(all_other_individuals)
# adult_individuals.setText(0, COMPMODEL_SMINDIVIDUAL)        #"Adult individuals, children with independent activities")
#
#        travel_time = QTreeWidgetItem(all_other_individuals)
# travel_time.setText(0, COMPMODEL_SMTRIPTIME)                #"Is travel time to next fixed activity \74 time available in the prism?")
#
#        activity_choice = QTreeWidgetItem(all_other_individuals)
# activity_choice.setText(0, COMPMODEL_ACTIVITYTYPE)             #"Activity Type Choice; Mode-Destination Choice")
#
#        actual_start_time = QTreeWidgetItem(all_other_individuals)
# actual_start_time.setText(0, COMPMODEL_SMSTARTTIME)         #"Actual start time for the activity")
#
#        time_in_activity = QTreeWidgetItem(all_other_individuals)
# time_in_activity.setText(0, COMPMODEL_ACTIVITYDURATION)         #"Is there enough time to engage in the activity?")
#
#        proceed_next_activity = QTreeWidgetItem(all_other_individuals)
# proceed_next_activity.setText(0, COMPMODEL_SMPROCEED)       #"Proceed to next fixed activity")
#
#        mode_choice_next_activity = QTreeWidgetItem(all_other_individuals)
# mode_choice_next_activity.setText(0, COMPMODEL_FIXEDACTIVITYMODE)   #"Mode Choice to the next fixed activity")
#
#        hov = QTreeWidgetItem(all_other_individuals)
# hov.setText(0, COMPMODEL_SMISHOV)                           #"Is the mode of the trip HOV?")
#
#        activity_pursued_2 = QTreeWidgetItem(all_other_individuals)
# activity_pursued_2.setText(0, COMPMODEL_SMACTIVEPURSED)     #"Can activity be pursued jointly with Household members?")
#
#        check_if_join_activity = QTreeWidgetItem(all_other_individuals)
# check_if_join_activity.setText(0, COMPMODEL_JOINTACTIVITY)   #"For each available household member, check to see if he/she will join the activity?")
#
#        activity_non_hhold = QTreeWidgetItem(all_other_individuals)
# activity_non_hhold.setText(0, COMPMODEL_SMACTIVENON)        #"Joint Activity with Non-household member")
#
#        activity_hhold = QTreeWidgetItem(all_other_individuals)
# activity_hhold.setText(0, COMPMODEL_SMACTIVEHOUSE)          #"Joint Activity with household member")
#
#        sov_hov = QTreeWidgetItem(activity_travel_pattern_simulator)
# sov_hov.setText(0, COMPMODEL_TRIPVEHICLE)                      #"If mode is SOV or HOV Driver identify vehicle")
#
#        activity_travel_pattern = QTreeWidgetItem(activity_travel_pattern_simulator)
# activity_travel_pattern.setText(0, COMPMODEL_SMPATTERN)     #"Activity-travel patterns for all individuals within the time-slice")
#
# Define Activity Travel Reconciliation System
#        travel_reconciliation_system = QTreeWidgetItem(short_term_models)
#        travel_reconciliation_system.setText(0, COMP_ACTTRAVRECONCILIATION)
#
#        pattern_reconciliation = QTreeWidgetItem(travel_reconciliation_system)
# pattern_reconciliation.setText(0, COMPMODEL_ATRECONCIL)             #"Activity-travel Pattern Reconciliation")
#
#        person_constraints_2 = QTreeWidgetItem(travel_reconciliation_system)
# person_constraints_2.setText(0, COMPMODEL_ATPERCONST)               #"Within person constraints")
#
#        hhold_constraints = QTreeWidgetItem(travel_reconciliation_system)
# hhold_constraints.setText(0, COMPMODEL_ATHOUCONST)                  #"Within household constraints")
#
#        adjustment_2 = QTreeWidgetItem(travel_reconciliation_system)
# adjustment_2.setText(0, COMPMODEL_ATADJUST)                         #"Duration adjustment after arrival")
#
#
#
#        time_use_utility_calculator = QTreeWidgetItem(self)
#        time_use_utility_calculator.setText(0, COMP_TIMEUSEUTILITY)

        self.hide_components = [COMPMODEL_IDENFIXEDVERTICES, COMPMODEL_CLEANDAILY, COMPMODEL_RECONLONGTERM, COMPMODEL_CHILDTERMALLOCATE, COMPMODEL_CLEANAGGREGATE, COMPMODEL_CHILDALLOCATE,
                                COMPMODEL_ARRTIMEPPROCESS, COMPMODEL_OCCUPPROCESS, COMPKEY_EXTRACTEPISODEHH,
                                AGGACT_SCHEDULE, 'ChildDependencyResolution', 'Fixing Trip Purpose', 'TourAttributeProcessing']

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(
            self, SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)

#        self.connect(self, SIGNAL('itemClicked (QTreeWidgetItem *,int)'), self.treeItemSelected)
#        self.connect(self, SIGNAL('itemClicked (QTreeWidgetItem *,int)'), self.openModelSelected)
        self.connect(
            self, SIGNAL('itemChanged (QTreeWidgetItem *,int)'), self.saveSkip)

    def setProjectElement(self):
        projelts = self.configobject.getProjects()
        for elt in projelts:
            if elt.tag != MODELCONFIG and elt.tag != "DTAConnection":
                root_term = QTreeWidgetItem(self)
                root_term.setText(0, str(elt.tag))

    def setTreeWidget(self):
        if self.configobject != None:
            #root_term1 = QTreeWidgetItem(self)
            #root_term1.setText(0, "Component")
            #compelts = self.configobject.getComponents()
            #self.components(root_term1, compelts)

            compelts = self.configobject.getModelConfigChildren()
            if compelts is not None:
                root_term = QTreeWidgetItem(self)
                root_term.setText(0, "Component")

                for comp in compelts:
                    if comp.tag == "Component" or comp.tag == "Component1":
                        self.components(root_term, comp)
                    elif comp.tag == "ComponentList":
                        subcompelts = comp.getchildren()
                        component_term = QTreeWidgetItem(root_term)
                        component_term.setText(0, "Component List")
                        for subcomp in subcompelts:
                            print subcomp.tag
                            if subcomp.tag.lower() == "subcomponent":
                                self.components(component_term, subcomp)
                            else:
                                element = QTreeWidgetItem(component_term)
                                element.setText(0, subcomp.tag)

    def components(self, root_term, comp):

        comtitle = str(comp.get(NAME))
        if comtitle in COMPONENTMAP.keys():
            compname = COMPONENTMAP[comp.get(NAME)][0]
        else:
            compname = comtitle
        component_term = QTreeWidgetItem(root_term)
        if compname in self.hide_components:
            component_term.setHidden(True)
        component_term.setText(0, compname)
        component_term.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)

        for key in comp.keys():
            if key == "skip" or key == "completed":
                attr = "%s" % (comp.get(key))
                if key == "skip":
                    if attr == "True":
                        component_term.setCheckState(2, Qt.Checked)
                    else:
                        component_term.setCheckState(2, Qt.Unchecked)
                else:
                    component_term.setIcon(1, QIcon("./images/%s" % (attr)))

        for elt in comp.getchildren():
            title = str(elt.tag)
            if title.lower() != 'model':
                element_term = QTreeWidgetItem(component_term)
                element_term.setText(0, title)
            else:
                name = str(elt.get("name")).lower()
                if name in MODELSMAP.keys():
                    name = title + ": " + MODELSMAP[name][0]
                    element_term = QTreeWidgetItem(component_term)
                    element_term.setText(0, name)
                else:
                    name = title + ": " + name
                    element_term = QTreeWidgetItem(component_term)
                    element_term.setText(0, name)


#    def setTreeWidgetEle(self,elt,tree_term):
#            attribute_term = QTreeWidgetItem(tree_term)
#            attribute_term.setText(0, "Attribute")
#            for key in elt.keys():
#                attr = "%s: %s"%(key,elt.get(key))
#                attr_term = QTreeWidgetItem(attribute_term)
#                attr_term.setText(0, attr)
#
#            for subelt in elt.getchildren():
#                element_term = QTreeWidgetItem(tree_term)
#                element_term.setText(0, subelt.tag)

    def on_context_menu(self, point):
        item = self.currentItem()
        father = item.parent()

        menubar = QMenu(self)
        if father == None:
            if item.text(0) != COMP:
                one = menubar.addAction("Open")
                self.connect(one, SIGNAL("triggered()"), self.openProject)
            else:
                one = menubar.addAction("Add Component")
                two = menubar.addAction("Add ComponentList")
                self.connect(one, SIGNAL("triggered()"), self.addComponent)
                self.connect(two, SIGNAL("triggered()"), self.addComponentList)

        elif item.text(0) == "Component List":
            one = menubar.addAction("Add Analysis Interval")
            two = menubar.addAction("Add Sub-Component")
            self.connect(one, SIGNAL("triggered()"), self.analy_inter)
            self.connect(two, SIGNAL("triggered()"), self.addSubComponent)

        elif father.text(0) == "Component" or father.text(0) == "Component List":
            open_com = menubar.addAction("Open Component")
            menubar.addSeparator()
            one = menubar.addAction("Add Model")
            two = menubar.addAction("Add DBTables")
            three = menubar.addAction("Add Spatial Constraints")
            four = menubar.addAction("Add Dynamic Spatial Constraints")
            five = menubar.addAction("Add Consistency Checks")
            six = menubar.addAction("Add Delete Records")
            seven = menubar.addAction("Add Analysis Interval")
            eight = menubar.addAction("Add History Information")
            nine = menubar.addAction("Add Aggregate")
            ten = menubar.addAction("Add Analysis Interval Filter")
            eleven = menubar.addAction("Add PreProcess Data")
            twelve = menubar.addAction("Add Delete Based On")
            menubar.addSeparator()
            remove = menubar.addAction("Delete Component")

            self.connect(open_com, SIGNAL("triggered()"), self.openComponent)
            self.connect(one, SIGNAL("triggered()"), self.add_model)
            self.connect(two, SIGNAL("triggered()"), self.dbtable)
            self.connect(three, SIGNAL("triggered()"), self.spatial_cons)
            self.connect(four, SIGNAL("triggered()"), self.dynamic_spat)
            self.connect(five, SIGNAL("triggered()"), self.consis_chek)
            self.connect(six, SIGNAL("triggered()"), self.dele_reco)
            self.connect(seven, SIGNAL("triggered()"), self.analy_inter)
            self.connect(eight, SIGNAL("triggered()"), self.hist_info)
            self.connect(nine, SIGNAL("triggered()"), self.aggregate)
            self.connect(ten, SIGNAL("triggered()"), self.analysis_filter)
            self.connect(eleven, SIGNAL("triggered()"), self.preprocess)
            self.connect(twelve, SIGNAL("triggered()"), self.delete_basedon)
            self.connect(remove, SIGNAL("triggered()"), self.remove_element)

        else:
            #            foreparent = father.parent()
            one = menubar.addAction("Open Element")
            menubar.addSeparator()
            remove = menubar.addAction("Delete Element")
            self.connect(remove, SIGNAL("triggered()"), self.remove_element)
            self.connect(one, SIGNAL("triggered()"), self.openElementSelected)

        menubar.popup(self.mapToGlobal(point))

    def moveup(self):

        if self.isMove == True:
            self.isMove = False
            index = []
            father = None
            item = self.currentItem()
#            if item.text(0) != "Attribute":
            if item != None:
                father = item.parent()
                if father != None:

                    i = father.indexOfChild(item)
                    index.append(i)
                    if i > 0:
                        father.removeChild(item)
                        father.insertChild(i - 1, item)
                        self.setCurrentItem(item)

            while father != None:
                item = father.parent()
                if item != None:
                    i = item.indexOfChild(father)
                    index.append(i)
                    father = father.parent
                father = item

            if len(index) > 0 and index[0] > 0:
                index.reverse()
                self.configobject.moveup(index)
        self.isMove = True

    def movedown(self):

        if self.isMove == True:
            self.isMove = False
            index = []
            item = self.currentItem()
#            if item.text(0) != "Attribute":
            if item != None:
                father = item.parent()
                if father != None:

                    i = father.indexOfChild(item)
                    index.append(i)
                    max_i = father.childCount()
                    if i < max_i - 1:
                        father.removeChild(item)
                        father.insertChild(i + 1, item)
                        self.setCurrentItem(item)

            while father != None:
                item = father.parent()
                if item != None:
                    i = item.indexOfChild(father)
                    index.append(i)
                    father = father.parent
                father = item

            if len(index) > 0 and index[0] < max_i - 1:
                index.reverse()
                self.configobject.movedown(index)

            self.isMove = True

    def setConfigObject(self, co):
        self.configobject = co
        self.setProjectElement()
        self.setTreeWidget()
#        self.setAllComSimStatuses()


#    def setAllComSimStatuses(self):
#        self.setCompSimStatus(COMPMODEL_NUMVEHS)
#        self.setCompSimStatus(COMPMODEL_NUMTYPES)
#        self.setCompSimStatus(COMPMODEL_DAYSTART)
#        self.setCompSimStatus(COMPMODEL_DAYEND)
#        self.setCompSimStatus(COMPMODEL_WRKEPISODES)
#        self.setCompSimStatus(COMPMODEL_1WEPISODE)
#        self.setCompSimStatus(COMPMODEL_2WEPISODE1)
#        self.setCompSimStatus(COMPMODEL_2WEPISODE2)
#        self.setCompSimStatus(COMPMODEL_SCHEPISODES)
#        self.setCompSimStatus(COMPMODEL_PRESCHEPISODES)
#        self.setCompSimStatus(COMPMODEL_SCHSTATUS)
#        self.setCompSimStatus(COMPMODEL_CHIDDEPEND)
#        self.setCompSimStatus(COMPMODEL_AFTSCHACTIVITY)
#
#
#    def setCompSimStatus(self,comptitle):
#        treecomp = self.findItems(QString(comptitle),Qt.MatchFixedString | Qt.MatchRecursive)[0]
#        treecomp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
#        compname = (COMPONENTMAP[comptitle])[0]
#        compsimstat = self.configobject.getCompSimStatus(compname)
#        if compsimstat != None:
#            treecomp.setIcon(1, QIcon("./images/%s" %(compsimstat[0])))
#            if compsimstat[1]:
#                treecomp.setCheckState(2, Qt.Checked)
#            else:
#                treecomp.setCheckState(2, Qt.Unchecked)

    def saveSkip(self, item, col):
        father = item.parent()
        if father != None:
            if str(father.text(0)) == "Component":
                index = father.indexOfChild(item)
                if self.configobject != None and col == 2:
                    #            compname = (COMPONENTMAP[str(item.text(0))])[0]
                    comp = self.configobject.getCompIndex(index)
                    if comp != None:
                        if item.checkState(2) == 2:
                            comp.set('skip', 'True')
                        else:
                            comp.set('skip', 'False')

#    def openModelSelected(self,item,col):
#        itemname = str(item.text(col))
#        itemlower = itemname.lower()
#        if itemlower.find("model") > -1:
#            index = self.findIndex(item)
#            model = self.configobject.getElement(index)
#
#            if model != None:
#                diag = AbtractSpecDialog(self.configobject,"","",model)
#                diag.exec_()

    def openProject(self):
        item = self.currentItem()
        eltname = str(item.text(0))
        model = self.configobject.protree.find(eltname)
        if model != None:
            if eltname != DB_CONFIG:
                diag = ProjectConfigDialog(self.configobject, model, self)
                diag.exec_()
            else:
                diag = DatabaseConfig(self.configobject)
                diag.exec_()

    def addComponent(self):
        model = self.configobject.protree.find(MODELCONFIG)
        if model != None:
            self.subcomponent = "Component"
            diag = AbtractMixedDialog(self.configobject, model, 4, self)
            diag.exec_()

    def addComponentList(self):
        model = self.configobject.protree.find(MODELCONFIG)
        if model != None:
            element = etree.Element("ComponentList")
            model.append(element)
            component_term = QTreeWidgetItem(self.currentItem())
            component_term.setText(0, "Component List")

    def addSubComponent(self):
        model = self.configobject.getElements("ComponentList")
        if model[0] != None:
            self.subcomponent = "SubComponent"
            diag = AbtractMixedDialog(self.configobject, model[0], 4, self)
            diag.exec_()

    def openElementSelected(self):
        item = self.currentItem()
        itemname = str(item.text(0))
        itemlower = itemname.lower()
        if itemlower.find("model") > -1:
            index = self.find_model()[1]
            if len(index) > 0:
                itemname = itemname.replace("Model: ", "")
                diag = AbtractSpecDialog(
                    self.configobject, "", itemname, index, self)
                diag.exec_()

                self.father.refreshflowchart()
        else:
            model = self.find_model()[0]
            if model != None:
                diag = AbtractMixedDialog(self.configobject, model, 1, self)
                diag.exec_()

    def openComponent(self):
        model = self.find_model()[0]
        if model != None:
            diag = AbtractMixedDialog(self.configobject, model, 3, self)
            diag.exec_()

    def add_model(self):
        model = self.find_model()[1]
        if model != None:
            diag = AbtractSpecDialog(self.configobject, "", "", model, self)
            diag.exec_()

    def spatial_cons(self):
        model = self.find_model()[0]
        if model != None:
            self.subcomponent = "SpatialConstraints"
            diag = AbtractMixedDialog(self.configobject, model, 2, self)
            diag.exec_()

    def dynamic_spat(self):
        model = self.find_model()[0]
        if model != None:
            self.subcomponent = "DynamicSpatialConstraints"
            diag = AbtractMixedDialog(self.configobject, model, 2, self)
            diag.exec_()

    def consis_chek(self):
        model = self.find_model()[0]
        if model != None:
            self.subcomponent = "ConsistencyChecks"
            diag = AbtractMixedDialog(self.configobject, model, 2, self)
            diag.exec_()

    def dele_reco(self):
        model = self.find_model()[0]
        if model != None:
            self.subcomponent = "DeleteRecords"
            diag = AbtractMixedDialog(self.configobject, model, 2, self)
            diag.exec_()

    def analy_inter(self):
        model = self.find_model()[0]
        if model != None:
            self.subcomponent = "AnalysisInterval"
            diag = AbtractMixedDialog(self.configobject, model, 2, self)
            diag.exec_()

    def hist_info(self):
        model = self.find_model()[0]
        if model != None:
            self.subcomponent = "HistoryInformation"
            diag = AbtractMixedDialog(self.configobject, model, 2, self)
            diag.exec_()

    def aggregate(self):
        model = self.find_model()[0]
        if model != None:
            self.subcomponent = "Aggregate"
            diag = AbtractMixedDialog(self.configobject, model, 2, self)
            diag.exec_()

    def analysis_filter(self):
        model = self.find_model()[0]
        if model != None:
            self.subcomponent = "AnalysisIntervalFilter"
            diag = AbtractMixedDialog(self.configobject, model, 2, self)
            diag.exec_()

    def preprocess(self):
        model = self.find_model()[0]
        if model != None:
            self.subcomponent = "PreProcessData"
            diag = AbtractMixedDialog(self.configobject, model, 2, self)
            diag.exec_()

    def delete_basedon(self):
        model = self.find_model()[0]
        if model != None:
            self.subcomponent = "DeleteBasedOn"
            diag = AbtractMixedDialog(self.configobject, model, 2, self)
            diag.exec_()

    def dbtable(self):
        model = self.find_model()[0]
        if model != None:
            self.subcomponent = "DBTables"
            diag = AbtractMixedDialog(self.configobject, model, 2, self)
            diag.exec_()

    def find_model(self):
        item = self.currentItem()
        index = self.findIndex(item)
        model = self.configobject.getElement(index)
        return [model, index]

#
#     def treeItemSelected(self,item,col):
#         diagtitle = None
#         diag = None
#         modelkey = None
#         if str(item.text(col)).lower() == COMPMODEL_NUMVEHS.lower():
#             diagtitle = COMPMODEL_NUMVEHS
#             modelkey = MODELKEY_NUMVEHS
#         elif str(item.text(col)).lower() == COMPMODEL_NUMTYPES.lower():
#             diagtitle = COMPMODEL_NUMTYPES
#             modelkey = MODELKEY_VEHTYPE
#
#         elif str(item.text(col)).lower() == ('Adult Workers').lower():
#             seg = str((item.parent()).text(0)).lower()
#             if seg == COMPMODEL_DAYSTART.lower():
#                 diagtitle = COMPMODEL_DAYSTART
#                 modelkey = MODELKEY_DAYSTART_AW
#             elif seg == COMPMODEL_DAYEND.lower():
#                 diagtitle = COMPMODEL_DAYEND
#                 modelkey = MODELKEY_DAYEND_AW
#         elif str(item.text(col)).lower() == ('Adult Non-workers').lower():
#             seg = str((item.parent()).text(0)).lower()
#             if seg == COMPMODEL_DAYSTART.lower():
#                 diagtitle = COMPMODEL_DAYSTART
#                 modelkey = MODELKEY_DAYSTART_AN
#             elif seg == COMPMODEL_DAYEND.lower():
#                 diagtitle = COMPMODEL_DAYEND
#                 modelkey = MODELKEY_DAYEND_AN
#         elif str(item.text(col)).lower() == ('Children (5-17 years) and\nAdult Students').lower():
#             seg = str((item.parent()).text(0)).lower()
#             if seg == COMPMODEL_DAYSTART.lower():
#                 diagtitle = COMPMODEL_DAYSTART
#                 modelkey = MODELKEY_DAYSTART_NA
#             elif seg == COMPMODEL_DAYEND.lower():
#                 diagtitle = COMPMODEL_DAYEND
#                 modelkey = MODELKEY_DAYEND_NA
#         elif str(item.text(col)).lower() == ('Pre-school Children\n(0-4 years)').lower():
#             seg = str((item.parent()).text(0)).lower()
#             if seg == COMPMODEL_DAYSTART.lower():
#                 diagtitle = COMPMODEL_DAYSTART
#                 modelkey = MODELKEY_DAYSTART_PS
#             elif seg == COMPMODEL_DAYEND.lower():
#                 diagtitle = COMPMODEL_DAYEND
#                 modelkey = MODELKEY_DAYEND_PS
#
#         elif str(item.text(col)).lower() == COMPMODEL_WRKEPISODES.lower():
#             diagtitle = COMPMODEL_WRKEPISODES
#             modelkey = MODELKEY_WRKEPISODES
#         elif str(item.text(col)).lower() == COMPMODEL_WORKSTART.lower():
#             diagtitle = COMPMODEL_WORKSTART
#             modelkey = MODELKEY_WORKSTART
#         elif str(item.text(col)).lower() == COMPMODEL_WORKEND.lower():
#             diagtitle = COMPMODEL_WORKEND
#             modelkey = MODELKEY_WORKEND
#         elif str(item.text(col)).lower() == COMPMODEL_WORKSTART1.lower():
#             diagtitle = COMPMODEL_WORKSTART1
#             modelkey = MODELKEY_WORKSTART1
#         elif str(item.text(col)).lower() == COMPMODEL_WORKEND1.lower():
#             diagtitle = COMPMODEL_WORKEND1
#             modelkey = MODELKEY_WORKEND1
#         elif str(item.text(col)).lower() == COMPMODEL_WORKSTART2.lower():
#             diagtitle = COMPMODEL_WORKSTART2
#             modelkey = MODELKEY_WORKSTART2
#         elif str(item.text(col)).lower() == COMPMODEL_WORKEND2.lower():
#             diagtitle = COMPMODEL_WORKEND2
#             modelkey = MODELKEY_WORKEND2
#
#         elif str(item.text(col)).lower() == COMPMODEL_SCHSTART.lower():
#             diagtitle = COMPMODEL_SCHSTART
#             modelkey = MODELKEY_SCHSTART
#         elif str(item.text(col)).lower() == COMPMODEL_SCHEND.lower():
#             diagtitle = COMPMODEL_SCHEND
#             modelkey = MODELKEY_SCHEND
#
#         elif str(item.text(col)).lower() == COMPMODEL_PRESCHSTART.lower():
#             diagtitle = COMPMODEL_PRESCHSTART
#             modelkey = MODELKEY_PRESCHSTART
#         elif str(item.text(col)).lower() == COMPMODEL_PRESCHEND.lower():
#             diagtitle = COMPMODEL_PRESCHEND
#             modelkey = MODELKEY_PRESCHEND
#
#         elif str(item.text(col)).lower() == COMPMODEL_PRESCHDAILYSTATUS.lower():
#             diagtitle = COMPMODEL_PRESCHDAILYSTATUS
#             modelkey = MODELKEY_PRESCHDAILYSTATUS
#         elif str(item.text(col)).lower() == COMPMODEL_SCHDAILYSTATUS.lower():
#             diagtitle = COMPMODEL_SCHDAILYSTATUS
#             modelkey = MODELKEY_SCHDAILYSTATUS
#         elif str(item.text(col)).lower() == COMPMODEL_HMINDEP.lower():
#             diagtitle = COMPMODEL_HMINDEP
#             modelkey = MODELKEY_HMINDEP
#         elif str(item.text(col)).lower() == COMPMODEL_SCHDAILYINDEP.lower():
#             diagtitle = COMPMODEL_SCHDAILYINDEP
#             modelkey = MODELKEY_SCHDAILYINDEP
#         elif str(item.text(col)).lower() == COMPMODEL_AFTSCHDAILYINDEP.lower():
#             diagtitle = COMPMODEL_AFTSCHDAILYINDEP
#             modelkey = MODELKEY_AFTSCHDAILYINDEP
#         elif str(item.text(col)).lower() == COMPMODEL_AFTSCHACTTYPE.lower():
#             diagtitle = COMPMODEL_AFTSCHACTTYPE
#             modelkey = MODELKEY_AFTSCHACTTYPE
#         elif str(item.text(col)).lower() == COMPMODEL_AFTSCHACTDEST.lower():
#             diagtitle = COMPMODEL_AFTSCHACTDEST
#             modelkey = MODELKEY_AFTSCHACTDEST
#         elif str(item.text(col)).lower() == COMPMODEL_AFTSCHACTDUR.lower():
#             diagtitle = COMPMODEL_AFTSCHACTDUR
#             modelkey = MODELKEY_AFTSCHACTDUR
#         elif str(item.text(col)).lower() == COMPMODEL_AFTSCHJOINTACT.lower():
#             diagtitle = COMPMODEL_AFTSCHJOINTACT
#             modelkey = MODELKEY_AFTSCHJOINTACT
#
#         elif str(item.text(col)).lower() == COMPMODEL_WRKDAILYSTATUS.lower():
#             diagtitle = COMPMODEL_WRKDAILYSTATUS
#             modelkey = MODELKEY_WRKDAILYSTATUS
#
#
#         elif item.text(col) == COMPMODEL_SMACTIVEPURSUE:
#             diagtitle = COMPMODEL_SMACTIVEPURSUE
#             modelkey = MODELKEY_SMACTIVEPURSUE
#         elif item.text(col) == COMPMODEL_SMACTIVEASSIGNED:
#             diagtitle = COMPMODEL_SMACTIVEASSIGNED
#             modelkey = MODELKEY_SMACTIVEASSIGNED
#         elif item.text(col) == COMPMODEL_SMASSIGNACTIVE:
#             diagtitle = COMPMODEL_SMASSIGNACTIVE
#             modelkey = MODELKEY_SMASSIGNACTIVE
#         elif item.text(col) == COMPMODEL_AFTSCHACTIVITYMODE:
#             diagtitle = COMPMODEL_AFTSCHACTIVITYMODE
#             modelkey = MODELKEY_AFTSCHACTIVITYMODE
#         elif item.text(col) == COMPMODEL_SMINDIVIDUAL:
#             diagtitle = COMPMODEL_SMINDIVIDUAL
#             modelkey = MODELKEY_SMINDIVIDUAL
#         elif item.text(col) == COMPMODEL_SMTRIPTIME:
#             diagtitle = COMPMODEL_SMTRIPTIME
#             modelkey = MODELKEY_SMTRIPTIME
#         elif item.text(col) == COMPMODEL_ACTIVITYTYPE:
#             diagtitle = COMPMODEL_ACTIVITYTYPE
#             modelkey = MODELKEY_ACTIVITYTYPE
#         elif item.text(col) == COMPMODEL_SMSTARTTIME:
#             diagtitle = COMPMODEL_SMSTARTTIME
#             modelkey = MODELKEY_SMSTARTTIME
#         elif item.text(col) == COMPMODEL_ACTIVITYDURATION:
#             diagtitle = COMPMODEL_ACTIVITYDURATION
#             modelkey = MODELKEY_ACTIVITYDURATION
#         elif item.text(col) == COMPMODEL_SMPROCEED:
#             diagtitle = COMPMODEL_SMPROCEED
#             modelkey = MODELKEY_SMPROCEED
#         elif item.text(col) == COMPMODEL_FIXEDACTIVITYMODE:
#             diagtitle = COMPMODEL_FIXEDACTIVITYMODE
#             modelkey = MODELKEY_FIXEDACTIVITYMODE
#         elif item.text(col) == COMPMODEL_SMISHOV:
#             diagtitle = COMPMODEL_SMISHOV
#             modelkey = MODELKEY_SMISHOV
#         elif item.text(col) == COMPMODEL_SMACTIVEPURSED:
#             diagtitle = COMPMODEL_SMACTIVEPURSED
#             modelkey = MODELKEY_SMACTIVEPURSED
#         elif item.text(col) == COMPMODEL_JOINTACTIVITY:
#             diagtitle = COMPMODEL_JOINTACTIVITY
#             modelkey = MODELKEY_JOINTACTIVITY
#         elif item.text(col) == COMPMODEL_TRIPVEHICLE:
#             diagtitle = COMPMODEL_TRIPVEHICLE
#             modelkey = MODELKEY_TRIPVEHICLE
#
#
#
#         if diagtitle != None and self.configobject != None:
#             diag = AbtractSpecDialog(self.configobject,modelkey,diagtitle)
#             diag.exec_()

    def remove_element(self):
        reply = QMessageBox.question(None, 'Remove', "Are you sure to remove?",
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            item = self.currentItem()
            index = self.findIndex(item)
            self.configobject.removeElement(index)
            self.removeItemWidget(item, 0)

    def findIndex(self, item):
        index = []
        father = None

        if item != None:
            father = item.parent()

        while father != None:
            i = father.indexOfChild(item)
            index.append(i)
            item = father
            father = father.parent()

        index.reverse()
        return index


class TreeWidgetItem(QTreeWidgetItem):

    def __init__(self, parent, name, elt):
        QTreeWidgetItem.__init__(self, parent, name, elt)
        self.setText(0, name)
        self.element = elt
