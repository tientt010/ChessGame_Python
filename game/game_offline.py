from game.board import Board
from game.graphics import Graphics
import pygame
from game.config import *
import threading

class Game_offline:
    def __init__(self):
        self.board = Board()
        self.graphics = Graphics(self.board)
        self.selected_square = None
        self.valid_moves = []
        self.game_over = False
        self.time_white = 1200  # 20 phút (1200 giây)
        self.time_black = 1200
        self.turn_start_time = pygame.time.get_ticks()

    def play_turn(self, start_pos, end_pos):
        if end_pos in self.valid_moves:
            self.board.move_piece(start_pos, end_pos)
            self.valid_moves = []
            self.switch_turn()
            self.graphics.draw_initial_board()  # Vẽ lại bàn cờ ngay sau nước đi
            if self.board.is_checkmate(self.board.current_turn):
                self.game_over = True
                print(f"{'White player' if self.board.current_turn == 'b' else 'Black player'} wins!")
                self.graphics.running = False
                return True
        return False


    def switch_turn(self):
        self.turn_start_time = pygame.time.get_ticks()
        self.board.current_turn = 'b' if self.board.current_turn == 'w' else 'w'

    def update_timer(self):
        while not self.game_over:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.turn_start_time) // 1000
            if self.board.current_turn == 'w':
                self.time_white -= elapsed_time
                if self.time_white <= 0:
                    self.time_white = 0
                    self.game_over = True
            else:
                self.time_black -= elapsed_time
                if self.time_black <= 0:
                    self.time_black = 0
                    self.game_over = True
            self.turn_start_time = current_time
            pygame.time.wait(1000)

    def start(self):
        clock = pygame.time.Clock()
        running = True

        timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        timer_thread.start()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_square = self.graphics.get_square_under_mouse(mouse_pos)

                    if clicked_square:
                        if self.selected_square:
                            # Xóa highlight của quân cờ trước đó bằng cách vẽ lại bàn cờ
                            self.graphics.draw_initial_board()

                            # Nếu đã chọn quân cờ, cố gắng di chuyển
                            if clicked_square in self.valid_moves:
                                if self.play_turn(self.selected_square, clicked_square):
                                    running = False
                                    self.game_over = True
                                self.selected_square = None
                            else:
                                # Nếu nhấp vào ô không hợp lệ, chọn lại quân cờ mới
                                self.select_piece(clicked_square)
                        else:
                            # Chọn quân cờ ban đầu
                            self.select_piece(clicked_square)

                        # Highlight quân cờ và các ô hợp lệ
                        if self.selected_square:
                            self.graphics.highlight_square(self.selected_square, 'piece')
                        for move in self.valid_moves:
                            self.graphics.highlight_square(move, 'move')
                        pygame.display.flip()

            self.graphics.draw_timer_box()
            self.graphics.draw_timers(self.time_white, self.time_black)
            pygame.display.update(800, 0, 200, 800)
            clock.tick(FPS)
        pygame.quit()

    def select_piece(self, position):
        piece = self.board.get_piece(position)
        if piece and piece.get_color() == self.board.current_turn:
            self.selected_square = position
            self.valid_moves = piece.get_safe_moves(self.board, position)
        else:
            self.selected_square = None
            self.valid_moves = []
