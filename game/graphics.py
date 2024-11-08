import pygame
from game.config import *

pygame.init()

class Graphics:
    def __init__(self, board):
        self.board = board
        self.window = pygame.display.set_mode((WIDTH + 200, HEIGHT), pygame.DOUBLEBUF | pygame.SRCALPHA)
        pygame.display.set_caption("Chess Game")
        self.load_images()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.running = True
        self.draw_initial_board()

    def load_images(self):
        self.images = {}
        pieces = ['wP', 'bP', 'wR', 'bR', 'wN', 'bN', 'wB', 'bB', 'wQ', 'bQ', 'wK', 'bK']
        for piece in pieces:
            # Tải hình ảnh và áp dụng convert_alpha() để hỗ trợ độ nét và trong suốt
            original_image = pygame.image.load(IMAGE_PATH + piece + ".png").convert_alpha()
            # Chỉnh kích thước để vừa với ô vuông trên bàn cờ
            self.images[piece] = pygame.transform.smoothscale(
                original_image, (SQUARE_SIZE, SQUARE_SIZE)
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
        black_rect = pygame.Rect(WIDTH, 0, 200, HEIGHT // 2)  # Nửa trên
        white_rect = pygame.Rect(WIDTH, HEIGHT // 2, 200, HEIGHT // 2)  # Nửa dưới
        pygame.draw.rect(self.window, (0, 0, 0), black_rect)
        pygame.draw.rect(self.window, (255, 255, 255), white_rect)
        pygame.display.flip()

    def draw_timer_box(self):
        
        white_timer_rect = pygame.Rect(WIDTH + 50, HEIGHT - 230, 100, 60)
        pygame.draw.rect(self.window, (255, 255, 255), white_timer_rect)  # Nền màu trắng
        #pygame.draw.rect(self.window, (255, 255, 255), white_timer_rect, 2)  # Viền màu trắng

        
        black_timer_rect = pygame.Rect(WIDTH + 50, 170, 100, 60)
        pygame.draw.rect(self.window, (0,0,0), black_timer_rect)
        #pygame.draw.rect(self.window, (255, 255, 255), black_timer_rect, 2)




    def draw_timers(self, time_white, time_black):
       
        # Phông chữ nhỏ hơn cho đồng hồ
        small_font = pygame.font.SysFont(None, 50)  # Đặt kích thước phông chữ nhỏ hơn cho phù hợp với ô đồng hồ

        # Tạo text thời gian cho quân trắng và đen
        white_time_text = small_font.render(f"{time_white // 60}:{time_white % 60:02}", True, (0, 0, 0))
        black_time_text = small_font.render(f"{time_black // 60}:{time_black % 60:02}", True, (255, 255, 255))

        # Đặt vị trí text thời gian để căn giữa trong các ô đồng hồ
        white_text_rect = white_time_text.get_rect(center=(WIDTH + 100, HEIGHT - 200))  
        black_text_rect = black_time_text.get_rect(center=(WIDTH + 100, 200))            

        # Vẽ text lên cửa sổ
        self.window.blit(white_time_text, white_text_rect)
        self.window.blit(black_time_text, black_text_rect)

        # Cập nhật phần hiển thị của các ô đồng hồ
        pygame.display.update(WIDTH, 0, 200, HEIGHT)


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
