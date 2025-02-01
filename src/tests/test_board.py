import unittest
from gomoku import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(size=20)
    
    def test_board_initialization(self): # Check the board initialization status
        self.assertEqual(self.board.size, 20)
        self.assertEqual(len(self.board.grid), 20)
        self.assertEqual(len(self.board.grid[0]), 20)
        self.assertEqual(len(self.board.available_moves), 400)
        self.assertIsNone(self.board.last_move)
        
    def test_valid_move(self):
        self.assertTrue(self.board.make_move(3, 4, 'X'))
        self.assertEqual(self.board.grid[3][4], 'X')
        self.assertEqual(self.board.last_move, (3, 4))
        self.assertNotIn((3, 4), self.board.available_moves)
        
    def test_out_of_bounds_move(self):
        self.assertFalse(self.board.make_move(-1, 0, 'X'))
        self.assertFalse(self.board.make_move(20, 0, 'X'))
        self.assertFalse(self.board.make_move(0, -1, 'X'))
        self.assertFalse(self.board.make_move(0, 20, 'X'))
        
    def test_duplicate_move(self):
        self.assertTrue(self.board.make_move(3, 4, 'X'))
        self.assertFalse(self.board.make_move(3, 4, 'O'))
        self.assertEqual(self.board.grid[3][4], 'X') # Original piece should remain
        
    def test_available_moves_update(self): # Update verification of available position set
        initial_moves = len(self.board.available_moves)
        self.board.make_move(3, 4, 'X')
        self.assertEqual(len(self.board.available_moves), initial_moves - 1)
        
    def test_multiple_valid_moves(self): # Can multiple consecutive moves be executed correctly?
        moves = [(3, 4), (10, 10), (0, 0), (19, 19)]
        for x, y in moves:
            self.assertTrue(self.board.make_move(x, y, 'X'))
        
        for x, y in moves:
            self.assertEqual(self.board.grid[x][y], 'X')
            self.assertNotIn((x, y), self.board.available_moves)

if __name__ == '__main__':
    unittest.main()
