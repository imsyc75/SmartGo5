from gomoku import Board
from gomoku_ai import GomokuAI

class GomokuGame:
    def __init__(self, board_size=20):
        self.board = Board(board_size)
        self.current_player = 'X'
        self.ai = GomokuAI(board_size)
    
    def play_turn(self, x, y):
        if self.board.make_move(x, y, self.current_player):
            if self.board.check_win():
                return self.current_player
            if self.current_player == 'X':  # X is player, O is AI
                self.current_player = 'O'
                if not self.board.last_move:
                    center = self.board.size // 2
                    return self.play_turn(center, center)
                
                _, ai_move = self.ai.minimax(self.board, self.ai.search_depth, True)
                if ai_move:
                    return self.play_turn(*ai_move)
            else:
                self.current_player = 'X'
            return None
        return False
    
    def start(self):
        print("Game started")