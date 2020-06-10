import numpy as np
from static_func import *
from ships import Ship


class Player:
    def __init__(self, name):
        self.name = name
        self.grid = np.zeros((10, 10))
        self.enemy_gird = np.zeros((10, 10))
        self.non_placed_ships = [
                                 ['AirCraft Carrier', 5],
                                 ['BattleShip', 4],
                                 ['Cruiser', 3],
                                 ['Destroyer-A', 2],
                                 ['Destroyer-B', 2],
                                 ['Submarine-A', 1],
                                 ['Submarines-B', 1]
                                ]
        self.my_ships = [Ship(ship[0], ship[1]) for ship in
                         self.non_placed_ships]
        self.grid_setup()

    # def __call__(self, pc, *args, **kwargs):
    #     """
    #     When the player object is called up, it will preform a turn.
    #     :param args:
    #     :param kwargs:
    #     :return: in-place
    #     """
    #     salvo = len(self.ships_alive)
    #     while salvo > 0:
    #         print('You have {} salvos Left!'.format(salvo))
    #         hit_loc = input('Please select a enemy gird square you would like '
    #                      'to hit? (example "H2") :')
    #         hit_loc = hit_loc.upper()
    #         if valid_entry(hit_loc) is False:
    #             continue
    #         hit_loc = to_numeric(hit_loc)
    #         if pc.grid[hit_loc[0]][hit_loc[1]] == 1:
    #             print('HIT!!')
    #         elif pc.grid[hit_loc[0]][hit_loc[1]] == 0:
    #             print('MISS!!')
    #     return

    def grid_setup(self):
        """
        Prints out the grid for a visual queue, places all the ships on
        the gird
         """
        for ship in self.my_ships:
            grid = to_dataframe(self.grid)
            print(grid)
            self.place_ship(ship)

        print("Final Grid is:")
        grid = to_dataframe(self.grid)
        print(grid)

    def place_ship(self, ship):
        """
        Asks the user for an anchor point and an end point for each
        ship that has not been placed.
        """
        while True:
            start_loc = input('Please enter the anchor point '
                              'for the \n {name} with a size of {size}: ['
                              'example "A3"]: '
                              .format(name=ship.name, size=ship.size))
            start_loc = start_loc.upper()
            if valid_entry(start_loc) is False:
                print('Invalid entry, please try again!')
                continue

            start_loc = to_numeric(start_loc)
            valid_end_loc = self.is_free(start_loc, ship)
            if valid_end_loc is False:
                print('Invalid entry, please try again!')
                continue

            valid_end_loc, print_loc = select_dict(valid_end_loc)
            print(print_loc)
            max_end_points = len(valid_end_loc)
            end_loc = input('Please enter an end point (1-{})'.format(
                            max_end_points))
            end_loc = valid_end_entry(end_loc, max_end_points, valid_end_loc)
            if end_loc[0]:
                place_ship_on_grid(ship, start_loc, end_loc[1])
                ship.in_place(self.grid)
                return

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
            if self.grid[start_loc_y, start_loc_x] == 0:
                return True
        else:
            return False

    def is_free(self, start_loc, ship):
        """
        Check if the Anchor point is free(first IF) AND at lest 1 end
        location is possible(2nd IF).
        """
        if self.grid[start_loc[0], start_loc[1]] == 0:
            end_loc = self.find_valid_end_loc(start_loc, ship)

            if len(end_loc) >= 1:
                return end_loc
            else:
                return False
        else:
            return False
