from ..Core import *
from ..core.command import *

############################################################
# Core
############################################################
# Duplicated objects
class PathArg(LRCArg):
    '''A path dup'''
    def initialize(self):
        pass

# Unique class
class DupEnvironments(LREnvironments):
    @LREnvironments.setEnv(PROJ_DESC='Test description')
    @LREnvironments.setEnv(SHELL='cmd')
    def initialize(self):
        pass


############################################################
# Arguments
############################################################
class Path(LRCArg):
    '''A path 2'''
    pass

class TestArg(LRCArg):
    '''A test 2'''
    pass

class ErrorArg(LRCArg):
    @LRCArg.argType(1)
    @LRCArg.argDefault(1)
    @LRCArg.argChoices('x', 'x', 1, 1, 'z', 7.5)
    def initialize(self):
        pass

############################################################
# Commands
############################################################
# Unknown Commands
class cerror1(LRCommand):
    @LRCommand.addArg('XXX')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Error')
    def initialize(self):
        pass

# non arguments cmd
class nonArgCmd(LRCommand):
    pass

# cmd using wrong arg in execution
class errorUsingArgCmd(LRCommand):
    @LRCommand.addArg('EnumTest')
    @LRCommand.addArg('Platform')
    @LRCommand.addArg('Incredibuild')
    def initialize(self):
        pass
    def execute(self, args):
        # non-exist args
        args.NotExist = 1
        print(args.NotExist)
        # error type
        args.Incredibuild = 1
        # not in choices list
        args.Platform = '1'
        return 1

# for compound cmd
class errorCompoundCmd(LRCompoundCommand):
    @LRCompoundCommand.addSubCmd('sub1', cmdName='test_enum', Platform='x1')
    @LRCompoundCommand.addSubCmd('sub1', cmdName='nonArgCmd')
    @LRCompoundCommand.addSubCmd('error1', cmdName='nonex')
    @LRCompoundCommand.addSubCmd('error2', cmdName='test_enum', nonArg=1)
    @LRCompoundCommand.addSubCmd('error3', cmdName='test_shell', Platform=1)
    @LRCompoundCommand.addSubCmd('error4', cmdName='test_shell', Platform='Error')
    def initialize(self):
        pass

class emptyCompoundCmd(LRCompoundCommand):
    pass

class errorSelectionCmd(LRSelectionCommand):
    @LRCompoundCommand.addSubCmd('sub1', cmdName='test_enum')
    def initialize(self):
        pass