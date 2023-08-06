from .classes import apiConnection

class QSOAPlatform:
    from .classes import Application
    from .classes import Asset
    from .classes import AssetManagementData
    from .classes import AssetManagementResult
    from .classes import CircuitGates
    from .classes import Context
    from .classes import CircuitFlow
    from .classes import DeviceItem
    from .classes import Execution
    from .classes import FlowItem
    from .classes import QuantumExecutionHistoryEntry
    from .classes import SolutionItem
    from .Exception import (ConfigFileError, Base64Error, AuthenticationError, ExecutionObjectError)

    from pathlib import Path
    from configparser import ConfigParser

    from matplotlib import pyplot as plt
    from prettytable import PrettyTable
    import collections
    import base64
    import time

    # CONSTRUCTOR
    def __init__(self, username: str = None, password: str = None, configFile: bool = False):
        """
        QSOAPlatform object constructor.

        Prerequisites
        ----------
        - User created in QPath.

        Parameters
        ----------
        username : str
            QPath account username to authenticate.
        password : str
            QPath account password to authenticate. (SHA-256)
        
        Prerequisites
        ----------
        - User created in QPath.
        - .qpath file created in home path.

        Parameters
        ----------
        authenticate : str
            True to authenticate using .qpath config file.

        Output
        ----------
        QSOAPlatform obj
        """
        if username and password:
            self.__checkInputTypes(
                ('username', username, (str,)),
                ('password', password, (str,)),
                ('configFile', configFile, (bool,))
            )


        # VARIABLES
        self.environments = {
            'default-environments': {
                'pro': 'https://qsoa.quantumpath.app:8443/api/',
                'lab': 'https://qsoa.quantumsoftt.com:10443/api/'
            },
            'custom-environments': {}
        }

        qpathFile = self.ConfigParser(allow_no_value=True)
        qpathFileExists = qpathFile.read(str(self.Path.home()) + '\.qpath')
        if qpathFileExists:
            self.activeEnvironment = eval(qpathFile.options('active-environment')[0])
        else:
            self.activeEnvironment = ('default-environments', 'pro')

        self.context = None

        # API ENDPOINTS
        self.securityEndpoints = {
            'echoping': 'login/echoping/',
            'echouser': 'login/echouser/',
            'echostatus': 'login/echostatus',
            'authenticate': 'login/authenticate/',
            'authenticateEx': 'login/authenticateEx/'
        }

        self.connectionPoints = {
            'getVersion': 'connectionPoint/getVersion/',
            'getQuantumSolutions': 'connectionPoint/getQuantumSolutions/',
            'getQuantumDevices': 'connectionPoint/getQuantumDevices/',
            'getQuantumFlows': 'connectionPoint/getQuantumFlows/',
            'runQuantumApplication': 'connectionPoint/runQuantumApplication/',
            'getQuantumExecutionResponse': 'connectionPoint/getQuantumExecutionResponse/',
            'getQuantumDevicesEx': 'connectionPoint/getQuantumDevicesEx/'
        }

        self.dynamicExtensions = {
            'getAssetCatalog': 'connectionPoint/getAssetCatalog/',
            'getAsset': 'connectionPoint/getAsset/',
            'createAsset': 'connectionPoint/createAsset?aSolutionID=',
            'updateAsset': 'connectionPoint/updateAsset/',
            'getAssetManagementResult': 'connectionPoint/getAssetManagementResult/',
            'publishFlow': 'connectionPoint/publishFlow/',
            'deleteAsset': 'connectionPoint/deleteAsset/',
            'getQuantumExecutionHistoric': 'connectionPoint/getQuantumExecutionHistoric/',
            'getQuantumExecutionHistoricResult': 'connectionPoint/getQuantumExecutionHistoricResult/'
        }

        if configFile:
            self.authenticateEx()
        
        elif username:
            self.authenticateEx(username, password)


    # INTERN FUNCTIONS
    def __updateEnviroments(self):
        customEnvironments = list()

        qpathFile = self.ConfigParser(allow_no_value=True)
        qpathFileExists = qpathFile.read(str(self.Path.home()) + '\.qpath')

        if qpathFileExists:
            for key in qpathFile['custom-environments']:
                customEnvironments.append((key, qpathFile['custom-environments'][key]))
                
        self.environments = {
            'default-environments': {
                'pro': 'https://qsoa.quantumpath.app:8443/api/',
                'lab': 'https://qsoa.quantumsoftt.com:10443/api/'
            },
            'custom-environments': dict(customEnvironments)
        }

    def __checkInputTypes(self, *args):
        for argTuple in args:
            expextedTypes = str([i.__name__ for i in argTuple[2]]).replace("['", "<").replace(" '", " <").replace("']", ">").replace("',", ">,")

            if type(argTuple[1]) not in argTuple[2]:
                raise ValueError(f'Argument "{argTuple[0]}" expected to be {expextedTypes}, not <{type(argTuple[1]).__name__}>')
    
    def __checkValues(self, *args):
        for argTuple in args:
            expextedValues = str([i for i in argTuple[2]]).replace('[', '').replace(']', '')
            
            if argTuple[1].upper() not in argTuple[2]:
                raise ValueError(f'Argument "{argTuple[0]}" expected to be {expextedValues}, not "{argTuple[1]}"')


    # USER METHODS
    def getEnvironments(self) -> dict: # getEnvironments. Returns a Dictionary
        """
        Show QuantumPath available environments.

        Prerequisites
        ----------
        None.

        Output
        ----------
        dict
        """

        qpathFile = self.ConfigParser(allow_no_value=True)
        qpathFileExists = qpathFile.read(str(self.Path.home()) + '\.qpath')

        if qpathFileExists:
            self.__updateEnviroments()

        return self.environments


    def getActiveEnvironment(self) -> tuple: # getActiveEnvironment. Returns a Tuple
        """
        Show active QuantumPath environment.

        Prerequisites
        ----------
        None.

        Output
        ----------
        tuple
        """

        return self.activeEnvironment


    def setActiveEnvironment(self, environmentName: str) -> tuple: # setActiveEnvironment. Returns a Tuple
        """
        Set active QuantumPath environment.

        Prerequisites
        ----------
        Existing QuantumPath environment.

        Parameters
        ----------
        environmentName : str
            QuantumPath environment name to set as active.

        Output
        ----------
        tuple
        """
        self.__checkInputTypes(
            ('environmentName', environmentName, (str,))
        )


        self.__updateEnviroments()

        if environmentName in self.environments['default-environments']:
            newActiveEnvironment = ('default-environments', environmentName)
        
        elif environmentName in self.environments['custom-environments']:
            newActiveEnvironment = ('custom-environments', environmentName)
        
        else:
            raise ValueError(f'Environment not valid. Active environment is still {self.activeEnvironment}')

        self.activeEnvironment = newActiveEnvironment

        return self.activeEnvironment


    def echoping(self) -> bool: # echoping. Returns a Boolean
        """
        Test to validate if the security service is enabled.

        Prerequisites
        ----------
        None.

        Output
        ----------
        bool
        """

        url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.securityEndpoints['echoping']
        
        ping = apiConnection(url, 'boolean')
        
        return ping


    def authenticate(self, username: str = None, password: str = None) -> bool: # authenticate. Returns a Boolean
        """
        Performs the user authentication process.
        
        Prerequisites
        ----------
        - User created in QPath.

        Parameters
        ----------
        username : str
            QPath account username to authenticate.
        password : str
            QPath account password to authenticate. (Base64)
        
        Prerequisites
        ----------
        - User created in QPath.
        - .qpath file created in home path.

        Parameters
        ----------
        None if .qpath file in home path contains the credentials.

        Output
        ----------
        bool
        """
        if username and password:
            self.__checkInputTypes(
                ('username', username, (str,)),
                ('password', password, (str,))
            )


        url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.securityEndpoints['authenticate']

        if not username and not password:
            try:
                qpathcredentials = self.ConfigParser(allow_no_value=True)
                qpathcredentials.read(str(self.Path.home()) + '\.qpath')

                username = qpathcredentials[self.activeEnvironment[1] + '-credentials']['username']
                password = qpathcredentials[self.activeEnvironment[1] + '-credentials']['password']

            except:
                raise self.ConfigFileError('Error reading username or password in config file')
            
        elif not username or not password:
            raise TypeError('QSOAPlatform.authenticate() takes from 1 to 3 positional arguments')

        else:
            try:
                base64_bytes = password.encode('ascii')
                password = str(self.base64.b64decode(base64_bytes).decode('ascii'))
            
            except:
                raise self.Base64Error('Invalid Base64 encoding in password')

        self.context = self.Context(username, password, url)

        return True


    def authenticateEx(self, username: str = None, password: str = None) -> bool: # authenticateEx. Returns a Boolean
        """
        Performs the user authentication process.
        
        Prerequisites
        ----------
        - User created in QPath.

        Parameters
        ----------
        username : str
            QPath account username to authenticate.
        password : str
            QPath account password to authenticate. (SHA-256)
        
        Prerequisites
        ----------
        - User created in QPath.
        - .qpath file created in home path.

        Parameters
        ----------
        None if .qpath file in home path contains the credentials.

        Output
        ----------
        bool
        """
        if username and password:
            self.__checkInputTypes(
                ('username', username, (str,)),
                ('password', password, (str,))
            )


        url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.securityEndpoints['authenticateEx']

        if not username and not password:
            try:
                qpathcredentials = self.ConfigParser(allow_no_value=True)
                qpathcredentials.read(str(self.Path.home()) + '\.qpath')

                username = qpathcredentials[self.activeEnvironment[1] + '-credentials']['username']
                password = qpathcredentials[self.activeEnvironment[1] + '-credentials']['password']
            
            except:
                raise self.ConfigFileError('Error reading username or password in config file')

        elif not username or not password:
            raise TypeError('QSOAPlatform.authenticate() takes from 1 to 3 positional arguments')

        self.context = self.Context(username, password, url)

        return True


    def echostatus(self) -> bool: # echostatus. Returns a Boolean
        """
        Check if user session is active.

        Prerequisites
        ----------
        None.

        Output
        ----------
        bool
        """
        
        status = False

        if self.context:
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.securityEndpoints['echostatus']

            status = apiConnection(url, self.context.getHeader(), 'boolean')

            if not status:
                self.context = None

        return status


    def echouser(self) -> str: # echouser. Returns a String
        """
        Check user login status.

        Prerequisites
        ----------
        - User already authenticated.

        Output
        ----------
        str
        """

        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.securityEndpoints['echouser']
            
            login = apiConnection(url, self.context.getHeader(), 'string')
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return login


    def getVersion(self) -> str: # getVersion. Returns a String
        """
        Check the ConnectionPoint service version.

        Prerequisites
        ----------
        - User already authenticated.

        Output
        ----------
        str
        """

        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['getVersion']

            version = apiConnection(url, self.context.getHeader(), 'string')
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return version


    def getQuantumSolutionList(self) -> dict: # getQuantumSolutionList. Returns a Dictionary
        """
        Show the list of solutions available to the user along with their IDs.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.

        Output
        ----------
        dict
        """

        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['getQuantumSolutions']

            solutionsDict = apiConnection(url, self.context.getHeader(), 'json')
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return solutionsDict


    def getQuantumSolutions(self) -> list: # getQuantumSolutions. Returns a SolutionItem List
        """
        Get the solutions available from the user as an object.

        Prerequisites
        ----------
        - User already authenticated.

        Output
        ----------
        SolutionItem obj list
        """

        solutions = list()

        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['getQuantumSolutions']

            solutionsDict = apiConnection(url, self.context.getHeader(), 'json')

            for idSolution in solutionsDict:
                solutions.append(self.SolutionItem(int(idSolution), solutionsDict[idSolution]))

        else:
            raise self.AuthenticationError('User not authenticated')

        return solutions


    def getQuantumSolutionName(self, idSolution: int) -> str: # getQuantumSolutionName. Returns a String
        """
        Get the name of a solution.

        Prerequisites
        ----------
        - User already authenticated.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to show their name.

        Output
        ----------
        str
        """
        self.__checkInputTypes(
            ('idSolution', idSolution, (int,))
        )


        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['getQuantumSolutions']

            solutionsDict = apiConnection(url, self.context.getHeader(), 'json')
            
            if str(idSolution) in solutionsDict.keys():
                solutionName = solutionsDict[str(idSolution)]
            
            else:
                raise ValueError('Incorrect Solution ID')
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return solutionName


    def getQuantumDeviceList(self, idSolution: int) -> dict: # getQuantumDeviceList. Returns a Dictionary
        """
        Show the list of devices available in a solution along with their IDs.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to show their devices.

        Output
        ----------
        dict
        """
        self.__checkInputTypes(
            ('idSolution', idSolution, (int,))
        )


        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['getQuantumDevices'] + str(idSolution)

            devicesDict = apiConnection(url, self.context.getHeader(), 'json')

        else:
            raise self.AuthenticationError('User not authenticated')

        return devicesDict


    def getQuantumDevices(self, idSolution: int) -> list: # getQuantumDevices. Returns a DeviceItem List
        """
        Get the available devices in a solution as an object.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to show their devices.
        
        Output
        ----------
        DeviceItem obj list
        """
        self.__checkInputTypes(
            ('idSolution', idSolution, (int,))
        )
            

        devices = list()

        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['getQuantumDevicesEx'] + str(idSolution)

            devicesDict = apiConnection(url, self.context.getHeader(), 'json')

            for device in devicesDict:
                devices.append(self.DeviceItem(device))
        
        else:
            raise self.AuthenticationError('User not authenticated')
        
        return devices


    def getQuantumDeviceName(self, idSolution: int, idDevice: int) -> str: # getQuantumDeviceName. Returns a String
        """
        Get the name of a device.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to wich the device belongs.
        idDevice : int
            Device ID to show their name.
        
        Output
        ----------
        str
        """
        self.__checkInputTypes(
            ('idSolution', idSolution, (int,)),
            ('idDevice', idDevice, (int,))
        )


        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['getQuantumDevices'] + str(idSolution)

            devicesDict = apiConnection(url, self.context.getHeader(), 'json')
            
            if str(idDevice) in devicesDict.keys():
                deviceName = devicesDict[str(idDevice)]
            
            else:
                raise ValueError('Incorrect Device ID')
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return deviceName


    def getQuantumFlowList(self, idSolution: int) -> dict: # getQuantumFlowList. Returns a Dictionary
        """
        Show the list of flows available in a solution along with their IDs.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to show their flows.
        
        Output
        ----------
        dict
        """
        self.__checkInputTypes(
            ('idSolution', idSolution, (int,))
        )


        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['getQuantumFlows'] + str(idSolution)

            flowsDict = apiConnection(url, self.context.getHeader(), 'json')
        
        else:
            raise self.AuthenticationError('User not authenticated')
        
        return flowsDict


    def getQuantumFlows(self, idSolution: int) -> list: # getQuantumFlows. Returns a FlowItem List
        """
        Get the flows available in a solution as an object.
        
        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.

        Parameters
        ----------
        idSolution : int
            Solution ID to show their flows.

        Output
        ----------
        FlowItem obj list
        """
        self.__checkInputTypes(
            ('idSolution', idSolution, (int,))
        )


        flows = list()

        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['getQuantumFlows'] + str(idSolution)

            flowsDict = apiConnection(url, self.context.getHeader(), 'json')

            for idFlow in flowsDict:
                flows.append(self.FlowItem(int(idFlow), flowsDict[idFlow]))
        
        else:
            raise self.AuthenticationError('User not authenticated')
        
        return flows


    def getQuantumFlowName(self, idSolution: int, idFlow: int) -> str: # getQuantumFlowName. Returns a String
        """
        Get the name of a flow.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to wich the flow belongs.
        idFlow : int
            Flow ID to show their name.

        Output
        ----------
        str
        """
        self.__checkInputTypes(
            ('idSolution', idSolution, (int,)),
            ('idFlow', idFlow, (int,))
        )


        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['getQuantumFlows'] + str(idSolution)

            flowsDict = apiConnection(url, self.context.getHeader(), 'json')
            
            if str(idFlow) in flowsDict.keys():
                flowName = flowsDict[str(idFlow)]
            
            else:
                raise ValueError('Incorrect Flow ID')
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return flowName


    def runQuantumApplication(self, applicationName: str, idSolution: int, idFlow: int, idDevice: int) -> Application: # runQuantumApplication. Returns an Application object
        """
        Run a created quantum solution.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        applicationName : str
            Nametag to identify the execution.
        idSolution : int
            Solution ID to run.
        idFlow : int
            Specific Flow ID to run.
        idDevice : int
            Specific Device ID to run the solution.
        
        Output
        ----------
        Application obj
        """
        self.__checkInputTypes(
            ('applicationName', applicationName, (str,)),
            ('idSolution', idSolution, (int,)),
            ('idFlow', idFlow, (int,)),
            ('idDevice', idDevice, (int,))
        )


        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['runQuantumApplication'] + str(applicationName) + '/' + str(idSolution) + '/' + str(idFlow) + '/' + str(idDevice)

            executionToken = apiConnection(url, self.context.getHeader(), 'string')

            application = self.Application(applicationName, int(idSolution), int(idFlow), int(idDevice), executionToken)
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return application


    def getQuantumExecutionResponse(self, *args) -> Execution: # getQuantumExecutionResponse. Returns an Execution object
        """
        Get the response of a quantum solution execution.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution run.
        - Application object generated.
        
        Parameters
        ----------
        application : Application obj
            Application object generated in running a quantum solution.
        
        Prerequisites
        ----------
        - User already authenticated.
        - Solution run.

        Parameters
        ----------
        executionToken : str
            Solution ID of the application already run.
        idSolution : int
            Solution ID of the solution already run.
        idFlow : int
            Specific Flow ID of the flow already run.
        
        Output
        ----------
        Execution obj
        """
        if len(args) == 1:
            self.__checkInputTypes(
                ('application', args[0], (self.Application,))
            )
        
        elif len(args) == 3:
            self.__checkInputTypes(
                ('executionToken', args[0], (str,)),
                ('idSolution', args[1], (int,)),
                ('idFlow', args[2], (int,))
            )
        
        else:
            raise TypeError('QSOAPlatform.authenticate() takes from 1 to 4 positional arguments')
        

        if self.echostatus():
            if len(args) == 1:
                executionToken = args[0].getExecutionToken()
                idSolution = args[0].getIdSolution()
                idFlow = args[0].getIdFlow()
            
            elif len(args) == 3:
                executionToken = args[0]
                idSolution = args[1]
                idFlow = args[2]

            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.connectionPoints['getQuantumExecutionResponse'] + str(executionToken) + '/' + str(idSolution) + '/' + str(idFlow)

            executionDict = apiConnection(url, self.context.getHeader(), 'json')
            
            execution = self.Execution(executionDict)
        
        else:
            raise self.AuthenticationError('User not authenticated')
        
        return execution


    def representResults(self, execution: Execution, resultIndex: int = None): # representResults. Returns a plot
        """
        Results visual representation.

        Prerequisites
        ----------
        - User already authenticated.
        - Execution completed.
        
        Parameters
        ----------
        execution : Execution obj
            Execution object generated by execution response method.
        resultIndex : int
            Value to just show that result by index. Optional argument.
        
        Output
        ----------
        png / string
        """
        self.__checkInputTypes(
            ('execution', execution, (self.Execution,))
        )

        if resultIndex:
            self.__checkInputTypes(
                ('resultIndex', resultIndex, (int,))
            )


        representation = None

        def plotQuantumGatesCircuit(histogramData: dict, name: str): # plotQuantumGatesCircuit. Returns a plot
            histogramTitle = name
            histogramValues = histogramData[name]

            histogramValues = self.collections.OrderedDict(sorted(histogramValues.items())) # sort values

            fig, ax = self.plt.subplots(1, 1)
            ax.bar([ str(i) for i in histogramValues.keys()], histogramValues.values(), color='g')

            ax.set_title(histogramTitle)

            rects = ax.patches
            labels = [list(histogramValues.values())[i] for i in range(len(rects))]

            for rect, label in zip(rects, labels):
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2, height+0.01, label, ha='center', va='bottom')

            self.plt.show()

        def plotAnnealingCircuit(histogramData, name): # plotAnnealingCircuit. Returns a String
            histogramTitle = name
            histogramValues = histogramData[name]

            histogramValues2 = histogramValues.copy()
            del histogramValues2['fullsample']

            tableResults = self.PrettyTable(['Name', 'Value'])

            for key, value in histogramValues['fullsample'].items():
                tableResults.add_row([key, value])

            tableInfo = self.PrettyTable()
            tableInfo.field_names = histogramValues2.keys()
            tableInfo.add_rows([histogramValues2.values()])

            return f'\n\n{histogramTitle}\n{tableInfo}\n{tableResults}'

        if self.echostatus():
            if execution.getExitCode() == 'OK':
                histogramData = execution.getHistogram()

                if 'number_of_samples' in (list(histogramData.values())[0]).keys(): # annealing
                    if resultIndex == None:
                        representation = ''

                        for name in histogramData:
                            representation = representation + plotAnnealingCircuit(histogramData, name)
                    
                    else:
                        if resultIndex > -1 and resultIndex < len(histogramData):
                            representation = plotAnnealingCircuit(histogramData, list(histogramData)[resultIndex])
                        
                        else:
                            raise IndexError(f'Invalid resultIndex. It should be 0 to {len(histogramData) - 1}')

                else: # quantum gates
                    if resultIndex == None:
                        for name in histogramData:
                            plotQuantumGatesCircuit(histogramData, name)
                    else:
                        if resultIndex > -1 and resultIndex < len(histogramData):
                            plotQuantumGatesCircuit(histogramData, list(histogramData)[resultIndex])

                        else:
                            raise IndexError(f'Invalid resultIndex. It should be 0 to {len(histogramData) - 1}')
            
            else:
                raise self.ExecutionObjectError('Execution status code is not "OK"')
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return representation


    def getAssetCatalog(self, idSolution: int, assetType: str, assetLevel: str) -> list: # getAssetCatalog. Returns an Asset List
        """
        Get asset information from a solution.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to show their information.
        assetType : str
            Type of the asset required. It can be CIRCUIT or FLOW.
        assetLevel : str
            Level of the Language specificated. It can be VL (Visual Language) or IL (Intermediate Language).
        
        Output
        ----------
        Asset obj list
        """
        self.__checkInputTypes(
            ('idSolution', idSolution, (int,)),
            ('assetType', assetType, (str,)),
            ('assetLevel', assetLevel, (str,))
        )
        self.__checkValues(
            ('assetType', assetType, ['CIRCUIT', 'FLOW']),
            ('assetLevel', assetLevel, ['VL', 'IL'])
        )


        assetCatalog = list()

        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.dynamicExtensions['getAssetCatalog'] + str(idSolution) + '/' + assetType + '/' + assetLevel

            assetCatalogList = apiConnection(url, self.context.getHeader(), 'json')

            for asset in assetCatalogList:
                assetCatalog.append(self.Asset(asset))
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return assetCatalog


    def getAsset(self, idAsset: int, assetType: str, assetLevel: str) -> Asset: # getAsset. Returns an Asset object
        """
        Get specific asset information.

        Prerequisites
        ----------
        - User already authenticated.
        - Asset created.
        
        Parameters
        ----------
        idAsset : int
            Asset ID to show their information.
        assetType : str
            Type of the asset required. It can be CIRCUIT or FLOW.
        assetLevel : str
            Level of the Language specificated. It can be VL (Visual Language) or IL (Intermediate Language).
        
        Output
        ----------
        Asset obj
        """
        self.__checkInputTypes(
            ('idAsset', idAsset, (int,)),
            ('assetType', assetType, (str,)),
            ('assetLevel', assetLevel, (str,))
        )
        self.__checkValues(
            ('assetType', assetType, ['CIRCUIT', 'FLOW']),
            ('assetLevel', assetLevel, ['VL', 'IL'])
        )


        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.dynamicExtensions['getAsset'] + str(idAsset) + '/' + assetType + '/' + assetLevel

            assetResponse = apiConnection(url, self.context.getHeader(), 'json')

            asset = self.Asset(assetResponse)
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return asset


    def createAsset(self, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody,
                    assetType: str, assetLevel: str) -> AssetManagementData: # createAsset. Returns an Asset Management Data object
        """
        Create asset.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution to create the asset.
        assetName : str
            New asset name.
        assetNamespace : str
            New asset namespace.
        assetDescription : str
            New asset description.
        assetBody : str / CircuitGates obj / CircuitFlow obj
            New asset body as string or as a circtuit obj.
        assetType : str
            New asset type. It can be GATES, ANNEAL or FLOW.
        assetLevel : str
            New asset level. It can be VL (Visual Language) or IL (Intermediate Language).
        
        Output
        ----------
        AssetManagementData obj
        """
        self.__checkInputTypes(
            ('idSolution', idSolution, (int,)),
            ('assetName', assetName, (str,)),
            ('assetNamespace', assetNamespace, (str,)),
            ('assetDescription', assetDescription, (str,)),
            ('assetBody', assetBody, (str, self.CircuitGates, self.CircuitFlow)),
            ('assetType', assetType, (str,)),
            ('assetLevel', assetLevel, (str,))
        )
        self.__checkValues(
            ('assetType', assetType, ['GATES', 'ANNEAL', 'FLOW']),
            ('assetLevel', assetLevel, ['VL', 'IL'])
        )
        
        
        if self.echostatus():
            if isinstance(assetBody, (self.CircuitGates, self.CircuitFlow)):
                assetBody = assetBody.getParsedBody()

            newAsset = {
                "AssetID": -1,
                "AssetName": assetName,
                "AssetNamespace": assetNamespace,
                "AssetDescription": assetDescription,
                "AssetBody": self.base64.b64encode(assetBody.encode('ascii')).decode('ascii'),
                "AssetType": assetType,
                "AssetLevel": assetLevel,
                "AssetLastUpdate": ''
            }

            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.dynamicExtensions['createAsset'] + str(idSolution)
            
            assetManagementDataResult = apiConnection(url, self.context.getHeader(), str(newAsset), 'json', 'data')

            assetManagementData = self.AssetManagementData(assetManagementDataResult)
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return assetManagementData


    def createAssetFlow(self, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody,
                        assetLevel: str, publish: bool = False) -> AssetManagementData: # createAssetFlow. Returns an Asset Management Data object
        """
        Create asset flow.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution to create the asset.
        assetName : str
            New asset name.
        assetNamespace : str
            New asset namespace.
        assetDescription : str
            New asset description.
        assetBody : str / CircuitFlow obj
            New asset body as string or as a circtuit obj.
        assetLevel : str
            New asset level. It can be VL (Visual Language) or IL (Intermediate Language).
        publish : bool
            Publish flow or not.

        Output
        ----------
        AssetManagementData obj
        """
        self.__checkInputTypes(
            ('assetBody', assetBody, (str, self.CircuitFlow)),
            ('publish', publish, (bool,))
        )

        if self.echostatus():
            assetManagementData = self.createAsset(idSolution, assetName, assetNamespace, assetDescription, assetBody, 'FLOW', assetLevel)

            if publish:
                self.publishFlow(assetManagementData.getIdAsset(), publish)

        else:
            raise self.AuthenticationError('User not authenticated')

        return assetManagementData


    def publishFlow(self, idFlow: int, publish: bool) -> bool:
        """
        Change flow publish status.

        Prerequisites
        ----------
        - User already authenticated.
        - Access permission to the flow.

        Parameters
        ----------
        idFlow : int
            Flow ID to change publish status.
        publish : bool
            Publish flow or not.

        Output
        ----------
        bool
        """
        self.__checkInputTypes(
            ('idFlow', idFlow, (int,)),
            ('publish', publish, (bool,))
        )


        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.dynamicExtensions['publishFlow'] + str(idFlow) + '/' + str(publish)
            
            apiConnection(url, self.context.getHeader(), 'string')
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return publish


    def updateAsset(self, asset: Asset, assetName: str = None, assetNamespace: str = None, assetDescription: str = None,
                    assetBody = None, assetType: str = None, assetLevel: str = None) -> AssetManagementData: # updateAsset. Returns an Asset Management Data object
        """
        Update asset values.

        Prerequisites
        ----------
        - User already authenticated.
        - Asset created.
        
        Parameters
        ----------
        asset : Asset obj
            Asset object to change information.
        assetName : str
            New asset name. Optional argument.
        assetNamespace : str
            New asset namespace. Optional argument.
        assetDescription : str
            New asset description. Optional argument.
        assetBody : str / CircuitGates obj / CircuitFlow obj
            New asset body as string or as a circtuit obj. Optional argument.
        assetType : str
            New asset type. It can be GATES, ANNEAL or FLOW. Optional argument.
        assetLevel : str
            New asset level. It can be VL (Visual Language) or IL (Intermediate Language). Optional argument.
        
        Output
        ----------
        AssetManagementData obj
        """
        self.__checkInputTypes(
            ('asset', asset, (self.Asset,))
        )
        if assetName:
            self.__checkInputTypes(
                ('assetName', assetName, (str,))
            )
        elif assetNamespace:
            self.__checkInputTypes(
                ('assetNamespace', assetNamespace, (str,))
            )
        elif assetDescription:
            self.__checkInputTypes(
                ('assetDescription', assetDescription, (str,))
            )
        elif assetBody:
            self.__checkInputTypes(
                ('assetBody', assetBody, (str, self.CircuitGates, self.CircuitFlow)),
                ('assetType', assetType, (str,)),
                ('assetLevel', assetLevel, (str,))
            )
            self.__checkValues(
                ('assetType', assetType, ['GATES', 'ANNEAL', 'FLOW']),
                ('assetLevel', assetLevel, ['VL', 'IL'])
            )
        
        
        if self.echostatus():
            if assetName:
                asset.setName(assetName)
            if assetNamespace:
                asset.setNamespace(assetNamespace)
            if assetDescription:
                asset.setDescription(assetDescription)
            if assetBody:
                if isinstance(assetBody, (self.CircuitGates, self.CircuitFlow)):
                    assetBody = assetBody.getParsedBody()
                asset.setBody(assetBody)
            if assetType:
                asset.setType(assetType)
            if assetLevel:
                asset.setLevel(assetLevel)

            newAsset = {
                "AssetID": asset.getId(),
                "AssetName": asset.getName(),
                "AssetNamespace": asset.getNamespace(),
                "AssetDescription": asset.getDescription() if asset.getDescription() else '',
                "AssetBody": self.base64.b64encode(asset.getBody().encode('ascii')).decode('ascii'),
                "AssetType": asset.getType(),
                "AssetLevel": asset.getLevel(),
                "AssetLastUpdate": asset.getLastUpdate()
            }
            
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.dynamicExtensions['updateAsset']

            assetManagementDataResult = apiConnection(url, self.context.getHeader(), str(newAsset), 'json', 'data')

            assetManagementData = self.AssetManagementData(assetManagementDataResult)
        
        else:
            raise self.AuthenticationError('User not authenticated')
        
        return assetManagementData


    def getAssetManagementResult(self, lifecycleToken: str) -> AssetManagementResult: # getAssetManagementResult. Returns an Asset Management Result object
        """
        Get Asset Management Result from a lifecycle token.

        Prerequisites
        ----------
        - Existing asset lifecycle token.
        
        Parameters
        ----------
        lifecycleToken : str
            Asset lifecycle token.
        
        Output
        ----------
        AssetManagementResult obj
        """
        self.__checkInputTypes(
            ('lifecycleToken', lifecycleToken, (str,))
        )
    

        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.dynamicExtensions['getAssetManagementResult'] + str(lifecycleToken)

            assetManagementResult = apiConnection(url, self.context.getHeader(), 'json')

            assetManagementResult = self.AssetManagementResult(assetManagementResult)
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return assetManagementResult


    def deleteAsset(self, *args) -> bool: # deleteAsset. Returns a Boolean
        """
        Delete asset.

        Prerequisites
        ----------
        - User already authenticated.
        - Asset created.
        
        Parameters
        ----------
        asset : Asset obj
            Asset object to delete.
        
        Parameters
        ----------
        idAsset : int
            Asset id to delete.
        assetType : str
            Asset type to delete. It can be CIRCUIT or FLOW.
        
        Output
        ----------
        bool
        """
        if len(args) == 1:
            self.__checkInputTypes(
                ('asset', args[0], (self.Asset,))
            )
        
        elif len(args) == 2:
            self.__checkInputTypes(
                ('idAsset', args[0], (int,)),
                ('assetType', args[1], (str,))
            )
            self.__checkValues(
                ('assetType', args[1], ['CIRCUIT', 'FLOW'])
            )


        if self.echostatus():
            if len(args) == 1:
                idAsset = str(args[0].getId())

                if args[0].getType() == 'FLOW':
                    assetType = args[0].getType()
                else:
                    assetType = 'CIRCUIT'

            else:
                idAsset = str(args[0])
                assetType = str(args[1])
                
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.dynamicExtensions['deleteAsset'] + idAsset + '/' + assetType

            assetDeleted = apiConnection(url, self.context.getHeader(), 'boolean')
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return assetDeleted
    

    def getQuantumExecutionHistoric(self, idSolution: int = None, idFlow: int = None, idDevice: int = None, dateFrom: str = None, isSimulator: bool = None,
                                    top: int = None, resultType: bool = None) -> list: # getQuantumExecutionHistoric. Returns a QuantumExecutionHistoryEntry List
        """
        Get a list of quantum execution history entries.

        Prerequisites
        ----------
        - User already authenticated.
        
        Parameters
        ----------
        idSolution : int
            Filter by solution ID. Optional argument.
        idFlow : int
            Filter by flow ID. Optional argument.
        idDevice : int
            Filter by device ID. Optional argument.
        dateFrom : str
            Filter from date. Format yyyy-mm-dd:hh:mm:ss. Optional argument.
        isSimulator : bool
            Filter is simulator. Optional argument.
        top : int
            Number of top results. 10 by default. Optional argument.
        resultType : bool
            Result type.True if it is OK and false if ERR. Optional argument.
        
        Output
        ----------
        QuantumExecutionHistoryEntry obj list
        """
        if idSolution:
            self.__checkInputTypes(
                ('idSolution', idSolution, (int,))
            )
        elif idFlow:
            self.__checkInputTypes(
                ('idFlow', idFlow, (int,))
            )
        elif idDevice:
            self.__checkInputTypes(
                ('idDevice', idDevice, (int,))
            )
        elif dateFrom:
            self.__checkInputTypes(
                ('dateFrom', dateFrom, (str,))
            )
        elif isSimulator:
            self.__checkInputTypes(
                ('isSimulator', isSimulator, (bool,))
            )
        elif top:
            self.__checkInputTypes(
                ('top', top, (int,))
            )
        elif resultType:
            self.__checkInputTypes(
                ('resultType', resultType, (bool,))
            )


        quantumExecutionHistoric = list()

        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.dynamicExtensions['getQuantumExecutionHistoric'] + str(idSolution) + '/' + str(idFlow) + '/' + str(idDevice) + '/' + str(dateFrom) + '/' + str(isSimulator) + '/' + str(top) + '/' + str(resultType)

            quantumExecutionHistoricList = apiConnection(url, self.context.getHeader(), 'json')

            for quantumExecutionHistoryEntry in quantumExecutionHistoricList:
                quantumExecutionHistoric.append(self.QuantumExecutionHistoryEntry(quantumExecutionHistoryEntry))
        
        else:
            raise self.AuthenticationError('User not authenticated')

        return quantumExecutionHistoric


    def getQuantumExecutionHistoricResult(self, idResult: int) -> QuantumExecutionHistoryEntry: # getQuantumExecutionHistoricResult. Returns a QuantumExecutionHistoryEntry object
        """
        Get a quantum execution history entry.

        Prerequisites
        ----------
        - User already authenticated.
        - Existing result.
        
        Parameters
        ----------
        idResult : int
            Result ID to get information about.
        
        Output
        ----------
        QuantumExecutionHistoryEntry obj
        """
        self.__checkInputTypes(
            ('idResult', idResult, (int,))
        )


        if self.echostatus():
            url = self.environments[self.activeEnvironment[0]][self.activeEnvironment[1]] + self.dynamicExtensions['getQuantumExecutionHistoricResult'] + str(idResult)

            quantumExecutionHistoricResultList = apiConnection(url, self.context.getHeader(), 'json')

            quantumExecutionHistoricResult = self.QuantumExecutionHistoryEntry(quantumExecutionHistoricResultList[0])
        
        else:
            raise self.AuthenticationError('User not authenticated')
                
        return quantumExecutionHistoricResult


    def runQuantumApplicationSync(self, applicationName: str, idSolution: int, idFlow: int, idDevice: int) -> Application: # runQuantumApplicationSync. Returns an Application object
        """
        Run a created quantum solution synchronous.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        applicationName : str
            Nametag to identify the execution.
        idSolution : int
            Solution ID to run.
        idFlow : int
            Specific Flow ID to run.
        idDevice : int
            Specific Device ID to run the solution.
        
        Output
        ----------
        Application obj
        """

        application = self.runQuantumApplication(applicationName, idSolution, idFlow, idDevice)

        execution = self.getQuantumExecutionResponse(application)

        while execution.getExitCode() == 'WAIT':
            self.time.sleep(1)
            execution = self.getQuantumExecutionResponse(application)
        
        return application


    def createAssetSync(self, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody,
                        assetType: str, assetLevel: str) -> AssetManagementResult: # createAssetSync. Returns an Asset Management Result object
        """
        Create asset and get result.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution to create the asset.
        assetName : str
            New asset name.
        assetNamespace : str
            New asset namespace.
        assetDescription : str
            New asset description.
        assetBody : str / CircuitGates obj / CircuitFlow obj
            New asset body as string or as a circtuit obj.
        assetType : str
            New asset type. It can be GATES, ANNEAL or FLOW.
        assetLevel : str
            New asset level. It can be VL (Visual Language) or IL (Intermediate Language).
        
        Output
        ----------
        AssetManagementResult obj
        """

        assetManagementData = self.createAsset(idSolution, assetName, assetNamespace, assetDescription, assetBody, assetType, assetLevel)

        assetManagementResult = self.getAssetManagementResult(assetManagementData.getLifecycleToken())

        while assetManagementResult.getExitCode() == 'WAIT' or assetManagementResult.getExitCode() == 'READY':
            self.time.sleep(1)
            assetManagementResult = self.getAssetManagementResult(assetManagementData.getLifecycleToken())

        return assetManagementResult


    def createAssetFlowSync(self, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody,
                            assetLevel: str, publish: bool = False) -> AssetManagementResult: # createAssetFlowSync. Returns an Asset Management Result object
        """
        Create asset flow and get result.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution to create the asset.
        assetName : str
            New asset name.
        assetNamespace : str
            New asset namespace.
        assetDescription : str
            New asset description.
        assetBody : str / CircuitGates obj / CircuitFlow obj
            New asset body as string or as a circtuit obj.
        assetLevel : str
            New asset level. It can be VL (Visual Language) or IL (Intermediate Language).
        publish : bool
            Publish flow or not.

        Output
        ----------
        AssetManagementResult obj
        """
        
        assetManagementData = self.createAssetFlow(idSolution, assetName, assetNamespace, assetDescription, assetBody, assetLevel, publish)

        assetManagementResult = self.getAssetManagementResult(assetManagementData.getLifecycleToken())

        while assetManagementResult.getExitCode() == 'WAIT' or assetManagementResult.getExitCode() == 'READY':
            self.time.sleep(1)
            assetManagementResult = self.getAssetManagementResult(assetManagementData.getLifecycleToken())

        return assetManagementResult

    
    def updateAssetSync(self, asset: Asset, assetName: str = None, assetNamespace: str = None, assetDescription: str = None,
                        assetBody = None, assetType: str = None, assetLevel: str = None) -> AssetManagementResult: # updateAssetSync. Returns an Asset Management Result object
        """
        Update asset values and get result.

        Prerequisites
        ----------
        - User already authenticated.
        - Asset created.
        
        Parameters
        ----------
        asset : Asset obj
            Asset object to change information.
        assetName : str
            New asset name. Optional argument.
        assetNamespace : str
            New asset namespace. Optional argument.
        assetDescription : str
            New asset description. Optional argument.
        assetBody : str / CircuitGates obj / CircuitFlow obj
            New asset body as string or as a circtuit obj. Optional argument.
        assetType : str
            New asset type. It can be GATES, ANNEAL or FLOW. Optional argument.
        assetLevel : str
            New asset level. It can be VL (Visual Language) or IL (Intermediate Language). Optional argument.
        
        Output
        ----------
        AssetManagementResult obj
        """
        
        assetManagementData = self.updateAsset(asset, assetName, assetNamespace, assetDescription, assetBody, assetType, assetLevel)

        assetManagementResult = self.getAssetManagementResult(assetManagementData.getLifecycleToken())

        while assetManagementResult.getExitCode() == 'WAIT' or assetManagementResult.getExitCode() == 'READY':
            self.time.sleep(3)
            assetManagementResult = self.getAssetManagementResult(assetManagementData.getLifecycleToken())

        return assetManagementResult