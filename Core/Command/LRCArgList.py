from .LRCArg import LRCArg 

class LRCArgList:

    def __getattr__(self, name):
        if name in self.__myDict:
            return self.__myDict[name]
        raise AttributeError("Argument '%s' is not existent."%(name))
    def __setattr__(self, name, value):
        if name.startswith('_LRCArgList__'):
            object.__setattr__(self, name, value)
        else:
            self.__setArg(name, value)

    def __init__(self, cmd):
        self.__myDict = {}
        for arg in cmd.iterArgs():
            self.__myDict[arg.myName] = arg.myDefault

    def __setArg(self, name, value):
        arg = LRCArg.sGetArg(name)
        # check type
        if value is not None and not isinstance(value, arg.myType):
            raise AttributeError('Type of value "{}" is not correct. "{}" is need.'.format(str(value), str(arg.myType)))
        # check choice
        if arg.myChoices is not None and value not in arg.myChoices:
            raise AttributeError('Value "{}" is not in choices list'.format(str(value)))
        self.__myDict[name] = value
