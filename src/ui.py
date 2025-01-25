import pygame
from app import GomokuGame

class GomokuUI:
    def __init__(self):
        pygame.init()
        self.WINDOW_SIZE = 800
        self.BOARD_SIZE = 20
        self.CELL_SIZE = self.WINDOW_SIZE // (self.BOARD_SIZE + 2)
        self.GRID_SIZE = self.CELL_SIZE * self.BOARD_SIZE
        
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Gomoku")
        
        self.game = GomokuGame(board_size=self.BOARD_SIZE)
        self.game.start()
        
        self.BOARD_COLOR = (222, 184, 135)
        self.LINE_COLOR = (0, 0, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
    def draw_board(self):
        self.screen.fill(self.BOARD_COLOR)
        
        # Draw grid lines
        offset = self.CELL_SIZE
        for i in range(self.BOARD_SIZE):
            start_pos = (offset + i * self.CELL_SIZE, offset)
            end_pos = (offset + i * self.CELL_SIZE, offset + self.GRID_SIZE - self.CELL_SIZE)
            pygame.draw.line(self.screen, self.LINE_COLOR, start_pos, end_pos)
            
            start_pos = (offset, offset + i * self.CELL_SIZE)
            end_pos = (offset + self.GRID_SIZE - self.CELL_SIZE, offset + i * self.CELL_SIZE)
            pygame.draw.line(self.screen, self.LINE_COLOR, start_pos, end_pos)
    
    def draw_pieces(self):
        offset = self.CELL_SIZE
        radius = self.CELL_SIZE // 2 - 2
        
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                piece = self.game.board.grid[x][y]
                if piece:
                    center = (offset + x * self.CELL_SIZE, offset + y * self.CELL_SIZE)
                    color = self.BLACK if piece == 'X' else self.WHITE
                    pygame.draw.circle(self.screen, color, center, radius)
                    if piece == 'O':  # Draw border for white pieces
                        pygame.draw.circle(self.screen, self.BLACK, center, radius, 1)
    
    def get_grid_position(self, mouse_pos):
        x, y = mouse_pos
        offset = self.CELL_SIZE
        grid_x = round((x - offset) / self.CELL_SIZE)
        grid_y = round((y - offset) / self.CELL_SIZE)
        return grid_x, grid_y
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = self.get_grid_position(event.pos)
                    if 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE:
                        result = self.game.play_turn(x, y)
                        if result:
                            print(f"Player {result} wins!")
                            running = False
            
            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    ui = GomokuUI()
    ui.run()