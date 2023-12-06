from typing import List, Tuple, Optional
from math import floor, ceil

def parse_input_part_1(input: str) -> List[Tuple[int, int]]:
    split_input = input.split("\n")
    time_limit_array = split_input[0].split(":")[1].split()
    time_limit_array = [int(x) for x in time_limit_array]
    record_array = split_input[1].split(":")[1].split()
    record_array = [int(x) for x in record_array]
    return list(zip(time_limit_array, record_array))


def solve_2nd_degree_pol(a: float, b: float, c: float) -> Tuple[Optional[float], Optional[float]]:
    delta = b**2 - 4*a*c
    if delta < 0:
        return (None, None)
    x1 = (-b + delta**0.5)/-2
    x2 = (-b - delta**0.5)/-2
    return (x1, x2)


def get_ints_between_roots(roots: Tuple[Optional[float], Optional[float]]) -> int:
    x1, x2 = roots
    if x1 is None or x2 is None or x1 == x2:
        return 0
    if max(x1, x2) == x1:
        x1 = ceil(x1)
        x2 = floor(x2)
    else:
        x1 = floor(x1)
        x2 = ceil(x2)
    number_of_ints = abs(x1 - x2) - 1
    return number_of_ints


def solution_part_1(input: str) -> None:
    """
        v*t' -> total distance traveled is velocity times the time actually running
        v = 1*x -> velocity is 1 times x milliseconds pressing the button
        t' = t - x -> time running is total time minus x

        x(t-x) > record

        -x**2 + x*t > record

        -x**2 + x*t - record > 0
    """
    
    result = 1
    time_and_record_list: List[Tuple[int, int]] = parse_input_part_1(input)
    for time_and_record in time_and_record_list:
        time, record = time_and_record[0], time_and_record[1]
        roots = solve_2nd_degree_pol(-1, time, -record)
        ways_to_beat_race = get_ints_between_roots(roots)
        if ways_to_beat_race:
            result *= ways_to_beat_race
    print(result)
        
        
def parse_input_part_2(input: str) -> Tuple[int, int]:
    split_input = input.split("\n")
    time_limit = split_input[0].split(":")[1].split()
    time_limit = int("".join([x for x in time_limit]))
    record = split_input[1].split(":")[1].split()
    record = int("".join([x for x in record]))
    return (time_limit, record)


def solution_part_2(input: str) -> None:
    time_limit, record = parse_input_part_2(input)
    roots = solve_2nd_degree_pol(-1, time_limit, -record)
    print(get_ints_between_roots(roots))


with open(r'day_6\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
with open(r'day_6\puzzle_input.txt', 'r') as input:
    solution_part_2(input.read())
