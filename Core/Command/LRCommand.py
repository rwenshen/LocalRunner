from ..LRObject import LRObjectMetaClass, LRObject
from .CommandArg.LRCArg import LRCArg
from ..LROFactory import LROFactory

class LRCommandMetaClass(LRObjectMetaClass):

    @staticmethod
    def getBaseClassName():
        return 'LRCommand'
    @staticmethod
    def isNeedInstance():
        return True

    def __new__(cls, name, bases, attrs):
        return LRCommandMetaClass.newImple(cls, name, bases, attrs)

class LRCommand(LRObject, metaclass=LRCommandMetaClass):
    
    def __init__(self):
        self.__myArgs=[]
        self.initArgs()

    @property
    def cmdName(self):
        return self.__class__.__name__

    def iterArgs(self):
        for arg in self.__myArgs:
            yield arg

    def addArg(self, argName:str):
        assert LROFactory.contain('LRCArg', argName), 'Argument "{}" is not defined.'.format(argName)
        self.__myArgs.append(argName)
    def initArgs(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError