from gomoku import Board

class GomokuGame:
    def __init__(self, board_size=20):
        self.board = Board(board_size)
        self.current_player = 'X'
    
    def play_turn(self, x, y):
        if self.board.make_move(x, y, self.current_player):
            if self.board.check_win():
                return self.current_player
            if self.current_player == 'X':
                self.current_player = 'O' 
            else:
                self.current_player = 'X'
            return None
        return False
    
    def start(self):
        print("Game started")