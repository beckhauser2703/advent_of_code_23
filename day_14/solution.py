from typing import List, Tuple, Dict

def move_col_north(grid: List[List[str]], col: int) -> int:
    last_obstacle_row = -1
    answer = 0
    for row in range(len(grid)):
        current_item = grid[row][col]
        if current_item == '.':
            continue
        if current_item == '#':
            last_obstacle_row = row
            continue
        #item can only be O
        grid[row][col] = '.'
        last_obstacle_row += 1
        grid[last_obstacle_row][col] = 'O'
        answer += (len(grid) - last_obstacle_row)
    return answer


def solution_part_1(input: str) -> None:
    split_input = [[char for char in line] for line in input.split("\n")]
    answer = 0
    for col in range(len(split_input[0])):
        answer += move_col_north(split_input, col)
    print(answer)


def solution_part_2(input: str) -> None:
    ...


with open(r'day_14\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
# with open(r'day_14\puzzle_input.txt', 'r') as input:
#     solution_part_2(input.read())
