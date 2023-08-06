import uuid

class CircuitAnnealing:
    
    # CONSTRUCTOR
    def __init__(self):
        self.__parameters = []
        self.__auxData = []
        self.__classes = []
        self.__variables = []
        self.__rules = []

        self.__circuitBody = {
            'Parameters': self.__parameters,
            'AuxData': self.__auxData,
            'Classes': self.__classes,
            'Variables': self.__variables,
            'Rules': self.__rules
        }
    

    # GETTERS
    def getCircuitBody(self):
        return self.__circuitBody


    # METHODS
    def addParameter(self, parameter):
        parameter = {
            'uiID': parameter.getUIID(),
            'Name': parameter.getName(),
            'Value': parameter.getValue()
        }

        self.__parameters.append(parameter)

        return parameter


    def addAuxData(self, auxData):
        auxData = {
            'uiID': auxData.getUIID(),
            'Name': auxData.getName(),
            'Value': auxData.getValue()
        }

        self.__auxData.append(auxData)

        return auxData


    def addClass(self, cls):
        cls = {
            'Properties': cls.getProperties(),
            'uiID': cls.getUIID(),
            'Name': cls.getName(),
            'NumberOfVars': cls.getNumberOfVars(),
            'Description': cls.getDescription()
        }

        self.__classes.append(cls)

        return cls


    def addVariable(self, variable):
        variable = {
            'Classes': variable.getClasses(),
            'uiID': variable.getUIID(),
            'Name': variable.getName(),
            'Description': variable.getDescription()
        }

        self.__variables.append(variable)

        return variable


    def addRule(self, rule):
        rule = {
            'Expressions': rule.getExpressions(),
            'uiID': rule.getUIID(),
            'Name': rule.getName(),
            'Lambda': rule.getLambda(),
            'Description': rule.getDescription()
        }

        self.__rules.append(rule)

        return rule

    
    # INNER CLASSES
    class Parameter:

        # CONSTRUCTOR
        def __init__(self, name, value):
            self.__uiID = str(uuid.uuid4())
            self.__name = name
            self.__value = str(value)
        
        # GETTERS
        def getUIID(self):
            return self.__uiID
        
        def getName(self):
            return self.__name
        
        def getValue(self):
            return self.__value
    

    class AuxData:

        # CONSTRUCTOR
        def __init__(self, name, value):
            self.__uiID = str(uuid.uuid4())
            self.__name = name
            self.__value = str(value)
        
        # GETTERS
        def getUIID(self):
            return self.__uiID
        
        def getName(self):
            return self.__name
        
        def getValue(self):
            return self.__value
    

    class Class:

        # CONSTRUCTOR
        def __init__(self, name, numberOfVars, description = ''):
            self.__properties = []
            self.__uiID = str(uuid.uuid4())
            self.__name = name
            self.__numberOfVars = str(numberOfVars)
            self.__description = description

        # GETTERS
        def getProperties(self):
            return self.__properties

        def getUIID(self):
            return self.__uiID
        
        def getName(self):
            return self.__name
        
        def getNumberOfVars(self):
            return self.__numberOfVars
        
        def getDescription(self):
            return self.__description
        
        # METHODS
        def addProperty(self, name, values):
            if len(values) == int(self.__numberOfVars): # number of values and number of vars are the same
                self.__properties.append(
                    {
                        'uiID': str(uuid.uuid4()),
                        'Name': name,
                        'Values': values
                    }
                )
    

    class Variable:

        # CONSTRUCTOR
        def __init__(self, name, classes, description = ''):
            classList = []

            for cls in classes:
                classList.append(cls.getUIID())

            self.__classes = classList
            self.__uiID = str(uuid.uuid4())
            self.__name = name
            self.__description = description
    
        # GETTERS
        def getClasses(self):
            return self.__classes

        def getUIID(self):
            return self.__uiID
        
        def getName(self):
            return self.__name
        
        def getDescription(self):
            return self.__description
    

    class Rule:

        # CONSTRUCTOR
        def __init__(self, name, lambdaValue, description = ''):
            self.__expressions = []
            self.__uiID = str(uuid.uuid4())
            self.__name = name
            self.__lambda = str(lambdaValue)
            self.__description = description

        # GETTERS
        def getExpressions(self):
            return self.__expressions

        def getUIID(self):
            return self.__uiID
        
        def getName(self):
            return self.__name
        
        def getLambda(self):
            return self.__lambda
        
        def getDescription(self):
            return self.__description