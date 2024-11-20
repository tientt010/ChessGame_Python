from logic.utils import *


# Lớp cha đại diện cho một quân cờ chung
class Piece:
    def __init__(self, color):
        self.color = color                     # 'w' là quân trắng, 'b' là quân đen

    # Trả về màu của quân cờ
    def get_color(self):
        return self.color
    
    # Trả về danh sách các nước đi hợp lệ 
    def get_valid_moves(self, board, position):
        raise NotImplementedError("Phương thức này cần được ghi đè trong lớp con.")

    # Trả về danh sách các nước đi an toàn(vua không bị chiếu)
    def get_safe_moves(self, board, position):
        return [move for move in self.get_valid_moves(board, position) if is_safe_move(board, self, position, move)]

    # Kiểm tra xem quân cờ có thể tấn công vị trí target_pos hay không.
    def can_attack(self, board, position, target_pos):
        return target_pos in self.get_valid_moves(board, position)


# Quân Tốt
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)

    # Nước đi hợp lẹ của tốt
    def get_valid_moves(self, board, position):
        moves = []
        row, col = position
        direction = -1 if self.color == 'w' else 1  # Trắng đi lên (-1), đen đi xuống (+1)

        # Di chuyển một ô phía trước
        if board.is_empty((row + direction, col)):
            moves.append((row + direction, col))

            # Di chuyển hai ô nếu đang ở vị trí ban đầu
            start_row = 6 if self.color == 'w' else 1
            if row == start_row and board.is_empty((row + 2 * direction, col)):
                moves.append((row + 2 * direction, col))

        # Bắt quân theo đường chéo
        for offset in [-1, 1]:
            next_col = col + offset
            if board.is_within_bounds((row + direction, next_col)) and not board.is_empty((row + direction, next_col)):
                piece = board.get_piece((row + direction, next_col))
                if piece.get_color() != self.color:
                    moves.append((row + direction, next_col))

        return moves


# Quân Xe
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_move = False

    # Nước đi hợp lệ của xe
    def get_valid_moves(self, board, position):
        moves = []
        row, col = position

        # Duyệt các hướng ngang và dọc
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r, c = row + direction[0], col + direction[1]
            while board.is_within_bounds((r, c)):
                if board.is_empty((r, c)):
                    moves.append((r, c))
                elif board.get_piece((r, c)).get_color() != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += direction[0]
                c += direction[1]

        return moves


# Quân Mã
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    # Nước đi của mã
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
                if board.is_empty((r, c)) or board.get_piece((r, c)).get_color() != self.color:
                    moves.append((r, c))

        return moves


# Quân Tượng
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    # Danh sách các nước đi hợp lệ của tượng
    def get_valid_moves(self, board, position):
        moves = []
        row, col = position

        # Duyệt các hướng chéo
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + direction[0], col + direction[1]
            while board.is_within_bounds((r, c)):
                if board.is_empty((r, c)):
                    moves.append((r, c))
                elif board.get_piece((r, c)).get_color() != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += direction[0]
                c += direction[1]

        return moves


# Quân Hậu
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

    # Nước đi hợp lệ của hậu
    def get_valid_moves(self, board, position):
        # Quân hậu có thể di chuyển như xe và tượng
        moves = Rook(self.color).get_valid_moves(board, position) + Bishop(self.color).get_valid_moves(board, position)
        return moves


# Quân Vua
class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_move = False

    # Nước đi hợp lệ của vua
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
                if board.is_empty((r, c)) or board.get_piece((r, c)).get_color() != self.color:
                    moves.append((r, c))

        return moves

    # Trả về danh sách các nước đi an toàn bao gồm cả hoán thành
    def get_safe_moves(self, board, position):
        castle_moves = []

        if can_left_castle(board, position, self.color, self.has_move):
            castle_moves.append((position[0], 2))
        if can_right_castle(board, position, self.color, self.has_move):
            castle_moves.append((position[0], 6))

        return super().get_safe_moves(board, position) + castle_moves
