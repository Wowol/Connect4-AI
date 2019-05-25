import sys
from game import Game
from random import randint
import copy
import numpy as np
import math

PLAYER_ONE = 1
PLAYER_TWO = 2

INFINITY = sys.maxsize
MINUS_INFINITY = -INFINITY - 1

WIN = 4

q = {}


def monte_carlo_tree_search(game, player):
    q[tuple(map(tuple, game.board))] = (0, 1)
    for i in range(10):
        leaf, next_player, path = traverse(game, player)
        all_sum, all_times = expand(leaf, next_player, player)
        backpropagate(path, all_sum, all_times)


def make_bot_move(game, player):
    q.clear()
    monte_carlo_tree_search(game, player)

    max_number = -1
    max_column = -1
    for i in range(game.columns):
        if game.make_move(player, i):
            t = tuple(map(tuple, game.board))
            if t in q and q[t][1] > max_number:
                max_number = q[t][1]
                max_column = i
            game.revert_move(i)

    game.make_move(player, max_column)


def make_best_move(game, current_player):
    max_value = MINUS_INFINITY
    max_column = -1
    for i in range(game.columns):
        w = q[tuple(map(tuple, game.board))][1]
        parent_visited_times_log = 2 * math.log(w)
        if game.make_move(current_player, i):
            t = tuple(map(tuple, game.board))

            if t in q:
                avg = q[t][0] / q[t][1]
                ucb = avg + math.sqrt(parent_visited_times_log/q[t][1])
                if ucb > max_value:
                    max_value = ucb
                    max_column = i

            # if t in q and q[t][0] / q[t][1] > max_value:
            #     max_value = q[t][0] / q[t][1]
            #     max_column = i
            game.revert_move(i)

    return max_column


def backpropagate(path, all_sum, all_times):
    for x in path:
        q[x] = (q[x][0] + all_sum, q[x][1] + all_times)


def traverse(oryginal_game, player):
    game = copy_game(oryginal_game)
    current_player = player

    path = []

    while True:
        path.append(tuple(map(tuple, game.board)))
        best_column = make_best_move(game, current_player)

        if best_column == -1 or game.check_win():
            return game, current_player, path

        if best_column != -1:
            game.make_move(current_player, best_column)
            current_player = 3 - current_player


def copy_game(game):
    return Game(game.columns, game.lines, copy.deepcopy(
        game.board), copy.deepcopy(game.current_heights), game.moves)


def expand(game, player, first_player):
    all_sum = 0
    all_times = 0
    for i in range(game.columns):
        if game.make_move(player, i):
            sum_results, times = rollout(game, player, first_player)
            q[tuple(map(tuple, game.board))] = (sum_results, times)
            all_sum += sum_results
            all_times += times
            game.revert_move(i)
    return all_sum, all_times


def rollout(oryginal_game, player, first_player, times=100):
    sum_results = 0

    w = oryginal_game.check_win()
    if w:
        if w == first_player:
            return times, times
        elif w == 3 - first_player:
            return -times, times
        else:
            return 0, times

    for i in range(times):
        # print("--------------------------------------------")
        current_player = player

        game = copy_game(oryginal_game)

        while True:
            while True:
                r = randint(0, game.columns - 1)
                if game.make_move(current_player, r):
                    break
            current_player = 3-current_player
            w = game.check_win()
            # print(game)
            if w:
                if w == first_player:
                    sum_results += 1
                elif w == 3 - first_player:
                    sum_results -= 1
                break

    return sum_results, times


# g = Game(7, 6)

# # print(monte_carlo_tree_search(g, 1))

# while(True):
#     print(make_bot_move(g, 1))

#     print(g)

#     print(make_bot_move(g, 2))
#     print(g)


# print(make_bot_move(g, 1))
# print(g)


# print(make_bot_move(g, 2))


# print(g)

# for k, v in q.items():
#     print(k, v)
