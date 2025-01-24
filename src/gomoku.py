class Board:
    def __init__(self, size=20):
        self.size = size
        self.grid = [[None] * size for _ in range(size)]
        self.move_manager = MoveManager(size)
        self.win_checker = WinChecker(size)
        self.available_moves = set((i, j) for i in range(size) for j in range(size))
        self.last_move = None
    
    def make_move(self, x, y, player):
        if 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] is None:
            self.grid[x][y] = player
            self.available_moves.remove((x, y))
            self.last_move = (x, y)
            return True
        return False
    
    def check_win(self):
            return self.win_checker.check_win(self, self.last_move)
  
        
class MoveManager:
    def __init__(self, board_size):
        self.board_size = board_size


class WinChecker:
    def __init__(self, board_size=20, win_count=5):
        self.board_size = board_size
        self.win_count = win_count
        # four directions: horizontal, vertical, two diagonals
        self.directions = [[(-1, 0),(1, 0)],
                           [(0, -1), (0, 1)],
                           [(-1, 1), (1, -1)],
                           [(-1, -1), (1, 1)]]  

    def check_win(self, board, last_move):
        if not last_move:
            return False
            
        x, y = last_move
        player = board.grid[x][y]
        
        for axis in self.directions:
            count = 1
            for (dx, dy) in axis:
                count += self.direction_count(x, y, dx, dy, player, board)
                if count >= 5:
                    return True

        return False
    
    def direction_count(self, x, y, xdirection, ydirection, player, board):
        count = 0
        next_x, next_y = x + xdirection, y + ydirection
        
        while 0 <= next_x < self.board_size and 0 <= next_y < self.board_size:
            if board.grid[next_x][next_y] == player:
                count += 1
                next_x += xdirection
                next_y += ydirection
            else:
                break
        return count
    