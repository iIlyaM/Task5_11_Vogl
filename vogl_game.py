import re


class Point:

    def __init__(self, r, c):
        self.r = int(r)
        self.c = int(c)


class Game:

    def __init__(self, level_number):
        self.game = GameService.get_level(level_number)

    @property
    def field_size(self):
        return len(self.game)

    @property
    def balls_count(self):
        count = 0
        for i in range(self.field_size):
            count += sum(self.game[i])
        return count

    @property
    def board(self):
        return self.game


class GameService:

    @staticmethod
    def get_level(num: int) -> list[list: int]:
        ball_positions = list()

        with open(f"levels/{num}") as file_object:
            lines = file_object.readlines()
        lines = filter(lambda x: x.strip(), lines)
        for line in lines:
            ball_positions.append(list(map(int, re.split('; |, | |,', line))))

        return ball_positions

    @staticmethod
    def get_between(curr_pos: Point, target_pos: Point):
        delta_row = (target_pos.r - curr_pos.r) / 2
        delta_col = (target_pos.c - curr_pos.c) / 2

        return Point(curr_pos.r + delta_row, curr_pos.c + delta_col)

    @staticmethod
    def make_move(board: list[list: int], curr_pos: Point, target_pos: Point):
        kill_cell = GameService.get_between(curr_pos, target_pos)
        board[target_pos.r][target_pos.c] = 1
        board[curr_pos.r][curr_pos.c] = 0
        board[kill_cell.r][kill_cell.c] = 0

    @staticmethod
    def in_field_range(board, row, col) -> bool:
        return 0 <= row < len(board) and 0 <= col < len(board)

    @staticmethod
    def get_possible_moves(board: list[list: int], curr_pos: Point):
        possible_moves = set()
        deltas = [-1, 1]

        for i in range(0, 2):
            for j in deltas:
                row = next_r = curr_pos.r
                col = next_c = curr_pos.c

                if i == 0:
                    row += j
                    next_r += 2 * j
                else:
                    col += j
                    next_c += 2 * j

                if not GameService.in_field_range(board, next_r, next_c):
                    continue

                if GameService.in_field_range(board, row, col):
                    temp_cell = board[row][col]
                    if temp_cell == 1:
                        temp_cell = board[next_r][next_c]
                        if GameService.in_field_range(board, next_r, next_c) and temp_cell == 0:
                            possible_moves.add((next_r, next_c))

        return list(possible_moves)

    @staticmethod
    def is_game_over(game: Game):
        if game.balls_count == 1:
            return 'Victory'

        board = game.board

        impossible_to_move_counter = 0

        for row in range(len(board)):
            for column in range(len(board[row])):
                if board[row][column] == 1:
                    temp_point = Point(row, column)
                    if not GameService.get_possible_moves(board, temp_point):
                        impossible_to_move_counter += 1
        return 'Lose' if game.balls_count == impossible_to_move_counter else None
