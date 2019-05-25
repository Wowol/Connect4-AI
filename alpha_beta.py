import sys
from game import Game

PLAYER_ONE = 1
PLAYER_TWO = 2

WIN = 4

DEPTH = 1

INFINITY = sys.maxsize
MINUS_INFINITY = -INFINITY - 1

results = [
    [0, 0, 0, -50, -512],
    [1, 0, 0, -10, -512],
    [10, 0, 0, -1, -512],
    [50, 0, 0, 0, -512],
    [512, 512, 512, 512, 512]
]


def _get_result(l, player):
    global results
    my_result = l.count(player)
    enemy_result = l.count(3-player)

    return results[my_result][enemy_result]


def _get_diagonal_result(game, right_up, player):
    result = 0
    for line in range(WIN - 1, game.lines):
        for column in range(0 if right_up else WIN - 1, game.columns - WIN + 1 if right_up else game.columns):
            arr = [game.board[line-i]
                   [column+(i if right_up else -i)] for i in range(0, WIN)]
            result += _get_result(arr, player)
    return result


def _get_columns_result(game, player):
    result = 0
    for c in range(game.columns):
        column = [row[c] for row in game.board]
        for k in range(game.lines - WIN + 1):
            result += _get_result(column[k:k + WIN], player)
    return result


def _get_line_result(game, player):
    result = 0
    for line in game.board:
        for k in range(game.columns - WIN + 1):
            result += _get_result(line[k:k + WIN], player)

    return result


def evaluateContent(game, player):
    win = game.check_win()
    if win == player:
        return 512
    elif win == 3:
        return 0
    elif win != None:
        return -512

    return _get_line_result(game, player) + _get_columns_result(game, player) + _get_diagonal_result(game, True, player) + _get_diagonal_result(game, False, player)


def alpha_beta(game, maximizing_player, player, last_move,  depth=DEPTH, alpha=MINUS_INFINITY, beta=INFINITY):
    value = 0

    if depth == 0 or (game.moves >= 8 and game.check_win()):
        value = (1 if maximizing_player else -1) * \
            evaluateContent(game, player)

    else:
        if maximizing_player:
            value = MINUS_INFINITY

            for i in range(game.columns):
                if game.make_move(player, i):
                    value = max(value, alpha_beta(
                        game, False, 3-player, i, depth - 1, alpha, beta))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break  # cut-off

        else:
            value = INFINITY

            for i in range(game.columns):
                if game.make_move(player, i):
                    value = min(value, alpha_beta(
                        game, True, 3-player, i, depth - 1, alpha, beta))
                    beta = min(beta, value)
                    if alpha >= beta:
                        break  # cut-off

    if last_move != -1:
        game.revert_move(last_move)
    return value


def make_bot_move(game, player):
    values = {}
    for i in range(game.columns):
        if game.make_move(player, i):
            values[i] = alpha_beta(
                game, False, 3-player, i)

    best_move = max(values, key=values.get)
    game.make_move(player, best_move)
