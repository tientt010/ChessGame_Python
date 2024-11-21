from logic.board import Board
from graphics import Graphics
import pygame
from config import *
from logic.stockfish import StockfishEngine

class Game_bot:
    # Khởi tạo trạng thái ban đầu cho game
    def __init__(self):
        self.board = Board()
        self.graphics = Graphics(self.board, "Single Player Mode")
        self.selected_square = None 
        self.valid_moves = [] 
        self.game_end = False 
        self.stockfish = StockfishEngine()  # Đối tượng Stockfish để chơi với bot
        self.move_sound = pygame.mixer.Sound("sounds/move.wav")  
        self.select_sound = pygame.mixer.Sound("sounds/capture.wav")  
        self.is_capture = False  
        self.option_endgame = -1 
        self.highlight_king = None 

    # Hàm chính, chạy vòng lặp game
    def start(self):
        clock = pygame.time.Clock()
        running = True

        # Kiểm tra khởi động Stockfish
        if not self.stockfish.start():  
            print("Error: Failed to start Stockfish.")
            return

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Người dùng đóng cửa sổ
                    running = False
                    self.game_end = True
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Người dùng nhấn chuột
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_square = self.graphics.get_square_under_mouse(mouse_pos)

                    if clicked_square:
                        if self.selected_square:  # Nếu ô cờ đã được chọn trước đó
                            self.graphics.draw_update(self.is_capture, self.board.current_turn, self.highlight_king)
                            self.is_capture = False
                            if clicked_square in self.valid_moves:  # Di chuyển hợp lệ
                                if self.play_turn('player', self.selected_square, clicked_square):
                                    running = False
                                    return self.option_endgame
                                self.selected_square = None
                            else:  # Chọn lại quân cờ
                                self.select_piece(clicked_square)
                        else:  # Chọn quân cờ ban đầu
                            self.select_piece(clicked_square)

                        # Highlight ô cờ và nước đi hợp lệ
                        if self.selected_square:
                            self.graphics.highlight_square(self.selected_square, 'piece')
                        for move in self.valid_moves:
                            self.graphics.highlight_square(move, 'move')
                        pygame.display.flip()

            pygame.display.update(800, 0, 200, 800)
            clock.tick(FPS)
        return self.option_endgame

    def select_piece(self, position):
        # Chọn quân cờ tại vị trí được nhấp chuột
        piece = self.board.get_piece(position)
        if piece and piece.get_color() == self.board.current_turn:
            self.selected_square = position
            self.valid_moves = piece.get_safe_moves(self.board, position)
            self.select_sound.play()
        else:
            self.selected_square = None
            self.valid_moves = []

    def play_turn(self, current_turn, start_pos=None, end_pos=None):
        # Thực hiện lượt đi của người chơi hoặc bot
        if current_turn == 'bot':  # Bot chọn nước đi
            self.stockfish.set_position(self.board.move_list)
            bot_move = self.stockfish.get_best_move()
            self.board.add_bot_move(bot_move)
            start_pos = (8 - int(bot_move[1]), ord(bot_move[0]) - ord('a'))
            end_pos = (8 - int(bot_move[3]), ord(bot_move[2]) - ord('a'))

        # Thực hiện di chuyển quân cờ
        if self.board.get_piece(end_pos):  # Kiểm tra nếu có quân cờ bị ăn
            self.is_capture = True
        self.board.move_piece(start_pos, end_pos, current_turn == 'bot')  # Di chuyển quân cờ
        self.move_sound.play()
        self.valid_moves = []
        self.switch_turn()  # Chuyển lượt
        self.highlight_king = self.board.find_king() if self.board.is_check() else None
        self.graphics.draw_update(self.is_capture, self.board.current_turn, self.highlight_king)
        if self.is_capture:
            self.graphics.draw_timer_box()
        self.is_capture = False
        check_mate = self.board.is_checkmate(self.board.current_turn)
        if check_mate != 'ongoing':  # Trò chơi kết thúc
            self.end_game("win" if check_mate == "win" else "draw")
            return True
        if current_turn == 'player' and self.graphics.running:  # Đến lượt của bot
            return self.play_turn('bot')

        return False

    # Chuyển lượt chơi
    def switch_turn(self):
        self.board.current_turn = 'b' if self.board.current_turn == 'w' else 'w'

    # Kết thúc trò chơi và hiển thị kết quả
    def end_game(self, result):
        if result == "win":
            message = 'Player win!' if self.board.current_turn == 'b' else 'Player Lose!'
            result = 'win_bot' if self.board.current_turn == 'b' else 'lose_bot'
        elif result == "draw":
            message = "Draw!"
        else:
            message = "Unknown result"

        self.option_endgame =0 if self.graphics.show_result(result, message) ==1 else 2
        self.graphics.running = False
        self.game_end = True
        self.stockfish.stop()