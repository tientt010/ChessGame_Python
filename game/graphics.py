import pygame
from game.config import *

pygame.init()

class Graphics:
    def __init__(self, board):
        self.board = board
        self.window = pygame.display.set_mode((WIDTH + 200, HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption("Chess Game")
        self.load_images()
        self.clock = pygame.time.Clock()
        # Sử dụng phông chữ có sẵn "Comic Sans MS" hoặc "Arial Rounded MT Bold"
        self.font = pygame.font.SysFont(None, 24)  # Chọn font sinh động
        self.running = True
        self.draw_initial_board()

    def load_images(self):
        self.images = {}
        pieces = ['wP', 'bP', 'wR', 'bR', 'wN', 'bN', 'wB', 'bB', 'wQ', 'bQ', 'wK', 'bK']
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(
                pygame.image.load(IMAGE_PATH + piece + ".png"),
                (SQUARE_SIZE, SQUARE_SIZE)
            )

    def draw_board(self):
        colors = [LIGHT_BROWN, DARK_BROWN]
        for row in range(ROWS):
            for col in range(COLS):
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece((row, col))
                if piece:
                    color = 'w' if piece.get_color() == 'w' else 'b'
                    piece_name = color + piece.__class__.__name__[0]
                    if piece.__class__.__name__ == "Knight":
                        piece_name = color + 'N'
                    self.window.blit(self.images[piece_name], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def draw_initial_board(self):
        self.draw_board()
        self.draw_pieces()
        #self.draw_timer_box()
        pygame.display.flip()

    def draw_timer_box(self):
        pygame.draw.rect(self.window, (169, 169, 169), (800, 0, 200, 800))

    def draw_timers(self, time_white, time_black):
        # Tạo text căn giữa
        white_time_text = self.font.render(f"White: {time_white // 60:02}:{time_white % 60:02}", True, (255, 255, 255))
        black_time_text = self.font.render(f"Black: {time_black // 60:02}:{time_black % 60:02}", True, (255, 255, 255))

        white_text_rect = white_time_text.get_rect(center=(900, 600))  # Căn giữa tại tọa độ
        black_text_rect = black_time_text.get_rect(center=(900, 100))

        self.window.blit(white_time_text, white_text_rect)
        self.window.blit(black_time_text, black_text_rect)
        pygame.display.update(800, 0, 200, 800)

    def highlight_square(self, position, highlight_type='piece'):
        if position:
            row, col = position
            if highlight_type == 'piece':
                pygame.draw.rect(self.window, HIGHLIGHT_COLOR,
                                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
            elif highlight_type == 'move':
                pygame.draw.circle(self.window, MOVE_HIGHLIGHT_COLOR,
                                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                SQUARE_SIZE // 4)
            pygame.display.flip()

    def get_square_under_mouse(self, mouse_pos):
        x, y = mouse_pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        if col >= COLS or row >= ROWS:  # Kiểm tra ngoài phạm vi
            return None
        return row, col
