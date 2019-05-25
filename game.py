
PLAYER_ONE = 1
PLAYER_TWO = 2

DEPTH = 1

WIN = 4


class Game:

    def __init__(self, columns, lines, board=None, current_heights=None, moves = 0):
        self.moves = moves
        self.columns = columns
        self.lines = lines
        self.board = board if board is not None else [
            [0 for i in range(columns)] for j in range(lines)]
        self.current_heights = current_heights if current_heights is not None else [
            0 for i in range(columns)]

    def make_move(self, player, column):
        if self.current_heights[column] == self.lines:
            return None

        self.board[self.lines -
                   self.current_heights[column] - 1][column] = player
        self.current_heights[column] += 1

        self.moves += 1

        return True

    def revert_move(self, column):
        self.board[self.lines -
                   self.current_heights[column]][column] = 0
        self.current_heights[column] -= 1
        self.moves -= 1

    def _check_win_in_array(arr):
        for x in range(len(arr) - WIN + 1):
            if (arr[x] == PLAYER_ONE or arr[x] == PLAYER_TWO):
                lst = arr[x:x+WIN]
                if lst.count(lst[0]) == len(lst):
                    return arr[x]
        return None

    def _check_line_win(self):
        for line in self.board:
            k = Game._check_win_in_array(line)
            if k:
                return k
        return None

    def _check_column_win(self):
        for c in range(self.columns):
            column = [row[c] for row in self.board]
            k = Game._check_win_in_array(column)
            if k:
                return k
        return None

    def _check_diagonal_win(self, right_up):
        q = 0 if right_up else WIN - 1
        w = self.columns - WIN + 1 if right_up else self.columns
        e = 1 if right_up else -1
        for line in range(WIN - 1, self.lines):
            for column in range(q, w):
                arr = [self.board[line-i]
                       [column+(i*e)] for i in range(0, WIN)]
                k = Game._check_win_in_array(arr)
                if k:
                    return k
        return None

    def check_win(self):
        if self.moves == self.lines * self.columns:
            return 3
        return self._check_line_win() or self._check_column_win() or self._check_diagonal_win(False) or self._check_diagonal_win(True)

    def __str__(self):
        s = ''.join(['{:4}'.format(str(i))
                     for i in range(len(self.board) + 1)]) + '\n'
        s += ''.join(['{:4}'.format('|')
                      for i in range(len(self.board) + 1)]) + '\n'

        s += '\n'.join([''.join(['{:4}'.format(str(item) if item > 0 else '-')
                                 for item in row]) for row in self.board])
        s += '\n'
        return s
