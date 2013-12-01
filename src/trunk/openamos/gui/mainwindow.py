import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from model_manager.models import *
from model_manager.model_manager_treewidget import *

from file_menu.newproject import *
from file_menu.openproject import *
from file_menu.saveproject import *
from file_menu.databaseconfig import *
from results_menu.to_postgis import *
from results_menu.view_sched import *
from results_menu.view_plot import *
from results_menu.kml_num_trips import *
from results_menu.import_nhts import *
from results_menu.to_msexcel import *
from run_menu.simulation_dialog import *

from openamos.core.config import *
from openamos.core.run.simulation_manager_cursor import SimulationManager

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("OpenAMOS: Version-1.0")
        self.showMaximized()
        self.setMinimumSize(800,600)
        self.setWindowIcon(QIcon('images/run.png'))

        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)
        
        # Variable for a project properties; can be used to see if a project is open or not
        self.proconfig = None
        
        # Defining central widget
        self.centralwidgetscroll = QScrollArea()
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidgetscroll)
        self.centralwidget.setFixedSize(1140, 1200)
        self.centralwidgetscroll.setWidget(self.centralwidget)
        
        # Defining help widget under central widget
#        size = self.geometry()
#        height = []
#        height.append(size.height() * 0.8)
#        height.append(size.height() * 0.2)
#        self.helpbrowser = QTextBrowser()
#        mainSplitter = QSplitter(Qt.Vertical)
#        mainSplitter.addWidget(self.centralwidgetscroll)
#        mainSplitter.addWidget(self.helpbrowser)
#        mainSplitter.setSizes(height)
#        self.setCentralWidget(mainSplitter)
#        self.centralwidget.setFixedSize(1140, 1200)
#        self.centralwidgetscroll.setWidget(self.centralwidget)

    
        # Defining status bar        
        self.sizelabel = QLabel()
        self.sizelabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizelabel)
        status.showMessage("Ready", 5000)
        
        # Setting help_dock_widget on the bottom of window to show instruction message
        help_dock_widget = QDockWidget(self.centralwidget)
        self.helpbrowser = QTextBrowser()
        help_dock_widget.setWidget(self.helpbrowser)
        help_dock_widget.setObjectName("help_dock_widget")
        help_dock_widget.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, help_dock_widget)
        
        
        # Defining manager widget
        # Setting all_manager_dock_widget
        all_manager_dock_widget = QDockWidget(self.centralwidget)
        splitter = QSplitter(Qt.Vertical)
        all_manager_dock_widget.setWidget(splitter)
        all_manager_dock_widget.setObjectName("all_manager_dock_widget")
        all_manager_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, all_manager_dock_widget)


        # Defining model_management as a QTreeWidget
        self.model_management = Model_Manager_Treewidget()
        self.model_management.setObjectName("model_management")
        self.model_management.headerItem().setText(0, "Model Management")
        self.connect(self.model_management, SIGNAL('itemClicked (QTreeWidgetItem *,int)'), self.showflowchart)


        # Defining data_management as a QTreeWidget
        self.data_management = QTreeWidget()
        self.data_management.setObjectName("data_management")
        self.data_management.headerItem().setText(0, "Data Management")
        self.data_management.setMinimumSize(50,50)

        buttonwidget = QWidget(self)
        buttonwidget.setMaximumHeight(32)
        buttonlayout = QHBoxLayout()
        buttonwidget.setLayout(buttonlayout)
        buttonlayout.setContentsMargins(0,0,0,0)
        
        tools = QToolBar()
        #tools.setMaximumWidth(70)
        up_action = self.createaction("",self.getup,"","arrow_up","Move up an element in the tree.")
        down_action = self.createaction("",self.getdown,"","arrow_down","Move down an element in the tree.")
        tools.addAction(up_action)
        tools.addAction(down_action)
        buttonlayout.addWidget(tools)


        # Adding model_management and data_management to all_manager_dock_widget
        splitter.addWidget(buttonwidget)
        splitter.addWidget(self.model_management)
        splitter.addWidget(self.data_management)
        



        # Call the class Models
        self.models = Models(self.centralwidget)
        
        #Method to disable menus and graphics based on whether a project is open or not
        self.checkProject()


