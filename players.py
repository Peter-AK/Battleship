import numpy as np


class Players:
    def __init__(self, name):
        self.name = name
        self.gird = np.zeros((10, 10))
        self.non_placed_ships = [
                                1*['AirCraft Carrier', 5],
                                1*['BattleShip', 4],
                                1*['Cruiser', 3],
                                2*['Destroyer', 2],
                                2*['Submarines', 1],
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
            condition_a = len(start_loc) == 2
            condition_b = start_loc
            if start_loc
        end_loc = find_valid_end_loc(ship, start_loc)

    def find_valid_end_loc(self, ship, start_loc):
        pass