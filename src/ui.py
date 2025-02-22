import pygame
from app import GomokuGame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            self.current_color = self.hover_color if self.is_hovered else self.color
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class GomokuUI:
    def __init__(self):
        pygame.init()
        self.WINDOW_SIZE = 800
        self.BOARD_SIZE = 20
        self.CELL_SIZE = self.WINDOW_SIZE // (self.BOARD_SIZE + 2)
        self.GRID_SIZE = self.CELL_SIZE * self.BOARD_SIZE
        
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("SmartGO5")
        
        self.BOARD_COLOR = (222, 184, 135)
        self.LINE_COLOR = (0, 0, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BUTTON_COLOR = (200, 150, 100)
        self.BUTTON_HOVER_COLOR = (180, 130, 80)
        
        self.state = "START" 
        self.create_buttons()
        
    def create_buttons(self):
        self.start_button = Button(
            self.WINDOW_SIZE//2 - 100,
            self.WINDOW_SIZE//2,
            200, 50,
            "Game Start",
            self.BUTTON_COLOR,
            self.BUTTON_HOVER_COLOR
        )
        
        self.play_again_button = Button(
            self.WINDOW_SIZE//2 - 220,
            self.WINDOW_SIZE//2,
            200, 50,
            "Play Again",
            self.BUTTON_COLOR,
            self.BUTTON_HOVER_COLOR
        )
        
        self.exit_button = Button(
            self.WINDOW_SIZE//2 + 20,
            self.WINDOW_SIZE//2,
            200, 50,
            "Exit",
            self.BUTTON_COLOR,
            self.BUTTON_HOVER_COLOR
        )
        
    def start_new_game(self):
        self.game = GomokuGame(board_size=self.BOARD_SIZE)
        self.game.start()
        self.state = "GAME"
        
    def draw_start_screen(self):
        self.screen.fill(self.BOARD_COLOR)
        font = pygame.font.Font(None, 74)
        title = font.render("SmartGO5", True, self.BLACK)
        title_rect = title.get_rect(center=(self.WINDOW_SIZE//2, self.WINDOW_SIZE//3))
        self.screen.blit(title, title_rect)
        self.start_button.draw(self.screen)
        
    def draw_end_screen(self, winner):
        self.screen.fill(self.BOARD_COLOR)
        font = pygame.font.Font(None, 74)
        if winner == 'X':
            text = "You Win!"
        else:
            text = "AI Wins!"
        winner_text = font.render(text, True, self.BLACK)
        text_rect = winner_text.get_rect(center=(self.WINDOW_SIZE//2, self.WINDOW_SIZE//3))
        self.screen.blit(winner_text, text_rect)
        self.play_again_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        
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
            
        # Draw coordinates
        font = pygame.font.Font(None, 24)
        for i in range(self.BOARD_SIZE):
            text = font.render(str(i), True, self.LINE_COLOR)
            self.screen.blit(text, (offset + i * self.CELL_SIZE - text.get_width()//2, offset//2))
            self.screen.blit(text, (offset + i * self.CELL_SIZE - text.get_width()//2, 
                           offset + self.GRID_SIZE - self.CELL_SIZE + offset//2))
            self.screen.blit(text, (offset//2 - text.get_width()//2, 
                           offset + i * self.CELL_SIZE - text.get_height()//2))
            self.screen.blit(text, (offset + self.GRID_SIZE - self.CELL_SIZE + offset//2 - text.get_width()//2,
                           offset + i * self.CELL_SIZE - text.get_height()//2))

    def draw_pieces(self):
        offset = self.CELL_SIZE
        radius = self.CELL_SIZE // 2 - 2
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.game.board.grid[col][row]
                if piece:
                    center = (offset + col * self.CELL_SIZE, offset + row * self.CELL_SIZE)
                    color = self.BLACK if piece == 'X' else self.WHITE
                    pygame.draw.circle(self.screen, color, center, radius)
                    if piece == 'O':  # Draw border for white pieces
                        pygame.draw.circle(self.screen, self.BLACK, center, radius, 1)
    
    def get_grid_position(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        offset = self.CELL_SIZE
        col = round((mouse_x - offset) / self.CELL_SIZE)
        row = round((mouse_y - offset) / self.CELL_SIZE)
        return col, row
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if self.state == "START":
                    if self.start_button.handle_event(event):
                        self.start_new_game()
                        
                elif self.state == "GAME":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = self.get_grid_position(event.pos)
                        if 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE:
                            result = self.game.play_turn(x, y)
                            if result:
                                print(f"Player {result} wins!")
                                self.state = "END"
                                self.winner = result
                                
                elif self.state == "END":
                    if self.play_again_button.handle_event(event):
                        self.start_new_game()
                    elif self.exit_button.handle_event(event):
                        running = False
            
            if self.state == "START":
                self.draw_start_screen()
            elif self.state == "GAME":
                self.draw_board()
                self.draw_pieces()
            elif self.state == "END":
                self.draw_end_screen(self.winner)
                
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    ui = GomokuUI()
    ui.run()