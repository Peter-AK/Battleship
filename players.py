import numpy as np


def valid_entry(entry):
    valid_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    condition_a = len(entry) == 2
    condition_b = entry[0] in valid_list
    condition_c = 1 <= int(entry[1]) <= 10

    if condition_a and condition_b and condition_c:
        return True

def numeric_entry(entry):
    dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6,
            'H': 7, 'I': 8, 'J': 9}
    entry = [dict[entry[0]], int(entry[1])]
    return entry


class Players:
    def __init__(self, name):
        self.name = name
        self.gird = np.zeros((10, 10))
        self.non_placed_ships = [
                                 ['AirCraft Carrier', 5],
                                 ['BattleShip', 4],
                                 ['Cruiser', 3],
                                 ['Destroyer', 2],
                                 ['Submarines', 3],
                                ]

    def player_setup(self):
        """ General function for the setup phase for each player."""
        self.grid_setup()

    def grid_setup(self):
        """Prints out the grid for a visual queue, places all the ships on
        the gird """
        for ship in self.non_placed_ships:
            print(self.gird)
            self.place_ship(ship)

    def place_ship(self, ship):
        """Asks the user for an anchor point and an end point for each
        ship"""
        valid_start_loc = False
        valid_end_loc = False

        while valid_start_loc is False:
            start_loc = input('Please enter the anchor point '
                              'for the {ship} with a size of {size}: [example '
                              '"A3"]: '
                              .format(ship=ship[0], size=ship[1]))
            start_loc = start_loc.upper()
            if valid_entry(start_loc):
                start_loc = numeric_entry(start_loc)
                valid_start_loc = self.is_free(start_loc)


        end_loc = find_valid_end_loc(ship, start_loc)

    def find_valid_end_loc(self, ship, start_loc):
        pass

    def is_free(self, start_loc):
        pass
