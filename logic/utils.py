from config import *

# Kiểm tra nếu vị trí 'target_pos' bị quân đối phương tấn công
def is_under_attack(board, piece_color, target_pos):
    for row in range(8):
        for col in range(8):
            piece = board.get_piece((row, col))
            if piece is None or piece.get_color() == piece_color:
                continue
            if piece.can_attack(board, (row, col), target_pos): 
                return True
    return False

# Kiểm tra nếu một nước đi là an toàn cho quân vua
def is_safe_move(board, piece, start_pos, end_pos):
    if board.is_king(piece) and abs(end_pos[1] - start_pos[1]) > 1:
        return True  # Đảm bảo tính hợp lệ cho nhập thành

    # Di chuyển tạm thời quân cờ
    original_piece = board.get_piece(end_pos)
    board.move_piece(start_pos, end_pos, True)

    # Kiểm tra xem vua có an toàn sau nước đi này không
    king_color = piece.get_color()
    safe = not board.is_check(king_color)

    # Hoàn tác di chuyển
    board.move_piece(end_pos, start_pos, True)
    board.board[end_pos[0]][end_pos[1]].set_piece(original_piece)
    return safe

# Kiểm tra nếu nhập thành bên trái được phép
def can_left_castle(board, pos, piece_color, has_move):
    if has_move or is_under_attack(board, piece_color, pos):
        return False  # Không nhập thành nếu vua đã di chuyển hoặc bị chiếu
    initial_row = 7 if piece_color == 'w' else 0
    piece = board.get_piece((initial_row, 0))
    if not board.is_rook(piece) or piece_color != piece.get_color():
        return False  # Quân Xe bên trái không hợp lệ
    if piece.has_move:
        return False  # Quân Xe đã di chuyển
    for col in range(1, 4):  # Kiểm tra các ô giữa vua và Xe
        if not board.is_empty((initial_row, col)) or is_under_attack(board, piece_color, (initial_row, col)):
            return False
    return True
# Kiểm tra nếu nhập thành bên phải được phép
def can_right_castle(board, pos, piece_color, has_move):
    if has_move or is_under_attack(board, piece_color, pos):
        return False  # Không nhập thành nếu vua đã di chuyển hoặc bị chiếu
    initial_row = 7 if piece_color == 'w' else 0
    piece = board.get_piece((initial_row, 7))
    if not board.is_rook(piece) or piece_color != piece.get_color():
        return False  # Quân Xe bên phải không hợp lệ
    if piece.has_move:
        return False  # Quân Xe đã di chuyển
    for col in range(5, 7):  # Kiểm tra các ô giữa vua và Xe
        if not board.is_empty((initial_row, col)) or is_under_attack(board, piece_color, (initial_row, col)):
            return False
    return True
