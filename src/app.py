from .gomoku import Board
from .gomoku_ai import GomokuAI

class GomokuGame:
    def __init__(self, board_size=20):
        self.board = Board(board_size)
        self.current_player = 'X'
        self.ai = GomokuAI(board_size)
        self.ai.candidate_moves = [(board_size//2, board_size//2)]  

    def play_turn(self, x, y):
        if self.board.make_move(x, y, self.current_player):
            self.ai.update_candidate_moves(self.board, (x, y))
            
            if self.ai.check_win(self.board, (x, y)):
                return self.current_player
                
            if self.current_player == 'X':  # X is player, O is AI
                self.current_player = 'O'
                
                # AI moves
                _, ai_move = self.ai.minimax(self.board, self.ai.search_depth, True)
                if ai_move:
                    return self.play_turn(*ai_move)
            else:
                self.current_player = 'X'
            return None
        return False
    
    def start(self):
        print("Game started")