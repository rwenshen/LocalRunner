from enum import Enum, unique

from .LRObjectMeta import LRObjectMetaClass
from .LRPropertyDefBase import LRPropertyDefBase

class LRObject(metaclass=LRObjectMetaClass):
    '''
    Base class for all object in LocalRunner project.
    Derived classed need to implement property "myPropertyDefines"
    Example
    class Sub(LRObject):
        @lrproperty('p1', int)
        @lrproperty_lro('p2', LRObjectSub)
        @lrproperty_list(lrproperty('p3', str))
        def registerPropertyDefs(self):
            pass
    '''
    
    cTypePropertyName = '__type'

    def __init__(self, saveData={}, parent=None):
        self.__properties = []
        self.registerPropertyDefs()
        self.__data = {}
        for pDef in self.__properties:
            self.__data[pDef.myName] = pDef.fromSaveData(saveData.get(pDef.myName))
        self.__parent = parent

    def registerPropertyDefs(self):
        raise NotImplementedError
    def addPropertyDef(self, propertyDef):
        self.__properties.append(propertyDef)

    def __getitem__(self, key):
        return self.__data[key]
    def __setitem__(self, key, value):
        self.__data[key] = value
    def __iter__(self):
        for pDef in self.__properties:
            yield pDef.myName
    def __contains__(self, name):
        for pDef in self.__properties:
            if pDef.myName == name:
                return True
        return False

    @property
    def myParent(self):
        return self.__parent

    @property
    def mySaveData(self):
        saveData = {LRObject.cTypePropertyName:str(type(self))}
        for pDef in self.__properties:
            saveData[pDef.myName] = pDef.toSaveData(self[pDef.myName])
        return saveData
