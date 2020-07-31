import sys
from players import Player
from pc import Pc
from static_gui_funcs import *
import random


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
        self.setWindowTitle("BattleShip!")
        self.center()
        self.show()

    def quit_now(self):
        self.close()
        sys.exit()

    def start_setup(self):
        global setup
        setup = Setup()
        setup.show()
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = qtw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Combat(qtw.QWidget):
    def __init__(self, obj):
        super().__init__()
        self.selected_locations = []
        self.combat_layout = qtw.QGridLayout()
        self.setLayout(self.combat_layout)
        self.setup_obj = obj
        self.pc = Pc('Pc')
        self.selected_limit = self.setup_obj.player.get_salvo_limit()

        # Enemy gird
        self.pc_widget = qtw.QWidget()
        self.pc_layout = qtw.QGridLayout()
        self.pc_widget.setLayout(self.pc_layout)

        # pc label
        self.pc_label = qtw.QLabel()
        self.pc_label.setText('PC:')
        self.pc_label.setFont(qtg.QFont('Impact', 16))
        self.pc_label.setAlignment(qtc.Qt.AlignCenter)

        # Fire button
        self.fire_button = qtw.QPushButton('Fire the Missiles')
        self.fire_button.setFixedHeight(60)

        # LCD num
        self.salvo_label = qtw.QLabel('Available salvos:')
        self.salvo_lcd = qtw.QLCDNumber()
        self.salvo_lcd.display(str(self.selected_limit))

        #  Logic
        self.pc_group_widget = qtw.QWidget()
        self.pc_group_layout = qtw.QGridLayout()
        self.pc_group_widget.setLayout(self.pc_group_layout)
        self.pc_tracking_grid = qtw.QButtonGroup(self)
        add_buttons(self.pc_group_layout, True, self.pc_tracking_grid)
        self.pc_tracking_grid.setExclusive(False)
        self.pc_tracking_grid.buttonClicked.connect(self.grid_space_selected)
        self.fire_button.clicked.connect(self.fire_button_action)

        # Layout
        # Player's widget space
        self.player_widget = qtw.QWidget()
        self.import_layout = qtw.QGridLayout()
        self.import_layout.addWidget(self.setup_obj.player_label, 0, 1)
        self.import_layout.addWidget(self.setup_obj.player_widget, 3, 1)
        self.import_layout.addWidget(self.setup_obj.console_label, 4, 1)
        add_horizontal_coordinates_label(self.import_layout, 2, 1)
        add_vertical_coordinates_label(self.import_layout, 3, 0)
        self.player_widget.setLayout(self.import_layout)

        # Pc layout
        self.pc_layout.addWidget(self.pc_label, 0, 1)
        add_horizontal_coordinates_label(self.pc_layout, 1, 1)
        add_vertical_coordinates_label(self.pc_layout, 2, 0)
        self.pc_layout.addWidget(self.pc_group_widget, 2, 1)

        # Controls layout
        self.controls_widget = qtw.QWidget()
        self.controls_layout = qtw.QVBoxLayout()
        self.controls_layout.addSpacing(100)
        self.controls_widget.setLayout(self.controls_layout)
        self.controls_layout.addWidget(self.fire_button)
        self.controls_layout.addWidget(self.salvo_label)
        self.controls_layout.addWidget(self.salvo_lcd)

        # Adding all Widgets to main grid layout
        self.combat_layout.addWidget(self.player_widget, 0, 1)
        self.combat_layout.addWidget(self.pc_widget, 0, 2)
        self.combat_layout.addWidget(self.controls_widget, 0, 3)
        self.combat_layout.addWidget(self.setup_obj.console_label, 1, 1, 1, 2)

        # Logic
        self.setup_to_combat()

        self.who_starts = random.randint(1, 2)
        if self.who_starts == 2:
            print('PC goes first')
            self.play_a_turn()

        self.update_combat_interface()

        self.move(200, 200)
        self.setWindowTitle("BattleShip!")

    def grid_space_selected(self, gid):
        if gid.isChecked():
            self.selected_limit -= 1
            self.salvo_lcd.display(str(self.selected_limit))
            self.selected_locations.append(self.pc_tracking_grid.id(gid))
        elif gid.isChecked() is False:
            self.selected_limit += 1
            self.selected_locations.remove(self.pc_tracking_grid.id(gid))
            self.salvo_lcd.display(str(self.selected_limit))

    def fire_button_action(self):
        if self.selected_limit >= 0:
            for i in self.selected_locations:
                loc = gid_to_grid(i)
                fire_salvo(self.pc, loc, self.setup_obj.player)

            self.pc.is_alive()
            self.play_a_turn()
            self.setup_obj.player.is_alive()
            self.selected_locations = []
            self.update_combat_interface()
            self.selected_limit = self.setup_obj.player.get_salvo_limit()
            self.salvo_lcd.display(str(self.selected_limit))

        else:
            print('Too many locations are selected')

    def paintEvent(self, event):
        qp = qtg.QPainter()
        qp.begin(self)
        self.draw_rect(qp)
        qp.end()

    def draw_rect(self, qp):
        for rect in self.setup_obj.ship_rect_obj:
            pos1 = [rect[0].pos().x(), rect[0].pos().y()]
            pos2 = [rect[1].pos().x(), rect[1].pos().y()]

            qp.setPen(qtg.QPen(qtc.Qt.black, 8, qtc.Qt.SolidLine))
            width = pos2[0] - pos1[0]
            height = pos2[1] - pos1[1]

            if height == 0:
                height = 45
                if width > 0:
                    qp.drawRect(pos1[0] + 55, pos1[1] + 85, width + 65,
                                height)
                else:
                    qp.drawRect(pos1[0] + 120, pos1[1] + 85, width - 65,
                                height)
            elif width == 0:
                width = 60
                if height > 0:
                    qp.drawRect(pos1[0] + 55, pos1[1] + 85, width, height +
                                45)
                else:
                    qp.drawRect(pos1[0] + 55, pos1[1] + 133, width, height -
                                45)

    def setup_to_combat(self):
        for button_id in range(100, 200, 1):
            button = self.setup_obj.player_group.button(button_id)
            button.setEnabled(False)

    def play_a_turn(self):
        hit_list = self.pc.make_hit_list(self.pc.get_salvo_limit())
        for i in hit_list:
            fire_salvo(self.setup_obj.player, i, self.pc)
        self.update_combat_interface()

    def update_combat_interface(self):
        update_interface_gird_values_combat(self.setup_obj.player_group,
                                            self.setup_obj.player.grid)

        update_interface_gird_values_combat(self.pc_tracking_grid,
                                        self.setup_obj.player.tracking_grid)


