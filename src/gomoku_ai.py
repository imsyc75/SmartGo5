# code design based on https://github.com/ZitongMao/gomoku-ai/blob/aeca9f0a52ec7f2b81faad441d846b33c9dc9049/gomoku_ai.py

class GomokuAI:
    def __init__(self, board_size=20, search_depth=4):
        self.board_size = board_size
        self.search_depth = search_depth
        self.pattern_scores = {
            'win5': 50000,    
            'open4': 10000,   
            'simple4': 5000,     
            'open3': 2000,   
            'broken3': 500, 
            'open2': 100,
            'broken2': 50
        }

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

    def has_neighbor(self, board, x, y, distance=2):
        #Check if there are chess pieces around the specified position
        start_x = max(0, x - distance)
        end_x = min(self.board_size, x + distance + 1)
        start_y = max(0, y - distance)
        end_y = min(self.board_size, y + distance + 1)
        
        return any(board.grid[i][j] is not None 
                  for i in range(start_x, end_x)
                  for j in range(start_y, end_y)
                  if (i != x or j != y))

    def get_valid_moves(self, board):
        valid_moves = set()
        last_x, last_y = board.last_move if board.last_move else (self.board_size//2, self.board_size//2)
        
        #Prioritize searching the positions around the last move
        search_radius = 2
        start_x = max(0, last_x - search_radius)
        end_x = min(self.board_size, last_x + search_radius + 1)
        start_y = max(0, last_y - search_radius)
        end_y = min(self.board_size, last_y + search_radius + 1)
        
        for i in range(start_x, end_x):
            for j in range(start_y, end_y):
                if board.grid[i][j] is None and self.has_neighbor(board, i, j):
                    valid_moves.add((i, j))
                    
        if not valid_moves:
            #If no suitable move is found, expand the search range
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if board.grid[i][j] is None and self.has_neighbor(board, i, j, 3):
                        valid_moves.add((i, j))
                        
        return valid_moves if valid_moves else {(self.board_size//2, self.board_size//2)}

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
        if depth == 0 or board.check_win():
            return self.evaluate_board(board), None
            
        valid_moves = self.get_valid_moves(board)
        best_move = None
        
        if is_maximizing:
            max_score = float('-inf')
            for move in valid_moves:
                x, y = move
                board.grid[x][y] = 'O'
                score, _ = self.minimax(board, depth-1, False, alpha, beta)
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
                score, _ = self.minimax(board, depth-1, True, alpha, beta)
                board.grid[x][y] = None
                
                if score < min_score:
                    min_score = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score, best_move