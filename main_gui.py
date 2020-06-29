import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from static_func import *
from players import Player
import numpy as np


def update_interface_gird_values(obj, grid, rest):
    for button_id in range(100, 200, 1):
        button_str = str(button_id)
        y = int(button_str[1])
        x = int(button_str[2])
        obj.player_group.button(button_id).setText(
            str(grid[y][x]))
        if grid[y][x] == 1:
            obj.player_group.button(button_id).setStyleSheet("background-color: "
                                                     "#808080")
        elif grid[y][x] == 555 and rest == True:
            obj.player_group.button(button_id).setStyleSheet("background-color: "
                                                     "None")


def clear_style_sheet(obj):
    for i in range(100, 199, 1):
        obj.player_group.button(i).setStyleSheet("background-color: "
                                                  "None")


def grid_to_gid(gird_loc):
    gid = 100 + int(str(gird_loc[0]) + str(gird_loc[1]))
    return gid


def gid_to_grid(gid):
    button_id = str(gid)
    button_id = [int(button_id[1]), int(button_id[2])]
    return button_id


def add_buttons(grid, ischeckable, group):
    positions = [[i, j] for i in range(10) for j in range(10)]
    for position in positions:
        gid = grid_to_gid([position[0], position[1]])
        loc = str(to_alpha_numeric(position))
        loc = loc.replace("['", "")
        loc = loc.replace("']", "")
        button = qtw.QPushButton("{}".format(loc))
        button.setFixedHeight(40)
        button.setFixedWidth(60)
        button.setCheckable(ischeckable)
        grid.addWidget(button, *position)
        group.addButton(button, id=gid)


