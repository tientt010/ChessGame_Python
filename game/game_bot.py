from logic.board import Board
from graphics import Graphics
import pygame
from config import *
from logic.stockfish import StockfishEngine
import threading

class Game_bot:
    def __init__(self):
        self.board = Board()
        self.graphics = Graphics(self.board)
        self.selected_square = None
        self.valid_moves = []
        self.game_end = False
        self.time_white = 1200  # 20 phút (1200 giây)
        self.time_black = 1200
        self.turn_start_time = pygame.time.get_ticks()
        # Âm thanh trò chơi
        self.move_sound = pygame.mixer.Sound("sounds/move.wav")
        self.select_sound = pygame.mixer.Sound("sounds/capture.wav")
        self.stockfish = StockfishEngine()
    
    # Thêm mới sư kiện end_game
    def end_game(self, result):
        if result == "win":
            message = 'Player win!' if self.board.current_turn == 'b' else 'Player Lose!'
        elif result == "draw":
            message = "Draw!"
        else:
            message = "Unknown result"
        
        self.graphics.show_message(message)
        self.graphics.running = False
        self.game_end = True
        self.stockfish.stop()

    def play_turn(self, current_turn, start_pos=None, end_pos=None):
        if current_turn == 'bot':
            self.stockfish.set_position(self.board.move_list)
            turn_bot = self.stockfish.get_best_move()
            start_pos = (8 - int(turn_bot[1]), ord(turn_bot[0]) - ord('a'))
            end_pos = (8 - int(turn_bot[3]), ord(turn_bot[2]) - ord('a'))
        
        if current_turn == 'bot' or end_pos in self.valid_moves:
            self.board.move_piece(start_pos, end_pos)
            self.move_sound.play()
            self.valid_moves = []
            self.switch_turn()
            self.graphics.draw_initial_board()
            check_mate = self.board.is_checkmate(self.board.current_turn)
            if check_mate!= 'ongoing':
                if check_mate == "win":
                    self.end_game("win")
                else:
                    self.end_game("draw")
                return True
            if current_turn == 'player':
                self.play_turn('bot')
        return False


    def switch_turn(self):
        self.turn_start_time = pygame.time.get_ticks()
        self.board.current_turn = 'b' if self.board.current_turn == 'w' else 'w'

    def update_timer(self):
        while not self.game_end:
            pygame.time.wait(1000)
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.turn_start_time) // 1000
            if self.board.current_turn == 'w':
                self.time_white = max(0, self.time_white - elapsed_time)
            else:
                self.time_black = max(0, self.time_black - elapsed_time)
            self.turn_start_time = current_time
            if self.time_white == 0 or self.time_black == 0:
                self.game_end = True

    def start(self):
        clock = pygame.time.Clock()
        running = True
        timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        timer_thread.start()

        if not self.stockfish.start():
            print("Error: Failed to start Stockfish.")
            return

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.game_end = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_square = self.graphics.get_square_under_mouse(mouse_pos)

                    if clicked_square:
                        if self.selected_square:
                            # Xóa highlight của quân cờ trước đó bằng cách vẽ lại bàn cờ
                            self.graphics.draw_initial_board()

                            # Nếu đã chọn quân cờ, cố gắng di chuyển
                            if clicked_square in self.valid_moves:
                                if self.play_turn('player', self.selected_square, clicked_square):
                                    running = False
                                    self.game_end = True
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
            self.select_sound.play()
        else:
            self.selected_square = None
            self.valid_moves = []
if __name__ == "__main__":
    try:
        game = Game_bot()
        game.start()
    except Exception as e:
        print(f"Error: {e}")

