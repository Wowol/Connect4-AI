import sys
from game import Game
from alpha_beta import make_bot_move as ab_bot, set_depth as minmax_set_depth
from mcts import make_bot_move as mcts_bot, set_roullout_times as mcts_set_roullout_times, set_expand_time as mcts_set_expand_time
from player import make_move as player_move
import argparse


players = {"mcts": mcts_bot, "monte_carlo_tree_search": mcts_bot, "montecarlotreesearch": mcts_bot, "alpha_beta": ab_bot,
           "minimax": ab_bot, "alphabeta": ab_bot, "mini_max": ab_bot, "human": player_move, "player": player_move}

parser = argparse.ArgumentParser(
    description='Connect4 AI')

parser.add_argument('first', type=str,
                    help='First player (human, mcts or minimax)')
parser.add_argument('second', type=str,
                    help='Second player (human, mcts or minimax)')
parser.add_argument('-d', '--depth', type=int, default=4,
                    help='Depth of the minimax tree')
parser.add_argument('-t', '--time', type=float, default=8,
                    help='Time of expanding tree in mcts algorithm')
parser.add_argument('-r', '--rollout', type=int, default=1,
                    help='How many times do the rollout in mcts algorithm')
parser.add_argument('-s', '--statistics', action='store_true',
                    default=False, help='Make statistics of bots')

args = parser.parse_args()


minmax_set_depth(args.depth)
mcts_set_roullout_times(args.rollout)
mcts_set_expand_time(args.time)

first_bot = None
second_bot = None
for name, fun in players.items():
    if name.lower().startswith(args.first.lower()):
        first_bot = fun
    if name.lower().startswith(args.second.lower()):
        second_bot = fun


def play(p=True):
    game = Game(7, 6)

    while not game.check_win():
        first_bot(game, 1)
        if p:
            print(game)
        if game.check_win():
            break
        second_bot(game, 2)
        if p:
            print(game)

    w = game.check_win()
    if w == 3:
        return 0
    else:
        return w


if args.statistics:
    results = {0: 0, 1: 0, 2: 0}
    for i in range(0, 10):
        results[play(False)] += 1

    print("DRAW: ", results[0])
    print(args.first, results[1])
    print(args.second, results[2])



else:
    play()
