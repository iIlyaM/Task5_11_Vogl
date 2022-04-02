from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.game = Game(self)
        self.textboxLevel = QLineEdit(self)

        self.themeLabel = QLabel(self)
        self.labelLevel = QLabel(self)

        self.radioBtnLite = QRadioButton(self)
        self.radioBtnDark = QRadioButton(self)

        self.buttonStart = QPushButton(self)
        self.buttonHelp = QPushButton(self)

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Вогл')
        # self.setWindowIcon(QIcon('items/logo.png'))
        # self.setStyleSheet("background-color: #E6E6FA")

        self.themeLabel.setText('Цветовая тема')
        self.themeLabel.move(120, 120)
        self.themeLabel.resize(80, 20)

        self.labelLevel.setText('Номер уровня 1-10')
        self.labelLevel.move(120, 180)
        self.labelLevel.resize(80, 20)

        self.radioBtnLite.setText('Светлая')
        self.radioBtnLite.move(120, 140)
        self.radioBtnLite.resize(80, 20)
        self.radioBtnDark.setText('Темная')
        self.radioBtnDark.move(200, 140)
        self.radioBtnDark.resize(80, 20)

        self.textboxLevel.move(220, 180)
        self.textboxLevel.resize(50, 20)
        self.textboxLevel.setText('1')

        self.buttonStart.move(100, 230)
        self.buttonStart.resize(200, 50)
        self.buttonStart.setText('START')
        self.buttonStart.clicked.connect(self.on_action)

        self.buttonHelp.move(100, 300)
        self.buttonHelp.resize(200, 30)
        self.buttonHelp.setText('HELP')
        # self.buttonHelp.clicked.connect(self.on_action_help)

    def on_action(self):
        theme = 0
        if self.radioBtnDark.isChecked():
            theme = 1
        if self.textboxLevel.text() == '':
           # self.game = Game(self, 0, theme)
            self.buttonStart.setText('RESTART')
            self.game.show()
            self.hide()
        elif int(self.textboxLevel.text()) > 0:
           # self.game = Game(self, int(self.textboxLevel.text()), theme)
            self.buttonStart.setText('RESTART')
            self.game.show()
            self.hide()
