# Gomoku logic design based on xerwin's tutorial
# http://www.cnblogs.com/erwin/p/7828956.html

class Board:
    def __init__(self, size=20):
        self.size = size
        self.grid = [[None] * size for _ in range(size)]
        self.win_checker = WinChecker(size)
        self.available_moves = set((i, j) for i in range(size) for j in range(size))
        self.last_move = None
    
    def make_move(self, x, y, player):
        """
        Make movement in somewhere.

        Args:
        x: horizontal axis
        y: vertival axis
        player: "X"(human) or "O"(AI)

        Return:
        bool: If the move was successful, return true, otherwise False.
        """
        
        if 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] is None:
            self.grid[x][y] = player
            self.available_moves.remove((x, y))
            self.last_move = (x, y)
            return True
        return False
    
    def check_win(self):
            return self.win_checker.check_win(self, self.last_move)


class WinChecker:
    def __init__(self, board_size=20):
        self.board_size = board_size
        self.directions = [[(-1, 0),(1, 0)], # up and down
                           [(0, -1), (0, 1)], # left and right
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
        """
        Count the number of consecutive pieces of the same color from a given position in a give direction

        Args:
        x: horizontal axis
        y: vertival axis
        xdirection: offset in the x direction
        ydirection: offset in the y ditection
        player: "X"(human) or "O"(AI)
        board: the board

        Return:
        count(int): the number of consectuive pieces of same color in a give direction.
        """

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
    