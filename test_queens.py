# test_queens.py
#
# ICS 33 Spring 2025
# Project 0: History of Modern
#
# Unit tests for the QueensState class in "queens.py".
#
# Docstrings are not required in your unit tests, though each test does need to have
# a name that clearly indicates its purpose.  Notice, for example, that the provided
# test method is named "test_queen_count_is_zero_initially" instead of something generic
# like "test_queen_count", since it doesn't entirely test the "queen_count" method,
# but instead focuses on just one aspect of how it behaves.  You'll want to do likewise.

from queens import QueensState
import unittest
from queens import Position


class TestQueensState(unittest.TestCase):
    def test_queen_count_is_zero_initially(self):
        state = QueensState(8, 8)
        state.queen_position = []
        self.assertEqual(state.queen_count(), 0)


    def test_queen_count_is_one(self):
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertEqual(state.queen_count(), 1)


    def test_queens_is_empty_initially(self):
        state = QueensState(8, 8)
        state.queen_position = []
        self.assertEqual(state.queens(), [])


    def test_queens_is_not_empty(self):
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertEqual(state.queens(), [Position(0, 0)])


    def test_has_queen_True(self):
        pass


    def test_has_queen_False(self):
        pass






if __name__ == '__main__':
    unittest.main()
