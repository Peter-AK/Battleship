import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QGridLayout,
    QPushButton, QButtonGroup)
from PyQt5.QtCore import Qt
from static_func import *
from main import new_round

def add_buttons(grid, ischeckable, group):
    positions = [[i, j] for i in range(10) for j in range(10)]

    for position in positions:
        gid = 100 + int(str(position[0]) + str(position[1]))
        loc = str(to_alpha_numeric(position))
        loc = loc.replace("['", "")
        loc = loc.replace("']", "")
        button = QPushButton("{}".format(loc))
        button.setCheckable(ischeckable)
        grid.addWidget(button, *position)
        group.addButton(button, id=gid)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_locations = []
        self.selected_sum = 0
        main_layout = QGridLayout()

        # Player's gird
        player_widget = QWidget()
        player_layout = QGridLayout()
        player_widget.setLayout(player_layout)
        # Enemy gird
        pc_widget = QWidget()
        pc_layout = QGridLayout()
        pc_widget.setLayout(pc_layout)

        # pc label
        pc_label = QLabel()
        pc_label.setText('PC')
        pc_label.setAlignment(Qt.AlignCenter)
        # Player : name label
        player_label = QLabel()
        player_label.setText('Player: <Name>')
        player_label.setAlignment(Qt.AlignCenter)

        # Fire button
        self.fire_button = QPushButton('Fire the Missiles')

        # Logic
        self.player_group = QButtonGroup(self)
        self.pc_group = QButtonGroup(self)
        add_buttons(player_layout, False, self.player_group)
        add_buttons(pc_layout, True, self.pc_group)
        self.pc_group.setExclusive(False)
        self.pc_group.buttonClicked.connect(self.grid_space_selected)
        self.fire_button.clicked.connect(self.fire_button_action)

        self.setLayout(main_layout)

        main_layout.addWidget(pc_label, 0, 0)
        main_layout.addWidget(pc_widget, 1, 0)
        main_layout.addWidget(player_label, 2, 0)
        main_layout.addWidget(player_widget, 3, 0)
        main_layout.addWidget(self.fire_button, 0, 2)

        self.move(800, 300)
        self.setWindowTitle("BattleShip!")
        self.show()
        new_round('Player')

    def grid_space_selected(self, gid):

        if gid.isChecked():
            self.selected_sum += 1
            print(self.selected_sum)
        elif gid.isChecked() is False:
            self.selected_sum -= 1
            print(self.selected_sum)

    def fire_button_action(self):
        if self.selected_sum < 7:
            # for button in enumerate(self.pc_group.buttons()):
            #     if button.isChecked():
            #         print(list(button))
            print([i for i, button in
                   enumerate(self.pc_group.buttons()) if
                   button.isChecked()])
        else:
            print('Too many are selected')

    def update_button_value(self, button_group):
        pass

def main():
    app = QApplication(sys.argv)
    run = Window()
    sys.exit(app.exec())
