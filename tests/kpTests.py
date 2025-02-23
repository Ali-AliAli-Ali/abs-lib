import unittest

import numpy as np

from abslib.kp import KnowledgePatternManager, DisjunctKnowledgePatternItem, MatrixProducer, QuantKnowledgePatternItem, \
    ConjunctKnowledgePatternItem


# Tests for knowledge pattern part of abslib
class KnowledgePatternManagerTest(unittest.TestCase):

    def testDisjunctsInconsistent(self):
        arrays = [[[1, 1], [0.1, 0.2], [0.2, 0.4], [0.5, 0.7]]]
        for disjunct_intervals_inconsistent in arrays:
            knowledgePattern = DisjunctKnowledgePatternItem(disjunct_intervals_inconsistent)
            result = KnowledgePatternManager.checkInconsistency(knowledgePattern)
            self.assertTrue(result.inconsistent, "False negative inconsistency result")
            self.assertTrue(np.array(result.array).shape == np.array(disjunct_intervals_inconsistent).shape,
                            "Incorrect result array size")
            for i in range(len(result.array)):
                self.assertTrue(disjunct_intervals_inconsistent[i][0] <= result.array[i][0]
                                and result.array[i][1] <= disjunct_intervals_inconsistent[i][1],
                                "Intervals couldn't become larger")

    def testDisjunctsNotInconsistent(self):
        arrays = [[[1, 1], [0.1, 0.2], [0.2, 0.4], [0.7, 0.7]]]
        for disjunct_intervals_inconsistent in arrays:
            knowledgePattern = DisjunctKnowledgePatternItem(disjunct_intervals_inconsistent)
            result = KnowledgePatternManager.checkInconsistency(knowledgePattern)
            self.assertFalse(result.inconsistent, "False positive inconsistency result")

    def testQuantsInconsistent(self):
        arrays = [[[0.24, 0.25], [0.25, 0.25], [0.25, 0.25], [0.25, 0.25]]]
        for quant_intervals_inconsistent in arrays:
            knowledgePattern = QuantKnowledgePatternItem(quant_intervals_inconsistent)
            result = KnowledgePatternManager.checkInconsistency(knowledgePattern)
            self.assertTrue(result.inconsistent, "False negative inconsistency result")
            self.assertTrue(np.array(result.array).shape == np.array(quant_intervals_inconsistent).shape,
                            "Incorrect result array size")
            for i in range(len(result.array)):
                self.assertTrue(quant_intervals_inconsistent[i][0] <= result.array[i][0]
                                and result.array[i][1] <= quant_intervals_inconsistent[i][1],
                                "Intervals couldn't become larger")

    def testQuantsNotInconsistent(self):
        arrays = [[[0.2, 0.3], [0.2, 0.3], [0.2, 0.3], [0.6, 0.7]]]
        for quant_intervals_inconsistent in arrays:
            knowledgePattern = QuantKnowledgePatternItem(quant_intervals_inconsistent)
            result = KnowledgePatternManager.checkInconsistency(knowledgePattern)
            self.assertFalse(result.inconsistent, "False positive inconsistency result")

    def testConjunctsInconsistent(self):
        arrays = [[[1, 1], [0.6, 0.9], [0.6, 0.9], [0.2, 0.3]]]
        for conjunct_intervals_inconsistent in arrays:
            knowledgePattern = ConjunctKnowledgePatternItem(conjunct_intervals_inconsistent)
            result = KnowledgePatternManager.checkInconsistency(knowledgePattern)
            self.assertTrue(result.inconsistent, "False negative inconsistency result")
            self.assertTrue(np.array(result.array).shape == np.array(conjunct_intervals_inconsistent).shape,
                            "Incorrect result array size")
            for i in range(len(result.array)):
                self.assertTrue(conjunct_intervals_inconsistent[i][0] <= result.array[i][0]
                                and result.array[i][1] <= conjunct_intervals_inconsistent[i][1],
                                "Intervals couldn't become larger")

    def testConjunctsNotInconsistent(self):
        arrays = [[[1, 1], [0.1, 0.2], [0.2, 0.4], [0.8, 0.8]]]
        for conjunct_intervals_inconsistent in arrays:
            knowledgePattern = DisjunctKnowledgePatternItem(conjunct_intervals_inconsistent)
            result = KnowledgePatternManager.checkInconsistency(knowledgePattern)
            self.assertFalse(result.inconsistent, "False positive inconsistency result")

    def testDisjunctsToQuantsMatrix(self):
        matrices = [(np.array([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 1.0],
                               [0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0],
                               [-0.0, -0.0, -0.0, -0.0, -1.0, 1.0, 1.0, -1.0],
                               [0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 1.0],
                               [-0.0, -0.0, -1.0, 1.0, -0.0, -0.0, 1.0, -1.0],
                               [-0.0, -1.0, -0.0, 1.0, -0.0, 1.0, -0.0, -1.0],
                               [0.0, 1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0]], dtype=np.double), 3)]
        for matrix, n in matrices:
            generated_matrix = MatrixProducer.getDisjunctsToQuantsMatrix(n)
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    self.assertEqual(matrix[i][j], generated_matrix[i][j], "Wrong matrix generation algorithm")

    def testConjunctsToQuantsMatrix(self):
        matrices = [(np.array([[1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0],
                               [0.0, 1.0, -0.0, -1.0, -0.0, -1.0, 0.0, 1.0],
                               [0.0, 0.0, 1.0, -1.0, -0.0, -0.0, -1.0, 1.0],
                               [0.0, 0.0, 0.0, 1.0, -0.0, -0.0, -0.0, -1.0],
                               [0.0, 0.0, 0.0, 0.0, 1.0, -1.0, -1.0, 1.0],
                               [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -0.0, -1.0],
                               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -1.0],
                               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]], dtype=np.double), 3)]
        for matrix, n in matrices:
            generated_matrix = MatrixProducer.getConjunctsToQuantsMatrix(n)
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    self.assertEqual(matrix[i][j], generated_matrix[i][j], "Wrong matrix generation algorithm")

    def testQuantsToDisjunctsMatrix(self):
        matrices = [(np.array([[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                               [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0],
                               [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0],
                               [0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0],
                               [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0],
                               [0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                               [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                               [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]], dtype=np.double), 3)]
        for matrix, n in matrices:
            generated_matrix = MatrixProducer.getQuantsToDisjunctsMatrix(n)
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    self.assertEqual(matrix[i][j], generated_matrix[i][j], "Wrong matrix generation algorithm")


if __name__ == '__main__':
    unittest.main()
