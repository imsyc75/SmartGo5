import unittest
from ..app import GomokuGame

class TestGomokuGame(unittest.TestCase):
    def setUp(self):
        self.game = GomokuGame(board_size=20)
    
    def test_game_initialization(self):
       # Check that player 'X' is correctly set as the first player when the game starts
        self.assertEqual(self.game.current_player, 'X')
        self.assertIsNotNone(self.game.ai)
    
    def test_player_turn_sequence(self):
        result = self.game.play_turn(3, 4)
        self.assertIsNone(result)  # No win
        self.assertEqual(self.game.current_player, 'X')  # After AI playing, its player.
    
    def test_win_detection(self):
        # Create a new game instance to test the win detection logic, avoiding the influence of AI
        game = GomokuGame(board_size=20)
        game.moves = []

        for i in range(4):
            game.board.grid[0][i] = 'X'

        game.board.last_move = (0, 3)
        game.current_player = 'X'
        result = game.play_turn(0, 4)
        self.assertEqual(result, 'X')