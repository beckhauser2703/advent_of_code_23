from typing import List, Tuple

"""TODO: make a grid class and make it take a spot instance and return the correct item.
         I believe it'll make everything more readable"""
class Spot:
    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row

    def __repr__(self):
        return f"col: {self.col}, row: {self.row}\n"


def is_valid_symbol(symbol: str) -> bool:
    return (not symbol.isdigit()) and (symbol != '.')


def is_inbounds(spot: Spot, number_of_cols: int, number_of_rows: int) -> bool:
    if spot.col < 0 or spot.col > number_of_cols - 1:
        return False
    if spot.row < 0 or spot.row > number_of_rows - 1:
        return False
    return True


def parse_input(input: str) -> List[List[str]]:
    return [[char for char in line] for line in input.split("\n")]


def get_number_idx(line: List[str]) -> List[List[int]]:
    number_idx = []
    start_idx, end_idx = None, None
    for idx, char in enumerate(line):
        if end_idx is not None and (not char.isdigit() or (idx == len(line) - 1)):
            number_idx.append([start_idx, end_idx])
            start_idx, end_idx = None, None
            continue
        if not char.isdigit():
            continue
        if start_idx is None:
            start_idx = idx
        end_idx = idx
    if line[-1].isdigit():
        number_idx[-1][1] = len(line) - 1
    return number_idx


def is_symbol_adjacent(number_idx: List[int], line_idx: int,  grid: List[List[str]]) -> bool:
    col_start_idx, col_end_idx = number_idx[0], number_idx[1]
    adjacent_spots = [Spot(col_idx, line_idx - 1) for col_idx in range(col_start_idx - 1, col_end_idx + 2)] +\
                     [Spot(col_start_idx - 1, line_idx), Spot(col_end_idx + 1, line_idx)] +\
                     [Spot(x, line_idx + 1)
                      for x in range(col_start_idx - 1, col_end_idx + 2)]

    adjacent_spots = [spot for spot in adjacent_spots if
                      is_inbounds(spot, len(grid[0]), len(grid))]
    for spot in adjacent_spots:
        if is_valid_symbol(grid[spot.row][spot.col]):
            return True
    return False


def solution_part_1(input: str) -> None:
    soma = 0
    grid = parse_input(input)
    for row_idx, row in enumerate(grid):
        for col_idx_tuple in get_number_idx(row):
            if is_symbol_adjacent(col_idx_tuple, row_idx, grid):
                str_number = "".join(grid[row_idx][col_idx_tuple[0]:col_idx_tuple[1] + 1])
                soma += int(str_number)
    print(soma)

def get_full_number_from_idx(spot: Spot, grid: List[List[str]]) -> int:
    number_of_cols, number_of_rows = len(grid[0]), len(grid)
    left_idx, right_idx = spot.col, spot.col
    original_spot = spot
    spot = Spot(spot.col - 1, spot.row)
    #going left
    while is_inbounds(spot, number_of_cols, number_of_rows):
        if not grid[spot.row][spot.col].isdigit():
            break
        left_idx = spot.col
        spot = Spot(spot.col - 1, spot.row)
    spot = original_spot
    spot = Spot(spot.col + 1, spot.row)
    #going right
    while is_inbounds(spot, number_of_cols, number_of_rows):
        if not grid[spot.row][spot.col].isdigit():
            break
        right_idx = spot.col
        spot = Spot(spot.col + 1, spot.row)
    number_str = "".join(grid[spot.row][left_idx:right_idx+1])
    return int(number_str)


def get_gear_ratio(gear_row_idx: int, gear_col_idx: int, grid: List[List[str]]) -> int:
    number_of_cols, number_of_rows = len(grid[0]), len(grid)
    scan_up_number_idx = [Spot(gear_col_idx - 1, gear_row_idx - 1),
                          Spot(gear_col_idx, gear_row_idx - 1),
                          Spot(gear_col_idx + 1, gear_row_idx - 1)]
    scan_left_number_idx = [Spot(gear_col_idx - 1, gear_row_idx)]
    scan_right_number_idx = [Spot(gear_col_idx + 1, gear_row_idx)]
    scan_down_number_idx = [Spot(gear_col_idx - 1, gear_row_idx + 1),
                            Spot(gear_col_idx, gear_row_idx + 1),
                            Spot(gear_col_idx + 1, gear_row_idx + 1)]
    scan_all_directions = [scan_up_number_idx,
                           scan_left_number_idx,
                           scan_right_number_idx,
                           scan_down_number_idx]
    number_idx = []
    #TODO: can be cleaner
    """checks all directions and if it's up or down checks if it's one number or two.
    It does this by checking if the middle index is None or not:
    If it is, then there may be two numbers so we keep both index
    If not we only keep the middle one as there is only one number and the middle one index
    is enough to get it"""
    for direction in scan_all_directions:
        direction_idx = []
        for spot in direction:
            if not is_inbounds(spot, number_of_cols, number_of_rows):
                direction_idx.append(None)
                continue
            if grid[spot.row][spot.col].isdigit():
                direction_idx.append(spot)
            else:
                direction_idx.append(None)

        if len(direction_idx) == 3:
            if direction_idx[1] is None:
                direction_idx = [direction_idx[0], direction_idx[2]]
            else:
                direction_idx = [direction_idx[1]]
    
        number_idx += [direction for direction in direction_idx\
                       if direction is not None]
    if len(number_idx) != 2:
        return 0
    first_number = get_full_number_from_idx(number_idx[0], grid)
    second_number = get_full_number_from_idx(number_idx[1], grid)
    return first_number*second_number


def solution_part_2(input: str) -> None:
    soma = 0
    grid = parse_input(input)
    for row_idx, row in enumerate(grid):
        for col_idx, item in enumerate(row):
            if item == '*':
                soma += get_gear_ratio(row_idx, col_idx, grid)
    print(soma)

with open(r'day_3\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
    solution_part_2(input.read())
