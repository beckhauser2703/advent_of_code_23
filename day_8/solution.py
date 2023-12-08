from typing import List, Tuple, Dict


def parse_input(input: str) -> Tuple[str, Dict[str, List[str]]]:
    split_input = input.split("\n")
    network_dictionary = {}
    instructions = split_input[0]
    for line in split_input[2:]:
        split_line = line.split(" = ")
        key = split_line[0]
        left, right = split_line[1][1:-1].split(", ")
        network_dictionary[key] = [left, right]
    return instructions, network_dictionary


def number_of_steps_until_zzz(current_node: str, endpoints: List[str], directions: str, network: Dict[str, List[str]]):
    counter = 0
    while (current_node not in endpoints):
        counter += 1
        current_direction = directions[(counter - 1) % len(directions)]
        idx_from_direction = 1 if current_direction == 'R' else 0
        current_node = network[current_node][idx_from_direction]
    return counter


def solution_part_1(input: str) -> None:
    directions, network_dict = parse_input(input)
    current_node = 'AAA'
    print(number_of_steps_until_zzz(
        current_node, ['ZZZ'], directions, network_dict))


def solution_part_2(input: str) -> None:
    from math import lcm
    directions, network_dict = parse_input(input)
    endpoint_nodes = [node for node in network_dict.keys() if node[-1] == 'Z']
    array_steps_to_xxz = [number_of_steps_until_zzz(node, endpoint_nodes, directions, network_dict)
                          for node in network_dict.keys() if node[-1] == 'A']
    print(lcm(*array_steps_to_xxz))


with open(r'day_8\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
with open(r'day_8\puzzle_input.txt', 'r') as input:
    solution_part_2(input.read())
