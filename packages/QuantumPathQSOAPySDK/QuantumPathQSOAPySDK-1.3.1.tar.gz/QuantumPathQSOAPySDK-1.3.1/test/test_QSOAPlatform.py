import unittest
import time

from QuantumPathQSOAPySDK import QSOAPlatform

idSolution_gates = 10391
idDevice_gates = 2
idFlow_gates = 596
executionToken_gates = 'be2b3021-d294-472e-8265-3b39583ad173'

applicationName = 'Application Name'

idSolution_annealing = 10396
idFlow_annealing = 335
executionToken_annealing = '10a763c4-4456-4c42-ad2b-46759886d7a8'

assetType_circuit = 'CIRCUIT'
assetType_gates = 'GATES'
assetType_flow = 'FLOW'
assetLevel_vl = 'VL'
assetName_circuit = 'test_circuit'
assetName_flow = 'test_flow'
assetDescription = 'assetDescription'
assetNamespace = 'test'
assetBody = 'circuit={"cols":[["H"],["CTRL","X"],["Measure","Measure"]]}'
idAsset = 21072

def waitForApplicationResponse(qsoa: QSOAPlatform, application):
    execution = qsoa.getQuantumExecutionResponse(application)

    while execution.getExitCode() == 'WAIT':
        time.sleep(1)
        execution = qsoa.getQuantumExecutionResponse(application)


##################_____GET ENVIRONMENTS_____##################
class Test_GetEnvironments(unittest.TestCase):

    def test_getEnvironments(self):
        qsoa = QSOAPlatform()

        environments = qsoa.getEnvironments()

        self.assertIsInstance(environments, dict)
        self.assertEqual(environments['default-environments'], {
            'pro': 'https://qsoa.quantumpath.app:8443/api/',
            'lab': 'https://qsoa.quantumsoftt.com:10443/api/'
        })


##################_____GET ACTIVE ENVIRONMENT_____##################
class Test_GetActiveEnvironment(unittest.TestCase):

    def test_getActiveEnvironment(self):
        qsoa = QSOAPlatform()

        qsoa.setActiveEnvironment('pro')
        activeEnvironment = qsoa.getActiveEnvironment()

        self.assertIsInstance(activeEnvironment, tuple)
        self.assertEqual(activeEnvironment, ('default-environments', 'pro'))


