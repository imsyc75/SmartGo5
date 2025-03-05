import unittest
from ..gomoku import Board, WinChecker

class TestWinChecker(unittest.TestCase):
    def setUp(self):
        self.board = Board(size=20)
        self.win_checker = WinChecker(board_size=20)
    
    def test_horizontal_win(self):
        for i in range(5):
            self.board.make_move(3, i, 'X')
        self.assertTrue(self.win_checker.check_win(self.board, (3, 4)))
    
    def test_vertical_win(self):
        for i in range(5):
            self.board.make_move(i, 3, 'O')
        self.assertTrue(self.win_checker.check_win(self.board, (4, 3)))
    
    def test_diagonal_win(self):
        for i in range(5):
            self.board.make_move(i, i, 'X')
        self.assertTrue(self.win_checker.check_win(self.board, (4, 4)))
        
        board2 = Board(size=20)
        for i in range(5):
            board2.make_move(i, 4-i, 'O')
        self.assertTrue(self.win_checker.check_win(board2, (4, 0)))
    
    def test_no_win(self):
        moves = [(0,0), (1,1), (2,2), (3,3)]
        for x, y in moves:
            self.board.make_move(x, y, 'X')
        self.assertFalse(self.win_checker.check_win(self.board, (3, 3)))
    
    def test_direction_count(self):
        moves = [(5,5), (6,5), (7,5)] 
        for x, y in moves:
            self.board.make_move(x, y, 'X')
        count = self.win_checker.direction_count(5, 5, 1, 0, 'X', self.board)
        self.assertEqual(count, 2)  
    
    def test_check_win_with_no_last_move(self):
        result = self.win_checker.check_win(self.board, None)
    
        self.assertFalse(result)
    
        self.board.last_move = None
        result = self.win_checker.check_win(self.board, self.board.last_move)
        self.assertFalse(result) 
    

if __name__ == '__main__':
    unittest.main()