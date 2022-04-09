import sys
from PyQt5.QtWidgets import QApplication
from source_ui.main_ui import *


def main():
    app = QApplication(sys.argv)
    # start_wind = Ui_MainWindow()
    # win = QtWidgets.QMainWindow()
    # #start_wind.setupUi(win)
    win = MainWindowUI()
#    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()