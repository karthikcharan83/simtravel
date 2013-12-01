'''
Created on Jun 8, 2010

@author: bsana
'''

from lxml import etree

from openamos.gui.env import *
import os
from copy import deepcopy

class ConfigObject(object):
    '''
    classdocs
    '''

    def __init__(self,configfileloc = None, configtree = None):
        self.fileloc = configfileloc
        if configfileloc:
            parser = etree.XMLParser(remove_blank_text=True)
            self.protree = etree.parse(configfileloc,parser)
        elif configtree:
            self.protree = configtree
            
        # Approach to the default configuration file
        parser = etree.XMLParser(remove_blank_text=True)
        #pathDef = os.path.realpath('/workspace/simtravel/openamos/configs/mag_zone/config_after_malta.xml')
        pathDef = str(os.getcwd()).replace('gui', 'configs/mag_zone/config_before_malta.xml')
        self.default = etree.parse(pathDef,parser)


    def getConfigElement(self, elt, prop='text' ):
        element = self.protree.find(elt)
        if prop == 'text':
            return self.protree.findtext(elt)
        else:
            return element.get(prop) 
         
    def getConfigElt(self, elt):
        element = self.protree.find(elt)
        return element

    def modelSpecInConfig(self,modelkey):
        if modelkey not in MODELMAP.keys():
            print "Model not found in the Map"
            return None
        #print "Model found in the Map"
        mapvals = MODELMAP[modelkey]
        compname = mapvals[0]
        modelname = mapvals[1]
        #print compname, modelname
        modelnum = 0
        if len(mapvals) == 3:
            modelnum = mapvals[2]
        #print modelnum
        compelt = self.protree.find(MODELCONFIG)
        components = [COMP, SUBCOMP]
        for comps in components:
            for comp in compelt.getiterator(comps):
                if compname.lower() == comp.get(NAME).lower():
                    modelcnt = 1
                    for model in comp.getiterator(MODEL): 
                        if modelname.lower() == model.get(NAME).lower():
                            if modelnum == 0:
                                return model
                            else:
                                if modelcnt ==  modelnum:
                                    return model
                                else:
                                    modelcnt += 1 
                                
    def modelSpecInDefault(self,modelkey):
        print "Model Key: %s" %(modelkey)
        if modelkey not in MODELMAP.keys():
            print "Model not found in the Map"
            return None
        #print "Model found in the Map"
        mapvals = MODELMAP[modelkey]
        compname = mapvals[0]
        modelname = mapvals[1]
        #print compname, modelname
        modelnum = 0
        if len(mapvals) == 3:
            modelnum = mapvals[2]
        #print modelnum
        compelt = self.default.find(MODELCONFIG)
        components = [COMP, SUBCOMP]
        for comps in components:
            for comp in compelt.getiterator(comps):
                if compname.lower() == comp.get(NAME).lower():
                    modelcnt = 1
                    for model in comp.getiterator(MODEL): 
                        if modelname.lower() == model.get(NAME).lower():
                            if modelnum == 0:
                                return model
                            else:
                                if modelcnt ==  modelnum:
                                    return model
                                else:
                                    modelcnt += 1 


    def getProjects(self):
        root = self.protree.getroot()
        childs = root.getchildren()
        return childs                                


    def getCompSimStatus(self,compname):
        compelt = self.protree.find(MODELCONFIG)
        for comp in compelt.getiterator(COMP):
            if compname.lower() == comp.get(NAME).lower():
                completed = comp.get('completed').lower() == 'true'
                skip = comp.get('skip').lower() == 'true'
                return [completed,skip]


    def getComponent(self,compname):
        compelt = self.protree.find(MODELCONFIG)
        for comp in compelt.getiterator(COMP):
            if compname.lower() == comp.get(NAME).lower():
                return comp
        return None

    def getCompIndex(self,index):
        compelt = self.protree.find(MODELCONFIG)
        comp = compelt.getchildren()
        child = comp[index]
        return child
    
    def getComponents(self):
        compelt = self.protree.find(MODELCONFIG)
        compelts = compelt.getiterator(COMP)
        return compelts
    
    def getModelConfigChildren(self):
        compelt = self.protree.find(MODELCONFIG)
        compelts = compelt.getchildren()
        return compelts
    
    def getElement(self,index):
        father = self.protree.find(MODELCONFIG)
        childs = father.getchildren()
        child = childs[index[0]]
        
        for i in range(len(index)-1):
            father = child
            childs = father.getchildren()
