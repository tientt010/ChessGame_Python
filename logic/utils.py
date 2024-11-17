# utils.py
from config import *
# from logic.pieces import Rook, King
# from logic.board import Board
def is_empty(board, position):
    return board.is_empty(position)

def is_under_attack(board, piece_color, target_pos) :
    for row in range(0,8):
        for col in range(0,8):
            piece=board.get_piece((row,col))
            if piece == None or piece.get_color() == piece_color:
                continue
            if piece.can_atack(board, (row,col), target_pos): 
                return True
    return False

def is_in_check(board, color):
    """
    Kiểm tra nếu màu 'color' đang bị chiếu.
    """
    return is_under_attack(board, color, board.find_king(color))


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
    if board.is_king(piece) and abs(end_pos[1]-start_pos[1])>1:
        return True
    # Di chuyển tạm thời quân cờ
    original_piece = board.get_piece(end_pos)
    board.move_piece(start_pos, end_pos,True)
    
    # Kiểm tra nếu vua vẫn an toàn sau nước đi này
    king_color = piece.get_color()
    safe = not board.is_check(king_color)
    
    # Hoàn tác di chuyển
    board.move_piece(end_pos, start_pos,True)
    board.board[end_pos[0]][end_pos[1]].set_piece(original_piece)
    return safe

def can_left_castle(board, pos, piece_color, has_move):
    if has_move or is_under_attack(board,piece_color, pos):
        return False
    initial_row= (7 if piece_color == 'w' else 0)
    piece = board.get_piece((initial_row,0))
    if not board.is_rook(piece) or piece_color != piece.get_color():
        return False
    if piece.has_move: return False
    for col in range(1, 4):
        if not is_empty(board,(initial_row,col)) or is_under_attack(board,piece_color,(initial_row,col)):
            return False
    return True

def can_right_castle(board, pos, piece_color, has_move):
    if has_move or is_under_attack(board,piece_color,pos):
        return False
    initial_row= (7 if piece_color == 'w' else 0)
    piece = board.get_piece((initial_row,7))
    if not board.is_rook(piece) or piece_color != piece.get_color():
        return False
    if piece.has_move: return False
    for col in range(5, 7):
        if not is_empty(board,(initial_row,col)) or is_under_attack(board,piece_color,(initial_row,col)) :
            return False
    return True



