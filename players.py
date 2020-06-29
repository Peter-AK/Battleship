import numpy as np
from static_func import *
from ships import Ship
import os


class Player:
    def __init__(self, name):
        self.name = name
        self.grid = np.full((10, 10), 555)
        self.tracking_grid = np.full((10, 10), 555)
        self.non_placed_ships = [
            ['AirCraft Carrier', 5, 1],
            ['BattleShip', 4, 2],
            ['Cruiser', 3, 3],
            ['Destroyer-A', 2, 4],
            ['Destroyer-B', 2, 5],
            ['Submarine-A', 1, 6],
            ['Submarines-B', 1, 7]
        ]
        self.my_ships = [Ship(ship[0], ship[1], ship[2]) for ship in
                         self.non_placed_ships]

    # def grid_setup(self):
    #     """
    #     Prints out the grid for a visual queue, places all the ships on
    #     the gird
    #      """
    #     for ship in self.my_ships:
    #         grid = to_dataframe(self.grid)
    #         print(grid)
    #         self.place_ship(ship)

    def get_ship_by_id(self, ship_id):
        for i in self.my_ships:
            if ship_id == i.id:
                return i

        return -1

    def set_anchor(self, ship, start_loc):
        """
        Asks the user for an anchor point and an end point for each
        ship that has not been placed.
        """

        valid_end_loc = self.is_free(start_loc, ship)

        valid_end_loc, print_loc = select_dict(valid_end_loc)
        return valid_end_loc, print_loc

    def place_ship(self, ship, start_loc, end_loc):

        place_ship_on_grid(ship, start_loc, end_loc)
        ship.in_place(self.grid)

    def is_free(self, start_loc, ship):
        """
        Check if the Anchor point is free(first IF) AND at lest 1 end
        location is possible(2nd IF).
        """
        if self.grid[start_loc[0], start_loc[1]] == 555:
            end_loc = self.find_valid_end_loc(start_loc, ship)

            if len(end_loc) >= 1:
                return end_loc
            else:
                return False
        else:
            return False

    def find_valid_end_loc(self, start_loc, ship):
        """
        With 1 Anchor point, there is a maximum of 4 possible end
        locations for 1 ship. If the spaces between anchor point and end
        point is 0 (all free) then location is valid. If the location is
        outside the gird range or there is another ship in on a grid square
        then the end location is not valid. Returns list of valid locations.
        """
        length = ship.size
        if length == 1:
            return [start_loc]

        vertical_down = 0
        vertical_up = 0
        horizontal_left = 0
        horizontal_right = 0
        valid_end_loc = []

        for i in range(length):
            if self.valid_loc(start_loc[0] + i, start_loc[1]):
                vertical_down += 1
                if vertical_down == length:
                    valid_end_loc.append([start_loc[0] + i, start_loc[1]])

            if self.valid_loc(start_loc[0] - i, start_loc[1]):
                vertical_up += 1
                if vertical_up == length:
                    valid_end_loc.append([start_loc[0] - i, start_loc[1]])

            if self.valid_loc(start_loc[0], start_loc[1] + i):
                horizontal_right += 1
                if horizontal_right == length:
                    valid_end_loc.append([start_loc[0], start_loc[1] + i])

            if self.valid_loc(start_loc[0], start_loc[1] - i):
                horizontal_left += 1
                if horizontal_left == length:
                    valid_end_loc.append([start_loc[0], start_loc[1] - i])

        return valid_end_loc

    def valid_loc(self, start_loc_y, start_loc_x):
        """
        Check if all the the grid square is inside grid and is not filled.
        :param start_loc_y [int]
        :param start_loc_x [int]
        :return: True/False
        """
        index_min = start_loc_x >= 0 and start_loc_y >= 0
        index_max = start_loc_x <= 9 and start_loc_y <= 9

        if index_min and index_max:
            if self.grid[start_loc_y, start_loc_x] == 555:
                return True
        else:
            return False



    # def __call__(self, pc, *args, **kwargs):
    #     """
    #     When the player object is called up, it will preform a turn.
    #     :param args:
    #     :param kwargs:
    #     :return: in-place
    #     """
    #     self.print_turn()
    #     salvo = get_salvo(self.my_ships)
    #     while True:
    #         hit_list, print_list = self.make_hit_list(salvo)
    #         print(print_list)
    #         confirm_shooting = input('Is this correct (Y/N) ?').lower()
    #         if confirm_shooting == "y":
    #             for hit_loc_in_list in hit_list:
    #                 self.fire_salvo(hit_loc_in_list, pc)
    #             return
    #         else:
    #             continue

    def fire_salvo(self, location, player):
        """
        Fires a single salvo, checks if it was a hit or miss. Makes the
        modifications necessary in both player and pc gird.
        :param location: [y, x] coordinates of the salvo location.
        :param player: player object to get grid info.
        :return: modify in-place.
        """
        y = location[0]
        x = location[1]
        if player.grid[y, x] == 1:
            if self.name != 'PC':
                print('Hit!!')
            self.tracking_grid[y, x] = 0
            for i in player.my_ships:
                for j in i.location:
                    if j[0] == y and j[1] == x:
                        j[2] = 0
                        i.in_place(player.grid)

        else:
            self.tracking_grid[location[0]][location[1]] = 7
            player.grid[location[0]][location[1]] = 7
            if self.name != 'PC':
                print('Miss!!')

    def print_turn(self):
        clear = lambda: os.system('cls')  # on Windows System
        clear()
        print('```````````````````````````````````````')
        print('Tracking Grid')
        print(to_dataframe(self.tracking_grid))
        print('```````````````````````````````````````')
        print('Player Grid')
        print(to_dataframe(self.grid))
        print('```````````````````````````````````````')

    def make_hit_list(self, salvo):
        """
        Receives a number of salvos that can be fired and asks the user to
        select locations.
        :param salvo:
        :return:
        """
        hit_list = []
        print_list = []

        while salvo > 0:
            print('You have {} salvos Left!'.format(salvo))
            hit_loc = input('Please select a enemy gird square you '
                            'would like to hit? (example "H2") :')
            hit_loc = hit_loc.upper()
            if valid_entry(hit_loc) is False:
                print('Invalid Entry')
                continue
            if [hit_loc] in print_list:
                print('Hit location already in list')
                continue
            hit_loc = to_numeric(hit_loc)
            condition_a = self.tracking_grid[hit_loc[0], hit_loc[1]] == 7
            condition_b = self.tracking_grid[hit_loc[0], hit_loc[1]] == 0
            if condition_a or condition_b:
                print('This gird space has been hit already!')
                continue
            print_list.append(to_alpha_numeric(hit_loc))

            hit_list.append(hit_loc)
            salvo -= 1
        return hit_list, print_list
