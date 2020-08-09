#!/home/mateusz/anaconda3/bin/python3.7

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow

from nmm_game import NMM_Game
from nmm_pawn_types import NMM_Pawn

const = 72
coordinates_x_y = {
    'A1': (50, 50),
    'A4': (50 + 3 * const, 50),
    'A7': (50 + 6 * const, 50),
    'B2': (50 + const, 50 + const),
    'B4': (50 + 3 * const, 50 + const),
    'B6': (50 + 5 * const, 50 + const),
    'C3': (50 + 2 * const, 50 + 2 * const),
    'C4': (50 + 3 * const, 50 + 2 * const),
    'C5': (50 + 4 * const, 50 + 2 * const),
    'D1': (50, 50 + 3 * const),
    'D2': (50 + const, 50 + 3 * const),
    'D3': (50 + 2 * const, 50 + 3 * const),
    'D5': (50 + 4 * const, 50 + 3 * const),
    'D6': (50 + 5 * const, 50 + 3 * const),
    'D7': (50 + 6 * const, 50 + 3 * const),
    'E3': (50 + 2 * const, 50 + 4 * const),
    'E4': (50 + 3 * const, 50 + 4 * const),
    'E5': (50 + 4 * const, 50 + 4 * const),
    'F2': (50 + const, 50 + 5 * const),
    'F4': (50 + 3 * const, 50 + 5 * const),
    'F6': (50 + 5 * const, 50 + 5 * const),
    'G1': (50, 50 + 6 * const),
    'G4': (50 + 3 * const, 50 + 6 * const),
    'G7': (50 + 6 * const, 50 + 6 * const)
}


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(530, 530)
        self.move(100, 100)
        self.setStyleSheet("background-image: url(nmm_board_coords_530.png);")
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 6, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))

        circle_size = 40

        for field, x_y in coordinates_x_y.items():
            if board.board[field].value is NMM_Pawn.BLACK:
                painter.setBrush(QBrush(Qt.darkGray, Qt.SolidPattern))
                painter.drawEllipse(x_y[0], x_y[1], circle_size, circle_size)
            elif board.board[field].value is NMM_Pawn.WHITE:
                painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                painter.drawEllipse(x_y[0], x_y[1], circle_size, circle_size)

        lfc = board.last_filled_field_coordinates
        if lfc:
            painter.setPen(QPen(Qt.blue, 6, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.transparent, Qt.SolidPattern))
            painter.drawEllipse(coordinates_x_y[lfc][0] - 10, coordinates_x_y[lfc][1] - 10, circle_size + 20,
                                circle_size + 20)

        if board.move_history:
            last_operation = board.move_history[-1]
            if len(last_operation) == 2:
                if last_operation[0] == 'REMOVED':
                    painter.setPen(QPen(Qt.red, 6, Qt.SolidLine))
                    painter.setBrush(QBrush(Qt.transparent, Qt.SolidPattern))
                    painter.drawEllipse(coordinates_x_y[last_operation[1]][0] - 10,
                                        coordinates_x_y[last_operation[1]][1] - 10,
                                        circle_size + 20, circle_size + 20)
                else:  # shift
                    painter.setPen(QPen(Qt.darkBlue, 6, Qt.SolidLine))
                    painter.setBrush(QBrush(Qt.transparent, Qt.SolidPattern))
                    painter.drawEllipse(coordinates_x_y[last_operation[0]][0] - 10,
                                        coordinates_x_y[last_operation[0]][1] - 10,
                                        circle_size + 20, circle_size + 20)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    game = NMM_Game()
    game.main_menu()

    # minimax = MiniMax(removed_difference_ratio, NMM_Pawn.BLACK, game)
    # print(minimax.return_best_move())

    board = game.board
    window = Window()
    import _thread

    _thread.start_new_thread(game.start, (window,))
    sys.exit(app.exec_())
