import unittest
from QuantumPathQSOAPySDK import QSOAPlatform


##################_____TEST GENERAL POSITIONING_____##################
class Test_GeneralPositioning(unittest.TestCase):
    
    # ADD MULTIPLE GATE Q0, Q2 EMPTY CIRCUIT
    def test_addMultipleGate_q0q2_emptyCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.cx(0, 2) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 1, 'X']]) # check circuit body

    # ADD MULTIPLE GATE Q2, Q0 EMPTY CIRCUIT
    def test_addMultipleGate_q2q0_emptyCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.cx(2, 0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['X', 1, 'CTRL']]) # check circuit body

    # ADD MULTIPLE GATE Q1, Q3 EMPTY CIRCUIT
    def test_addMultipleGate_q1q3_emptyCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.cx(1, 3) # add gate

        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 1, 'X']]) # check circuit body

    # ADD MULTIPLE GATE Q1, Q2 CIRCUIT Q0
    def test_addMultipleGate_q1q2_circuit_q0(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.h(0) # existing circuit

        circuit.cx(1, 2) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'X']]) # check circuit body
    
    # ADD MULTIPLE GATE Q0, Q1, Q3 EMPTY CIRCUIT
    def test_addMultipleGate_q0q1q3_emptyCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.ccx(0, 1, 3) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 1, 'X']]) # check circuit body

    # ADD MULTIPLE GATE Q0, Q3, Q1 EMPTY CIRCUIT
    def test_addMultipleGate_q0q3q1_emptyCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.ccx(0, 3, 1) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X', 1, 'CTRL']]) # check circuit body
    
    # ADD MULTIPLE GATE Q2, Q3, Q0 EMPTY CIRCUIT
    def test_addMultipleGate_q2q3q0_emptyCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.ccx(2, 3, 0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['X', 1, 'CTRL', 'CTRL']]) # check circuit body


##################_____TEST SWAP GATE_____##################
class Test_SwapGate(unittest.TestCase):
    
    # ADD SWAP GATE Q0, Q1 EMPTY CIRCUIT
    def test_addSwapGate_q0q1_emptyCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.swap(0, 1) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap']]) # check circuit body
    
    # ADD SWAP GATE Q0, Q1 MEASURE Q0
    def test_addSwapGate_q0q1_measure_q0(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.measure(0) # existing circuit

        circuit.swap(0, 1) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['Measure'], ['Swap', 'Swap']]) # check circuit body
        self.assertEqual(circuit.getClassicRegisters(), {1}) # check classic registers
    
    # ADD SWAP GATE Q0, Q1 MEASURE Q1
    def test_addSwapGate_q0q1_measure_q1(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.measure(1) # existing circuit

        circuit.swap(0, 1) # add gate

        self.assertEqual(circuit.getCircuitBody(), [[1, 'Measure'], ['Swap', 'Swap']]) # check circuit body
        self.assertEqual(circuit.getClassicRegisters(), {0}) # check classic registers
    
    # ADD SWAP GATE Q0, Q1 MEASURE Q0, Q1
    def test_addSwapGate_q0q1_measure_q0q1(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.measure(0) # existing circuit
        circuit.measure(1) # existing circuit

        circuit.swap(0, 1) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['Measure'], [1, 'Measure'], ['Swap', 'Swap']]) # check circuit body
        self.assertEqual(circuit.getClassicRegisters(), {0, 1}) # check classic registers
    
    # ADD CONTROL SWAP GATE Q0, Q1, Q2 MEASURE Q2
    def test_addControlSwapGate_q0q1q2_measure_q2(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.measure(2) # existing circuit

        cswap = circuit.control( # create cccx gate, add control
            0, circuit.swap(1, 2, False) # add swap gate
        )

        circuit.addCreatedGate(cswap) # add cswap gate

        self.assertEqual(circuit.getCircuitBody(), [[1, 1, 'Measure']]) # check circuit body


##################_____TEST MULTIPLE GATES WITHOUT PREVIUOUS MEASURE_____##################
class Test_Multiple_WithoutPreviousMeasure(unittest.TestCase):
    
    # ADD MULTIPLE GATE Q0, Q1 MEASURE Q1
    def test_addMultiple_q0q1_measure_q1(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.measure(1) # existing circuit

        circuit.cx(0, 1) # add gate

        self.assertEqual(circuit.getCircuitBody(), [[1, 'Measure']]) # check circuit body

    # ALL MULTIPLE GATES WITHOUT PREVIUOUS MEASURE
    def test_multipleGates_noPreviousMeasure(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.ch(1, 2) # add gate
        circuit.cx(1, 2) # add gate
        circuit.ccx(0, 1, 2) # add gate

        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 'H'], [1, 'CTRL', 'X'], ['CTRL', 'CTRL', 'X']]) # check circuit body


##################_____TEST MULTIPLE CONTROL GATES_____##################
class Test_MultipleControlGate(unittest.TestCase):

    # ADD MULTIPLE CONTROL GATE CONTROL Q0 TARGET Q1
    def test_addMultipleControlGate_controlq0_targetq1(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.mcg(0, circuit.x(1, False)) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']]) # check circuit body
    
    # ADD MULTIPLE CONTROL GATE MANUAL LIST CONTROL Q0, Q2, Q3 TARGET Q4
    def test_addMultipleControlGate_manualList_controlq0q2q3_targetq4(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.mcg([0, 2, 3], circuit.x(4, False)) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 1, 'CTRL', 'CTRL', 'X']]) # check circuit body

    # ADD MULTIPLE CONTROL GATE AUTOMATED LIST CONTROL Q0, Q1, Q2 TARGET Q3
    def test_addMultipleControlGate_automatedList_controlq0q1q2_targetq3(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.mcg([i for i in range(3)], circuit.x(3, False)) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 'CTRL', 'X']]) # check circuit body


if __name__ == '__main__':
    unittest.main()