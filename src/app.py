from gomoku import Board
from gomoku_ai import GomokuAI

class GomokuGame:
    def __init__(self, board_size=20):
        self.board = Board(board_size)
        self.current_player = 'X'
        self.ai = GomokuAI(board_size)
        self.moves = []

    def play_turn(self, x, y):
        print(f"Game received move: ({x}, {y})") #debug
        if self.board.make_move(x, y, self.current_player):
            print(f"Move made, last_move is now: {self.board.last_move}") #debug
            if (x, y) in self.moves:
                self.moves.remove((x, y))
            self.ai.update_candidate_moves(self.board, (x, y), self.moves)
            
            if self.board.check_win():
                return self.current_player
                
            if self.current_player == 'X':  # X is player, O is AI
                self.current_player = 'O'
                # debug: 在 AI 行动前添加调试
                self.ai.debug_evaluate_position(self.board)
                # AI moves
                _, ai_move = self.ai.minimax(self.board, self.ai.search_depth, True, self.moves)
                if ai_move:
                    return self.play_turn(*ai_move)
            else:
                self.current_player = 'X'
            return None
        return False
    
    def start(self):
        print("Game started")