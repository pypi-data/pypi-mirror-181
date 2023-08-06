import unittest
from QuantumPathQSOAPySDK import QSOAPlatform

##################_____CIRCUITFLOW_____##################
class Test_CircuitFlow(unittest.TestCase):

    # CIRCUIT FLOW
    def test_CircuitFlow(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        self.assertEqual(type(flow).__name__, 'CircuitFlow')


##################_____GET FLOW BODY_____##################
class Test_GetFlowBody(unittest.TestCase):

    # GET FLOW BODY
    def test_getFlowBody(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        flowBody = flow.getFlowBody()

        self.assertIsInstance(flowBody, dict)


##################_____GET PARSED BODY_____##################
class Test_GetParsedBody(unittest.TestCase):

    # GET PARSED BODY
    def test_getParsedBody(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        parsedBody = flow.getParsedBody()

        self.assertIsInstance(parsedBody, str)


##################_____START NODE_____##################
class Test_StartNode(unittest.TestCase):

    # START NODE
    def test_startNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        startNode = flow.startNode()

        self.assertIsInstance(startNode, dict)


##################_____INIT NODE_____##################
class Test_InitNode(unittest.TestCase):

    # INIT NODE
    def test_initNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        startValue = 0

        initNode = flow.initNode(startValue)

        self.assertIsInstance(initNode, dict)
    
    # BAD ARGUMENT TYPE startValue
    def test_initNode_badArgumentType_startValue(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        startValue = 'startValue'

        try:
            flow.initNode(startValue)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')


##################_____CIRCUIT NODE_____##################
class Test_CircuitNode(unittest.TestCase):

    # CIRCUIT NODE
    def test_circuitNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        circuitName = 'circuitName'

        circuitNode = flow.circuitNode(circuitName)

        self.assertIsInstance(circuitNode, dict)
    
    # BAD ARGUMENT TYPE circuitName
    def test_circuitNode_badArgumentType_circuitName(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        circuitName = 99

        try:
            flow.circuitNode(circuitName)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')


##################_____REPEAT NODE_____##################
class Test_RepeatNode(unittest.TestCase):

    # REPEAT NODE
    def test_repeatNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        numReps = 100

        repeatNode = flow.repeatNode(numReps)

        self.assertIsInstance(repeatNode, dict)
    
    # BAD ARGUMENT TYPE numReps
    def test_repeatNode_badArgumentType_numReps(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        numReps = 'numReps'

        try:
            flow.repeatNode(numReps)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')


##################_____END NODE_____##################
class Test_EndNode(unittest.TestCase):

    # END NODE
    def test_endNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        endNode = flow.endNode()

        self.assertIsInstance(endNode, dict)


##################_____COMMENT NODE_____##################
class Test_CommentNode(unittest.TestCase):

    # COMMENT NODE
    def test_commentNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        comment = 'comment'

        commentNode = flow.commentNode(comment)

        self.assertIsInstance(commentNode, dict)
    
    # BAD ARGUMENT TYPE numReps
    def test_commentNode_badArgumentType_numReps(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        comment = 99

        try:
            flow.commentNode(comment)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')


##################_____LINK NODES_____##################
class Test_LinkNodes(unittest.TestCase):

    # LINK NODES
    def test_linkNodes(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        fromNode = flow.startNode()
        toNode = flow.startNode()

        link = flow.linkNodes(fromNode, toNode)

        self.assertIsInstance(link, dict)
    
    # BAD ARGUMENT TYPE fromNode
    def test_linkNodes_badArgumentType_fromNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        fromNode = 99
        toNode = flow.startNode()

        try:
            flow.linkNodes(fromNode, toNode)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE toNode
    def test_linkNodes_badArgumentType_toNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        fromNode = flow.startNode()
        toNode = 99

        try:
            flow.linkNodes(fromNode, toNode)

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')


if __name__ == '__main__':
    unittest.main()