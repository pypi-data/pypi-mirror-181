class CircuitFlow:
    """
    Create Flow.
    """
    
    # CONSTRUCTOR
    def __init__(self):
        self.__nodeData = []
        self.__linkData = []
        self.__keyValue = -1

        self.__flowBody = {
            'class': 'go.GraphLinksModel',
            'nodeDataArray': self.__nodeData,
            'linkDataArray': self.__linkData
        }


    # GETTERS
    def getFlowBody(self) -> dict:
        """
        Get Flow Body.

        Output
        ----------
        dict
        """

        return self.__flowBody
    
    def getParsedBody(self) -> str:
        parsedBody = str(self.__flowBody).replace("'", '"').replace(' ', '')

        return parsedBody
    

    # INTERN FUNCTIONS
    def __checkInputTypes(self, *args):
        for argTuple in args:
            expextedTypes = str([i.__name__ for i in argTuple[2]]).replace("['", "<").replace(" '", " <").replace("']", ">").replace("',", ">,")

            if type(argTuple[1]) not in argTuple[2]:
                raise ValueError(f'Argument "{argTuple[0]}" expected to be {expextedTypes}, not <{type(argTuple[1]).__name__}>')


    # METHODS
    def startNode(self) -> dict:
        """
        Add Start node.

        Prerequisites
        ----------
        - Created flow.
        """

        startNode = {
            'category': 'Start',
            'text': 'Start',
            'key': self.__keyValue,
            'loc': ''
        }

        self.__nodeData.append(startNode)
        self.__keyValue -= 1

        return startNode
    
    def initNode(self, startValue: int) -> dict:
        """
        Add Init node.

        Prerequisites
        ----------
        - Created flow.

        Parameters
        ----------
        startValue : int
            Initial value for the flow iterations.
        """
        self.__checkInputTypes(
            ('startValue', startValue, (int,))
        )

        initNode = {
            'category': 'Init',
            'text': str(startValue),
            'key': self.__keyValue,
            'loc': ''
        }

        self.__nodeData.append(initNode)
        self.__keyValue -= 1

        return initNode
    
    def circuitNode(self, circuitName) -> dict:
        """
        Add Circuit node.

        Prerequisites
        ----------
        - Created flow.

        Parameters
        ----------
        circuitName : str
            Circuit name to introduce in the flow.
        """
        self.__checkInputTypes(
            ('circuitName', circuitName, (str,))
        )

        circuitNode = {
            'category': 'Circuit',
            'text': circuitName,
            'key': self.__keyValue,
            'loc': ''
        }

        self.__nodeData.append(circuitNode)
        self.__keyValue -= 1

        return circuitNode
    
    def repeatNode(self, numReps: int) -> dict:
        """
        Add Repeat node.

        Prerequisites
        ----------
        - Created flow.

        Parameters
        ----------
        numReps : int
            Number of circuit repetitions.
        """
        self.__checkInputTypes(
            ('numReps', numReps, (int,))
        )

        repeatNode = {
            'category': 'Repeat',
            'text': str(numReps),
            'key': self.__keyValue,
            'loc': ''
        }

        self.__nodeData.append(repeatNode)
        self.__keyValue -= 1

        return repeatNode
    
    def endNode(self) -> dict:
        """
        Add End node.

        Prerequisites
        ----------
        - Created flow.
        """
        
        endNode = {
            'category': 'End',
            'text': 'End',
            'key': self.__keyValue,
            'loc': ''
        }

        self.__nodeData.append(endNode)
        self.__keyValue -= 1

        return endNode
    
    def commentNode(self, comment: str) -> dict:
        """
        Add Comment node.

        Prerequisites
        ----------
        - Created flow.

        Parameters
        ----------
        comment : str
            Comment.
        """
        self.__checkInputTypes(
            ('comment', comment, (str,))
        )

        commentNode = {
            'category': 'Comment',
            'text': comment,
            'key': self.__keyValue,
            'loc': ''
        }

        self.__nodeData.append(commentNode)
        self.__keyValue -= 1

        return commentNode
    
    def linkNodes(self, fromNode: dict, toNode: dict) -> dict:
        """
        Link two nodes.

        Prerequisites
        ----------
        - Created flow.
        - Minimum two existing nodes.

        Parameters
        ----------
        fromNode : node
            Origin node to link.
        toNode : node
            Destiny node to link.
        """
        self.__checkInputTypes(
            ('fromNode', fromNode, (dict,)),
            ('toNode', toNode, (dict,))
        )

        link = {
            'from': fromNode['key'],
            'to': toNode['key'],
            'points': []
        }

        self.__linkData.append(link)

        return link