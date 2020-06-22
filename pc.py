from players import Player
from static_func import *
import random


class Pc(Player):
    def __call__(self, player, *args, **kwargs):
        """
        When the player object is called up, it will preform a turn.
        :param args:
        :param kwargs:
        :return: in-place
        """
        salvo = get_salvo(self.my_ships)
        while True:
            hit_list = self.make_hit_list(salvo)
            for hit_loc_in_list in hit_list:
                self.fire_salvo(hit_loc_in_list, player)
            return

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

    def make_hit_list(self, salvo):
        """
        Receives a number of salvos that can be fired and asks the user to
        select locations.
        :param salvo:
        :return:
        """
        hit_list = []
        while salvo > 0:
            hit_loc = [random.randint(0, 9), random.randint(0, 9)]
            if hit_loc in hit_list:
                continue
            condition_a = self.tracking_grid[hit_loc[0], hit_loc[1]] == 7
            condition_b = self.tracking_grid[hit_loc[0], hit_loc[1]] == 0
            if condition_a or condition_b:
                continue
            hit_list.append(hit_loc)
            salvo -= 1
        return hit_list
