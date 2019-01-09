import unittest
from Vector import Vector


class VectorTest(unittest.TestCase):
    def test_vector_equals(self):
        val = Vector(1, 0, 1)
        other = Vector(1, 0, 1)
        non_equal = Vector(1, 1, 1)

        self.assertEqual(val, other)
        self.assertNotEqual(val, non_equal)

    def test_vector_scalar_multiplication(self):
        vector = Vector(1, 1, 2)

        result = vector.scalar(2)

        self.assertEqual(result, Vector(2, 2, 4))

    def test_vector_vector_multiplication(self):
        vector = Vector(1, 2, 3)
        other = Vector(4, 5, 6)

        result = vector.vector_multiplication(other)

        self.assertEqual(result, Vector(12 - 15, -6 + 12, 5 - 8))

    def test_vector_scalar_vector_multiplication(self):
        vector = Vector(1, 2, 3)
        other = Vector(4, 5, 6)

        result = vector.scalar_multiplication(other)

        self.assertEqual(result, 32)

    def test_vector_get_norm(self):
        vector = Vector(1, 2, 2)

        self.assertEqual(3, vector.get_norm())

    def test_vector_get_angle(self):
        def eq(a, b):
            return abs(a - b) < 1e-6

        vector = Vector(1, 2, 3)
        other = Vector(4, 5, 6)

        assert(eq(vector.get_angle(other),  0.2257261))

    def test_vector_change_len(self):
        vector = Vector(1, 2, 2)

        self.assertEqual(vector.change_len(9), Vector(3, 6, 6))

