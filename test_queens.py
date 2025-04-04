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


# coverage testing:
# 1. coverage report -m (shows report with percent)
# 2. coverage run -m --branch pytest . (branch coverage)


class TestQueensState(unittest.TestCase):
    def test_queen_count_is_zero_initially(self):
        """Testcase: queen_count() should return zero initially"""
        state = QueensState(8, 8)
        state.queen_position = []
        self.assertEqual(state.queen_count(), 0)


    def test_queen_count_is_one(self):
        """Testcase: queen_count() should return 1
        if one queen exists on the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertEqual(state.queen_count(), 1)


    def test_queen_count_is_more_than_one(self):
        """Testcase: queen_count() should return 2
        if two queen exists on the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0), Position(1, 0)]
        self.assertEqual(state.queen_count(), 2)


    def test_queens_is_empty_initially(self):
        """Testcase: queens() should return an empty list
        if queen does not exist"""
        state = QueensState(8, 8)
        state.queen_position = []
        self.assertEqual(state.queens(), [])


    def test_queens_is_one(self):
        """Testcase: queens() should return a list of the position
        in which queens appear on the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertEqual(state.queens(), [Position(0, 0)])


    def test_queens_are_two(self):
        """Testcase: queens() should return a list of the positions
        in which queens appear on the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0), Position(1, 0)]
        self.assertEqual(state.queens(), [Position(0, 0), Position(1, 0)])


    def test_has_queen_True(self):
        """Testcase: has_queen() should return True
        if queen exists on given position of the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertTrue(state.has_queen(Position(0, 0)))


    def test_has_queen_False(self):
        """Testcase: has_queen() should return False
        if queen does not exist on given position of the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertFalse(state.has_queen(Position(1, 0)))


    def test_queens_unsafe_True_rows(self):
        """Testcase: queens_unsafe() should return True if queen can
        be captured by at least one other queen on the chessboard
        by same rows"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0), Position(0, 1)]
        self.assertTrue(state.any_queens_unsafe())


    def test_queens_unsafe_True_columns(self):
        """Testcase: queens_unsafe() should return True if queen can
        be captured by at least one other queen on the chessboard
        by same columns"""
        state = QueensState(8, 8)
        state.queen_position = [Position(1, 1), Position(0, 1)]
        self.assertTrue(state.any_queens_unsafe())


    def test_queens_unsafe_True_Diagonals(self):
        """Testcase: queens_unsafe() should return True if queen can
        be captured by at least one other queen on the chessboard by diagonals"""
        state = QueensState(8, 8)
        state.queen_position = [Position(1, 1), Position(2, 2)]
        self.assertTrue(state.any_queens_unsafe())


    def test_queens_unsafe_False_single_queen(self):
        """Testcase: There are less than two queen exists on the chessboard
        so queen cannot attack each other"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertFalse(state.any_queens_unsafe())


    def test_queens_unsafe_False_no_queen(self):
        """Testcase: There are no queen exists on the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = []
        self.assertFalse(state.any_queens_unsafe())


    def test_queens_unsafe_False_cannot_attack_each_other(self):
        """Testcase: should return False if no queens can attack each other"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0), Position(1, 2), Position(2, 4)]
        self.assertFalse(state.any_queens_unsafe())


if __name__ == '__main__':
    unittest.main()
