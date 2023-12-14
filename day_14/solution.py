from typing import List, Tuple, Dict

def move_north(grid: List[List[str]]) -> None:
    return

def solution_part_1(input: str) -> None:
    split_input = [[char for char in line] for line in input.split("\n")]
    answer = 0
    for col in range(len(split_input[0])):
        last_obstacle_row = -1
        for row in range(len(split_input)):
            current_item = split_input[row][col]
            if current_item == '.':
                continue
            if current_item == '#':
                last_obstacle_row = row
                continue
            #item can only be O
            split_input[row][col] = '.'
            last_obstacle_row += 1
            split_input[last_obstacle_row][col] = 'O'
            answer += (len(split_input) - last_obstacle_row)
    print(answer)


def solution_part_2(input: str) -> None:
    ...


with open(r'day_14\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
# with open(r'day_14\puzzle_input.txt', 'r') as input:
#     solution_part_2(input.read())
