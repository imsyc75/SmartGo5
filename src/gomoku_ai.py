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
        """
        Update the list of candidate positions.
        Add empty spaces within 2 spaces arount the last move as candidate positions.

        Args:
        board: the board
        move: the position of the last move (x,y)
        moves: the list of candidate positions
        """

        x, y = move
        # Add an empty space within 2 spaces around
        for i in range(max(0, x-2), min(self.board_size, x+3)):
            for j in range(max(0, y-2), min(self.board_size, y+3)):
                if board.grid[i][j] is None:
                    if (i, j) in moves:
                        moves.remove((i, j))
                    moves.append((i, j)) 

    def get_vectors(self, board):
        """
        Get all valid vectors(rows, columns and diagonals) on the chess board.

        Return:
        vectors(list): list of all valid vectors
        """

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
        """
        Evaluate the score of a single vector (five/four/three in a row, etc.)

        Args:
        vector(list): the vector to be evaluated
        player: "X"(human) or "O"(AI)

        Return:
        score(int): the score of the vector
        """

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
        """
        Evaluate the score of the whole board status.

        Return:
        int: the score difference between the AI and the opponent
        """

        vectors = self.get_vectors(board)
        ai_score = sum(self.evaluate_vector(v, 'O') for v in vectors)
        opponent_score = sum(self.evaluate_vector(v, 'X') for v in vectors)
        return ai_score - opponent_score


    def minimax(self, board, depth, is_maximizing, moves, alpha=-float('inf'), beta=float('inf')):
        """
        Minimax algorithm with alpha-beta puring. Search the best placement.

        Args:
        board: the board
        depth: the depthe of current search
        is_maximizing: maximized player (AI)
        moves: the list of candidate positions
        alpha: default is negative infinity
        beta: default is positive infinity

        Return:
        tuple: (the best score, the best position)
        """

        if board.check_win():
            if is_maximizing:
                return -9999999999, None
            else:
                return 9999999999, None    
        
        if depth == 0:
            score = self.evaluate_board(board)
            return score, None
        
        best_move = None
        
        if is_maximizing:#AI's turn
            max_score = float('-inf')
            for move in moves:
                x, y = move
                board.grid[x][y] = 'O'
                old_last_move = board.last_move
                board.last_move = (x, y)
                
                if board.check_win(): #Check if this step is a direct win
                    board.grid[x][y] = None
                    board.last_move = old_last_move
                    return float('inf'), move
            

                new_moves = moves.copy()
                new_moves.remove(move)
                self.update_candidate_moves(board, move, new_moves)
                
                score, _ = self.minimax(board, depth-1, False, new_moves, alpha, beta)

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

                if board.check_win(): #Check if this step is a direct win
                    board.grid[x][y] = None
                    board.last_move = old_last_move
                    return -float('inf'), move
                
                new_moves = moves.copy()
                new_moves.remove(move)
                self.update_candidate_moves(board, move, new_moves)
                
                score, _ = self.minimax(board, depth-1, True, new_moves, alpha, beta)

                board.grid[x][y] = None
                board.last_move = old_last_move
                
                if score < min_score:
                    min_score = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score, best_move