from typing import List, Tuple, Dict
import numpy as np

Grid = List[List[str]] | np.ndarray


def move_col_north(grid: Grid, col: int) -> int:
    last_obstacle_row = -1
    answer = 0
    for row in range(len(grid)):
        current_item = grid[row][col]
        if current_item == '.':
            continue
        if current_item == '#':
            last_obstacle_row = row
            continue
        # item can only be O
        last_obstacle_row += 1
        grid[row][col] = '.'
        grid[last_obstacle_row][col] = 'O'
        answer += (len(grid) - last_obstacle_row)
    return answer


def solution_part_1(input: str) -> None:
    split_input = [[char for char in line] for line in input.split("\n")]
    answer = 0
    for col in range(len(split_input[0])):
        answer += move_col_north(split_input, col)
    print(answer)


def move_grid_north(grid: Grid) -> int:
    grid_points = 0
    for col in range(len(grid)):
        grid_points += move_col_north(grid, col)
    return grid_points


def cycle_grid(grid: Grid) -> None:
    move_grid_north(grid)
    def rotate_270(x): return np.rot90(x, k=3)
    for _ in range(3):
        grid = rotate_270(grid)
        move_grid_north(grid)
    grid = rotate_270(grid)


def solution_part_2(input: str) -> None:
    split_input = np.array([[char for char in line]
                           for line in input.split("\n")])
    #tortoise hare if there is a cycle and exploit it if there is
    tortoise_counter = 1
    hare_counter = 2
    tortoise = split_input.copy()
    hare = split_input.copy()
    cycle_grid(tortoise)
    cycle_grid(hare)
    cycle_grid(hare)
    while not (tortoise == hare).all():
        cycle_grid(tortoise)
        cycle_grid(hare)
        cycle_grid(hare)
        tortoise_counter += 1
        hare_counter += 2
    print(tortoise_counter, hare_counter)

    tortoise = hare.copy()
    cycle_grid(tortoise)
    tortoise_counter = 1
    while not (tortoise == hare).all():
        tortoise_counter += 1
        cycle_grid(tortoise)
    for _ in range(10**9 % (tortoise_counter)):
        cycle_grid(hare)
    print(sum([len(hare) - idx for idx, line in enumerate(hare)
               for char in line if char == 'O']))


with open(r'day_14\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
with open(r'day_14\puzzle_input.txt', 'r') as input:
    solution_part_2(input.read())
