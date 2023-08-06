import unittest
from QuantumPathQSOAPySDK import QSOAPlatform


class Test_CircuitAnnealing(unittest.TestCase):

    # EMPTY CIRCUIT
    def test_createCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitAnnealing() # create circuit

        self.assertEqual(circuit.getCircuitBody(), {'Parameters': [], 'AuxData': [], 'Classes': [], 'Variables': [], 'Rules': []}) # check circuit body
    

    # ADD PARAMETERS
    def test_addParameters(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitAnnealing() # create circuit

        parameter1 = circuit.Parameter('FirstParameter', 1) # create parameter
        parameter2 = circuit.Parameter('SecondParameter', 2) # create parameter

        circuit.addParameter(parameter1) # add parameter
        circuit.addParameter(parameter2) # add parameter

        for elem in circuit.getCircuitBody()['Parameters']: # replace generated uiID values to 'uiID'
            elem['uiID'] = 'uiID'
    
        self.assertEqual(parameter1.getName(), 'FirstParameter') # check first parameter name
        self.assertEqual(parameter1.getValue(), '1') # check first parameter value
        self.assertEqual(circuit.getCircuitBody()['Parameters'], [
            {'Name': 'FirstParameter', 'Value': '1', 'uiID': 'uiID'},
            {'Name': 'SecondParameter', 'Value': '2', 'uiID': 'uiID'}
        ]) # check all circuit parameters
        

    # ADD AUXILIARY DATA
    def test_addAuxData(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitAnnealing() # create circuit

        auxData1 = circuit.AuxData('FirstAuxData', [4, 1, 2, 3, 5]) # create axiliary data
        auxData2 = circuit.AuxData('SecondAuxData', [1, 2, 3, 4, 4]) # create axiliary data

        circuit.addAuxData(auxData1) # add axiliary data
        circuit.addAuxData(auxData2) # add axiliary data

        for elem in circuit.getCircuitBody()['AuxData']: # replace generated uiID values to 'uiID'
            elem['uiID'] = 'uiID'

        self.assertEqual(auxData1.getName(), 'FirstAuxData') # check auxiliary data name
        self.assertEqual(auxData1.getValue(), '[4, 1, 2, 3, 5]') # check auxiliary data value
        self.assertEqual(circuit.getCircuitBody()['AuxData'], [
            {'uiID': 'uiID', 'Name': 'FirstAuxData', 'Value': '[4, 1, 2, 3, 5]'},
            {'uiID': 'uiID', 'Name': 'SecondAuxData', 'Value': '[1, 2, 3, 4, 4]'}
        ]) # check all circuit auxiliary data


    # ADD CLASSES
    def test_addClasses(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitAnnealing() # create circuit
    
        class1 = circuit.Class('FirstClass', 5) # create class
        class2 = circuit.Class('SecondClass', 2) # create class

        class1.addProperty('FirstClassProperties', [1, 2, 3, 4, 5]) # add property
        class2.addProperty('SecondClassProperties', [1, 2]) # add property

        circuit.addClass(class1) # add class
        circuit.addClass(class2) # add class

        for elem in circuit.getCircuitBody()['Classes']: # replace generated uiID values to 'uiID'
            elem['uiID'] = 'uiID'

            if elem['Properties']:
                for e in elem['Properties']:
                    e['uiID'] = 'uiID'
        
        self.assertEqual(class1.getName(), 'FirstClass') # check class name
        self.assertEqual(class1.getNumberOfVars(), '5') # # check number of variables
        self.assertEqual(circuit.getCircuitBody()['Classes'], [
            {'Properties': [{'uiID': 'uiID', 'Name': 'FirstClassProperties', 'Values': [1, 2, 3, 4, 5]}],
                'uiID': 'uiID', 'Name': 'FirstClass', 'NumberOfVars': '5', 'Description': ''
            },
            {'Properties': [{'uiID': 'uiID', 'Name': 'SecondClassProperties', 'Values': [1, 2]}],
                'uiID': 'uiID', 'Name': 'SecondClass', 'NumberOfVars': '2', 'Description': ''}
        ]) # check all circuit classes
    

    # ADD VARIABLES
    def test_addVariables(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitAnnealing() # create circuit
        class1 = circuit.Class('FirstClass', 5) # existing circuit
        class2 = circuit.Class('SecondClass', 2) # existing circuit
        class1.addProperty('FirstClassProperties', [1, 2, 3, 4, 5]) # existing circuit
        class2.addProperty('SecondClassProperties', [1, 2]) # existing circuit
        circuit.addClass(class1) # existing circuit
        circuit.addClass(class2) # existing circuit

        variable1 = circuit.Variable('FirstVariable', [class1]) # create variable
        variable2 = circuit.Variable('SecondVariable', [class1, class2]) # create variable

        circuit.addVariable(variable1) # add variable
        circuit.addVariable(variable2) # add variable

        for elem in circuit.getCircuitBody()['Variables']: # replace generated uiID values to 'uiID'
            elem['uiID'] = 'uiID'

            for i in range(len(elem['Classes'])):
                elem['Classes'][i] = 'uiID'

        self.assertEqual(variable1.getName(), 'FirstVariable') # check variable name
        self.assertEqual(circuit.getCircuitBody()['Variables'], [
            {'Classes': ['uiID'], 'uiID': 'uiID', 'Name': 'FirstVariable', 'Description': ''},
            {'Classes': ['uiID', 'uiID'], 'uiID': 'uiID', 'Name': 'SecondVariable', 'Description': ''}
        ]) # check all circuit variables
    

    # ADD RULES
    def test_addRules(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitAnnealing() # create circuit

        rule1 = circuit.Rule('FirstRule', 1) # create rule
        rule2 = circuit.Rule('SecondRule', 2) # create rule

        circuit.addRule(rule1) # add rule
        circuit.addRule(rule2) # add rule

        self.assertEqual(rule1.getName(), 'FirstRule') # check rule name
        self.assertEqual(rule1.getLambda(), '1') # check rule lambda

        for elem in circuit.getCircuitBody()['Rules']: # replace generated uiID values to 'uiID'
            elem['uiID'] = 'uiID'

        self.assertEqual(circuit.getCircuitBody()['Rules'], [
            {'Expressions': [], 'uiID': 'uiID', 'Name': 'FirstRule', 'Lambda': '1', 'Description': ''},
            {'Expressions': [], 'uiID': 'uiID', 'Name': 'SecondRule', 'Lambda': '2', 'Description': ''}
        ]) # check all circuit variables



if __name__ == '__main__':
    unittest.main()