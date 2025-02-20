from gomoku import Board

class GomokuAI:
    def __init__(self, board_size=20, search_depth=3):
        self.board_size = board_size
        self.search_depth = search_depth
        self.pattern_scores = {
            'win5': 500000000,    
            'open4': 100000,   
            'simple4': 20000,     
            'open3': 2000,   
            'broken3': 500, 
            'open2': 100,
            'broken2': 50
        }

    def update_candidate_moves(self, board, move, moves):
        x, y = move
        # Add an empty space within 2 spaces around
        for i in range(max(0, x-2), min(self.board_size, x+3)):
            for j in range(max(0, y-2), min(self.board_size, y+3)):
                if board.grid[i][j] is None:
                    if (i, j) in moves:
                        moves.remove((i, j))
                    moves.append((i, j)) 

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
            score -= self.pattern_scores['open4'] * 1.2
          
        for pattern in [f'{opponent}{opponent}{opponent}{opponent}.', 
                       f'.{opponent}{opponent}{opponent}{opponent}',
                       f'{opponent}{opponent}.{opponent}{opponent}']:
            score -= vector_str.count(pattern) * self.pattern_scores['simple4'] * 1.2
        
        for pattern in [f'..{opponent}{opponent}{opponent}..',
                       f'.{opponent}.{opponent}{opponent}.',
                       f'.{opponent}{opponent}.{opponent}.']:
            score -= vector_str.count(pattern) * self.pattern_scores['open3']
            
        return score
    
    def evaluate_board(self, board):
        vectors = self.get_vectors(board)
        ai_score = sum(self.evaluate_vector(v, 'O') for v in vectors)
        opponent_score = sum(self.evaluate_vector(v, 'X') for v in vectors)
        return ai_score - opponent_score
    
    def debug_evaluate_position(self, board):#Debug
        print("\n=== Debug: Evaluating Current Position ===")
        vectors = self.get_vectors(board)
        print(f"Total vectors found: {len(vectors)}")
        
        for i, vector in enumerate(vectors):
            vector_str = ''.join(['.' if x is None else x for x in vector])
            if 'OOOO' in vector_str:
                print(f"\nFound vector {i} with four O's:")
                print(f"Vector content: {vector_str}")
                score = self.evaluate_vector(vector, 'O')
                print(f"Vector score: {score}")
                
        total_score = self.evaluate_board(board)
        print(f"\nTotal board evaluation score: {total_score}")

    def minimax(self, board, depth, is_maximizing, moves, alpha=-float('inf'), beta=float('inf')):
        # Debug
        is_top_level = depth == self.search_depth

        if board.check_win():
            if is_maximizing:
                return -9999999999, None
            else:
                return 9999999999, None    
        
        if depth == 0:
            score = self.evaluate_board(board)
            if is_top_level: #debug
                print(f"Leaf node evaluation: {score}")
            return score, None
        
        best_move = None
        
        if is_maximizing:
            max_score = float('-inf')
            for move in moves:
                x, y = move
                board.grid[x][y] = 'O'
                old_last_move = board.last_move
                board.last_move = (x, y)
                # Debug: 打印模拟落子位置和上一步位置
                if is_top_level:
                    print(f"simulation: {(x, y)}, lastmove: {old_last_move}")

                new_moves = moves.copy()
                new_moves.remove(move)
                self.update_candidate_moves(board, move, new_moves)
                
                score, _ = self.minimax(board, depth-1, False, new_moves, alpha, beta)
                if is_top_level: #debug
                    print(f"Move {move} score: {score}")

                board.grid[x][y] = None
                board.last_move = old_last_move
                
                if score > max_score:
                    max_score = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score, best_move
        else:
            min_score = float('inf')
            for move in moves:
                x, y = move
                board.grid[x][y] = 'X'
                old_last_move = board.last_move
                board.last_move = (x, y)
                # Debug: 打印模拟落子位置和上一步位置
                if is_top_level:
                    print(f"simulation: {(x, y)}, lastmove: {old_last_move}")

                new_moves = moves.copy()
                new_moves.remove(move)
                self.update_candidate_moves(board, move, new_moves)
                
                score, _ = self.minimax(board, depth-1, True, new_moves, alpha, beta)
                if is_top_level:#debug
                    print(f"Move {move} score: {score}")

                board.grid[x][y] = None
                board.last_move = old_last_move
                
                if score < min_score:
                    min_score = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score, best_move