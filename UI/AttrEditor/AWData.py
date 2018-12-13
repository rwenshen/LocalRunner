class AWData:
    def __init__(self, obj, name:str):
        self.myIsDict = False
        
        if isinstance(obj, dict):
            self.myIsDict = name in obj
            assert self.myIsDict, 'Key {} is not in dict!'.format(name)
        elif '__dict__' in dir(obj):
            assert name in vars(obj), 'Attribut {} is not in object instance!'.format(name)
        else:
            raise TypeError('Only dict and object with __dict__ are supported. The type {} is not a supported!'.format(type(obj)))

        self.myObj = obj
        self.myName = name
        self.myType = type(self.data)

    def isType(self, _type):
        return isinstance(self.data, _type)

    @property
    def data(self):
        if self.myIsDict:
            return self.myObj[self.myName]
        else:
            return getattr(self.myObj, self.myName)

    @data.setter
    def data(self, value):
        if not isinstance(value, self.myType):
            raise TypeError('The value "{}" with type "{}" dose NOT match data type {}!'.format(str(value), type(value), self.myType))
        
        if self.myIsDict:
            self.myObj[self.myName] = value
        else:
            setattr(self.myObj, self.myName, value)
