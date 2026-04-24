# ============================================================
# main.py — Điểm khởi chạy chính
# Chạy bằng: python main.py
# ============================================================
#
# Cấu trúc project:
#   main.py              ← file này
#   ai/
#     minimax.py         ← CELL 3: minimax + get_best_move
#   game/
#     game_logic.py      ← CELL 2: PIECE_VALUES + evaluate
#   ui/
#     ui.py              ← CELL 4: ClickToMoveUI (pygame version)

import sys
import os

# Đảm bảo import được các module trong project
sys.path.insert(0, os.path.dirname(__file__))

from ui.ui import ClickToMoveUI


def main():
    game = ClickToMoveUI()
    game.run()


if __name__ == '__main__':
    main()
