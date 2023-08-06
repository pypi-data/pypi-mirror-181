class CircuitGates:
    """
    Create Circuit Gates.
    """

    # CONSTRUCTOR
    def __init__(self):
        self.classicRegisters = set()
        self.__circuitBody = [[]]


    # GETTERS
    def getCircuitBody(self) -> list:
        """
        Get Circuit Body.

        Output
        ----------
        list
        """

        return self.__circuitBody
    
    def getParsedBody(self) -> str:
        stringBody = str(self.__circuitBody).replace("'", '"').replace(' ', '')
        parsedtBody = 'circuit={"cols":' + stringBody + '}'

        return parsedtBody
    
    def getClassicRegisters(self) -> set:
        return self.classicRegisters


    # INTERN FUNCTIONS
    def __checkInputTypes(self, *args):
        for argTuple in args:
            expextedTypes = str([i.__name__ for i in argTuple[2]]).replace("['", "<").replace(" '", " <").replace("']", ">").replace("',", ">,")

            if type(argTuple[1]) not in argTuple[2]:
                raise ValueError(f'Argument "{argTuple[0]}" expected to be {expextedTypes}, not <{type(argTuple[1]).__name__}>')
    
    def __checkAllItemsSameType(self, itemsList: list):
        if not all(isinstance(n, int) for n in itemsList):
            raise ValueError(f'Argument "position" expected to be <int>')
    
    def __addMeasure(self, position, gate, circuitBody, classicRegisters):
        if circuitBody[0] == []: # if circuit is empty
            column = 0

        else: # if circuit is not empty
            column = -1
            circuitBody.append([])


        while len(circuitBody[column]) != position: # fill with 1 the positions until the gate position
            circuitBody[column].append(1)
            
        circuitBody[column].append(gate) # add the gate
        classicRegisters.add(position) # transform quantum register to classic register
    
    def __addSimpleGate(self, position, gate, circuitBody, classicRegisters = {}):
        if position not in classicRegisters:

            numColumn = len(circuitBody) - 1 # column indexes
            lastColumn = -1 # last column with gate

            while numColumn >= 0: # while there are columns

                if 'CTRL' in circuitBody[numColumn] or 'Swap' in circuitBody[numColumn]: # if column have a multiple gate
                    break

                elif len(circuitBody[numColumn]) - 1 < position: # column is smaller than the gate position
                    lastColumn = numColumn # column available to add the gate
                
                else: # column is greater than the gate position

                    if circuitBody[numColumn][position] == 1: # position is 1
                        lastColumn = numColumn # column available to add the gate
                    
                    else: # column have a gate, so is not available to add the gate
                        break

                numColumn -= 1 # check previous column
            

            if lastColumn != -1: # add the gate in an existing column

                if len(circuitBody[lastColumn]) - 1 < position: # column is smaller than the gate position

                    while len(circuitBody[lastColumn]) != position: # fill with 1 the positions until the gate position
                        circuitBody[lastColumn].append(1)
                    
                    circuitBody[lastColumn].append(gate) # add the gate
                
                else: # column is larger than the gate position
                    circuitBody[lastColumn][position] = gate # replace 1 by the gate
            
            else: # add a new column
                circuitBody.append([])

                while len(circuitBody[lastColumn]) != position: # fill with 1 the positions until the gate position
                    circuitBody[-1].append(1)
                    
                circuitBody[-1].append(gate) # add the gate
    
    def __addMultipleGate(self, positions, circuitBody, classicRegisters = {}):
        # swap --> add gate
        # control swap with classic register in swap --> not add gate
        # control gate without classic register in gate --> add gate
        # control gate with classic register in gate --> not add gate

        addGate = True
        control = False

        for gate in positions: # check all gates
            if 'CTRL' in gate: # if control in any position
                control = True
                break

        if control: # if is a controlled gate
            for gate in positions: # check all gates
                if 'CTRL' not in gate: # is a gate position, not a control
                    if gate[0] in classicRegisters: # gate position is a classic register
                        addGate = False
                        break

        if addGate:
            positions = sorted(positions)
            
            if circuitBody[0] == []: # if circuit is empty
                column = 0

            else: # if circuit is not empty
                column = -1
                circuitBody.append([])

            for position in positions:

                while len(circuitBody[column]) != position[0]: # fill with 1 the positions until the gate position
                    circuitBody[column].append(1)
                
                circuitBody[column].append(position[1]) # add the gate

            if 'Swap' in positions[0]: # if the multiple gate is a swap

                if positions[0][0] in classicRegisters and positions[1][0] not in classicRegisters: # swap quantum regiter and classic register
                    classicRegisters.remove(positions[0][0])
                    classicRegisters.add(positions[1][0])
                
                elif positions[1][0] in classicRegisters and positions[0][0] not in classicRegisters: # swap quantum regiter and classic register
                    classicRegisters.remove(positions[1][0])
                    classicRegisters.add(positions[0][0])
    
    def __definePositions(self, position, gate: str, circuitBody: list) -> list:
        positions = list()

        if isinstance(position, int): # gate in one position
            positions.append((position, gate))

        elif isinstance(position, list): # gate in multiple positions
            self.__checkAllItemsSameType(position)

            for i in position:
                positions.append((i, gate)) # add all controls

        elif position is None:
            lenCircuitBody = list()

            for column in circuitBody:
                lenCircuitBody.append(len(column))

            times = max(lenCircuitBody)

            for i in range(times):
                positions.append((i, gate))
            
        return positions


    # METHODS
    def x(self, position: int = None, add: bool = True) -> list: # Not gate
        """
        Add Pauli X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )
        

        gateSymbol = 'X'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        return positions


    def y(self, position: int = None, add: bool = True) -> list: # pauli y gate
        """
        Add Pauli Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'Y'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        return positions
    

    def z(self, position: int = None, add: bool = True) -> list: # pauli z gate
        """
        Add Pauli Z gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'Z'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        return positions
    

    def s(self, position: int = None, add: bool = True) -> list: # square root of z, s gate
        """
        Add Square root of Z, S gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'S'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        return positions
    

    def sdg(self, position: int = None, add: bool = True) -> list: # s dagger gate
        """
        Add S Dagger gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'I_S'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        return positions
    

    def t(self, position: int = None, add: bool = True) -> list: # fourth root of z, t gate
        """
        Add Fourt root of Z, T gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'T'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        return positions
    

    def tdg(self, position: int = None, add: bool = True) -> list: # t dagger gate
        """
        Add T Dagger gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'I_T'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        return positions
    

    def barrier(self, position: int = None): # barrier
        """
        Add Barrier.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the barrier. In the case that the position is not indicated, the barrier will be added in all qubits. It can also be a list of positions.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        

        gateSymbol = 'SPACER'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure
        
        if position is None:
            self.__addMultipleGate(positions, self.__circuitBody) # add to circuit
        
        else:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit


    def p(self, position: int = None, argument = 'pi', add: bool = True) -> list: # phase gate
        """
        Add Phase gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        argument: string
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('argument', argument, (str, int)),
            ('add', add, (bool,))
        )


        gateSymbol = {'id': 'P', 'arg': str(argument)}

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        return positions
    

    def rz(self, position: int = None, argument = 'pi', add: bool = True) -> list: # retation z gate
        """
        Add Rotation Z gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        argument: string
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('argument', argument, (str, int)),
            ('add', add, (bool,))
        )


        gateSymbol = {'id': 'RZ', 'arg': str(argument)}

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        return positions


    def measure(self, position: int = None) -> list: # measure
        """
        Add Measure.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the measurement. In the case that the position is not indicated, the measurement will be added in all qubits. It can also be a list of positions.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )

        
        gateSymbol = 'Measure'
        
        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        for gate in positions: # to all gates
            self.__addMeasure(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions


    def h(self, position: int = None, add: bool = True) -> list: # hadamard gate
        """
        Add Hadamard gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'H'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions
    

    def sx(self, position: int = None, add: bool = True) -> list: # square root of not gate
        """
        Add Square root of X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'SX'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions


    def sxdg(self, position: int = None, add: bool = True) -> list: # square root of not dagger gate
        """
        Add Square root of X Dagger gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'I_SX'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions
    

    def sy(self, position: int = None, add: bool = True) -> list: # square root of y gate
        """
        Add Square root of Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'SY'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions


    def sydg(self, position: int = None, add: bool = True) -> list: # square root of y dagger
        """
        Add Square root of Y Dagger gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'I_SY'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions
    

    def tx(self, position: int = None, add: bool = True) -> list: # fourth root of x gate
        """
        Add Fourth root of X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'TX'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions


    def txdg(self, position: int = None, add: bool = True) -> list: # fourth root of x dagger gate
        """
        Add Fourth root of X Dagger gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'I_TX'
        
        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions
    

    def ty(self, position: int = None, add: bool = True) -> list: # fourth root of y gate
        """
        Add Fourth root of Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'TY'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions
    

    def tydg(self, position: int = None, add: bool = True) -> list: # fourth root of y dagger gate
        """
        Add Fourth root of Y Dagger gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('add', add, (bool,))
        )


        gateSymbol = 'I_TY'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions
    

    def rx(self, position: int = None, argument = 'pi', add: bool = True) -> list: # rotation x gate
        """
        Add Rotation X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        argument: string
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('argument', argument, (str, int)),
            ('add', add, (bool,))
        )


        gateSymbol = {'id': 'RX', 'arg': str(argument)}

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions
    

    def ry(self, position: int = None, argument = 'pi', add: bool = True) -> list: # rotation y gate
        """
        Add Rotation Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        argument: string
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        if position:
            self.__checkInputTypes(
                ('position', position, (int, list))
            )
        self.__checkInputTypes(
            ('argument', argument, (str, int)),
            ('add', add, (bool,))
        )


        gateSymbol = {'id': 'RY', 'arg': str(argument)}

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions
    

    def control(self, position: int, circuit: list) -> list: # control
        """
        Add Control.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Mandatory argument. Qubit position to add the control.
        circuit : list
            Gate or set of elements to add a control.
        """
        self.__checkInputTypes(
            ('position', position, (int, list)),
            ('circuit', circuit, (list,))
        )


        correctPosition = True

        for gate in circuit:
            if position in gate:
                correctPosition = False
                break

        if correctPosition:
            circuit.append((position, 'CTRL'))

        return circuit
    

    def addCreatedGate(self, gate: list): # add created gate
        """
        Add Created gate.

        Prerequisites
        ----------
        - Created circuit.
        - Created gate.

        Parameters
        ----------
        gate : list
            Created gate to add to the circuit.
        """
        self.__checkInputTypes(
            ('gate', gate, (list,))
        )


        self.__addMultipleGate(gate, self.__circuitBody, self.classicRegisters) # add to circuit
    

    def swap(self, position1: int, position2: int, add: bool = True) -> list: # swap gate
        """
        Add Rotation Swap gates.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the swap.
        position2 : int
            Mandatory argument. Second qubit position to add the swap.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        self.__checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('add', add, (bool,)),
        )

        positions = [
            (position1, 'Swap'),
            (position2, 'Swap')
        ]

        if add:
            self.__addMultipleGate(positions, self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions
    

    def ch(self, position1: int, position2: int, add: bool = True) -> list: # control hadamard gate
        """
        Add Rotation Control Hadamard gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the swap.
        position2 : int
            Mandatory argument. Second qubit position to add the swap.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        self.__checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('add', add, (bool,)),
        )


        positions = [
            (position1, 'CTRL'),
            (position2, 'H')
        ]

        if add:
            self.__addMultipleGate(positions, self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions


    def cx(self, position1: int, position2: int, add: bool = True) -> list: # control not gate
        """
        Add Control X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the swap.
        position2 : int
            Mandatory argument. Second qubit position to add the swap.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        self.__checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('add', add, (bool,)),
        )


        positions = [
            (position1, 'CTRL'),
            (position2, 'X')
        ]

        if add:
            self.__addMultipleGate(positions, self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions
    

    def ccx(self, position1: int, position2: int, position3: int, add = True) -> list: # toffoli gate
        """
        Add Rotation Control Control Hadamard gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the swap.
        position2 : int
            Mandatory argument. Second qubit position to add the swap.
        position3 : int
            Mandatory argument. Second qubit position to add the swap.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        self.__checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('position3', position3, (int,)),
            ('add', add, (bool,)),
        )


        positions = [
            (position1, 'CTRL'),
            (position2, 'CTRL'),
            (position3, 'X')
        ]

        if add:
            self.__addMultipleGate(positions, self.__circuitBody, self.classicRegisters) # add to circuit
        
        return positions
    

    def mcg(self, position: int, circuit: list, add: bool = True) -> list: # multi control gate
        """
        Add Multi Control gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int
            Qubit position or list of positions to add the control.
        gate : list
            Gate or set of elements to add a control.
        add : bool
            Optional argument, True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        """
        self.__checkInputTypes(
            ('position', position, (int, list)),
            ('circuit', circuit, (list,)),
            ('add', add, (bool,)),
        )
        

        gateSymbol = 'CTRL'

        if isinstance(position, int): # one postion
            circuit.append((position, gateSymbol))

        elif isinstance(position, list): # multiple positions
            for i in position:
                circuit.append((i, gateSymbol)) # add all controls

        if add:
            self.__addMultipleGate(circuit, self.__circuitBody, self.classicRegisters) # add to circuit
        
        return circuit