# FILE MENU
# Defining menu
    # Defining File
        self.fileMenu = self.menuBar().addMenu("&File")
        project_new_action = self.createaction("&New Project", self.projectnew, QKeySequence.New, 
                                            "projectnew", "Create a new OpenAMOS project.")

        project_open_action = self.createaction("&Open Project", self.projectopen, QKeySequence.Open, 
                                            "projectopen", "Open a new OpenAMOS project.")

        project_save_action = self.createaction("&Save Project", self.projectsave, QKeySequence.Save, 
                                              "projectsave", "Save the current OpenAMOS project.")

        project_save_as_action = self.createaction("Save Project &As...", self.projectSaveAs, "Ctrl+Shift+S",
                                                icon="projectsaveas", tip="Save the current OpenAMOS project with a new name.")

        project_close_action = self.createaction("&Close Project", self.projectClose, QKeySequence.Close,
                                                "close",tip="Close the current OpenAMOS project.")

        project_print_action = self.createaction("&Print", None , QKeySequence.Print,
                                                tip="Print the current OpenAMOS project.")

        project_quit_action = self.createaction("&Quit", self.projectQuit, "Ctrl+Q",icon="Quit",
                                                tip="Quit OpenAMOS.")

#        self.addActions(self.fileMenu, (project_new_action,project_open_action,None,project_save_action,project_save_as_action,
#                                        project_print_action,None,project_close_action,project_quit_action, ))
        self.addActions(self.fileMenu, (project_new_action,project_open_action,None,project_save_action,project_save_as_action,
                                        None,project_close_action,project_quit_action, ))
      
    # Defining Models
        self.models_menu = self.menuBar().addMenu("&Models")

#        models_interactive_ui_action = self.createaction("&Interactive UI", None, None, 
#                                            None, "Chose a model in a visual form.")
        component_long_term_choices_action = self.createaction(COMP_LONGTERM, self.models.show_long_term_models, None, 
                                            None, None)
        component_fixed_activity_location_choice_generator_action = self.createaction(COMP_FIXEDACTLOCATION, self.models.show_fixed_activity_models, None, 
                                            None, None)
        component_vehicle_ownership_model_action = self.createaction(COMP_VEHOWN, self.models.show_vehicle_ownership_models, None, 
                                            None, None)
        component_fixed_activity_prism_generator_action = self.createaction(COMP_FIXEDACTPRISM, self.models.show_fixed_activity_prism_models, None, 
                                            None, None)
        component_child_daily_status_and_allocation_model_action = self.createaction(COMP_CHILDSTATUS, self.models.show_child_model, None, 
                                            None, None)
        component_adult_daily_status_model_action = self.createaction(COMP_ADULTSTATUS, self.models.show_adult_model, None, 
                                            None, None)
        component_activity_skeleton_reconciliation_system_action = self.createaction(COMP_ACTSKELRECONCILIATION, self.models.show_skeleton_reconciliation_system, None, 
                                            None, None)
        component_activity_travel_pattern_simulator_action = self.createaction(COMP_ACTTRAVSIMULATOR, self.models.show_activity_travel_pattern_simulator, None, 
                                            None, None)
        component_activity_travel_reconciliation_system_action = self.createaction(COMP_ACTTRAVRECONCILIATION, self.models.show_travel_reconciliation_system, None, 
                                            None, None)
#        component_time_use_utility_calculator_action = self.createaction(COMP_TIMEUSEUTILITY, None, None, 
#                                            None, None)

        modelsComponentSubMenu = self.models_menu.addMenu("&Component")
        modelsComponentSubMenu.setIcon(QIcon("./images/component.png"))
#        self.addActions(self.models_menu, (models_interactive_ui_action, ))
        self.addActions(modelsComponentSubMenu, (component_long_term_choices_action, component_fixed_activity_location_choice_generator_action,
                                                      component_vehicle_ownership_model_action, component_fixed_activity_prism_generator_action,
                                                       component_child_daily_status_and_allocation_model_action, component_adult_daily_status_model_action,
                                                      component_activity_skeleton_reconciliation_system_action,component_activity_travel_pattern_simulator_action,
                                                      component_activity_travel_reconciliation_system_action))#,component_time_use_utility_calculator_action))

    # Defining Data

        
        self.data_menu = self.menuBar().addMenu("&Data")
#        data_import_action = self.createaction("Import data", None, None,
#                                            "import", "Import data.")
        importSubMenu = self.data_menu.addMenu("Import data")
        importSubMenu.setIcon(QIcon("./images/import.png"))
        import_shapefile = self.createaction("Import spatial data (.shp)", self.importshape, None, 
                                    None, None)
        import_nhts = self.createaction("Import NHTS (.csv)", self.importnhts, None, 
                                    None, None)
        self.addActions(importSubMenu, (import_shapefile,import_nhts))
        
        data_export_action = self.createaction("Export data", None, None,
                                            "export", "Export data.")
        data_dataconfig_action = self.createaction("Database Configuration", self.databaseconfiguration, None,
                                                 "datasource", "Database Configuration", False, True)
        self.addActions(self.data_menu, (data_export_action,data_dataconfig_action,))


    # Defining Display
