import unittest
from QuantumPathQSOAPySDK import QSOAPlatform


##################_____TEST GENERAL POSITIONING_____##################
class Test_GeneralPositioning(unittest.TestCase):

    # EMPTY CIRCUIT
    def test_emptyCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # ADD SIMPLE GATE Q0 EMPTY CIRCUIT
    def test_addSimpleGate_q0_emptyCircuit(self):
        qsoa = QSOAPlatform()

        circuit = qsoa.CircuitGates() # create circuit

        circuit.x(0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['X']]) # check circuit body

    # ADD SIMPLE GATE Q2 EMPTY CIRCUIT
    def test_addSimpleGate_q2_emptyCircuit(self):
        qsoa = QSOAPlatform()

        circuit = qsoa.CircuitGates() # create circuit

        circuit.x(2) # add gate

        self.assertEqual(circuit.getCircuitBody(), [[1, 1, 'X']]) # check circuit body

    # ADD SIMPLE GATE Q0 CIRCUIT Q2
    def test_addSimpleGate_q0_circuit_q2(self):
        qsoa = QSOAPlatform()

        circuit = qsoa.CircuitGates() # create circuit
        circuit.x(2) # existing circuit

        circuit.x(0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['X', 1, 'X']]) # check circuit body

    # ADD SIMPLE GATE Q0 CIRCUIT Q0, Q2
    def test_addSimpleGate_q0_circuit_q0q2(self):
        qsoa = QSOAPlatform()

        circuit = qsoa.CircuitGates() # create circuit
        circuit.x(0) # existing circuit
        circuit.x(2) # existing circuit

        circuit.x(0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['X', 1, 'X'], ['X']]) # check circuit body

    # ADD SIMPLE GATE Q0 CIRCUIT MULTIPLE GATE Q1, Q2
    def test_addSimpleGate_q0_circuitMultipleGate_q1q2(self):
        qsoa = QSOAPlatform()

        circuit = qsoa.CircuitGates() # create circuit
        circuit.cx(1, 2) # existing circuit

        circuit.x(0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 'X'], ['X']]) # check circuit body


##################_____TEST SIMPLE GATES_____##################
class Test_Simple(unittest.TestCase):
    
    # ALL SIMPLE GATES
    def test_simpleGates(self):
        qsoa = QSOAPlatform()

        circuit = qsoa.CircuitGates() # create circuit

        circuit.x(0) # add gate
        circuit.y(0) # add gate
        circuit.z(0) # add gate
        circuit.s(0) # add gate
        circuit.sdg(0) # add gate
        circuit.t(0) # add gate
        circuit.tdg(0) # add gate
        circuit.barrier(0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['X'], ['Y'], ['Z'], ['S'], ['I_S'], ['T'], ['I_T'], ['SPACER']]) # check circuit body
    
    # ADD GENERAL BARRIER
    def test_barrier_all(self):
        qsoa = QSOAPlatform()

        circuit = qsoa.CircuitGates() # create circuit
        circuit.h(0) # existing circuit
        circuit.cx(1, 2) # existing circuit
        circuit.h(1) # existing circuit

        circuit.barrier() # add barriers

        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'X'], [1, 'H'], ['SPACER', 'SPACER', 'SPACER']]) # check circuit body
    
    # ADD BARRIER SPECIFIC POSITIONS MANUALLY
    def test_addBarrier_manualList(self):
        qsoa = QSOAPlatform()

        circuit = qsoa.CircuitGates() # create circuit
        circuit.h(0) # existing circuit

        circuit.barrier([0, 2, 3]) # add barriers

        self.assertEqual(circuit.getCircuitBody(), [['H', 1, 'SPACER', 'SPACER'], ['SPACER']]) # check circuit body
    
    # ADD BARRIER SPECIFIC POSITIONS AUTOMATED
    def test_addBarrier_automatedList(self):
        qsoa = QSOAPlatform()

        circuit = qsoa.CircuitGates() # create circuit
        circuit.h(0) # existing circuit

        circuit.barrier([i for i in range(3)]) # add barriers

        self.assertEqual(circuit.getCircuitBody(), [['H', 'SPACER', 'SPACER'], ['SPACER']]) # check circuit body


##################_____TEST SIMPLE GATES WITH ARGUMENT_____##################
class Test_Simple_Argument(unittest.TestCase):
    
    # SIMPLE GATE WITH ARGUMENT
    def test_simpleGate_argument(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.p(0, 'e') # add gate

        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'P', 'arg': 'e'}]]) # check circuit body
    
    # SIMPLE GATE WITHOUT ARGUMENT
    def test_simpleGate_noArgument(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.p(0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'P', 'arg': 'pi'}]]) # check circuit body
    
    # ALL SIMPLE GATES WITH ARGUMENT
    def test_simpleGates_argument(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.p(0) # add gate
        circuit.rz(0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'P', 'arg': 'pi'}], [{'id': 'RZ', 'arg': 'pi'}]]) # check circuit body


