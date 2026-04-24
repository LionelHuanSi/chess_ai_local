import chess
# Đơn vị: centipawn (cp)
#   1 Tốt = 100 cp  (đơn vị cơ sở)
#   1 Mã  = 320 cp  (Mã mạnh hơn 3.2 Tốt)
#   v.v...
#
# Hàm đánh giá Version 1 rất đơn giản:
#   - CHỈ đếm vật chất (số quân và giá trị)
#   - Không quan tâm vị trí quân cờ (sẽ thêm ở Version 3)
#
# Kết quả hàm đánh giá:
#   > 0  → Trắng đang tốt hơn
#   < 0  → Đen đang tốt hơn
#   = 0  → Cân bằng

# Từ điển: loại quân → giá trị (centipawns)
# Vua có giá trị rất lớn để AI không bao giờ "đổi" Vua
PIECE_VALUES = {
    chess.PAWN:   100,    # Tốt
    chess.KNIGHT: 320,    # Mã
    chess.BISHOP: 330,    # Tượng
    chess.ROOK:   500,    # Xe
    chess.QUEEN:  900,    # Hậu
    chess.KING:   20000,  # Vua (không thể mất)
}


def evaluate(board: chess.Board) -> int:
    """
    Hàm đánh giá vị trí bàn cờ — VERSION 1 (chỉ đếm vật chất).

    Tham số:
        board: đối tượng bàn cờ hiện tại (chess.Board)

    Trả về:
        int: điểm số từ góc nhìn của Trắng
            > 0 = Trắng tốt hơn | < 0 = Đen tốt hơn | 0 = cân bằng
    """

    # --- Xử lý các trạng thái kết thúc trước ---

    # Chiếu hết: bên đang đến lượt bị thua
    if board.is_checkmate():
        # Nếu Trắng đang đến lượt mà bị chiếu hết → Trắng thua → điểm rất âm
        if board.turn == chess.WHITE:
            return -99999
        # Ngược lại Đen thua → điểm rất dương (tốt cho Trắng)
        else:
            return 99999

    # Hòa cờ: tất cả các loại hòa đều trả về 0 (không bên nào lợi)
    if (board.is_stalemate()            # Hết nước đi nhưng không bị chiếu
            or board.is_insufficient_material()  # Không đủ quân để chiếu hết
            or board.is_fifty_moves()            # 50 nước không ăn/không đi Tốt
            or board.is_repetition(3)):          # Lặp vị trí 3 lần
        return 0

    # --- Tính điểm vật chất ---
    score = 0  # Bắt đầu từ 0 (cân bằng)

    # board.piece_map() trả về dict: {ô → quân}
    # Ví dụ: {chess.E1: Piece(KING, WHITE), chess.D8: Piece(QUEEN, BLACK), ...}
    for square, piece in board.piece_map().items():
        # Lấy giá trị của loại quân này (Tốt=100, Mã=320,...)
        value = PIECE_VALUES[piece.piece_type]

        if piece.color == chess.WHITE:
            score += value   # Quân Trắng → cộng vào điểm
        else:
            score -= value   # Quân Đen → trừ vào điểm

    return score