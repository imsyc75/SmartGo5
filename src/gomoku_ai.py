class GomokuAI:
    def __init__(self, board_size=20, search_depth=4):
        self.board_size = board_size
        self.search_depth = search_depth
        self.candidate_moves = []
        self.pattern_scores = {
            'win5': 50000,    
            'open4': 10000,   
            'simple4': 5000,     
            'open3': 2000,   
            'broken3': 500, 
            'open2': 100,
            'broken2': 50
        }

    def update_candidate_moves(self, board, move):
        x, y = move
        if (x, y) in self.candidate_moves:
            self.candidate_moves.remove((x, y)) 
        
        # Add an empty space within 2 spaces around
        for i in range(max(0, x-2), min(self.board_size, x+3)):
            for j in range(max(0, y-2), min(self.board_size, y+3)):
                if board.grid[i][j] is None and (i, j) not in self.candidate_moves:
                    self.candidate_moves.append((i, j)) 

    def get_vectors(self, board):
        vectors = []
        
        # Horizontal vector
        for i in range(self.board_size):
            if any(x is not None for x in board.grid[i]) or \
               (i > 0 and any(x is not None for x in board.grid[i-1])) or \
               (i < self.board_size-1 and any(x is not None for x in board.grid[i+1])):
                vectors.append(board.grid[i])
            
        # Vertical vector   
        for j in range(self.board_size):
            column = [board.grid[i][j] for i in range(self.board_size)]
            if any(x is not None for x in column) or \
               (j > 0 and any(board.grid[i][j-1] is not None for i in range(self.board_size))) or \
               (j < self.board_size-1 and any(board.grid[i][j+1] is not None for i in range(self.board_size))):
                vectors.append(column)
            
        # Main diagonal vector
        for i in range(-4, self.board_size-4):
            diagonal = []
            for j in range(max(0, -i), min(self.board_size-i, self.board_size)):
                diagonal.append(board.grid[j+i][j])
            if any(x is not None for x in diagonal):
                vectors.append(diagonal)
            
        # Another diagonal vector
        for i in range(-4, self.board_size-4):
            diagonal = []
            for j in range(max(0, -i), min(self.board_size-i, self.board_size)):
                diagonal.append(board.grid[j+i][self.board_size-1-j])
            if any(x is not None for x in diagonal):
                vectors.append(diagonal)
            
        return vectors

    def get_valid_moves(self, board):
        valid_moves = []
        last_x, last_y = board.last_move if board.last_move else (self.board_size//2, self.board_size//2)
        
        last_x, last_y = board.last_move
        priority_moves = []
        
        for i in range(max(0, last_x-1), min(self.board_size, last_x+2)):
            for j in range(max(0, last_y-1), min(self.board_size, last_y+2)):
                if board.grid[i][j] is None and (i, j) in self.candidate_moves:
                    priority_moves.append((i, j)) 
        
        if priority_moves:
            return priority_moves
            
        return self.candidate_moves
    
    def check_win(self, board, last_move): #Only check the lines related to the last move
        if not last_move:
            return False
            
        x, y = last_move
        player = board.grid[x][y]
        directions = [(1,0), (0,1), (1,1), (1,-1)] 
        
        for dx, dy in directions:
            count = 1  
            for direction in [-1, 1]:
                nx, ny = x + dx * direction, y + dy * direction
                while (0 <= nx < self.board_size and 
                       0 <= ny < self.board_size and 
                       board.grid[nx][ny] == player):
                    count += 1
                    if count >= 5:
                        return True
                    nx += dx * direction
                    ny += dy * direction
        return False
    
    def evaluate_vector(self, vector, player):
        score = 0
        vector_str = ''.join(['.' if x is None else x for x in vector])
        opponent = 'X' if player == 'O' else 'O'
        
        if f'{player}{player}{player}{player}{player}' in vector_str:
            score += self.pattern_scores['win5']
        
        if f'.{player}{player}{player}{player}.' in vector_str:
            score += self.pattern_scores['open4']
        
        for pattern in [f'{player}{player}{player}{player}.', 
                       f'.{player}{player}{player}{player}',
                       f'{player}{player}.{player}{player}']:
            score += vector_str.count(pattern) * self.pattern_scores['simple4']

        for pattern in [f'..{player}{player}{player}..',
                       f'.{player}.{player}{player}.',
                       f'.{player}{player}.{player}.']:
            score += vector_str.count(pattern) * self.pattern_scores['open3']

        for pattern in [f'..{player}{player}{player}.',
                       f'.{player}{player}{player}..',
                       f'{player}{player}.{player}',
                       f'{player}.{player}{player}']:
            score += vector_str.count(pattern) * self.pattern_scores['broken3']

        for pattern in [f'...{player}{player}...',
                       f'..{player}.{player}..',
                       f'.{player}..{player}.',
                       f'.{player}.{player}..']:
            score += vector_str.count(pattern) * self.pattern_scores['open2']
        
        for pattern in [f'..{player}{player}.',
                       f'.{player}{player}..',
                       f'.{player}.{player}',
                       f'{player}..{player}']:
            score += vector_str.count(pattern) * self.pattern_scores['broken2']
            
        # Adversary Threat Assessment
        if f'.{opponent}{opponent}{opponent}{opponent}.' in vector_str:
            score -= self.pattern_scores['open4'] * 2
          
        for pattern in [f'{opponent}{opponent}{opponent}{opponent}.', 
                       f'.{opponent}{opponent}{opponent}{opponent}',
                       f'{opponent}{opponent}.{opponent}{opponent}']:
            score -= vector_str.count(pattern) * self.pattern_scores['simple4'] * 1.5
        
        for pattern in [f'..{opponent}{opponent}{opponent}..',
                       f'.{opponent}.{opponent}{opponent}.',
                       f'.{opponent}{opponent}.{opponent}.']:
            score -= vector_str.count(pattern) * self.pattern_scores['open3'] * 1.2
            
        return score
    
    def evaluate_board(self, board):
        vectors = self.get_vectors(board)
        ai_score = sum(self.evaluate_vector(v, 'O') for v in vectors)
        opponent_score = sum(self.evaluate_vector(v, 'X') for v in vectors)
        return ai_score - opponent_score

    def minimax(self, board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        if self.check_win(board, board.last_move):
            if is_maximizing:
                return -1000000, None
            else:
                return 1000000, None
            
        if depth == 0:
            return self.evaluate_board(board), None
        
        valid_moves = self.get_valid_moves(board)
        best_move = None
        
        if board.last_move:
            last_x, last_y = board.last_move
            valid_moves = sorted(valid_moves, 
                               key=lambda m: abs(m[0]-last_x) + abs(m[1]-last_y)) 
        
        
        if is_maximizing:
            max_score = float('-inf')
            for move in valid_moves:
                x, y = move
                board.grid[x][y] = 'O'
                old_last_move = board.last_move
                board.last_move = (x, y)
                
                #关注一下这里之后的代码。
                old_candidates = self.candidate_moves.copy()
                self.update_candidate_moves(board, move)
                
                score, _ = self.minimax(board, depth-1, False, alpha, beta)
                
                board.grid[x][y] = None
                board.last_move = old_last_move
                self.candidate_moves = old_candidates
                
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
                old_last_move = board.last_move
                board.last_move = (x, y)
                
                old_candidates = self.candidate_moves.copy()
                self.update_candidate_moves(board, move)
                
                score, _ = self.minimax(board, depth-1, True, alpha, beta)
                
                board.grid[x][y] = None
                board.last_move = old_last_move
                self.candidate_moves = old_candidates
                
                if score < min_score:
                    min_score = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score, best_move