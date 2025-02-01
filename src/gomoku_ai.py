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
        

    def _get_valid_moves(self, board):
        valid_moves = set()
        x, y = board.last_move  
    
        search_radius = 2  
    
        start_x = max(0, x - search_radius)
        end_x = min(self.board_size, x + search_radius + 1)
        start_y = max(0, y - search_radius)
        end_y = min(self.board_size, y + search_radius + 1)
    
        for i in range(start_x, end_x):
            for j in range(start_y, end_y):
                if board.grid[i][j] is None:  
                    has_neighbor = False
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            ni, nj = i + dx, j + dy
                            if (0 <= ni < self.board_size and 
                                0 <= nj < self.board_size and 
                                board.grid[ni][nj] is not None):
                                has_neighbor = True
                                break
                        if has_neighbor:
                            break
                    if has_neighbor:
                        valid_moves.add((i, j))
    
        if not valid_moves:  
        # If no valid moves are found, the search radius is increased to 4 and the search is repeated.
            search_radius *= 2
            return self._get_valid_moves(board)
    
        return valid_moves

    
    def _minimax(self, board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        if depth == 0 or board.check_win():
            return self._evaluate_board(board), None
        
        valid_moves = self._get_valid_moves(board)
        best_move = None
    
        if is_maximizing:
            max_score = float('-inf')
            for move in valid_moves:
                x, y = move
                board.grid[x][y] = 'O'
                score, _ = self._minimax(board, depth-1, False, alpha, beta)
                board.grid[x][y] = None
            
                if score > max_score:
                    max_score = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score, best_move
        else:
            min_score = float('inf')
            for move in valid_moves:
                x, y = move
                board.grid[x][y] = 'X'
                score, _ = self._minimax(board, depth-1, True, alpha, beta)
                board.grid[x][y] = None
            
                if score < min_score:
                    min_score = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score, best_move


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