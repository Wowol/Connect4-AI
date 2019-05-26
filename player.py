from game import Game


def make_move(game, player):
    while(True):
        column = int(input())
        t = game.make_move(player, column)
        if t:
            return