#            index[i+1] = index[i+1]-1
            child = childs[index[i+1]]
            
        return child
    
    def getElements(self,key):
        compelt = self.protree.find(MODELCONFIG)
        elements = []
        for comp in compelt.getiterator(key):

            elements.append(comp)
            
        return elements
    
    def getDElements(self,key):
        compelt = self.default.find(MODELCONFIG)
        elements = []
        for comp in compelt.getiterator(key):

            elements.append(comp)
            
        return elements

    def removeElement(self,index):
        father = self.protree.find(MODELCONFIG)
        childs = father.getchildren()
        child = childs[index[0]]
        
        for i in range(len(index)-1):
            father = child
            childs = father.getchildren()
#            index[i+1] = index[i+1]-1
            child = childs[index[i+1]]
            
        father.remove(child)
    
    def moveup(self,index):
        father = self.protree.find(MODELCONFIG)
        childs = father.getchildren()
        child = childs[index[0]]
        count = len(index)
        
        for i in range(count-1):
            father = child
            childs = father.getchildren()
#            index[i+1] = index[i+1]-1
            child = childs[index[i+1]]

        father.remove(child)
        father.insert(index[count-1]-1, child)
        
        
    def movedown(self,index):
        father = self.protree.find(MODELCONFIG)
        childs = father.getchildren()
        child = childs[index[0]]
        count = len(index)
        
        for i in range(count-1):
            father = child
            childs = father.getchildren()
#            index[i+1] = index[i+1]-1
            child = childs[index[i+1]]

        father.remove(child)
        father.insert(index[count-1]+1, child)

            
    def addModelElement(self,modelelt):
        compname = self.getCompName(modelelt.get(NAME))
        modelconfigelt = self.protree.find(MODELCONFIG)
        if modelconfigelt != None:
            compfound = False
            for comp in modelconfigelt.getiterator(COMP):
                if compname == comp.get(NAME):
                    compfound = True
                    modelidx = 0
                    modelreplaced = False
                    for model in comp.getiterator(MODEL):
                        if modelelt.get(NAME) == model.get(NAME):
                            comp.remove(model)
                            comp.insert(modelidx,modelelt)
                            modelreplaced = True
                        modelidx = modelidx + 1
                    if not modelreplaced:
                        comp.append(modelelt)
            if not compfound:
                compelt = etree.SubElement(modelconfigelt,COMP)
                compelt.set(NAME,compname)
                compelt.append(modelelt) 
        else:
            proconfigelt = self.protree.getroot()  
            modelconfigelt = etree.SubElement(proconfigelt,MODELCONFIG) 
            compelt = etree.SubElement(modelconfigelt,COMP)
            compelt.set(NAME,compname)
            compelt.append(modelelt)  
    
    
    def getCompName(self,modelkey):
        mapvals = MODELMAP[modelkey]
        compkey = mapvals[0]
        return compkey

            
            
