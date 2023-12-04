from typing import Set, Sequence

def get_card_score(card: Set[str], winning_numbers: Sequence[str]) -> int:
    winning_numbers_in_card = len(card.intersection(winning_numbers))
    if not winning_numbers_in_card:
        return 0
    return 2**(winning_numbers_in_card - 1)


def solution_part_1(input: str) -> None:
    cards_score_sum = 0
    for line in input.split("\n"):
        card_and_winning_numbers = line.split(":")[1]
        card, winning_numbers = card_and_winning_numbers.split("|")
        card = set(card.split())
        winning_numbers = winning_numbers.split()
        cards_score_sum += get_card_score(card, winning_numbers)
    print(cards_score_sum)
        

def solution_part_2(input: str) -> None:
    split_input = input.split("\n")
    list_number_of_cards = [1] * len(split_input)
    final_total_number_of_cards = 0
    for card_idx, line in enumerate(split_input):
        card_and_winning_numbers = line.split(":")[1]
        card, winning_numbers = card_and_winning_numbers.split("|")
        card = set(card.split())
        winning_numbers = winning_numbers.split()
        winning_numbers_in_card = card.intersection(winning_numbers)
        final_total_number_of_cards += 1 + len(winning_numbers_in_card)*list_number_of_cards[card_idx]
        for next_card_idx in range(card_idx + 1, card_idx + len(winning_numbers_in_card) + 1):
            list_number_of_cards[next_card_idx] += 1*list_number_of_cards[card_idx]
    print(final_total_number_of_cards)


with open(r'day_4\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
with open(r'day_4\puzzle_input.txt', 'r') as input:
    solution_part_2(input.read())
