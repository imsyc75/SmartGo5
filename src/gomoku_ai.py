class GomokuAI:
    def __init__(self, board_size=20, search_depth=2):
        self.board_size = board_size
        self.search_depth = search_depth
        # These numbers represent the threat value of different chess patterns. 
        self.pattern_scores = {
            'win5': 50000,    
            'open4': 4300,   
            'simple4': 700,     
            'open3': 7200,   
            'broken3': 100, 
        } 
        # High-value chess patterns will strongly influence the AI's choice, giving priority to forming or defending high-value chess patterns.
        

    def get_next_move(self, board):
        valid_moves = self._get_valid_moves(board)
        best_score = float('-inf')
        best_move = None
        
        for move in valid_moves:
            x, y = move
            board.grid[x][y] = 'O'  # # X is player, O is AI
            score = self._minimax(board, self.search_depth, False)
            board.grid[x][y] = None
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move


    def _get_valid_moves(self, board):
        valid_moves = set()
        directions = [(-1, 0),(1, 0),
                      (0, -1), (0, 1),
                      (-1, 1), (1, -1),
                      (-1, -1), (1, 1)]  
        
        for x in range(self.board_size):
            for y in range(self.board_size):
                if board.grid[x][y] is not None:
                    for dx, dy in directions:
                        new_x, new_y = x + dx, y + dy
                        if (0 <= new_x < self.board_size and 
                            0 <= new_y < self.board_size and 
                            board.grid[new_x][new_y] is None):
                            valid_moves.add((new_x, new_y))
                            
        return valid_moves if valid_moves else board.available_moves


    def _minimax(self, board, depth, is_maximizing):
        if depth == 0 or board.check_win():
            return self._evaluate_board(board)
            
        valid_moves = self._get_valid_moves(board)
        
        if is_maximizing:
            max_score = float('-inf')
            for move in valid_moves:
                x, y = move
                board.grid[x][y] = 'O'
                score = self._minimax(board, depth-1, False)
                board.grid[x][y] = None
                max_score = max(score, max_score)
            return max_score
        else:
            min_score = float('inf')
            for move in valid_moves:
                x, y = move
                board.grid[x][y] = 'X'
                score = self._minimax(board, depth-1, True)
                board.grid[x][y] = None
                min_score = min(score, min_score)
            return min_score


    def _evaluate_board(self, board):
        ai_score = self._evaluate_player(board, 'O')
        opponent_score = self._evaluate_player(board, 'X')
        return ai_score - opponent_score


    def _evaluate_player(self, board, player):
        total_score = 0
        # Horizontal direction
        for i in range(self.board_size):
            line = ''.join([str(board.grid[i][j]) if board.grid[i][j] else '.' 
                          for j in range(self.board_size)])
            total_score += self._evaluate_line(line, player)
            
        # Vertical direction 
        for j in range(self.board_size):
            line = ''.join([str(board.grid[i][j]) if board.grid[i][j] else '.' 
                          for i in range(self.board_size)])
            total_score += self._evaluate_line(line, player)
            
        # Diagonal direction
        for i in range(self.board_size-4):
            # Top left to bottom right
            line = ''.join([str(board.grid[i+k][i+k]) if board.grid[i+k][i+k] else '.' 
                          for k in range(self.board_size-i)])
            total_score += self._evaluate_line(line, player)
            # Bottom left to top right
            line = ''.join([str(board.grid[i+k][self.board_size-1-i-k]) 
                          if board.grid[i+k][self.board_size-1-i-k] else '.' 
                          for k in range(self.board_size-i)])
            total_score += self._evaluate_line(line, player)
            
        return total_score
        

    def _evaluate_line(self, line, player):
        score = 0
        opponent = 'X' if player == 'O' else 'O'
        
        # win5
        if f'{player}{player}{player}{player}{player}' in line:
            score += self.pattern_scores['win5']
            
        # open4
        if f'.{player}{player}{player}{player}.' in line:
            score += self.pattern_scores['open4']
            
        # simple4
        pat_simple4 = [f'{player}{player}{player}{player}.', 
                    f'.{player}{player}{player}{player}',
                    f'{player}{player}.{player}{player}']
        for pattern in pat_simple4:
            score += line.count(pattern) * self.pattern_scores['simple4']
            
        # open3
        if f'..{player}{player}{player}..' in line:
            score += self.pattern_scores['open3']
            
        # broken3
        pat_broken3 = [f'..{player}{player}{player}.',
                    f'.{player}{player}{player}..',
                    f'.{player}.{player}{player}.',
                    f'.{player}{player}.{player}.']
        for pattern in pat_broken3:
            score += line.count(pattern) * self.pattern_scores['broken3']
            
        return score