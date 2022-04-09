from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from source_ui.main_screen_ui import Ui_MainWindow
from source_ui.game_process_ui import Ui_vogl_g_w
from PyQt5.QtWidgets import QMainWindow
from vogl_game import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from vogl_game import *
import functools

image = 'pictures/pepe_bear (2).png'
white_color = 'background-color:white; border-radius:5px'
green_color = 'background: rgb(0,255,0); border-radius:5px'


class MainWindowUI(QMainWindow):

    def __init__(self):
        super(MainWindowUI, self).__init__()

        uic.loadUi('source_ui/vogl.ui', self)
        self.show()
        #

        self.button = self.findChild(QPushButton, "startButton")

        self.button.clicked.connect(lambda: self.game_window())
        self.button.clicked.connect(self.close)

        self.game = GameUI(self)

    def game_window(self):
        self.g_window = GameUI(self)
        self.g_window.show()


class GameUI(QMainWindow):

    def __init__(self, main):
        super(GameUI, self).__init__()

        uic.loadUi('source_ui/vogl_g_w.ui', self)

        self.game = Game(1)
        self.game_service = GameService()
        self.board = self.game.board
        self.main_window = main
        self.point_to_label = self.init_game()

    def init_game(self):
        return self.draw_game_field(Ui_vogl_g_w.get_layout(self), self.game)

    def click_to_move(self, row, col):
        def click(event):
            state = 0
            if hasattr(self, 'pos_x') and hasattr(self, 'pos_y'):
                self.prev = Point(self.pos_x, self.pos_y)
                self.light_possible_moves(self.board, self.curr, state)
                state = 1
            self.pos_x = col
            self.pos_y = row
            self.curr = Point(row, col)
            self.light_possible_moves(self.board, self.curr, state)
            self.repaint()

        return click

    def draw_game_field(self, layout: QtWidgets.QGridLayout, game: Game):
        point_to_label = dict()
        size = game.field_size
        for row in range(size):
            for column in range(size):
                label = QtWidgets.QLabel()
                label.setAlignment(Qt.AlignCenter)
                if game.board[row][column] == 0:
                    point_to_label[(row, column)] = label
                    label.mousePressEvent = self.click_to_move(row, column)
                    label.setStyleSheet(white_color)
                else:
                    point_to_label[(row, column)] = label
                    label.mousePressEvent = self.click_to_move(row, column)
                    label.setStyleSheet(white_color)
                    pixmap = QPixmap(image)
                    label.setPixmap(pixmap)
                    label.resize(pixmap.width(), pixmap.height())
                layout.addWidget(label, row, column)
        return point_to_label

    def light_possible_moves(self, board: list[list: int], curr_pos: Point, state):
        moves = self.game_service.get_possible_moves(board, curr_pos)
        for i in range(len(moves)):
            curr_label = self.point_to_label.get(moves[0])
            if state == 1:
                curr_label.setStyleSheet(green_color)
            if state == 0:
                curr_label.setStyleSheet(white_color)
