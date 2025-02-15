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
        self.assertEqual(self.game.current_player, 'O')  # AI's turn
    
    def test_win_detection(self):
        #Check if player 'X' wins are correctly detected after step 5
        moves = [(0,0), (0,1), (0,2), (0,3), (0,4)]
        result = self.game.play_turn(*moves[-1])
        for x, y in moves[:-1]:
            self.game.play_turn(x, y)
            self.assertIsNone(result)  

        self.assertEqual(result, 'X')