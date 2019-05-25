import sys
from game import Game
from alpha_beta import make_bot_move as ab_bot
from mcts import make_bot_move as mcts_bot


def play():
    game = Game(7, 6)

    while not game.check_win():
        mcts_bot(game, 1)

        print(game)

        if game.check_win():
            break

        # i = int(input())
        # game.make_move(2, i)

        ab_bot(game, 2)

        print(game)

    print(game.check_win())


play()
