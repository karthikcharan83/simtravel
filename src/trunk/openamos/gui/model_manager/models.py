from long_term_models import *
from fixed_activity_models import *
from vehicle_ownership_models import *
from fixed_activity_prism_models import *
from activity_skeleton_reconciliation_system import *
from activity_travel_reconciliation_system import *
from child_daily_status_and_allocation_model import *
from child_daily_status_model import *
from after_school_model import *
from adult_daily_status_model import *
from activity_travel_pattern_simulator import *

class Models(QWidget):
    def __init__(self, parent = None):
        super(Models, self).__init__(parent)
        # Define a global var named "model_widget" to ues in the each function as a parent widget
        global model_widget
        model_widget = parent


    def show_long_term_models(self):
        self.long_term_models = LongTermModels(model_widget, self.configobject)
        self.long_term_models.show()

    def show_fixed_activity_models(self):
        self.fixed_activity_models = FixedActivityModels(model_widget, self.configobject)
        self.fixed_activity_models.show()

    def show_vehicle_ownership_models(self):
        self.vehicle_ownership_models = VehicleOwnershipModels(model_widget, self.configobject)
        self.vehicle_ownership_models.show()

    def show_fixed_activity_prism_models(self):
        self.fixed_activity_prism_models = FixedActivityPrismModels(model_widget, self.configobject)
        self.fixed_activity_prism_models.show()

    def show_skeleton_reconciliation_system(self):
        self.skeleton_reconciliation_system = Skeleton_Reconciliation_System(model_widget, self.configobject)
        self.skeleton_reconciliation_system.show()

    def show_travel_reconciliation_system(self):
        self.travel_reconciliation_system = Travel_Reconciliation_System(model_widget, self.configobject)
        self.travel_reconciliation_system.show()

    def show_child_model(self):
        self.child_model = Child_Model(model_widget, self.configobject)
        self.child_model.show()

    def show_child_status_model(self):
        self.child_status_model = Child_Status_Model(model_widget, self.configobject)
        self.child_status_model.show()

    def show_after_school_model(self):
        self.after_school_model = After_School(model_widget, self.configobject)
        self.after_school_model.show()

    def show_adult_model(self):
        self.adult_model = Adult_Model(model_widget, self.configobject)
        self.adult_model.show()

    def show_activity_travel_pattern_simulator(self):
        self.activity_travel_pattern_simulator = Activity_Travel_Pattern_Simulator(model_widget, self.configobject)
        self.activity_travel_pattern_simulator.show()

    def setConfigObject(self,co):
        self.configobject = co

    def show_clear_widget(self):
        self.clearWidgets = ClearWidgets(model_widget)
        self.clearWidgets.show()



class ClearWidgets(QWidget):
    def __init__(self, parent=None):
        super(ClearWidgets, self).__init__(parent)

        self.setAutoFillBackground(True)
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()

        Dummy  = QPushButton('', self)
        Dummy.setGeometry(0, size.height() - 4, 1140, 2)
