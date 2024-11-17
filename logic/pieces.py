# pieces.py
from logic.utils import*
class Piece:
    def __init__(self, color):
        self.color = color  # Màu của quân cờ: 'w' (trắng) hoặc 'b' (đen)

    def get_color(self):
        return self.color
    
    def get_type(self):
        return self.__class__.__name__.lower() # trả về tên lớp, ví dụ 'pawn', 'king'

    def get_valid_moves(self, board, position):
        """
        Trả về danh sách các nước đi hợp lệ cho quân cờ này.
        - Phương thức này cần được ghi đè trong các lớp con.
        """
        raise NotImplementedError("Phương thức này cần được ghi đè trong lớp con.")
    def get_safe_moves(self,board,position):
        return [move for move in self.get_valid_moves(board,position) if is_safe_move(board,self,position,move)]
    
    def can_atack(self,board, position, target_pos):
        return target_pos in self.get_valid_moves(board, position) 
       

class Pawn(Piece):
    def init(self, color):
        super().__init__(color)

    def get_type(self):
        return 'P'
    def get_valid_moves(self, board, position):
        moves = []
        row, col = position
        direction = -1 if self.color == 'w' else 1  # Tốt trắng đi lên (-1), tốt đen đi xuống (+1)

        # Di chuyển một ô phía trước
        if board.is_empty((row + direction, col)):
            moves.append((row + direction, col))

            # Di chuyển hai ô nếu quân cờ đang ở vị trí ban đầu
            start_row = 6 if self.color == 'w' else 1
            if row == start_row and board.is_empty((row + 2 * direction, col)):
                moves.append((row + 2 * direction, col))

        # Bắt quân theo đường chéo
        for offset in [-1, 1]:
            next_col = col + offset
            if board.is_within_bounds((row + direction, next_col)) and not board.is_empty((row + direction, next_col)):
                piece = board.get_piece((row + direction, next_col))
                if piece.get_color() != self.color :
                    moves.append((row + direction, next_col))

        return moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_move = False

    def get_type(self):
        return 'R'

    def get_valid_moves(self, board, position):
        moves = []
        row, col = position

        # Duyệt các hướng ngang và dọc
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r, c = row + direction[0], col + direction[1]
            while board.is_within_bounds((r, c)):
                if board.is_empty((r, c)) : 
                    moves.append((r, c))
                elif board.get_piece((r, c)).get_color() != self.color:
                    moves.append((r, c))
                    break 
                else :
                    break
                r += direction[0]
                c += direction[1]

        return moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_type(self):
        return 'K'  # Quân Mã
    
    def get_valid_moves(self, board, position):
        moves = []
        row, col = position
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for move in knight_moves:
            r, c = row + move[0], col + move[1]
            if board.is_within_bounds((r, c)):
                if (board.is_empty((r, c)) or board.get_piece((r, c)).get_color() != self.color) :
                    moves.append((r, c))

        return moves


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_type(self):
        return 'B'  # Quân Mã
    
    def get_valid_moves(self, board, position):
        moves = []
        row, col = position

        # Duyệt các hướng chéo
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + direction[0], col + direction[1]
            while board.is_within_bounds((r, c)):
                if board.is_empty((r, c)) : 
                    moves.append((r, c))
                elif board.get_piece((r, c)).get_color() != self.color:
                    moves.append((r, c))
                    break                    
                else:
                    break
                r += direction[0]
                c += direction[1]

        return moves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_type(self):
        return 'Q'  # Quân Mã

    def get_valid_moves(self, board, position):
        # Hậu có thể di chuyển như cả Tượng và Xe
        moves = Rook(self.color).get_valid_moves(board, position) + Bishop(self.color).get_valid_moves(board, position)
        return moves


class King(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_type(self):
        return 'K'  # Quân Mã
    
    def __init__(self, color):
        super().__init__(color)
        self.has_move = False
    def get_valid_moves(self, board, position):
        moves = []
        row, col = position
        king_moves = [
            (1, 0), (1, 1), (1, -1), (0, 1),
            (0, -1), (-1, 0), (-1, 1), (-1, -1)
        ]

        for move in king_moves:
            r, c = row + move[0], col + move[1]
            if board.is_within_bounds((r, c)):
                if (board.is_empty((r, c)) or board.get_piece((r, c)).get_color() != self.color) :
                    moves.append((r, c))
        return moves
    
    def get_safe_moves(self, board, position):
        castle_moves = []

        if can_left_castle(board, position, self.color,self.has_move):
            castle_moves.append((position[0], 2))
        if can_right_castle(board, position, self.color,self.has_move):
            castle_moves.append((position[0], 6))
        return super().get_safe_moves(board, position)+castle_moves 
    