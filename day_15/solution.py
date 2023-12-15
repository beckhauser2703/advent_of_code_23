from typing import List, Tuple, Dict
from enum import Enum, auto


def hash_word(word: str) -> int:
    current_value = 0
    for char in word:
        current_value += ord(char)
        current_value *= 17
        current_value = current_value % 256
    return current_value


def solution_part_1(input: str) -> None:
    split_input = input.split(",")
    print(sum([hash_word(word) for word in split_input]))


class Lens:
    def __init__(self, label: str, focal_length: int) -> None:
        self.label = label
        self.focal_length = focal_length
        self.hash_value = hash_word(label)

    def __repr__(self):
        return f'label: {self.label}, focal_length: {self.focal_length}'

    def __eq__(self, other):
        # comparing only by label
        return self.label == other.label


def parse_instruction_and_lens(instruction_and_lens: str) -> Tuple[str, Lens]:
    if '-' in instruction_and_lens:
        label, focal_length = instruction_and_lens.split("-")
        return ('-', Lens(label, 0))
    label, focal_length = instruction_and_lens.split("=")
    return ('=', Lens(label, int(focal_length)))


def solution_part_2(input: str) -> None:
    split_input = input.split(",")
    boxes: List[List[Lens]] = [[] for _ in range(256)]
    for instruction_and_lens in split_input:
        instruction, lens = parse_instruction_and_lens(instruction_and_lens)
        is_lens_in_box = lens in boxes[lens.hash_value]
        if not is_lens_in_box and '=' in instruction:
            boxes[lens.hash_value].append(lens)
        elif is_lens_in_box and '=' in instruction:
            lens_index = boxes[lens.hash_value].index(lens)
            boxes[lens.hash_value][lens_index] = lens
        elif is_lens_in_box and '-' in instruction:
            boxes[lens.hash_value].remove(lens)
    print(sum([(box_idx + 1) * (lens_idx + 1) * lens.focal_length for
               box_idx, box in enumerate(boxes)
               for lens_idx, lens in enumerate(box)]))


with open(r'day_15\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
with open(r'day_15\puzzle_input.txt', 'r') as input:
    solution_part_2(input.read())