#################_____TEST MEASURE_____##################
class Test_Measure(unittest.TestCase):

    # ADD MEASURE Q0 EMPTY CIRCUIT
    def test_addMeasure_q0_emptyCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.measure(0) # add measure

        self.assertEqual(circuit.getCircuitBody(), [['Measure']]) # check circuit body
        self.assertEqual(circuit.getClassicRegisters(), {0}) # check classic registers
    
    # ADD MEASURE Q1 CIRCUIT Q0
    def test_addMeasure_q1_circuit_q0(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.measure(0) # existing circuit

        circuit.measure(1) # add measure

        self.assertEqual(circuit.getCircuitBody(), [['Measure'], [1, 'Measure']]) # check circuit body
        self.assertEqual(circuit.getClassicRegisters(), {0, 1}) # check classic registers
    
    # ADD MEASURE Q0 CIRCUIT Q0
    def test_addMeasure_q0_circuit_q0(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.measure(0) # existing circuit

        circuit.measure(0) # add measure

        self.assertEqual(circuit.getCircuitBody(), [['Measure'], ['Measure']]) # check circuit body
        self.assertEqual(circuit.getClassicRegisters(), {0}) # check classic registers
    
    # ADD MEASURE ALL
    def test_measure_all(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.h(0) # existing circuit
        circuit.cx(1, 2) # existing circuit
        circuit.h(1) # existing circuit

        circuit.measure() # add all

        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'X'], [1, 'H'], ['Measure'], [1, 'Measure'], [1, 1, 'Measure']]) # check circuit body
        self.assertEqual(circuit.getClassicRegisters(), {0, 1, 2}) # check classic registers
    
    # ADD MEASURE SPECIFIC POSITIONS MANUALLY
    def test_addMeasure_manualList(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.measure([0, 2, 3]) # add gates

        self.assertEqual(circuit.getCircuitBody(), [['Measure'], [1, 1, 'Measure'], [1, 1, 1, 'Measure']]) # check circuit body
    
    # ADD MEASURE SPECIFIC POSITIONS AUTOMATED
    def test_addMeasure_automatedList(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.measure([i for i in range(3)]) # add gates

        self.assertEqual(circuit.getCircuitBody(), [['Measure'], [1, 'Measure'], [1, 1, 'Measure']]) # check circuit body
    

##################_____TEST SIMPLE GATES WITHOUT PREVIUOUS MEASURE_____##################
class Test_Simple_WithoutPreviousMeasure(unittest.TestCase):
    
    # ADD SIMPLE GATE Q0 MEASURE Q0
    def test_addSimpleGate_q0_measure_q0(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.measure(0) # existing circuit

        circuit.h(0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['Measure']]) # check circuit body

    # ALL SIMPLE GATES WITHOUT PREVIUOUS MEASURE
    def test_simpleGates_noPreviousMeasure(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.h(0) # add gate
        circuit.sx(0) # add gate
        circuit.sxdg(0) # add gate
        circuit.sy(0) # add gate
        circuit.sydg(0) # add gate
        circuit.tx(0) # add gate
        circuit.txdg(0) # add gate
        circuit.ty(0) # add gate
        circuit.tydg(0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['H'], ['SX'], ['I_SX'], ['SY'], ['I_SY'], ['TX'], ['I_TX'], ['TY'], ['I_TY']]) # check circuit body


##################_____TEST SIMPLE GATES WITH ARGUMENT WITHOUT PREVIUOUS MEASURE_____##################
class Test_Simple_Argument_WithoutPreviousMeasure(unittest.TestCase):
    
    # ADD SIMPLE GATE WITH ARGUMENT Q0 MEASURE Q0
    def test_addSimpleGate_argument_q0_measure_q0(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.measure(0) # existing circuit

        circuit.rx(0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [['Measure']]) # check circuit body

    # ALL SIMPLE GATES WITH ARGUMENT WITHOUT PREVIUOUS MEASURE
    def test_simpleGates_argument_noPreviousMeasure(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.rx(0) # add gate
        circuit.ry(0) # add gate

        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RX', 'arg': 'pi'}], [{'id': 'RY', 'arg': 'pi'}]]) # check circuit body


##################_____TEST CONTROL GATE_____##################
class Test_Control(unittest.TestCase):
    
    # ADD CREATED GATE CCCX EMPTY CIRCUIT
    def test_addCreatedGate_cccx_emptyCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        cccx = circuit.control( # create cccx gate, add control
            0, circuit.control( # add control
                1, circuit.control( # add control
                    2, circuit.x(3, False) # add x gate
                )
            )
        )

        circuit.addCreatedGate(cccx) # add cccx gate

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 'CTRL', 'X']]) # check circuit body
    
    # ADD CREATED MULTIPLE GATE CSWAP EMPTY CIRCUIT
    def test_addCreatedGate_cswap_emptyCircuit(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        cswap = circuit.control( # create cswap gate, add control
            0, circuit.swap(1, 2, False) # add swap gate
        )

        circuit.addCreatedGate(cswap) # add cswap gate

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'Swap', 'Swap']]) # check circuit body


##################_____TEST SIMPLE GATE MULTIPLE POSITIONS_____##################
class Test_SimpleGateMultiplePositions(unittest.TestCase):

    # ADD SIMPLE GATE ALL POSITIONS
    def test_addSimpleGate_all(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit
        circuit.h(1) # existing circuit

        circuit.x() # add gates

        self.assertEqual(circuit.getCircuitBody(), [['X', 'H'], [1, 'X']]) # check circuit body
    
    # ADD SIMPLE GATE SPECIFIC POSITIONS MANUALLY
    def test_addSimpleGate_manualList(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.x([0, 2, 3]) # add gates

        self.assertEqual(circuit.getCircuitBody(), [['X', 1, 'X', 'X']]) # check circuit body

    # ADD SIMPLE GATE SPECIFIC POSITIONS AUTOMATED
    def test_addSimpleGate_automatedList(self):
        qsoa = QSOAPlatform()
        
        circuit = qsoa.CircuitGates() # create circuit

        circuit.x([i for i in range(3)]) # add gates

        self.assertEqual(circuit.getCircuitBody(), [['X', 'X', 'X']]) # check circuit body


if __name__ == '__main__':
    unittest.main()