#    def getCompName(self,modelkey):
#        for compkey in COMPMODELMAP.keys():
#            modelist = COMPMODELMAP[compkey]
#            if modelkey in modelist:
#                return compkey
    
    def write(self):
        projecthome = self.getConfigElement(PROJECT,PROJECT_HOME)
        projectname = self.getConfigElement(PROJECT,PROJECT_NAME)
        configpath = self.getConfigElement(PROJECT,LOCATION)
        if not os.path.exists(configpath):
            os.mkdir(configpath)
        configfileloc = projecthome + '/' + projectname + '.xml'

        print configfileloc
        configfile = open(configfileloc, 'w')
        self.protree.write(configfile, pretty_print=True)
        configfile.close()
        
    def saveconfig(self):
        configfile = open(self.fileloc, 'w')
        self.protree.write(configfile, pretty_print=True)
        configfile.close()
        
    def comparemodels(self,modelkey):
        previous = self.modelSpecInDefault(modelkey)
        current = self.modelSpecInConfig(modelkey)

        if current == None or previous == None:
            return True

        
        #Model name="EndTime" formulation='Regression' type="Linear" vertex='end' threshold='755' seed="1"
        temp1 = str(previous.get(NAME))
        temp2 = str(current.get(NAME))
        if temp1 <> temp2:
            return False
        
        temp1 = str(previous.get(FORMULATION))
        temp2 = str(current.get(FORMULATION))
        if temp1 <> temp2:
            return False
        
        temp1 = str(previous.get(MODELTYPE))
        temp2 = str(current.get(MODELTYPE))
        if temp1 <> temp2:
            return False
        
        temp1 = str(previous.get(VERTEX))
        temp2 = str(current.get(VERTEX))
        if temp1 <> temp2:
            return False
        
        temp1 = str(previous.get(THRESHOLD))
        temp2 = str(current.get(THRESHOLD))
        if temp1 <> temp2:
            return False
        
        temp1 = str(previous.get(SEED))
        temp2 = str(current.get(SEED))
        if temp1 <> temp2:
            return False
        
        pre_var = previous.findall(VARIANCE)
        cur_var = current.findall(VARIANCE)
        if len(pre_var) <> len(cur_var):
            return False
            
        i = 0
        for varelt in pre_var:
            value1 = str(varelt.get(VALUE))
            value2 = str((cur_var[i]).get(VALUE))
            if value1 <> value2:
                return False
            
            type1 = str(varelt.get(MODELTYPE))
            type2 = str((cur_var[i]).get(MODELTYPE))
            if type1 <> type2:
                return False
                
            i = i+1
            
        
        pre_alt = previous.findall(ALTERNATIVE)
        cur_alt = current.findall(ALTERNATIVE)
        if len(pre_alt) <> len(cur_alt):
            return False
            
        i = 0
        for altelt in pre_alt:
            id1 = str(altelt.get(ID))
            id2 = str((cur_alt[i]).get(ID))
            if id1 <> id2:
                return False
            
            value1 = str(altelt.get(VALUE))
            value2 = str((cur_alt[i]).get(VALUE))
            if value1 <> value2:
                return False
            
            thres1 = str(altelt.get(THRESHOLD))
            thres2 = str((cur_alt[i]).get(THRESHOLD))
            if thres1 <> thres2:
                return False
            
            p_vari = altelt.findall(VARIABLE)
            c_vari = (cur_alt[i]).findall(VARIABLE)
            if len(p_vari) <> len(c_vari):
                return False
            
            j = 0
            for varielt in p_vari:
                table1 = str(varielt.get(TABLE))
                table2 = str((c_vari[j]).get(TABLE))
                if table1 <> table2:
                    return False
                
                var1 = str(varielt.get(COLUMN))
                var2 = str((c_vari[j]).get(COLUMN))
                if var1 <> var2:
                    return False
                
                coeff1 = str(varielt.get(COEFF))
                coeff2 = str((c_vari[j]).get(COEFF))
                if coeff1 <> coeff2:
                    return False
                j = j+1
            
            i = i+1
            
            
        pre_vari = previous.findall(VARIABLE)
        cur_vari = current.findall(VARIABLE)
        if len(pre_vari) <> len(cur_vari):
            return False
            
        i = 0
        for varielt in pre_vari:
            table1 = str(varielt.get(TABLE))
            table2 = str((cur_vari[i]).get(TABLE))
            if table1 <> table2:
                return False
            
            var1 = str(varielt.get(COLUMN))
            var2 = str((cur_vari[i]).get(COLUMN))
            if var1 <> var2:
                return False
            
            coeff1 = str(varielt.get(COEFF))
            coeff2 = str((cur_vari[i]).get(COEFF))
            if coeff1 <> coeff2:
                return False
            i = i+1
            
        return True
