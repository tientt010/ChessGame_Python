# utils.py
from game.config import *
def is_in_check(board, color):
    """
    Kiểm tra nếu màu 'color' đang bị chiếu.
    """
    return board.is_check(color)

def is_in_checkmate(board, color):
    """
    Kiểm tra nếu màu 'color' đang bị chiếu hết.
    """
    return board.is_checkmate(color)

def is_stalemate(board, color):
    """
    Kiểm tra nếu trò chơi kết thúc hòa do không có nước đi hợp lệ nào.
    """
    if board.is_check(color):
        return False
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.get_piece((row, col))
            if piece and piece.get_color() == color:
                valid_moves = piece.get_valid_moves(board, (row, col))
                if valid_moves:
                    return False
    return True

def is_valid_position(pos):
    """
    Kiểm tra nếu vị trí (pos) nằm trong phạm vi bàn cờ.
    """
    row, col = pos
    return 0 <= row < ROWS and 0 <= col < COLS

def is_safe_move(board, piece, start_pos, end_pos):
    # Di chuyển tạm thời quân cờ
    original_piece = board.get_piece(end_pos)
    board.move_piece(start_pos, end_pos)
    
    # Kiểm tra nếu vua vẫn an toàn sau nước đi này
    king_color = piece.get_color()
    safe = not board.is_check(king_color)
    
    # Hoàn tác di chuyển
    board.move_piece(end_pos, start_pos)
    board.board[end_pos[0]][end_pos[1]].set_piece(original_piece)
    return safe