#        self.display_menu = self.menuBar().addMenu("D&isplay")
#        display_zoom_in_action = self.createaction("Zoom &In",None,None,
#                                               "viewmag+", "Zoom in.")
#        display_zoom_out_action = self.createaction("Zoom &Out",None,None,
#                                               "viewmag-", "Zoom out.")
#        self.addActions(self.display_menu, (display_zoom_in_action,display_zoom_out_action,))

    # Defining Run
        self.run_menu = self.menuBar().addMenu("&Run")
        run_simulation_action = self.createaction("&Simulation", self.run_simulation, None,
                                            "run", "Implement the model.", False, True)
#        setting_preference_action = self.createaction("&Preference", None, None,
#                                            "preferences", "Make a configuration.")
#        self.addActions(self.run_menu, (setting_preference_action, ))
        self.addActions(self.run_menu, (run_simulation_action, ))

    # Defining Results
        self.result_menu = self.menuBar().addMenu("R&esults")
        activity_pattern_action = self.createaction("Travel or Activity Characteristics", self.results_schedules, None,
                                            "plot", "Show travel or activity characteristics", False, True)
        person_schedule_action = self.createaction("Profile of Activity Travel Pattern", self.results_person, None,
                                                  "schedule", "Show profile of activity travel pattern in persons or households", False, True)
        kml_tirps_action = self.createaction("Travel or Activity Characteristics in KML", self.create_kml, None,
                                                  "earth", "Show travel characteristics", False, True)
        export_output = self.createaction("Export Output (.xls)", self.exportoutput, None, 
                                    "excel","Produce the basic OpenAmos or NHTS results as MS Excel", False, True)
        self.addActions(self.result_menu, (activity_pattern_action,person_schedule_action,kml_tirps_action,export_output, ))

    # Defining help
        self.help_menu = self.menuBar().addMenu("&Help")
        help_about_action = self.createaction("&About OpenAMOS", None, None,
                                            "help", "Display software information.")
        help_documentation_action = self.createaction("&Documentation", None, None,
                                            "documentation", "Quick reference for important parameters.")
        self.addActions(self.help_menu, (help_documentation_action,None,help_about_action,  ))
 
# Defining toolbar
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.setObjectName("FileToolBar")
#        self.addActions(self.fileToolBar, (project_new_action, project_open_action,
#                                           project_save_action, display_zoom_in_action,
#                                           display_zoom_out_action,))
        self.addActions(self.fileToolBar, (project_new_action, project_open_action,
                                           project_save_action,))


    def getup(self):
        if self.proconfig != None:
            self.model_management.moveup()
        
    def getdown(self):
        if self.proconfig != None:
            self.model_management.movedown()
        
