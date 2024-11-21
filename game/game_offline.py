from logic.board import Board
from graphics import Graphics
import pygame
from config import *
import threading

class Game_offline:
    
    # Khởi tạo trò chơi với các thành phần cơ bản và trạng thái ban đầu.
    def __init__(self):
        self.board = Board()  # Bàn cờ
        self.graphics = Graphics(self.board, "Two Player Mode")  # Giao diện đồ họa
        self.selected_square = None  # Vị trí ô được chọn
        self.valid_moves = []  # Danh sách nước đi hợp lệ
        self.game_end = False  # Trạng thái kết thúc game
        self.time_white = 1200  # Thời gian cho người chơi trắng (20 phút)
        self.time_black = 1200  # Thời gian cho người chơi đen (20 phút)
        self.turn_start_time = pygame.time.get_ticks()  # Thời gian bắt đầu lượt đi hiện tại
        self.highlight_king = None  # Highlight vua nếu bị chiếu
        self.move_sound = pygame.mixer.Sound("sounds/move.wav")  # Âm thanh di chuyển
        self.select_sound = pygame.mixer.Sound("sounds/capture.wav")  # Âm thanh chọn quân
        self.is_capture = False  # Trạng thái có quân bị ăn
        self.option_endgame = -1  # Lựa chọn kết thúc game

    # Vòng lặp chính để xử lý trò chơi
    def start(self):
        clock = pygame.time.Clock()
        running = True
        self.graphics.draw_initial_board()  # Vẽ bàn cờ ban đầu
        timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        timer_thread.start()  # Khởi động luồng đồng hồ đếm ngược

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Thoát trò chơi
                    running = False
                    self.game_end = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Xử lý click chuột
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_square = self.graphics.get_square_under_mouse(mouse_pos)

                    if clicked_square:
                        if self.selected_square:
                            # Nếu đã chọn quân cờ, kiểm tra di chuyển hoặc chọn lại
                            self.graphics.draw_update(self.is_capture, self.board.current_turn, self.highlight_king)
                            if clicked_square in self.valid_moves:
                                if self.play_turn(self.selected_square, clicked_square):
                                    running = False  # Trò chơi kết thúc
                                    self.game_end = True
                                self.selected_square = None
                            else:
                                self.select_piece(clicked_square)
                        else:
                            # Chọn quân cờ ban đầu
                            self.select_piece(clicked_square)

                        # Highlight quân cờ và các ô hợp lệ
                        if self.selected_square:
                            self.graphics.highlight_square(self.selected_square, 'piece')
                        for move in self.valid_moves:
                            self.graphics.highlight_square(move, 'move')

                        pygame.display.update(0, 0, WIDTH, HEIGHT)

            self.graphics.draw_timers(self.time_white, self.time_black)  # Hiển thị thời gian còn lại
            pygame.display.update(800, 0, 200, 800)
            clock.tick(FPS)

        return self.option_endgame
    
    # Chọn quân cờ tại vị trí được click và tính toán nước đi hợp lệ
    def select_piece(self, position):
        piece = self.board.get_piece(position)
        if piece and piece.get_color() == self.board.current_turn:
            self.selected_square = position
            self.valid_moves = piece.get_safe_moves(self.board, position)
            self.select_sound.play()
        else:
            self.selected_square = None
            self.valid_moves = []

    # Xử lý một lượt đi, bao gồm cập nhật bàn cờ và kiểm tra kết thúc trò chơi.
    def play_turn(self, start_pos, end_pos):
        captured_piece = self.board.get_piece(end_pos)  # Kiểm tra quân bị ăn
        self.is_capture = bool(captured_piece)
        self.board.move_piece(start_pos, end_pos)  # Di chuyển quân cờ(logic)
        self.move_sound.play()
        self.valid_moves = []
        self.switch_turn()  # Chuyển lượt
        self.highlight_king = self.board.find_king() if self.board.is_check() else None
        self.graphics.draw_update(self.is_capture, self.board.current_turn, self.highlight_king)
        self.is_capture = False
        # Kiểm tra trạng thái chiếu hết hoặc hòa
        check_mate = self.board.is_checkmate(self.board.current_turn)
        if check_mate != 'ongoing':
            self.end_game("win" if check_mate == "win" else "draw")
            return True
        return False

    # Chuyển lượt chơi giữa trắng và đen.
    def switch_turn(self):
        self.turn_start_time = pygame.time.get_ticks()
        self.board.current_turn = 'b' if self.board.current_turn == 'w' else 'w'

    # Cập nhật đồng hồ đếm ngược cho mỗi bên.
    def update_timer(self):
        while not self.game_end:
            self.graphics.draw_timers(self.time_white, self.time_black)
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.turn_start_time) // 1000

            if self.board.current_turn == 'w':
                self.time_white -= elapsed_time
                if self.time_white <= 0:
                    self.time_white = 0
                    self.game_end = True
                    self.end_game('win')
            else:
                self.time_black -= elapsed_time
                if self.time_black <= 0:
                    self.time_black = 0
                    self.game_end = True
                    self.end_game('win')

            self.turn_start_time = current_time
            pygame.time.wait(1000)

    # Kết thúc trò chơi và hiển thị kết quả.
    def end_game(self, result):
        if result == "win":
            message = 'White player win!' if self.board.current_turn == 'b' else 'Black player win!'
        elif result == "draw":
            message = "Draw!"
        else:
            message = "Unknown result"

        self.graphics.running = False
        self.game_end = True
        self.option_endgame = self.graphics.show_result(result, message, WHITE if self.board.current_turn == 'b' else BLACK)
