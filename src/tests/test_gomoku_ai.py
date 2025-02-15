import unittest
from ..gomoku import Board
from ..gomoku_ai import GomokuAI

class TestGomokuAI(unittest.TestCase):
    def setUp(self):
        self.board = Board(size=20)
        self.ai = GomokuAI(board_size=20)
        
    def test_ai_initialization(self):
        self.assertEqual(self.ai.board_size, 20)
        self.assertEqual(self.ai.search_depth, 4)
        self.assertIsNotNone(self.ai.pattern_scores)
        self.assertEqual(len(self.ai.candidate_moves), 1)  # Initial center move
        
    def test_candidate_moves_update(self):
        # Test initial move
        initial_move = (10, 10)
        self.board.make_move(*initial_move, 'X')
        self.ai.update_candidate_moves(self.board, initial_move)
        
        # Should generate moves within 2 spaces of the initial move
        for move in self.ai.candidate_moves:
            x, y = move
            self.assertTrue(abs(x - initial_move[0]) <= 2)
            self.assertTrue(abs(y - initial_move[1]) <= 2)
            
        # Test that occupied positions are not in candidates
        self.assertNotIn(initial_move, self.ai.candidate_moves)
        
    def test_get_vectors(self):
        # Place some moves on the board
        moves = [(5,5), (5,6), (6,5)]
        for x, y in moves:
            self.board.make_move(x, y, 'X')
            
        vectors = self.ai.get_vectors(self.board)
        self.assertGreater(len(vectors), 0)
        
        # Check if horizontal vector contains our moves
        horizontal_vector = [vec for vec in vectors if vec[5][5:7] == ['X', 'X']]
        self.assertTrue(any(horizontal_vector))
        
    def test_evaluate_vector(self):
        # Test empty vector
        empty_vector = [None] * 20
        score = self.ai.evaluate_vector(empty_vector, 'O')
        self.assertEqual(score, 0)
        
        # Test winning pattern
        winning_vector = [None] * 20
        for i in range(5):
            winning_vector[i] = 'O'
        score = self.ai.evaluate_vector(winning_vector, 'O')
        self.assertEqual(score, self.ai.pattern_scores['win5'])
        
        # Test open four pattern
        open_four = [None] * 20
        open_four[1:5] = ['O'] * 4
        score = self.ai.evaluate_vector(open_four, 'O')
        self.assertGreater(score, 0)
        
    def test_minimax_basic(self):
        # Test immediate winning move
        self.board.make_move(10, 10, 'O')
        self.board.make_move(10, 11, 'O')
        self.board.make_move(10, 12, 'O')
        self.board.make_move(10, 13, 'O')
        self.board.last_move = (10, 13)
        
        self.ai.update_candidate_moves(self.board, (10, 13))
        score, move = self.ai.minimax(self.board, 2, True)
        
        # AI should find the winning move at (10, 14)
        self.assertIsNotNone(move)
        self.assertEqual(move, (10, 14))
        
    def test_get_valid_moves(self):
        # Test valid moves generation with empty board
        self.board.make_move(10, 10, 'X')
        self.board.last_move = (10, 10)
        self.ai.update_candidate_moves(self.board, (10, 10))
        
        valid_moves = self.ai.get_valid_moves(self.board)
        self.assertTrue(len(valid_moves) > 0)
        
        # All moves should be valid board positions
        for x, y in valid_moves:
            self.assertTrue(0 <= x < self.board.size)
            self.assertTrue(0 <= y < self.board.size)
            self.assertIsNone(self.board.grid[x][y])
            
    def test_evaluate_board(self):
        # Empty board should have neutral evaluation
        score = self.ai.evaluate_board(self.board)
        self.assertEqual(score, 0)
        
        # Board with advantage for AI should have positive score
        self.board.make_move(10, 10, 'O')
        self.board.make_move(10, 11, 'O')
        self.board.make_move(10, 12, 'O')
        score = self.ai.evaluate_board(self.board)
        self.assertGreater(score, 0)
        
        # Board with advantage for opponent should have negative score
        self.board = Board(size=20)  # Reset board
        self.board.make_move(10, 10, 'X')
        self.board.make_move(10, 11, 'X')
        self.board.make_move(10, 12, 'X')
        score = self.ai.evaluate_board(self.board)
        self.assertLess(score, 0)

if __name__ == '__main__':
    unittest.main()