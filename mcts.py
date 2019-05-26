import sys
from game import Game
from random import randint
import copy
import numpy as np
import math
import time


PLAYER_ONE = 1
PLAYER_TWO = 2

INFINITY = sys.maxsize
MINUS_INFINITY = -INFINITY - 1

WIN = 4

ROLLOUT_TIMES = 1
EXPAND_TIME_SECONDS = 1

q = {}

def set_roullout_times(new):
    global ROLLOUT_TIMES
    ROLLOUT_TIMES = new

def set_expand_time(new):
    global EXPAND_TIME_SECONDS
    EXPAND_TIME_SECONDS = new

def monte_carlo_tree_search(game, player):
    q[tuple(map(tuple, game.board))] = (0, 1)
    start = time.time()
    while True:
        for i in range(10):
            leaf, next_player, path = traverse(game, player)
            all_wins, all_loses, all_draws, all_times = expand(
                leaf, next_player, player)
            backpropagate(path, all_wins, all_loses,
                        all_times, player, next_player)
        if time.time() - start > EXPAND_TIME_SECONDS:
            break

def backpropagate(path, all_wins, all_loses, all_times, first_player, last_player):
    for i in range(len(path)):
        if i % 2:
            k = all_wins
        else:
            k = all_loses
        q[path[i]] = (q[path[i]][0] + k, q[path[i]][1] + all_times)


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
                ucb = avg + 2 * math.sqrt(parent_visited_times_log/q[t][1])
                if ucb > max_value:
                    max_value = ucb
                    max_column = i

            game.revert_move(i)

    return max_column


def traverse(oryginal_game, player):
    game = copy_game(oryginal_game)
    current_player = player

    path = []

    while True:
        path.append(tuple(map(tuple, game.board)))
        best_column = make_best_move(game, current_player)

        if best_column == -1:
            return game, current_player, path

        if best_column != -1:
            game.make_move(current_player, best_column)
            current_player = 3 - current_player


def copy_game(game):
    return Game(game.columns, game.lines, copy.deepcopy(
        game.board), copy.deepcopy(game.current_heights), game.moves)


def expand(game, player, first_player):
    all_wins = 0
    all_loses = 0
    all_draw = 0
    all_times = 0

    w = game.check_win()
    if w == first_player:
        return ROLLOUT_TIMES*7, 0, 0, ROLLOUT_TIMES*7
    elif w == 3 - first_player:
        return 0, ROLLOUT_TIMES*7, 0, ROLLOUT_TIMES*7

    for i in range(game.columns):
        if game.make_move(player, i):
            sum_wins, sum_loses, sum_draws, times = rollout(
                game, 3 - player, first_player, ROLLOUT_TIMES)
            q[tuple(map(tuple, game.board))] = (sum_wins, times)
            all_wins += sum_wins
            all_loses += sum_loses
            all_draw += sum_draws
            all_times += times
            game.revert_move(i)
    return all_wins, all_loses, all_draw, all_times


def rollout(oryginal_game, player, first_player, times):
    sum_wins = 0
    sum_draws = 0
    sum_loses = 0

    w = oryginal_game.check_win()
    if w:
        if w == first_player:
            return times, 0, 0, times
        elif w == 3 - first_player:
            return 0, times, 0, times
        else:
            return 0, 0, times, times

    for i in range(times):
        current_player = player

        game = copy_game(oryginal_game)

        while True:
            while True:
                r = randint(0, game.columns - 1)
                if game.make_move(current_player, r):
                    break
            current_player = 3-current_player
            w = game.check_win()
            if w:
                if w == first_player:
                    sum_wins += 1
                elif w == 3 - first_player:
                    sum_loses += 1
                else:
                    sum_draws += 1
                break

    return sum_wins, sum_loses, sum_draws, times