class Setup(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.player = Player('Player')
        self.main_layout = qtw.QGridLayout()
        self.end_loc = []
        self.anchor_point = []
        self.anchor_obj = None
        self.ship_rect_obj = []

        # Player : name label
        self.player_label = qtw.QLabel()
        self.player_label.setFont(qtg.QFont('Impact', 16))
        self.player_label.setText('Your grid : ')
        self.player_label.setAlignment(qtc.Qt.AlignCenter)

        # Player's gird
        self.player_widget = qtw.QWidget()
        self.player_layout = qtw.QGridLayout()
        self.player_widget.setLayout(self.player_layout)

        # Warning label
        self.console_label = qtw.QLabel()
        self.console_label.setText('Please set up your ships.')
        self.console_label.setAlignment(qtc.Qt.AlignCenter)
        self.console_label.setFont(qtg.QFont('monospace [Consolas]', 14))

        # BattleShip button
        self.player_group = qtw.QButtonGroup()
        add_buttons(self.player_layout, False, self.player_group)

        # BattleShip button group
        self.ships_label = qtw.QLabel()
        self.ships_label.setFont(qtg.QFont('monospace [Consolas]', 18))
        self.ships_label.setText('Select a ship : ')
        self.ships_label.setAlignment(qtc.Qt.AlignCenter)

        self.ship_list = qtw.QWidget()
        self.ship_layout = qtw.QVBoxLayout()
        self.ship_button_group = qtw.QButtonGroup()
        add_ship_buttons(self, self.player)

        # Reset button
        self.reset = qtw.QPushButton('Reset placement')
        self.ship_layout.addWidget(self.reset)
        self.ship_list.setLayout(self.ship_layout)

        # Done button
        self.done = qtw.QPushButton('Done', clicked=self.setup_done)
        self.done.setFixedHeight(40)
        self.ship_layout.addWidget(self.done)

        # Logic
        self.reset_ship_list()
        self.player_group.buttonClicked.connect(self.setup_button_click)
        self.reset.clicked.connect(self.reset_ship_list)

        # Layout
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.player_label, 0, 1)
        self.main_layout.addWidget(self.player_widget, 2, 1)
        self.main_layout.addWidget(self.ships_label, 0, 2)
        self.main_layout.addWidget(self.ship_list, 2, 2)
        self.main_layout.addWidget(self.console_label, 3, 1)
        add_horizontal_coordinates_label(self.main_layout, 1, 1)
        add_vertical_coordinates_label(self.main_layout, 2, 0)

        update_interface_gird_values_setup(self, self.player.grid, False)
        self.center()
        self.setWindowTitle("BattleShip!")

    def setup_button_click(self, button_obj):
        selected_button = gid_to_grid(self.player_group.id(button_obj))
        ship_id = self.ship_button_group.checkedId()
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
            self.ship_rect_obj.append([self.anchor_obj, button_obj])
            self.console_label.setStyleSheet("background-color: #00ffa5")
            self.console_label.setText(ship_obj.name + " has been placed")
            self.placed_ship_radio_btn(ship_id)
            self.anchor_point = []
            self.end_loc = []

        elif is_grid_free:
            self.end_loc, print_loc = self.get_end_loc(selected_button,
                                                       ship_obj)
            self.anchor_point = selected_button
            self.anchor_obj = button_obj
            self.console_label.setText(str(print_loc))
            self.console_label.setStyleSheet("background-color: #00ffa5")

        update_interface_gird_values_setup(self, self.player.grid, False)
        self.update()

    def get_end_loc(self, selected_button, ship):
        return self.player.set_anchor(ship, selected_button)

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
        self.ship_button_group.setExclusive(False)
        self.ship_button_group.button(ship_id).setChecked(False)
        self.ship_button_group.button(ship_id).setEnabled(False)
        self.ship_button_group.button(ship_id).setText('Placed')
        self.ship_button_group.setExclusive(True)

    def reset_ship_list(self):
        ship_list_reset_text(self, self.player.my_ships)
        self.ship_button_group.setExclusive(False)
        for i in self.ship_button_group.buttons():
            i.setChecked(False)
            i.setEnabled(True)
        self.ship_button_group.setExclusive(True)
        self.player = Player('Player')
        self.anchor_point = []
        self.end_loc = []
        self.ship_rect_obj = []
        self.update()
        self.console_label.setText('Board was reset')
        self.console_label.setStyleSheet("background-color: #00ffa5")
        update_interface_gird_values_setup(self, self.player.grid, True)

    def paintEvent(self, event):
        qp = qtg.QPainter()
        qp.begin(self)
        self.draw_rect(qp)
        qp.end()

    def draw_rect(self, qp):
        for rect in self.ship_rect_obj:
            pos1 = [rect[0].pos().x(), rect[0].pos().y()]
            pos2 = [rect[1].pos().x(), rect[1].pos().y()]

            qp.setPen(qtg.QPen(qtc.Qt.black, 8, qtc.Qt.SolidLine))
            width = pos2[0] - pos1[0]
            height = pos2[1] - pos1[1]

            if height == 0:
                height = 45
                if width > 0:
                    qp.drawRect(pos1[0] + 45, pos1[1] + 80, width + 65,
                                height)
                else:
                    qp.drawRect(pos1[0] + 110, pos1[1] + 80, width - 65,
                                height)
            elif width == 0:
                width = 60
                if height > 0:
                    qp.drawRect(pos1[0] + 47, pos1[1] + 80, width, height +
                                45)
                else:
                    qp.drawRect(pos1[0] + 47, pos1[1] + 125, width, height -
                                45)

    def setup_done(self):
        global combat

        all_ships_placed = True
        for i in self.player.my_ships:
            if not i.location:
                all_ships_placed = False

        if all_ships_placed:
            combat = Combat(self)
            self.hide()
            combat.show()
        else:
            msg_box = qtw.QMessageBox()
            msg_box.setIcon(qtw.QMessageBox.Warning)
            msg_box.setText('You need to place all ships')
            msg_box.exec()

    def center(self):
        qr = self.frameGeometry()
        cp = qtw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    splash = SplashScreen()
    setup = None
    combat = None
    sys.exit(app.exec())

