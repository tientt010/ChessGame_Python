from config import *
from logic.pieces import Pawn, Rook, Knight, Bishop, Queen, King
import inspect


# Class đại diện cho từng ô trên bàn cờ
class Box:
    def __init__(self, piece=None):
        self.piece = piece

    def set_piece(self, piece):
        self.piece = piece

    def get_piece(self):
        return self.piece

    def is_empty(self):
        return self.piece is None


# Class đại diện cho bàn cờ
class Board:
    # Contrustor
    def __init__(self):
        self.board = self.create_board()
        self.current_turn = 'w'
        self.move_list = []

    # Khởi tạo bàn cờ với các quân cờ ở vị trí ban đầu
    def create_board(self):
        board = [
            [Box(Rook("b")), Box(Knight("b")), Box(Bishop("b")), Box(Queen("b")), Box(King("b")), Box(Bishop("b")), Box(Knight("b")), Box(Rook("b"))],
            [Box(Pawn("b")) for _ in range(8)],
            [Box() for _ in range(8)],
            [Box() for _ in range(8)],
            [Box() for _ in range(8)],
            [Box() for _ in range(8)],
            [Box(Pawn("w")) for _ in range(8)],
            [Box(Rook("w")), Box(Knight("w")), Box(Bishop("w")), Box(Queen("w")), Box(King("w")), Box(Bishop("w")), Box(Knight("w")), Box(Rook("w"))]
        ]
        return board
    # Kiểm tra vị trí đã chọn có thuộc bàn cờ hay không?
    def is_within_bounds(self, position):
        row, col = position
        return 0 <= row < ROWS and 0 <= col < COLS
    
    # Trả về true nếu có quân cờ, ngược lại false
    def is_empty(self, position):
        row, col = position
        return self.board[row][col].is_empty()

    # Trả về quân cờ ở vị trí position
    def get_piece(self, position):
        row, col = position
        return self.board[row][col].get_piece()

    # Kiểm tra có phải xe hay vua không?
    def is_rook(self, piece):
        return isinstance(piece, Rook)

    def is_king(self, piece):
        return isinstance(piece, King)

    # Hàm chính di chuyển quân cờ (logic)
    def move_piece(self, start_pos, end_pos, fake_move=False, is_turn_bot=False):
        # Di chuyển quân cờ từ vị trí start_pos đến end_pos
        piece = self.get_piece(start_pos)
        self.board[end_pos[0]][end_pos[1]].set_piece(piece)
        self.board[start_pos[0]][start_pos[1]].set_piece(None)

        # Xử lý phép hoán thành
        if isinstance(piece, King) and abs(end_pos[1] - start_pos[1]) > 1:
            self.castle(start_pos, end_pos)

        # Xử lý trường hợp tốt phong hậu
        if isinstance(piece, Pawn) and end_pos[0] == (0 if piece.get_color() == 'w' else 7):
            self.board[end_pos[0]][end_pos[1]].set_piece(Queen(piece.get_color()))
            if inspect.currentframe().f_back.f_code.co_name == "is_safe_move":
                self.board[end_pos[0]][end_pos[1]].set_piece(Pawn(piece.get_color()))

        if fake_move:
            return

        if not is_turn_bot: self.move_list.append(self.move_to_string(start_pos, end_pos))
        if isinstance(piece, (King, Rook)):
            piece.has_move = True

    # Xử lý phép hoán thành
    def castle(self, start_pos, end_pos):
        if start_pos[1] == 4:
            rook_start_pos = (start_pos[0], 0 if end_pos[1] < start_pos[1] else 7)
            rook_end_pos = (start_pos[0], 3 if end_pos[1] < start_pos[1] else 5)
        else:
            rook_start_pos = (start_pos[0], 3 if end_pos[1] > start_pos[1] else 5)
            rook_end_pos = (start_pos[0], 0 if end_pos[1] > start_pos[1] else 7)
        self.move_piece(rook_start_pos, rook_end_pos, True)

    # Kiểm tra xem vua của bên color có đang bị chiếu không?
    def is_check(self, color=None):
        if color is None:
            color = self.current_turn
        # Kiểm tra nếu vua của màu 'color' đang bị chiếu
        king_pos = self.find_king(color)
        opponent_color = 'b' if color == 'w' else 'w'
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece((row, col))
                if piece and piece.get_color() == opponent_color:
                    if king_pos in piece.get_valid_moves(self, (row, col)):
                        return True
        return False

    # Kiểm tra trạng thái bàn cờ
    def is_checkmate(self, color=None):
        if color is None:
            color = self.current_turn
        # Kiểm tra nếu không còn nước đi nào hợp lệ
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece((row, col))
                if piece and piece.get_color() == color:
                    moves = piece.get_safe_moves(self, (row, col))
                    if len(moves) > 0:
                        return 'ongoing'
        if self.is_check(color):
            return "win"
        else:
            return "draw"

    # Tìm vị trí hiện tại của vua bên color
    def find_king(self, color=None):
        if color is None:
            color = self.current_turn
        # Tìm vị trí của quân Vua màu 'color'
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece((row, col))
                if isinstance(piece, King) and piece.get_color() == color:
                    return (row, col)
        return None

    # Chuyển nước đi về dạng chuẩn phục vụ cho game bot
    def move_to_string(self, start_pos, end_pos):
        # Chuyển nước đi thành chuỗi
        return chr(ord('a') + start_pos[1]) + str(8 - start_pos[0]) + chr(ord('a') + end_pos[1]) + str(8 - end_pos[0])

    def add_bot_move(self, move):
        self.move_list.append(move)