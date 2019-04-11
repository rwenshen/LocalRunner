from ..Core.Command import *

class ErrorArg(LRCArg):
    #@LRCArg.argType(1)
    #@LRCArg.argType(None)    
    #@LRCArg.argChoices()
    #@LRCArg.argType(int)
    @LRCArg.argChoices('x64', 'x1', 'ps4')
    #@LRCArg.argDefault(1)
    #@LRCArg.argDefault('1')
    def defineArg(self):
        pass

class PlatformArg(LRCArg):
    '''The platform used.'''
    @LRCArg.argChoices('x64', 'x1', 'ps4')
    @LRCArg.argDefault('x64')
    def defineArg(self):
        self.__default = 'x64'

class IncredibuildArg(LRCArg):
    '''Using incredibuild?'''
    @LRCArg.argType(bool)
    def defineArg(self):
        pass

class Command1(LRCommand):
    def initArgs(self):
        self.addArg('PlatformArg')

class Command2(LRCommand):
    def initArgs(self):
        self.addArg('PlatformArg')
        self.addArg('IncredibuildArg')