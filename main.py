import sys
from PyQt5.QtWidgets import QApplication, QWidget
from window import *
from vogl_game import *


def main():
    # app = QApplication(sys.argv)
    # start_wind = MainWindow()
    # start_wind.show()
    # sys.exit(app.exec_())
    game = Game("1")
    pos = Point(4, 1)
    game.get_possible_moves(pos)

if __name__ == '__main__':
    main()