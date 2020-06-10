from players import Player
from static_func import *
import random


class Pc(Player):

    def place_ship(self, ship):
        """
        Asks the user for an anchor point and an end point for each
        ship that has not been placed.
        """
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)

            start_loc = [y, x]
            valid_end_loc = self.is_free(start_loc, ship)
            if valid_end_loc is False:
                continue

            valid_end_loc = select_dict(valid_end_loc)[0]

            max_end_points = len(valid_end_loc)
            end_loc = random.randint(1, max_end_points)
            end_loc = valid_end_entry(end_loc, max_end_points, valid_end_loc)
            if end_loc[0]:
                place_ship_on_grid(ship, start_loc, end_loc[1])
                ship.in_place(self.grid)
                return
