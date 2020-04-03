from .. import *
from .arg import *
from . import base_commands


class LRCommandLogger(LRLogger):
    def getLogger(self):
        return LRLogger.cGetLogger('command')

    def log(self, func, msg: str, *args, **kwargs):
        func(msg, *args, **kwargs)
        indent = '\t'
        func(f'{indent}in command {self.__class__}.')


class LRCommandMetaClass(LRObjectMetaClass):
    baseClassName = 'LRCommand'
    extraInterfaces = (LRCommandLogger,)
    isSingleton = True


class LRCommand(LRObject, metaclass=LRCommandMetaClass):

    @staticmethod
    def sGetCmdList():
        return LROFactory.sFindList(LRCommand.__name__)

    @staticmethod
    def sGetCmd(cmdName: str):
        cmd = LROFactory.sFind(LRCommand.__name__, cmdName)
        assert cmd is not None,\
            f'Unregistered command "{cmdName}", please check the spell or '\
            'whether the command is abstract.'
        return cmd

    @staticmethod
    def sParseCmdArgs(cmdName: str, argList: list):
        cmd = LRCommand.sGetCmd(cmdName)
        return LRCArgParser.parse(cmd, argList)

    @staticmethod
    def sCallCmd(cmdName: str, argList: list):
        args = LRCommand.sParseCmdArgs(cmdName, argList)
        cmd = LRCommand.sGetCmd(cmdName)
        return cmd.doExecution(args)

    def __init__(self):
        self.__myArgs = []
        self.__myDynamicArgs = {}
        self.__myCategories = []
        # call initialize from base classes
        called = []
        for cl in reversed(self.__class__.__mro__):
            if issubclass(cl, LRCommand) and cl.initialize not in called:
                cl.initialize(self)
                called.append(cl.initialize)

        cat = ''
        if len(self.myCategories) > 0:
            cat = '/'.join(self.__myCategories)
            cat += '/'
        self.__myDescription = 'Command: {}{}'.format(
            cat,
            self.__class__.__name__)
        if self.__doc__ is not None:
            self.__myDescription += '\n\t'
            self.__myDescription += self.__doc__

    def appendLindToDescription(self, line: str):
        self.__myDescription += line
        self.__myDescription += '\n'

    @property
    def myName(self):
        return self.__class__.__name__

    @property
    def myDescription(self):
        return self.__myDescription

    @property
    def myCategories(self):
        return self.__myCategories

    def iterArgs(self):
        for argName in self.__myArgs:
            if argName in self.__myDynamicArgs:
                yield self.__myDynamicArgs[argName]
            else:
                yield LRCArg.sGetArg(argName)

    def containArg(self, argName: str):
        return argName in self.__myArgs

    @staticmethod
    def addArg(argName: str):
        def decorator(func):
            def wrapper(self):
                if not LRCArg.sDoesArgExist(argName):
                    self.logError(
                        f'Argument "{argName}" has been registered! Skipped.')
                elif argName in self.__myArgs:
                    self.logWarning(
                        f'Argument "{argName}" is duplicated! Skipped the second one.')
                else:
                    self.__myArgs.append(argName)
                return func(self)
            return wrapper
        return decorator

    @staticmethod
    def addArgDirectly(
            argName: str,
            description: str,
            argType: type=str,
            isPlacement: bool=False,
            choice = None,
            default = None,
            shortName = None):
        def decorator(func):
            def wrapper(self):
                if argName in self.__myArgs:
                    self.logWarning(
                        f'Argument "{argName}" is duplicated! Skipped the second one.')
                else:
                    dynamicArg = LRCArg.sCreateDynamicArg(
                        argName,
                        description=description,
                        argType=argType,
                        isPlacement=isPlacement,
                        choice=choice,
                        default=default,
                        shortName=shortName)
                    if dynamicArg is not None:
                        self.__myDynamicArgs[argName] = dynamicArg
                        self.__myArgs.append(argName)
                return func(self)
            return wrapper
        return decorator

    @staticmethod
    def setCategory(category: str):
        def decorator(func):
            def wrapper(self):
                cat = category.replace('\\', '/')
                self.__myCategories = cat.split('/')
                return func(self)
            return wrapper
        return decorator

    @abstractmethod
    def initialize(self):
        pass

    def printHelp(self, *args):
        LRCArgParser.printHelp(self)

    def doExecution(self, args: LRCArgList):
        self.getLogger().info(
            f'Start execution of command {self.__class__}...')
        self.preExecute(args)
        returnCode = self.execute(args)
        self.postExecute(args, returnCode)
        self.getLogger().info(
            f'Finish execution of command {self.__class__}, with return code: "{returnCode}".')
        if returnCode != 0:
            self.logError(
                f'Command {self.__class__} was exit with code "{returnCode}".')
        return returnCode

    def preExecute(self, args: LRCArgList):
        pass
    
    @abstractmethod
    def execute(self, args: LRCArgList) -> int:
        return 0

    def postExecute(self, args: LRCArgList, returnCode: int):
        pass
