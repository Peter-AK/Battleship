"""
---------------------
BattleShip
by Peter Agalakov
---------------------

v0.1:
    initial backend build

"""
from players import Player
from pc import Pc
from static_func import intro_text
import random


def new_round(name):
    """New round function that generates a new game."""
    # Player and PC class creation
    player = Player(name)
    pc = Pc('PC')
    who_starts = random.randint(1, 2)
    victory = False

    while victory is False:
        if who_starts == 1:
            victory = player(pc)
            who_starts += 1

        elif who_starts == 2:
            victory = pc(player)
            who_starts -= 1

        elif who_starts == 'exit':
            return True


# Sets exit trigger to False, when True game will exit.
game_exit = False
intro_text()
player_name = input("Please enter your name: ")


if __name__ == '__main__':
    while game_exit is False:
        game_exit = new_round(player_name)