##################_____SET ACTIVE ENVIRONMENT_____##################
class Test_SetActiveEnvironment(unittest.TestCase):

    # SET ACTIVE ENVIRONMENT
    def test_setActiveEnvironment(self):
        qsoa = QSOAPlatform()

        setActiveEnvironment = qsoa.setActiveEnvironment('pro')

        self.assertIsInstance(setActiveEnvironment, tuple)
        self.assertEqual(setActiveEnvironment, ('default-environments', 'pro'))
    
    # BAD ARGUMENT TYPE environmentName
    def test_setActiveEnvironment_badArgumentType_environmentName(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.setActiveEnvironment(0)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ENVIRONMENT
    def test_setActiveEnvironment_badEnvironment(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.setActiveEnvironment('badEnvironment')

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')


##################_____ECHOPING_____##################
class Test_Echoping(unittest.TestCase):

    # ECHOPING
    def test_echoping(self):
        qsoa = QSOAPlatform()

        ping = qsoa.echoping()

        self.assertIsInstance(ping, bool)


##################_____AUTHENTICATE_____##################
class Test_Authenticate(unittest.TestCase):

    '''
    INTRODUCE MANUALLY USERNAME AND PASSWORD
    '''
    # AUTHENTICATE MANUALLY
    # def test_authenticate_manually(self):
    #     qsoa = QSOAPlatform()

    #     username = 'username'
    #     password = 'password' # password encoded in Base64

    #     authenticated = qsoa.authenticate(username, password)

    #     self.assertTrue(authenticated)

    '''
    CREATE .QPATH CONFIG FILE
    '''
    # AUTHENTICATE CONFIG FILE
    # def test_authenticate_configFile(self):
    #     qsoa = QSOAPlatform()

    #     authenticated = qsoa.authenticate()

    #     self.assertTrue(authenticated)

    # AUTHENTICATE USER MANUALLY BAD CREDENTIALS
    def test_authenticate_manually_badCredentials(self):
        qsoa = QSOAPlatform()

        username = 'username'
        password = 'cGFzc3dvcmQ=' # password encoded in Base64

        try:
            qsoa.authenticate(username, password)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT QUANTITY
    def test_authenticate_badArgumentQuantity(self):
        qsoa = QSOAPlatform()

        username = 'username'

        try:
            qsoa.authenticate(username)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE username
    def test_authenticate_badArgumentType_username(self):
        qsoa = QSOAPlatform()

        username = 99
        password = 'password'

        try:
            qsoa.authenticate(username, password)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE password
    def test_authenticate_badArgumentType_password(self):
        qsoa = QSOAPlatform()

        username = 'username'
        password = 99

        try:
            qsoa.authenticate(username, password)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT FORMAT password
    def test_authenticate_badArgumentFormat_password(self):
        qsoa = QSOAPlatform()

        username = 'username'
        password = 'password'

        try:
            qsoa.authenticate(username, password)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'Base64Error')


##################_____AUTHENTICATEEX_____##################
class Test_AuthenticateEx(unittest.TestCase):

    '''
    INTRODUCE MANUALLY USERNAME AND PASSWORD
    '''
    # AUTHENTICATE MANUALLY
    # def test_authenticateEx_manually(self):
    #     qsoa = QSOAPlatform()

    #     username = 'username'
    #     password = 'password' # password encrypted in SHA-256

    #     authenticated = qsoa.authenticateEx(username, password)

    #     self.assertTrue(authenticated)

    '''
    CREATE .QPATH CONFIG FILE
    '''
    # AUTHENTICATE CONFIG FILE
    # def test_authenticateEx_configFile(self):
    #     qsoa = QSOAPlatform()

    #     authenticated = qsoa.authenticateEx()

    #     self.assertTrue(authenticated)

    # AUTHENTICATE USER MANUALLY BAD CREDENTIALS
    def test_authenticateEx_manually_badCredentials(self):
        qsoa = QSOAPlatform()

        username = 'username'
        password = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8' # password encrypted in SHA-256

        try:
            qsoa.authenticateEx(username, password)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT QUANTITY
    def test_authenticateEx_badArgumentQuantity(self):
        qsoa = QSOAPlatform()

        username = 'username'

        try:
            qsoa.authenticateEx(username)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE username
    def test_authenticateEx_badArgumentType_username(self):
        qsoa = QSOAPlatform()

        username = 99
        password = 'password'

        try:
            qsoa.authenticateEx(username, password)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE password
    def test_authenticateEx_badArgumentType_password(self):
        qsoa = QSOAPlatform()

        username = 'username'
        password = 99

        try:
            qsoa.authenticateEx(username, password)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')


##################_____QSOAPLATFORM_____##################
class Test_QSOAPlatform(unittest.TestCase):

    # NOT AUTHENTICATE
    def test_QSOAPlatform_notAuthenticate(self):
        qsoa = QSOAPlatform()

        authenticated = qsoa.echostatus()

        self.assertFalse(authenticated)

    '''
    INTRODUCE MANUALLY USERNAME AND PASSWORD
    '''
    # AUTHENTICATE MANUALLY
    # def test_QSOAPlatform_manually(self):
    #     username = 'username'
    #     password = 'password' # password in SHA-256

    #     qsoa = QSOAPlatform(username, password)

    #     authenticated = qsoa.echostatus()

    #     self.assertTrue(authenticated)

    '''
    CREATE .QPATH CONFIG FILE
    '''
    # AUTHENTICATE CONFIG FILE
    # def test_QSOAPlatform_configFile(self):
    #     qsoa = QSOAPlatform(configFile=True)

    #     authenticated = qsoa.authenticateEx()

    #     self.assertTrue(authenticated)

    # AUTHENTICATE USER MANUALLY BAD CREDENTIALS
    def test_QSOAPlatform_manually_badCredentials(self):
        username = 'username'
        password = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8' # password encrypted in SHA-256

        try:
            QSOAPlatform(username, password)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT QUANTITY
    def test_QSOAPlatform_badArgumentQuantity(self):
        username = 'username'

        try:
            QSOAPlatform(username)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE username
    def test_QSOAPlatform_badArgumentType_username(self):
        username = 99
        password = 'password'

        try:
            QSOAPlatform(username, password)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE password
    def test_QSOAPlatform_badArgumentType_password(self):
        username = 'username'
        password = 99

        try:
            QSOAPlatform(username, password)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE configFile
    def test_QSOAPlatform_badArgumentType_configFile(self):
        try:
            QSOAPlatform(configFile=99)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')


##################_____ECHOSTATUS_____##################
class Test_Echostatus(unittest.TestCase):

    # ECHOSTATUS
    def test_echostatus(self):
        qsoa = QSOAPlatform()

        status = qsoa.echostatus()

        self.assertIsInstance(status, bool)


##################_____ECHOUSER_____##################
class Test_Echouser(unittest.TestCase):

    # ECHOUSER
    def test_echouser(self):
        qsoa = QSOAPlatform(configFile=True)

        login = qsoa.echouser()

        self.assertIsInstance(login, str)

    # NOT LOGGED IN
    def test_echouser_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.echouser()

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET VERSION_____##################
class Test_GetVersion(unittest.TestCase):

    # GET VERSION
    def test_getVersion(self):
        qsoa = QSOAPlatform(configFile=True)

        version = qsoa.getVersion()

        self.assertIsInstance(version, str)

    # NOT LOGGED IN
    def test_getVersion_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getVersion()

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM SOLUTION LIST_____##################
class Test_GetQuantumSolutionList(unittest.TestCase):

    # GET QUANTUM SOLUTION LIST
    def test_getQuantumSolutionList(self):
        qsoa = QSOAPlatform(configFile=True)

        solutionList = qsoa.getQuantumSolutionList()

        self.assertIsInstance(solutionList, dict)

    # NOT LOGGED IN
    def test_getQuantumSolutionList_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumSolutionList()

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM SOLUTIONS_____##################
class Test_GetQuantumSolutions(unittest.TestCase):

    # GET QUANTUM SOLUTIONS
    def test_getQuantumSolutions(self):
        qsoa = QSOAPlatform(configFile=True)

        solutions = qsoa.getQuantumSolutions()

        self.assertIsInstance(solutions, list)

        firstSolution = solutions[0]
        self.assertEqual(type(firstSolution).__name__, 'SolutionItem')

    # NOT LOGGED IN
    def test_getQuantumSolutions_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumSolutions()

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM SOLUTION NAME_____##################
class Test_GetQuantumSolutionName(unittest.TestCase):

    # GET QUANTUM SOLUTION NAME
    def test_getQuantumSolutionName(self):
        qsoa = QSOAPlatform(configFile=True)

        solutionName = qsoa.getQuantumSolutionName(idSolution_gates)

        self.assertIsInstance(solutionName, str)

    # BAD ARGUMENT idSolution
    def test_getQuantumSolutionName_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.getQuantumSolutionName(idSolution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'NonExistentItemError')

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumSolutionName_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.getQuantumSolutionName(idSolution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getQuantumSolutionName_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumSolutionName(idSolution_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM DEVICE LIST_____##################
class Test_GetQuantumDeviceList(unittest.TestCase):

    # GET QUANTUM DEVICE LIST
    def test_getQuantumDeviceList(self):
        qsoa = QSOAPlatform(configFile=True)

        deviceList = qsoa.getQuantumDeviceList(idSolution_gates)

        self.assertIsInstance(deviceList, dict)

    # BAD ARGUMENT idSolution
    def test_getQuantumDeviceList_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.getQuantumDeviceList(idSolution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumDeviceList_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.getQuantumDeviceList(idSolution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getQuantumDeviceList_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumDeviceList(idSolution_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM DEVICES_____##################
class Test_GetQuantumDevices(unittest.TestCase):

    # GET QUANTUM DEVICES
    def test_getQuantumDevices(self):
        qsoa = QSOAPlatform(configFile=True)

        devices = qsoa.getQuantumDevices(idSolution_gates)

        self.assertIsInstance(devices, list)

        firstDevice = devices[0]
        self.assertEqual(type(firstDevice).__name__, 'DeviceItem')

    # BAD ARGUMENT idSolution
    def test_getQuantumDevices_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.getQuantumDevices(idSolution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumDevices_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.getQuantumDevices(idSolution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getQuantumDevices_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumDevices(idSolution_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM DEVICE NAME_____##################
class Test_GetQuantumDeviceName(unittest.TestCase):

    # GET QUANTUM DEVICE NAME
    def test_getQuantumDeviceName(self):
        qsoa = QSOAPlatform(configFile=True)

        deviceName = qsoa.getQuantumDeviceName(idSolution_gates, idDevice_gates)

        self.assertIsInstance(deviceName, str)

    # BAD ARGUMENT idSolution
    def test_getQuantumDeviceName_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.getQuantumDeviceName(idSolution, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
    
    # BAD ARGUMENT idDevice
    def test_getQuantumDeviceName_badArgument_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        idDevice = 99

        try:
            qsoa.getQuantumDeviceName(idSolution_gates, idDevice)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'NonExistentItemError')

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumDeviceName_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.getQuantumDeviceName(idSolution, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idDevice
    def test_getQuantumDeviceName_badArgumentType_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        idDevice = 'id'

        try:
            qsoa.getQuantumDeviceName(idSolution_gates, idDevice)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getQuantumDeviceName_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumDeviceName(idSolution_gates, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM FLOW LIST_____##################
class Test_GetQuantumFlowList(unittest.TestCase):

    # GET QUANTUM FLOW LIST
    def test_getQuantumFlowList(self):
        qsoa = QSOAPlatform(configFile=True)

        flowList = qsoa.getQuantumFlowList(idSolution_gates)

        self.assertIsInstance(flowList, dict)

    # BAD ARGUMENT idSolution
    def test_getQuantumFlowList_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.getQuantumFlowList(idSolution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumFlowList_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.getQuantumFlowList(idSolution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getQuantumFlowList_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumFlowList(idSolution_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM FLOWS_____##################
class Test_GetQuantumDevices(unittest.TestCase):

    # GET QUANTUM FLOWS
    def test_getQuantumFlows(self):
        qsoa = QSOAPlatform(configFile=True)

        flows = qsoa.getQuantumFlows(idSolution_gates)

        self.assertIsInstance(flows, list)

        firstFlow = flows[0]
        self.assertEqual(type(firstFlow).__name__, 'FlowItem')

    # BAD ARGUMENT idSolution
    def test_getQuantumFlows_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.getQuantumFlows(idSolution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumFlows_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.getQuantumFlows(idSolution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getQuantumFlows_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumFlows(idSolution_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM FLOW NAME_____##################
class Test_GetQuantumFlowName(unittest.TestCase):

    # GET QUANTUM FLOW NAME
    def test_getQuantumFlowName(self):
        qsoa = QSOAPlatform(configFile=True)

        flowName = qsoa.getQuantumFlowName(idSolution_gates, idFlow_gates)

        self.assertIsInstance(flowName, str)

    # BAD ARGUMENT idSolution
    def test_getQuantumFlowName_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.getQuantumFlowName(idSolution, idFlow_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
    
    # BAD ARGUMENT idFlow
    def test_getQuantumFlowName_badArgument_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = 99

        try:
            qsoa.getQuantumFlowName(idSolution_gates, idFlow)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'NonExistentItemError')

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumFlowName_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.getQuantumFlowName(idSolution, idFlow_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idFlow
    def test_getQuantumFlowName_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = 'id'

        try:
            qsoa.getQuantumFlowName(idSolution_gates, idFlow)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getQuantumFlowName_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumFlowName(idSolution_gates, idFlow_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____RUN QUANTUM APPLICATION_____##################
class Test_RunQuantumApplication(unittest.TestCase):

    # RUN QUANTUM APPLICATION
    def test_runQuantumApplication(self):
        qsoa = QSOAPlatform(configFile=True)

        application = qsoa.runQuantumApplication(applicationName, idSolution_gates, idFlow_gates, idDevice_gates)
        waitForApplicationResponse(qsoa, application)

        self.assertEqual(type(application).__name__, 'Application')

    # BAD ARGUMENT idSolution
    def test_runQuantumApplication_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.runQuantumApplication(applicationName, idSolution, idFlow_gates, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
    
    # BAD ARGUMENT idFlow
    def test_runQuantumApplication_badArgument_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = 99

        try:
            qsoa.runQuantumApplication(applicationName, idSolution_gates, idFlow, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT idDevice
    def test_runQuantumApplication_badArgument_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        idDevice = 99

        try:
            qsoa.runQuantumApplication(applicationName, idSolution_gates, idFlow_gates, idDevice)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE applicationName
    def test_runQuantumApplication_badArgumentType_applicationName(self):
        qsoa = QSOAPlatform(configFile=True)

        applicationName = 99

        try:
            qsoa.runQuantumApplication(applicationName, idSolution_gates, idFlow_gates, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idSolution
    def test_runQuantumApplication_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.runQuantumApplication(applicationName, idSolution, idFlow_gates, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
    
    # BAD ARGUMENT TYPE idFlow
    def test_runQuantumApplication_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = '99'

        try:
            qsoa.runQuantumApplication(applicationName, idSolution_gates, idFlow, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idDevice
    def test_runQuantumApplication_badArgumentType_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        idDevice = '99'

        try:
            qsoa.runQuantumApplication(applicationName, idSolution_gates, idFlow_gates, idDevice)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_runQuantumApplication_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.runQuantumApplication(applicationName, idSolution_gates, idFlow_gates, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____RUN QUANTUM EXECUTION RESPONSE_____##################
class Test_RunQuantumExecutionResponse(unittest.TestCase):

    # GET QUANTUM EXECTUTION RESPONSE APPLICATION OBJECT
    def test_getQuantumExecutionResponse_applicationObject(self):
        qsoa = QSOAPlatform(configFile=True)

        application = qsoa.runQuantumApplication(applicationName, idSolution_gates, idFlow_gates, idDevice_gates)
        waitForApplicationResponse(qsoa, application)

        execution = qsoa.getQuantumExecutionResponse(application)

        self.assertEqual(type(execution).__name__, 'Execution')

    # GET QUANTUM EXECTUTION RESPONSE MANUALLY
    def test_getQuantumExecutionResponse_manually(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)

        self.assertEqual(type(execution).__name__, 'Execution')

    # MANUALLY BAD ARGUMENT executionToken
    def test_getQuantumExecutionResponse_manually_badArgument_executionToken(self):
        qsoa = QSOAPlatform(configFile=True)

        executionToken = '99'

        execution = qsoa.getQuantumExecutionResponse(executionToken, idSolution_gates, idFlow_gates)

        self.assertEqual(type(execution).__name__, 'Execution')

    # MANUALLY BAD ARGUMENT idSolution
    def test_getQuantumExecutionResponse_manually_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution, idFlow_gates)

        self.assertEqual(type(execution).__name__, 'Execution')

    # MANUALLY BAD ARGUMENT idFlow
    def test_getQuantumExecutionResponse_manually_badArgument_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = 99

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow)

        self.assertEqual(type(execution).__name__, 'Execution')

    # APPLICATION OBJECT BAD ARGUMENT TYPE application
    def test_getQuantumExecutionResponse_applicationObject_badArgumentType_application(self):
        qsoa = QSOAPlatform(configFile=True)

        application = 99

        try:
            qsoa.getQuantumExecutionResponse(application)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # MANUALLY BAD ARGUMENT TYPE executionToken
    def test_getQuantumExecutionResponse_manually_badArgumentType_executionToken(self):
        qsoa = QSOAPlatform(configFile=True)

        executionToken = 99

        try:
            qsoa.getQuantumExecutionResponse(executionToken, idSolution_gates, idFlow_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # MANUALLY BAD ARGUMENT TYPE idSolution
    def test_getQuantumExecutionResponse_manually_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = '99'

        try:
            qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution, idFlow_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # MANUALLY BAD ARGUMENT TYPE idFlow
    def test_getQuantumExecutionResponse_manually_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = '99'

        try:
            qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getQuantumExecutionResponse_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____REPRESENT RESULTS_____##################
class Test_RepresentResults(unittest.TestCase):

    # REPRESENT RESULTS GATES
    def test_representResults_gates(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)

        representation = qsoa.representResults(execution)

        self.assertIsNone(representation)

    # REPRESENT RESULTS GATES RESULT INDEX
    def test_representResults_gates_resultIndex(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)

        resultIndex = 0

        representation = qsoa.representResults(execution, resultIndex)

        self.assertIsNone(representation, resultIndex)
    
    # REPRESENT RESULTS ANNEALING
    def test_representResults_annealing(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_annealing, idSolution_annealing, idFlow_annealing)

        representation = qsoa.representResults(execution)

        self.assertIsInstance(representation, str)

    # REPRESENT RESULTS ANNEALING RESULT INDEX
    def test_representResults_annealing_resultIndex(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_annealing, idSolution_annealing, idFlow_annealing)

        resultIndex = 0

        representation = qsoa.representResults(execution, resultIndex)

        self.assertIsInstance(representation, str)

    # BAD ARGUMENT execution
    def test_representResults_badArgument_execution(self):
        qsoa = QSOAPlatform(configFile=True)

        executionToken = 'be2b3021-d294-472e-8265-3b39583ad172'
        execution = qsoa.getQuantumExecutionResponse(executionToken, idSolution_gates, idFlow_gates)

        try:
            qsoa.representResults(execution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ExecutionObjectError')

    # BAD ARGUMENT resultIndex
    def test_representResults_badArgument_resultIndex(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)

        try:
            qsoa.representResults(execution, 1)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'IndexError')

    # BAD ARGUMENT TYPE execution
    def test_representResults_badArgumentType_execution(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = 99

        try:
            qsoa.representResults(execution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE resultIndex
    def test_representResults_badArgumentType_resultIndex(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)
        resultIndex = '99'

        try:
            qsoa.representResults(execution, resultIndex)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_representResults_notloggedIn(self):
        qsoa = QSOAPlatform(configFile=True)
        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)
        qsoa = QSOAPlatform()

        try:
            qsoa.representResults(execution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET ASSET CATALOG_____##################
class Test_GetAssetCatalog(unittest.TestCase):

    # GET ASSET CATALOG
    def test_getAssetCatalog(self):
        qsoa = QSOAPlatform(configFile=True)

        assetCatalog = qsoa.getAssetCatalog(idSolution_gates, assetType_circuit, assetLevel_vl)

        self.assertIsInstance(assetCatalog, list)

        firstAsset = assetCatalog[0]
        self.assertEqual(type(firstAsset).__name__, 'Asset')

    # BAD ARGUMENT idSolution
    def test_getAssetCatalog_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.getAssetCatalog(idSolution, assetType_circuit, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetType
    def test_getAssetCatalog_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetType = 'assetType'

        try:
            qsoa.getAssetCatalog(idSolution_gates, assetType, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT assetLevel
    def test_getAssetCatalog_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 'assetLevel'

        try:
            qsoa.getAssetCatalog(idSolution_gates, assetType_circuit, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idSolution
    def test_getAssetCatalog_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.getAssetCatalog(idSolution, assetType_circuit, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetType
    def test_getAssetCatalog_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetType = 99

        try:
            qsoa.getAssetCatalog(idSolution_gates, assetType, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetLevel
    def test_getAssetCatalog_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 99

        try:
            qsoa.getAssetCatalog(idSolution_gates, assetType_circuit, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getAssetCatalog_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getAssetCatalog(idSolution_gates, assetType_circuit, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET ASSET_____##################
class Test_GetAsset(unittest.TestCase):

    # GET ASSET
    def test_getAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetType = 'CIRCUIT'
        assetLevel = 'VL'

        asset = qsoa.getAsset(idAsset, assetType, assetLevel)

        self.assertEqual(type(asset).__name__, 'Asset')

    # BAD ARGUMENT idAsset
    def test_getAsset_badArgument_idAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        idAsset = 99

        try:
            qsoa.getAsset(idAsset, assetType_circuit, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetType
    def test_getAsset_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetType = 'assetType'

        try:
            qsoa.getAsset(idAsset, assetType, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT assetLevel
    def test_getAsset_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 'assetLevel'

        try:
            qsoa.getAsset(idAsset, assetType_circuit, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idAsset
    def test_getAsset_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idAsset = 'id'

        try:
            qsoa.getAsset(idAsset, assetType_circuit, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetType
    def test_getAsset_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetType = 99

        try:
            qsoa.getAsset(idAsset, assetType, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetLevel
    def test_getAsset_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 99

        try:
            qsoa.getAsset(idAsset, assetType_circuit, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getAsset_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getAsset(idAsset, assetType_circuit, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____CREATE ASSET_____##################
class Test_CreateAsset(unittest.TestCase):

    # CREATE ASSET assetBody STRING
    def test_createAsset_assetBody_string(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl))

    # CREATE ASSET assetBody CIRCUITGATES
    def test_createAsset_assetBody_circuitGates(self):
        qsoa = QSOAPlatform(configFile=True)

        circuit = qsoa.CircuitGates()
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure()

        assetBody = circuit

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl))

    # CREATE ASSET assetBody CIRCUITFLOW
    def test_createAsset_assetBody_circuitFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        flow = qsoa.CircuitFlow()
        startNode = flow.startNode()
        circuitNode = flow.circuitNode('circuit')
        endNode = flow.endNode()
        flow.linkNodes(startNode, circuitNode)
        flow.linkNodes(circuitNode, endNode)

        assetBody = flow

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_flow, assetNamespace, assetDescription, assetBody, assetType_flow, assetLevel_vl)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_flow, assetLevel_vl))

    # CREATE ASSET EXISTING ASSET
    def test_createAsset_existingAsset(self):
        qsoa = QSOAPlatform(configFile=True)


        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl))

    # BAD ARGUMENT idSolution
    def test_createAsset_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.createAsset(idSolution, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetNamespace
    def test_createAsset_badArgument_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetNamespace = 'asset_namepace'

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetType
    def test_createAsset_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetType = 'assetType'

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT assetLevel
    def test_createAsset_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 'assetLevel'

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idSolution
    def test_createAsset_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.createAsset(idSolution, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetName
    def test_createAsset_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetName = 99

        try:
            qsoa.createAsset(idSolution_gates, assetName, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetNamespace
    def test_createAsset_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetNamespace = 99

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetDescription
    def test_createAsset_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        assetDescription = 99

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetBody
    def test_createAsset_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        assetBody = 99

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetType
    def test_createAsset_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetType = 99

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetLevel
    def test_createAsset_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 99

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_createAsset_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____CREATE ASSET FLOW_____##################
class Test_CreateAssetFlow(unittest.TestCase):

    # CREATE ASSET FLOW assetBody STRING
    def test_createAssetFlow_assetBody_string(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_flow, assetLevel_vl))

    # CREATE ASSET FLOW assetBody CIRCUITFLOW
    def test_createAssetFlow_assetBody_circuitFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        flow = qsoa.CircuitFlow()
        startNode = flow.startNode()
        circuitNode = flow.circuitNode('circuit')
        endNode = flow.endNode()
        flow.linkNodes(startNode, circuitNode)
        flow.linkNodes(circuitNode, endNode)

        assetBody = flow

        assetManagementData = qsoa.createAssetFlow(idSolution_gates, assetName_flow, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_flow, assetLevel_vl))
    
    # CREATE ASSET FLOW PUBLISH
    def test_createAssetFlow_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        publish = True

        assetManagementData = qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl, publish)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_flow, assetLevel_vl))

    # CREATE ASSET FLOW EXISTING ASSET
    def test_createAssetFlow_existingAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_flow, assetLevel_vl))

    # BAD ARGUMENT idSolution
    def test_createAssetFlow_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.createAssetFlow(idSolution, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetNamespace
    def test_createAssetFlow_badArgument_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetNamespace = 'asset_namepace'

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetLevel
    def test_createAssetFlow_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 'assetLevel'

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
    
    # BAD ARGUMENT publish
    def test_createAssetFlow_badArgument_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        publish = 99

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl, publish)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idSolution
    def test_createAssetFlow_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.createAssetFlow(idSolution, assetName_circuit, assetNamespace, assetDescription, assetBody,assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetName
    def test_createAssetFlow_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetName = 99

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetNamespace
    def test_createAssetFlow_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetNamespace = 99

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetDescription
    def test_createAssetFlow_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        assetDescription = 99

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetBody
    def test_createAssetFlow_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        assetBody = 99

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetLevel
    def test_createAssetFlow_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 99

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE publish
    def test_createAssetFlow_badArgumentType_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        publish = 99

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl, publish)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_createAssetFlow_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____PUBLISH FLOW_____##################

class Test_PublishFlow(unittest.TestCase):

    # PUBLISH FLOW
    def test_publishFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = 596
        publish = True

        published = qsoa.publishFlow(idFlow, publish)

        self.assertIsInstance(published, bool)

    # BAD ARGUMENT idFlow
    def test_publishFlow_badArgument_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = 99
        publish = True

        try:
            qsoa.publishFlow(idFlow, publish)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE idFlow
    def test_publishFlow_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = '99'
        publish = True

        try:
            qsoa.publishFlow(idFlow, publish)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE publish
    def test_publishFlow_badArgumentType_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = 596
        publish = 99

        try:
            qsoa.publishFlow(idFlow, publish)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_publishFlow_notloggedIn(self):
        qsoa = QSOAPlatform()

        idFlow = 596
        publish = True

        try:
            qsoa.publishFlow(idFlow, publish)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____UPDATE ASSET_____##################
class Test_UpdateAsset(unittest.TestCase):

    # UPDATE ASSET
    def test_updateAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetName = 'newAssetName'
        new_assetNamespace = 'newAssetNamespace'
        new_assetDescription = 'newAssetDescription'
        new_assetBody = 'circuit={"cols":[["H"]]}'

        assetManagementData = qsoa.updateAsset(asset, new_assetName, new_assetNamespace, new_assetDescription, new_assetBody, assetType_gates, assetLevel_vl)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')

        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        self.assertEqual(asset.getName(), new_assetName)
        self.assertEqual(asset.getNamespace(), new_assetNamespace)
        self.assertEqual(asset.getDescription(), new_assetDescription)
        self.assertEqual(asset.getBody(), new_assetBody)
        self.assertEqual(asset.getType(), assetType_gates)
        self.assertEqual(asset.getLevel(), assetLevel_vl)
        qsoa.deleteAsset(asset)
    
    # UPDATE ASSET EXISTING NAME
    def test_updateAsset_existingName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData1 = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        assetManagementData2 = qsoa.createAsset(idSolution_gates, assetName_circuit+'2', assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData2.getIdAsset(), assetType_circuit, assetLevel_vl)

        try:
            qsoa.updateAsset(asset, assetName_circuit)
        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData1.getIdAsset(), assetType_circuit, assetLevel_vl))
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT QUANTITY
    def test_updateAsset_badArgumentQuantity(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetNamespace
    def test_updateAsset_badArgument_username(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetNamespace = 'new_assetNamespace'

        try:
            qsoa.updateAsset(asset, assetNamespace=new_assetNamespace)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetType
    def test_updateAsset_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 'circuit={"cols":[["H"]]}'
        new_assetType = 'new_assetType'

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType=new_assetType)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetLevel
    def test_updateAsset_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 'circuit={"cols":[["H"]]}'
        new_assetLevel = 'new_assetLevel'

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType=assetType_gates, assetLevel=new_assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE asset
    def test_updateAsset_badArgumentType_asset(self):
        qsoa = QSOAPlatform(configFile=True)

        asset = 99

        try:
            qsoa.updateAsset(asset)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetName
    def test_updateAsset_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetName = 99

        try:
            qsoa.updateAsset(asset, assetName=new_assetName)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetNamespace
    def test_updateAsset_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetNamespace = 99

        try:
            qsoa.updateAsset(asset, assetNamespace=new_assetNamespace)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetDescription
    def test_updateAsset_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetDescription = 99

        try:
            qsoa.updateAsset(asset, assetDescription=new_assetDescription)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetBody
    def test_updateAsset_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 99

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetType
    def test_updateAsset_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 'circuit={"cols":[["H"]]}'
        new_assetType = 99

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType=new_assetType)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetLevel
    def test_updateAsset_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 'circuit={"cols":[["H"]]}'
        new_assetLevel = 99

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType=assetType_gates, assetLevel=new_assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # NOT LOGGED IN
    def test_updateAsset_notloggedIn(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        qsoa = QSOAPlatform()

        try:
            qsoa.updateAsset(asset)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')
        
        qsoa = QSOAPlatform(configFile=True)
        qsoa.deleteAsset(asset)


##################_____GET ASSET MANAGEMENT RESULT_____##################
class Test_GetAssetManagementResult(unittest.TestCase):

    # GET ASSET MANAGEMENT RESULT
    def test_getAssetManagementResult(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        lifecycleToken = assetManagementData.getLifecycleToken()

        assetManagementResult = qsoa.getAssetManagementResult(lifecycleToken)

        self.assertEqual(type(assetManagementResult).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl))

    # BAD ARGUMENT lifecycleToken
    def test_getAssetManagementResult_badArgument_lifecycleToken(self):
        qsoa = QSOAPlatform(configFile=True)

        lifecycleToken = 'lifecycleToken'

        try:
            qsoa.getAssetManagementResult(lifecycleToken)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE lifecycleToken
    def test_getAssetManagementResult_badArgumentType_lifecycleToken(self):
        qsoa = QSOAPlatform(configFile=True)

        lifecycleToken = 99

        try:
            qsoa.getAssetManagementResult(lifecycleToken)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getAssetManagementResult_notloggedIn(self):
        qsoa = QSOAPlatform()

        lifecycleToken = 'lifecycleToken'

        try:
            qsoa.getAssetManagementResult(lifecycleToken)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____DELETE ASSET_____##################
class Test_DeleteAsset(unittest.TestCase):

    # DELETE ASSET
    def test_deleteAsset_asset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        assetDeleted = qsoa.deleteAsset(asset)

        self.assertTrue(assetDeleted)

    # DELETE ASSET MANUALLY
    def test_deleteAsset_asset_manually(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        idAsset = asset.getId()

        assetDeleted = qsoa.deleteAsset(idAsset, assetType_circuit)

        self.assertTrue(assetDeleted)

    # BAD ARGUMENT idAsset
    def test_deleteAsset_badArgument_idAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        idAsset = 99

        try:
            qsoa.deleteAsset(idAsset, assetType_circuit)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetType
    def test_deleteAsset_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        idAsset = asset.getId()
        assetType = 'assetType'

        try:
            qsoa.deleteAsset(idAsset, assetType)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE asset
    def test_deleteAsset_badArgumentType_asset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        asset = 99

        try:
            qsoa.deleteAsset(asset)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl))

    # BAD ARGUMENT TYPE idAsset
    def test_deleteAsset_badArgumentType_idAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        idAsset = 'id'

        try:
            qsoa.deleteAsset(idAsset, assetType_circuit)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetType
    def test_deleteAsset_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        idAsset = asset.getId()
        assetType = 99

        try:
            qsoa.deleteAsset(idAsset, assetType)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # NOT LOGGED IN
    def test_deleteAsset_notloggedIn(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        qsoa = QSOAPlatform()

        try:
            qsoa.deleteAsset(asset)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')
        
        qsoa = QSOAPlatform(configFile=True)
        qsoa.deleteAsset(asset)


##################_____GET QUANTUM EXECUTION HISTORIC_____##################
class Test_GetQuantumExecutionHistoric(unittest.TestCase):

    # GET QUANTUM EXECUTION HISTORIC
    def test_getQuantumExecutionHistoric(self):
        qsoa = QSOAPlatform(configFile=True)

        quantumExecutionHistoryEntryList = qsoa.getQuantumExecutionHistoric(idSolution_gates)

        self.assertNotEqual(quantumExecutionHistoryEntryList, list)

        firstExecutionHistoryEntry = quantumExecutionHistoryEntryList[0]
        self.assertEqual(type(firstExecutionHistoryEntry).__name__, 'QuantumExecutionHistoryEntry')
    
    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumExecutionHistoric_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.getQuantumExecutionHistoric(idSolution=idSolution)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idFlow
    def test_getQuantumExecutionHistoric_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = 'id'

        try:
            qsoa.getQuantumExecutionHistoric(idFlow=idFlow)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idDevice
    def test_getQuantumExecutionHistoric_badArgumentType_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        idDevice = 'id'

        try:
            qsoa.getQuantumExecutionHistoric(idDevice=idDevice)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE dateFrom
    def test_getQuantumExecutionHistoric_badArgumentType_dateFrom(self):
        qsoa = QSOAPlatform(configFile=True)

        dateFrom = 99

        try:
            qsoa.getQuantumExecutionHistoric(dateFrom=dateFrom)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE isSimulator
    def test_getQuantumExecutionHistoric_badArgumentType_isSimulator(self):
        qsoa = QSOAPlatform(configFile=True)

        isSimulator = 99

        try:
            qsoa.getQuantumExecutionHistoric(isSimulator=isSimulator)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE top
    def test_getQuantumExecutionHistoric_badArgumentType_top(self):
        qsoa = QSOAPlatform(configFile=True)

        top = 'top'

        try:
            qsoa.getQuantumExecutionHistoric(top=top)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE resultType
    def test_getQuantumExecutionHistoric_badArgumentType_resultType(self):
        qsoa = QSOAPlatform(configFile=True)

        resultType = 99

        try:
            qsoa.getQuantumExecutionHistoric(resultType=resultType)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getQuantumExecutionHistoric_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumExecutionHistoric(idSolution_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM EXECUTION HISTORIC RESULT_____##################
class Test_GetQuantumExecutionHistoricResult(unittest.TestCase):

    # GET QUANTUM EXECUTION HISTORIC RESULT
    def test_getQuantumExecutionHistoricResult(self):
        qsoa = QSOAPlatform(configFile=True)

        quantumExecutionHistoryEntryList = qsoa.getQuantumExecutionHistoric(idSolution_gates)
        idResult = quantumExecutionHistoryEntryList[0].getIdResult()

        quantumExecutionHistoryEntry = qsoa.getQuantumExecutionHistoricResult(idResult)

        self.assertEqual(type(quantumExecutionHistoryEntry).__name__, 'QuantumExecutionHistoryEntry')
    
    # BAD ARGUMENT TYPE idResult
    def test_getQuantumExecutionHistoricResult_badArgumentType_idResult(self):
        qsoa = QSOAPlatform(configFile=True)

        idResult = 'id'

        try:
            qsoa.getQuantumExecutionHistoricResult(idResult)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_getQuantumExecutionHistoricResult_notloggedIn(self):
        qsoa = QSOAPlatform(configFile=True)

        quantumExecutionHistoryEntryList = qsoa.getQuantumExecutionHistoric(idSolution_gates)
        idResult = quantumExecutionHistoryEntryList[0].getIdResult()

        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumExecutionHistoricResult(idResult)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____RUN QUANTUM APPLICATION SYNC_____##################
class Test_RunQuantumApplicationSync(unittest.TestCase):

    # RUN QUANTUM APPLICATION SYNC
    def test_runQuantumApplicationSync(self):
        qsoa = QSOAPlatform(configFile=True)

        application = qsoa.runQuantumApplicationSync(applicationName, idSolution_gates, idFlow_gates, idDevice_gates)

        self.assertEqual(type(application).__name__, 'Application')

    # BAD ARGUMENT idSolution
    def test_runQuantumApplicationSync_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.runQuantumApplicationSync(applicationName, idSolution, idFlow_gates, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
    
    # BAD ARGUMENT idFlow
    def test_runQuantumApplicationSync_badArgument_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = 99

        try:
            qsoa.runQuantumApplicationSync(applicationName, idSolution_gates, idFlow, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT idDevice
    def test_runQuantumApplicationSync_badArgument_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        idDevice = 99

        try:
            qsoa.runQuantumApplicationSync(applicationName, idSolution_gates, idFlow_gates, idDevice)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE applicationName
    def test_runQuantumApplicationSync_badArgumentType_applicationName(self):
        qsoa = QSOAPlatform(configFile=True)

        applicationName = 99

        try:
            qsoa.runQuantumApplicationSync(applicationName, idSolution_gates, idFlow_gates, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idSolution
    def test_runQuantumApplicationSync_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.runQuantumApplicationSync(applicationName, idSolution, idFlow_gates, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
    
    # BAD ARGUMENT TYPE idFlow
    def test_runQuantumApplicationSync_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        idFlow = '99'

        try:
            qsoa.runQuantumApplicationSync(applicationName, idSolution_gates, idFlow, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idDevice
    def test_runQuantumApplicationSync_badArgumentType_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        idDevice = '99'

        try:
            qsoa.runQuantumApplicationSync(applicationName, idSolution_gates, idFlow_gates, idDevice)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_runQuantumApplicationSync_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.runQuantumApplicationSync(applicationName, idSolution_gates, idFlow_gates, idDevice_gates)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____CREATE ASSET SYNC_____##################
class Test_CreateAssetSync(unittest.TestCase):

    # CREATE ASSET SYNC assetBody STRING
    def test_createAssetSync_assetBody_string(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl))

    # CREATE ASSET SYNC assetBody CIRCUITGATES
    def test_createAssetSync_assetBody_circuitGates(self):
        qsoa = QSOAPlatform(configFile=True)

        circuit = qsoa.CircuitGates()
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure()

        assetBody = circuit

        assetManagementData = qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl))

    # CREATE ASSET SYNC assetBody CIRCUITFLOW
    def test_createAssetSync_assetBody_circuitFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        flow = qsoa.CircuitFlow()
        startNode = flow.startNode()
        circuitNode = flow.circuitNode('circuit')
        endNode = flow.endNode()
        flow.linkNodes(startNode, circuitNode)
        flow.linkNodes(circuitNode, endNode)

        assetBody = flow

        assetManagementData = qsoa.createAssetSync(idSolution_gates, assetName_flow, assetNamespace, assetDescription, assetBody, assetType_flow, assetLevel_vl)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_flow, assetLevel_vl))

    # CREATE ASSET SYNC EXISTING ASSET
    def test_createAsset_existingAsset(self):
        qsoa = QSOAPlatform(configFile=True)


        assetManagementData = qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl))

    # BAD ARGUMENT idSolution
    def test_createAssetSync_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.createAssetSync(idSolution, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetNamespace
    def test_createAssetSync_badArgument_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetNamespace = 'asset_namepace'

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetType
    def test_createAssetSync_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetType = 'assetType'

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT assetLevel
    def test_createAssetSync_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 'assetLevel'

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idSolution
    def test_createAssetSync_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.createAssetSync(idSolution, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetName
    def test_createAssetSync_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetName = 99

        try:
            qsoa.createAssetSync(idSolution_gates, assetName, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetNamespace
    def test_createAssetSync_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetNamespace = 99

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetDescription
    def test_createAssetSync_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        assetDescription = 99

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetBody
    def test_createAssetSync_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        assetBody = 99

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetType
    def test_createAssetSync_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetType = 99

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetLevel
    def test_createAssetSync_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 99

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_createAssetSync_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____CREATE ASSET FLOW SYNC_____##################
class Test_CreateAssetFlowSync(unittest.TestCase):

    # CREATE ASSET FLOW SYNC assetBody STRING
    def test_createAssetFlowSync_assetBody_string(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_flow, assetLevel_vl))

    # CREATE ASSET FLOW SYNC assetBody CIRCUITFLOW
    def test_createAssetFlowSync_assetBody_circuitFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        flow = qsoa.CircuitFlow()
        startNode = flow.startNode()
        circuitNode = flow.circuitNode('circuit')
        endNode = flow.endNode()
        flow.linkNodes(startNode, circuitNode)
        flow.linkNodes(circuitNode, endNode)

        assetBody = flow

        assetManagementData = qsoa.createAssetFlowSync(idSolution_gates, assetName_flow, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_flow, assetLevel_vl))
    
    # CREATE ASSET FLOW SYNC PUBLISH
    def test_createAssetFlowSync_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        publish = True

        assetManagementData = qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl, publish)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_flow, assetLevel_vl))

    # CREATE ASSET FLOW SYNC EXISTING ASSET
    def test_createAssetFlowSync_existingAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), assetType_flow, assetLevel_vl))

    # BAD ARGUMENT idSolution
    def test_createAssetFlowSync_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 99

        try:
            qsoa.createAssetFlowSync(idSolution, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetNamespace
    def test_createAssetFlowSync_badArgument_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetNamespace = 'asset_namepace'

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetLevel
    def test_createAssetFlowSync_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 'assetLevel'

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
    
    # BAD ARGUMENT publish
    def test_createAssetFlowSync_badArgument_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        publish = 99

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl, publish)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE idSolution
    def test_createAssetFlowSync_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.createAssetFlowSync(idSolution, assetName_circuit, assetNamespace, assetDescription, assetBody,assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetName
    def test_createAssetFlowSync_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetName = 99

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetNamespace
    def test_createAssetFlowSync_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetNamespace = 99

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetDescription
    def test_createAssetFlowSync_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        assetDescription = 99

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetBody
    def test_createAssetFlowSync_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        assetBody = 99

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetLevel
    def test_createAssetFlowSync_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 99

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE publish
    def test_createAssetFlowSync_badArgumentType_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        publish = 99

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl, publish)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # NOT LOGGED IN
    def test_createAssetFlowSync_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel_vl)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____UPDATE ASSET SYNC_____##################
class Test_UpdateAssetSync(unittest.TestCase):

    # UPDATE ASSET SYNC
    def test_updateAssetSync(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetName = 'test_newAssetName'
        new_assetNamespace = 'newAssetNamespace'
        new_assetDescription = 'newAssetDescription'
        new_assetBody = 'circuit={"cols":[["H"]]}'

        assetManagementResult = qsoa.updateAssetSync(asset, new_assetName, new_assetNamespace, new_assetDescription, new_assetBody, assetType_gates, assetLevel_vl)

        self.assertEqual(type(assetManagementResult).__name__, 'AssetManagementResult')

        asset = qsoa.getAsset(assetManagementResult.getIdAsset(), assetType_circuit, assetLevel_vl)

        self.assertEqual(asset.getName(), new_assetName)
        self.assertEqual(asset.getNamespace(), new_assetNamespace)
        self.assertEqual(asset.getDescription(), new_assetDescription)
        self.assertEqual(asset.getBody(), new_assetBody)
        self.assertEqual(asset.getType(), assetType_gates)
        self.assertEqual(asset.getLevel(), assetLevel_vl)
        qsoa.deleteAsset(asset)
    
    # UPDATE ASSET SYNC EXISTING NAME
    def test_updateAssetSync_existingName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData1 = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        assetManagementData2 = qsoa.createAsset(idSolution_gates, assetName_circuit+'2', assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData2.getIdAsset(), assetType_circuit, assetLevel_vl)

        try:
            qsoa.updateAssetSync(asset, assetName_circuit)
        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData1.getIdAsset(), assetType_circuit, assetLevel_vl))
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT QUANTITY
    def test_updateAssetSync_badArgumentQuantity(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAssetSync(asset, assetBody=new_assetBody)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetNamespace
    def test_updateAsset_badArgument_username(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetNamespace = 'new_assetNamespace'

        try:
            qsoa.updateAsset(asset, assetNamespace=new_assetNamespace)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetType
    def test_updateAsset_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 'circuit={"cols":[["H"]]}'
        new_assetType = 'new_assetType'

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType=new_assetType)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetLevel
    def test_updateAsset_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 'circuit={"cols":[["H"]]}'
        new_assetLevel = 'new_assetLevel'

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType=assetType_gates, assetLevel=new_assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE asset
    def test_updateAsset_badArgumentType_asset(self):
        qsoa = QSOAPlatform(configFile=True)

        asset = 99

        try:
            qsoa.updateAsset(asset)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE assetName
    def test_updateAsset_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetName = 99

        try:
            qsoa.updateAsset(asset, assetName=new_assetName)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetNamespace
    def test_updateAsset_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetNamespace = 99

        try:
            qsoa.updateAsset(asset, assetNamespace=new_assetNamespace)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetDescription
    def test_updateAsset_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetDescription = 99

        try:
            qsoa.updateAsset(asset, assetDescription=new_assetDescription)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetBody
    def test_updateAsset_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 99

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetType
    def test_updateAsset_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 'circuit={"cols":[["H"]]}'
        new_assetType = 99

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType=new_assetType)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetLevel
    def test_updateAsset_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        new_assetBody = 'circuit={"cols":[["H"]]}'
        new_assetLevel = 99

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType=assetType_gates, assetLevel=new_assetLevel)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
        
        qsoa.deleteAsset(asset)

    # NOT LOGGED IN
    def test_updateAsset_notloggedIn(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetType_gates, assetLevel_vl)
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), assetType_circuit, assetLevel_vl)

        qsoa = QSOAPlatform()

        try:
            qsoa.updateAsset(asset)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')
        
        qsoa = QSOAPlatform(configFile=True)
        qsoa.deleteAsset(asset)


if __name__ == '__main__':
    unittest.main()