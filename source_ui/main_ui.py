import enum

from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from vogl_game import *

image = 'pictures/pepe_bear (2).png'
victory_image = 'pictures/h_pepe.png'
defeat_image = 'pictures/think_pepe.png'
white_color = 'background-color:white; border-radius:5px'
red_color = 'background-color:red; border-radius:5px'
green_color = 'background: rgb(0,255,0); border-radius:5px'


class MainWindowUI(QMainWindow):

    def __init__(self):
        super(MainWindowUI, self).__init__()

        uic.loadUi('source_ui/vogl.ui', self)
        self.show()

        self.button = self.findChild(QPushButton, "startButton")

        self.level_line = self.findChild(QLineEdit, "levelLine")

        self.level_box = self.findChild(QComboBox, "levelsBox")
        self.fill_combobox(self.level_box)
        self.level_box.currentTextChanged.connect(self.level_selected)

        self.button.clicked.connect(lambda: self.game_window(self.level_box.currentText()))
        self.button.clicked.connect(self.close)

    def fill_combobox(self, level_box: QtWidgets.QComboBox):
        files = os.listdir(path)
        for i in files:
            level_box.addItem(i)

    def game_window(self, level):
        self.g_window = GameUI(self, level)
        self.g_window.show()

    def level_selected(self):
        pass


class GameUI(QMainWindow):

    def __init__(self, main, level):
        super(GameUI, self).__init__()

        uic.loadUi('source_ui/vogl_g_w.ui', self)

        self.exit_button = self.findChild(QPushButton, "exitButton")
        self.exit_button.clicked.connect(lambda: self.close())

        self.restart_button = self.findChild(QPushButton, "restartButton")
        self.restart_button.clicked.connect(lambda: self.restart_game())

        self.grid = self.findChild(QGridLayout, "gridLayout")

        self.game = Game(level)
        self.game_service = GameService()
        self.board = self.game.board
        self.game_board = self.board.copy()
        self.main_window = main
        self.point_to_label = self.init_game()

    def init_game(self):
        return self.draw_game_field(self.grid, self.game)

    def click_to_move(self, row, col):
        def click(event):
            state = StateEnum.start
            if hasattr(self, 'pos_r') and hasattr(self, 'pos_c'):
                self.prev = Point(self.pos_r, self.pos_c)
                self.light_possible_moves(self.board, self.curr, state)
            state = StateEnum.in_process
            self.curr = Point(row, col)
            if self.game_board[row][col] == 1:
                self.pos_r = row
                self.pos_c = col
                self.prev = Point(self.pos_r, self.pos_c)
                self.moves = self.light_possible_moves(self.board, self.curr, state)
            if self.game_board[row][col] == 0:
                self.show_move(self.game_board, self.moves, self.prev, self.curr)
            result = GameService.is_game_over(self.game)

            if result is None:
                pass
            else:
                self.show_result_window(self.main_window, GameService.is_game_over(self.game))

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

    def draw_board(self, point_label_dict: dict):
        size = len(self.board)
        for row in range(size):
            for column in range(size):
                temp_label = point_label_dict.get((row, column))
                if self.game_board[row][column] == 0:
                    temp_label.clear()
                    temp_label.setStyleSheet(white_color)
                if self.game_board[row][column] == 1:
                    temp_label.setStyleSheet(white_color)
                    pixmap = QPixmap(image)
                    temp_label.setPixmap(pixmap)
                    temp_label.resize(pixmap.width(), pixmap.height())

    def light_possible_moves(self, board: list[list: int], curr_pos: Point, state):
        moves = self.game_service.get_possible_moves(board, curr_pos)
        for i in range(len(moves)):
            curr_label = self.point_to_label.get(moves[i])
            if state == StateEnum.in_process:
                curr_label.setStyleSheet(green_color)
            if state == StateEnum.start:
                curr_label.setStyleSheet(white_color)
                pass
        return moves

    def show_move(self, board, moves: list, curr_pos: Point, target_pos: Point):
        for i in moves:
            if i == (target_pos.r, target_pos.c):
                self.game_service.make_move(board, curr_pos, target_pos)
                self.draw_board(self.point_to_label)
                break
        pass

    def show_result_window(self, main_window, result):
        self.res_win = GameResultUI(main_window, self, result)
        self.res_win.show()

    def restart_game(self):
        self.main_window.show()
        self.close()


class GameResultUI(QMainWindow):
    def __init__(self, main, game, result):
        super(GameResultUI, self).__init__()

        uic.loadUi('source_ui/result.ui', self)

        self.image_label = self.findChild(QLabel, "image_label")
        self.text_label = self.findChild(QLabel, "text_label")

        self.restart_btn = self.findChild(QPushButton, 'menu_button')
        self.restart_btn.clicked.connect(lambda: self.back_to_menu())
        self.restart_btn.clicked.connect(self.close)

        self.exit_btn = self.findChild(QPushButton, 'exit_button')
        self.exit_btn.clicked.connect(lambda: self.exit_game())
        self.exit_btn.clicked.connect(self.close)

        self.show_result(result, self.image_label, self.text_label)

        self.main_window = main
        self.game_window = game

    def show_result(self, result, img_label: QLabel, txt_label: QLabel):
        img_label.setAlignment(Qt.AlignCenter)
        txt_label.setAlignment(Qt.AlignCenter)

        if result == 'Victory':
            pixmap = QPixmap(victory_image)
            img_label.setPixmap(pixmap)
            img_label.resize(pixmap.width(), pixmap.height())
            txt_label.setText('Congratulations! You won!')
        if result == 'Defeat':
            pixmap = QPixmap(defeat_image)
            img_label.setPixmap(pixmap)
            img_label.resize(pixmap.width(), pixmap.height())
            txt_label.setText("Oh no, no more moves! \n Well, that's okay next time you win!")

    def back_to_menu(self):
        self.game_window.close()
        self.main_window.show()

    def exit_game(self):
        self.game_window.close()


class StateEnum(enum.Enum):
    start = 0,
    in_process = 1,
    to_step_over = 2