# Define Action
    def createaction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, disabled = None, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon("./images/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        if disabled:
            action.setDisabled(True)

        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

# Show flowcharts from model management tree widget
    def showflowchart(self,selitem,col):
#        if selitem.text(col) == COMP_LONGTERM:
#            self.models.show_long_term_models()
#        if selitem.text(col) == COMP_FIXEDACTLOCATION:
#            self.models.show_fixed_activity_models()
#        if selitem.text(col) == COMP_VEHOWN:
#            self.models.show_vehicle_ownership_models()
#        if selitem.text(col) == COMP_FIXEDACTPRISM:
#            self.models.show_fixed_activity_prism_models()
#        if selitem.text(col) == COMP_CHILDSTATUS:
#            self.models.show_child_model()
#        if selitem.text(col) == COMP_ADULTSTATUS:
#            self.models.show_adult_model()
#        if selitem.text(col) == COMP_ACTSKELRECONCILIATION:
#            self.models.show_skeleton_reconciliation_system()
#        if selitem.text(col) == COMP_ACTTRAVSIMULATOR:
#            self.models.show_activity_travel_pattern_simulator()
#        if selitem.text(col) == COMP_ACTTRAVRECONCILIATION:
#            self.models.show_travel_reconciliation_system()
        
        if selitem.text(col) == COMP_LONGTERM:
            self.models.show_long_term_models()
        if selitem.text(col) == COMP_FIXEDACTLOCATION:
            self.models.show_fixed_activity_models()
        if selitem.text(col) == COMPMODEL_NUMVEHS or selitem.text(col) == COMPMODEL_NUMTYPES:
            self.models.show_vehicle_ownership_models()
        if selitem.text(col) == COMPMODEL_WRKEPISODES or selitem.text(col) == COMPMODEL_DAYSTART or \
            selitem.text(col) == COMPMODEL_DAYEND or selitem.text(col) == COMPMODEL_1WEPISODE or \
            selitem.text(col) == COMPMODEL_2WEPISODE1 or selitem.text(col) == COMPMODEL_2WEPISODE2 or \
            selitem.text(col) == COMPMODEL_PRESCHEPISODES or selitem.text(col) == COMPMODEL_SCHEPISODES:
            self.models.show_fixed_activity_prism_models()
        if selitem.text(col) == COMPMODEL_AFTSCHACTIVITY: #selitem.text(col) == COMPMODEL_SCHSTATUS or selitem.text(col) == COMPMODEL_CHIDDEPEND or selitem.text(col) == COMPMODEL_PERATTR:
            #self.models.show_child_model()
            self.models.show_after_school_model()
        if selitem.text(col) == COMPMODEL_WRKDAILYSTATUS or selitem.text(col) == COMPMODEL_PERATTR:
            self.models.show_child_status_model()
        if selitem.text(col) == COMP_ACTSKELRECONCILIATION or selitem.text(col) == COMPMODEL_RECONCILENDADJ:
            self.models.show_skeleton_reconciliation_system()
        if selitem.text(col) == COMP_ACTTRAVSIMULATOR or selitem.text(col) == COMPMODEL_NONMANDATORY:
            self.models.show_activity_travel_pattern_simulator()
        if selitem.text(col) == COMPMODEL_RECONCILSTRTADJ: #COMP_ACTTRAVRECONCILIATION:
            self.models.show_travel_reconciliation_system()
            
        if selitem.text(col) == COMPMODEL_SCHEPISODES:
            self.models.show_work_status_model()


# Call file functions
    def projectnew(self):
        project_new = NewProject()
        project_new.exec_()
        if project_new.configtree != None:
            if self.proconfig <> None:
                Temp = self.model_management.currentItem()
                if Temp <> None:
                    Temp.setSelected(False)
                self.proconfig = None
#                self.models = None
#                self.centralwidget = None
#                self.centralwidget = QWidget()
#                self.centralwidget.setObjectName("centralwidget")        
#                self.centralwidget.setFixedSize(1140, 1200)
#                self.centralwidgetscroll.setWidget(self.centralwidget)
#                self.models = Models(self.centralwidget)
                self.models.show_clear_widget()

        
            self.proconfig = ConfigObject(configtree=project_new.configtree)
            self.checkProject()
            self.data_menu.actions()[2].setEnabled(True)
            self.run_menu.actions()[0].setEnabled(True)
            self.result_menu.actions()[0].setEnabled(True)
            self.result_menu.actions()[1].setEnabled(True)
            self.result_menu.actions()[2].setEnabled(True)
            self.result_menu.actions()[3].setEnabled(True)



    def projectopen(self):
        if self.proconfig <> None:
            reply = QMessageBox.warning(self, "Save Existing Project...",
                                        QString("""Would you like to save the project?"""), 
                                        QMessageBox.Yes| QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.proconfig.write()
            
        self.project_open = OpenProject()
#        print self.project_open.file
        if self.project_open.file != '':
            Temp = self.model_management.currentItem()
            if Temp <> None:
                Temp.setSelected(False)
            self.proconfig = None
#            self.models = None
#            self.centralwidget = None
#            self.centralwidget = QWidget()
#            self.centralwidget.setObjectName("centralwidget")        
#            self.centralwidget.setFixedSize(1140, 1200)
#            self.centralwidgetscroll.setWidget(self.centralwidget)
#            self.models = Models(self.centralwidget)
            self.models.show_clear_widget()

            
            self.proconfig = ConfigObject(configfileloc=str(self.project_open.file))
            self.checkProject()
            self.data_menu.actions()[2].setEnabled(True)
            self.run_menu.actions()[0].setEnabled(True)
            self.result_menu.actions()[0].setEnabled(True)
            self.result_menu.actions()[1].setEnabled(True)
            self.result_menu.actions()[2].setEnabled(True)
            self.result_menu.actions()[3].setEnabled(True)


            

    def projectsave(self):
#        self.proconfig.write()
        self.proconfig.saveconfig()



    def projectSaveAs(self):
        file = QFileDialog.getSaveFileName(self, QString("Save As..."), 
                                                             "%s" %self.proconfig.getConfigElement(PROJECT_HOME), 
                                                             "XML File (*.xml)")
        
#        fileparse = re.split("[/.]", file)
#        location = ""
#        for i in range(len(file)-3):
#            location = location + file[i] + '/'
#        location =  location + file[len(file)-3]
#            
#        filename = fileparse[-2]
        if not file.isEmpty():
            reply = QMessageBox.warning(self, "Save Existing Project As...",
                                        QString("""Would you like to continue?"""), 
                                        QMessageBox.Yes| QMessageBox.No)
            if reply == QMessageBox.Yes:
#                print "%s"%(filename)
                elt = self.proconfig.getConfigElt(PROJECT)
                projname = str(elt.get(PROJECT_NAME))
                self.proconfig.fileloc = file
                self.proconfig.saveconfig()
                self.setWindowTitle("OpenAMOS: Version-1.0 (%s)" %projname)
                
#                self.project.filename = filename
#                self.project.save()
#                self.setWindowTitle("OpenAMOS: Version-1.0 (%s)" %self.project.name)

    
    def projectClose(self):
        self.proconfig = None
        self.checkProject()
        self.setWindowTitle("OpenAMOS: Version-1.0")
        self.run_menu.actions()[0].setDisabled(True)
        self.data_menu.actions()[2].setDisabled(True)
        self.result_menu.actions()[0].setDisabled(True)
        self.result_menu.actions()[1].setDisabled(True)
        self.result_menu.actions()[2].setDisabled(True)
        self.result_menu.actions()[3].setDisabled(True)

        

    def projectQuit(self):
        reply = QMessageBox.question(None, 'Quit', "Are you sure to quit?",
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.proconfig.write()
            self.close()
            
    def checkProject(self):
        actpro = bool(self.proconfig)
        self.model_management.clear()
        if actpro:
            self.setWindowTitle("OpenAMOS: Version-1.0 (%s)" %self.proconfig.getConfigElement(PROJECT,NAME))
            self.model_management.setConfigObject(self.proconfig)
            self.models.setConfigObject(self.proconfig)
        self.centralwidget.setEnabled(actpro)

    def importshape(self):
        if self.proconfig <> None:
            import_shape = Read_Shape(self.proconfig)
            import_shape.exec_()
            
    def importnhts(self):
        if self.proconfig <> None:
            import_nhts = Import_NHTS(self.proconfig)
            import_nhts.exec_()
            
    def exportoutput(self):
        if self.proconfig <> None:
            export_output = Export_Outputs(self.proconfig)
            export_output.exec_()
            
    def databaseconfiguration(self):
        if self.proconfig <> None:
            project_database = DatabaseConfig(self.proconfig)
            project_database.exec_()
    
    def results_schedules(self):
        if self.proconfig <> None:
            show_plot = MakeResultPlot(self.proconfig) #MakePlot(self.proconfig,"schedule_final_r")
            show_plot.exec_()
            
    def create_kml(self):
        if self.proconfig <> None:
            show_plot = kml_trips(self.proconfig)
            show_plot.exec_()
            
    def results_person(self):
        if self.proconfig <> None:
            show_plot = MakeSchedPlot(self.proconfig)
            show_plot.exec_()
            
    def run_simulation(self):
        simdiag = SimDialog(self.proconfig)  
        simdiag.exec_() 
        
        self.models.show_clear_widget() 
        self.proconfig = ConfigObject(configfileloc=str(self.project_open.file))
        self.checkProject()
            
#        fileloc = self.proconfig.getConfigElement(PROJECT,LOCATION)
#        pname = self.proconfig.getConfigElement(PROJECT,NAME)
#        """This accepts only one argument which is the location of the configuration """\
#        """file. e.g. /home/config.xml (linux machine) """\
#        """or c:/testproject/config.xml (windows machine)"""
#
#        simulationManagerObject = SimulationManager(fileLoc = "%s/%s.xml" %(fileloc,pname))
#        simulationManagerObject.setup_databaseConnection()
#        simulationManagerObject.setup_cacheDatabase('w')
#        simulationManagerObject.setup_location_information()
#        simulationManagerObject.setup_tod_skims()
#        simulationManagerObject.parse_config()
#        simulationManagerObject.clean_database_tables()
#        simulationManagerObject.run_components()
#        simulationManagerObject.close_connections()

#        if fileloc <> None and fileloc <> "" and pname <> None and pname <> "":
#            componentManager = ComponentManager(fileLoc = "%s/%s.xml" %(fileloc,pname))
#            componentManager.establish_databaseConnection()
#            componentManager.establish_cacheDatabase(fileloc, 'w')
#            componentManager.run_components()
#            componentManager.db.close()
#        else:
#            print "Something Wrong"




def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SimTRAVEL")
    form = MainWindow()
    form.show()
    app.exec_()

if __name__=="__main__":
    main()
