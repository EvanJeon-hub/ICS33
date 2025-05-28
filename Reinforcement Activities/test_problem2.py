# Evan-Soobin Jeon
# ejeon2@uci.edu
# test_problem2.py

import unittest
from problem2 import Person, Coordinate

class TestHashableByAttributes(unittest.TestCase):

    def test_person_hash_equality(self):
        p1 = Person("EVAN", 30)
        p2 = Person("EVAN", 30)
        p3 = Person("Alice", 25)

        self.assertEqual(p1, p2)
        self.assertEqual(hash(p1), hash(p2))
        self.assertNotEqual(p1, p3)

    def test_coordinate_hash(self):
        c1 = Coordinate(1, 2)
        c2 = Coordinate(1, 2)
        c3 = Coordinate(2, 3)

        self.assertEqual(c1, c2)
        self.assertEqual(hash(c1), hash(c2))
        self.assertNotEqual(c1, c3)

    def test_ignores_unhashable(self):
        c1 = Coordinate(1, 2, metadata={"note": "test"})
        c2 = Coordinate(1, 2, metadata={"note": "test"})

        self.assertEqual(hash(c1), hash(c2))

if __name__ == '__main__':
    unittest.main()
