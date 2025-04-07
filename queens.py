# queens.py
#
# ICS 33 Spring 2025
# Project 0: History of Modern
#
# A module containing tools that could assist in solving variants of the
# well-known "n-queens" problem.  Note that we're only implementing one part
# of the problem: immutably managing the "state" of the board (i.e., which
# queens are arranged in which cells).  The rest of the problem -- determining
# a valid solution for it -- is not our focus here.
#
# Your goal is to complete the QueensState class described below, though
# you'll need to build it incrementally, as well as test it incrementally by
# writing unit tests in test_queens.py.  Make sure you've read the project
# write-up before you proceed, as it will explain the requirements around
# following (and documenting) an incremental process of solving this problem.
#
# DO NOT MODIFY THE Position NAMEDTUPLE OR THE PROVIDED EXCEPTION CLASSES.

from collections import namedtuple
from typing import Self, Type

Position = namedtuple('Position', ['row', 'column'])

# Ordinarily, we would write docstrings within classes or their methods.
# Since a namedtuple builds those classes and methods for us, we instead
# add the documentation by hand afterward.
Position.__doc__ = 'A position on a chessboard, specified by zero-based row and column numbers.'
Position.row.__doc__ = 'A zero-based row number'
Position.column.__doc__ = 'A zero-based column number'


class DuplicateQueenError(Exception):
    """An exception indicating an attempt to add a queen where one is already present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where the duplicate queen exists."""
        self._position = position

    def __str__(self) -> str:
        return f'duplicate queen in row {self._position.row} column {self._position.column}'


class MissingQueenError(Exception):
    """An exception indicating an attempt to remove a queen where one is not present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where a queen is missing."""
        self._position = position

    def __str__(self) -> str:
        return f'missing queen in row {self._position.row} column {self._position.column}'


class QueensState:
    """Immutably represents the state of a chessboard being used to assist in
    solving the n-queens problem."""

    def __init__(self, rows: int, columns: int):
        """Initializes the chessboard to have the given numbers of rows and columns,
        with no queens occupying any of its cells."""
        self.rows = rows
        self.columns = columns
        self.queen_position = []

    def queen_count(self) -> int:
        """Returns the number of queens on the chessboard."""
        return len(self.queen_position)

    def queens(self) -> list[Position]:
        """Returns a list of the positions in which queens appear on the chessboard,
        arranged in no particular order."""
        return self.queen_position

    def has_queen(self, position: Position) -> bool:
        """Returns True if a queen occupies the given position on the chessboard, or
        False otherwise."""
        return True if position in self.queens() else False

    def any_queens_unsafe(self) -> bool:
        """Returns True if any queens on the chessboard are unsafe (i.e., they can
        be captured by at least one other queen on the chessboard), or False otherwise."""
        if self.queen_count() < 2:
            return False
        queens = self.queens()
        for i, q1 in enumerate(queens):
            for q2 in queens[i+1:]:
                if q1.column == q2.column or q1.row == q2.row: # check if queens are in same row or column
                    return True
                elif abs(q1.column - q2.column) == abs(q1.row - q2.row): # check Diagonals
                    return True
        return False

    def with_queens_added(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens added in the given positions,
        without modifying 'self' in any way.  Raises a DuplicateQueenError when
        there is already a queen in at least one of the given positions."""
        new_queen_position = list(self.queen_position)
        for position in positions:
            if position in new_queen_position:
                raise DuplicateQueenError(position)
            new_queen_position.append(position)
        new_queen_state = QueensState(self.rows, self.columns)
        new_queen_state.queen_position = new_queen_position
        return new_queen_state

    def with_queens_removed(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens removed from the given positions,
        without modifying 'self' in any way.  Raises a MissingQueenError when there
        is no queen in at least one of the given positions."""
        new_queen_position = list(self.queen_position)
        for position in positions:
            if position in new_queen_position:
                new_queen_position.remove(position)
            raise MissingQueenError(position)
        new_queen_state = QueensState(self.rows, self.columns)
        new_queen_state.queen_position = new_queen_position
        return new_queen_state


