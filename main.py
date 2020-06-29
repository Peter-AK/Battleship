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
from main_gui import *
import random


def check_victory(player_object):
    health = 0
    for i in player_object.my_ships:
        for j in i.location:
            health += j[2]

    if health == 0:
        return True
    else:
        return False


def new_round(name):
    """New round function that generates a new game."""
    # Player and PC class creation
    player = Player(name)
    pc = Pc('PC')
    # Random int to see who starts
    who_starts = random.randint(1, 2)
    if who_starts == 1:
        print('Player starts!!')

    # Victory flag set to False
    victory = False
    while victory is False:
        if who_starts == 1:
            player(pc)
            who_starts += 1
            if check_victory(pc):
                victory = True
                print('Player WINS!!!')

        elif who_starts == 2:
            pc(player)
            who_starts -= 1
            if check_victory(pc):
                victory = True
                print('PC WINS!!!')

        elif who_starts == 'exit':
            return True


if __name__ == '__main__':
    game_exit = False
    intro_text()
    while game_exit is False:
        game_exit = new_round('player')

