import numpy as np


def valid_entry(entry):
    """
    Checks if an entry is a valid one.
    """
    valid_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    condition_a = len(entry) == 2
    condition_b = entry[0] in valid_list
    condition_c = 1 <= int(entry[1]) <= 10

    if condition_a and condition_b and condition_c:
        return True


def to_alpha_numeric(entry):
    """
    Transforms a grid position into a matrix position (IE: A3 --> [0, 3]
    """
    grid_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G',
            7: 'H', 8: 'I', 9: 'J'}
    # Columns then rows
    entry = [grid_dict[entry[1]] + str(entry[0] + 1)]
    return entry


def to_numeric(entry):
    """
        Transforms a grid position into a matrix position (IE: A3 --> [0, 3]
        """
    grid_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6,
                 'H': 7, 'I': 8, 'J': 9}
    # Columns then rows
    entry = [int(entry[1]) - 1, grid_dict[entry[0]]]
    return entry


def select_dict(list):
    """
    Takes a list of valid locations and make a dictionary with them so the
    user can easily select an end location.
    :param list:
    :return: dictionary
    """
    my_dict_matrix = {}
    my_dict_print = {}
    for i in range(len(list)):
        my_dict_matrix[i + 1] = list[i]
        my_dict_print[i + 1] = to_alpha_numeric(list[i])
    return my_dict_matrix, my_dict_print


class Players:
    def __init__(self, name):
        self.name = name
        self.grid = np.zeros((10, 10))
        self.non_placed_ships = [
                                 ['AirCraft Carrier', 5],
                                 ['BattleShip', 4],
                                 ['Cruiser', 3],
                                 ['Destroyer', 2],
                                 ['Submarines', 3],
                                ]

    def player_setup(self):
        """
        General function for the setup phase for each player.
        """
        self.grid_setup()

    def grid_setup(self):
        """
        Prints out the grid for a visual queue, places all the ships on
        the gird
         """
        for ship in self.non_placed_ships:
            print(self.grid)

            self.place_ship(ship)

    def place_ship(self, ship):
        """
        Asks the user for an anchor point and an end point for each
        ship that has not been placed.
        """

        while True:
            start_loc = input('Please enter the anchor point '
                              'for the {ship} with a size of {size}: [example '
                              '"A3"]: '
                              .format(ship=ship[0], size=ship[1]))
            start_loc = start_loc.upper()
            if valid_entry(start_loc) is False:
                continue
            start_loc = to_numeric(start_loc)
            valid_end_loc = self.is_free(start_loc, ship)
            if valid_end_loc is False:
                continue
            valid_end_loc, print_loc = select_dict(valid_end_loc)
            print(print_loc)
            max = len(valid_end_loc)
            end_loc = input('Please enter an end point (1-{})'.format(max))
            if 1 <= int(end_loc) <= 4:
                end_loc = valid_end_loc[int(end_loc)]
                self.place_ship_on_grid(start_loc, end_loc)
                return


    def find_valid_end_loc(self, start_loc, ship):
        """
        With 1 Anchor point, there is a maximum of 4 possible end
        locations for 1 ship. If the spaces between anchor point and end
        point is 0 (all free) then location is valid. If the location is
        outside the gird range or there is another ship in on a grid square
        then the end location is not valid. Returns list of valid locations.
        """
        length = ship[1]

        vertical_down = 0
        vertical_up = 0
        horizontal_left = 0
        horizontal_right = 0
        valid_end_loc = []

        for i in range(length + 1):
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
        :param start_loc_y
        :param start_loc_x
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

    def place_ship_on_grid(self, start, end):
        """
        Once a start location and an end location was selected, do the
        actual placement on the players grid. Changes the state from 0 to 1
        on the matrix in-place.
        :param start:
        :param end:
        :return: Nothing
        """
        vertical = end[0] - start[0]
        horizontal = end[1] - start[1]

        if horizontal:
            fixed_column = start[0]
            for i in range(start[1], end[1]):
                self.grid[fixed_column][i] = 1

        if vertical:
            fixed_column = start[1]
            for i in range(start[0], end[0]):
                self.grid[fixed_column][i] = 1
