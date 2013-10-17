import logging
import unittest
import numpy as np
from cython_example_proj import array_sum, tessellate, factorial

"""
Some basic tests
"""

logging.basicConfig(level=logging.DEBUG)


class TestSTL(unittest.TestCase):

    def test_array_sum(self):

        A = np.random.randn(500, 500)
        result = array_sum(A)
        self.assertAlmostEqual(A.sum(), result)

    def test_tessellate(self):

        A = np.random.randn(100, 100)
        result = tessellate(A)
        m, n = result.shape
        assert m == 20000
        assert n == 12

    def test_factorial(self):
        assert factorial(10) == 3628800

if __name__ == '__main__':
    unittest.main()
