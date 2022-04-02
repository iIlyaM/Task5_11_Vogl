import re


class Point:

    def __init__(self, r, c):
        self.r = r
        self.c = c


class Game:

    def __init__(self, level_number):
        self.game = self.get_level(level_number)
        self.field_size = len(self.game)

    @staticmethod
    def get_level(num: int) -> list[list: int]:
        ball_positions = list()

        with open(f"levels/{num}") as file_object:
            lines = file_object.readlines()
        lines = filter(lambda x: x.strip(), lines)
        for line in lines:
            ball_positions.append(list(map(float, re.split('; |, | |,', line))))

        return ball_positions

    def in_field_range(self, row, col) -> bool:
        return 0 < row < self.field_size and 0 < col < self.field_size

    def get_possible_moves(self, curr_pos: Point):
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
                temp_cell = self.game[row][col]
                if self.in_field_range(row, col) and temp_cell == 1:
                    temp_cell = self.game[next_r][next_c]
                    if self.in_field_range(next_r, next_c) and temp_cell == 0:
                        possible_moves.add(Point(next_r, next_c))

        return possible_moves

    def make_move(self, curr_pos: Point):
        # todo  Доделать совершения хода, продумать остаток логики
        return  None
