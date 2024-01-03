from typing import List, Tuple, Dict
from copy import deepcopy

class Part:
    def __init__(self, input: str):
        x, m, a, s = [input.split("=") for input in input.split(",")]
        self.x = int(x[1])
        self.m = int(m[1])
        self.a = int(a[1])
        self.s = int(s[1][:-1])

    def __repr__(self) -> str:
        return f'x: {self.x}, a: {self.a}, m: {self.m}, s: {self.s}'

    def get_sum(self) -> int:
        return self.x + self.m + self.a + self.s


def get_category(char: str, part: Part) -> int:
    match char:
        case 'x':
            return int(part.x)
        case 'm':
            return int(part.m)
        case 'a':
            return int(part.a)
        case 's':
            return int(part.s)
        case _:
            raise RuntimeError("Should be unreachable")


class Rule:
    def __init__(self, preparse_rule: str) -> None:
        import re
        self.preparse_rule = preparse_rule
        if '>' not in self.preparse_rule and '<' not in self.preparse_rule:
            self.category_char, self.str_number = None, None
            self.destination = preparse_rule
            return
        if '>' in self.preparse_rule:
            self.inequality = 'gt'
        else:
            self.inequality = 'lt'
        self.category_char, self.str_number, self.destination = re.split(
            "[<>:]", self.preparse_rule)
        self.number = int(self.str_number)

    def __repr__(self) -> str:
        if self.category_char is not None:
            return f'{self.category_char} {self.inequality} {self.number}:{self.destination}'
        return f'{self.destination}'

    def apply_rule(self, part: Part) -> bool:
        if self.category_char is None or self.number is None:
            return True
        relevant_category = get_category(self.category_char, part)
        if self.inequality == 'gt':
            return relevant_category > self.number
        return relevant_category < self.number


def solve(from_workflow_to_rules: Dict[str, List[Rule]], starting_workflow: str, part: Part) -> bool:
    current_workflow = starting_workflow
    rules = from_workflow_to_rules[current_workflow]
    for rule in rules:
        if (not rule.apply_rule(part)):
            continue
        destination = rule.destination
        if destination in ['A', 'R']:
            return destination == 'A'
        return solve(from_workflow_to_rules, destination, part)
    raise RuntimeError('Should be unreachable')


def solution_part_1(input: str) -> None:
    from_workflow_to_rules: Dict[str, List[Rule]] = {}
    workflows, str_parts = [input.split("\n") for input in input.split("\n\n")]
    parts = [Part(str_part) for str_part in str_parts]
    final_sum = 0
    for workflow in workflows:
        workflow_name, preparse_rules = workflow.split('{')
        preparse_rules = preparse_rules[:-1]
        rules = [Rule(preparse_rule)
                 for preparse_rule in preparse_rules.split(',')]
        from_workflow_to_rules[workflow_name] = rules
    for part in parts:
        is_approved = solve(from_workflow_to_rules, 'in', part)
        if is_approved:
            final_sum += part.get_sum()
    print(final_sum)


def solve_part_2(min_max_dict: Dict[str, List[int]], current_workflow: str, 
                 from_workflow_to_rules: Dict[str, List[Rule]]) -> List[Dict[str, List[int]]]:
    min_max_dict = deepcopy(min_max_dict)
    min_max_dicts_list = []
    if current_workflow == 'A':
        return [min_max_dict]
    if current_workflow == 'R':
        return []
    rules = from_workflow_to_rules[current_workflow]
    for rule in rules:
        if rule.category_char is None:
            min_max_dicts_list.extend(solve_part_2(min_max_dict, rule.destination, from_workflow_to_rules))
            continue
        if rule.inequality == 'gt':
            tmp_dict = deepcopy(min_max_dict)
            if rule.category_char is None:
                continue
            #gt branch
            current_min_in_category = tmp_dict[rule.category_char][0]
            tmp_dict[rule.category_char][0] = max([current_min_in_category, rule.number + 1])
            min_max_dicts_list.extend(solve_part_2(tmp_dict, rule.destination, from_workflow_to_rules))
            #lt branch
            current_max_in_category = min_max_dict[rule.category_char][1]
            min_max_dict[rule.category_char][1] = min(rule.number, current_max_in_category)
        elif rule.inequality == 'lt':
            tmp_dict = deepcopy(min_max_dict)
            if rule.category_char is None:
                continue
            #lt branch
            current_min_in_category = tmp_dict[rule.category_char][1]
            tmp_dict[rule.category_char][1] = min([current_min_in_category, rule.number - 1])
            min_max_dicts_list.extend(solve_part_2(tmp_dict, rule.destination, from_workflow_to_rules))
            #gt branch
            current_max_in_category = min_max_dict[rule.category_char][0]
            min_max_dict[rule.category_char][0] = max(rule.number, current_max_in_category)
    return min_max_dicts_list


def solution_part_2(input: str) -> None:
    from_workflow_to_rules: Dict[str, List[Rule]] = {}
    workflows, _ = [input.split("\n") for input in input.split("\n\n")]
    rules: List[Rule] = []
    for workflow in workflows:
        workflow_name, preparse_rules = workflow.split('{')
        preparse_rules = preparse_rules[:-1]
        rules = [Rule(preparse_rule)
                 for preparse_rule in preparse_rules.split(',')]
        from_workflow_to_rules[workflow_name] = rules
    min_max_dict = {
        'x': [1, 4000],
        'm': [1, 4000],
        'a': [1, 4000],
        's': [1, 4000],
    }
    min_max_dicts = (solve_part_2(min_max_dict, 'in', from_workflow_to_rules))
    result = 0
    for mm_dict in min_max_dicts:
        number_of_possible_parts = 1
        for v in mm_dict.values():
            number_of_possible_parts *= (v[1] - v[0] + 1)
        result += number_of_possible_parts
    print(result)
    

with open(r'day_19\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
with open(r'day_19\puzzle_input.txt', 'r') as input:
    solution_part_2(input.read())