class SplashScreen(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.slash_widget = qtw.QWidget()
        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        # Heading label
        self.heading = qtw.QLabel()
        self.heading.setText('You sunk my BattleShip!!')
        self.layout.addWidget(self.heading)
        heading_font = qtg.QFont('Impact', 18, qtg.QFont.Bold)
        heading_font.setStretch(qtg.QFont.ExtraExpanded)
        self.heading.setFont(heading_font)

        # Logo
        logo = qtg.QPixmap('pic/battleship_icon.png')
        logo_label = qtw.QLabel()
        logo_label.setPixmap(logo)
        self.layout.addWidget(logo_label)

        # Start and quit buttons
        self.start_btn = qtw.QPushButton('New Round')
        self.quit_btn = qtw.QPushButton('Quit')
        self.layout.addWidget(self.start_btn)
        self.layout.addWidget(self.quit_btn)

        # About
        footing = qtw.QLabel()
        footing.setText('V0.1 By Peter Agalakov')
        footing.setAlignment(qtc.Qt.AlignCenter)
        self.layout.addWidget(footing)

        # Logic
        self.start_btn.clicked.connect(self.start_setup)
        self.quit_btn.clicked.connect(self.quit_now)

        # Frame settings
        self.move(800, 300)
        self.setWindowTitle("BattleShip!")
        self.center()
        self.show()

    def quit_now(self):
        self.close()
        sys.exit()

    def start_setup(self):
        setup.show()
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = qtw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Window(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.test_value = np.full((10, 10), 555)
        self.selected_locations = []
        self.selected_sum = 0
        self.selected_limit = 7
        main_layout = qtw.QGridLayout()

        # Player's gird
        player_widget = qtw.QWidget()
        player_layout = qtw.QGridLayout()
        player_widget.setLayout(player_layout)
        # Enemy gird
        pc_widget = qtw.QWidget()
        pc_layout = qtw.QGridLayout()
        pc_widget.setLayout(pc_layout)

        # pc label
        pc_label = qtw.QLabel()
        pc_label.setText('PC:')
        pc_label.setAlignment(qtc.Qt.AlignCenter)
        # Player : name label
        player_label = qtw.QLabel()
        player_label.setText('Player:')
        player_label.setAlignment(qtc.Qt.AlignCenter)

        # Fire button
        self.fire_button = qtw.QPushButton('Fire the Missiles')

        #  Logic
        self.player_group = qtw.QButtonGroup(self)
        self.pc_group = qtw.QButtonGroup(self)
        add_buttons(player_layout, False, self.player_group)
        add_buttons(pc_layout, True, self.pc_group)
        self.pc_group.setExclusive(False)
        self.pc_group.buttonClicked.connect(self.grid_space_selected)
        self.fire_button.clicked.connect(self.fire_button_action)
        self.update_player_button_value()
        # Layout
        self.setLayout(main_layout)

        main_layout.addWidget(pc_label, 0, 0)
        main_layout.addWidget(pc_widget, 1, 0)
        main_layout.addWidget(player_label, 2, 0)
        main_layout.addWidget(player_widget, 3, 0)
        main_layout.addWidget(self.fire_button, 0, 2)

        self.move(500, 100)
        self.center()
        self.setWindowTitle("BattleShip!")

    def grid_space_selected(self, gid):
        if gid.isChecked():
            self.selected_sum += 1
            print(self.selected_sum)
            self.selected_locations.append(self.pc_group.id(gid))
        elif gid.isChecked() is False:
            self.selected_sum -= 1
            self.selected_locations.remove(self.pc_group.id(gid))
            print(self.selected_sum)

    def fire_button_action(self):
        if self.selected_sum < self.selected_limit:
            print(self.selected_locations)
            # print([i for i, button in
            #        enumerate(self.pc_group.buttons()) if
            #        button.isChecked()])
        else:
            print('Too many locations are selected')

    def update_player_button_value(self):
        for y in range(0, 10, 1):
            for x in range(0, 10, 1):
                gid = 100 + (y * 10) + x
                self.player_group.button(gid).setText(
                    str(self.test_value[y][x]))

    def update_pc_button_value(self):
        for y in range(0, 10, 1):
            for x in range(0, 10, 1):
                gid = 100 + (y * 10) + x
                self.pc.button(gid).setText(
                    str(self.test_value[y][x]))

    def show_window(self):
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = qtw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Setup(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.player = Player('Player')
        self.main_layout = qtw.QGridLayout()
        self.end_loc = []
        self.anchor_point = []

        # Player's gird
        player_widget = qtw.QWidget()
        player_layout = qtw.QGridLayout()
        player_widget.setLayout(player_layout)

        # Player : name label
        player_label = qtw.QLabel()
        player_label.setFont(qtg.QFont('Impact', 16))
        player_label.setText('Your grid : ')
        player_label.setAlignment(qtc.Qt.AlignCenter)

        # Place holder label
        ships_label = qtw.QLabel()
        ships_label.setFont(qtg.QFont('monospace [Consolas]', 18))
        ships_label.setText('Select a ship : ')
        ships_label.setAlignment(qtc.Qt.AlignCenter)

        # BattleShip button group
        self.ship_list = qtw.QWidget()
        self.ship_layout = qtw.QVBoxLayout()
        self.ship_list.setLayout(self.ship_layout)
        self.ship_setup_group = qtw.QButtonGroup(self)

        self.battleship = qtw.QRadioButton()
        self.cruiser = qtw.QRadioButton()
        self.sub = qtw.QRadioButton()
        self.reset = qtw.QPushButton('Reset placement')

        self.ship_setup_group.addButton(self.battleship, id=1)
        self.ship_setup_group.addButton(self.cruiser, id=2)
        self.ship_setup_group.addButton(self.sub, id=3)


        self.ship_layout.addWidget(self.battleship)
        self.ship_layout.addWidget(self.cruiser)
        self.ship_layout.addWidget(self.sub)
        self.ship_layout.addWidget(self.reset)


        # BattleShip button group Logic
        self.player_group = qtw.QButtonGroup()
        add_buttons(player_layout, False, self.player_group)
        self.player_group.buttonClicked.connect(self.setup_button_click)
        self.reset.clicked.connect(self.reset_radio_buttons)
        self.reset_radio_buttons()

        # Warning label
        self.console_label = qtw.QLabel()
        self.console_label.setText('Please set up your ships.')
        self.console_label.setAlignment(qtc.Qt.AlignCenter)
        self.console_label.setFont(qtg.QFont('monospace [Consolas]', 14))



        # Layout
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(player_label, 0, 0)
        self.main_layout.addWidget(player_widget, 1, 0)
        self.main_layout.addWidget(ships_label, 0, 1)
        self.main_layout.addWidget(self.ship_list, 1, 1)
        self.main_layout.addWidget(self.console_label, 2, 0)

        update_interface_gird_values(self, self.player.grid, False)
        self.move(200, 200)
        self.setWindowTitle("BattleShip!")

    def setup_button_click(self, button_obj):
        clear_style_sheet(self)
        selected_button = gid_to_grid(self.player_group.id(button_obj))
        ship_id = self.ship_setup_group.checkedId()
        if ship_id != -1:
            ship_obj = self.player.get_ship_by_id(ship_id)

        end_point_check = self.end_point_in_end_loc(selected_button)
        is_grid_free = self.is_free_grid(selected_button)

        if ship_id == -1:
            self.console_label.setText('No ship is selected')
            self.console_label.setStyleSheet("background-color: #ffa500")

        elif is_grid_free is False:
            self.console_label.setText('Location is used!')
            self.console_label.setStyleSheet("background-color: #ffa500")
            self.anchor_point = []
            self.end_loc = []

        elif end_point_check:
            self.player.place_ship(ship_obj, self.anchor_point, selected_button)
            self.console_label.setStyleSheet("background-color: #00ffa5")
            self.console_label.setText(ship_obj.name + " Has been placed")
            self.placed_ship_radio_btn(ship_id)
            self.anchor_point = []
            self.end_loc = []

        elif is_grid_free:
            self.end_loc, print_loc = self.get_end_loc(selected_button,
                                                       ship_obj)
            self.anchor_point = selected_button
            self.console_label.setText(str(print_loc))
            self.console_label.setStyleSheet("background-color: #00ffa5")
            self.set_end_loc_buttons(self.end_loc)

        update_interface_gird_values(self, self.player.grid, False)

    def get_end_loc(self, selected_button, ship):
        return self.player.set_anchor(ship, selected_button)

    def set_end_loc_buttons(self, end_loc):
        for i in end_loc:
            gid = 100 + (10 * i[0]) + i[1]
            self.player_group.button(gid).setStyleSheet("background-color: "
                                                        "red")

    def is_free_grid(self, selected_button):
        if self.player.grid[selected_button[0], selected_button[1]] == 555:
            return True
        else:
            return False

    def end_point_in_end_loc(self, selected_button):
        for i in self.end_loc:
            if i == selected_button:
                return True
        else:
            return False

    def placed_ship_radio_btn(self, ship_id):
        self.ship_setup_group.setExclusive(False)
        self.ship_setup_group.button(ship_id).setChecked(False)
        self.ship_setup_group.button(ship_id).setEnabled(False)
        self.ship_setup_group.button(ship_id).setText('Placed')
        self.ship_setup_group.setExclusive(True)

    def reset_radio_buttons(self):
        self.ship_setup_group.setExclusive(False)
        for i in self.ship_setup_group.buttons():
            i.setChecked(False)
            i.setEnabled(True)
        self.ship_setup_group.setExclusive(True)
        self.battleship.setText('Battleship (size : 5)')
        self.cruiser.setText('Cruiser (size : 3)')
        self.sub.setText('Submarine (size : 1)')
        self.player = Player('Player')
        self.anchor_point = []
        self.end_loc = []
        update_interface_gird_values(self, self.player.grid, True)



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    setup = Setup()
    run = Window()
    splash = SplashScreen()
    sys.exit(app.exec())

