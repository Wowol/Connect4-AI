import sys
from game import Game
from alpha_beta import make_bot_move


def play():
    game = Game(7, 6)

    while not game.check_win():

        make_bot_move(game, 1)

        print(game)

        if game.check_win():
            break

        # i = int(input())
        # game.make_move(2, i)

        make_bot_move(game, 2)

        print(game)

    print(game.check_win())


play()
