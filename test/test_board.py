import unittest
from hypothesis import given, settings, strategies, assume
from unittest.mock import Mock, patch
import hypothesis.strategies as some

from board import Board, Piece, Spot, FullError


class TestPiece(unittest.TestCase):

    @given(player_number=strategies.integers())
    def test_init_and_player_number(self, player_number) -> None:
        piece = Piece(player_number)
        self.assertEqual(piece.player_number, player_number)


class TestSpot(unittest.TestCase):

    def setUp(self) -> None:
        self.spot = Spot()

    def test_init(self) -> None:
        self.assertIsNone(self.spot.piece)

    def test_piece_getter(self) -> None:
        piece: Piece = Piece(1)
        self.spot._piece = piece
        self.assertEqual(self.spot.piece, piece)

    @given(first=strategies.integers(), second=strategies.integers())
    def test_add_piece(self, first, second) -> None:
        self.spot: Spot = Spot()
        self.assertIsNone(self.spot.piece)
        self.spot.add_piece(first)
        self.assertIsNotNone(self.spot.piece)
        self.assertEqual(self.spot.piece.player_number, first)
        self.assertRaises(FullError, self.spot.add_piece, second)

    @given(playernum=strategies.integers())
    def test_is_player_empty(self, playernum: int) -> None:
        self.spot: Spot = Spot()
        self.assertFalse(self.spot.is_player(playernum))

    @given(first=strategies.integers(), second=strategies.integers())
    def test_is_player_nonempty(self, first: int, second: int) -> None:
        self.spot: Spot = Spot()
        self.spot.add_piece(first)
        self.assertEqual(self.spot.is_player(second), first == second)

    @given(some.integers())
    def test_is_empty(self, test_int: int) -> None:
        """
        function to test the is_empty function
        """
        self.spot._piece = test_int
        if test_int is None:
            self.assertEqual(self.spot.is_empty(), True)
        else:
            self.assertEqual(self.spot.is_empty(), False)

    @given(some.integers())
    def test_player_number(self, test_int: int) -> None:
        """
        function to test the player_number function
        """
        self.spot.add_piece(test_int)
        if test_int is None:
            self.assertEqual(self.spot.player_number(), 0)
        else:
            self.assertEqual(self.spot.player_number(), test_int)
        self.spot._piece = None

    def test_player_number_when_None(self) -> None:
        """
        function to test the player_number function when piece is None
        """
        test_spot: Spot = Spot()
        self.assertEqual(test_spot.player_number(), 0)

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board: Board = Board()
    
    # No deadline was a temporary change to satisfy CI/CD
    @settings(deadline=None)
    @given(x=strategies.integers(0, 6), y=strategies.integers(0, 5))
    def test_init_empty(self, x, y) -> None:
        self.board: Board = Board()
        self.assertEqual(len(self.board._board), 6)
        self.assertEqual(len(self.board._board[y]), 7)
        self.assertIsInstance(self.board._board[y][x], Spot)

    # No deadline was a temporary change to satisfy CI/CD
    # @settings(deadline=None)
    # @given(width=strategies.integers(1, 100),
    #        height=strategies.integers(1, 100),
    #        x=strategies.integers(0, 100),
    #        y=strategies.integers(0, 100))
    # def test_init_args(self, width: int, height: int, x: int, y: int) -> None:
    #     assume(x < width)
    #     assume(y < height)
    #     self.board = board.Board(width, height)
    #     self.assertEqual(len(self.board._board), height)
    #     self.assertEqual(len(self.board._board[y]), width)
    #     self.assertIsInstance(self.board._board[y][x], board.Spot)

    @given(some.tuples(some.integers(), some.integers()))
    def test_window_size_getter(self, test_tuple: tuple[int, int]) -> None:
        """
        function to test the window_size getter property
        """
        self.board._window_size = test_tuple
        self.assertEqual(self.board.window_size, test_tuple)

    @given(some.integers())
    def test_window_width_getter(self, test_int: int) -> None:
        """
        function to test the window_width getter
        """
        self.board._window_width = test_int
        self.assertEqual(self.board.window_width, test_int)

    @given(some.integers())
    def test_window_height_getter(self, test_int: int) -> None:
        """
        function to test the window_height getter
        """
        self.board._window_height = test_int
        self.assertEqual(self.board.window_height, test_int)

    def test_spot(self) -> None:
        """
        function to test the spot getter property
        """
        self.assertEqual(isinstance(self.board.spot, Spot), True)

    @given(some.integers())
    def test_rows_getter(self, test_int: int) -> None:
        """
        function to test the rows getter property
        """
        self.board._rows = test_int
        self.assertEqual(self.board.rows, test_int)

    @given(some.integers())
    def test_cols_getter(self, test_int: int) -> None:
        """
        function to test the cols getter property
        """
        self.board._cols = test_int
        self.assertEqual(self.board.cols, test_int)

    def test_reset(self) -> None:
        """
        function to test the reset method
        """
        self.board.reset()
        for row in self.board._board:
            for spot in row:
                self.assertIs(spot._piece, None)

    def test_get_player_at_spot(self) -> None:
        """
        function to test the get_player_at_spot method
        """
        self.board._board[0][0].add_piece(1)
        self.assertEqual(self.board.get_player_at_spot(0,0), 1)
        self.board.reset()
        self.assertEqual(self.board.get_player_at_spot(0,0), 0)

    def test_drop_piece(self) -> None:
        """
        function to test the drop_piece method
        """
        self.board.reset()
        self.board.drop_piece(1, 2)
        self.assertEqual(self.board.get_player_at_spot(1,0), 2)
        try:
            self.board.drop_piece(-1, 1)
        except(ValueError):
            pass
        try:
            self.board.reset()
            for i in range(7):
                self.board.drop_piece(0, 1)
        except(FullError):
            pass