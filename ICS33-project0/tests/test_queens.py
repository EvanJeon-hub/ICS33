# test_queens.py
"""Testing module for queens.py"""
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

import unittest
from queens import QueensState, Position, DuplicateQueenError, MissingQueenError



# coverage report -m (shows report with percent)
# coverage run -m --branch pytest . (branch coverage)

class TestExceptions(unittest.TestCase):
    """Testing class for DuplicateQueenError and MissingQueenError"""
    def test_duplicate_queen_error(self):
        """Testcase for DuplicateQueenError."""
        position = Position(2, 5)
        try:
            raise DuplicateQueenError(position)
        except DuplicateQueenError as e:
            expected_message = "duplicate queen in row 2 column 5"
            self.assertEqual(str(e), expected_message)

    def test_missing_queen_error(self):
        """Testcase for MissingQueenError."""
        position = Position(2, 5)
        try:
            raise MissingQueenError(position)
        except MissingQueenError as e:
            expected_message = "missing queen in row 2 column 5"
            self.assertEqual(str(e), expected_message)


class TestQueensState(unittest.TestCase):
    """Testing Class for QueensState"""
    def test_queen_count_is_zero_initially_sq(self):
        """Testcase: queen_count() should return zero initially"""
        state = QueensState(8, 8)
        state.queen_position = []
        self.assertEqual(state.queen_count(), 0)

    def test_queen_count_is_zero_initially_rect(self):
        """Testcase: queen_count() should return zero initially"""
        state = QueensState(4, 8)
        state.queen_position = []
        self.assertEqual(state.queen_count(), 0)

    def test_queen_count_is_one_sq(self):
        """Testcase: queen_count() should return 1
        if one queen exists on the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertEqual(state.queen_count(), 1)

    def test_queen_count_is_one_rect(self):
        """Testcase: queen_count() should return 1
        if one queen exists on the chessboard"""
        state = QueensState(4, 8)
        state.queen_position = [Position(0, 0)]
        self.assertEqual(state.queen_count(), 1)

    def test_queen_count_is_more_than_one_sq(self):
        """Testcase: queen_count() should return 2
        if two queen exists on the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0), Position(1, 0)]
        self.assertEqual(state.queen_count(), 2)

    def test_queen_count_is_more_than_one_rect(self):
        """Testcase: queen_count() should return 2
        if two queen exists on the chessboard"""
        state = QueensState(4, 8)
        state.queen_position = [Position(0, 0), Position(1, 0)]
        self.assertEqual(state.queen_count(), 2)

    def test_queens_is_empty_initially_sq(self):
        """Testcase: queens() should return an empty list
        if queen does not exist"""
        state = QueensState(8, 8)
        state.queen_position = []
        self.assertEqual(state.queens(), [])

    def test_queens_is_empty_initially_rect(self):
        """Testcase: queens() should return an empty list
        if queen does not exist"""
        state = QueensState(4, 8)
        state.queen_position = []
        self.assertEqual(state.queens(), [])

    def test_queens_is_one_sq(self):
        """Testcase: queens() should return a list of the position
        in which queens appear on the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertEqual(state.queens(), [Position(0, 0)])

    def test_queens_is_one_rect(self):
        """Testcase: queens() should return a list of the position
        in which queens appear on the chessboard"""
        state = QueensState(4, 8)
        state.queen_position = [Position(0, 0)]
        self.assertEqual(state.queens(), [Position(0, 0)])

    def test_queens_are_more_than_one_sq(self):
        """Testcase: queens() should return a list of the positions
        in which queens appear on the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0), Position(1, 0)]
        self.assertEqual(state.queens(), [Position(0, 0), Position(1, 0)])

    def test_queens_are_more_than_one_rect(self):
        """Testcase: queens() should return a list of the positions
        in which queens appear on the chessboard"""
        state = QueensState(4, 8)
        state.queen_position = [Position(0, 0), Position(1, 0)]
        self.assertEqual(state.queens(), [Position(0, 0), Position(1, 0)])

    # Checkpoint
    def test_has_queen_true_sq(self):
        """Testcase: has_queen() should return True
        if queen exists on given position of the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertTrue(state.has_queen(Position(0, 0)))

    def test_has_queen_true_rect(self):
        """Testcase: has_queen() should return True
        if queen exists on given position of the chessboard"""
        state = QueensState(4, 8)
        state.queen_position = [Position(0, 0)]
        self.assertTrue(state.has_queen(Position(0, 0)))

    def test_has_queen_false_sq(self):
        """Testcase: has_queen() should return False
        if queen does not exist on given position of the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertFalse(state.has_queen(Position(1, 0)))

    def test_has_queen_false_rect(self):
        """Testcase: has_queen() should return False
        if queen does not exist on given position of the chessboard"""
        state = QueensState(4, 8)
        state.queen_position = [Position(0, 0)]
        self.assertFalse(state.has_queen(Position(1, 0)))

    def test_queens_unsafe_true_rows_sq(self):
        """Testcase: queens_unsafe() should return True if queen can
        be captured by at least one other queen on the chessboard
        by same rows"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0), Position(0, 1)]
        self.assertTrue(state.any_queens_unsafe())

    def test_queens_unsafe_true_rows_rect(self):
        """Testcase: queens_unsafe() should return True if queen can
        be captured by at least one other queen on the chessboard
        by same rows"""
        state = QueensState(4, 8)
        state.queen_position = [Position(0, 0), Position(0, 1)]
        self.assertTrue(state.any_queens_unsafe())

    def test_queens_unsafe_true_columns_sq(self):
        """Testcase: queens_unsafe() should return True if queen can
        be captured by at least one other queen on the chessboard
        by same columns"""
        state = QueensState(8, 8)
        state.queen_position = [Position(1, 1), Position(0, 1)]
        self.assertTrue(state.any_queens_unsafe())

    def test_queens_unsafe_true_columns_rect(self):
        """Testcase: queens_unsafe() should return True if queen can
        be captured by at least one other queen on the chessboard
        by same columns"""
        state = QueensState(4, 8)
        state.queen_position = [Position(1, 1), Position(0, 1)]
        self.assertTrue(state.any_queens_unsafe())

    def test_queens_unsafe_true_diagonals_sq(self):
        """Testcase: queens_unsafe() should return True if queen can
        be captured by at least one other queen on the board by diagonals"""
        state = QueensState(8, 8)
        state.queen_position = [Position(1, 1), Position(2, 2)]
        self.assertTrue(state.any_queens_unsafe())

    def test_queens_unsafe_true_diagonals_rect(self):
        """Testcase: queens_unsafe() should return True if queen can
        be captured by at least one other queen on the board by diagonals"""
        state = QueensState(4, 8)
        state.queen_position = [Position(1, 1), Position(2, 2)]
        self.assertTrue(state.any_queens_unsafe())

    def test_queens_unsafe_true_only_one_queen_unsafe_sq(self):
        """Testcase: only one queen unsafe"""
        state = QueensState(8, 8)
        state.queen_position = [Position(1, 1), Position(2, 2), Position(2, 3)]
        self.assertTrue(state.any_queens_unsafe())

    def test_queens_unsafe_true_only_one_queen_unsafe_rect(self):
        """Testcase: only one queen unsafe"""
        state = QueensState(4, 8)
        state.queen_position = [Position(1, 1), Position(2, 2), Position(2, 3)]
        self.assertTrue(state.any_queens_unsafe())

    def test_queens_unsafe_false_single_queen_sq(self):
        """Testcase: There are less than two queen exists on the chessboard
        so queen cannot attack each other"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0)]
        self.assertFalse(state.any_queens_unsafe())

    def test_queens_unsafe_false_single_queen_rect(self):
        """Testcase: There are less than two queen exists on the chessboard
        so queen cannot attack each other"""
        state = QueensState(4, 8)
        state.queen_position = [Position(0, 0)]
        self.assertFalse(state.any_queens_unsafe())

    def test_queens_unsafe_false_no_queen_sq(self):
        """Testcase: There are no queen exists on the chessboard"""
        state = QueensState(8, 8)
        state.queen_position = []
        self.assertFalse(state.any_queens_unsafe())

    def test_queens_unsafe_false_no_queen_rect(self):
        """Testcase: There are no queen exists on the chessboard"""
        state = QueensState(4, 8)
        state.queen_position = []
        self.assertFalse(state.any_queens_unsafe())

    def test_queens_unsafe_false_cannot_attack_each_other_sq(self):
        """Testcase: should return False if no queens can attack each other"""
        state = QueensState(8, 8)
        state.queen_position = [Position(0, 0), Position(1, 2), Position(2, 4)]
        self.assertFalse(state.any_queens_unsafe())

    def test_queens_unsafe_false_cannot_attack_each_other_rect(self):
        """Testcase: should return False if no queens can attack each other"""
        state = QueensState(4, 8)
        state.queen_position = [Position(0, 0), Position(1, 2), Position(2, 4)]
        self.assertFalse(state.any_queens_unsafe())

    def test_queens_added_success_single_queen_sq(self):
        """Testcase: returns a new QueensState with single queen"""
        state = QueensState(8, 8)
        new_position = [Position(1, 1)]
        new_queen_state = state.with_queens_added(new_position)
        self.assertEqual(new_queen_state.queen_count(), 1)
        self.assertIn(Position(1, 1), new_queen_state.queens())
        self.assertNotIn(Position(1, 1), state.queens())

    def test_queens_added_success_single_queen_rect(self):
        """Testcase: returns a new QueensState with a single queen"""
        state = QueensState(4, 8)
        new_position = [Position(1, 1)]
        new_queen_state = state.with_queens_added(new_position)
        self.assertEqual(new_queen_state.queen_count(), 1)
        self.assertIn(Position(1, 1), new_queen_state.queens())
        self.assertNotIn(Position(1, 1), state.queens())

    def test_queens_added_success_multiple_queen_sq(self):
        """Testcase: returns a new QueensState with multiple queens"""
        state = QueensState(8, 8)
        current_position = [Position(1, 1)]
        current_state = state.with_queens_added(current_position)
        new_position = [Position(2, 2)]
        new_queen_state = current_state.with_queens_added(new_position)
        self.assertEqual(new_queen_state.queen_count(), 2)
        self.assertIn(Position(2, 2), new_queen_state.queens())
        self.assertIn(Position(1, 1), new_queen_state.queens())
        self.assertIn(Position(1, 1), current_state.queens())
        self.assertNotIn(Position(2, 2), current_state.queens())
        self.assertNotIn(Position(1, 1), state.queens())
        self.assertNotIn(Position(2, 2), state.queens())

    def test_queens_added_success_multiple_queen_rect(self):
        """Testcase: returns a new QueensState with multiple queens"""
        state = QueensState(4, 8)
        current_position = [Position(1, 1)]
        current_state = state.with_queens_added(current_position)
        new_position = [Position(2, 2)]
        new_queen_state = current_state.with_queens_added(new_position)
        self.assertEqual(new_queen_state.queen_count(), 2)
        self.assertIn(Position(2, 2), new_queen_state.queens())
        self.assertIn(Position(1, 1), new_queen_state.queens())
        self.assertIn(Position(1, 1), current_state.queens())
        self.assertNotIn(Position(2, 2), current_state.queens())
        self.assertNotIn(Position(1, 1), state.queens())
        self.assertNotIn(Position(2, 2), state.queens())

    def test_queens_added_success_add_multiple_queens_at_once_sq(self):
        """Testcase: adding multiple queens at once"""
        state = QueensState(8, 8)
        new_position = [Position(1, 1), Position(2, 2)]
        new_queen_state = state.with_queens_added(new_position)
        self.assertEqual(new_queen_state.queen_count(), 2)
        self.assertNotIn(Position(1, 1), state.queens())
        self.assertNotIn(Position(2, 2), state.queens())
        self.assertIn(Position(1, 1), new_queen_state.queens())
        self.assertIn(Position(2, 2), new_queen_state.queens())

    def test_queens_added_success_add_multiple_queens_at_once_rect(self):
        """Testcase: adding multiple queens at once"""
        state = QueensState(4, 8)
        new_position = [Position(1, 1), Position(2, 2)]
        new_queen_state = state.with_queens_added(new_position)
        self.assertEqual(new_queen_state.queen_count(), 2)
        self.assertNotIn(Position(1, 1), state.queens())
        self.assertNotIn(Position(2, 2), state.queens())
        self.assertIn(Position(1, 1), new_queen_state.queens())
        self.assertIn(Position(2, 2), new_queen_state.queens())

    def test_queens_added_failure_sq(self):
        """raise DuplicateQueenError when
        there is already a queen in the given positions"""
        state = QueensState(8, 8)
        current_position = [Position(1, 1)]
        current_state = state.with_queens_added(current_position)

        with self.assertRaises(DuplicateQueenError):
            current_state.with_queens_added([Position(1, 1)])

        self.assertIn(Position(1, 1), current_state.queens())
        self.assertNotIn(Position(1, 1), state.queens())

    def test_queens_added_failure_rect(self):
        """raise DuplicateQueenError when
        there is already a queen in the given positions"""
        state = QueensState(4, 8)
        current_position = [Position(1, 1)]
        current_state = state.with_queens_added(current_position)

        with self.assertRaises(DuplicateQueenError):
            current_state.with_queens_added([Position(1, 1)])

        self.assertIn(Position(1, 1), current_state.queens())
        self.assertNotIn(Position(1, 1), state.queens())

    def test_queens_removed_success_single_queen_sq(self):
        """Testcase: Builds a new QueensState with single queen removed"""
        state = QueensState(8, 8)
        current_position = [Position(1, 1)]
        current_state = state.with_queens_added(current_position)
        new_position = [Position(1, 1)]
        new_state = current_state.with_queens_removed(new_position)
        self.assertEqual(new_state.queen_count(), 0)
        self.assertNotIn(Position(1, 1), new_state.queens())

    def test_queens_removed_success_single_queen_rect(self):
        """Testcase: Builds a new QueensState with single queen removed"""
        state = QueensState(4, 8)
        current_position = [Position(1, 1)]
        current_state = state.with_queens_added(current_position)
        new_position = [Position(1, 1)]
        new_state = current_state.with_queens_removed(new_position)
        self.assertEqual(new_state.queen_count(), 0)
        self.assertNotIn(Position(1, 1), new_state.queens())

    def test_queens_removed_success_multiple_queen_sq(self):
        """Testcase: Builds a new QueensState with multiple queens removed"""
        state = QueensState(8, 8)
        current_position = [Position(1, 1), Position(2, 2)]
        current_state = state.with_queens_added(current_position)
        new_position = [Position(1, 1), Position(2, 2)]
        new_state = current_state.with_queens_removed(new_position)
        self.assertEqual(new_state.queen_count(), 0)
        self.assertNotIn(Position(1, 1), new_state.queens())
        self.assertNotIn(Position(2, 2), new_state.queens())

    def test_queens_removed_success_multiple_queen_rect(self):
        """Testcase: Builds a new QueensState with multiple queens removed"""
        state = QueensState(4, 8)
        current_position = [Position(1, 2), Position(2, 3)]
        current_state = state.with_queens_added(current_position)
        new_position = [Position(1, 2), Position(2, 3)]
        new_state = current_state.with_queens_removed(new_position)
        self.assertEqual(new_state.queen_count(), 0)
        self.assertNotIn(Position(1, 2), new_state.queens())
        self.assertNotIn(Position(2, 3), new_state.queens())

    def test_queens_removed_failure_sq(self):
        """raise MissingQueenError when there is no queen"""
        state = QueensState(8, 8)
        current_position = [Position(1, 1)]
        current_state = state.with_queens_added(current_position)

        with self.assertRaises(MissingQueenError):
            current_state.with_queens_removed([Position(0, 0)])

        self.assertIn(Position(1, 1), current_state.queens())
        self.assertNotIn(Position(1, 1), state.queens())

    def test_queens_removed_failure_rect(self):
        """raise MissingQueenError when there is no queen"""
        state = QueensState(4, 8)
        current_position = [Position(1, 1)]
        current_state = state.with_queens_added(current_position)

        with self.assertRaises(MissingQueenError):
            current_state.with_queens_removed([Position(0, 0)])

        self.assertIn(Position(1, 1), current_state.queens())
        self.assertNotIn(Position(1, 1), state.queens())


if __name__ == '__main__':
    unittest.main()
